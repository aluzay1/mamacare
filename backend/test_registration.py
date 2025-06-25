import requests
import json
import random
import string

def generate_random_email():
    """Generate a random email for testing"""
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{username}@test.com"

def test_registration():
    """Test the patient registration endpoint"""
    
    # Generate random test data
    test_email = generate_random_email()
    test_data = {
        "name": "Test Patient",
        "email": test_email,
        "phone": "1234567890",
        "date_of_birth": "1990-01-01",
        "gender": "Female",
        "address": "123 Test Street",
        "emergency_contact": "0987654321",
        "medical_history": "None",
        "allergies": "None"
    }
    
    print(f"Testing registration with email: {test_email}")
    print(f"Test data: {json.dumps(test_data, indent=2)}")
    
    try:
        # Test the registration endpoint
        response = requests.post(
            "http://localhost:5000/api/patient/register",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\nResponse Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"SUCCESS: Registration successful!")
            print(f"Response: {json.dumps(result, indent=2)}")
            
            if 'pin' in result:
                print(f"\n🔑 PIN Code: {result['pin']}")
                print(f"📧 Email: {test_email}")
                print("Check your email inbox for the registration confirmation!")
            
            return True
        else:
            print(f"ERROR: Registration failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to the server. Make sure the Flask app is running on port 5000.")
        return False
    except Exception as e:
        print(f"ERROR: Unexpected error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Patient Registration with Email...")
    print("=" * 50)
    test_registration() 