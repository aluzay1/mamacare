#!/usr/bin/env python3
"""
Referral Feedback SMS Testing Script
Tests the complete referral feedback flow with SMS sending
"""

import os
import sys
import json
import requests
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_referral_feedback_with_sms():
    """Test referral feedback submission with SMS sending"""
    print("=" * 60)
    print("TESTING REFERRAL FEEDBACK WITH SMS")
    print("=" * 60)
    
    # Test data
    test_data = {
        "patient_name": "Test Patient - SMS Test",
        "feedback_notes": "This is a test referral feedback to verify SMS functionality. Patient condition is stable and responding well to treatment.",
        "doctor_name": "Dr. Test Doctor",
        "doctor_phone": "+23212345678",
        "doctor_affiliation": "Test Hospital",
        "referral_source": "PresTrack"
    }
    
    print("Test Data:")
    print(json.dumps(test_data, indent=2))
    
    # Backend URL
    backend_url = "http://localhost:5000/api/referral-feedback"
    
    try:
        print(f"\n📡 Sending request to: {backend_url}")
        
        response = requests.post(
            backend_url,
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"📊 Response Status: {response.status_code}")
        print(f"📋 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 201:
            result = response.json()
            print("\n✅ Referral feedback submitted successfully!")
            print(f"   Feedback ID: {result.get('feedback_id')}")
            print(f"   SMS Sent: {result.get('sms_sent')}")
            print(f"   Timestamp: {result.get('timestamp')}")
            
            # Check SMS status
            if result.get('sms_sent'):
                print("🎉 SMS was sent successfully!")
            else:
                print("⚠️  SMS was NOT sent!")
                print("   This could be due to:")
                print("   - Invalid phone number (+23233237891)")
                print("   - Twilio account issues")
                print("   - Network connectivity problems")
            
            return result
            
        else:
            print(f"❌ API request failed!")
            print(f"Response: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend API!")
        print("Make sure the Flask app is running on localhost:5000")
        return None
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        return None

def test_sms_directly():
    """Test SMS sending directly using Twilio"""
    print("\n" + "=" * 60)
    print("TESTING SMS DIRECTLY WITH TWILIO")
    print("=" * 60)
    
    try:
        from twilio.rest import Client
        
        # Get Twilio credentials
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        from_number = os.getenv('TWILIO_PHONE_NUMBER')
        
        if not all([account_sid, auth_token, from_number]):
            print("❌ Twilio credentials not configured!")
            return False
        
        client = Client(account_sid, auth_token)
        
        # Test message
        test_message = """REFERRAL FEEDBACK - MamaCare

Patient ID: TEST123
Patient: Test Patient
Patient Contact: +23212345678
Doctor: Dr. Test Doctor
Doctor Phone: +23212345678
Hospital/Affiliation: Test Hospital
Feedback: This is a direct SMS test from MamaCare system.

Submitted: 11th July, 2025 at 10:30 PM"""
        
        # Get test number from user
        print("Enter a phone number to test SMS (e.g., +23212345678):")
        to_number = input("Phone number: ").strip()
        
        if not to_number:
            print("❌ No phone number provided. Test cancelled.")
            return False
        
        print(f"\n📱 Sending SMS:")
        print(f"   From: {from_number}")
        print(f"   To: {to_number}")
        print(f"   Message: {test_message}")
        
        confirm = input(f"\nSend SMS to {to_number}? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            print("\n📤 Sending SMS...")
            
            message = client.messages.create(
                body=test_message,
                from_=from_number,
                to=to_number
            )
            
            print("✅ SMS sent successfully!")
            print(f"   Message SID: {message.sid}")
            print(f"   Status: {message.status}")
            print(f"   To: {message.to}")
            print(f"   From: {message.from_}")
            
            return True
        else:
            print("❌ SMS sending cancelled.")
            return False
            
    except ImportError:
        print("❌ Twilio library not installed!")
        print("Install with: pip install twilio")
        return False
    except Exception as e:
        print(f"❌ SMS sending failed: {str(e)}")
        return False

def check_referral_feedback_records():
    """Check recent referral feedback records"""
    print("\n" + "=" * 60)
    print("CHECKING RECENT REFERRAL FEEDBACK RECORDS")
    print("=" * 60)
    
    try:
        response = requests.get(
            "http://localhost:5000/api/referral-feedback?limit=5",
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
    """Run all referral feedback tests"""
    print("REFERRAL FEEDBACK SMS TESTING SUITE")
    print("=" * 60)
    
    # Test 1: Referral feedback submission
    result = test_referral_feedback_with_sms()
    
    # Test 2: Check recent records
    check_referral_feedback_records()
    
    # Test 3: Direct SMS test
    print("\n" + "=" * 60)
    print("OPTIONAL: DIRECT SMS TEST")
    print("=" * 60)
    print("This will send a real SMS to test Twilio functionality.")
    
    direct_test = input("Run direct SMS test? (yes/no): ").strip().lower()
    if direct_test == 'yes':
        test_sms_directly()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    if result:
        print("✅ Referral feedback API is working")
        if result.get('sms_sent'):
            print("✅ SMS sending is working")
        else:
            print("⚠️  SMS sending failed - check the hardcoded number +23233237891")
    else:
        print("❌ Referral feedback API failed")
    
    print("\n" + "=" * 60)
    print("TROUBLESHOOTING")
    print("=" * 60)
    print("If SMS is not sending:")
    print("1. Check if +23233237891 is a valid phone number")
    print("2. Verify Twilio account has sufficient credits")
    print("3. Check Twilio console for error messages")
    print("4. Try the direct SMS test above")
    print("=" * 60)

if __name__ == "__main__":
    main() 