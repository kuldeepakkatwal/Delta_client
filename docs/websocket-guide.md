# WebSocket Client Guide

## Overview

The Delta Exchange WebSocket client provides real-time streaming data for both public market data and private account updates. It's built with `async/await` and includes automatic reconnection, authentication, and comprehensive error handling.

## Features

✅ **Public Channels** (no authentication required):
- Real-time ticker updates
- Level 2 orderbook streaming
- Live trades
- Funding rates
- Mark prices

✅ **Private Channels** (authentication required):
- Order updates (placements, fills, cancellations)
- Position updates (entries, PnL, liquidations)
- User trade notifications
- Margin updates

✅ **Advanced Features**:
- Automatic reconnection with exponential backoff
- WebSocket authentication for private channels
- Event-based callbacks
- Heartbeat/ping-pong for connection health
- Multiple concurrent subscriptions
- Async/await support

## Quick Start

### Public Channels (No Auth Required)

```python
import asyncio
from delta_exchange import DeltaWebSocketClient

async def on_ticker(data):
    ticker = data.get("ticker", {})
    print(f"Price: {ticker.get('close')}")

async def main():
    client = DeltaWebSocketClient()
    
    # Connect
    await client.connect()
    
    # Subscribe to ticker
    await client.subscribe_ticker(["BTCUSD", "ETHUSD"], on_ticker)
    
    # Run
    await client.run()

asyncio.run(main())
```

### Private Channels (Auth Required)

```python
import asyncio
from delta_exchange import DeltaWebSocketClient

async def on_order(data):
    order = data.get("order", {})
    print(f"Order {order.get('id')}: {order.get('state')}")

async def main():
    client = DeltaWebSocketClient(
        api_key="your_key",
        api_secret="your_secret"
    )
    
    # Connect and authenticate
    await client.connect()
    
    # Subscribe to orders
    await client.subscribe_orders(on_order)
    
    # Run
    await client.run()

asyncio.run(main())
```

## Channel Reference

### Public Channels

#### 1. Ticker (`subscribe_ticker`)

Real-time ticker data including last price, volume, open interest, etc.

```python
async def on_ticker(data):
    ticker = data.get("ticker", {})
    symbol = ticker.get("symbol")
    mark_price = ticker.get("mark_price")
    volume = ticker.get("volume")
    print(f"{symbol}: ${mark_price} | Volume: {volume}")

await client.subscribe_ticker(["BTCUSD", "ETHUSD"], on_ticker)
```

**Data Structure:**
```json
{
  "type": "ticker",
  "ticker": {
    "symbol": "BTCUSD",
    "close": "67850.5",
    "open": "67200.0",
    "high": "68000.0",
    "low": "67100.0",
    "volume": "12345678",
    "mark_price": "67851.2",
    "funding_rate": "0.0001",
    "open_interest": "98765432"
  }
}
```

#### 2. Orderbook (`subscribe_orderbook`)

Level 2 orderbook updates with bids and asks.

```python
async def on_orderbook(data):
    orderbook = data.get("orderbook", {})
    buy = orderbook.get("buy", [])
    sell = orderbook.get("sell", [])
    
    if buy and sell:
        best_bid = buy[0]["price"]
        best_ask = sell[0]["price"]
        spread = float(best_ask) - float(best_bid)
        print(f"Spread: ${spread:.2f}")

await client.subscribe_orderbook(["BTCUSD"], on_orderbook)
```

**Data Structure:**
```json
{
  "type": "l2_orderbook",
  "orderbook": {
    "symbol": "BTCUSD",
    "buy": [
      {"price": "67800", "size": "100"},
      {"price": "67799", "size": "250"}
    ],
    "sell": [
      {"price": "67801", "size": "150"},
      {"price": "67802", "size": "200"}
    ]
  }
}
```

#### 3. Trades (`subscribe_trades`)

Live executed trades on the exchange.

```python
async def on_trade(data):
    trades = data.get("trades", [])
    for trade in trades:
        symbol = trade.get("symbol")
        price = trade.get("price")
        size = trade.get("size")
        side = trade.get("buyer_role")  # 'taker' or 'maker'
        print(f"{side.upper()} {size} @ ${price}")

await client.subscribe_trades(["BTCUSD"], on_trade)
```

#### 4. Funding Rate (`subscribe_funding_rate`)

Periodic funding rate updates (important for perpetuals).

```python
await client.subscribe_funding_rate(["BTCUSD"], on_funding_rate)
```

#### 5. Mark Price (`subscribe_mark_price`)

Mark price updates (used for liquidations and PnL calculations).

```python
await client.subscribe_mark_price(["BTCUSD"], on_mark_price)
```

### Private Channels

**Note**: All private channels require authentication.

#### 1. Orders (`subscribe_orders`)

Real-time order updates - placements, edits, fills, cancellations.

```python
async def on_order(data):
    order = data.get("order", {})
    order_id = order.get("id")
    symbol = order.get("product_symbol")
    state = order.get("state")
    size = order.get("size")
    unfilled = order.get("unfilled_size")
    
    print(f"Order #{order_id} ({symbol})")
    print(f"  State: {state}")
    print(f"  Filled: {size - unfilled}/{size}")

await client.subscribe_orders(on_order)
```

**Trigger Events:**
- New order placed
- Order partially filled
- Order fully filled
- Order cancelled
- Order edited

#### 2. Positions (`subscribe_positions`)

Real-time position updates - entries, exits, PnL changes.

```python
async def on_position(data):
    position = data.get("position", {})
    symbol = position.get("product_symbol")
    size = position.get("size")
    entry_price = position.get("entry_price")
    unrealized_pnl = position.get("unrealized_pnl")
    
    position_type = "LONG" if size > 0 else "SHORT" if size < 0 else "FLAT"
    print(f"{symbol} {position_type}")
    print(f"  Size: {abs(size)}")
    print(f"  Entry: ${entry_price}")
    print(f"  Unrealized PnL: ${unrealized_pnl}")

await client.subscribe_positions(on_position)
```

**Trigger Events:**
- Position opened
- Position increased/decreased
- Position closed
- PnL updated
- Liquidation

#### 3. User Trades (`subscribe_user_trades`)

Your executed trades (fills).

```python
async def on_user_trade(data):
    trade = data.get("trade", {})
    symbol = trade.get("product_symbol")
    side = trade.get("side")
    size = trade.get("size")
    price = trade.get("price")
    commission = trade.get("commission")
    
    print(f"FILLED: {side.upper()} {size} {symbol} @ ${price}")
    print(f"  Commission: ${commission}")

await client.subscribe_user_trades(on_user_trade)
```

#### 4. Margins (`subscribe_margins`)

Margin updates for your account.

```python
await client.subscribe_margins(on_margin)
```

## Connection Management

### Connection States

The client maintains connection state:

```python
from delta_exchange.websocket_client import ConnectionState

# Check connection state
print(client.state)  # ConnectionState.CONNECTED

# Check if connected
if client.is_connected:
    print("Connected!")

# Check if authenticated
if client.is_authenticated:
    print("Authenticated!")
```

**States:**
- `DISCONNECTED`: Not connected
- `CONNECTING`: Connection in progress
- `CONNECTED`: Connected to WebSocket
- `AUTHENTICATED`: Connected and authenticated
- `RECONNECTING`: Attempting to reconnect
- `CLOSED`: Connection closed permanently

### Manual Disconnection

```python
await client.disconnect()
```

### Reconnection

The client automatically reconnects on connection loss:

- **Exponential backoff**: 1s, 2s, 4s, 8s, ... up to 60s
- **Max attempts**: 10 attempts before giving up
- **Auto-resubscribe**: Automatically resubscribes to all channels

**Disable auto-reconnect:**
```python
client = DeltaWebSocketClient(auto_reconnect=False)
```

## Advanced Usage

### Multiple Callbacks

You can register multiple callbacks for the same channel:

```python
async def callback1(data):
    # Process data one way
    pass

async def callback2(data):
    # Process data another way
    pass

await client.subscribe_ticker(["BTCUSD"], callback1)
await client.subscribe_ticker(["BTCUSD"], callback2)
# Both callbacks will be called
```

### Unsubscribe

```python
# Unsubscribe from specific symbols
await client.unsubscribe("v2/ticker", ["BTCUSD"])

# Unsubscribe from all
await client.unsubscribe("v2/ticker")
```

### Custom Ping Interval

```python
client = DeltaWebSocketClient(
    ping_interval=15  # Send ping every 15 seconds (default: 30)
)
```

### Custom Base URL

```python
client = DeltaWebSocketClient(
    base_url="wss://socket.testnet.delta.exchange"  # Use testnet
)
```

### Logging

The WebSocket client uses Python's built-in logging:

```python
import logging

# Enable debug logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Now you'll see detailed WebSocket logs
```

## Error Handling

### Connection Errors

```python
from delta_exchange import WebSocketError

try:
    await client.connect()
except WebSocketError as e:
    print(f"Connection failed: {e}")
```

### Authentication Errors

```python
from delta_exchange import AuthenticationError

try:
    await client.subscribe_orders(on_order)
except AuthenticationError as e:
    print(f"Authentication required: {e}")
```

### Callback Errors

Errors in callbacks are caught and logged, but don't crash the client:

```python
async def buggy_callback(data):
    raise Exception("Oops!")  # This won't crash the client

await client.subscribe_ticker(["BTCUSD"], buggy_callback)
# Client continues running, error is logged
```

## Best Practices

### 1. Use Async/Await Properly

```python
# ✅ Good: Proper async usage
async def main():
    client = DeltaWebSocketClient()
    await client.connect()
    await client.subscribe_ticker(["BTCUSD"], on_ticker)
    await client.run()

asyncio.run(main())

# ❌ Bad: Not awaiting properly
client = DeltaWebSocketClient()
client.connect()  # Missing await!
```

### 2. Handle Graceful Shutdown

```python
async def main():
    client = DeltaWebSocketClient()
    
    try:
        await client.connect()
        await client.subscribe_ticker(["BTCUSD"], on_ticker)
        await client.run()
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        await client.disconnect()  # Always disconnect
```

### 3. Keep Callbacks Fast

```python
# ✅ Good: Fast callback
async def on_ticker(data):
    ticker = data.get("ticker", {})
    price = ticker.get("close")
    await queue.put(price)  # Quick operation

# ❌ Bad: Slow callback
async def on_ticker(data):
    ticker = data.get("ticker", {})
    await slow_database_operation(ticker)  # Blocks other messages!
```

### 4. Use Message Queues for Processing

```python
import asyncio
from asyncio import Queue

message_queue = Queue()

async def on_ticker(data):
    await message_queue.put(data)  # Fast

async def process_messages():
    while True:
        data = await message_queue.get()
        # Do expensive processing here
        await expensive_operation(data)

async def main():
    client = DeltaWebSocketClient()
    await client.connect()
    await client.subscribe_ticker(["BTCUSD"], on_ticker)
    
    # Run processor and client concurrently
    await asyncio.gather(
        client.run(),
        process_messages()
    )
```

### 5. Monitor Connection Health

```python
async def monitor_connection(client):
    while True:
        if not client.is_connected:
            print("⚠️  Connection lost!")
        await asyncio.sleep(5)

# Run monitor alongside client
await asyncio.gather(
    client.run(),
    monitor_connection(client)
)
```

## Examples

See the `examples/` directory for complete working examples:

- `websocket_ticker.py` - Simple ticker streaming
- `websocket_orderbook.py` - Orderbook and trades
- `websocket_private.py` - Private channels (orders, positions)

## Testing

Run the WebSocket test suite:

```bash
python test_websocket.py
```

This will test:
- ✅ Public channel subscriptions
- ✅ Private channel authentication
- ✅ Reconnection logic
- ✅ Connection stability

## Troubleshooting

### Connection Keeps Dropping

1. Check your internet connection
2. Verify you're using the correct WebSocket URL
3. Enable debug logging to see connection details
4. Try increasing ping interval

### Not Receiving Data

1. Verify you're subscribed to the correct channel
2. Check that symbols are valid (use correct format like "BTCUSD")
3. For private channels, ensure authentication succeeded
4. Check callback function is defined correctly

### Authentication Failed

1. Verify API key and secret are correct
2. Ensure API key has WebSocket permissions enabled
3. Check timestamp is within 5 seconds of server time
4. Try regenerating API key on Delta Exchange

### High Memory Usage

1. Limit number of concurrent subscriptions
2. Process messages quickly in callbacks
3. Don't accumulate data in memory - process and discard
4. Use message queues for heavy processing

## Performance Tips

1. **Batch subscriptions**: Subscribe to multiple symbols at once
2. **Use specific symbols**: Don't subscribe to all symbols if you only need a few
3. **Minimize callbacks**: Fewer callbacks = less overhead
4. **Async processing**: Use async functions for callbacks
5. **Monitor memory**: Use memory profiling tools if needed

## Security

1. **Never log API secrets**: Be careful with logging when authenticated
2. **Use environment variables**: Store credentials securely
3. **Enable SSL/TLS**: Always use `wss://` (not `ws://`)
4. **Rotate API keys**: Regularly regenerate your API keys
5. **Monitor connections**: Log unusual connection patterns

## API Rate Limits

WebSocket connections have different limits:

- **Max connections**: 10 concurrent connections per API key
- **Max subscriptions**: 100 channels per connection
- **Message rate**: No hard limit, but avoid excessive subscriptions

## Conclusion

The Delta Exchange WebSocket client provides a robust, production-ready solution for real-time data streaming. With automatic reconnection, comprehensive error handling, and an easy-to-use async API, you can build reliable trading systems with confidence.

For more information:
- **Examples**: See `examples/` directory
- **API Docs**: https://docs.delta.exchange/
- **Support**: GitHub Issues

