#!/usr/bin/env python3
"""
Simple test script to verify CORS is working
"""

import requests
import json

def test_cors():
    """Test CORS configuration"""
    
    # Test data
    test_data = {
        "email": "test@example.com",
        "name": "Test User",
        "given_name": "Test",
        "family_name": "User",
        "gender": "female",
        "date_of_birth": "1990-01-01",
        "phone": "+23212345678",
        "address_line": "123 Test St",
        "city": "Freetown",
        "state": "Western Area",
        "country": "Sierra Leone"
    }
    
    print("Testing CORS configuration...")
    print("=" * 50)
    
    # Test 1: OPTIONS request (preflight)
    print("1. Testing OPTIONS request (preflight)...")
    try:
        response = requests.options(
            'http://localhost:5000/api/patient/register',
            headers={
                'Origin': 'http://localhost',
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'Content-Type'
            }
        )
        print(f"   Status: {response.status_code}")
        print(f"   CORS Headers: {dict(response.headers)}")
        print(f"   Success: {'Access-Control-Allow-Origin' in response.headers}")
    except Exception as e:
        print(f"   Error: {str(e)}")
    
    print()
    
    # Test 2: POST request
    print("2. Testing POST request...")
    try:
        response = requests.post(
            'http://localhost:5000/api/patient/register',
            headers={
                'Content-Type': 'application/json',
                'Origin': 'http://localhost'
            },
            json=test_data
        )
        print(f"   Status: {response.status_code}")
        print(f"   CORS Headers: {dict(response.headers)}")
        print(f"   Response: {response.text[:200]}...")
    except Exception as e:
        print(f"   Error: {str(e)}")
    
    print()
    print("CORS test completed!")

if __name__ == "__main__":
    test_cors() 