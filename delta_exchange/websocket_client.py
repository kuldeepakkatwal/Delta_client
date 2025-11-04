"""
Delta Exchange WebSocket Client

This module provides a WebSocket client for real-time data streaming from Delta Exchange.
Supports both public channels (ticker, orderbook, trades) and private channels (orders, positions).
"""

import asyncio
import json
import logging
import time
from typing import Any, Callable, Dict, List, Optional, Set
from enum import Enum

try:
    import websockets
    from websockets.client import WebSocketClientProtocol
    from websockets.exceptions import WebSocketException, ConnectionClosed
except ImportError:
    raise ImportError(
        "websockets library is required for WebSocket client. "
        "Install it with: pip install websockets"
    )

from .auth import DeltaAuth
from .constants import (
    WS_BASE_URL,
    WS_CHANNEL_TICKER,
    WS_CHANNEL_ORDERBOOK,
    WS_CHANNEL_TRADES,
    WS_CHANNEL_FUNDING_RATE,
    WS_CHANNEL_MARK_PRICE,
    WS_CHANNEL_ORDERS,
    WS_CHANNEL_POSITIONS,
    WS_CHANNEL_USER_TRADES,
    WS_CHANNEL_MARGINS,
    WS_TYPE_SUBSCRIBE,
    WS_TYPE_UNSUBSCRIBE,
    WS_TYPE_AUTH,
    WS_TYPE_PING,
    WS_TYPE_PONG,
    WS_PING_INTERVAL,
    WS_RECONNECT_DELAY_INITIAL,
    WS_RECONNECT_DELAY_MAX,
    WS_RECONNECT_EXPONENTIAL_BASE,
    WS_MAX_RECONNECT_ATTEMPTS,
)
from .exceptions import WebSocketError, AuthenticationError


logger = logging.getLogger(__name__)


class ConnectionState(Enum):
    """WebSocket connection states"""
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    AUTHENTICATED = "authenticated"
    RECONNECTING = "reconnecting"
    CLOSED = "closed"


class DeltaWebSocketClient:
    """
    WebSocket client for Delta Exchange real-time data streaming.
    
    Supports:
    - Public channels: ticker, orderbook, trades, funding rate, mark price
    - Private channels: orders, positions, user trades, margins
    - Automatic reconnection with exponential backoff
    - Authentication for private channels
    - Event-based callbacks
    - Heartbeat/ping-pong for connection health
    
    Example:
        >>> async def on_ticker(data):
        ...     print(f"Ticker: {data}")
        ...
        >>> client = DeltaWebSocketClient(api_key="key", api_secret="secret")
        >>> await client.connect()
        >>> await client.subscribe_ticker(["BTCUSD"], on_ticker)
        >>> await client.run()
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        base_url: str = WS_BASE_URL,
        auto_reconnect: bool = True,
        ping_interval: int = WS_PING_INTERVAL,
    ):
        """
        Initialize WebSocket client.
        
        Args:
            api_key: API key (required for private channels)
            api_secret: API secret (required for private channels)
            base_url: WebSocket base URL
            auto_reconnect: Enable automatic reconnection
            ping_interval: Ping interval in seconds
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.auto_reconnect = auto_reconnect
        self.ping_interval = ping_interval
        
        # Authentication
        self.auth: Optional[DeltaAuth] = None
        if api_key and api_secret:
            self.auth = DeltaAuth(api_key, api_secret)
        
        # Connection state
        self._ws: Optional[WebSocketClientProtocol] = None
        self._state = ConnectionState.DISCONNECTED
        self._reconnect_attempts = 0
        self._should_reconnect = True
        
        # Subscriptions
        self._subscriptions: Dict[str, Dict[str, Any]] = {}
        self._callbacks: Dict[str, List[Callable]] = {}
        
        # Tasks
        self._receive_task: Optional[asyncio.Task] = None
        self._ping_task: Optional[asyncio.Task] = None
        
        # Message queue for handling
        self._message_queue: asyncio.Queue = asyncio.Queue()
        self._handler_task: Optional[asyncio.Task] = None
    
    # ============================================================================
    # Connection Management
    # ============================================================================
    
    async def connect(self) -> None:
        """
        Establish WebSocket connection.
        
        Raises:
            WebSocketError: If connection fails
        """
        if self._state in [ConnectionState.CONNECTED, ConnectionState.AUTHENTICATED]:
            logger.warning("Already connected")
            return
        
        self._state = ConnectionState.CONNECTING
        logger.info(f"Connecting to {self.base_url}")
        
        try:
            self._ws = await websockets.connect(
                self.base_url,
                ping_interval=None,  # We'll handle ping ourselves
                ping_timeout=None,
            )
            
            self._state = ConnectionState.CONNECTED
            self._reconnect_attempts = 0
            logger.info("Connected to Delta Exchange WebSocket")
            
            # Start background tasks
            self._receive_task = asyncio.create_task(self._receive_loop())
            self._handler_task = asyncio.create_task(self._message_handler())
            self._ping_task = asyncio.create_task(self._ping_loop())
            
            # Authenticate if credentials provided
            if self.auth:
                await self._authenticate()
            
        except Exception as e:
            self._state = ConnectionState.DISCONNECTED
            raise WebSocketError(f"Failed to connect: {e}")
    
    async def disconnect(self) -> None:
        """
        Close WebSocket connection gracefully.
        """
        logger.info("Disconnecting...")
        self._should_reconnect = False
        self._state = ConnectionState.CLOSED
        
        # Cancel background tasks
        if self._receive_task:
            self._receive_task.cancel()
        if self._handler_task:
            self._handler_task.cancel()
        if self._ping_task:
            self._ping_task.cancel()
        
        # Close WebSocket
        if self._ws:
            await self._ws.close()
            self._ws = None
        
        logger.info("Disconnected")
    
    async def _authenticate(self) -> None:
        """
        Authenticate WebSocket connection for private channels.
        
        Raises:
            AuthenticationError: If authentication fails
        """
        if not self.auth:
            raise AuthenticationError("Authentication credentials not provided")
        
        logger.info("Authenticating...")
        
        # Generate authentication payload
        auth_payload = self.auth.generate_websocket_auth_payload()
        
        # Send auth message
        message = {
            "type": WS_TYPE_AUTH,
            "payload": auth_payload
        }
        
        await self._send_message(message)
        
        # Wait for auth confirmation (we'll handle it in message handler)
        # For now, just mark as authenticated
        self._state = ConnectionState.AUTHENTICATED
        logger.info("Authentication request sent")
    
    async def _reconnect(self) -> None:
        """
        Attempt to reconnect with exponential backoff.
        """
        if not self.auto_reconnect or not self._should_reconnect:
            return
        
        if self._reconnect_attempts >= WS_MAX_RECONNECT_ATTEMPTS:
            logger.error(f"Max reconnection attempts ({WS_MAX_RECONNECT_ATTEMPTS}) reached")
            self._state = ConnectionState.CLOSED
            return
        
        self._state = ConnectionState.RECONNECTING
        self._reconnect_attempts += 1
        
        # Calculate backoff delay
        delay = min(
            WS_RECONNECT_DELAY_INITIAL * (WS_RECONNECT_EXPONENTIAL_BASE ** (self._reconnect_attempts - 1)),
            WS_RECONNECT_DELAY_MAX
        )
        
        logger.info(f"Reconnecting in {delay}s (attempt {self._reconnect_attempts}/{WS_MAX_RECONNECT_ATTEMPTS})")
        await asyncio.sleep(delay)
        
        try:
            await self.connect()
            
            # Resubscribe to all channels
            if self._subscriptions:
                logger.info("Resubscribing to channels...")
                for channel_key, sub_info in self._subscriptions.items():
                    await self._send_subscription(sub_info)
            
        except Exception as e:
            logger.error(f"Reconnection failed: {e}")
            await self._reconnect()
    
    # ============================================================================
    # Message Handling
    # ============================================================================
    
    async def _send_message(self, message: Dict[str, Any]) -> None:
        """
        Send a message to the WebSocket.
        
        Args:
            message: Message dictionary to send
            
        Raises:
            WebSocketError: If not connected or send fails
        """
        if not self._ws:
            raise WebSocketError("Not connected")
        
        try:
            await self._ws.send(json.dumps(message))
            logger.debug(f"Sent: {message}")
        except Exception as e:
            raise WebSocketError(f"Failed to send message: {e}")
    
    async def _receive_loop(self) -> None:
        """
        Background task to receive messages from WebSocket.
        """
        while self._should_reconnect and self._ws:
            try:
                message = await self._ws.recv()
                
                # Parse message
                try:
                    data = json.loads(message)
                    await self._message_queue.put(data)
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse message: {e}")
                
            except ConnectionClosed as e:
                logger.warning(f"Connection closed: {e}")
                if self.auto_reconnect:
                    await self._reconnect()
                break
            except Exception as e:
                logger.error(f"Error receiving message: {e}")
                if self.auto_reconnect:
                    await self._reconnect()
                break
    
    async def _message_handler(self) -> None:
        """
        Background task to handle received messages.
        """
        while self._should_reconnect:
            try:
                # Get message from queue
                data = await asyncio.wait_for(self._message_queue.get(), timeout=1.0)
                
                # Handle different message types
                msg_type = data.get("type")
                
                if msg_type == "pong":
                    logger.debug("Received pong")
                
                elif msg_type == "auth":
                    # Authentication response
                    success = data.get("success", False)
                    if success:
                        logger.info("Authentication successful")
                        self._state = ConnectionState.AUTHENTICATED
                    else:
                        error = data.get("error", "Unknown error")
                        logger.error(f"Authentication failed: {error}")
                
                elif msg_type in ["subscribed", "unsubscribed"]:
                    # Subscription confirmation
                    logger.info(f"Subscription confirmed: {data}")
                
                else:
                    # Data message - route to callbacks
                    await self._route_message(data)
                
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error handling message: {e}")
    
    async def _route_message(self, data: Dict[str, Any]) -> None:
        """
        Route received data to appropriate callbacks.
        
        Args:
            data: Received message data
        """
        # Try to identify the channel
        channel = data.get("type") or data.get("channel")
        
        if not channel:
            logger.warning(f"Unable to identify channel for message: {data}")
            return
        
        # Get callbacks for this channel
        callbacks = self._callbacks.get(channel, [])
        
        # Execute callbacks
        for callback in callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(data)
                else:
                    callback(data)
            except Exception as e:
                logger.error(f"Error in callback for {channel}: {e}")
    
    async def _ping_loop(self) -> None:
        """
        Background task to send periodic pings.
        """
        while self._should_reconnect and self._ws:
            try:
                await asyncio.sleep(self.ping_interval)
                
                if self._ws and self._state in [ConnectionState.CONNECTED, ConnectionState.AUTHENTICATED]:
                    message = {"type": WS_TYPE_PING}
                    await self._send_message(message)
                    logger.debug("Sent ping")
                
            except Exception as e:
                logger.error(f"Error in ping loop: {e}")
    
    # ============================================================================
    # Subscription Management
    # ============================================================================
    
    async def _send_subscription(self, sub_info: Dict[str, Any]) -> None:
        """
        Send a subscription request.
        
        Args:
            sub_info: Subscription information
        """
        message = {
            "type": WS_TYPE_SUBSCRIBE,
            "payload": {
                "channels": [sub_info["channel_config"]]
            }
        }
        await self._send_message(message)
    
    async def subscribe(
        self,
        channel_name: str,
        symbols: Optional[List[str]] = None,
        callback: Optional[Callable] = None
    ) -> None:
        """
        Subscribe to a channel.
        
        Args:
            channel_name: Channel name (e.g., "v2/ticker", "orders")
            symbols: List of symbols to subscribe to
            callback: Callback function for messages
            
        Raises:
            WebSocketError: If not connected
        """
        if self._state == ConnectionState.DISCONNECTED:
            raise WebSocketError("Not connected. Call connect() first.")
        
        # Build channel config
        channel_config: Dict[str, Any] = {"name": channel_name}
        if symbols:
            channel_config["symbols"] = symbols
        
        # Store subscription
        channel_key = f"{channel_name}:{','.join(symbols) if symbols else 'all'}"
        self._subscriptions[channel_key] = {
            "channel_name": channel_name,
            "symbols": symbols,
            "channel_config": channel_config
        }
        
        # Store callback
        if callback:
            if channel_name not in self._callbacks:
                self._callbacks[channel_name] = []
            self._callbacks[channel_name].append(callback)
        
        # Send subscription request
        await self._send_subscription(self._subscriptions[channel_key])
        
        logger.info(f"Subscribed to {channel_key}")
    
    async def unsubscribe(
        self,
        channel_name: str,
        symbols: Optional[List[str]] = None
    ) -> None:
        """
        Unsubscribe from a channel.
        
        Args:
            channel_name: Channel name
            symbols: List of symbols to unsubscribe from
        """
        channel_key = f"{channel_name}:{','.join(symbols) if symbols else 'all'}"
        
        if channel_key in self._subscriptions:
            sub_info = self._subscriptions[channel_key]
            
            message = {
                "type": WS_TYPE_UNSUBSCRIBE,
                "payload": {
                    "channels": [sub_info["channel_config"]]
                }
            }
            
            await self._send_message(message)
            del self._subscriptions[channel_key]
            
            logger.info(f"Unsubscribed from {channel_key}")
    
    # ============================================================================
    # Public Channel Subscriptions
    # ============================================================================
    
    async def subscribe_ticker(
        self,
        symbols: List[str],
        callback: Callable
    ) -> None:
        """
        Subscribe to ticker updates.
        
        Args:
            symbols: List of symbols (e.g., ["BTCUSD", "ETHUSD"])
            callback: Callback function for ticker updates
            
        Example:
            >>> async def on_ticker(data):
            ...     print(f"Ticker: {data}")
            >>> await client.subscribe_ticker(["BTCUSD"], on_ticker)
        """
        await self.subscribe(WS_CHANNEL_TICKER, symbols, callback)
    
    async def subscribe_orderbook(
        self,
        symbols: List[str],
        callback: Callable
    ) -> None:
        """
        Subscribe to orderbook updates.
        
        Args:
            symbols: List of symbols
            callback: Callback function for orderbook updates
        """
        await self.subscribe(WS_CHANNEL_ORDERBOOK, symbols, callback)
    
    async def subscribe_trades(
        self,
        symbols: List[str],
        callback: Callable
    ) -> None:
        """
        Subscribe to trade updates.
        
        Args:
            symbols: List of symbols
            callback: Callback function for trade updates
        """
        await self.subscribe(WS_CHANNEL_TRADES, symbols, callback)
    
    async def subscribe_funding_rate(
        self,
        symbols: List[str],
        callback: Callable
    ) -> None:
        """
        Subscribe to funding rate updates.
        
        Args:
            symbols: List of symbols
            callback: Callback function for funding rate updates
        """
        await self.subscribe(WS_CHANNEL_FUNDING_RATE, symbols, callback)
    
    async def subscribe_mark_price(
        self,
        symbols: List[str],
        callback: Callable
    ) -> None:
        """
        Subscribe to mark price updates.
        
        Args:
            symbols: List of symbols
            callback: Callback function for mark price updates
        """
        await self.subscribe(WS_CHANNEL_MARK_PRICE, symbols, callback)
    
    # ============================================================================
    # Private Channel Subscriptions
    # ============================================================================
    
    async def subscribe_orders(self, callback: Callable, symbols: Optional[List[str]] = None) -> None:
        """
        Subscribe to order updates (private channel).
        
        Requires authentication.
        
        Args:
            callback: Callback function for order updates
            symbols: List of symbols to monitor (e.g., ["BTCUSD", "ETHUSD"]).
                    If None, uses ["all"] to monitor all symbols.
            
        Raises:
            AuthenticationError: If not authenticated
            
        Example:
            >>> await client.subscribe_orders(on_order, ["BTCUSD"])
            >>> # Or for all symbols:
            >>> await client.subscribe_orders(on_order, ["all"])
        """
        if self._state != ConnectionState.AUTHENTICATED:
            raise AuthenticationError("Must be authenticated to subscribe to private channels")
        
        # Delta Exchange requires symbols array even for private channels
        # Use ["all"] to monitor all symbols
        if symbols is None:
            symbols = ["all"]
        
        await self.subscribe(WS_CHANNEL_ORDERS, symbols, callback)
    
    async def subscribe_positions(self, callback: Callable, symbols: Optional[List[str]] = None) -> None:
        """
        Subscribe to position updates (private channel).
        
        Requires authentication.
        
        Args:
            callback: Callback function for position updates
            symbols: List of symbols to monitor (e.g., ["BTCUSD", "ETHUSD"]).
                    If None, uses ["all"] to monitor all symbols.
        """
        if self._state != ConnectionState.AUTHENTICATED:
            raise AuthenticationError("Must be authenticated to subscribe to private channels")
        
        # Delta Exchange requires symbols array even for private channels
        if symbols is None:
            symbols = ["all"]
        
        await self.subscribe(WS_CHANNEL_POSITIONS, symbols, callback)
    
    async def subscribe_user_trades(self, callback: Callable, symbols: Optional[List[str]] = None) -> None:
        """
        Subscribe to user trade updates (private channel).
        
        Requires authentication.
        
        Args:
            callback: Callback function for trade updates
            symbols: List of symbols to monitor (e.g., ["BTCUSD", "ETHUSD"]).
                    If None, uses ["all"] to monitor all symbols.
        """
        if self._state != ConnectionState.AUTHENTICATED:
            raise AuthenticationError("Must be authenticated to subscribe to private channels")
        
        # Delta Exchange requires symbols array even for private channels
        if symbols is None:
            symbols = ["all"]
        
        await self.subscribe(WS_CHANNEL_USER_TRADES, symbols, callback)
    
    async def subscribe_margins(self, callback: Callable, symbols: Optional[List[str]] = None) -> None:
        """
        Subscribe to margin updates (private channel).
        
        Requires authentication.
        
        Args:
            callback: Callback function for margin updates
            symbols: List of symbols to monitor (e.g., ["BTCUSD", "ETHUSD"]).
                    If None, uses ["all"] to monitor all symbols.
        """
        if self._state != ConnectionState.AUTHENTICATED:
            raise AuthenticationError("Must be authenticated to subscribe to private channels")
        
        # Delta Exchange requires symbols array even for private channels
        if symbols is None:
            symbols = ["all"]
        
        await self.subscribe(WS_CHANNEL_MARGINS, symbols, callback)
    
    # ============================================================================
    # Main Loop
    # ============================================================================
    
    async def run(self) -> None:
        """
        Run the WebSocket client indefinitely.
        
        This will keep the connection alive and process messages until
        disconnect() is called or an unrecoverable error occurs.
        
        Example:
            >>> client = DeltaWebSocketClient(api_key="...", api_secret="...")
            >>> await client.connect()
            >>> await client.subscribe_ticker(["BTCUSD"], on_ticker)
            >>> await client.run()  # Runs forever
        """
        try:
            while self._should_reconnect:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("Received interrupt signal")
        finally:
            await self.disconnect()
    
    # ============================================================================
    # Properties
    # ============================================================================
    
    @property
    def is_connected(self) -> bool:
        """Check if WebSocket is connected."""
        return self._state in [ConnectionState.CONNECTED, ConnectionState.AUTHENTICATED]
    
    @property
    def is_authenticated(self) -> bool:
        """Check if WebSocket is authenticated."""
        return self._state == ConnectionState.AUTHENTICATED
    
    @property
    def state(self) -> ConnectionState:
        """Get current connection state."""
        return self._state

