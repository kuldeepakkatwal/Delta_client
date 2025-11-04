"""
WebSocket Orderbook Example

This example demonstrates how to subscribe to real-time orderbook updates
and trades for a specific symbol.
"""

import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
from delta_exchange import DeltaWebSocketClient

# Load environment variables
load_dotenv()


async def on_orderbook_update(data):
    """
    Callback function for orderbook updates.
    
    Args:
        data: Orderbook data from the WebSocket
    """
    # Data is at root level
    symbol = data.get("symbol", "Unknown")
    
    # Get best bid and ask from quotes
    quotes = data.get("quotes", {})
    best_bid = quotes.get("best_bid")
    best_ask = quotes.get("best_ask")
    bid_size = quotes.get("bid_size")
    ask_size = quotes.get("ask_size")
    
    if best_bid and best_ask:
        print(f"\n📖 {symbol} Orderbook")
        print(f"   Best Bid: ${best_bid} ({bid_size} contracts)")
        print(f"   Best Ask: ${best_ask} ({ask_size} contracts)")
        
        # Calculate spread
        try:
            spread = float(best_ask) - float(best_bid)
            print(f"   Spread: ${spread:.2f}")
        except:
            pass
        
        print("-" * 50)


async def on_trade_update(data):
    """
    Callback function for trade updates.
    
    Args:
        data: Trade data from the WebSocket
    """
    trades = data.get("trades", [])
    
    for trade in trades:
        symbol = trade.get("symbol", "Unknown")
        price = trade.get("price", "N/A")
        size = trade.get("size", "N/A")
        side = trade.get("buyer_role", "N/A")
        timestamp = trade.get("timestamp", 0)
        
        # Format timestamp
        dt = datetime.fromtimestamp(timestamp / 1000000) if timestamp else datetime.now()
        time_str = dt.strftime("%H:%M:%S")
        
        # Use emoji for buy/sell
        emoji = "🟢" if side == "taker" else "🔴"
        
        print(f"{emoji} [{time_str}] {symbol}: {size} @ ${price}")


async def main():
    """
    Main function to run the WebSocket orderbook example.
    """
    print("="*60)
    print("DELTA EXCHANGE - WEBSOCKET ORDERBOOK & TRADES")
    print("="*60)
    print()
    
    # Symbol to watch
    symbol = "BTCUSD"
    
    # Initialize WebSocket client
    client = DeltaWebSocketClient()
    
    try:
        # Connect to WebSocket
        print("🔌 Connecting to Delta Exchange WebSocket...")
        await client.connect()
        print("✅ Connected!")
        print()
        
        # Subscribe to orderbook updates
        print(f"📖 Subscribing to orderbook for {symbol}...")
        await client.subscribe_orderbook([symbol], on_orderbook_update)
        print("✅ Subscribed to orderbook!")
        
        # Subscribe to trade updates
        print(f"💹 Subscribing to trades for {symbol}...")
        await client.subscribe_trades([symbol], on_trade_update)
        print("✅ Subscribed to trades!")
        print()
        
        print("Listening for updates... (Press Ctrl+C to stop)")
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

