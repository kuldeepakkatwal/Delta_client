#!/usr/bin/env python3
"""
Example: Cancel Orders

This example demonstrates how to cancel orders on Delta Exchange.
"""

import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from delta_exchange import DeltaRestClient, OrderSide, OrderType, OrderState
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
        # First, get all open orders
        print("="*60)
        print("Fetching Open Orders")
        print("="*60)
        
        open_orders = client.get_orders(state=OrderState.OPEN)
        
        print(f"\nFound {len(open_orders)} open order(s)")
        
        if not open_orders:
            print("\nNo open orders to cancel. Let's place a test order first.")
            
            # Place a test order
            test_order = client.place_order(
                symbol="BTCUSD",
                side=OrderSide.BUY,
                order_type=OrderType.LIMIT_ORDER,
                size=1,
                limit_price="25000",  # Far from market price
                post_only=True
            )
            
            print(f"✅ Test order placed: {test_order.id}")
            open_orders = [test_order]
        
        # Display open orders
        for i, order in enumerate(open_orders, 1):
            print(f"\n{i}. Order ID: {order.id}")
            print(f"   Symbol: {order.product_symbol}")
            print(f"   Side: {order.side.value}")
            print(f"   Size: {order.size}")
            print(f"   Price: {order.limit_price}")
        
        # Example 1: Cancel a single order
        if open_orders:
            print("\n" + "="*60)
            print("Example 1: Cancel Single Order")
            print("="*60)
            
            order_to_cancel = open_orders[0]
            print(f"\nCancelling order {order_to_cancel.id}...")
            
            result = client.cancel_order(order_id=order_to_cancel.id)
            print(f"✅ Order cancelled successfully!")
            print(f"   Result: {result}")
        
        # Example 2: Cancel all orders for a symbol
        print("\n" + "="*60)
        print("Example 2: Cancel All Orders for BTCUSD")
        print("="*60)
        
        # First place some test orders
        print("\nPlacing 2 test orders...")
        order1 = client.place_order(
            symbol="BTCUSD",
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT_ORDER,
            size=1,
            limit_price="25000",
            post_only=True
        )
        
        order2 = client.place_order(
            symbol="BTCUSD",
            side=OrderSide.SELL,
            order_type=OrderType.LIMIT_ORDER,
            size=1,
            limit_price="75000",
            post_only=True
        )
        
        print(f"✅ Placed orders: {order1.id}, {order2.id}")
        
        # Cancel all
        print("\nCancelling all orders for BTCUSD...")
        cancelled = client.cancel_all_orders(symbol="BTCUSD")
        
        print(f"✅ Cancelled {len(cancelled)} order(s)")
        
        # Example 3: Batch cancel orders
        print("\n" + "="*60)
        print("Example 3: Batch Cancel Orders")
        print("="*60)
        
        # Place multiple orders
        print("\nPlacing 3 test orders...")
        order_ids = []
        
        for i in range(3):
            order = client.place_order(
                symbol="BTCUSD",
                side=OrderSide.BUY,
                order_type=OrderType.LIMIT_ORDER,
                size=1,
                limit_price=str(25000 + i * 100),
                post_only=True
            )
            order_ids.append(order.id)
            print(f"   Placed order: {order.id}")
        
        # Batch cancel
        print(f"\nBatch cancelling {len(order_ids)} orders...")
        results = client.cancel_batch_orders(order_ids=order_ids)
        
        print(f"✅ Batch cancel completed!")
        print(f"   Cancelled: {len(results)} order(s)")
        
        print("\n" + "="*60)
        print("✅ All examples completed!")
        print("="*60)
        
    except AuthenticationError as e:
        print(f"\n❌ Authentication Error: {e}")
    
    except OrderError as e:
        print(f"\n❌ Order Error: {e}")
    
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
    
    finally:
        client.close()


if __name__ == "__main__":
    main()

