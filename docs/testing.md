# Testing the Delta Exchange REST Client

This guide explains how to test the REST client implementation at different levels.

---

## 📋 Testing Levels

### 1. **Unit Testing** (No API Calls) ✅
Tests the code structure without making real API calls.

### 2. **Integration Testing** (Read-Only) ⭐ RECOMMENDED
Tests with real API credentials but only reads data (safe).

### 3. **Full Integration Testing** (Trading Enabled) ⚠️
Tests actual order placement and cancellation (use with caution).

---

## 🧪 Level 1: Unit Testing (No API Required)

### Run Validation Script

This validates the client structure without API credentials:

```bash
python3 validate_phase2.py
```

**What it tests:**
- ✅ All imports work
- ✅ Client initializes correctly
- ✅ Models parse API responses
- ✅ Enums have correct values
- ✅ All methods exist
- ✅ Context manager works

**Output:**
```
✅ PASS: Imports
✅ PASS: Client Initialization
✅ PASS: Model Parsing
✅ PASS: Enum Values
✅ PASS: Request Building
✅ PASS: Context Manager

🎉 ALL TESTS PASSED
```

---

## 🔍 Level 2: Integration Testing - Read Only (SAFE) ⭐

### Step 1: Set Up Credentials

```bash
# Copy the template
cp examples/.env.example examples/.env

# Edit and add your credentials
nano examples/.env  # or use any editor
```

In `examples/.env`:
```env
DELTA_API_KEY=your_actual_api_key_here
DELTA_API_SECRET=your_actual_api_secret_here
```

### Step 2: Run Safe Tests

```bash
# This only reads data, NO ORDERS placed
python3 test_rest_client.py
```

**What it tests:**
- ✅ Authentication with real API
- ✅ Get products
- ✅ Get wallet balances
- ✅ Get open positions
- ✅ Get open orders
- ✅ Query specific products

**Safe because:**
- No orders are placed
- No positions are opened
- No funds are risked
- Only reads account data

### Step 3: Run Examples (Read-Only)

```bash
# View your positions and balances
python3 examples/get_positions.py
```

This will show:
- Your open positions
- Wallet balances
- Available products
- No risk involved!

---

## ⚠️ Level 3: Full Integration Testing (Trading Enabled)

**WARNING:** This will place actual orders (though they are designed to be safe).

### Safety Features

The test script places SAFE orders:
- ✅ **Post-only**: Won't fill immediately
- ✅ **Far from market**: Price set at $10,000 for BTC (way below market)
- ✅ **Small size**: Minimum order size (1 contract)
- ✅ **Immediate cancel**: Order is cancelled right after placement

### How to Enable Trading Tests

Edit `test_rest_client.py` (line near the end):

```python
# Change this line:
tester.run_all_tests(enable_trading=False)

# To this:
tester.run_all_tests(enable_trading=True)
```

Or run with a flag:

```bash
# Add trading test at the end of script
python3 test_rest_client.py --enable-trading  # (if you implement arg parsing)
```

### What Trading Tests Do

1. Place a limit order far from market price
2. Verify order was created
3. Immediately cancel the order
4. Verify cancellation succeeded

**Total risk**: Minimal (order won't fill, cancelled immediately)

---

## 🎯 Recommended Testing Workflow

### For First-Time Testing

```bash
# 1. Unit tests (no credentials needed)
python3 validate_phase2.py

# 2. Set up credentials
cp examples/.env.example examples/.env
nano examples/.env  # Add your API keys

# 3. Test authentication and data access (safe)
python3 test_rest_client.py

# 4. Try read-only examples
python3 examples/get_positions.py

# 5. (Optional) Try safe order placement
python3 examples/place_order.py  # Orders are post-only and far from market
```

### For Development Testing

```python
# Quick test in Python REPL
python3

>>> from delta_exchange import DeltaRestClient
>>> import os
>>> from dotenv import load_dotenv
>>> load_dotenv()
>>> 
>>> client = DeltaRestClient(
...     api_key=os.getenv("DELTA_API_KEY"),
...     api_secret=os.getenv("DELTA_API_SECRET")
... )
>>> 
>>> # Test authentication
>>> products = client.get_products()
>>> print(f"✅ Found {len(products)} products")
>>> 
>>> # Test getting positions
>>> positions = client.get_positions()
>>> print(f"✅ Found {len(positions)} positions")
>>> 
>>> client.close()
```

---

## 📊 Test Results Interpretation

### Successful Output

```
============================================================
DELTA EXCHANGE REST CLIENT TESTING
============================================================

✅ Safe Mode: Only read operations
   No orders will be placed

============================================================
TEST 1: Client Initialization
============================================================
✅ PASS: Client Initialization - Client created successfully

============================================================
TEST 2: Authentication
============================================================
✅ PASS: Authentication - Successfully authenticated, found 50 products

[... more tests ...]

============================================================
TEST SUMMARY
============================================================
✅ PASS: Initialize Client
✅ PASS: Authentication
✅ PASS: Get Products
✅ PASS: Get Specific Product
✅ PASS: Get Wallet Balances
✅ PASS: Get Positions
✅ PASS: Get Open Orders
✅ PASS: Place and Cancel Order

============================================================
Total Tests: 8
Passed: 8 ✅
Failed: 0 ❌
Success Rate: 100.0%
============================================================

🎉 ALL TESTS PASSED!

Your REST client is working perfectly!
You can now use it in your projects.
```

### Common Issues and Solutions

#### ❌ Authentication Failed

```
❌ FAIL: Authentication - Auth failed: Authentication failed
```

**Solution:**
- Check your API key and secret in `.env`
- Verify credentials are correct on Delta Exchange website
- Ensure no extra spaces in `.env` file

#### ❌ No Products Returned

```
❌ FAIL: Get Products - No products returned
```

**Solution:**
- Your API key might not have the right permissions
- Network issue - check internet connection
- Delta Exchange API might be down

#### ❌ Rate Limit Exceeded

```
❌ FAIL: Rate limit exceeded
```

**Solution:**
- Wait a few seconds and try again
- The client has automatic retry logic built-in
- Reduce frequency of API calls

---

## 🔧 Manual Testing Commands

### Test Authentication

```bash
python3 -c "
from delta_exchange import DeltaRestClient
import os
from dotenv import load_dotenv
load_dotenv()

client = DeltaRestClient(
    api_key=os.getenv('DELTA_API_KEY'),
    api_secret=os.getenv('DELTA_API_SECRET')
)

try:
    products = client.get_products()
    print(f'✅ Authentication successful! Found {len(products)} products')
except Exception as e:
    print(f'❌ Authentication failed: {e}')
finally:
    client.close()
"
```

### Test Getting Balances

```bash
python3 -c "
from delta_exchange import DeltaRestClient
import os
from dotenv import load_dotenv
load_dotenv()

with DeltaRestClient(
    api_key=os.getenv('DELTA_API_KEY'),
    api_secret=os.getenv('DELTA_API_SECRET')
) as client:
    balances = client.get_wallet_balances()
    for b in balances:
        if float(b.balance) > 0:
            print(f'{b.asset_symbol}: {b.balance}')
"
```

### Test Getting Positions

```bash
python3 -c "
from delta_exchange import DeltaRestClient
import os
from dotenv import load_dotenv
load_dotenv()

with DeltaRestClient(
    api_key=os.getenv('DELTA_API_KEY'),
    api_secret=os.getenv('DELTA_API_SECRET')
) as client:
    positions = client.get_positions()
    if positions:
        for p in positions:
            print(f'{p.product_symbol}: {p.size} @ {p.entry_price}')
    else:
        print('No open positions')
"
```

---

## 🎓 Best Practices for Testing

### DO ✅

1. **Start with unit tests** - No risk, validates structure
2. **Test with read-only operations first** - Safe way to verify API access
3. **Use post-only orders** - Prevents accidental fills
4. **Set prices far from market** - Extra safety for limit orders
5. **Test in testnet if available** - Delta Exchange may offer a test environment
6. **Use small sizes** - Minimize risk if something goes wrong
7. **Cancel orders immediately** - Don't leave test orders hanging

### DON'T ❌

1. **Don't test with market orders** - They execute immediately
2. **Don't use production funds for testing** - Start with small amounts
3. **Don't skip validation tests** - They catch issues early
4. **Don't test during high volatility** - Prices can move quickly
5. **Don't hardcode credentials** - Always use environment variables
6. **Don't leave test orders open** - Clean up after testing

---

## 🐛 Debugging Failed Tests

### Enable Debug Output

Add this to your test script:

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Check API Response

```python
from delta_exchange import DeltaRestClient

client = DeltaRestClient(api_key="...", api_secret="...")

try:
    response = client._request("GET", "/v2/products")
    print("Raw response:", response)
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
```

---

## 📈 Next Steps After Testing

Once all tests pass:

1. **Start using the client in your project**
2. **Build your trading bot**
3. **Continue to Phase 3** (WebSocket implementation)
4. **Add more comprehensive tests** (Phase 4)

---

## 🆘 Getting Help

If tests fail:

1. Check this guide first
2. Review error messages carefully
3. Verify API credentials
4. Check Delta Exchange API status
5. Review `examples/` for working code patterns
6. Check `SPEC.md` for implementation details

---

## ✅ Testing Checklist

Before considering the client "tested":

- [ ] `validate_phase2.py` passes
- [ ] Can initialize client with credentials
- [ ] Can authenticate successfully
- [ ] Can retrieve products
- [ ] Can get wallet balances
- [ ] Can get positions
- [ ] Can query open orders
- [ ] (Optional) Can place and cancel test order

Once all checked, your REST client is ready for use! 🎉

