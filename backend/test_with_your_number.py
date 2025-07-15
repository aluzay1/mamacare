#!/usr/bin/env python3
"""
Test Referral Feedback SMS with Your Phone Number
This script temporarily changes the PresTrack number to test SMS sending
"""

import os
import sys
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_with_your_number():
    """Test referral feedback with your phone number"""
    print("=" * 60)
    print("TESTING REFERRAL FEEDBACK WITH YOUR PHONE NUMBER")
    print("=" * 60)
    
    # Get your phone number
    print("Enter your phone number to receive the test SMS:")
    print("Format: +23212345678 (Sierra Leone format)")
    your_number = input("Your phone number: ").strip()
    
    if not your_number:
        print("❌ No phone number provided. Test cancelled.")
        return
    
    # Validate phone number format
    if not your_number.startswith('+232') or len(your_number) != 12:
        print("❌ Invalid phone number format. Must be +232XXXXXXXX")
        return
    
    print(f"\n📱 Will send SMS to: {your_number}")
    confirm = input("Continue? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print("❌ Test cancelled.")
        return
    
    # Test data
    test_data = {
        "patient_name": "SMS Test Patient",
        "feedback_notes": "This is a test referral feedback to verify SMS functionality. Patient is responding well to treatment and all vital signs are normal.",
        "doctor_name": "Dr. Test Doctor",
        "doctor_phone": "+23212345678",
        "doctor_affiliation": "Test Hospital",
        "referral_source": "PresTrack"
    }
    
    print("\n📡 Sending referral feedback...")
    
    try:
        response = requests.post(
            "http://localhost:5000/api/referral-feedback",
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 201:
            result = response.json()
            print("✅ Referral feedback submitted successfully!")
            print(f"   Feedback ID: {result.get('feedback_id')}")
            print(f"   SMS Sent: {result.get('sms_sent')}")
            
            if result.get('sms_sent'):
                print("🎉 SMS was sent successfully!")
                print(f"   Check your phone ({your_number}) for the SMS")
            else:
                print("⚠️  SMS was NOT sent!")
                print("   The system is trying to send to +23233237891 (hardcoded)")
                print("   To fix this, we need to update the code to use your number")
                
                # Offer to create a modified version
                print("\n🔧 Would you like me to create a temporary version that uses your number?")
                modify = input("Create modified version? (yes/no): ").strip().lower()
                
                if modify == 'yes':
                    create_modified_version(your_number)
        else:
            print(f"❌ API request failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")

def create_modified_version(your_number):
    """Create a modified version of the app with your phone number"""
    print(f"\n🔧 Creating modified version with your number: {your_number}")
    
    try:
        # Read the current app.py
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the hardcoded number
        modified_content = content.replace(
            'prestrack_number = "+23233237891"  # Fixed number for PresTrack',
            f'prestrack_number = "{your_number}"  # Your number for testing'
        )
        
        # Create backup
        with open('app_backup_before_test.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Write modified version
        with open('app_modified.py', 'w', encoding='utf-8') as f:
            f.write(modified_content)
        
        print("✅ Modified version created: app_modified.py")
        print("📝 Original backed up as: app_backup_before_test.py")
        print("\n🚀 To test with your number:")
        print("1. Stop the current Flask app (Ctrl+C)")
        print("2. Run: python app_modified.py")
        print("3. Submit referral feedback again")
        print("4. Check your phone for SMS")
        
    except Exception as e:
        print(f"❌ Failed to create modified version: {str(e)}")

def main():
    """Main function"""
    print("REFERRAL FEEDBACK SMS TEST WITH YOUR NUMBER")
    print("=" * 60)
    
    test_with_your_number()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print("The issue is that the SMS is being sent to a hardcoded number")
    print("(+23233237891) instead of a valid number.")
    print("\nTo fix this permanently, you can:")
    print("1. Update the PresTrack number in app.py")
    print("2. Make it configurable via environment variable")
    print("3. Allow it to be set per referral feedback")
    print("=" * 60)

if __name__ == "__main__":
    main() 