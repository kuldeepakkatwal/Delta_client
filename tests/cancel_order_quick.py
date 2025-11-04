#!/usr/bin/env python3
"""
Quick script to cancel a specific order by ID
"""

import os
from dotenv import load_dotenv
from delta_exchange import DeltaRestClient

# Load environment variables
load_dotenv()

# Initialize client
client = DeltaRestClient(
    api_key=os.getenv("DELTA_API_KEY"),
    api_secret=os.getenv("DELTA_API_SECRET")
)

# Order ID from the test that failed
order_id = 1020335971
product_id = 104724  # C-BTC-94000-211125

try:
    print(f"\n🔄 Attempting to cancel order {order_id}...")
    client.cancel_order(order_id=order_id, product_id=product_id)
    print(f"✅ Order {order_id} cancelled successfully!\n")
except Exception as e:
    print(f"ℹ️  Could not cancel order: {e}")
    print(f"   (Order may already be cancelled or filled)\n")

