#!/usr/bin/env python3
"""
Delta Exchange - Options Trading Examples

This script demonstrates how to trade options (calls and puts) on Delta Exchange.

Examples include:
- Finding available options contracts
- Placing call and put option orders
- Managing options positions
- Options order book and pricing
"""

import os
from dotenv import load_dotenv
from delta_exchange import DeltaRestClient

# Load environment variables
load_dotenv()

def main():
    # Initialize client
    client = DeltaRestClient(
        api_key=os.getenv("DELTA_API_KEY"),
        api_secret=os.getenv("DELTA_API_SECRET")
    )
    
    print("\n" + "="*70)
    print("  DELTA EXCHANGE - OPTIONS TRADING EXAMPLES")
    print("="*70)
    
    # ==================================================================
    # EXAMPLE 1: Find Available Options Contracts
    # ==================================================================
    print("\n📋 EXAMPLE 1: Find Available Options Contracts\n")
    
    # Get all products
    products = client.get_products()
    
    # Filter for BTC call options
    btc_calls = [p for p in products if p.symbol.startswith("C-BTC")]
    print(f"✅ Found {len(btc_calls)} BTC Call Options")
    print("   Sample contracts:")
    for call in btc_calls[:3]:
        print(f"   - {call.symbol} (ID: {call.id})")
    
    # Filter for BTC put options
    btc_puts = [p for p in products if p.symbol.startswith("P-BTC")]
    print(f"\n✅ Found {len(btc_puts)} BTC Put Options")
    print("   Sample contracts:")
    for put in btc_puts[:3]:
        print(f"   - {put.symbol} (ID: {put.id})")
    
    # Filter for ETH options (just show count)
    eth_calls = [p for p in products if p.symbol.startswith("C-ETH")]
    eth_puts = [p for p in products if p.symbol.startswith("P-ETH")]
    print(f"\n✅ Found {len(eth_calls)} ETH Call Options")
    print(f"✅ Found {len(eth_puts)} ETH Put Options")
    
    # ==================================================================
    # EXAMPLE 2: Place a Call Option Order (Long Call)
    # ==================================================================
    print("\n" + "="*70)
    print("\n📞 EXAMPLE 2: Place a Call Option Order (Long Call)\n")
    print("💡 Long call = Bullish position, profits if price rises\n")
    
    # Choose a BTC call option (use first available from the list)
    # Replace with actual symbol from your exchange
    call_symbol = btc_calls[0].symbol if btc_calls else "C-BTC-100000-071125"  # Format: C-[Asset]-[Strike]-[DDMMYY]
    
    # Buy 1 call option at limit price $100
    print(f"   Placing BUY order for {call_symbol}")
    print(f"   Side: BUY (Long)")
    print(f"   Size: 1 contract")
    print(f"   Type: Limit Order")
    print(f"   Price: $100 per contract\n")
    
    # UNCOMMENT TO PLACE REAL ORDER:
    # call_order = client.place_order(
    #     symbol=call_symbol,
    #     side="buy",
    #     order_type="limit_order",
    #     size=1,
    #     limit_price=100.0,
    #     time_in_force="gtc"
    # )
    # print(f"✅ Call order placed! Order ID: {call_order.id}\n")
    
    print("   ⚠️  (Commented out - uncomment to place real order)")
    
    # ==================================================================
    # EXAMPLE 3: Place a Put Option Order (Long Put)
    # ==================================================================
    print("\n" + "="*70)
    print("\n📉 EXAMPLE 3: Place a Put Option Order (Long Put)\n")
    print("💡 Long put = Bearish position, profits if price drops\n")
    
    # Choose a BTC put option (use first available from the list)
    put_symbol = btc_puts[0].symbol if btc_puts else "P-BTC-90000-141125"  # Format: P-[Asset]-[Strike]-[DDMMYY]
    
    # Buy 1 put option at limit price $500
    print(f"   Placing BUY order for {put_symbol}")
    print(f"   Side: BUY (Long)")
    print(f"   Size: 1 contract")
    print(f"   Type: Limit Order")
    print(f"   Price: $500 per contract\n")
    
    # UNCOMMENT TO PLACE REAL ORDER:
    # put_order = client.place_order(
    #     symbol=put_symbol,
    #     side="buy",
    #     order_type="limit_order",
    #     size=1,
    #     limit_price=500.0,
    #     time_in_force="gtc"
    # )
    # print(f"✅ Put order placed! Order ID: {put_order.id}\n")
    
    print("   ⚠️  (Commented out - uncomment to place real order)")
    
    # ==================================================================
    # EXAMPLE 4: Sell (Write) a Call Option (Short Call)
    # ==================================================================
    print("\n" + "="*70)
    print("\n📞 EXAMPLE 4: Sell a Call Option (Short Call - Advanced)\n")
    print("💡 Short call = Neutral to bearish, collect premium\n")
    print("⚠️  WARNING: Unlimited risk if price rises significantly!\n")
    
    # Sell (write) a call option to collect premium
    call_symbol = btc_calls[0].symbol if btc_calls else "C-BTC-110000-071125"  # Out-of-the-money call
    
    print(f"   Placing SELL order for {call_symbol}")
    print(f"   Side: SELL (Short)")
    print(f"   Size: 1 contract")
    print(f"   Type: Limit Order")
    print(f"   Price: $100 per contract (collect $100 premium)\n")
    
    # UNCOMMENT TO PLACE REAL ORDER:
    # short_call_order = client.place_order(
    #     symbol=call_symbol,
    #     side="sell",
    #     order_type="limit_order",
    #     size=1,
    #     limit_price=100.0,
    #     time_in_force="gtc"
    # )
    # print(f"✅ Short call order placed! Order ID: {short_call_order.id}\n")
    
    print("   ⚠️  (Commented out - uncomment to place real order)")
    
    # ==================================================================
    # EXAMPLE 5: Check Options Positions
    # ==================================================================
    print("\n" + "="*70)
    print("\n📊 EXAMPLE 5: Check Options Positions\n")
    
    # Get all BTC positions (includes futures and options)
    btc_positions = client.get_positions(underlying_asset_symbol="BTC")
    
    # Filter for options only
    options_positions = [p for p in btc_positions if p.symbol.startswith(('C-', 'P-'))]
    
    if not options_positions:
        print("   📭 No open options positions for BTC")
    else:
        print(f"   ✅ Found {len(options_positions)} options position(s):\n")
        for pos in options_positions:
            option_type = "CALL 📞" if pos.symbol.startswith('C-') else "PUT 📉"
            side = "LONG" if pos.size > 0 else "SHORT"
            pnl_emoji = "🟢" if pos.unrealized_pnl and float(pos.unrealized_pnl) > 0 else "🔴"
            
            print(f"   {option_type} | {pos.symbol}")
            print(f"      Position: {side} {abs(pos.size)} contracts")
            print(f"      Entry: ${pos.entry_price}")
            if pos.unrealized_pnl:
                print(f"      {pnl_emoji} PnL: ${pos.unrealized_pnl}")
            print()
    
    # ==================================================================
    # EXAMPLE 6: Close an Options Position
    # ==================================================================
    print("\n" + "="*70)
    print("\n🔄 EXAMPLE 6: Close an Options Position\n")
    
    # To close a long call position (previously bought), sell it
    print("   💡 To close a LONG position: SELL the same contract")
    print("   💡 To close a SHORT position: BUY the same contract\n")
    
    # Example: Close a long call position
    call_symbol = btc_calls[0].symbol if btc_calls else "C-BTC-100000-071125"
    
    print(f"   Closing LONG position in {call_symbol}")
    print(f"   Action: SELL (to exit)")
    print(f"   Size: 1 contract (same as original position)")
    print(f"   Type: Market Order (for immediate exit)\n")
    
    # UNCOMMENT TO PLACE REAL ORDER:
    # close_order = client.place_order(
    #     symbol=call_symbol,
    #     side="sell",
    #     order_type="market_order",
    #     size=1
    # )
    # print(f"✅ Position closed! Order ID: {close_order.id}\n")
    
    print("   ⚠️  (Commented out - uncomment to place real order)")
    
    # ==================================================================
    # EXAMPLE 7: Get Options Order Book
    # ==================================================================
    print("\n" + "="*70)
    print("\n📖 EXAMPLE 7: Get Options Order Book\n")
    
    # Get a product ID for an options contract
    if btc_calls:
        product_id = btc_calls[0].id
        symbol = btc_calls[0].symbol
        
        print(f"   Fetching order book for {symbol} (ID: {product_id})")
        
        # UNCOMMENT TO FETCH REAL ORDER BOOK:
        # orderbook = client.get_l2_orderbook(product_id=product_id)
        # print(f"\n   Best Bid: ${orderbook['buy'][0]['price']} ({orderbook['buy'][0]['size']} contracts)")
        # print(f"   Best Ask: ${orderbook['sell'][0]['price']} ({orderbook['sell'][0]['size']} contracts)")
        # spread = float(orderbook['sell'][0]['price']) - float(orderbook['buy'][0]['price'])
        # print(f"   Spread: ${spread:.2f}")
        
        print("\n   ⚠️  (Commented out - uncomment to fetch real data)")
    
    # ==================================================================
    # EXAMPLE 8: Cancel an Options Order
    # ==================================================================
    print("\n" + "="*70)
    print("\n❌ EXAMPLE 8: Cancel an Options Order\n")
    
    # Get open orders
    orders = client.get_orders(state="open")
    options_orders = [o for o in orders if o.symbol.startswith(('C-', 'P-'))]
    
    if not options_orders:
        print("   📭 No open options orders to cancel")
    else:
        print(f"   ✅ Found {len(options_orders)} open options order(s):\n")
        for order in options_orders:
            option_type = "CALL 📞" if order.symbol.startswith('C-') else "PUT 📉"
            print(f"   {option_type} | Order ID: {order.id}")
            print(f"      Symbol: {order.symbol}")
            print(f"      Side: {order.side.upper()}")
            print(f"      Size: {order.size}")
            print(f"      Price: ${order.limit_price}\n")
            
            # UNCOMMENT TO CANCEL:
            # client.cancel_order(order_id=order.id, product_id=order.product_id)
            # print(f"      ✅ Cancelled!\n")
        
        print("   ⚠️  (Cancellation commented out - uncomment to cancel real orders)")
    
    # ==================================================================
    # Summary
    # ==================================================================
    print("\n" + "="*70)
    print("\n📚 OPTIONS TRADING SUMMARY\n")
    print("   Options Basics:")
    print("   • Call Option = Right to BUY at strike price (bullish)")
    print("   • Put Option = Right to SELL at strike price (bearish)")
    print()
    print("   Long vs Short:")
    print("   • Long (Buy) = Limited risk, pay premium")
    print("   • Short (Sell/Write) = Collect premium, higher risk")
    print()
    print("   Symbol Format:")
    print("   • C-BTC-100000-071125 = BTC Call, $100000 strike, exp 07/11/25")
    print("   • P-BTC-90000-141125 = BTC Put, $90000 strike, exp 14/11/25")
    print()
    print("   All examples above are COMMENTED OUT for safety.")
    print("   Uncomment the code you want to execute!\n")
    print("="*70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

