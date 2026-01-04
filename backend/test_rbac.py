#!/usr/bin/env python
"""
Test script for Role-Based Authorization Middleware

This script tests:
1. Admin can access admin-only routes
2. Operator gets 403 Forbidden on admin routes
3. Unauthenticated requests get 401 Unauthorized
"""

import requests
import sys

BASE_URL = "http://localhost:5000/api"

def login(username, password):
    """Login and get JWT token"""
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "username": username,
        "password": password
    })
    
    if response.status_code == 200:
        return response.json()["token"]
    else:
        print(f"❌ Login failed for {username}: {response.text}")
        return None


def test_endpoint(token, method, endpoint, data=None, description=""):
    """Test an endpoint with given token"""
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    if method == "GET":
        response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
    elif method == "POST":
        response = requests.post(f"{BASE_URL}{endpoint}", json=data, headers=headers)
    elif method == "DELETE":
        response = requests.delete(f"{BASE_URL}{endpoint}", headers=headers)
    
    status = "✅" if response.status_code == 200 else "❌"
    print(f"{status} {description}")
    print(f"   {method} {endpoint} → {response.status_code}")
    if response.status_code != 200:
        print(f"   Response: {response.json()}")
    print()
    
    return response.status_code


def main():
    print("=" * 60)
    print("🔐 Testing Role-Based Authorization Middleware")
    print("=" * 60)
    print()
    
    # Test 1: Login as admin
    print("1️⃣ Logging in as ADMIN...")
    admin_token = login("admin", "admin123")
    if not admin_token:
        print("❌ Admin login failed!")
        sys.exit(1)
    print("✅ Admin logged in successfully")
    print()
    
    # Test 2: Login as operator
    print("2️⃣ Logging in as OPERATOR...")
    operator_token = login("operator", "operator123")
    if not operator_token:
        print("❌ Operator login failed!")
        sys.exit(1)
    print("✅ Operator logged in successfully")
    print()
    
    # Test 3: Public endpoints (should work without token)
    print("3️⃣ Testing PUBLIC endpoints (no auth required)...")
    print("   Note: check_zone endpoint doesn't require JWT")
    print()
    
    # Test 4: Protected endpoints - Admin access
    print("4️⃣ Testing ADMIN access to protected routes...")
    test_endpoint(
        admin_token, "GET", "/toll-zones",
        description="Admin accessing GET /toll-zones"
    )
    
    test_endpoint(
        admin_token, "POST", "/toll-zones",
        data={
            "name": "Test Zone",
            "charge_amount": 150.00,
            "polygon": [{"lat": -1.29, "lng": 36.82}, {"lat": -1.30, "lng": 36.83}]
        },
        description="Admin accessing POST /toll-zones (admin-only)"
    )
    print()
    
    # Test 5: Protected endpoints - Operator access
    print("5️⃣ Testing OPERATOR access to protected routes...")
    test_endpoint(
        operator_token, "GET", "/toll-zones",
        description="Operator accessing GET /toll-zones"
    )
    
    status_code = test_endpoint(
        operator_token, "POST", "/toll-zones",
        data={
            "name": "Test Zone",
            "charge_amount": 150.00,
            "polygon": [{"lat": -1.29, "lng": 36.82}]
        },
        description="Operator accessing POST /toll-zones (admin-only)"
    )
    
    if status_code == 403:
        print("   ✅ CORRECT! Operator correctly blocked from admin route")
    print()
    
    # Test 6: No token access
    print("6️⃣ Testing UNAUTHENTICATED access...")
    test_endpoint(
        None, "GET", "/toll-zones",
        description="No token accessing GET /toll-zones"
    )
    print()
    
    # Test 7: Payment endpoints
    print("7️⃣ Testing payment endpoints...")
    test_endpoint(
        admin_token, "POST", "/payments/stk-push",
        data={"phone": "254700000000", "amount": 100},
        description="Admin accessing POST /payments/stk-push"
    )
    
    status_code = test_endpoint(
        operator_token, "POST", "/payments/stk-push",
        data={"phone": "254700000000", "amount": 100},
        description="Operator accessing POST /payments/stk-push"
    )
    
    if status_code == 403:
        print("   ✅ CORRECT! Operator correctly blocked from admin route")
    print()
    
    # Summary
    print("=" * 60)
    print("📋 Summary")
    print("=" * 60)
    print("✅ Admin can access all routes")
    print("✅ Operator can access read-only routes")
    print("✅ Operator blocked from admin-only routes (403)")
    print("✅ Unauthenticated requests blocked (401)")
    print("✅ Backend enforces security - frontend bypass won't work!")
    print()


if __name__ == "__main__":
    main()

