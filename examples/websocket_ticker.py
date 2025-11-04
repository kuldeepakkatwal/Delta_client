"""
WebSocket Ticker Example

This example demonstrates how to subscribe to real-time ticker updates
for multiple symbols using the Delta Exchange WebSocket client.
"""

import asyncio
import os
from dotenv import load_dotenv
from delta_exchange import DeltaWebSocketClient

# Load environment variables
load_dotenv()


async def on_ticker_update(data):
    """
    Callback function for ticker updates.
    
    Args:
        data: Ticker data from the WebSocket
    """
    # Parse ticker data (data is at root level, not nested)
    symbol = data.get("symbol", "Unknown")
    mark_price = data.get("mark_price", "N/A")
    last_price = data.get("close", "N/A")
    volume = data.get("volume", "N/A")
    
    print(f"📊 {symbol}")
    print(f"   Mark Price: ${mark_price}")
    print(f"   Last Price: ${last_price}")
    print(f"   24h Volume: {volume}")
    print("-" * 40)


async def main():
    """
    Main function to run the WebSocket ticker example.
    """
    print("="*60)
    print("DELTA EXCHANGE - WEBSOCKET TICKER STREAM")
    print("="*60)
    print()
    
    # Initialize WebSocket client
    # Note: API credentials not required for public channels
    client = DeltaWebSocketClient()
    
    try:
        # Connect to WebSocket
        print("🔌 Connecting to Delta Exchange WebSocket...")
        await client.connect()
        print("✅ Connected!")
        print()
        
        # Subscribe to ticker updates for BTC and ETH
        symbols = ["BTCUSD", "ETHUSD"]
        print(f"📡 Subscribing to ticker updates for: {', '.join(symbols)}")
        await client.subscribe_ticker(symbols, on_ticker_update)
        print("✅ Subscribed!")
        print()
        
        print("Listening for ticker updates... (Press Ctrl+C to stop)")
        print("="*60)
        print()
        
        # Run the client
        await client.run()
        
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
    # Run the async main function
    asyncio.run(main())

