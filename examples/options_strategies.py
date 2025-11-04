#!/usr/bin/env python3
"""
Delta Exchange - Options Strategies Examples

This script demonstrates common options trading strategies:
- Bull Call Spread
- Bear Put Spread
- Long Straddle
- Short Straddle
- Iron Condor
- Covered Call

⚠️  WARNING: Options strategies involve complex risks.
    Only use if you understand options trading completely.
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
    print("  DELTA EXCHANGE - OPTIONS STRATEGIES EXAMPLES")
    print("="*70)
    
    # ==================================================================
    # STRATEGY 1: Bull Call Spread (Moderately Bullish)
    # ==================================================================
    print("\n📈 STRATEGY 1: Bull Call Spread\n")
    print("   💡 Use when: Moderately bullish, expecting price to rise")
    print("   💡 Max Profit: Limited (Strike difference - Net premium)")
    print("   💡 Max Loss: Limited (Net premium paid)")
    print("   💡 Risk: Low to Moderate\n")
    
    print("   Setup: Assume BTC = $97,000")
    print("   1. BUY 1 Call @ $100,000 strike for $1,500 (long leg)")
    print("   2. SELL 1 Call @ $105,000 strike for $800 (short leg)")
    print("   3. Net Cost: $1,500 - $800 = $700")
    print("   4. Max Profit: ($105,000 - $100,000) - $700 = $4,300")
    print("   5. Max Loss: $700 (if BTC stays below $100,000)\n")
    
    # UNCOMMENT TO EXECUTE:
    # # Buy lower strike call
    # buy_call = client.place_order(
    #     symbol="C-BTC-100000-141125",
    #     side="buy",
    #     order_type="limit_order",
    #     size=1,
    #     limit_price=1500.0
    # )
    # 
    # # Sell higher strike call
    # sell_call = client.place_order(
    #     symbol="C-BTC-105000-141125",
    #     side="sell",
    #     order_type="limit_order",
    #     size=1,
    #     limit_price=800.0
    # )
    # print(f"   ✅ Bull Call Spread executed!")
    
    print("   ⚠️  (Commented out - uncomment to execute)\n")
    
    # ==================================================================
    # STRATEGY 2: Bear Put Spread (Moderately Bearish)
    # ==================================================================
    print("="*70)
    print("\n📉 STRATEGY 2: Bear Put Spread\n")
    print("   💡 Use when: Moderately bearish, expecting price to fall")
    print("   💡 Max Profit: Limited (Strike difference - Net premium)")
    print("   💡 Max Loss: Limited (Net premium paid)")
    print("   💡 Risk: Low to Moderate\n")
    
    print("   Setup: Assume BTC = $97,000")
    print("   1. BUY 1 Put @ $95,000 strike for $1,300 (long leg)")
    print("   2. SELL 1 Put @ $90,000 strike for $600 (short leg)")
    print("   3. Net Cost: $1,300 - $600 = $700")
    print("   4. Max Profit: ($95,000 - $90,000) - $700 = $4,300")
    print("   5. Max Loss: $700 (if BTC stays above $95,000)\n")
    
    # UNCOMMENT TO EXECUTE:
    # # Buy higher strike put
    # buy_put = client.place_order(
    #     symbol="P-BTC-95000-141125",
    #     side="buy",
    #     order_type="limit_order",
    #     size=1,
    #     limit_price=1300.0
    # )
    # 
    # # Sell lower strike put
    # sell_put = client.place_order(
    #     symbol="P-BTC-90000-141125",
    #     side="sell",
    #     order_type="limit_order",
    #     size=1,
    #     limit_price=600.0
    # )
    # print(f"   ✅ Bear Put Spread executed!")
    
    print("   ⚠️  (Commented out - uncomment to execute)\n")
    
    # ==================================================================
    # STRATEGY 3: Long Straddle (High Volatility Expected)
    # ==================================================================
    print("="*70)
    print("\n⚡ STRATEGY 3: Long Straddle\n")
    print("   💡 Use when: Expecting big move but unsure of direction")
    print("   💡 Max Profit: Unlimited (on upside), Very high (on downside)")
    print("   💡 Max Loss: Limited (Total premium paid)")
    print("   💡 Risk: Moderate (time decay works against you)\n")
    
    print("   Setup: Assume BTC = $97,000 (at-the-money)")
    print("   1. BUY 1 Call @ $97,000 strike for $2,000")
    print("   2. BUY 1 Put @ $97,000 strike for $1,900")
    print("   3. Total Cost: $2,000 + $1,900 = $3,900")
    print("   4. Breakeven Points: $93,100 (downside) or $100,900 (upside)")
    print("   5. Profit if BTC moves significantly in either direction\n")
    
    # UNCOMMENT TO EXECUTE:
    # # Buy ATM call
    # buy_call = client.place_order(
    #     symbol="C-BTC-97000-141125",
    #     side="buy",
    #     order_type="limit_order",
    #     size=1,
    #     limit_price=2000.0
    # )
    # 
    # # Buy ATM put
    # buy_put = client.place_order(
    #     symbol="P-BTC-97000-141125",
    #     side="buy",
    #     order_type="limit_order",
    #     size=1,
    #     limit_price=1900.0
    # )
    # print(f"   ✅ Long Straddle executed!")
    
    print("   ⚠️  (Commented out - uncomment to execute)\n")
    
    # ==================================================================
    # STRATEGY 4: Short Straddle (Low Volatility Expected)
    # ==================================================================
    print("="*70)
    print("\n🔻 STRATEGY 4: Short Straddle (ADVANCED - HIGH RISK)\n")
    print("   💡 Use when: Expecting no significant price movement")
    print("   💡 Max Profit: Limited (Total premium collected)")
    print("   💡 Max Loss: UNLIMITED (on upside), Very high (on downside)")
    print("   💡 Risk: VERY HIGH - Only for experienced traders\n")
    
    print("   ⚠️  WARNING: This strategy has unlimited risk!")
    print("   ⚠️  Only use if you fully understand the risks!\n")
    
    print("   Setup: Assume BTC = $97,000 (at-the-money)")
    print("   1. SELL 1 Call @ $97,000 strike for $2,000")
    print("   2. SELL 1 Put @ $97,000 strike for $1,900")
    print("   3. Total Credit: $2,000 + $1,900 = $3,900")
    print("   4. Max Profit: $3,900 (if BTC stays at $97,000)")
    print("   5. Breakeven: $93,100 (downside) or $100,900 (upside)")
    print("   6. Loss accelerates rapidly if BTC moves significantly\n")
    
    # UNCOMMENT TO EXECUTE (NOT RECOMMENDED WITHOUT EXPERIENCE):
    # # Sell ATM call
    # sell_call = client.place_order(
    #     symbol="C-BTC-97000-141125",
    #     side="sell",
    #     order_type="limit_order",
    #     size=1,
    #     limit_price=2000.0
    # )
    # 
    # # Sell ATM put
    # sell_put = client.place_order(
    #     symbol="P-BTC-97000-141125",
    #     side="sell",
    #     order_type="limit_order",
    #     size=1,
    #     limit_price=1900.0
    # )
    # print(f"   ✅ Short Straddle executed!")
    
    print("   ⚠️  (Commented out - HIGH RISK strategy)\n")
    
    # ==================================================================
    # STRATEGY 5: Iron Condor (Neutral Strategy)
    # ==================================================================
    print("="*70)
    print("\n🦅 STRATEGY 5: Iron Condor\n")
    print("   💡 Use when: Expecting price to stay in a range")
    print("   💡 Max Profit: Limited (Net premium collected)")
    print("   💡 Max Loss: Limited (Strike difference - Net premium)")
    print("   💡 Risk: Moderate\n")
    
    print("   Setup: Assume BTC = $97,000")
    print("   1. SELL 1 Put @ $95,000 for $1,000 (short put)")
    print("   2. BUY 1 Put @ $90,000 for $500 (long put)")
    print("   3. SELL 1 Call @ $100,000 for $900 (short call)")
    print("   4. BUY 1 Call @ $105,000 for $400 (long call)")
    print("   5. Net Credit: ($1,000 + $900) - ($500 + $400) = $1,000")
    print("   6. Max Profit: $1,000 (if BTC stays between $95,000-$100,000)")
    print("   7. Max Loss: $4,000 (if BTC moves outside range significantly)\n")
    
    # UNCOMMENT TO EXECUTE:
    # # Put spread (bear put spread on lower side)
    # sell_put_lower = client.place_order(
    #     symbol="P-BTC-95000-141125",
    #     side="sell",
    #     order_type="limit_order",
    #     size=1,
    #     limit_price=1000.0
    # )
    # 
    # buy_put_lower = client.place_order(
    #     symbol="P-BTC-90000-141125",
    #     side="buy",
    #     order_type="limit_order",
    #     size=1,
    #     limit_price=500.0
    # )
    # 
    # # Call spread (bull call spread on upper side)
    # sell_call_upper = client.place_order(
    #     symbol="C-BTC-100000-141125",
    #     side="sell",
    #     order_type="limit_order",
    #     size=1,
    #     limit_price=900.0
    # )
    # 
    # buy_call_upper = client.place_order(
    #     symbol="C-BTC-105000-141125",
    #     side="buy",
    #     order_type="limit_order",
    #     size=1,
    #     limit_price=400.0
    # )
    # print(f"   ✅ Iron Condor executed!")
    
    print("   ⚠️  (Commented out - uncomment to execute)\n")
    
    # ==================================================================
    # STRATEGY 6: Covered Call (Income Generation)
    # ==================================================================
    print("="*70)
    print("\n💰 STRATEGY 6: Covered Call\n")
    print("   💡 Use when: You own ETH futures and want to earn premium")
    print("   💡 Max Profit: Limited (Strike - Entry + Premium)")
    print("   💡 Max Loss: Significant (same as owning the underlying)")
    print("   💡 Risk: Moderate\n")
    
    print("   Setup: You own 1 BTC perpetual contract @ $97,000")
    print("   1. SELL 1 Call @ $105,000 strike for $1,000 (OTM call)")
    print("   2. Collect $1,000 premium immediately")
    print("   3. If BTC stays below $105,000: Keep premium + unrealized gains")
    print("   4. If BTC goes above $105,000: Gains capped at $105,000")
    print("   5. Your perpetual position provides 'coverage'\n")
    
    print("   Prerequisites:")
    print("   • Must own the underlying (BTC futures/perpetual)")
    print("   • Sell call against existing long position\n")
    
    # UNCOMMENT TO EXECUTE (only if you have a long ETH position):
    # # Check if you have a long BTC position
    # positions = client.get_positions(underlying_asset_symbol="BTC")
    # btc_futures = [p for p in positions if not p.symbol.startswith(('C-', 'P-'))]
    # 
    # if btc_futures and btc_futures[0].size > 0:
    #     # Sell call option against your position
    #     covered_call = client.place_order(
    #         symbol="C-BTC-105000-141125",
    #         side="sell",
    #         order_type="limit_order",
    #         size=1,  # Same size as your underlying position
    #         limit_price=1000.0
    #     )
    #     print(f"   ✅ Covered Call executed!")
    # else:
    #     print("   ❌ No long BTC position found - cannot execute covered call")
    
    print("   ⚠️  (Commented out - requires existing long position)\n")
    
    # ==================================================================
    # Summary
    # ==================================================================
    print("="*70)
    print("\n📚 OPTIONS STRATEGIES SUMMARY\n")
    print("   Bullish Strategies:")
    print("   • Bull Call Spread - Moderate risk, limited profit")
    print("   • Long Call - Higher risk, unlimited profit")
    print()
    print("   Bearish Strategies:")
    print("   • Bear Put Spread - Moderate risk, limited profit")
    print("   • Long Put - Higher risk, high profit potential")
    print()
    print("   Neutral Strategies:")
    print("   • Iron Condor - Range-bound profit")
    print("   • Short Straddle - High risk, profit from low volatility")
    print()
    print("   Volatility Strategies:")
    print("   • Long Straddle - Profit from big moves (either direction)")
    print()
    print("   Income Strategies:")
    print("   • Covered Call - Generate income from existing positions")
    print()
    print("   ⚠️  RISK WARNING:")
    print("   • Options are complex derivatives with significant risks")
    print("   • Always understand max profit, max loss, and breakevens")
    print("   • Start small and gain experience before scaling up")
    print("   • Consider using paper trading first")
    print()
    print("   All examples above are COMMENTED OUT for safety.")
    print("   Uncomment carefully and only if you understand the risks!\n")
    print("="*70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

