#!/usr/bin/env python3
"""
SMS Testing Script for MamaCare Healthcare Management System
Tests Twilio SMS functionality for referral feedback notifications
"""

import os
import sys
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the current directory to Python path to import from app.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_twilio_credentials():
    """Test if Twilio credentials are properly configured"""
    print("=" * 60)
    print("TESTING TWILIO CREDENTIALS")
    print("=" * 60)
    
    # Check environment variables
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    from_number = os.getenv('TWILIO_PHONE_NUMBER')
    
    print(f"Account SID: {'✅ Set' if account_sid else '❌ Not set'}")
    print(f"Auth Token: {'✅ Set' if auth_token else '❌ Not set'}")
    print(f"From Number: {'✅ Set' if from_number else '❌ Not set'}")
    
    if not all([account_sid, auth_token, from_number]):
        print("\n❌ Twilio credentials are not properly configured!")
        print("Please set the following environment variables:")
        print("- TWILIO_ACCOUNT_SID")
        print("- TWILIO_AUTH_TOKEN") 
        print("- TWILIO_PHONE_NUMBER")
        return False
    
    print("\n✅ All Twilio credentials are configured!")
    return True

def test_twilio_connection():
    """Test Twilio API connection"""
    print("\n" + "=" * 60)
    print("TESTING TWILIO API CONNECTION")
    print("=" * 60)
    
    try:
        from twilio.rest import Client
        
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        
        client = Client(account_sid, auth_token)
        
        # Try to get account info to test connection
        account = client.api.accounts(account_sid).fetch()
        print(f"✅ Twilio connection successful!")
        print(f"Account Name: {account.friendly_name}")
        print(f"Account Status: {account.status}")
        print(f"Account Type: {account.type}")
        
        return True
        
    except ImportError:
        print("❌ Twilio library not installed!")
        print("Install with: pip install twilio")
        return False
    except Exception as e:
        print(f"❌ Twilio connection failed: {str(e)}")
        return False

def test_sms_format():
    """Test the SMS message format"""
    print("\n" + "=" * 60)
    print("TESTING SMS MESSAGE FORMAT")
    print("=" * 60)
    
    def format_datetime_with_ordinal(datetime_obj):
        """Format datetime as '30th June, 2025 at 2:30 PM'"""
        if not datetime_obj:
            return "Unknown"
        
        day = datetime_obj.day
        month = datetime_obj.strftime('%B')  # Full month name
        year = datetime_obj.year
        time = datetime_obj.strftime('%I:%M %p')  # 12-hour format with AM/PM
        
        # Add ordinal suffix to day
        if 10 <= day % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
        
        return f"{day}{suffix} {month}, {year} at {time}"
    
    # Sample data
    patient_id = "12345"
    patient_name = "Sylvia Bobson Hardings"
    patient_contact = "+23212345678"
    doctor_name = "Dr. Ahmed"
    doctor_phone = "+23278656832"
    doctor_affiliation = "Life Care"
    feedback_notes = "Patient is responding well to treatment. Follow-up scheduled for next week."
    current_datetime = format_datetime_with_ordinal(datetime.now())
    
    # Create SMS message (same format as in the backend)
    sms_message = f"""REFERRAL FEEDBACK - MamaCare
        
Patient ID: {patient_id}
Patient: {patient_name}
Patient Contact: {patient_contact}
Doctor: {doctor_name}
Doctor Phone: {doctor_phone}
Hospital/Affiliation: {doctor_affiliation}
Feedback: {feedback_notes[:150]}{'...' if len(feedback_notes) > 150 else ''}
        
Submitted: {current_datetime}
        """
    
    print("SMS MESSAGE FORMAT:")
    print(sms_message)
    
    print(f"\nMessage Length: {len(sms_message)} characters")
    print(f"Message Segments: {len(sms_message) // 160 + 1 if len(sms_message) > 160 else 1}")
    
    return sms_message

def test_backend_api():
    """Test the backend API referral feedback endpoint"""
    print("\n" + "=" * 60)
    print("TESTING BACKEND API")
    print("=" * 60)
    
    # Test data
    test_data = {
        "patient_name": "Test Patient",
        "feedback_notes": "This is a test feedback message for SMS testing purposes.",
        "doctor_name": "Dr. Test Doctor",
        "doctor_phone": "+23212345678",
        "doctor_affiliation": "Test Hospital"
    }
    
    # Backend URL (adjust as needed)
    backend_url = "http://localhost:5000/api/referral-feedback"
    
    try:
        print(f"Testing API endpoint: {backend_url}")
        print(f"Test data: {json.dumps(test_data, indent=2)}")
        
        response = requests.post(
            backend_url,
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"Response Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ API test successful!")
            print(f"Feedback ID: {result.get('feedback_id')}")
            print(f"SMS Sent: {result.get('sms_sent')}")
            print(f"Timestamp: {result.get('timestamp')}")
            return True
        else:
            print(f"❌ API test failed!")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend API!")
        print("Make sure the Flask app is running on localhost:5000")
        return False
    except Exception as e:
        print(f"❌ API test error: {str(e)}")
        return False

def test_mock_sms():
    """Test SMS sending with mock data (no real SMS sent)"""
    print("\n" + "=" * 60)
    print("TESTING MOCK SMS SENDING")
    print("=" * 60)
    
    try:
        from twilio.rest import Client
        
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        from_number = os.getenv('TWILIO_PHONE_NUMBER')
        
        if not all([account_sid, auth_token, from_number]):
            print("❌ Twilio credentials not configured for mock test")
            return False
        
        client = Client(account_sid, auth_token)
        
        # Test message
        test_message = "This is a test SMS from MamaCare Healthcare System. If you receive this, SMS functionality is working correctly!"
        test_to_number = "+23212345678"  # Replace with your test number
        
        print(f"From: {from_number}")
        print(f"To: {test_to_number}")
        print(f"Message: {test_message}")
        
        # Uncomment the following lines to actually send SMS
        # print("\n⚠️  WARNING: This will send a real SMS!")
        # confirm = input("Do you want to send a real SMS? (yes/no): ")
        # if confirm.lower() == 'yes':
        #     message = client.messages.create(
        #         body=test_message,
        #         from_=from_number,
        #         to=test_to_number
        #     )
        #     print(f"✅ SMS sent successfully!")
        #     print(f"Message SID: {message.sid}")
        #     return True
        # else:
        #     print("SMS sending cancelled")
        #     return False
        
        print("\n✅ Mock SMS test completed (no real SMS sent)")
        print("To send real SMS, uncomment the lines in the test_mock_sms function")
        return True
        
    except Exception as e:
        print(f"❌ Mock SMS test failed: {str(e)}")
        return False

def test_referral_feedback_flow():
    """Test the complete referral feedback flow"""
    print("\n" + "=" * 60)
    print("TESTING COMPLETE REFERRAL FEEDBACK FLOW")
    print("=" * 60)
    
    # Test data for referral feedback
    feedback_data = {
        "patient_name": "Mary Johnson",
        "feedback_notes": "Patient completed treatment successfully. All vital signs normal. Recommended follow-up in 2 weeks.",
        "doctor_name": "Dr. Sarah Ahmed",
        "doctor_phone": "+23278656832",
        "doctor_affiliation": "Connaught Hospital",
        "referral_source": "PresTrack"
    }
    
    print("1. Testing referral feedback submission...")
    
    try:
        response = requests.post(
            "http://localhost:5000/api/referral-feedback",
            json=feedback_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 201:
            result = response.json()
            print("✅ Referral feedback submitted successfully!")
            print(f"   Feedback ID: {result.get('feedback_id')}")
            print(f"   SMS Sent: {result.get('sms_sent')}")
            print(f"   Timestamp: {result.get('timestamp')}")
            
            # Test retrieving the feedback
            print("\n2. Testing feedback retrieval...")
            feedback_id = result.get('feedback_id')
            
            get_response = requests.get(
                f"http://localhost:5000/api/referral-feedback/{feedback_id}",
                timeout=10
            )
            
            if get_response.status_code == 200:
                feedback_detail = get_response.json()
                print("✅ Feedback retrieved successfully!")
                print(f"   Patient: {feedback_detail.get('patient_name')}")
                print(f"   Doctor: {feedback_detail.get('doctor_name')}")
                print(f"   SMS Sent: {feedback_detail.get('sms_sent')}")
                print(f"   SMS Sent At: {feedback_detail.get('sms_sent_at')}")
                return True
            else:
                print(f"❌ Failed to retrieve feedback: {get_response.status_code}")
                return False
        else:
            print(f"❌ Failed to submit feedback: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Referral feedback flow test failed: {str(e)}")
        return False

def main():
    """Run all SMS tests"""
    print("MAMACARE SMS TESTING SUITE")
    print("=" * 60)
    print("This script tests the Twilio SMS functionality for referral feedback")
    print("=" * 60)
    
    tests = [
        ("Twilio Credentials", test_twilio_credentials),
        ("Twilio Connection", test_twilio_connection),
        ("SMS Format", test_sms_format),
        ("Backend API", test_backend_api),
        ("Mock SMS", test_mock_sms),
        ("Referral Feedback Flow", test_referral_feedback_flow)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! SMS functionality is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the configuration and try again.")
    
    print("\n" + "=" * 60)
    print("NEXT STEPS")
    print("=" * 60)
    print("1. If all tests pass, your SMS functionality is ready for production")
    print("2. To test real SMS sending, uncomment the lines in test_mock_sms()")
    print("3. Make sure to use a valid phone number for testing")
    print("4. Monitor your Twilio account for SMS charges")
    print("=" * 60)

if __name__ == "__main__":
    main() 