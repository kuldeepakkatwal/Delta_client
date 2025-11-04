"""
Test WebSocket Order Updates

This script places an order, waits, then cancels it.
Use this while running websocket_private.py in another terminal.
"""

import os
import time
from dotenv import load_dotenv
from delta_exchange import DeltaRestClient

# Load environment variables
load_dotenv()

def test_order():
    print("="*60)
    print("WEBSOCKET ORDER TEST")
    print("="*60)
    print()
    
    # Initialize client
    client = DeltaRestClient(
        api_key=os.getenv("DELTA_API_KEY"),
        api_secret=os.getenv("DELTA_API_SECRET")
    )
    
    try:
        print("📝 Placing test order...")
        order = client.place_order(
            symbol="BTCUSD",
            side="buy",
            order_type="limit_order",
            size=1,
            limit_price="20000",  # Far below market
            post_only=True
        )
        
        print(f"✅ Order placed!")
        print(f"   Order ID: {order.id}")
        print(f"   Symbol: {order.product_symbol}")
        print(f"   Price: ${order.limit_price}")
        print()
        
        print("⏳ Waiting 5 seconds (check WebSocket listener)...")
        time.sleep(5)
        
        print(f"\n❌ Cancelling order {order.id}...")
        result = client.cancel_order(
            order_id=order.id,
            product_id=order.product_id
        )
        
        print(f"✅ Order cancelled!")
        print()
        
        print("="*60)
        print("✅ TEST COMPLETE")
        print("="*60)
        print()
        print("Check your WebSocket listener - you should see:")
        print("  1. Order placement notification")
        print("  2. Order cancellation notification")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        client.close()


if __name__ == "__main__":
    test_order()

