#!/usr/bin/env python3
"""
Debug Authentication Issues

This script helps diagnose authentication problems by showing
exactly what's being sent to the API.
"""

import os
import json
from dotenv import load_dotenv

load_dotenv()

from delta_exchange import DeltaRestClient
from delta_exchange.auth import DeltaAuth

def debug_authentication():
    """Debug authentication in detail"""
    
    api_key = os.getenv("DELTA_API_KEY")
    api_secret = os.getenv("DELTA_API_SECRET")
    
    if not api_key or not api_secret:
        print("❌ No API credentials found in .env")
        return
    
    print("="*60)
    print("AUTHENTICATION DEBUG")
    print("="*60)
    
    # Show credentials (masked)
    print(f"\n1. API Key: {api_key[:10]}...{api_key[-5:]}")
    print(f"   Secret: {api_secret[:10]}...{api_secret[-5:]}")
    
    # Test signature generation
    print("\n2. Testing signature generation...")
    auth = DeltaAuth(api_key, api_secret)
    
    timestamp = "1234567890"
    method = "GET"
    path = "/v2/positions"
    
    signature = auth.generate_signature(method, timestamp, path, "", "")
    print(f"   ✅ Signature generated: {signature[:20]}...")
    
    # Test with real client
    print("\n3. Testing actual API calls...")
    client = DeltaRestClient(api_key=api_key, api_secret=api_secret)
    
    # Test 1: Public endpoint (products)
    print("\n   Test 1: GET /v2/products (public-ish)")
    try:
        products = client.get_products()
        print(f"   ✅ SUCCESS: Got {len(products)} products")
    except Exception as e:
        print(f"   ❌ FAILED: {e}")
    
    # Test 2: Private endpoint (positions)
    print("\n   Test 2: GET /v2/positions (requires auth)")
    try:
        # Let's see the actual request details
        import time
        timestamp = str(int(time.time()))
        headers = auth.generate_headers("GET", "/v2/positions", "", "", timestamp)
        
        print(f"   Headers being sent:")
        print(f"     api-key: {headers['api-key'][:10]}...")
        print(f"     timestamp: {headers['timestamp']}")
        print(f"     signature: {headers['signature'][:20]}...")
        
        positions = client.get_positions()
        print(f"   ✅ SUCCESS: Got {len(positions)} positions")
    except Exception as e:
        print(f"   ❌ FAILED: {e}")
        
        # Show more details
        if "401" in str(e):
            print("\n   🔍 401 Error Analysis:")
            print("   This means authentication failed. Possible causes:")
            print("   1. API key doesn't have 'Read' permissions")
            print("   2. API key is restricted to certain IPs")
            print("   3. API key is for testnet, but using mainnet")
            print("   4. Signature is correct but key lacks privileges")
    
    # Test 3: Wallet balances
    print("\n   Test 3: GET /v2/wallet/balances (requires auth)")
    try:
        balances = client.get_wallet_balances()
        print(f"   ✅ SUCCESS: Got {len(balances)} balances")
    except Exception as e:
        print(f"   ❌ FAILED: {e}")
    
    client.close()
    
    print("\n" + "="*60)
    print("DIAGNOSIS")
    print("="*60)
    print("""
If products work but positions/balances fail:
→ Your API key needs additional permissions!

How to fix on Delta Exchange:
1. Go to https://www.delta.exchange/app/account-settings/api
2. Find your API key
3. Check that it has these permissions enabled:
   ✅ Read (for viewing positions, balances)
   ✅ Trade (for placing orders) - optional for testing
   
4. If permissions are correct, check:
   - Is there an IP whitelist? (disable or add your IP)
   - Are you using testnet key on mainnet? (or vice versa)
   
5. After changing permissions:
   - May need to regenerate the API key
   - Update your .env file with new key/secret
   - Try again!
    """)

if __name__ == "__main__":
    debug_authentication()

