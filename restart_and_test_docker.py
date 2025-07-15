#!/usr/bin/env python3
"""
Restart Docker Containers and Test SMS
"""

import subprocess
import time
import requests
import json

def restart_docker_containers():
    """Restart Docker containers"""
    print("=" * 60)
    print("RESTARTING DOCKER CONTAINERS")
    print("=" * 60)
    
    try:
        print("🔄 Stopping Docker containers...")
        subprocess.run(["docker-compose", "down"], check=True)
        print("✅ Docker containers stopped")
        
        print("🔄 Starting Docker containers...")
        subprocess.run(["docker-compose", "up", "-d"], check=True)
        print("✅ Docker containers started")
        
        print("⏳ Waiting for containers to be ready...")
        time.sleep(10)  # Wait for containers to start
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error restarting containers: {e}")
        return False
    except FileNotFoundError:
        print("❌ Docker Compose not found. Please run manually:")
        print("   docker-compose down")
        print("   docker-compose up -d")
        return False

def test_sms_after_restart():
    """Test SMS after Docker restart"""
    print("\n" + "=" * 60)
    print("TESTING SMS AFTER DOCKER RESTART")
    print("=" * 60)
    
    # Wait a bit more for Flask to be ready
    print("⏳ Waiting for Flask app to be ready...")
    time.sleep(5)
    
    # Test health endpoint
    try:
        health_response = requests.get("http://localhost:5000/health", timeout=10)
        if health_response.status_code == 200:
            print("✅ Flask app is ready after restart")
        else:
            print("⚠️  Flask app health check failed")
            return False
    except Exception as e:
        print(f"❌ Flask app not ready: {e}")
        return False
    
    # Test SMS with verified number
    verified_number = "+23233237891"
    print(f"\n📱 Testing SMS with verified number: {verified_number}")
    
    test_data = {
        "patient_name": "Post-Restart Test Patient",
        "feedback_notes": "This is a test after Docker restart to verify SMS functionality.",
        "doctor_name": "Dr. Post-Restart Test",
        "doctor_phone": "+23212345678",
        "doctor_affiliation": "Post-Restart Hospital",
        "referral_source": "PresTrack"
    }
    
    try:
        response = requests.post(
            "http://localhost:5000/api/referral-feedback",
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 201:
            result = response.json()
            print("✅ Referral feedback submitted after restart!")
            print(f"   Feedback ID: {result.get('feedback_id')}")
            print(f"   SMS Sent: {result.get('sms_sent')}")
            
            if result.get('sms_sent'):
                print("🎉 SMS was sent successfully after restart!")
                print("✅ Docker restart fixed the SMS issue!")
                return True
            else:
                print("⚠️  SMS still not sending after restart")
                print("   The issue might be with the verified number itself")
                return False
        else:
            print(f"❌ API failed after restart: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed after restart: {e}")
        return False

def main():
    """Main function"""
    print("DOCKER RESTART AND SMS TEST")
    print("=" * 60)
    
    # Ask user if they want to restart
    print("This will restart your Docker containers to apply code changes.")
    restart = input("Restart Docker containers? (yes/no): ").strip().lower()
    
    if restart == 'yes':
        # Restart containers
        if restart_docker_containers():
            # Test SMS after restart
            success = test_sms_after_restart()
            
            # Summary
            print("\n" + "=" * 60)
            print("RESTART TEST SUMMARY")
            print("=" * 60)
            
            if success:
                print("🎉 Docker restart and SMS test successful!")
                print("✅ Your SMS system is working in Docker!")
            else:
                print("⚠️  SMS still not working after restart")
                print("   The issue might be with the verified number +23233237891")
                print("   Consider checking Twilio console for verification status")
        else:
            print("❌ Failed to restart Docker containers")
    else:
        print("❌ Docker restart cancelled")
    
    print("\n" + "=" * 60)
    print("MANUAL RESTART COMMANDS")
    print("=" * 60)
    print("If you prefer to restart manually:")
    print("1. docker-compose down")
    print("2. docker-compose up -d")
    print("3. Wait for containers to start")
    print("4. Test SMS functionality")
    print("=" * 60)

if __name__ == "__main__":
    main() 