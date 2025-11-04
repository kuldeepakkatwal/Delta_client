#!/usr/bin/env python3
"""
Example: Get Positions

This example demonstrates how to query positions on Delta Exchange.
"""

import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from delta_exchange import DeltaRestClient
from delta_exchange.exceptions import AuthenticationError, APIError

load_dotenv()

def main():
    """Main example function"""
    
    api_key = os.getenv("DELTA_API_KEY")
    api_secret = os.getenv("DELTA_API_SECRET")
    
    if not api_key or not api_secret:
        print("❌ Error: Please set DELTA_API_KEY and DELTA_API_SECRET in .env file")
        return
    
    client = DeltaRestClient(api_key=api_key, api_secret=api_secret)
    
    try:
        # Example 1: Get all positions
        print("="*60)
        print("Example 1: Get All Positions")
        print("="*60)
        
        # Get positions for all major assets
        all_positions = []
        for asset in ["BTC", "ETH", "SOL", "XRP", "BNB"]:
            positions = client.get_positions(underlying_asset_symbol=asset)
            all_positions.extend(positions)
        
        print(f"\nFound {len(all_positions)} position(s)")
        
        if all_positions:
            for i, position in enumerate(all_positions, 1):
                print(f"\n{i}. {position.product_symbol}")
                print(f"   Size: {position.size} ({'Long' if position.size > 0 else 'Short'})")
                print(f"   Entry Price: {position.entry_price}")
                print(f"   Margin: {position.margin}")
                print(f"   Liquidation Price: {position.liquidation_price}")
                print(f"   Realized PnL: {position.realized_pnl}")
                print(f"   Realized Funding: {position.realized_funding}")
        else:
            print("\nNo open positions found")
        
        # Example 2: Get wallet balances
        print("\n" + "="*60)
        print("Example 2: Get Wallet Balances")
        print("="*60)
        
        balances = client.get_wallet_balances()
        
        print(f"\nFound {len(balances)} balance(s)")
        
        for balance in balances:
            if float(balance.balance) > 0:  # Only show non-zero balances
                print(f"\n{balance.asset_symbol}:")
                print(f"   Total Balance: {balance.balance}")
                if balance.available_balance:
                    print(f"   Available: {balance.available_balance}")
                if balance.position_margin:
                    print(f"   Position Margin: {balance.position_margin}")
                if balance.order_margin:
                    print(f"   Order Margin: {balance.order_margin}")
        
        # Example 3: Get products
        print("\n" + "="*60)
        print("Example 3: Get Available Products")
        print("="*60)
        
        products = client.get_products()
        
        print(f"\nFound {len(products)} product(s)")
        print("\nShowing first 5 products:")
        
        for i, product in enumerate(products[:5], 1):
            print(f"\n{i}. {product.symbol}")
            if product.description:
                print(f"   Description: {product.description}")
            if product.contract_type:
                print(f"   Type: {product.contract_type}")
            if product.underlying_asset_symbol:
                print(f"   Underlying: {product.underlying_asset_symbol}")
        
        # Example 4: Get specific product
        print("\n" + "="*60)
        print("Example 4: Get Specific Product (BTCUSD)")
        print("="*60)
        
        try:
            btc_product = client.get_product("BTCUSD")
            print(f"\n✅ Found product: {btc_product.symbol}")
            print(f"   Product ID: {btc_product.id}")
            if btc_product.tick_size:
                print(f"   Tick Size: {btc_product.tick_size}")
            if btc_product.contract_value:
                print(f"   Contract Value: {btc_product.contract_value}")
        except APIError as e:
            print(f"\n❌ Product not found: {e}")
        
        # Example 5: Change position margin (commented out for safety)
        print("\n" + "="*60)
        print("Example 5: Change Position Margin (COMMENTED OUT)")
        print("="*60)
        print("# Uncomment to add/remove margin from a position:")
        print("""
# if positions:
#     position = positions[0]
#     updated_position = client.change_margin(
#         product_id=position.product_id,
#         delta_margin="100"  # Positive to add, negative to remove
#     )
#     print(f"Updated margin: {updated_position.margin}")
        """)
        
        print("\n" + "="*60)
        print("✅ All examples completed!")
        print("="*60)
        
    except AuthenticationError as e:
        print(f"\n❌ Authentication Error: {e}")
    
    except APIError as e:
        print(f"\n❌ API Error: {e}")
    
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
    
    finally:
        client.close()


if __name__ == "__main__":
    main()

