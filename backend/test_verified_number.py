#!/usr/bin/env python3
"""
Test SMS with Verified Number +23233237891
"""

import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_verified_number():
    """Test SMS with the verified number"""
    print("=" * 60)
    print("TESTING SMS WITH VERIFIED NUMBER")
    print("=" * 60)
    
    verified_number = "+23233237891"
    print(f"📱 Testing with verified number: {verified_number}")
    
    # Test data
    test_data = {
        "patient_name": "Verified Number Test Patient",
        "feedback_notes": "This is a test to verify SMS functionality works with the verified number +23233237891. Patient is responding well to treatment.",
        "doctor_name": "Dr. Test Doctor",
        "doctor_phone": "+23212345678",
        "doctor_affiliation": "Test Hospital",
        "referral_source": "PresTrack"
    }
    
    print("\n📡 Sending referral feedback...")
    print(f"Test data: {json.dumps(test_data, indent=2)}")
    
    try:
        response = requests.post(
            "http://localhost:5000/api/referral-feedback",
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 201:
            result = response.json()
            print("\n✅ Referral feedback submitted successfully!")
            print(f"   Feedback ID: {result.get('feedback_id')}")
            print(f"   SMS Sent: {result.get('sms_sent')}")
            print(f"   Timestamp: {result.get('timestamp')}")
            
            if result.get('sms_sent'):
                print("🎉 SMS was sent successfully!")
                print(f"   Check the verified number ({verified_number}) for the SMS")
            else:
                print("⚠️  SMS was NOT sent!")
                print("   This might indicate another issue")
            
            return result
        else:
            print(f"❌ API request failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return None

def test_direct_sms():
    """Test direct SMS sending to verified number"""
    print("\n" + "=" * 60)
    print("TESTING DIRECT SMS TO VERIFIED NUMBER")
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
        test_message = """MAMACARE SMS TEST - VERIFIED NUMBER

This is a test SMS to the verified number +23233237891.

✅ Twilio integration is working!
✅ SMS functionality is operational!
✅ Verified number test successful!

Best regards,
MamaCare Team"""
        
        verified_number = "+23233237891"
        
        print(f"📱 Sending direct SMS:")
        print(f"   From: {from_number}")
        print(f"   To: {verified_number}")
        print(f"   Message: {test_message}")
        
        confirm = input(f"\nSend SMS to verified number {verified_number}? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            print("\n📤 Sending SMS...")
            
            message = client.messages.create(
                body=test_message,
                from_=from_number,
                to=verified_number
            )
            
            print("✅ SMS sent successfully!")
            print(f"   Message SID: {message.sid}")
            print(f"   Status: {message.status}")
            print(f"   To: {message.to}")
            print(f"   From: {message.from_}")
            
            return True
        else:
            print("❌ SMS test cancelled.")
            return False
            
    except Exception as e:
        print(f"❌ SMS sending failed: {str(e)}")
        return False

def main():
    """Main test function"""
    print("VERIFIED NUMBER SMS TESTING")
    print("=" * 60)
    
    # Test 1: Referral feedback with verified number
    result = test_verified_number()
    
    # Test 2: Direct SMS test
    print("\n" + "=" * 60)
    print("OPTIONAL: DIRECT SMS TEST")
    print("=" * 60)
    print("This will send a direct SMS to the verified number.")
    
    direct_test = input("Run direct SMS test? (yes/no): ").strip().lower()
    if direct_test == 'yes':
        test_direct_sms()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    if result:
        print("✅ Referral feedback API is working")
        if result.get('sms_sent'):
            print("✅ SMS sending is working with verified number")
            print("🎉 Your SMS system is fully functional!")
        else:
            print("⚠️  SMS sending failed - check the logs")
    else:
        print("❌ Referral feedback API failed")
    
    print("\n" + "=" * 60)
    print("NEXT STEPS")
    print("=" * 60)
    print("If SMS is working with +23233237891:")
    print("✅ Your SMS system is ready for production")
    print("✅ You can use this number for PresTrack notifications")
    print("✅ Consider adding more verified numbers if needed")
    print("=" * 60)

if __name__ == "__main__":
    main() 