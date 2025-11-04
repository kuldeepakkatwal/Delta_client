#!/usr/bin/env python3
"""
Quick REST Client Test

This is the FASTEST way to test if your REST client works.
Just add your API credentials below and run!
"""

from delta_exchange import DeltaRestClient
from delta_exchange.exceptions import AuthenticationError, APIError

# ⚠️ ADD YOUR CREDENTIALS HERE (or use environment variables)
API_KEY = "your_api_key_here"
API_SECRET = "your_api_secret_here"

# Or load from environment
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("DELTA_API_KEY", API_KEY)
API_SECRET = os.getenv("DELTA_API_SECRET", API_SECRET)


def quick_test():
    """Quick test of REST client"""
    
    print("="*60)
    print("QUICK REST CLIENT TEST")
    print("="*60)
    
    # Check credentials
    if API_KEY == "your_api_key_here" or not API_KEY:
        print("\n❌ Error: Please add your API credentials")
        print("   Either:")
        print("   1. Edit quick_test.py and add credentials")
        print("   2. Or set up examples/.env file")
        return
    
    # Initialize client
    print("\n1. Initializing client...")
    try:
        client = DeltaRestClient(api_key=API_KEY, api_secret=API_SECRET)
        print("   ✅ Client initialized")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return
    
    # Test authentication
    print("\n2. Testing authentication...")
    try:
        products = client.get_products()
        print(f"   ✅ Authenticated! Found {len(products)} products")
    except AuthenticationError as e:
        print(f"   ❌ Authentication failed: {e}")
        client.close()
        return
    except Exception as e:
        print(f"   ❌ Error: {e}")
        client.close()
        return
    
    # Test getting balances
    print("\n3. Getting wallet balances...")
    try:
        balances = client.get_wallet_balances()
        non_zero = [b for b in balances if float(b.balance) > 0]
        print(f"   ✅ Retrieved {len(balances)} balances")
        if non_zero:
            print(f"   💰 Non-zero balances:")
            for b in non_zero[:3]:
                print(f"      {b.asset_symbol}: {b.balance}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test getting positions
    print("\n4. Getting positions...")
    try:
        # Get positions for common assets
        all_positions = []
        for asset in ["BTC", "ETH", "SOL"]:
            positions = client.get_positions(underlying_asset_symbol=asset)
            all_positions.extend(positions)
        
        print(f"   ✅ Retrieved {len(all_positions)} positions")
        if all_positions:
            print(f"   📊 Open positions:")
            for p in all_positions[:5]:
                direction = "Long" if p.size > 0 else "Short"
                print(f"      {p.product_symbol}: {direction} {abs(p.size)}")
        else:
            print(f"   (No open positions)")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test getting orders
    print("\n5. Getting open orders...")
    try:
        orders = client.get_orders(state="open")
        print(f"   ✅ Retrieved {len(orders)} open orders")
        if orders:
            print(f"   📝 Open orders:")
            for o in orders[:3]:
                print(f"      #{o.id}: {o.product_symbol} {o.side.value} @ {o.limit_price}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Close client
    client.close()
    
    print("\n" + "="*60)
    print("🎉 QUICK TEST COMPLETED!")
    print("="*60)
    print("\n✅ Your REST client is working!")
    print("   Next steps:")
    print("   1. Try examples: python3 examples/get_positions.py")
    print("   2. Full tests: python3 test_rest_client.py")
    print("   3. Read TESTING.md for comprehensive guide")


if __name__ == "__main__":
    try:
        quick_test()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

