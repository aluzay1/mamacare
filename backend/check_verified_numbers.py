#!/usr/bin/env python3
"""
Check Verified Phone Numbers in Twilio Account
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_verified_numbers():
    """Check verified phone numbers in Twilio account"""
    print("=" * 60)
    print("CHECKING VERIFIED PHONE NUMBERS")
    print("=" * 60)
    
    try:
        from twilio.rest import Client
        
        # Get Twilio credentials
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        
        if not all([account_sid, auth_token]):
            print("❌ Twilio credentials not configured!")
            return
        
        client = Client(account_sid, auth_token)
        
        # Get verified caller IDs
        print("📱 Checking verified caller IDs...")
        try:
            verified_numbers = client.verified_caller_ids.list()
            
            if verified_numbers:
                print(f"✅ Found {len(verified_numbers)} verified number(s):")
                for number in verified_numbers:
                    print(f"   📞 {number.phone_number}")
                    print(f"      Status: {number.status}")
                    print(f"      Verified: {number.verified}")
                    print()
            else:
                print("❌ No verified numbers found!")
                print("\n🔧 To verify your number:")
                print("1. Go to: https://console.twilio.com/")
                print("2. Navigate to: Phone Numbers → Verified Caller IDs")
                print("3. Add your phone number: +23278656832")
                print("4. Verify it by receiving a code")
        except Exception as e:
            print(f"❌ Error checking verified numbers: {str(e)}")
            print("\n🔧 To verify your number manually:")
            print("1. Go to: https://console.twilio.com/")
            print("2. Navigate to: Phone Numbers → Verified Caller IDs")
            print("3. Add your phone number: +23278656832")
            print("4. Verify it by receiving a code")
        
        # Get Twilio phone numbers
        print("📱 Checking Twilio phone numbers...")
        twilio_numbers = client.incoming_phone_numbers.list()
        
        if twilio_numbers:
            print(f"✅ Found {len(twilio_numbers)} Twilio number(s):")
            for number in twilio_numbers:
                print(f"   📞 {number.phone_number}")
                print(f"      Friendly Name: {number.friendly_name}")
                print(f"      Status: {number.status}")
                print()
        else:
            print("❌ No Twilio phone numbers found!")
        
    except ImportError:
        print("❌ Twilio library not installed!")
    except Exception as e:
        print(f"❌ Error checking numbers: {str(e)}")

if __name__ == "__main__":
    check_verified_numbers() 