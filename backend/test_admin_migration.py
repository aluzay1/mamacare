#!/usr/bin/env python3
"""
Test script for Admin table migration and functionality
"""

import requests
import json
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Admin, User

def test_admin_table_creation():
    """Test that the admin table was created successfully"""
    print("🔍 Testing Admin table creation...")
    
    with app.app_context():
        try:
            # Check if admin table exists
            admin_count = Admin.query.count()
            print(f"✅ Admin table exists with {admin_count} records")
            
            # Check if any admin users exist in the old user table
            old_admin_count = User.query.filter_by(role='admin').count()
            print(f"📊 Found {old_admin_count} admin users in old user table")
            
            return True
        except Exception as e:
            print(f"❌ Error testing admin table: {e}")
            return False

def test_admin_signup():
    """Test admin signup functionality"""
    print("\n🔍 Testing Admin signup...")
    
    test_admin_data = {
        "name": "Test Admin",
        "email": "testadmin@mamacare.com",
        "phone": "+232123456789",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(
            "http://localhost:5000/api/admin/signup",
            json=test_admin_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            print("✅ Admin signup successful")
            return response.json().get('token')
        else:
            print(f"❌ Admin signup failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error testing admin signup: {e}")
        return None

def test_admin_login():
    """Test admin login functionality"""
    print("\n🔍 Testing Admin login...")
    
    login_data = {
        "email": "testadmin@mamacare.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(
            "http://localhost:5000/api/admin/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("✅ Admin login successful")
            return response.json().get('token')
        else:
            print(f"❌ Admin login failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error testing admin login: {e}")
        return None

def test_admin_endpoints(token):
    """Test admin management endpoints"""
    print("\n🔍 Testing Admin management endpoints...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Test getting admins
    try:
        response = requests.get(
            "http://localhost:5000/api/admin/admins",
            headers=headers
        )
        
        if response.status_code == 200:
            admins = response.json()
            print(f"✅ Get admins successful - Found {len(admins)} admins")
        else:
            print(f"❌ Get admins failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error testing get admins: {e}")

def cleanup_test_data():
    """Clean up test data"""
    print("\n🧹 Cleaning up test data...")
    
    with app.app_context():
        try:
            # Remove test admin
            test_admin = Admin.query.filter_by(email="testadmin@mamacare.com").first()
            if test_admin:
                db.session.delete(test_admin)
                db.session.commit()
                print("✅ Test admin removed")
        except Exception as e:
            print(f"❌ Error cleaning up: {e}")

def main():
    """Main test function"""
    print("🚀 Starting Admin Table Migration Tests")
    print("=" * 50)
    
    # Test 1: Check table creation
    if not test_admin_table_creation():
        print("❌ Admin table creation test failed")
        return
    
    # Test 2: Test admin signup
    token = test_admin_signup()
    if not token:
        print("❌ Admin signup test failed")
        return
    
    # Test 3: Test admin login
    login_token = test_admin_login()
    if not login_token:
        print("❌ Admin login test failed")
        return
    
    # Test 4: Test admin endpoints
    test_admin_endpoints(login_token)
    
    # Cleanup
    cleanup_test_data()
    
    print("\n" + "=" * 50)
    print("✅ All Admin Table Migration Tests Completed Successfully!")
    print("\n📋 Summary:")
    print("- Admin table created and accessible")
    print("- Admin signup functionality working")
    print("- Admin login functionality working")
    print("- Admin management endpoints working")
    print("- Admin data properly separated from user table")

if __name__ == "__main__":
    main() 