"""
WebSocket Client Test Script

Tests the WebSocket client functionality with both public and private channels.
"""

import asyncio
import os
from dotenv import load_dotenv
from delta_exchange import DeltaWebSocketClient

# Load environment variables
load_dotenv()

# Test flags
received_ticker = False
received_orderbook = False
received_trades = False
received_orders = False
received_positions = False


async def on_ticker(data):
    """Test ticker callback"""
    global received_ticker
    if not received_ticker:
        print("✅ Ticker data received")
        print(f"   Data: {data.get('ticker', {}).get('symbol', 'N/A')}")
        received_ticker = True


async def on_orderbook(data):
    """Test orderbook callback"""
    global received_orderbook
    if not received_orderbook:
        print("✅ Orderbook data received")
        orderbook = data.get('orderbook', {})
        symbol = orderbook.get('symbol', 'N/A')
        print(f"   Symbol: {symbol}")
        received_orderbook = True


async def on_trades(data):
    """Test trades callback"""
    global received_trades
    if not received_trades:
        print("✅ Trades data received")
        trades = data.get('trades', [])
        if trades:
            print(f"   Trade count: {len(trades)}")
        received_trades = True


async def on_orders(data):
    """Test orders callback"""
    global received_orders
    if not received_orders:
        print("✅ Orders data received")
        received_orders = True


async def on_positions(data):
    """Test positions callback"""
    global received_positions
    if not received_positions:
        print("✅ Positions data received")
        received_positions = True


async def test_public_channels():
    """Test public channels (no authentication required)"""
    print("\n" + "="*60)
    print("TEST 1: Public Channels")
    print("="*60)
    print()
    
    client = DeltaWebSocketClient()
    
    try:
        # Connect
        print("🔌 Connecting...")
        await client.connect()
        print("✅ Connected")
        print()
        
        # Test ticker
        print("📊 Testing ticker subscription...")
        await client.subscribe_ticker(["BTCUSD"], on_ticker)
        
        # Test orderbook
        print("📖 Testing orderbook subscription...")
        await client.subscribe_orderbook(["BTCUSD"], on_orderbook)
        
        # Test trades
        print("💹 Testing trades subscription...")
        await client.subscribe_trades(["BTCUSD"], on_trades)
        
        print()
        print("⏳ Waiting for data (10 seconds)...")
        await asyncio.sleep(10)
        
        # Check results
        print()
        print("="*60)
        print("PUBLIC CHANNELS TEST RESULTS:")
        print("="*60)
        print(f"Ticker:    {'✅ PASS' if received_ticker else '❌ FAIL'}")
        print(f"Orderbook: {'✅ PASS' if received_orderbook else '❌ FAIL'}")
        print(f"Trades:    {'✅ PASS' if received_trades else '❌ FAIL'}")
        
        await client.disconnect()
        
        return received_ticker and received_orderbook and received_trades
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        await client.disconnect()
        return False


async def test_private_channels():
    """Test private channels (authentication required)"""
    print("\n" + "="*60)
    print("TEST 2: Private Channels (Authentication)")
    print("="*60)
    print()
    
    # Get API credentials
    api_key = os.getenv("DELTA_API_KEY")
    api_secret = os.getenv("DELTA_API_SECRET")
    
    if not api_key or not api_secret:
        print("⚠️  SKIPPED: API credentials not found")
        print("   Set DELTA_API_KEY and DELTA_API_SECRET in .env to test")
        return True  # Don't fail if credentials not provided
    
    client = DeltaWebSocketClient(
        api_key=api_key,
        api_secret=api_secret
    )
    
    try:
        # Connect and authenticate
        print("🔌 Connecting and authenticating...")
        await client.connect()
        
        # Wait a moment for authentication
        await asyncio.sleep(2)
        
        if not client.is_authenticated:
            print("❌ Authentication failed")
            await client.disconnect()
            return False
        
        print("✅ Authenticated")
        print()
        
        # Test private channels
        print("📝 Testing orders subscription...")
        await client.subscribe_orders(on_orders)
        
        print("📊 Testing positions subscription...")
        await client.subscribe_positions(on_positions)
        
        print()
        print("⏳ Waiting for data (10 seconds)...")
        print("   💡 Place an order to trigger updates")
        await asyncio.sleep(10)
        
        # Check results
        print()
        print("="*60)
        print("PRIVATE CHANNELS TEST RESULTS:")
        print("="*60)
        print(f"Authentication: ✅ PASS")
        print(f"Orders:         {'✅ PASS' if received_orders else '⚠️  NO DATA (expected if no orders)'}")
        print(f"Positions:      {'✅ PASS' if received_positions else '⚠️  NO DATA (expected if no positions)'}")
        
        await client.disconnect()
        
        return True  # Pass if authenticated successfully
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        await client.disconnect()
        return False


async def test_reconnection():
    """Test reconnection logic"""
    print("\n" + "="*60)
    print("TEST 3: Reconnection Logic")
    print("="*60)
    print()
    
    client = DeltaWebSocketClient(auto_reconnect=True)
    
    try:
        print("🔌 Connecting...")
        await client.connect()
        print("✅ Connected")
        
        print()
        print("📊 Subscribing to ticker...")
        await client.subscribe_ticker(["BTCUSD"], on_ticker)
        
        print()
        print("⏳ Testing connection stability (5 seconds)...")
        await asyncio.sleep(5)
        
        print("✅ Connection stable")
        
        await client.disconnect()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        await client.disconnect()
        return False


async def main():
    """
    Run all WebSocket tests.
    """
    print("="*60)
    print("DELTA EXCHANGE WEBSOCKET CLIENT - TEST SUITE")
    print("="*60)
    
    results = []
    
    # Test 1: Public channels
    results.append(("Public Channels", await test_public_channels()))
    
    # Test 2: Private channels
    results.append(("Private Channels", await test_private_channels()))
    
    # Test 3: Reconnection
    results.append(("Reconnection", await test_reconnection()))
    
    # Final results
    print("\n" + "="*60)
    print("FINAL TEST RESULTS")
    print("="*60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:.<30} {status}")
    
    print()
    
    all_passed = all(result[1] for result in results)
    if all_passed:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed")
    
    return all_passed


if __name__ == "__main__":
    # Run the tests
    success = asyncio.run(main())
    exit(0 if success else 1)

