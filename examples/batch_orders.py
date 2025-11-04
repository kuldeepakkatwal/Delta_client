#!/usr/bin/env python3
"""
Example: Batch Operations

This example demonstrates how to perform batch operations on Delta Exchange,
including placing, editing, and cancelling multiple orders at once.
"""

import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from delta_exchange import DeltaRestClient, OrderSide, OrderType
from delta_exchange.exceptions import OrderError, AuthenticationError

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
        # Example 1: Place batch orders
        print("="*60)
        print("Example 1: Place Batch Orders")
        print("="*60)
        
        print("\nPlacing 3 orders in a single batch request...")
        
        orders_to_place = [
            {
                "side": "buy",
                "size": 1,
                "order_type": "limit_order",
                "limit_price": "30000",
                "post_only": True
            },
            {
                "side": "buy",
                "size": 1,
                "order_type": "limit_order",
                "limit_price": "30100",
                "post_only": True
            },
            {
                "side": "buy",
                "size": 1,
                "order_type": "limit_order",
                "limit_price": "30200",
                "post_only": True
            }
        ]
        
        placed_orders = client.place_batch_orders(
            symbol="BTCUSD",
            orders=orders_to_place
        )
        
        print(f"✅ Successfully placed {len(placed_orders)} orders!")
        
        order_ids = []
        for i, order in enumerate(placed_orders, 1):
            print(f"\n{i}. Order ID: {order.id}")
            print(f"   Price: {order.limit_price}")
            print(f"   Size: {order.size}")
            print(f"   State: {order.state.value}")
            order_ids.append(order.id)
        
        # Example 2: Edit batch orders
        print("\n" + "="*60)
        print("Example 2: Edit Batch Orders")
        print("="*60)
        
        print("\nEditing prices of all orders...")
        
        orders_to_edit = [
            {
                "id": order_ids[0],
                "limit_price": "30050"
            },
            {
                "id": order_ids[1],
                "limit_price": "30150"
            },
            {
                "id": order_ids[2],
                "limit_price": "30250"
            }
        ]
        
        edited_orders = client.edit_batch_orders(
            symbol="BTCUSD",
            orders=orders_to_edit
        )
        
        print(f"✅ Successfully edited {len(edited_orders)} orders!")
        
        for i, order in enumerate(edited_orders, 1):
            print(f"\n{i}. Order ID: {order.id}")
            print(f"   New Price: {order.limit_price}")
            print(f"   State: {order.state.value}")
        
        # Example 3: Cancel batch orders
        print("\n" + "="*60)
        print("Example 3: Cancel Batch Orders")
        print("="*60)
        
        print(f"\nCancelling {len(order_ids)} orders in a single batch request...")
        
        cancel_results = client.cancel_batch_orders(
            order_ids=order_ids,
            symbol="BTCUSD"
        )
        
        print(f"✅ Successfully cancelled {len(cancel_results)} orders!")
        
        # Example 4: Place orders on both sides
        print("\n" + "="*60)
        print("Example 4: Place Orders on Both Sides")
        print("="*60)
        
        print("\nPlacing buy and sell orders simultaneously...")
        
        both_sides_orders = [
            # Buy orders
            {
                "side": "buy",
                "size": 1,
                "order_type": "limit_order",
                "limit_price": "29000",
                "post_only": True
            },
            {
                "side": "buy",
                "size": 1,
                "order_type": "limit_order",
                "limit_price": "29500",
                "post_only": True
            },
            # Sell orders
            {
                "side": "sell",
                "size": 1,
                "order_type": "limit_order",
                "limit_price": "70000",
                "post_only": True
            },
            {
                "side": "sell",
                "size": 1,
                "order_type": "limit_order",
                "limit_price": "70500",
                "post_only": True
            }
        ]
        
        both_orders = client.place_batch_orders(
            symbol="BTCUSD",
            orders=both_sides_orders
        )
        
        print(f"✅ Placed {len(both_orders)} orders on both sides!")
        
        buy_orders = [o for o in both_orders if o.side.value == "buy"]
        sell_orders = [o for o in both_orders if o.side.value == "sell"]
        
        print(f"\nBuy orders: {len(buy_orders)}")
        for order in buy_orders:
            print(f"   ID {order.id}: {order.limit_price}")
        
        print(f"\nSell orders: {len(sell_orders)}")
        for order in sell_orders:
            print(f"   ID {order.id}: {order.limit_price}")
        
        # Clean up - cancel all orders
        print("\n" + "="*60)
        print("Cleanup: Cancelling All Orders")
        print("="*60)
        
        all_order_ids = [o.id for o in both_orders]
        client.cancel_batch_orders(order_ids=all_order_ids)
        
        print(f"✅ Cleaned up all test orders")
        
        print("\n" + "="*60)
        print("✅ All batch operations completed!")
        print("="*60)
        
        print("\n💡 Key Benefits of Batch Operations:")
        print("   • Reduced latency (single network round-trip)")
        print("   • Atomic operations (all succeed or all fail)")
        print("   • Better rate limit efficiency")
        print("   • Ideal for market making and algorithmic trading")
        
    except AuthenticationError as e:
        print(f"\n❌ Authentication Error: {e}")
    
    except OrderError as e:
        print(f"\n❌ Order Error: {e}")
    
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        client.close()


if __name__ == "__main__":
    main()

