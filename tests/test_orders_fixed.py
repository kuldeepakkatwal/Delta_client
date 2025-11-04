"""
Test Fixed Order Subscriptions

This tests if the order subscription now works with the symbols array.
"""

import asyncio
import os
import json
from dotenv import load_dotenv
from delta_exchange import DeltaWebSocketClient, DeltaRestClient

# Load environment variables
load_dotenv()

order_messages_received = 0

async def on_order(data):
    """Callback for order updates"""
    global order_messages_received
    order_messages_received += 1
    
    print("\n" + "="*60)
    print(f"🎉 ORDER UPDATE #{order_messages_received}:")
    print("="*60)
    print(json.dumps(data, indent=2)[:500])
    print("="*60)


async def main():
    print("="*60)
    print("TEST: FIXED ORDER SUBSCRIPTIONS")
    print("="*60)
    print()
    
    api_key = os.getenv("DELTA_API_KEY")
    api_secret = os.getenv("DELTA_API_SECRET")
    
    if not api_key:
        print("❌ No API credentials")
        return
    
    # Initialize WebSocket client
    ws_client = DeltaWebSocketClient(api_key=api_key, api_secret=api_secret)
    
    # Initialize REST client for placing orders
    rest_client = DeltaRestClient(api_key=api_key, api_secret=api_secret)
    
    try:
        print("🔌 Connecting WebSocket...")
        await ws_client.connect()
        await asyncio.sleep(2)
        
        if not ws_client.is_authenticated:
            print("❌ Authentication failed")
            await ws_client.disconnect()
            return
        
        print("✅ Connected & Authenticated")
        print()
        
        print("📝 Subscribing to orders with symbols=['all']...")
        await ws_client.subscribe_orders(on_order, ["all"])
        print("✅ Subscribed!")
        print()
        
        print("⏳ Waiting 2 seconds for subscription to activate...")
        await asyncio.sleep(2)
        
        print()
        print("📝 Placing test order via REST...")
        order = rest_client.place_order(
            symbol="BTCUSD",
            side="buy",
            order_type="limit_order",
            size=1,
            limit_price="20000",
            post_only=True
        )
        print(f"✅ Order placed: ID={order.id}")
        print()
        
        print("⏳ Waiting 3 seconds for WebSocket update...")
        await asyncio.sleep(3)
        
        print()
        print("❌ Cancelling order...")
        rest_client.cancel_order(order.id, order.product_id)
        print("✅ Order cancelled")
        print()
        
        print("⏳ Waiting 3 seconds for WebSocket update...")
        await asyncio.sleep(3)
        
        print()
        print("="*60)
        print("TEST RESULTS:")
        print("="*60)
        if order_messages_received > 0:
            print(f"✅ SUCCESS! Received {order_messages_received} order update(s)")
            print("   Private channels are now working!")
        else:
            print("⚠️  NO UPDATES RECEIVED")
            print("   Possible reasons:")
            print("   1. Delta Exchange may not send updates for immediately cancelled orders")
            print("   2. There may be a delay in message delivery")
            print("   3. Try leaving an order open longer")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        rest_client.close()
        await ws_client.disconnect()
        print("\n✅ Disconnected")


if __name__ == "__main__":
    asyncio.run(main())

