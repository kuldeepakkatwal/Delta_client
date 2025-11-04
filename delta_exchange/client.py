"""
Delta Exchange REST Client

This module provides the main REST API client for Delta Exchange.
"""

import json
import time
from typing import Dict, List, Optional, Any, Union
from urllib.parse import urlencode

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .auth import DeltaAuth
from .constants import (
    REST_BASE_URL,
    DEFAULT_TIMEOUT,
    ORDERS_ENDPOINT,
    ORDERS_BY_ID_ENDPOINT,
    BATCH_ORDERS_ENDPOINT,
    BATCH_EDIT_ORDERS_ENDPOINT,
    BATCH_DELETE_ORDERS_ENDPOINT,
    POSITIONS_ENDPOINT,
    CHANGE_MARGIN_ENDPOINT,
    WALLET_BALANCES_ENDPOINT,
    PRODUCTS_ENDPOINT,
)
from .exceptions import (
    APIError,
    AuthenticationError,
    OrderError,
    RateLimitError,
    ValidationError,
    NetworkError,
)
from .models import Order, Position, Balance, Product, Fill
from .enums import OrderSide, OrderType, OrderState, TimeInForce, MMPLevel


class DeltaRestClient:
    """
    Main REST API client for Delta Exchange.
    
    This class provides methods for interacting with the Delta Exchange REST API,
    including order management, position queries, and account information.
    
    Example:
        >>> client = DeltaRestClient(api_key="your_key", api_secret="your_secret")
        >>> order = client.place_order(
        ...     symbol="BTCUSD",
        ...     side="buy",
        ...     order_type="limit_order",
        ...     size=10,
        ...     limit_price="50000"
        ... )
        >>> positions = client.get_positions()
    """
    
    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: str = REST_BASE_URL,
        timeout: tuple = DEFAULT_TIMEOUT
    ):
        """
        Initialize Delta REST Client.
        
        Args:
            api_key: Your Delta Exchange API key
            api_secret: Your Delta Exchange API secret
            base_url: Base URL for API (default: https://api.india.delta.exchange)
            timeout: Request timeout tuple (connect_timeout, read_timeout)
            
        Raises:
            AuthenticationError: If API key or secret is invalid
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        
        # Initialize authentication
        self.auth = DeltaAuth(api_key, api_secret)
        
        # Setup session with connection pooling and retries
        self.session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
    
    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make an authenticated HTTP request to the API.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            params: Query parameters
            data: Request body data
            
        Returns:
            API response as dictionary
            
        Raises:
            AuthenticationError: If authentication fails
            APIError: If API returns an error
            RateLimitError: If rate limit is exceeded
            NetworkError: If network error occurs
        """
        # Build URL
        url = f"{self.base_url}{endpoint}"
        
        # Prepare query string
        query_string = ""
        if params:
            query_string = urlencode(params)
        
        # Prepare request body
        body = ""
        if data:
            body = json.dumps(data)
        
        # Generate authentication headers
        headers = self.auth.generate_headers(
            method=method,
            path=endpoint,
            query_string=query_string,
            body=body
        )
        
        try:
            # Make request
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                data=body if body else None,
                headers=headers,
                timeout=self.timeout
            )
            
            # Handle response
            return self._handle_response(response)
            
        except requests.exceptions.Timeout as e:
            raise NetworkError(f"Request timeout: {e}")
        except requests.exceptions.ConnectionError as e:
            raise NetworkError(f"Connection error: {e}")
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Network error: {e}")
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Handle API response and raise appropriate exceptions for errors.
        
        Args:
            response: HTTP response object
            
        Returns:
            Parsed response data
            
        Raises:
            AuthenticationError: If authentication fails (401)
            RateLimitError: If rate limit exceeded (429)
            APIError: For other API errors
        """
        # Check for rate limiting
        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After", 60)
            raise RateLimitError(
                "Rate limit exceeded",
                retry_after=int(retry_after),
                status_code=429
            )
        
        # Try to parse JSON response
        try:
            response_data = response.json()
        except json.JSONDecodeError:
            if not response.ok:
                raise APIError(
                    f"API error: {response.status_code} - {response.text}",
                    status_code=response.status_code
                )
            raise APIError("Invalid JSON response from API")
        
        # Check for authentication errors
        if response.status_code == 401:
            error_message = response_data.get("error", {}).get("message", "Authentication failed")
            raise AuthenticationError(error_message, status_code=401)
        
        # Check for API errors
        if not response.ok:
            error_data = response_data.get("error", {})
            error_message = error_data.get("message", "API request failed")
            error_code = error_data.get("code")
            
            raise APIError(
                error_message,
                error_code=error_code,
                status_code=response.status_code
            )
        
        # Check success field
        if not response_data.get("success", True):
            error_data = response_data.get("error", {})
            error_message = error_data.get("message", "API request failed")
            raise APIError(error_message)
        
        return response_data
    
    # ============================================================================
    # Order Management Methods
    # ============================================================================
    
    def place_order(
        self,
        symbol: str,
        side: Union[str, OrderSide],
        order_type: Union[str, OrderType],
        size: int,
        limit_price: Optional[str] = None,
        product_id: Optional[int] = None,
        **kwargs
    ) -> Order:
        """
        Place a new order.
        
        Args:
            symbol: Product symbol (e.g., "BTCUSD")
            side: Order side ("buy" or "sell")
            order_type: Order type ("limit_order" or "market_order")
            size: Order size
            limit_price: Limit price (required for limit orders)
            product_id: Product ID (use either symbol or product_id)
            **kwargs: Additional order parameters (stop_price, time_in_force, etc.)
            
        Returns:
            Created Order object
            
        Raises:
            ValidationError: If required parameters are missing
            OrderError: If order placement fails
            
        Example:
            >>> order = client.place_order(
            ...     symbol="BTCUSD",
            ...     side="buy",
            ...     order_type="limit_order",
            ...     size=10,
            ...     limit_price="50000"
            ... )
        """
        # Convert enums to strings
        if isinstance(side, OrderSide):
            side = side.value
        if isinstance(order_type, OrderType):
            order_type = order_type.value
        
        # Validate required parameters
        if order_type == "limit_order" and not limit_price:
            raise ValidationError("limit_price is required for limit orders")
        
        # Build request payload
        payload = {
            "size": size,
            "side": side,
            "order_type": order_type,
        }
        
        if product_id:
            payload["product_id"] = product_id
        else:
            payload["product_symbol"] = symbol
        
        if limit_price:
            payload["limit_price"] = limit_price
        
        # Add optional parameters
        for key, value in kwargs.items():
            if value is not None:
                if isinstance(value, Enum):
                    payload[key] = value.value
                else:
                    payload[key] = value
        
        try:
            response = self._request("POST", ORDERS_ENDPOINT, data=payload)
            return Order.from_dict(response["result"])
        except APIError as e:
            raise OrderError(f"Failed to place order: {e.message}", error_code=e.error_code)
    
    def edit_order(
        self,
        order_id: int,
        size: Optional[int] = None,
        limit_price: Optional[str] = None,
        product_id: Optional[int] = None,
        symbol: Optional[str] = None,
        **kwargs
    ) -> Order:
        """
        Edit an existing order.
        
        Args:
            order_id: Order ID to edit
            size: New order size
            limit_price: New limit price
            product_id: Product ID (use either product_id or symbol)
            symbol: Product symbol (use either product_id or symbol)
            **kwargs: Additional parameters to update
            
        Returns:
            Updated Order object
            
        Raises:
            ValidationError: If neither product_id nor symbol is provided
            OrderError: If order edit fails
            
        Example:
            >>> order = client.edit_order(
            ...     order_id=12345,
            ...     product_id=27,
            ...     limit_price="51000"
            ... )
        """
        # Validate that product_id or symbol is provided
        if not product_id and not symbol:
            raise ValidationError("Either product_id or symbol must be provided")
        
        payload = {"id": order_id}
        
        # Add product identifier (required by API)
        if product_id:
            payload["product_id"] = product_id
        else:
            payload["product_symbol"] = symbol
        
        if size is not None:
            payload["size"] = size
        if limit_price is not None:
            payload["limit_price"] = limit_price
        
        for key, value in kwargs.items():
            if value is not None:
                if isinstance(value, Enum):
                    payload[key] = value.value
                else:
                    payload[key] = value
        
        try:
            response = self._request("PUT", ORDERS_ENDPOINT, data=payload)
            return Order.from_dict(response["result"])
        except APIError as e:
            raise OrderError(f"Failed to edit order: {e.message}", error_code=e.error_code)
    
    def cancel_order(self, order_id: int, product_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Cancel an order.
        
        Args:
            order_id: Order ID to cancel
            product_id: Product ID (optional, but recommended)
            
        Returns:
            Cancellation response
            
        Raises:
            OrderError: If order cancellation fails
            
        Example:
            >>> result = client.cancel_order(order_id=12345, product_id=27)
        """
        # API uses DELETE /v2/orders with order_id in body (NOT /v2/orders/{id})
        data = {"id": order_id}
        if product_id:
            data["product_id"] = product_id
        
        try:
            response = self._request("DELETE", ORDERS_ENDPOINT, data=data)
            return response.get("result", {})
        except APIError as e:
            raise OrderError(f"Failed to cancel order: {e.message}", error_code=e.error_code)
    
    def cancel_all_orders(self, symbol: Optional[str] = None, product_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Cancel all open orders for a product or all products.
        
        Args:
            symbol: Product symbol (optional)
            product_id: Product ID (optional)
            
        Returns:
            List of cancelled orders
            
        Example:
            >>> cancelled = client.cancel_all_orders(symbol="BTCUSD")
        """
        params = {}
        if product_id:
            params["product_id"] = product_id
        elif symbol:
            params["product_symbol"] = symbol
        
        try:
            response = self._request("DELETE", ORDERS_ENDPOINT, params=params)
            return response.get("result", [])
        except APIError as e:
            raise OrderError(f"Failed to cancel all orders: {e.message}", error_code=e.error_code)
    
    def get_order(self, order_id: int) -> Order:
        """
        Get order by ID.
        
        Args:
            order_id: Order ID
            
        Returns:
            Order object
            
        Example:
            >>> order = client.get_order(order_id=12345)
        """
        endpoint = ORDERS_BY_ID_ENDPOINT.format(order_id=order_id)
        response = self._request("GET", endpoint)
        return Order.from_dict(response["result"])
    
    def get_orders(
        self,
        product_id: Optional[int] = None,
        state: Optional[Union[str, OrderState]] = None,
        **kwargs
    ) -> List[Order]:
        """
        Get orders with optional filters.
        
        Args:
            product_id: Filter by product ID
            state: Filter by order state ("open", "pending", "closed", "cancelled")
            **kwargs: Additional filter parameters
            
        Returns:
            List of Order objects
            
        Example:
            >>> orders = client.get_orders(product_id=27, state="open")
        """
        params = {}
        
        if product_id is not None:
            params["product_id"] = product_id
        
        if state is not None:
            if isinstance(state, OrderState):
                params["state"] = state.value
            else:
                params["state"] = state
        
        for key, value in kwargs.items():
            if value is not None:
                if isinstance(value, Enum):
                    params[key] = value.value
                else:
                    params[key] = value
        
        response = self._request("GET", ORDERS_ENDPOINT, params=params)
        orders_data = response.get("result", [])
        
        return [Order.from_dict(order_data) for order_data in orders_data]
    
    # ============================================================================
    # Batch Operations
    # ============================================================================
    
    def place_batch_orders(self, symbol: str, orders: List[Dict[str, Any]], product_id: Optional[int] = None) -> List[Order]:
        """
        Place multiple orders in a single batch request.
        
        Args:
            symbol: Product symbol
            orders: List of order dictionaries
            product_id: Product ID (optional, use either symbol or product_id)
            
        Returns:
            List of created Order objects
            
        Example:
            >>> orders = client.place_batch_orders(
            ...     symbol="BTCUSD",
            ...     orders=[
            ...         {"side": "buy", "size": 10, "order_type": "limit_order", "limit_price": "50000"},
            ...         {"side": "sell", "size": 10, "order_type": "limit_order", "limit_price": "51000"}
            ...     ]
            ... )
        """
        payload = {"orders": orders}
        
        if product_id:
            payload["product_id"] = product_id
        else:
            payload["product_symbol"] = symbol
        
        try:
            response = self._request("POST", BATCH_ORDERS_ENDPOINT, data=payload)
            return [Order.from_dict(order_data) for order_data in response.get("result", [])]
        except APIError as e:
            raise OrderError(f"Failed to place batch orders: {e.message}", error_code=e.error_code)
    
    def edit_batch_orders(self, symbol: str, orders: List[Dict[str, Any]], product_id: Optional[int] = None) -> List[Order]:
        """
        Edit multiple orders in a single batch request.
        
        Args:
            symbol: Product symbol
            orders: List of order edit dictionaries (must include 'id')
            product_id: Product ID (optional)
            
        Returns:
            List of updated Order objects
            
        Example:
            >>> orders = client.edit_batch_orders(
            ...     symbol="BTCUSD",
            ...     orders=[
            ...         {"id": 12345, "limit_price": "50500"},
            ...         {"id": 12346, "limit_price": "51500"}
            ...     ]
            ... )
        """
        payload = {"orders": orders}
        
        if product_id:
            payload["product_id"] = product_id
        else:
            payload["product_symbol"] = symbol
        
        try:
            response = self._request("PUT", BATCH_EDIT_ORDERS_ENDPOINT, data=payload)
            return [Order.from_dict(order_data) for order_data in response.get("result", [])]
        except APIError as e:
            raise OrderError(f"Failed to edit batch orders: {e.message}", error_code=e.error_code)
    
    def cancel_batch_orders(self, order_ids: List[int], symbol: Optional[str] = None, product_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Cancel multiple orders. 
        
        Note: If the batch delete endpoint is not available (404 error),
        this method will fall back to cancelling orders individually.
        
        Args:
            order_ids: List of order IDs to cancel
            symbol: Product symbol (optional, used for fallback)
            product_id: Product ID (optional, used for fallback)
            
        Returns:
            List of cancellation results
            
        Example:
            >>> results = client.cancel_batch_orders(
            ...     order_ids=[12345, 12346],
            ...     product_id=27
            ... )
        """
        payload = {
            "orders": [{"id": order_id} for order_id in order_ids]
        }
        
        if product_id:
            payload["product_id"] = product_id
        elif symbol:
            payload["product_symbol"] = symbol
        
        try:
            response = self._request("POST", BATCH_DELETE_ORDERS_ENDPOINT, data=payload)
            return response.get("result", [])
        except APIError as e:
            # If batch endpoint doesn't exist (404), fall back to individual cancels
            if e.status_code == 404:
                results = []
                for order_id in order_ids:
                    try:
                        result = self.cancel_order(order_id=order_id, product_id=product_id)
                        results.append(result)
                    except OrderError:
                        # Continue even if one order fails
                        pass
                return results
            else:
                raise OrderError(f"Failed to cancel batch orders: {e.message}", error_code=e.error_code)
    
    # ============================================================================
    # Position Methods
    # ============================================================================
    
    def get_positions(
        self,
        product_id: Optional[int] = None,
        underlying_asset_symbol: Optional[str] = None
    ) -> List[Position]:
        """
        Get all open positions.
        
        Args:
            product_id: Filter by product ID (optional)
            underlying_asset_symbol: Filter by underlying asset (e.g., 'BTC', 'ETH') (optional)
                Use this to get ALL positions for an asset (including options)
            
        Returns:
            List of Position objects
            
        Example:
            >>> # Get all positions for BTC (futures + options)
            >>> positions = client.get_positions(underlying_asset_symbol="BTC")
            >>> 
            >>> # Get all positions for ETH
            >>> eth_positions = client.get_positions(underlying_asset_symbol="ETH")
            >>> 
            >>> # Get specific product position
            >>> btc_position = client.get_positions(product_id=27)
        """
        params = {}
        if product_id is not None:
            params["product_id"] = product_id
        elif underlying_asset_symbol is not None:
            params["underlying_asset_symbol"] = underlying_asset_symbol
        
        try:
            response = self._request("GET", POSITIONS_ENDPOINT, params=params)
            positions_data = response.get("result", [])
            
            # Handle empty positions
            if not positions_data:
                return []
            
            # Handle both single position and array responses
            if isinstance(positions_data, dict):
                # Single position returned
                if positions_data:  # Not empty dict
                    return [Position.from_dict(positions_data)]
                return []
            
            # Array of positions
            return [Position.from_dict(pos_data) for pos_data in positions_data]
            
        except APIError as e:
            # If "bad_schema" error when no params, try getting all by asset
            if "bad_schema" in str(e).lower() and not params:
                # No positions or need to specify parameters
                return []
            raise
    
    def change_margin(self, product_id: int, delta_margin: str) -> Position:
        """
        Add or remove margin from a position.
        
        Args:
            product_id: Product ID
            delta_margin: Margin change amount (positive to add, negative to remove)
            
        Returns:
            Updated Position object
            
        Example:
            >>> position = client.change_margin(product_id=27, delta_margin="100")
        """
        payload = {
            "product_id": product_id,
            "delta_margin": delta_margin
        }
        
        response = self._request("POST", CHANGE_MARGIN_ENDPOINT, data=payload)
        return Position.from_dict(response["result"])
    
    # ============================================================================
    # Account Methods
    # ============================================================================
    
    def get_wallet_balances(self) -> List[Balance]:
        """
        Get wallet balances for all assets.
        
        Returns:
            List of Balance objects
            
        Example:
            >>> balances = client.get_wallet_balances()
            >>> for balance in balances:
            ...     print(f"{balance.asset_symbol}: {balance.balance}")
        """
        response = self._request("GET", WALLET_BALANCES_ENDPOINT)
        balances_data = response.get("result", [])
        
        return [Balance.from_dict(balance_data) for balance_data in balances_data]
    
    def get_products(self) -> List[Product]:
        """
        Get all available trading products.
        
        Returns:
            List of Product objects
            
        Example:
            >>> products = client.get_products()
            >>> for product in products:
            ...     print(f"{product.symbol}: {product.description}")
        """
        response = self._request("GET", PRODUCTS_ENDPOINT)
        products_data = response.get("result", [])
        
        return [Product.from_dict(product_data) for product_data in products_data]
    
    def get_product(self, symbol: str) -> Product:
        """
        Get a specific product by symbol.
        
        Args:
            symbol: Product symbol (e.g., "BTCUSD")
            
        Returns:
            Product object
            
        Example:
            >>> product = client.get_product("BTCUSD")
        """
        products = self.get_products()
        for product in products:
            if product.symbol == symbol:
                return product
        
        raise APIError(f"Product not found: {symbol}")
    
    def close(self):
        """Close the HTTP session."""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# Fix missing import
from enum import Enum

