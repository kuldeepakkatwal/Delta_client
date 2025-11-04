#!/usr/bin/env python3
"""
Delta Exchange - WebSocket Options Monitoring

This script demonstrates real-time monitoring of options:
- Options price updates (ticker)
- Options order book
- Your options positions updates
- Your options orders updates
"""

import os
import asyncio
from dotenv import load_dotenv
from delta_exchange import DeltaWebSocketClient

# Load environment variables
load_dotenv()

# Sample BTC options symbols to monitor
# NOTE: Replace these with actual symbols from your Delta Exchange
OPTIONS_SYMBOLS = [
    "C-BTC-100000-071125",  # BTC Call option
    "P-BTC-90000-141125",   # BTC Put option
]

async def main():
    """Main WebSocket monitoring function."""
    
    print("\n" + "="*70)
    print("  DELTA EXCHANGE - OPTIONS WEBSOCKET MONITORING")
    print("="*70 + "\n")
    
    # Initialize WebSocket client
    client = DeltaWebSocketClient(
        api_key=os.getenv("DELTA_API_KEY"),
        api_secret=os.getenv("DELTA_API_SECRET")
    )
    
    # ==================================================================
    # Callback Functions for Different Data Types
    # ==================================================================
    
    def on_options_ticker(data):
        """Handle options ticker updates."""
        symbol = data.get('symbol', 'Unknown')
        
        # Only show if it's an options contract
        if not symbol.startswith(('C-', 'P-')):
            return
        
        option_type = "CALL 📞" if symbol.startswith('C-') else "PUT 📉"
        
        mark_price = data.get('mark_price', 'N/A')
        close = data.get('close', 'N/A')
        volume = data.get('volume', 'N/A')
        turnover = data.get('turnover', 'N/A')
        oi = data.get('oi', 'N/A')  # Open Interest
        
        print(f"\n{option_type} TICKER UPDATE")
        print(f"   Symbol: {symbol}")
        print(f"   Mark Price: ${mark_price}")
        print(f"   Last Price: ${close}")
        print(f"   Volume: {volume}")
        print(f"   Open Interest: {oi}")
    
    def on_options_orderbook(data):
        """Handle options order book updates."""
        symbol = data.get('symbol', 'Unknown')
        
        # Only show if it's an options contract
        if not symbol.startswith(('C-', 'P-')):
            return
        
        option_type = "CALL 📞" if symbol.startswith('C-') else "PUT 📉"
        
        # Parse orderbook data
        if 'buy' in data and 'sell' in data:
            buy_quotes = data['buy']
            sell_quotes = data['sell']
            
            if buy_quotes and sell_quotes:
                best_bid = buy_quotes[0]
                best_ask = sell_quotes[0]
                
                bid_price = best_bid.get('price', 'N/A')
                bid_size = best_bid.get('size', 'N/A')
                ask_price = best_ask.get('price', 'N/A')
                ask_size = best_ask.get('size', 'N/A')
                
                print(f"\n{option_type} ORDER BOOK")
                print(f"   Symbol: {symbol}")
                print(f"   Best Bid: ${bid_price} ({bid_size} contracts)")
                print(f"   Best Ask: ${ask_price} ({ask_size} contracts)")
                
                # Calculate spread
                if bid_price != 'N/A' and ask_price != 'N/A':
                    try:
                        spread = float(ask_price) - float(bid_price)
                        spread_pct = (spread / float(ask_price)) * 100
                        print(f"   Spread: ${spread:.2f} ({spread_pct:.2f}%)")
                    except:
                        pass
    
    def on_options_position(data):
        """Handle options position updates."""
        symbol = data.get('symbol', 'Unknown')
        
        # Only show if it's an options contract
        if not symbol.startswith(('C-', 'P-')):
            return
        
        option_type = "CALL 📞" if symbol.startswith('C-') else "PUT 📉"
        
        size = data.get('size', 0)
        side = "LONG 📈" if size > 0 else "SHORT 📉"
        entry_price = data.get('entry_price', 'N/A')
        mark_price = data.get('mark_price', 'N/A')
        unrealized_pnl = data.get('unrealized_pnl', 'N/A')
        
        pnl_emoji = "🟢" if unrealized_pnl != 'N/A' and float(unrealized_pnl) > 0 else "🔴"
        
        print(f"\n{option_type} POSITION UPDATE")
        print(f"   Symbol: {symbol}")
        print(f"   Type: {side}")
        print(f"   Size: {abs(size)} contracts")
        print(f"   Entry Price: ${entry_price}")
        print(f"   Mark Price: ${mark_price}")
        
        if unrealized_pnl != 'N/A':
            print(f"   {pnl_emoji} Unrealized PnL: ${unrealized_pnl}")
    
    def on_options_order(data):
        """Handle options order updates."""
        symbol = data.get('symbol', 'Unknown')
        
        # Only show if it's an options contract
        if not symbol.startswith(('C-', 'P-')):
            return
        
        option_type = "CALL 📞" if symbol.startswith('C-') else "PUT 📉"
        
        order_id = data.get('id', 'N/A')
        side = data.get('side', 'N/A').upper()
        state = data.get('state', 'N/A').upper()
        size = data.get('size', 'N/A')
        unfilled_size = data.get('unfilled_size', 'N/A')
        limit_price = data.get('limit_price', 'N/A')
        
        # Color code based on state
        if state == 'OPEN':
            state_emoji = "🟡"
        elif state == 'FILLED':
            state_emoji = "🟢"
        elif state == 'CANCELLED':
            state_emoji = "⚪"
        else:
            state_emoji = "🔵"
        
        print(f"\n{option_type} ORDER UPDATE")
        print(f"   {state_emoji} State: {state}")
        print(f"   Order ID: {order_id}")
        print(f"   Symbol: {symbol}")
        print(f"   Side: {side}")
        print(f"   Size: {size} (Unfilled: {unfilled_size})")
        print(f"   Price: ${limit_price}")
    
    def on_options_trade(data):
        """Handle options trade/fill updates."""
        symbol = data.get('symbol', 'Unknown')
        
        # Only show if it's an options contract
        if not symbol.startswith(('C-', 'P-')):
            return
        
        option_type = "CALL 📞" if symbol.startswith('C-') else "PUT 📉"
        
        side = data.get('side', 'N/A').upper()
        size = data.get('size', 'N/A')
        price = data.get('price', 'N/A')
        realized_pnl = data.get('realized_pnl', 'N/A')
        
        pnl_emoji = ""
        if realized_pnl != 'N/A':
            pnl_emoji = "🟢" if float(realized_pnl) > 0 else "🔴"
        
        print(f"\n{option_type} TRADE EXECUTED ✅")
        print(f"   Symbol: {symbol}")
        print(f"   Side: {side}")
        print(f"   Size: {size} contracts")
        print(f"   Price: ${price}")
        
        if realized_pnl != 'N/A':
            print(f"   {pnl_emoji} Realized PnL: ${realized_pnl}")
    
    def on_error(error):
        """Handle WebSocket errors."""
        print(f"\n❌ WebSocket Error: {error}")
    
    # ==================================================================
    # Connect and Subscribe
    # ==================================================================
    
    print("🔌 Connecting to Delta Exchange WebSocket...")
    await client.connect()
    print("✅ Connected!\n")
    
    # Subscribe to options ticker updates
    print("📡 Subscribing to OPTIONS ticker updates...")
    for symbol in OPTIONS_SYMBOLS:
        await client.subscribe_ticker(
            symbols=[symbol],
            callback=on_options_ticker
        )
    
    # Subscribe to options order book
    print("📡 Subscribing to OPTIONS order book...")
    for symbol in OPTIONS_SYMBOLS:
        await client.subscribe_l2_orderbook(
            symbols=[symbol],
            callback=on_options_orderbook
        )
    
    # Subscribe to your options positions
    print("📡 Subscribing to YOUR OPTIONS positions...")
    await client.subscribe_positions(
        symbols=["all"],  # Monitor all your positions
        callback=on_options_position
    )
    
    # Subscribe to your options orders
    print("📡 Subscribing to YOUR OPTIONS orders...")
    await client.subscribe_orders(
        symbols=["all"],  # Monitor all your orders
        callback=on_options_order
    )
    
    # Subscribe to your options trades
    print("📡 Subscribing to YOUR OPTIONS trades...")
    await client.subscribe_user_trades(
        symbols=["all"],  # Monitor all your trades
        callback=on_options_trade
    )
    
    print("\n✅ All subscriptions active!")
    print("\n" + "="*70)
    print("  MONITORING OPTIONS - Press Ctrl+C to stop")
    print("="*70 + "\n")
    
    # Keep running until interrupted
    try:
        while True:
            await asyncio.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Stopping WebSocket monitoring...")
    
    finally:
        # Clean disconnect
        await client.disconnect()
        print("✅ Disconnected from WebSocket")
        print("\n" + "="*70)
        print("  OPTIONS MONITORING STOPPED")
        print("="*70 + "\n")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Program interrupted")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

