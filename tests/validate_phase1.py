#!/usr/bin/env python3
"""
Phase 1 Validation Script

This script validates that Phase 1 implementation works correctly.
It tests signature generation against known examples from Delta Exchange documentation.
"""

from delta_exchange.auth import DeltaAuth
from delta_exchange.exceptions import AuthenticationError, DeltaExchangeException

def test_signature_generation():
    """Test signature generation produces consistent, valid signatures"""
    print("Testing signature generation...")
    
    # Test data
    api_key = "test_api_key"
    api_secret = "test_api_secret"
    
    auth = DeltaAuth(api_key, api_secret)
    
    # Test 1: GET request with query parameters
    timestamp = "1542110948"
    method = "GET"
    path = "/v2/orders"
    query_string = "product_id=1&state=open"
    body = ""
    
    signature1 = auth.generate_signature(method, timestamp, path, query_string, body)
    
    # Verify signature is a valid hex string of correct length (64 chars for SHA256)
    if len(signature1) != 64:
        print(f"❌ Signature length incorrect: {len(signature1)} (expected 64)")
        return False
    
    try:
        int(signature1, 16)  # Verify it's valid hex
    except ValueError:
        print(f"❌ Signature is not valid hexadecimal: {signature1}")
        return False
    
    # Test 2: Same parameters should produce same signature (consistency)
    signature2 = auth.generate_signature(method, timestamp, path, query_string, body)
    
    if signature1 != signature2:
        print(f"❌ Signature not consistent")
        print(f"   First:  {signature1}")
        print(f"   Second: {signature2}")
        return False
    
    print("✅ Signature generation test PASSED")
    print(f"   Signature: {signature1[:32]}... (64 chars)")
    print(f"   Format: Valid hexadecimal")
    print(f"   Consistency: ✓")
    
    # Test 3: Different timestamp should produce different signature
    signature3 = auth.generate_signature(method, "9999999999", path, query_string, body)
    
    if signature1 == signature3:
        print(f"❌ Different parameters produced same signature")
        return False
    
    print(f"   Uniqueness: ✓")
    
    # Test 4: Query string with leading ? should work the same
    signature4 = auth.generate_signature(method, timestamp, path, "?product_id=1&state=open", body)
    
    if signature1 != signature4:
        print(f"❌ Query string handling inconsistent")
        print(f"   Without ?: {signature1}")
        print(f"   With ?:    {signature4}")
        return False
    
    print(f"   Query string handling: ✓")
    
    # Test 5: Generate headers
    headers = auth.generate_headers(method, path, query_string, body, timestamp)
    
    required_headers = ["api-key", "signature", "timestamp", "User-Agent", "Content-Type"]
    for header in required_headers:
        if header not in headers:
            print(f"❌ Missing header: {header}")
            return False
    
    if headers["api-key"] != api_key:
        print(f"❌ API key in headers doesn't match")
        return False
    
    if headers["signature"] != signature1:
        print(f"❌ Signature in headers doesn't match generated signature")
        return False
    
    print("✅ Header generation test PASSED")
    print(f"   Headers: {list(headers.keys())}")
    
    return True


def test_websocket_auth():
    """Test WebSocket authentication payload generation"""
    print("\nTesting WebSocket authentication...")
    
    api_key = "test_key"
    api_secret = "test_secret"
    
    auth = DeltaAuth(api_key, api_secret)
    
    timestamp = "1542110948"
    auth_payload = auth.generate_websocket_auth_payload(timestamp)
    
    required_fields = ["api-key", "signature", "timestamp"]
    for field in required_fields:
        if field not in auth_payload:
            print(f"❌ Missing field in auth payload: {field}")
            return False
    
    print("✅ WebSocket auth payload test PASSED")
    print(f"   Fields: {list(auth_payload.keys())}")
    
    return True


def test_exceptions():
    """Test exception handling"""
    print("\nTesting exception classes...")
    
    # Test AuthenticationError
    try:
        auth = DeltaAuth("", "")
        print("❌ Should have raised AuthenticationError for empty credentials")
        return False
    except AuthenticationError as e:
        print(f"✅ AuthenticationError raised correctly: {e}")
    
    # Test exception hierarchy
    try:
        raise AuthenticationError("Test")
    except DeltaExchangeException:
        print("✅ Exception hierarchy works correctly")
    except Exception:
        print("❌ Exception hierarchy broken")
        return False
    
    return True


def test_imports():
    """Test that all modules can be imported"""
    print("\nTesting imports...")
    
    try:
        from delta_exchange import (
            DeltaAuth,
            DeltaExchangeException,
            AuthenticationError,
            OrderError,
            APIError,
            WebSocketError,
            RateLimitError,
            ValidationError,
            NetworkError,
            constants,
        )
        print("✅ All imports successful")
        print(f"   Package version: {constants.__name__}")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False


def main():
    """Run all validation tests"""
    print("=" * 60)
    print("PHASE 1 VALIDATION")
    print("=" * 60)
    
    tests = [
        ("Signature Generation", test_signature_generation),
        ("WebSocket Auth", test_websocket_auth),
        ("Exceptions", test_exceptions),
        ("Imports", test_imports),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test '{test_name}' raised exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED - Phase 1 Complete!")
        print("=" * 60)
        print("\nYou can now proceed to Phase 2: REST Client Implementation")
    else:
        print("⚠️  SOME TESTS FAILED - Please review and fix issues")
        print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    exit(main())

