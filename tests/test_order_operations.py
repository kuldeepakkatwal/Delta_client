#!/usr/bin/env python3
"""
Test Order Operations (SAFE)

This script tests order placement, editing, and cancellation with SAFE parameters:
- Post-only orders (won't fill immediately)
- Prices far from market
- Small sizes
- Immediate cancellation

Make sure your API key has TRADE permission enabled!
"""

import os
import time
from dotenv import load_dotenv

load_dotenv()

from delta_exchange import DeltaRestClient, OrderSide, OrderType, OrderState
from delta_exchange.exceptions import OrderError, AuthenticationError

def test_order_operations():
    """Test order operations safely"""
    
    api_key = os.getenv("DELTA_API_KEY")
    api_secret = os.getenv("DELTA_API_SECRET")
    
    if not api_key or not api_secret:
        print("❌ Please set API credentials in .env file")
        return
    
    client = DeltaRestClient(api_key=api_key, api_secret=api_secret)
    
    print("="*60)
    print("TESTING ORDER OPERATIONS (SAFE MODE)")
    print("="*60)
    print("\n⚠️  This will place SAFE test orders:")
    print("   • Post-only (won't fill immediately)")
    print("   • Prices far from market")
    print("   • Small sizes")
    print("   • Will be cancelled immediately")
    
    # Check if running in interactive mode
    import sys
    if sys.stdin.isatty():
        input("\nPress Enter to continue or Ctrl+C to cancel...")
    else:
        print("\n▶️  Running in automated mode, starting tests in 2 seconds...")
        time.sleep(2)
    
    try:
        # Test 1: Place a limit order
        print("\n" + "="*60)
        print("TEST 1: Place Limit Order")
        print("="*60)
        
        print("\nPlacing buy order at $20,000 (far below market)...")
        order = client.place_order(
            symbol="BTCUSD",
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT_ORDER,
            size=1,  # Minimum size
            limit_price="20000",  # Very low price
            post_only=True  # Won't fill immediately
        )
        
        print(f"✅ Order placed successfully!")
        print(f"   Order ID: {order.id}")
        print(f"   Symbol: {order.product_symbol}")
        print(f"   Side: {order.side.value}")
        print(f"   Size: {order.size}")
        print(f"   Price: {order.limit_price}")
        print(f"   State: {order.state.value}")
        
        order_id = order.id
        product_id = order.product_id
        
        # Wait a moment
        time.sleep(1)
        
        # Test 2: Get the order
        print("\n" + "="*60)
        print("TEST 2: Get Order by ID")
        print("="*60)
        
        print(f"\nFetching order {order_id}...")
        fetched_order = client.get_order(order_id)
        
        print(f"✅ Order fetched successfully!")
        print(f"   Order ID: {fetched_order.id}")
        print(f"   State: {fetched_order.state.value}")
        print(f"   Unfilled Size: {fetched_order.unfilled_size}")
        
        # Test 3: Edit the order
        print("\n" + "="*60)
        print("TEST 3: Edit Order Price")
        print("="*60)
        
        print(f"\nEditing order {order_id} price to $19,000...")
        edited_order = client.edit_order(
            order_id=order_id,
            symbol="BTCUSD",
            limit_price="19000"
        )
        
        print(f"✅ Order edited successfully!")
        print(f"   New Price: {edited_order.limit_price}")
        print(f"   State: {edited_order.state.value}")
        
        # Wait a moment
        time.sleep(1)
        
        # Test 4: Cancel the order
        print("\n" + "="*60)
        print("TEST 4: Cancel Order")
        print("="*60)
        
        print(f"\nCancelling order {order_id}...")
        result = client.cancel_order(order_id=order_id, product_id=product_id)
        
        print(f"✅ Order cancelled successfully!")
        print(f"   Result: {result}")
        
        # Test 5: Place batch orders
        print("\n" + "="*60)
        print("TEST 5: Batch Order Operations")
        print("="*60)
        
        print("\nPlacing 3 orders in a batch...")
        batch_orders = client.place_batch_orders(
            symbol="BTCUSD",
            orders=[
                {
                    "side": "buy",
                    "size": 1,
                    "order_type": "limit_order",
                    "limit_price": "21000",
                    "post_only": True
                },
                {
                    "side": "buy",
                    "size": 1,
                    "order_type": "limit_order",
                    "limit_price": "21500",
                    "post_only": True
                },
                {
                    "side": "buy",
                    "size": 1,
                    "order_type": "limit_order",
                    "limit_price": "22000",
                    "post_only": True
                }
            ]
        )
        
        print(f"✅ Batch orders placed successfully!")
        print(f"   Placed {len(batch_orders)} orders")
        
        batch_order_ids = [o.id for o in batch_orders]
        for i, order in enumerate(batch_orders, 1):
            print(f"   {i}. Order #{order.id} @ ${order.limit_price}")
        
        # Wait a moment
        time.sleep(1)
        
        # Test 6: Cancel batch orders
        print("\n" + "="*60)
        print("TEST 6: Cancel Batch Orders")
        print("="*60)
        
        print(f"\nCancelling {len(batch_order_ids)} orders...")
        cancel_results = client.cancel_batch_orders(order_ids=batch_order_ids, product_id=product_id)
        
        print(f"✅ Batch orders cancelled successfully!")
        print(f"   Cancelled {len(cancel_results)} orders")
        
        # Test 7: Verify all orders are cancelled
        print("\n" + "="*60)
        print("TEST 7: Verify Cleanup")
        print("="*60)
        
        print("\nChecking for any remaining test orders...")
        open_orders = client.get_orders(state=OrderState.OPEN)
        
        # Filter for our test orders (BTCUSD at low prices)
        test_orders = [o for o in open_orders if o.product_symbol == "BTCUSD" and 
                       o.limit_price and float(o.limit_price) < 25000]
        
        if test_orders:
            print(f"⚠️  Found {len(test_orders)} remaining test orders, cleaning up...")
            for order in test_orders:
                client.cancel_order(order_id=order.id, product_id=order.product_id)
                print(f"   Cancelled order #{order.id}")
        else:
            print(f"✅ No test orders remaining - all cleaned up!")
        
        print("\n" + "="*60)
        print("ALL TESTS PASSED! ✅")
        print("="*60)
        
        print("\n📊 Test Summary:")
        print("   ✅ Place order")
        print("   ✅ Get order by ID")
        print("   ✅ Edit order")
        print("   ✅ Cancel order")
        print("   ✅ Batch place orders")
        print("   ✅ Batch cancel orders")
        print("   ✅ Cleanup verification")
        
        print("\n🎉 Your order operations are working perfectly!")
        print("\n💡 You can now:")
        print("   • Place real orders with proper prices")
        print("   • Build trading bots")
        print("   • Automate order management")
        
    except AuthenticationError as e:
        print(f"\n❌ Authentication Error: {e}")
        print("\n💡 Make sure your API key has TRADE permission enabled:")
        print("   1. Go to: https://www.delta.exchange/app/account-settings/api")
        print("   2. Find your API key")
        print("   3. Enable 'Trade' permission")
        print("   4. Save and try again")
        
    except OrderError as e:
        print(f"\n❌ Order Error: {e}")
        print("\n💡 This could mean:")
        print("   • Insufficient balance")
        print("   • Invalid order parameters")
        print("   • Rate limit exceeded")
        
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        client.close()
        print("\n✅ Client session closed")


if __name__ == "__main__":
    try:
        test_order_operations()
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests cancelled by user")

