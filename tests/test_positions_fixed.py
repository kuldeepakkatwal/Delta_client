#!/usr/bin/env python3
"""Test fixed positions functionality"""

import os
from dotenv import load_dotenv

load_dotenv()

from delta_exchange import DeltaRestClient

def test_positions():
    """Test positions retrieval"""
    
    api_key = os.getenv("DELTA_API_KEY")
    api_secret = os.getenv("DELTA_API_SECRET")
    
    client = DeltaRestClient(api_key=api_key, api_secret=api_secret)
    
    print("="*60)
    print("TESTING FIXED POSITIONS")
    print("="*60)
    
    # Test 1: Get ETH positions (should find your 2 options positions)
    print("\n1. Get ETH positions:")
    eth_positions = client.get_positions(underlying_asset_symbol="ETH")
    print(f"   Found {len(eth_positions)} ETH position(s)")
    
    for i, pos in enumerate(eth_positions, 1):
        direction = "Long" if pos.size > 0 else "Short"
        print(f"\n   Position {i}:")
        print(f"     Symbol: {pos.product_symbol}")
        print(f"     Product ID: {pos.product_id}")
        print(f"     Direction: {direction}")
        print(f"     Size: {abs(pos.size)}")
        print(f"     Entry Price: {pos.entry_price}")
    
    # Test 2: Get BTC positions
    print("\n2. Get BTC positions:")
    btc_positions = client.get_positions(underlying_asset_symbol="BTC")
    print(f"   Found {len(btc_positions)} BTC position(s)")
    
    # Test 3: Try without parameters (should handle gracefully)
    print("\n3. Get positions (no params - should handle gracefully):")
    try:
        all_positions = client.get_positions()
        print(f"   Found {len(all_positions)} position(s)")
    except Exception as e:
        print(f"   Handled gracefully: {e}")
    
    client.close()
    
    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60)
    
    if len(eth_positions) == 2:
        print("\n🎉 SUCCESS! Found your 2 ETH positions!")
        print("\n✅ To get ALL your positions, use:")
        print("   positions = client.get_positions(underlying_asset_symbol='ETH')")
        print("   # or")
        print("   positions = client.get_positions(underlying_asset_symbol='BTC')")
    else:
        print(f"\n⚠️  Expected 2 ETH positions, found {len(eth_positions)}")

if __name__ == "__main__":
    test_positions()

