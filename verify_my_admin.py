#!/usr/bin/env python3
"""
Simple script to verify the specific admin account: alusinekuyateh6@gmail.com
"""

import requests
import json

# Configuration
API_BASE_URL = "https://mamacare-backend.onrender.com"
EMAIL = "alusinekuyateh6@gmail.com"

def verify_admin():
    """Verify the specific admin account"""
    print(f"🔍 Verifying admin account: {EMAIL}")
    print("=" * 50)
    
    try:
        # Call the verify admin endpoint
        url = f"{API_BASE_URL}/api/admin/verify-admin/{EMAIL}"
        response = requests.post(url)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print(f"📧 Admin verified: {result['message']}")
            print(f"🆔 Admin ID: {result['admin_id']}")
            print(f"📊 Table: {result['table']}")
        else:
            result = response.json()
            print("❌ FAILED!")
            print(f"Error: {result.get('error', 'Unknown error')}")
            print(f"Status Code: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print("❌ NETWORK ERROR!")
        print(f"Error: {e}")
    except Exception as e:
        print("❌ UNEXPECTED ERROR!")
        print(f"Error: {e}")

def test_login():
    """Test if the admin can login after verification"""
    print(f"\n🔐 Testing login for: {EMAIL}")
    print("=" * 30)
    
    try:
        # Test login
        url = f"{API_BASE_URL}/api/admin/login"
        data = {
            "email": EMAIL,
            "password": "Admin123"
        }
        
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ LOGIN SUCCESSFUL!")
            print(f"👤 Welcome: {result['user']['name']}")
            print(f"📧 Email: {result['user']['email']}")
            print(f"🔑 Token: {result['token'][:20]}...")
        else:
            result = response.json()
            print("❌ LOGIN FAILED!")
            print(f"Error: {result.get('error', 'Unknown error')}")
            
    except requests.exceptions.RequestException as e:
        print("❌ NETWORK ERROR!")
        print(f"Error: {e}")
    except Exception as e:
        print("❌ UNEXPECTED ERROR!")
        print(f"Error: {e}")

def main():
    """Main function"""
    print("🚀 Admin Verification Tool")
    print("=" * 50)
    print(f"📧 Target Email: {EMAIL}")
    print(f"🌐 API URL: {API_BASE_URL}")
    print()
    
    # Step 1: Verify the admin
    verify_admin()
    
    # Step 2: Test login
    test_login()
    
    print("\n" + "=" * 50)
    print("🎉 Verification process completed!")
    print("📋 Next steps:")
    print("1. Try logging into the admin dashboard")
    print("2. If login fails, check the error message above")
    print("3. Contact support if issues persist")

if __name__ == "__main__":
    main() 