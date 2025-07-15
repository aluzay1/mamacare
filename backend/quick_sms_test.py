#!/usr/bin/env python3
"""
Quick SMS Test - Test referral feedback with your phone number
"""

import os
import requests
import json

def test_sms_with_your_number():
    """Test SMS with your phone number"""
    print("=" * 60)
    print("QUICK SMS TEST")
    print("=" * 60)
    
    # Get your phone number
    print("Enter your phone number to test SMS:")
    print("Format: +23212345678")
    your_number = input("Your phone number: ").strip()
    
    if not your_number:
        print("❌ No phone number provided.")
        return
    
    # Validate format
    if not your_number.startswith('+232') or len(your_number) != 12:
        print("❌ Invalid format. Must be +232XXXXXXXX")
        return
    
    print(f"\n📱 Testing SMS to: {your_number}")
    
    # Test data
    test_data = {
        "patient_name": "Quick SMS Test Patient",
        "feedback_notes": "This is a quick test to verify SMS functionality is working correctly.",
        "doctor_name": "Dr. Test Doctor",
        "doctor_phone": "+23212345678",
        "doctor_affiliation": "Test Hospital"
    }
    
    # Temporarily set environment variable
    original_number = os.getenv('PRESTRACK_PHONE_NUMBER')
    os.environ['PRESTRACK_PHONE_NUMBER'] = your_number
    
    try:
        print("📡 Sending referral feedback...")
        
        response = requests.post(
            "http://localhost:5000/api/referral-feedback",
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 201:
            result = response.json()
            print("✅ Referral feedback submitted!")
            print(f"   Feedback ID: {result.get('feedback_id')}")
            print(f"   SMS Sent: {result.get('sms_sent')}")
            
            if result.get('sms_sent'):
                print("🎉 SMS was sent successfully!")
                print(f"   Check your phone ({your_number}) for the message")
            else:
                print("⚠️  SMS was NOT sent!")
                print("   This might be due to Twilio restrictions or account issues")
        else:
            print(f"❌ API failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
    finally:
        # Restore original environment variable
        if original_number:
            os.environ['PRESTRACK_PHONE_NUMBER'] = original_number
        else:
            os.environ.pop('PRESTRACK_PHONE_NUMBER', None)

if __name__ == "__main__":
    test_sms_with_your_number() 