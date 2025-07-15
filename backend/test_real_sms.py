#!/usr/bin/env python3
"""
Real SMS Testing Script for MamaCare
Use this to test actual SMS sending to your phone number
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def send_test_sms():
    """Send a real test SMS"""
    try:
        from twilio.rest import Client
        
        # Get Twilio credentials
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        from_number = os.getenv('TWILIO_PHONE_NUMBER')
        
        if not all([account_sid, auth_token, from_number]):
            print("❌ Twilio credentials not configured!")
            return
        
        client = Client(account_sid, auth_token)
        
        # Test message
        test_message = """MAMACARE SMS TEST

This is a test SMS from your MamaCare Healthcare System.

✅ Twilio integration is working correctly!
✅ SMS functionality is operational!
✅ Your healthcare system is ready for production!

Best regards,
MamaCare Team"""
        
        # Get recipient number from user
        print("=" * 60)
        print("REAL SMS TEST")
        print("=" * 60)
        print(f"From: {from_number}")
        print(f"Message: {test_message}")
        print("\n⚠️  WARNING: This will send a real SMS and may incur charges!")
        
        to_number = input("Enter your phone number (e.g., +23212345678): ").strip()
        
        if not to_number:
            print("❌ No phone number provided. Test cancelled.")
            return
        
        # Confirm before sending
        confirm = input(f"\nSend SMS to {to_number}? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            print("\n📱 Sending SMS...")
            
            message = client.messages.create(
                body=test_message,
                from_=from_number,
                to=to_number
            )
            
            print("✅ SMS sent successfully!")
            print(f"Message SID: {message.sid}")
            print(f"Status: {message.status}")
            print(f"To: {message.to}")
            print(f"From: {message.from_}")
            print(f"Body: {message.body}")
            
        else:
            print("❌ SMS sending cancelled.")
            
    except ImportError:
        print("❌ Twilio library not installed!")
        print("Install with: pip install twilio")
    except Exception as e:
        print(f"❌ SMS sending failed: {str(e)}")

if __name__ == "__main__":
    send_test_sms() 