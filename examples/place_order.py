#!/usr/bin/env python3
"""
Example: Place Order

This example demonstrates how to place different types of orders
on Delta Exchange using the Python client library.
"""

import os
import sys
from dotenv import load_dotenv

# Add parent directory to path to import delta_exchange
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from delta_exchange import DeltaRestClient, OrderSide, OrderType
from delta_exchange.exceptions import OrderError, AuthenticationError, APIError

# Load environment variables from .env file
load_dotenv()

def main():
    """Main example function"""
    
    # Get API credentials from environment variables
    api_key = os.getenv("DELTA_API_KEY")
    api_secret = os.getenv("DELTA_API_SECRET")
    
    if not api_key or not api_secret:
        print("❌ Error: Please set DELTA_API_KEY and DELTA_API_SECRET in .env file")
        print("   Copy .env.example to .env and add your credentials")
        return
    
    # Initialize the client
    print("Initializing Delta Exchange client...")
    client = DeltaRestClient(api_key=api_key, api_secret=api_secret)
    
    try:
        # Example 1: Place a limit buy order
        print("\n" + "="*60)
        print("Example 1: Place Limit Buy Order")
        print("="*60)
        
        order = client.place_order(
            symbol="BTCUSD",
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT_ORDER,
            size=1,  # Small size for testing
            limit_price="30000",  # Set a reasonable price
            post_only=True  # Only place if it won't fill immediately
        )
        
        print(f"✅ Order placed successfully!")
        print(f"   Order ID: {order.id}")
        print(f"   Symbol: {order.product_symbol}")
        print(f"   Side: {order.side.value}")
        print(f"   Size: {order.size}")
        print(f"   Limit Price: {order.limit_price}")
        print(f"   State: {order.state.value}")
        
        # Example 2: Place a market order (commented out for safety)
        print("\n" + "="*60)
        print("Example 2: Place Market Order (COMMENTED OUT FOR SAFETY)")
        print("="*60)
        print("# Uncomment the following code to place a market order:")
        print("# WARNING: Market orders execute immediately!")
        print("""
# market_order = client.place_order(
#     symbol="BTCUSD",
#     side=OrderSide.SELL,
#     order_type=OrderType.MARKET_ORDER,
#     size=1
# )
# print(f"Market order placed: {market_order.id}")
        """)
        
        # Example 3: Place a stop-loss order
        print("\n" + "="*60)
        print("Example 3: Place Stop-Loss Order")
        print("="*60)
        
        stop_order = client.place_order(
            symbol="BTCUSD",
            side=OrderSide.SELL,
            order_type=OrderType.LIMIT_ORDER,
            size=1,
            limit_price="29500",
            stop_price="29000",  # Trigger when price drops to 29000
            stop_order_type="stop_loss_order"
        )
        
        print(f"✅ Stop-loss order placed!")
        print(f"   Order ID: {stop_order.id}")
        print(f"   Stop Price: {stop_order.stop_price}")
        print(f"   Limit Price: {stop_order.limit_price}")
        
        # Example 4: Place order with time in force
        print("\n" + "="*60)
        print("Example 4: Place IOC (Immediate or Cancel) Order")
        print("="*60)
        
        ioc_order = client.place_order(
            symbol="BTCUSD",
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT_ORDER,
            size=1,
            limit_price="30000",
            time_in_force="ioc"  # Immediate or cancel
        )
        
        print(f"✅ IOC order placed!")
        print(f"   Order ID: {ioc_order.id}")
        print(f"   Time in Force: {ioc_order.time_in_force.value if ioc_order.time_in_force else 'N/A'}")
        
        print("\n" + "="*60)
        print("✅ All examples completed successfully!")
        print("="*60)
        
    except AuthenticationError as e:
        print(f"\n❌ Authentication Error: {e}")
        print("   Please check your API key and secret")
    
    except OrderError as e:
        print(f"\n❌ Order Error: {e}")
        print("   The order could not be placed. Check the parameters.")
    
    except APIError as e:
        print(f"\n❌ API Error: {e}")
    
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
    
    finally:
        # Close the client session
        client.close()
        print("\n✅ Client session closed")


if __name__ == "__main__":
    main()

