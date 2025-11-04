# Delta Exchange Python Client - Examples

This directory contains example scripts demonstrating how to use the Delta Exchange Python client library.

## Setup

1. **Install Dependencies**

```bash
cd ..
pip install -e .
```

2. **Configure API Credentials**

Copy the `.env.example` file to `.env` and add your API credentials:

```bash
cp .env.example .env
```

Edit `.env`:
```
DELTA_API_KEY=your_actual_api_key
DELTA_API_SECRET=your_actual_api_secret
```

⚠️ **Security Warning**: Never commit your `.env` file with real credentials!

## REST API Examples

### 1. Place Order (`place_order.py`)

Demonstrates how to place different types of orders:
- Limit orders
- Market orders (commented out for safety)
- Stop-loss orders
- Orders with time-in-force settings (IOC, GTC)

```bash
python examples/place_order.py
```

### 2. Cancel Order (`cancel_order.py`)

Shows different ways to cancel orders:
- Cancel a single order by ID
- Cancel all orders for a specific symbol
- Batch cancel multiple orders

```bash
python examples/cancel_order.py
```

### 3. Get Positions (`get_positions.py`)

Demonstrates how to query account information:
- Get all open positions
- Get wallet balances
- Get available trading products
- Query specific product details
- Change position margin (commented out for safety)

```bash
python examples/get_positions.py
```

### 4. Batch Operations (`batch_orders.py`)

Shows efficient batch operations:
- Place multiple orders in a single request
- Edit multiple orders simultaneously
- Cancel multiple orders at once
- Place orders on both buy and sell sides

```bash
python examples/batch_orders.py
```

## Options Trading Examples

### 5. Options Trading (`options_trading.py`)

Complete examples of trading options (calls and puts):
- Finding available options contracts
- Placing call and put orders (long/short)
- Closing options positions
- Managing options orders
- Understanding symbol format (C-ETH-3600-071125)

```bash
python examples/options_trading.py
```

**Note**: All trading code is commented out for safety. Uncomment carefully!

### 6. Options Strategies (`options_strategies.py`)

Implementation of common options strategies:
- **Bull Call Spread** - Moderately bullish
- **Bear Put Spread** - Moderately bearish
- **Long Straddle** - High volatility expected
- **Short Straddle** - Low volatility (high risk!)
- **Iron Condor** - Range-bound profit
- **Covered Call** - Income generation

```bash
python examples/options_strategies.py
```

⚠️ **WARNING**: Options strategies involve complex risks. Only use if you fully understand them!

### 7. Options WebSocket (`websocket_options.py`)

Real-time monitoring of options:
- Options price updates (ticker)
- Options order book
- Your options positions updates
- Your options orders updates
- Your options trades/fills

```bash
python examples/websocket_options.py
```

**See**: [`../docs/options-guide.md`](../docs/options-guide.md) for a complete guide to options trading.

## WebSocket Examples

### 8. Ticker Stream (`websocket_ticker.py`)

Real-time ticker updates for multiple symbols:
- Subscribe to ticker data
- Monitor price changes
- Track volume and other metrics
- **No authentication required**

```bash
python examples/websocket_ticker.py
```

### 9. Orderbook & Trades (`websocket_orderbook.py`)

Stream real-time orderbook and trade data:
- Monitor best bid/ask
- Calculate spread
- See live trades as they happen
- **No authentication required**

```bash
python examples/websocket_orderbook.py
```

### 10. Private Channels (`websocket_private.py`)

Real-time updates for your account (requires API credentials):
- Order updates (placement, fills, cancellations)
- Position updates (entry, PnL, liquidations)
- User trade notifications
- Margin updates

```bash
python examples/websocket_private.py
```

**Note**: WebSocket examples run indefinitely until you press `Ctrl+C`.

## Safety Features

Many examples include safety features to prevent accidental trades:

1. **Post-only orders**: Orders that won't fill immediately (only rest in order book)
2. **Far from market prices**: Limit prices set intentionally far from current market
3. **Commented out dangerous operations**: Market orders and margin changes are commented
4. **Small position sizes**: Examples use minimal sizes for testing

## Best Practices

### Error Handling

All examples include comprehensive error handling:

```python
try:
    order = client.place_order(...)
except AuthenticationError as e:
    # Handle auth failures
except OrderError as e:
    # Handle order-specific errors
except APIError as e:
    # Handle general API errors
finally:
    client.close()  # Always close the session
```

### Using Context Manager

For automatic resource cleanup:

```python
with DeltaRestClient(api_key=key, api_secret=secret) as client:
    positions = client.get_positions()
    # Session automatically closed
```

### Environment Variables

Always use environment variables for credentials:

```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("DELTA_API_KEY")
api_secret = os.getenv("DELTA_API_SECRET")
```

## Testing Without Risk

To test the library without risking real funds:

1. **Use Post-Only Orders**: Set `post_only=True` so orders won't fill immediately
2. **Set Unrealistic Prices**: Use prices far from market to ensure orders won't execute
3. **Cancel Immediately**: Place orders then immediately cancel them
4. **Use Testnet**: If Delta Exchange offers a testnet, use those credentials

## Common Issues

### Authentication Errors

```
❌ Authentication Error: Authentication failed
```

**Solution**: Check that your API key and secret are correct in the `.env` file.

### Order Errors

```
❌ Order Error: Insufficient balance
```

**Solution**: Ensure you have sufficient funds in your account.

### Rate Limits

```
❌ Rate Limit Error: Rate limit exceeded
```

**Solution**: The client has built-in retry logic, but reduce request frequency if this persists.

## Advanced Usage

### Custom Timeouts

```python
client = DeltaRestClient(
    api_key=key,
    api_secret=secret,
    timeout=(5, 30)  # (connect_timeout, read_timeout)
)
```

### Using Enums

```python
from delta_exchange import OrderSide, OrderType, TimeInForce

order = client.place_order(
    symbol="BTCUSD",
    side=OrderSide.BUY,
    order_type=OrderType.LIMIT_ORDER,
    time_in_force=TimeInForce.IOC,
    size=10,
    limit_price="50000"
)
```

### Batch Operations for Efficiency

When placing/editing/cancelling multiple orders, use batch operations:

```python
# Instead of this (slow, multiple network calls):
for order_data in orders:
    client.place_order(**order_data)

# Do this (fast, single network call):
client.place_batch_orders(symbol="BTCUSD", orders=orders)
```

## Support

- **Documentation**: https://docs.delta.exchange/
- **API Reference**: https://docs.delta.exchange/api/swagger_v2
- **GitHub Issues**: Report bugs or request features

## Disclaimer

These examples are for educational purposes. Always test thoroughly with small amounts before using in production. Trading cryptocurrency derivatives involves substantial risk.

