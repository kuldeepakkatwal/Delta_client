"""
Capture ALL WebSocket Messages

This intercepts messages before routing to see what's actually coming through.
"""

import asyncio
import json
import os
from dotenv import load_dotenv
from delta_exchange.websocket_client import DeltaWebSocketClient

# Load environment variables
load_dotenv()

# Monkey-patch to see all messages
original_route = DeltaWebSocketClient._route_message

async def debug_route(self, data):
    print("\n" + "="*60)
    print("INTERCEPTED MESSAGE:")
    print("="*60)
    msg_type = data.get("type") or data.get("channel") or "UNKNOWN"
    print(f"Message Type/Channel: {msg_type}")
    print(json.dumps(data, indent=2)[:500])  # First 500 chars
    print("="*60)
    
    # Call original
    await original_route(self, data)

DeltaWebSocketClient._route_message = debug_route


async def dummy_callback(data):
    """This should be called if routing works"""
    print(f"  ✅ CALLBACK EXECUTED! Type: {data.get('type')}")


async def main():
    print("="*60)
    print("CAPTURE ALL WEBSOCKET MESSAGES")
    print("="*60)
    print()
    
    api_key = os.getenv("DELTA_API_KEY")
    api_secret = os.getenv("DELTA_API_SECRET")
    
    if not api_key:
        print("❌ No API credentials")
        return
    
    client = DeltaWebSocketClient(api_key=api_key, api_secret=api_secret)
    
    try:
        print("🔌 Connecting...")
        await client.connect()
        await asyncio.sleep(2)
        
        print("✅ Connected & Authenticated")
        print()
        
        print("📝 Subscribing to orders...")
        await client.subscribe_orders(dummy_callback)
        print()
        
        print("📊 Subscribing to ticker (for comparison)...")
        await client.subscribe_ticker(["BTCUSD"], dummy_callback)
        print()
        
        print("⏳ Listening for 30 seconds...")
        print("   💡 Place an order in another terminal to trigger updates")
        print()
        
        await asyncio.sleep(30)
        
    except KeyboardInterrupt:
        print("\n\nInterrupted")
    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())

