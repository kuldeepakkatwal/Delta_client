#!/usr/bin/env python3
"""
Debug Positions - Try Different Approaches
"""

import os
import json
from dotenv import load_dotenv

load_dotenv()

from delta_exchange import DeltaRestClient

def debug_positions_advanced():
    """Try different ways to get positions"""
    
    api_key = os.getenv("DELTA_API_KEY")
    api_secret = os.getenv("DELTA_API_SECRET")
    
    client = DeltaRestClient(api_key=api_key, api_secret=api_secret)
    
    print("="*60)
    print("ADVANCED POSITIONS DEBUG")
    print("="*60)
    
    # Approach 1: Try with underlying asset symbol
    print("\n1. Try: GET /v2/positions?underlying_asset_symbol=ETH")
    try:
        response = client._request("GET", "/v2/positions", params={"underlying_asset_symbol": "ETH"})
        print("✅ Success!")
        print(json.dumps(response, indent=2))
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    # Approach 2: Try specific product IDs from the orders
    print("\n2. Try: GET /v2/positions for specific products")
    
    # Get the product symbols from your open positions
    symbols = ["C-ETH-3600-071125", "P-ETH-3600-261225"]
    
    for symbol in symbols:
        print(f"\n   Trying {symbol}...")
        try:
            # First get the product ID
            product = client.get_product(symbol)
            print(f"   Product ID: {product.id}")
            
            # Then try to get position
            response = client._request("GET", "/v2/positions", params={"product_id": product.id})
            print(f"   ✅ Success!")
            print(f"   Response: {json.dumps(response, indent=2)}")
        except Exception as e:
            print(f"   ❌ Failed: {e}")
    
    # Approach 3: Check if there's a different endpoint for options
    print("\n3. Try: GET /v2/positions (no params)")
    try:
        response = client._request("GET", "/v2/positions", params={})
        print("✅ Success!")
        print(json.dumps(response, indent=2))
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    # Approach 4: Try to get margined positions
    print("\n4. Try: GET /v2/positions/margined")
    try:
        response = client._request("GET", "/v2/positions/margined")
        print("✅ Success!")
        print(json.dumps(response, indent=2))
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    client.close()
    
    print("\n" + "="*60)

if __name__ == "__main__":
    debug_positions_advanced()

