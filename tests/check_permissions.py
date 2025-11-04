#!/usr/bin/env python3
"""
Check API Key Permissions

This script tests different endpoints to determine what permissions
your API key has.
"""

import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from delta_exchange import DeltaRestClient

load_dotenv()

def check_permissions():
    """Check what permissions the API key has"""
    
    api_key = os.getenv("DELTA_API_KEY")
    api_secret = os.getenv("DELTA_API_SECRET")
    
    if not api_key or api_secret == "your_api_secret_here":
        print("❌ Please add real API credentials to .env file")
        return
    
    print("="*60)
    print("API KEY PERMISSIONS CHECK")
    print("="*60)
    
    # Mask credentials for security
    print(f"\nAPI Key: {api_key[:8]}...{api_key[-4:]}")
    print(f"Secret:  {api_secret[:8]}...{api_secret[-4:]}")
    
    client = DeltaRestClient(api_key=api_key, api_secret=api_secret)
    
    endpoints = [
        ("Public", "GET /v2/products", lambda: client.get_products()),
        ("Read", "GET /v2/wallet/balances", lambda: client.get_wallet_balances()),
        ("Read", "GET /v2/positions", lambda: client.get_positions()),
        ("Read", "GET /v2/orders", lambda: client.get_orders()),
    ]
    
    results = []
    
    print("\n" + "="*60)
    print("TESTING ENDPOINTS")
    print("="*60)
    
    for permission, endpoint, func in endpoints:
        print(f"\n{endpoint}")
        print(f"Permission needed: {permission}")
        
        try:
            result = func()
            status = "✅ SUCCESS"
            count = len(result) if isinstance(result, list) else 1
            detail = f"Got {count} items"
            results.append((endpoint, True, detail))
            print(f"  {status}: {detail}")
        except Exception as e:
            status = "❌ FAILED"
            error = str(e)
            results.append((endpoint, False, error))
            print(f"  {status}: {error}")
    
    client.close()
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    for endpoint, success, detail in results:
        status = "✅" if success else "❌"
        print(f"{status} {endpoint}")
    
    # Diagnosis
    print("\n" + "="*60)
    print("DIAGNOSIS")
    print("="*60)
    
    public_works = results[0][1]  # products
    private_works = any(r[1] for r in results[1:])  # wallet, positions, orders
    
    if public_works and not private_works:
        print("""
🔍 Your API key is VALID but lacks READ permissions!

This is why:
  ✅ Public endpoints work (products)
  ❌ Private endpoints fail (balances, positions, orders)

HOW TO FIX:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OPTION 1: Enable Permissions on Existing Key
────────────────────────────────────────────
1. Go to: https://www.delta.exchange/app/account-settings/api

2. Find your API key in the list

3. Click "Edit" or settings icon

4. Enable these permissions:
   ☑️  Read    (View balances, positions, orders)
   ☑️  Trade   (Place/cancel orders) - optional
   
5. Check IP whitelist:
   • If restricted, add your IP
   • Or disable IP whitelist for testing

6. Save changes

7. Wait 30 seconds, then test again:
   python3 quick_test.py


OPTION 2: Create a New API Key (RECOMMENDED)
─────────────────────────────────────────────
1. Go to: https://www.delta.exchange/app/account-settings/api

2. Click "Create New API Key"

3. Set permissions:
   ☑️  Read    (Required for viewing data)
   ☑️  Trade   (Optional - for placing orders)

4. IP Whitelist: Leave EMPTY or add your current IP

5. Click "Create"

6. COPY both:
   • API Key
   • API Secret

7. Update your .env file:
   DELTA_API_KEY=<paste your new key>
   DELTA_API_SECRET=<paste your new secret>

8. Test again:
   python3 quick_test.py


TROUBLESHOOTING:
────────────────
• Make sure you're on the CORRECT exchange:
  India: https://www.delta.exchange
  Global: https://delta.exchange (different!)
  
• Our code uses: api.india.delta.exchange
  If you're on global exchange, you need to change base URL

• Check if you have testnet key vs mainnet
  
• After ANY changes, wait 30 seconds before testing
        """)
    elif public_works and private_works:
        print("""
🎉 SUCCESS! Your API key has all required permissions!

All endpoints are working correctly:
  ✅ Public endpoints (products)
  ✅ Private endpoints (balances, positions, orders)

You can now use the client for:
  • Viewing positions and balances
  • Querying orders
  • (With Trade permission) Placing orders

Try the examples:
  python3 examples/get_positions.py
  python3 examples/place_order.py
        """)
    else:
        print("""
❌ API key validation failed completely.

Possible issues:
  • Invalid API key or secret
  • Wrong exchange (India vs Global)
  • Testnet key on mainnet (or vice versa)
  • API key has been revoked

Please double-check your credentials in .env file.
        """)

if __name__ == "__main__":
    check_permissions()

