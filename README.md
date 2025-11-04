# Delta Exchange Python Client

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A professional Python client library for the [Delta Exchange](https://www.delta.exchange/) API. This library provides a clean, intuitive interface for trading **perpetual futures, dated futures, and options** on Delta Exchange.

## Features

- ✅ **REST API Client** - Complete support for order management, positions, and account operations
- ✅ **WebSocket Client** - Real-time market data and order updates
- ✅ **Options Trading** - Full support for calls, puts, and options strategies
- ✅ **Futures Trading** - Perpetual and dated futures contracts
- ✅ **Type Hints** - Full type annotations for better IDE support
- ✅ **Async Support** - Asynchronous WebSocket client using `asyncio`
- ✅ **Comprehensive Error Handling** - Clear, specific exceptions for different error types
- ✅ **Authentication** - Automatic request signing with HMAC-SHA256
- ✅ **Easy to Use** - Simple, intuitive API design

**Supported Contract Types:**
- 📈 **Perpetual Futures** (BTCUSD, ETHUSD, etc.)
- 📅 **Dated Futures** (with expiration)
- 📞 **Call Options** (C-ETH-3600-071125, etc.)
- 📉 **Put Options** (P-BTC-95000-141125, etc.)
- ❌ **Spot Trading** (not available on Delta Exchange)

## 📚 Documentation

**Complete documentation is available in the `docs/` directory:**

- **[docs/README.md](docs/README.md)** - 📖 **Documentation index** (start here!)
- **[docs/options-guide.md](docs/options-guide.md)** - 📊 Complete guide to options trading (500+ lines)
- **[docs/websocket-guide.md](docs/websocket-guide.md)** - 🔌 Complete WebSocket guide (600+ lines)
- **[docs/architecture.md](docs/architecture.md)** - 🔧 Technical specification and design
- **[docs/testing.md](docs/testing.md)** - 🧪 Testing guide
- **[examples/README.md](examples/README.md)** - 💻 All code examples

**Quick Links:**
- [Options Trading](docs/options-guide.md) - Learn to trade calls and puts
- [WebSocket Streaming](docs/websocket-guide.md) - Real-time market data
- [Code Examples](examples/) - 10+ working examples
- [Testing Guide](docs/testing.md) - How to test the client

## Installation

### From Source

```bash
git clone https://github.com/kuldeepakkatwal/Delta_client.git
cd Delta_client
pip install -e .
```

### Using pip (once published to PyPI)

```bash
pip install delta-exchange-python
```

## Quick Start

### REST API

```python
from delta_exchange import DeltaRestClient

# Initialize the client
client = DeltaRestClient(
    api_key="your_api_key",
    api_secret="your_api_secret"
)

# Place an order
order = client.place_order(
    symbol="BTCUSD",
    side="buy",
    order_type="limit_order",
    size=10,
    limit_price="50000"
)
print(f"Order placed: {order}")

# Get positions
positions = client.get_positions()
for position in positions:
    print(f"Position: {position}")

# Cancel an order
client.cancel_order(order_id=12345)
```

### WebSocket API

```python
import asyncio
from delta_exchange import DeltaWebSocketClient

async def on_ticker(data):
    print(f"Ticker update: {data}")

async def main():
    # Initialize WebSocket client
    ws_client = DeltaWebSocketClient(
        api_key="your_api_key",
        api_secret="your_api_secret"
    )
    
    # Subscribe to ticker updates
    await ws_client.subscribe_ticker(["BTCUSD", "ETHUSD"], callback=on_ticker)
    
    # Run the client
    await ws_client.run()

# Run the async main function
asyncio.run(main())
```

### Options Trading

```python
from delta_exchange import DeltaRestClient

client = DeltaRestClient(
    api_key="your_api_key",
    api_secret="your_api_secret"
)

# Buy a call option (bullish)
call_order = client.place_order(
    symbol="C-ETH-3600-071125",  # ETH Call, $3600 strike, exp 07/11/25
    side="buy",
    order_type="limit_order",
    size=5,
    limit_price="80.0"
)
print(f"Call option order: {call_order}")

# Buy a put option (bearish)
put_order = client.place_order(
    symbol="P-BTC-95000-141125",  # BTC Put, $95000 strike, exp 14/11/25
    side="buy",
    order_type="limit_order",
    size=3,
    limit_price="1200.0"
)
print(f"Put option order: {put_order}")

# Get options positions
eth_positions = client.get_positions(underlying_asset_symbol="ETH")
options_positions = [p for p in eth_positions if p.symbol.startswith(('C-', 'P-'))]

for position in options_positions:
    option_type = "CALL" if position.symbol.startswith('C-') else "PUT"
    print(f"{option_type}: {position.symbol} | PnL: ${position.unrealized_pnl}")
```

**📖 See `OPTIONS_GUIDE.md` for a complete guide to options trading, including:**
- Options basics (calls vs puts, long vs short)
- Symbol format explanation
- Common strategies (spreads, straddles, iron condors, etc.)
- Risk management and best practices

## API Key Setup

1. Sign up for a [Delta Exchange](https://www.delta.exchange/) account
2. Go to **Settings** → **API Keys**
3. Create a new API key with appropriate permissions
4. Store your API key and secret securely

### Environment Variables (Recommended)

Create a `.env` file in your project:

```env
DELTA_API_KEY=your_api_key_here
DELTA_API_SECRET=your_api_secret_here
```

Then load it in your code:

```python
import os
from dotenv import load_dotenv
from delta_exchange import DeltaRestClient

load_dotenv()

client = DeltaRestClient(
    api_key=os.getenv("DELTA_API_KEY"),
    api_secret=os.getenv("DELTA_API_SECRET")
)
```

## Available Methods

### REST Client

#### Order Management
- `place_order()` - Place a new order
- `edit_order()` - Edit an existing order
- `cancel_order()` - Cancel an order
- `cancel_all_orders()` - Cancel all orders for a symbol
- `get_order()` - Get order by ID
- `get_orders()` - Get all orders with filters

#### Batch Operations
- `place_batch_orders()` - Place multiple orders at once
- `edit_batch_orders()` - Edit multiple orders at once
- `cancel_batch_orders()` - Cancel multiple orders at once

#### Positions
- `get_positions()` - Get all positions
- `change_margin()` - Add or remove margin from a position

#### Account
- `get_wallet_balances()` - Get wallet balances
- `get_products()` - Get available products
- `get_product()` - Get specific product details

### WebSocket Client

#### Public Channels
- `subscribe_ticker()` - Real-time ticker data
- `subscribe_orderbook()` - Real-time orderbook updates
- `subscribe_trades()` - Real-time trade data
- `subscribe_funding_rate()` - Funding rate updates
- `subscribe_mark_price()` - Mark price updates

#### Private Channels (Requires Authentication)
- `subscribe_orders()` - Real-time order updates
- `subscribe_positions()` - Real-time position updates
- `subscribe_user_trades()` - Your executed trades
- `subscribe_margins()` - Margin updates

## Examples

Check the `examples/` directory for more detailed examples:

### Futures Trading
- `examples/place_order.py` - Order placement examples
- `examples/cancel_order.py` - Order cancellation examples
- `examples/get_positions.py` - Position management
- `examples/batch_orders.py` - Batch operations

### Options Trading
- `examples/options_trading.py` - Basic options trading (calls & puts)
- `examples/options_strategies.py` - Options strategies (spreads, straddles, etc.)
- `examples/websocket_options.py` - Real-time options monitoring

### WebSocket Streaming
- `examples/websocket_ticker.py` - Real-time ticker updates
- `examples/websocket_orderbook.py` - Order book streaming
- `examples/websocket_private.py` - Private account updates

## Error Handling

The library provides specific exception classes for different error types:

```python
from delta_exchange import DeltaRestClient
from delta_exchange.exceptions import (
    AuthenticationError,
    OrderError,
    APIError,
    RateLimitError
)

client = DeltaRestClient(api_key="key", api_secret="secret")

try:
    order = client.place_order(
        symbol="BTCUSD",
        side="buy",
        order_type="limit_order",
        size=10,
        limit_price="50000"
    )
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except OrderError as e:
    print(f"Order failed: {e}")
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after}s")
except APIError as e:
    print(f"API error: {e}")
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/delta-exchange-python.git
cd delta-exchange-python

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with dev dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=delta_exchange

# Run specific test file
pytest tests/test_auth.py
```

### Code Quality

```bash
# Format code with black
black delta_exchange/

# Type checking with mypy
mypy delta_exchange/

# Linting with flake8
flake8 delta_exchange/
```

## Documentation

- [Delta Exchange Official Documentation](https://docs.delta.exchange/)
- [API Reference](https://docs.delta.exchange/api/swagger_v2)
- [Technical Specification](SPEC.md)
- [Development Roadmap](ROADMAP.md)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This library is not officially affiliated with Delta Exchange. Use at your own risk. Always test thoroughly with small amounts before using in production.

## Support

- **Issues**: Report bugs or request features on [GitHub Issues](https://github.com/yourusername/delta-exchange-python/issues)
- **Documentation**: Check the [official Delta Exchange docs](https://docs.delta.exchange/)
- **Community**: Join the Delta Exchange community for discussions

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes.

---

**Happy Trading! 🚀**

