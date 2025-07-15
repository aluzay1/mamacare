#!/usr/bin/env python3
"""
Test SMS in Docker Environment with Verified Number
"""

import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_docker_sms():
    """Test SMS functionality in Docker environment"""
    print("=" * 60)
    print("TESTING SMS IN DOCKER ENVIRONMENT")
    print("=" * 60)
    
    # Check if Flask app is running
    try:
        health_response = requests.get("http://localhost:5000/health", timeout=5)
        if health_response.status_code == 200:
            print("✅ Flask app is running in Docker")
        else:
            print("⚠️  Flask app responded but health check failed")
    except Exception as e:
        print(f"❌ Cannot connect to Flask app: {str(e)}")
        print("Make sure Docker containers are running")
        return
    
    # Test referral feedback with verified number
    verified_number = "+23233237891"
    print(f"\n📱 Testing with verified number: {verified_number}")
    
    # Test data
    test_data = {
        "patient_name": "Docker SMS Test Patient",
        "feedback_notes": "This is a test from Docker environment to verify SMS functionality with the verified number +23233237891.",
        "doctor_name": "Dr. Docker Test",
        "doctor_phone": "+23212345678",
        "doctor_affiliation": "Docker Test Hospital",
        "referral_source": "PresTrack"
    }
    
    print("\n📡 Sending referral feedback to Docker container...")
    print(f"Test data: {json.dumps(test_data, indent=2)}")
    
    try:
        response = requests.post(
            "http://localhost:5000/api/referral-feedback",
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print("\n✅ Referral feedback submitted successfully!")
            print(f"   Feedback ID: {result.get('feedback_id')}")
            print(f"   SMS Sent: {result.get('sms_sent')}")
            print(f"   Timestamp: {result.get('timestamp')}")
            
            if result.get('sms_sent'):
                print("🎉 SMS was sent successfully!")
                print(f"   Check the verified number ({verified_number}) for the SMS")
                print("✅ Your SMS system is working perfectly in Docker!")
            else:
                print("⚠️  SMS was NOT sent!")
                print("   This indicates the verified number might not be working")
                print("   or there's still an issue with the SMS function")
            
            return result
        else:
            print(f"❌ API request failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return None

def check_recent_records():
    """Check recent referral feedback records"""
    print("\n" + "=" * 60)
    print("CHECKING RECENT REFERRAL FEEDBACK RECORDS")
    print("=" * 60)
    
    try:
        response = requests.get(
            "http://localhost:5000/api/referral-feedback?limit=3",
            timeout=10
        )
        
        if response.status_code == 200:
            records = response.json()
            print(f"Found {len(records)} recent records:")
            
            for i, record in enumerate(records, 1):
                print(f"\n{i}. Record ID: {record['id']}")
                print(f"   Patient: {record['patient_name']}")
                print(f"   Doctor: {record['doctor_name']}")
                print(f"   SMS Sent: {record['sms_sent']}")
                print(f"   SMS Sent At: {record['sms_sent_at']}")
                print(f"   Created: {record['created_at']}")
        else:
            print(f"❌ Failed to get records: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error checking records: {str(e)}")

def main():
    """Main test function"""
    print("DOCKER SMS TESTING SUITE")
    print("=" * 60)
    
    # Test 1: Docker SMS functionality
    result = test_docker_sms()
    
    # Test 2: Check recent records
    check_recent_records()
    
    # Summary
    print("\n" + "=" * 60)
    print("DOCKER TEST SUMMARY")
    print("=" * 60)
    
    if result:
        print("✅ Docker container is working")
        print("✅ API endpoints are functional")
        if result.get('sms_sent'):
            print("✅ SMS sending is working in Docker")
            print("🎉 Your Docker SMS system is fully operational!")
        else:
            print("⚠️  SMS sending failed in Docker")
            print("   The issue might be with the verified number")
    else:
        print("❌ Docker container or API failed")
    
    print("\n" + "=" * 60)
    print("TROUBLESHOOTING")
    print("=" * 60)
    print("If SMS is not working in Docker:")
    print("1. Check if the verified number +23233237891 is correct")
    print("2. Verify Twilio credentials in Docker environment")
    print("3. Check Docker logs for any errors")
    print("4. Restart Docker containers if needed")
    print("=" * 60)

if __name__ == "__main__":
    main() 