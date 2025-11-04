"""
Debug WebSocket Messages

This script will show the raw messages received from Delta Exchange
so we can see the actual data structure.
"""

import asyncio
import json
from delta_exchange import DeltaWebSocketClient

message_count = 0
max_messages = 3

async def debug_callback(data):
    """Print raw message data"""
    global message_count
    message_count += 1
    
    print("\n" + "="*60)
    print(f"RAW MESSAGE #{message_count}:")
    print("="*60)
    print(json.dumps(data, indent=2))
    print("="*60)
    
    if message_count >= max_messages:
        print(f"\n✅ Received {max_messages} messages, exiting...")
        # Will be caught in main loop


async def main():
    print("="*60)
    print("WEBSOCKET MESSAGE DEBUGGER")
    print("="*60)
    print()
    
    client = DeltaWebSocketClient()
    
    try:
        print("🔌 Connecting...")
        await client.connect()
        print("✅ Connected!")
        print()
        
        print("📡 Subscribing to ticker for BTCUSD...")
        await client.subscribe_ticker(["BTCUSD"], debug_callback)
        print("✅ Subscribed!")
        print()
        
        print(f"Waiting for messages (will show first {max_messages} messages)...")
        print("Press Ctrl+C to stop early")
        print()
        
        # Wait for messages
        while message_count < max_messages:
            await asyncio.sleep(1)
        
        print("\n✅ Debug complete!")
        
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

