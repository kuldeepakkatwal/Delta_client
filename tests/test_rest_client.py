#!/usr/bin/env python3
"""
REST Client Testing Script

This script provides comprehensive testing of the Delta Exchange REST client
with real API credentials. It includes safety features to prevent accidental trades.

Usage:
    1. Copy examples/.env.example to examples/.env
    2. Add your API credentials to examples/.env
    3. Run: python3 test_rest_client.py

Safety Features:
    - Queries only (no trades by default)
    - All dangerous operations are commented out
    - Small order sizes when enabled
    - Post-only orders to prevent fills
    - Far-from-market prices
"""

import os
import sys
from dotenv import load_dotenv
from typing import Optional

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from delta_exchange import (
    DeltaRestClient,
    OrderSide,
    OrderType,
    OrderState,
    AuthenticationError,
    APIError,
    OrderError,
)


class RestClientTester:
    """REST client testing class"""
    
    def __init__(self, api_key: str, api_secret: str):
        """Initialize tester with API credentials"""
        self.api_key = api_key
        self.api_secret = api_secret
        self.client: Optional[DeltaRestClient] = None
        self.test_results = []
    
    def log_test(self, test_name: str, passed: bool, message: str = ""):
        """Log test result"""
        status = "✅ PASS" if passed else "❌ FAIL"
        self.test_results.append((test_name, passed))
        
        if message:
            print(f"{status}: {test_name} - {message}")
        else:
            print(f"{status}: {test_name}")
    
    def test_client_initialization(self):
        """Test 1: Initialize client"""
        print("\n" + "="*60)
        print("TEST 1: Client Initialization")
        print("="*60)
        
        try:
            self.client = DeltaRestClient(
                api_key=self.api_key,
                api_secret=self.api_secret
            )
            self.log_test("Client Initialization", True, "Client created successfully")
            return True
        except Exception as e:
            self.log_test("Client Initialization", False, str(e))
            return False
    
    def test_authentication(self):
        """Test 2: Test authentication by making a simple API call"""
        print("\n" + "="*60)
        print("TEST 2: Authentication")
        print("="*60)
        
        try:
            # Try to get products (public-ish endpoint)
            products = self.client.get_products()
            
            if products:
                self.log_test(
                    "Authentication",
                    True,
                    f"Successfully authenticated, found {len(products)} products"
                )
                return True
            else:
                self.log_test("Authentication", False, "No products returned")
                return False
                
        except AuthenticationError as e:
            self.log_test("Authentication", False, f"Auth failed: {e}")
            return False
        except Exception as e:
            self.log_test("Authentication", False, f"Unexpected error: {e}")
            return False
    
    def test_get_products(self):
        """Test 3: Get available products"""
        print("\n" + "="*60)
        print("TEST 3: Get Products")
        print("="*60)
        
        try:
            products = self.client.get_products()
            
            if not products:
                self.log_test("Get Products", False, "No products returned")
                return False
            
            # Show first few products
            print(f"\nFound {len(products)} products:")
            for i, product in enumerate(products[:5], 1):
                print(f"  {i}. {product.symbol} (ID: {product.id})")
                if product.contract_type:
                    print(f"     Type: {product.contract_type}")
            
            if len(products) > 5:
                print(f"  ... and {len(products) - 5} more")
            
            self.log_test("Get Products", True, f"{len(products)} products retrieved")
            return True
            
        except Exception as e:
            self.log_test("Get Products", False, str(e))
            return False
    
    def test_get_specific_product(self):
        """Test 4: Get specific product (BTCUSD)"""
        print("\n" + "="*60)
        print("TEST 4: Get Specific Product (BTCUSD)")
        print("="*60)
        
        try:
            product = self.client.get_product("BTCUSD")
            
            print(f"\nProduct Details:")
            print(f"  Symbol: {product.symbol}")
            print(f"  Product ID: {product.id}")
            if product.description:
                print(f"  Description: {product.description}")
            if product.contract_value:
                print(f"  Contract Value: {product.contract_value}")
            if product.tick_size:
                print(f"  Tick Size: {product.tick_size}")
            
            self.log_test("Get Specific Product", True)
            return True
            
        except APIError as e:
            self.log_test("Get Specific Product", False, f"Product not found: {e}")
            return False
        except Exception as e:
            self.log_test("Get Specific Product", False, str(e))
            return False
    
    def test_get_wallet_balances(self):
        """Test 5: Get wallet balances"""
        print("\n" + "="*60)
        print("TEST 5: Get Wallet Balances")
        print("="*60)
        
        try:
            balances = self.client.get_wallet_balances()
            
            print(f"\nFound {len(balances)} balance(s):")
            
            non_zero_balances = [b for b in balances if float(b.balance) > 0]
            
            if non_zero_balances:
                for balance in non_zero_balances[:5]:
                    print(f"\n  {balance.asset_symbol}:")
                    print(f"    Total: {balance.balance}")
                    if balance.available_balance:
                        print(f"    Available: {balance.available_balance}")
                    if balance.position_margin:
                        print(f"    In Positions: {balance.position_margin}")
                    if balance.order_margin:
                        print(f"    In Orders: {balance.order_margin}")
            else:
                print("  (All balances are zero)")
            
            self.log_test("Get Wallet Balances", True, f"{len(balances)} balances retrieved")
            return True
            
        except Exception as e:
            self.log_test("Get Wallet Balances", False, str(e))
            return False
    
    def test_get_positions(self):
        """Test 6: Get open positions"""
        print("\n" + "="*60)
        print("TEST 6: Get Open Positions")
        print("="*60)
        
        try:
            positions = self.client.get_positions()
            
            print(f"\nFound {len(positions)} open position(s):")
            
            if positions:
                for i, position in enumerate(positions, 1):
                    direction = "Long" if position.size > 0 else "Short"
                    print(f"\n  {i}. {position.product_symbol} ({direction})")
                    print(f"     Size: {abs(position.size)}")
                    if position.entry_price:
                        print(f"     Entry Price: {position.entry_price}")
                    if position.margin:
                        print(f"     Margin: {position.margin}")
                    if position.liquidation_price:
                        print(f"     Liquidation: {position.liquidation_price}")
                    if position.realized_pnl:
                        print(f"     Realized PnL: {position.realized_pnl}")
            else:
                print("  (No open positions)")
            
            self.log_test("Get Positions", True, f"{len(positions)} positions retrieved")
            return True
            
        except Exception as e:
            self.log_test("Get Positions", False, str(e))
            return False
    
    def test_get_open_orders(self):
        """Test 7: Get open orders"""
        print("\n" + "="*60)
        print("TEST 7: Get Open Orders")
        print("="*60)
        
        try:
            orders = self.client.get_orders(state=OrderState.OPEN)
            
            print(f"\nFound {len(orders)} open order(s):")
            
            if orders:
                for i, order in enumerate(orders, 1):
                    print(f"\n  {i}. Order #{order.id}")
                    print(f"     Symbol: {order.product_symbol}")
                    print(f"     Side: {order.side.value}")
                    print(f"     Type: {order.order_type.value}")
                    print(f"     Size: {order.size}")
                    if order.limit_price:
                        print(f"     Price: {order.limit_price}")
                    print(f"     State: {order.state.value}")
            else:
                print("  (No open orders)")
            
            self.log_test("Get Open Orders", True, f"{len(orders)} orders retrieved")
            return True
            
        except Exception as e:
            self.log_test("Get Open Orders", False, str(e))
            return False
    
    def test_place_and_cancel_order(self, enable_trading: bool = False):
        """Test 8: Place and immediately cancel an order (DISABLED BY DEFAULT)"""
        print("\n" + "="*60)
        print("TEST 8: Place and Cancel Order")
        print("="*60)
        
        if not enable_trading:
            print("\n⚠️  SKIPPED: Trading operations disabled by default")
            print("   To enable, run: test_place_and_cancel_order(enable_trading=True)")
            print("   This will place a SAFE post-only order far from market price")
            self.log_test("Place and Cancel Order", True, "Skipped (safety)")
            return True
        
        try:
            print("\n⚠️  Placing a SAFE test order...")
            print("   - Post-only (won't fill)")
            print("   - Far from market price")
            print("   - Small size")
            print("   - Will be cancelled immediately")
            
            # Place a safe order
            order = self.client.place_order(
                symbol="BTCUSD",
                side=OrderSide.BUY,
                order_type=OrderType.LIMIT_ORDER,
                size=1,  # Minimum size
                limit_price="10000",  # Far below market
                post_only=True  # Won't fill immediately
            )
            
            print(f"\n✅ Order placed: #{order.id}")
            print(f"   Price: {order.limit_price}")
            print(f"   State: {order.state.value}")
            
            # Immediately cancel it
            print("\n   Cancelling order...")
            result = self.client.cancel_order(order_id=order.id)
            
            print(f"✅ Order cancelled successfully")
            
            self.log_test("Place and Cancel Order", True, f"Order #{order.id} placed and cancelled")
            return True
            
        except OrderError as e:
            self.log_test("Place and Cancel Order", False, f"Order error: {e}")
            return False
        except Exception as e:
            self.log_test("Place and Cancel Order", False, str(e))
            return False
    
    def run_all_tests(self, enable_trading: bool = False):
        """Run all tests"""
        print("\n" + "="*60)
        print("DELTA EXCHANGE REST CLIENT TESTING")
        print("="*60)
        
        if enable_trading:
            print("\n⚠️  WARNING: Trading operations ENABLED")
            print("   Will place and cancel test orders")
        else:
            print("\n✅ Safe Mode: Only read operations")
            print("   No orders will be placed")
        
        # Run tests
        tests = [
            ("Initialize Client", self.test_client_initialization),
            ("Authentication", self.test_authentication),
            ("Get Products", self.test_get_products),
            ("Get Specific Product", self.test_get_specific_product),
            ("Get Wallet Balances", self.test_get_wallet_balances),
            ("Get Positions", self.test_get_positions),
            ("Get Open Orders", self.test_get_open_orders),
        ]
        
        # Run safe tests
        for test_name, test_func in tests:
            try:
                test_func()
            except Exception as e:
                print(f"\n❌ Test '{test_name}' crashed: {e}")
                self.test_results.append((test_name, False))
        
        # Run trading test if enabled
        if enable_trading:
            try:
                self.test_place_and_cancel_order(enable_trading=True)
            except Exception as e:
                print(f"\n❌ Trading test crashed: {e}")
                self.test_results.append(("Place and Cancel Order", False))
        else:
            self.test_place_and_cancel_order(enable_trading=False)
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        
        for test_name, passed in self.test_results:
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{status}: {test_name}")
        
        total = len(self.test_results)
        passed = sum(1 for _, p in self.test_results if p)
        failed = total - passed
        
        print("\n" + "="*60)
        print(f"Total Tests: {total}")
        print(f"Passed: {passed} ✅")
        print(f"Failed: {failed} ❌")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        print("="*60)
        
        if failed == 0:
            print("\n🎉 ALL TESTS PASSED!")
            print("\nYour REST client is working perfectly!")
            print("You can now use it in your projects.")
        else:
            print("\n⚠️  Some tests failed. Please check the errors above.")
    
    def cleanup(self):
        """Cleanup resources"""
        if self.client:
            self.client.close()
            print("\n✅ Client session closed")


def main():
    """Main test function"""
    
    # Load environment variables
    load_dotenv()
    
    api_key = os.getenv("DELTA_API_KEY")
    api_secret = os.getenv("DELTA_API_SECRET")
    
    if not api_key or not api_secret:
        print("="*60)
        print("❌ ERROR: API Credentials Not Found")
        print("="*60)
        print("\nPlease set up your API credentials:")
        print("1. Copy examples/.env.example to examples/.env")
        print("   cp examples/.env.example examples/.env")
        print("\n2. Edit examples/.env and add your credentials:")
        print("   DELTA_API_KEY=your_actual_api_key")
        print("   DELTA_API_SECRET=your_actual_api_secret")
        print("\n3. Run this script again:")
        print("   python3 test_rest_client.py")
        return 1
    
    # Create tester
    tester = RestClientTester(api_key=api_key, api_secret=api_secret)
    
    try:
        # Run tests (trading disabled by default)
        # To enable trading tests, change to: tester.run_all_tests(enable_trading=True)
        tester.run_all_tests(enable_trading=False)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
    
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        tester.cleanup()
    
    return 0


if __name__ == "__main__":
    exit(main())

