# Options Trading Guide - Delta Exchange Python Client

Complete guide to trading options using the Delta Exchange Python client.

---

## 📚 Table of Contents

1. [Options Basics](#options-basics)
2. [Symbol Format](#symbol-format)
3. [Finding Options Contracts](#finding-options-contracts)
4. [Basic Options Trading](#basic-options-trading)
5. [Common Options Strategies](#common-options-strategies)
6. [Managing Positions](#managing-positions)
7. [WebSocket Monitoring](#websocket-monitoring)
8. [Risk Management](#risk-management)

---

## Options Basics

### What are Options?

**Options** are derivatives that give you the right (but not the obligation) to buy or sell an asset at a specific price (strike) by a specific date (expiration).

### Types of Options

#### Call Options 📞
- **Right to BUY** the underlying at the strike price
- **Use when**: You're bullish (expect price to rise)
- **Max Profit**: Unlimited (theoretically)
- **Max Loss**: Premium paid (if long), Unlimited (if short)

#### Put Options 📉
- **Right to SELL** the underlying at the strike price
- **Use when**: You're bearish (expect price to fall)
- **Max Profit**: High (strike price minus premium if long), Premium collected (if short)
- **Max Loss**: Premium paid (if long), Strike price (if short)

### Long vs Short

| Position | Action | Risk | Reward |
|----------|--------|------|--------|
| **Long Call** | Buy a call | Premium paid (limited) | Unlimited |
| **Short Call** | Sell a call | Unlimited | Premium collected |
| **Long Put** | Buy a put | Premium paid (limited) | High |
| **Short Put** | Sell a put | High (strike - premium) | Premium collected |

---

## Symbol Format

Delta Exchange uses this format for options symbols:

```
[TYPE]-[ASSET]-[STRIKE]-[EXPIRY]

Examples:
C-ETH-3600-071125   = ETH Call, $3,600 strike, expires 07/11/2025
P-BTC-95000-141125  = BTC Put, $95,000 strike, expires 14/11/2025
C-BTC-100000-261225 = BTC Call, $100,000 strike, expires 26/12/2025
```

**Components:**
- `C` = Call option
- `P` = Put option
- `ETH/BTC` = Underlying asset
- `3600` = Strike price in USD
- `071125` = Expiration date (DD/MM/YY)

---

## Finding Options Contracts

### Get All Available Options

```python
from delta_exchange import DeltaRestClient
import os

client = DeltaRestClient(
    api_key=os.getenv("DELTA_API_KEY"),
    api_secret=os.getenv("DELTA_API_SECRET")
)

# Get all products
products = client.get_products()

# Filter for ETH call options
eth_calls = [p for p in products if p.symbol.startswith("C-ETH")]
print(f"Found {len(eth_calls)} ETH Call Options")

for call in eth_calls[:5]:
    print(f"  {call.symbol} (ID: {call.id})")

# Filter for ETH put options
eth_puts = [p for p in products if p.symbol.startswith("P-ETH")]
print(f"\nFound {len(eth_puts)} ETH Put Options")

for put in eth_puts[:5]:
    print(f"  {put.symbol} (ID: {put.id})")
```

### Filter by Expiration

```python
# Get options expiring on 14/11/2025
nov_14_options = [p for p in products if p.symbol.endswith("-141125")]

# Get options expiring in November 2025
nov_options = [p for p in products if "-1125" in p.symbol]
```

### Filter by Strike Price

```python
# Get options with strike around $3,500 (±$200)
eth_3500_options = [
    p for p in products 
    if p.symbol.startswith(("C-ETH-", "P-ETH-")) 
    and 3300 <= int(p.symbol.split('-')[2]) <= 3700
]
```

---

## Basic Options Trading

### 1. Buy a Call Option (Long Call)

**Use Case**: You expect ETH to rise above $3,600

```python
# Buy 5 ETH call options at $3,600 strike
order = client.place_order(
    symbol="C-ETH-3600-071125",
    side="buy",
    order_type="limit_order",
    size=5,
    limit_price=80.0,  # Willing to pay $80 per contract
    time_in_force="gtc"
)

print(f"Order placed! ID: {order.id}")
```

**Profit Scenario**: If ETH rises to $3,800:
- Option value: ~$200 (intrinsic value)
- Your cost: $80
- Profit per contract: $120
- Total profit: $120 × 5 = $600

### 2. Buy a Put Option (Long Put)

**Use Case**: You expect ETH to fall below $3,400

```python
# Buy 5 ETH put options at $3,400 strike
order = client.place_order(
    symbol="P-ETH-3400-141125",
    side="buy",
    order_type="limit_order",
    size=5,
    limit_price=70.0,  # Willing to pay $70 per contract
    time_in_force="gtc"
)
```

**Profit Scenario**: If ETH falls to $3,200:
- Option value: ~$200 (intrinsic value)
- Your cost: $70
- Profit per contract: $130
- Total profit: $130 × 5 = $650

### 3. Sell a Call Option (Short Call)

⚠️ **WARNING**: Unlimited risk if price rises!

**Use Case**: You're neutral to bearish and want to collect premium

```python
# Sell 3 ETH call options at $4,000 strike (out-of-the-money)
order = client.place_order(
    symbol="C-ETH-4000-071125",
    side="sell",
    order_type="limit_order",
    size=3,
    limit_price=30.0,  # Collect $30 per contract
    time_in_force="gtc"
)

# Total premium collected: $30 × 3 = $90
```

**Risk**: If ETH rises above $4,000, losses are unlimited!

### 4. Sell a Put Option (Short Put)

⚠️ **WARNING**: High risk if price falls significantly!

**Use Case**: You're bullish and want to collect premium

```python
# Sell 3 ETH put options at $3,000 strike (out-of-the-money)
order = client.place_order(
    symbol="P-ETH-3000-141125",
    side="sell",
    order_type="limit_order",
    size=3,
    limit_price=40.0,  # Collect $40 per contract
    time_in_force="gtc"
)

# Total premium collected: $40 × 3 = $120
```

---

## Common Options Strategies

### 1. Bull Call Spread (Moderately Bullish)

**Risk**: Limited | **Reward**: Limited

```python
# Assume ETH = $3,500
# Buy lower strike call
buy_call = client.place_order(
    symbol="C-ETH-3600-141125",
    side="buy",
    order_type="limit_order",
    size=1,
    limit_price=80.0
)

# Sell higher strike call
sell_call = client.place_order(
    symbol="C-ETH-3800-141125",
    side="sell",
    order_type="limit_order",
    size=1,
    limit_price=40.0
)

# Net cost: $80 - $40 = $40
# Max profit: ($3,800 - $3,600) - $40 = $160
# Max loss: $40
```

### 2. Long Straddle (Expect Big Move, Unsure Direction)

**Risk**: Limited (premium) | **Reward**: Unlimited (one side)

```python
# Assume ETH = $3,500 (at-the-money)
# Buy ATM call
buy_call = client.place_order(
    symbol="C-ETH-3500-141125",
    side="buy",
    order_type="limit_order",
    size=1,
    limit_price=90.0
)

# Buy ATM put
buy_put = client.place_order(
    symbol="P-ETH-3500-141125",
    side="buy",
    order_type="limit_order",
    size=1,
    limit_price=85.0
)

# Total cost: $90 + $85 = $175
# Breakeven: $3,325 or $3,675
# Profit if ETH moves significantly in either direction
```

### 3. Iron Condor (Expect Low Volatility)

**Risk**: Limited | **Reward**: Limited

```python
# Assume ETH = $3,500, expect it to stay between $3,400-$3,600

# Lower put spread
sell_put_3400 = client.place_order(
    symbol="P-ETH-3400-141125", side="sell",
    order_type="limit_order", size=1, limit_price=50.0
)

buy_put_3300 = client.place_order(
    symbol="P-ETH-3300-141125", side="buy",
    order_type="limit_order", size=1, limit_price=25.0
)

# Upper call spread
sell_call_3600 = client.place_order(
    symbol="C-ETH-3600-141125", side="sell",
    order_type="limit_order", size=1, limit_price=45.0
)

buy_call_3700 = client.place_order(
    symbol="C-ETH-3700-141125", side="buy",
    order_type="limit_order", size=1, limit_price=20.0
)

# Net credit: ($50 + $45) - ($25 + $20) = $50
# Max profit: $50 (if ETH stays between $3,400-$3,600)
```

---

## Managing Positions

### Check Your Options Positions

```python
# Get all ETH positions (futures + options)
positions = client.get_positions(underlying_asset_symbol="ETH")

# Filter for options only
options_positions = [p for p in positions if p.symbol.startswith(('C-', 'P-'))]

for pos in options_positions:
    option_type = "CALL" if pos.symbol.startswith('C-') else "PUT"
    side = "LONG" if pos.size > 0 else "SHORT"
    
    print(f"{option_type} | {pos.symbol}")
    print(f"  Position: {side} {abs(pos.size)} contracts")
    print(f"  Entry: ${pos.entry_price}")
    print(f"  PnL: ${pos.unrealized_pnl}")
    print()
```

### Close an Options Position

```python
# To close a LONG position: SELL
# To close a SHORT position: BUY

# Example: Close a long call position
close_order = client.place_order(
    symbol="C-ETH-3600-071125",
    side="sell",  # Opposite of original side
    order_type="market_order",  # For immediate execution
    size=5  # Same size as your position
)

print(f"Position closed! Order ID: {close_order.id}")
```

### Check Your Options Orders

```python
# Get all open orders
orders = client.get_orders(state="open")

# Filter for options only
options_orders = [o for o in orders if o.symbol.startswith(('C-', 'P-'))]

for order in options_orders:
    option_type = "CALL" if order.symbol.startswith('C-') else "PUT"
    print(f"{option_type} | {order.symbol}")
    print(f"  Order ID: {order.id}")
    print(f"  Side: {order.side.upper()}")
    print(f"  Size: {order.size}")
    print(f"  Price: ${order.limit_price}")
    print()
```

### Cancel an Options Order

```python
# Cancel a specific order
client.cancel_order(
    order_id=12345678,
    product_id=987  # Get from the order object
)

print("Order cancelled!")
```

---

## WebSocket Monitoring

### Real-Time Options Updates

```python
import asyncio
from delta_exchange import DeltaWebSocketClient

async def monitor_options():
    client = DeltaWebSocketClient(
        api_key=os.getenv("DELTA_API_KEY"),
        api_secret=os.getenv("DELTA_API_SECRET")
    )
    
    # Callback for options ticker
    def on_ticker(data):
        if data.get('symbol', '').startswith(('C-', 'P-')):
            print(f"Ticker: {data['symbol']} @ ${data.get('mark_price')}")
    
    # Callback for your options positions
    def on_position(data):
        if data.get('symbol', '').startswith(('C-', 'P-')):
            print(f"Position Update: {data['symbol']} | PnL: ${data.get('unrealized_pnl')}")
    
    # Connect
    await client.connect()
    
    # Subscribe to options ticker
    await client.subscribe_ticker(
        symbols=["C-ETH-3600-071125", "P-ETH-3400-141125"],
        callback=on_ticker
    )
    
    # Subscribe to your positions
    await client.subscribe_positions(
        symbols=["all"],
        callback=on_position
    )
    
    # Keep running
    while True:
        await asyncio.sleep(1)

asyncio.run(monitor_options())
```

---

## Risk Management

### Key Risks

1. **Time Decay (Theta)**: Options lose value as expiration approaches
2. **Volatility (Vega)**: Options prices sensitive to volatility changes
3. **Unlimited Loss**: Short calls have unlimited loss potential
4. **High Loss**: Short puts can lose up to strike price
5. **Liquidity**: Some options may have wide bid-ask spreads

### Best Practices

✅ **Start Small**: Begin with small position sizes
✅ **Understand Greeks**: Learn delta, gamma, theta, vega
✅ **Set Stop Losses**: Exit if position moves against you
✅ **Monitor Expiration**: Close or roll positions before expiry
✅ **Diversify**: Don't put all capital in one position
✅ **Use Limit Orders**: Avoid slippage with market orders
✅ **Test First**: Use paper trading to practice

❌ **Don't Sell Naked Options**: Unless you fully understand the risk
❌ **Don't Hold to Expiration**: Exit early to avoid settlement risk
❌ **Don't Over-Leverage**: Options are already leveraged instruments
❌ **Don't Ignore Fees**: Factor in trading fees and slippage

### Position Sizing

```python
# Example: Risk-based position sizing
account_balance = 10000  # $10,000
risk_per_trade = 0.02    # 2% risk per trade
max_risk = account_balance * risk_per_trade  # $200

option_premium = 80  # $80 per contract
max_contracts = max_risk / option_premium  # 2.5 → 2 contracts

# Place order with calculated size
order = client.place_order(
    symbol="C-ETH-3600-071125",
    side="buy",
    order_type="limit_order",
    size=2,  # Calculated size
    limit_price=80.0
)
```

---

## Example Scripts

We provide several example scripts:

### `test_options_basic.py`
Test basic options operations with real orders (safe test parameters)

### `examples/options_trading.py`
Complete examples of placing and managing options orders

### `examples/options_strategies.py`
Implementation of common options strategies (spreads, straddles, etc.)

### `examples/websocket_options.py`
Real-time monitoring of options prices and positions

---

## Quick Reference

### Options Trading Commands

```python
# Buy call
client.place_order(symbol="C-ETH-3600-071125", side="buy", order_type="limit_order", size=5, limit_price=80)

# Buy put
client.place_order(symbol="P-ETH-3400-141125", side="buy", order_type="limit_order", size=5, limit_price=70)

# Sell call (collect premium)
client.place_order(symbol="C-ETH-4000-071125", side="sell", order_type="limit_order", size=3, limit_price=30)

# Get options positions
positions = client.get_positions(underlying_asset_symbol="ETH")
options = [p for p in positions if p.symbol.startswith(('C-', 'P-'))]

# Close position (opposite side)
client.place_order(symbol="C-ETH-3600-071125", side="sell", order_type="market_order", size=5)

# Cancel order
client.cancel_order(order_id=12345, product_id=987)
```

---

## Additional Resources

- **Delta Exchange Docs**: https://docs.delta.exchange/
- **Options Greeks**: https://www.investopedia.com/trading/using-the-greeks-to-understand-options/
- **Options Strategies**: https://www.optionseducation.org/

---

⚠️ **DISCLAIMER**: Options trading involves significant risk and is not suitable for all investors. Only trade options if you fully understand the risks and mechanics. Past performance does not guarantee future results.

