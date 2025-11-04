"""
Debug Private Channel Messages

This script will show the raw messages received from private channels
so we can see the actual data structure for orders and positions.
"""

import asyncio
import json
import os
from dotenv import load_dotenv
from delta_exchange import DeltaWebSocketClient

# Load environment variables
load_dotenv()

message_count = 0

async def debug_callback(data):
    """Print raw message data"""
    global message_count
    message_count += 1
    
    print("\n" + "="*60)
    print(f"PRIVATE CHANNEL MESSAGE #{message_count}:")
    print("="*60)
    print(json.dumps(data, indent=2))
    print("="*60)


async def main():
    print("="*60)
    print("PRIVATE CHANNELS MESSAGE DEBUGGER")
    print("="*60)
    print()
    
    # Get API credentials
    api_key = os.getenv("DELTA_API_KEY")
    api_secret = os.getenv("DELTA_API_SECRET")
    
    if not api_key or not api_secret:
        print("❌ Error: API credentials not found in .env file")
        return
    
    client = DeltaWebSocketClient(
        api_key=api_key,
        api_secret=api_secret
    )
    
    try:
        print("🔌 Connecting and authenticating...")
        await client.connect()
        
        # Wait a moment for authentication
        await asyncio.sleep(2)
        
        if not client.is_authenticated:
            print("❌ Authentication failed")
            await client.disconnect()
            return
        
        print("✅ Authenticated!")
        print()
        
        print("📝 Subscribing to orders...")
        await client.subscribe_orders(debug_callback)
        print("✅ Subscribed to orders!")
        
        print("📊 Subscribing to positions...")
        await client.subscribe_positions(debug_callback)
        print("✅ Subscribed to positions!")
        
        print()
        print("⏳ Listening for messages (60 seconds)...")
        print("💡 Now place or cancel an order in another terminal!")
        print()
        print("   To test, run:")
        print("   python3 -c \"from delta_exchange import DeltaRestClient; import os; from dotenv import load_dotenv; load_dotenv(); client = DeltaRestClient(os.getenv('DELTA_API_KEY'), os.getenv('DELTA_API_SECRET')); order = client.place_order('BTCUSD', 'buy', 'limit_order', 1, '20000', post_only=True); print(f'Order placed: {order.id}'); import time; time.sleep(2); client.cancel_order(order.id, order.product_id); print('Order cancelled')\"")
        print()
        
        # Wait for messages
        await asyncio.sleep(60)
        
        if message_count == 0:
            print("\n⚠️  No messages received.")
            print("   This could mean:")
            print("   1. No orders were placed/cancelled during the wait period")
            print("   2. The subscription might not be working")
            print("   3. Delta Exchange might not send updates for instant cancel")
        else:
            print(f"\n✅ Received {message_count} messages!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n🔌 Disconnecting...")
        await client.disconnect()
        print("✅ Disconnected")


if __name__ == "__main__":
    asyncio.run(main())

