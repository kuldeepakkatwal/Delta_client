"""
WebSocket Private Channels Example

This example demonstrates how to subscribe to real-time updates for:
- Orders
- Positions
- User Trades

Requires API credentials with appropriate permissions.
"""

import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
from delta_exchange import DeltaWebSocketClient

# Load environment variables
load_dotenv()


async def on_order_update(data):
    """
    Callback function for order updates.
    
    Args:
        data: Order data from the WebSocket
    """
    # Check if it's a snapshot (array of orders) or single order update
    if data.get("action") == "snapshot":
        # Snapshot contains array of orders
        orders = data.get("result", [])
        for order in orders:
            print_order(order)
        return
    
    # Single order update (data is at root level)
    print_order(data)


def print_order(order):
    """Helper function to print order data"""
    order_id = order.get("id", "N/A")
    symbol = order.get("product_symbol") or order.get("symbol", "Unknown")
    side = order.get("side", "N/A")
    size = order.get("size", "N/A")
    price = order.get("limit_price", order.get("stop_price", "Market"))
    state = order.get("state", "N/A")
    
    # Use emoji for order state
    emoji_map = {
        "open": "🟢",
        "pending": "🟡",
        "closed": "✅",
        "cancelled": "❌",
        "filled": "✅"
    }
    emoji = emoji_map.get(state, "📝")
    
    print(f"\n{emoji} ORDER UPDATE")
    print(f"   ID: {order_id}")
    print(f"   Symbol: {symbol}")
    print(f"   Side: {side.upper()}")
    print(f"   Size: {size}")
    print(f"   Price: ${price}")
    print(f"   State: {state.upper()}")
    print("-" * 50)


async def on_position_update(data):
    """
    Callback function for position updates.
    
    Args:
        data: Position data from the WebSocket
    """
    # Check if it's a snapshot or single position update
    if data.get("action") == "snapshot":
        positions = data.get("result", [])
        for position in positions:
            print_position(position)
        return
    
    # Single position update
    print_position(data)


def print_position(position):
    """Helper function to print position data"""
    symbol = position.get("product_symbol") or position.get("symbol", "Unknown")
    size = position.get("size", 0)
    entry_price = position.get("entry_price", "N/A")
    mark_price = position.get("mark_price", "N/A")
    unrealized_pnl = position.get("unrealized_pnl", 0)
    
    # Determine if long or short
    position_type = "LONG 📈" if size > 0 else "SHORT 📉" if size < 0 else "FLAT"
    
    # Color for PnL
    pnl_emoji = "🟢" if float(unrealized_pnl) > 0 else "🔴" if float(unrealized_pnl) < 0 else "⚪"
    
    print(f"\n📊 POSITION UPDATE")
    print(f"   Symbol: {symbol}")
    print(f"   Type: {position_type}")
    print(f"   Size: {abs(size)}")
    print(f"   Entry: ${entry_price}")
    print(f"   Mark: ${mark_price}")
    print(f"   {pnl_emoji} Unrealized PnL: ${unrealized_pnl}")
    print("-" * 50)


async def on_user_trade_update(data):
    """
    Callback function for user trade updates (fills).
    
    Args:
        data: Trade data from the WebSocket
    """
    # Check if it's a snapshot or single trade update
    if data.get("action") == "snapshot":
        trades = data.get("result", [])
        for trade in trades:
            print_trade(trade)
        return
    
    # Single trade update
    print_trade(data)


def print_trade(trade):
    """Helper function to print trade data"""
    symbol = trade.get("product_symbol") or trade.get("symbol", "Unknown")
    side = trade.get("side", "N/A")
    size = trade.get("size", "N/A")
    price = trade.get("price", "N/A")
    commission = trade.get("commission", "0")
    role = trade.get("role", "N/A")
    
    # Format timestamp
    timestamp = trade.get("created_at", "")
    time_str = timestamp[:19] if timestamp else "Unknown"
    
    emoji = "✅"
    
    print(f"\n{emoji} TRADE EXECUTED")
    print(f"   Time: {time_str}")
    print(f"   Symbol: {symbol}")
    print(f"   Side: {side.upper()}")
    print(f"   Size: {size}")
    print(f"   Price: ${price}")
    print(f"   Role: {role}")
    print(f"   Commission: ${commission}")
    print("-" * 50)


async def main():
    """
    Main function to run the WebSocket private channels example.
    """
    print("="*60)
    print("DELTA EXCHANGE - WEBSOCKET PRIVATE CHANNELS")
    print("="*60)
    print()
    
    # Get API credentials
    api_key = os.getenv("DELTA_API_KEY")
    api_secret = os.getenv("DELTA_API_SECRET")
    
    if not api_key or not api_secret:
        print("❌ Error: API credentials not found in .env file")
        print()
        print("Please set:")
        print("  DELTA_API_KEY=your_api_key")
        print("  DELTA_API_SECRET=your_api_secret")
        return
    
    # Initialize WebSocket client with authentication
    client = DeltaWebSocketClient(
        api_key=api_key,
        api_secret=api_secret
    )
    
    try:
        # Connect to WebSocket
        print("🔌 Connecting to Delta Exchange WebSocket...")
        await client.connect()
        print("✅ Connected and authenticated!")
        print()
        
        # Subscribe to order updates (use ["all"] to monitor all symbols)
        print("📝 Subscribing to order updates...")
        await client.subscribe_orders(on_order_update, ["all"])
        print("✅ Subscribed to orders!")
        
        # Subscribe to position updates
        print("📊 Subscribing to position updates...")
        await client.subscribe_positions(on_position_update, ["all"])
        print("✅ Subscribed to positions!")
        
        # Subscribe to user trade updates
        print("💹 Subscribing to trade updates...")
        await client.subscribe_user_trades(on_user_trade_update, ["all"])
        print("✅ Subscribed to trades!")
        print()
        
        print("Listening for updates... (Press Ctrl+C to stop)")
        print("="*60)
        print()
        print("💡 Tip: Place or edit orders to see real-time updates!")
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

