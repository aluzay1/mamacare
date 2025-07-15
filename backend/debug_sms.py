#!/usr/bin/env python3
"""
Debug SMS Function - Test the SMS function directly to see what's happening
"""

import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up detailed logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def debug_sms_function():
    """Debug the SMS function directly"""
    print("=" * 60)
    print("DEBUGGING SMS FUNCTION")
    print("=" * 60)
    
    # Check Twilio availability
    try:
        from twilio.rest import Client
        print("✅ Twilio library is available")
        TWILIO_AVAILABLE = True
    except ImportError:
        print("❌ Twilio library not installed")
        TWILIO_AVAILABLE = False
        return
    
    if not TWILIO_AVAILABLE:
        print("❌ Twilio not available")
        return
    
    # Check credentials
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    from_number = os.getenv('TWILIO_PHONE_NUMBER')
    
    print(f"Account SID: {'✅ Set' if account_sid else '❌ Not set'}")
    print(f"Auth Token: {'✅ Set' if auth_token else '❌ Not set'}")
    print(f"From Number: {'✅ Set' if from_number else '❌ Not set'}")
    
    if not all([account_sid, auth_token, from_number]):
        print("❌ Missing Twilio credentials")
        return
    
    # Test Twilio client
    try:
        client = Client(account_sid, auth_token)
        print("✅ Twilio client created successfully")
        
        # Get account info
        account = client.api.accounts(account_sid).fetch()
        print(f"Account Name: {account.friendly_name}")
        print(f"Account Status: {account.status}")
        print(f"Account Type: {account.type}")
        
    except Exception as e:
        print(f"❌ Twilio client error: {str(e)}")
        return
    
    # Test SMS sending
    test_message = "This is a debug test SMS from MamaCare system."
    test_to_number = "+23278656832"  # Your number
    
    print(f"\n📱 Testing SMS:")
    print(f"   From: {from_number}")
    print(f"   To: {test_to_number}")
    print(f"   Message: {test_message}")
    
    confirm = input(f"\nSend test SMS to {test_to_number}? (yes/no): ").strip().lower()
    
    if confirm == 'yes':
        try:
            print("\n📤 Sending SMS...")
            
            message = client.messages.create(
                body=test_message,
                from_=from_number,
                to=test_to_number
            )
            
            print("✅ SMS sent successfully!")
            print(f"   Message SID: {message.sid}")
            print(f"   Status: {message.status}")
            print(f"   To: {message.to}")
            print(f"   From: {message.from_}")
            print(f"   Error Code: {message.error_code}")
            print(f"   Error Message: {message.error_message}")
            
            return True
            
        except Exception as e:
            print(f"❌ SMS sending failed: {str(e)}")
            print(f"Error type: {type(e).__name__}")
            return False
    else:
        print("❌ SMS test cancelled")
        return False

def test_referral_sms_function():
    """Test the exact SMS function from the app"""
    print("\n" + "=" * 60)
    print("TESTING REFERRAL SMS FUNCTION")
    print("=" * 60)
    
    def send_sms_via_twilio(to_number, message):
        """Send SMS using Twilio API - copied from app.py"""
        try:
            from twilio.rest import Client
            TWILIO_AVAILABLE = True
        except ImportError:
            print("Twilio not available")
            return False
        
        if not TWILIO_AVAILABLE:
            print("Twilio not available")
            return False
        
        try:
            # Get Twilio credentials from environment variables
            account_sid = os.getenv('TWILIO_ACCOUNT_SID')
            auth_token = os.getenv('TWILIO_AUTH_TOKEN')
            from_number = os.getenv('TWILIO_PHONE_NUMBER')
            
            if not all([account_sid, auth_token, from_number]):
                print("Twilio credentials not configured")
                return False
            
            # Initialize Twilio client
            client = Client(account_sid, auth_token)
            
            # Send SMS
            message_obj = client.messages.create(
                body=message,
                from_=from_number,
                to=to_number
            )
            
            print(f"SMS sent successfully: {message_obj.sid}")
            return True
            
        except Exception as e:
            print(f"Error sending SMS: {str(e)}")
            return False
    
    # Test the referral SMS format
    from datetime import datetime
    
    def format_datetime_with_ordinal(datetime_obj):
        """Format datetime as '30th June, 2025 at 2:30 PM'"""
        if not datetime_obj:
            return "Unknown"
        
        day = datetime_obj.day
        month = datetime_obj.strftime('%B')
        year = datetime_obj.year
        time = datetime_obj.strftime('%I:%M %p')
        
        if 10 <= day % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
        
        return f"{day}{suffix} {month}, {year} at {time}"
    
    # Create the exact SMS message format
    current_datetime = format_datetime_with_ordinal(datetime.now())
    
    sms_message = f"""REFERRAL FEEDBACK - MamaCare
        
Patient ID: TEST123
Patient: Test Patient
Patient Contact: +23212345678
Doctor: Dr. Test Doctor
Doctor Phone: +23212345678
Hospital/Affiliation: Test Hospital
Feedback: This is a test referral feedback to verify SMS functionality.
        
Submitted: {current_datetime}
        """
    
    print("SMS Message:")
    print(sms_message)
    
    # Test sending
    test_number = "+23278656832"
    print(f"\n📱 Testing referral SMS to: {test_number}")
    
    confirm = input("Send referral SMS? (yes/no): ").strip().lower()
    
    if confirm == 'yes':
        result = send_sms_via_twilio(test_number, sms_message)
        if result:
            print("✅ Referral SMS sent successfully!")
        else:
            print("❌ Referral SMS failed!")
        return result
    else:
        print("❌ Test cancelled")
        return False

if __name__ == "__main__":
    debug_sms_function()
    test_referral_sms_function() 