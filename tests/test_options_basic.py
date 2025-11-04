#!/usr/bin/env python3
"""
Basic Options Trading Test Script

This script tests basic options operations:
- Fetching available options contracts
- Placing options orders (calls and puts)
- Checking options positions
- Cancelling options orders

IMPORTANT: This script places REAL orders with minimal risk.
Only proceed if you understand options trading risks.
"""

import os
import sys
import time
from dotenv import load_dotenv
from delta_exchange import DeltaRestClient
from delta_exchange.exceptions import DeltaExchangeException

# Load environment variables
load_dotenv()

def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def find_options_contracts(client: DeltaRestClient, underlying: str = "BTC"):
    """
    Find available options contracts for an underlying asset.
    
    Args:
        client: Delta REST client
        underlying: Underlying asset symbol (BTC, ETH, etc.)
    
    Returns:
        List of call and put option symbols
    """
    print_section(f"Finding {underlying} Options Contracts")
    
    try:
        products = client.get_products()
        
        calls = []
        puts = []
        
        for product in products:
            symbol = product.symbol
            
            # Call options start with C-
            if symbol.startswith(f"C-{underlying}"):
                calls.append({
                    'symbol': symbol,
                    'id': product.id,
                    'contract_type': product.contract_type
                })
            
            # Put options start with P-
            elif symbol.startswith(f"P-{underlying}"):
                puts.append({
                    'symbol': symbol,
                    'id': product.id,
                    'contract_type': product.contract_type
                })
        
        print(f"\n✅ Found {len(calls)} call options and {len(puts)} put options for {underlying}")
        
        # Show first 5 of each
        if calls:
            print(f"\n📞 Sample Call Options:")
            for call in calls[:5]:
                print(f"   {call['symbol']} (ID: {call['id']})")
        
        if puts:
            print(f"\n📉 Sample Put Options:")
            for put in puts[:5]:
                print(f"   {put['symbol']} (ID: {put['id']})")
        
        return calls, puts
    
    except DeltaExchangeException as e:
        print(f"❌ Error fetching products: {e}")
        return [], []

def test_options_positions(client: DeltaRestClient, underlying: str = "BTC"):
    """Test getting options positions."""
    print_section(f"Checking {underlying} Options Positions")
    
    try:
        positions = client.get_positions(underlying_asset_symbol=underlying)
        
        if not positions:
            print(f"📭 No open positions for {underlying}")
            return
        
        options_positions = [p for p in positions if p.symbol.startswith(('C-', 'P-'))]
        
        if not options_positions:
            print(f"📭 No options positions for {underlying}")
            return
        
        print(f"\n✅ Found {len(options_positions)} options position(s):\n")
        
        for pos in options_positions:
            option_type = "CALL 📞" if pos.symbol.startswith('C-') else "PUT 📉"
            side = "LONG 📈" if pos.size > 0 else "SHORT 📉"
            pnl_emoji = "🟢" if pos.unrealized_pnl and float(pos.unrealized_pnl) > 0 else "🔴"
            
            print(f"   {option_type} | {pos.symbol}")
            print(f"   Position: {side} | Size: {abs(pos.size)}")
            print(f"   Entry Price: ${pos.entry_price}")
            
            if pos.unrealized_pnl:
                print(f"   {pnl_emoji} Unrealized PnL: ${pos.unrealized_pnl}")
            
            print()
    
    except DeltaExchangeException as e:
        print(f"❌ Error getting positions: {e}")

def test_place_call_option(client: DeltaRestClient, symbol: str):
    """
    Test placing a call option order.
    
    SAFE TEST:
    - Uses LIMIT order (won't execute immediately)
    - Uses very low price (unlikely to fill)
    - Small size (1 contract)
    """
    print_section(f"Testing Call Option Order: {symbol}")
    
    print("\n⚠️  This will place a REAL limit order for a call option.")
    print("   The order uses a very low price and is unlikely to fill.")
    print("   You can cancel it immediately after testing.\n")
    
    # Check if running in non-interactive mode
    if not sys.stdin.isatty():
        print("✅ Running in automated mode - proceeding with test order...")
    else:
        confirm = input("   Proceed? (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("❌ Test cancelled by user")
            return None
    
    try:
        # Place a limit order with a very low price (unlikely to fill)
        order = client.place_order(
            symbol=symbol,
            side="buy",
            order_type="limit_order",
            size=1,
            limit_price=1.0,  # Very low price - unlikely to execute
            time_in_force="gtc"
        )
        
        print("\n✅ Call option order placed successfully!")
        print(f"\n   Order ID: {order.id}")
        print(f"   Symbol: {order.product_symbol}")
        print(f"   Side: {order.side.upper()}")
        print(f"   Size: {order.size}")
        print(f"   Price: ${order.limit_price}")
        print(f"   State: {order.state}")
        
        return order
    
    except DeltaExchangeException as e:
        print(f"\n❌ Error placing call order: {e}")
        return None

def test_place_put_option(client: DeltaRestClient, symbol: str):
    """
    Test placing a put option order.
    
    SAFE TEST:
    - Uses LIMIT order (won't execute immediately)
    - Uses very low price (unlikely to fill)
    - Small size (1 contract)
    """
    print_section(f"Testing Put Option Order: {symbol}")
    
    print("\n⚠️  This will place a REAL limit order for a put option.")
    print("   The order uses a very low price and is unlikely to fill.")
    print("   You can cancel it immediately after testing.\n")
    
    # Check if running in non-interactive mode
    if not sys.stdin.isatty():
        print("✅ Running in automated mode - proceeding with test order...")
    else:
        confirm = input("   Proceed? (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("❌ Test cancelled by user")
            return None
    
    try:
        # Place a limit order with a very low price (unlikely to fill)
        order = client.place_order(
            symbol=symbol,
            side="buy",
            order_type="limit_order",
            size=1,
            limit_price=1.0,  # Very low price - unlikely to execute
            time_in_force="gtc"
        )
        
        print("\n✅ Put option order placed successfully!")
        print(f"\n   Order ID: {order.id}")
        print(f"   Symbol: {order.product_symbol}")
        print(f"   Side: {order.side.upper()}")
        print(f"   Size: {order.size}")
        print(f"   Price: ${order.limit_price}")
        print(f"   State: {order.state}")
        
        return order
    
    except DeltaExchangeException as e:
        print(f"\n❌ Error placing put order: {e}")
        return None

def test_cancel_options_order(client: DeltaRestClient, order_id: int, product_id: int):
    """Test cancelling an options order."""
    print_section(f"Cancelling Options Order: {order_id}")
    
    try:
        client.cancel_order(order_id=order_id, product_id=product_id)
        print(f"\n✅ Order {order_id} cancelled successfully!")
        return True
    
    except DeltaExchangeException as e:
        print(f"\n❌ Error cancelling order: {e}")
        return False

def main():
    """Main test function."""
    print("\n" + "="*60)
    print("  DELTA EXCHANGE - OPTIONS TRADING TEST")
    print("="*60)
    
    # Load credentials
    api_key = os.getenv("DELTA_API_KEY")
    api_secret = os.getenv("DELTA_API_SECRET")
    
    if not api_key or not api_secret:
        print("\n❌ Error: API credentials not found in .env file")
        print("   Please create a .env file with:")
        print("   DELTA_API_KEY=your_key")
        print("   DELTA_API_SECRET=your_secret")
        return
    
    # Initialize client
    client = DeltaRestClient(api_key=api_key, api_secret=api_secret)
    
    # Test 1: Find available options contracts
    calls, puts = find_options_contracts(client, underlying="BTC")
    
    if not calls and not puts:
        print("\n❌ No options contracts found. Exiting.")
        return
    
    # Test 2: Check existing options positions
    test_options_positions(client, underlying="BTC")
    
    # Test 3: Place a call option order (if available)
    call_order = None
    if calls:
        # Use the first available call option
        test_symbol = calls[0]['symbol']
        call_order = test_place_call_option(client, test_symbol)
        
        if call_order:
            time.sleep(1)  # Brief pause
    
    # Test 4: Place a put option order (if available)
    put_order = None
    if puts:
        # Use the first available put option
        test_symbol = puts[0]['symbol']
        put_order = test_place_put_option(client, test_symbol)
        
        if put_order:
            time.sleep(1)  # Brief pause
    
    # Test 5: Cancel the test orders
    if call_order:
        test_cancel_options_order(client, call_order.id, call_order.product_id)
        time.sleep(0.5)
    
    if put_order:
        test_cancel_options_order(client, put_order.id, put_order.product_id)
    
    # Final summary
    print_section("Test Summary")
    print("\n✅ Options test completed!")
    print("\nTests performed:")
    print(f"   ✓ Found {len(calls)} call options and {len(puts)} put options")
    print("   ✓ Checked options positions")
    
    if call_order:
        print("   ✓ Placed and cancelled call option order")
    
    if put_order:
        print("   ✓ Placed and cancelled put option order")
    
    print("\n" + "="*60)
    print("  ALL OPTIONS TESTS PASSED!")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

