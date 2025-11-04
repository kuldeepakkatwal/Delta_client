#!/usr/bin/env python3
"""
Debug Positions API Response

This script shows the raw API response for positions to help debug parsing issues.
"""

import os
import json
from dotenv import load_dotenv

load_dotenv()

from delta_exchange import DeltaRestClient

def debug_positions():
    """Debug positions API response"""
    
    api_key = os.getenv("DELTA_API_KEY")
    api_secret = os.getenv("DELTA_API_SECRET")
    
    client = DeltaRestClient(api_key=api_key, api_secret=api_secret)
    
    print("="*60)
    print("POSITIONS API DEBUG")
    print("="*60)
    
    # Make raw API request to see actual response
    print("\n1. Making raw API request to /v2/positions...")
    
    try:
        response = client._request("GET", "/v2/positions")
        
        print("\n2. Raw API Response:")
        print("-"*60)
        print(json.dumps(response, indent=2))
        print("-"*60)
        
        # Check what's in the result
        result = response.get("result", [])
        
        print(f"\n3. Result type: {type(result)}")
        print(f"   Result value: {result}")
        
        if isinstance(result, list):
            print(f"   List length: {len(result)}")
            if result:
                print(f"   First item: {result[0]}")
        elif isinstance(result, dict):
            print(f"   Dict keys: {result.keys()}")
        
        # Try to parse positions
        print("\n4. Trying to parse positions...")
        positions = client.get_positions()
        print(f"   Parsed {len(positions)} positions")
        
        if positions:
            for i, pos in enumerate(positions, 1):
                print(f"\n   Position {i}:")
                print(f"     Symbol: {pos.product_symbol}")
                print(f"     Size: {pos.size}")
                print(f"     Entry Price: {pos.entry_price}")
        else:
            print("   ⚠️  No positions parsed (but UI shows 2 positions!)")
            print("\n   Possible issues:")
            print("   - API returns different format for options positions")
            print("   - Need to filter by contract type")
            print("   - Positions might be in a nested structure")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        client.close()
    
    print("\n" + "="*60)
    print("DEBUG COMPLETE")
    print("="*60)

if __name__ == "__main__":
    debug_positions()

