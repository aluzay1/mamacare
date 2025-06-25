import requests
import json

def test_profile_access():
    url = 'http://localhost:5000/api/patient/profile'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Access-Control-Allow-Origin': '*'
    }
    
    # Get user input for email and PIN
    email = input("Enter your email: ")
    pin = input("Enter your PIN: ")
    
    data = {
        'email': email,
        'pin': pin
    }
    
    try:
        print(f"\nSending request to: {url}")
        print(f"With data: {json.dumps(data, indent=2)}")
        
        response = requests.post(url, json=data, headers=headers)
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response Headers: {json.dumps(dict(response.headers), indent=2)}")
        
        try:
            response_json = response.json()
            print(f"Response Body: {json.dumps(response_json, indent=2)}")
        except json.JSONDecodeError:
            print(f"Raw Response Body: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the server. Make sure the backend is running.")
    except requests.exceptions.RequestException as e:
        print(f"\nError making request: {str(e)}")
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")

if __name__ == '__main__':
    test_profile_access() 