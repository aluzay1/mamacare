import requests
import json

def get_pins():
    try:
        # Make a request to the debug pins endpoint
        response = requests.get('http://localhost:5000/api/debug/pins')
        
        if response.status_code == 200:
            data = response.json()
            pins = data.get('pins', [])
            
            if pins:
                print("Existing PINs in the database:")
                print("-" * 50)
                for pin_data in pins:
                    print(f"ID: {pin_data['id']}")
                    print(f"Email: {pin_data['email']}")
                    print(f"PIN: {pin_data['pin']}")
                    print("-" * 30)
                
                # Return the first PIN for easy testing
                if pins:
                    first_pin = pins[0]['pin']
                    print(f"\nYou can use this PIN for testing: {first_pin}")
                    return first_pin
            else:
                print("No PINs found in the database.")
                print("You need to register a patient first to get a PIN.")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the Flask server.")
        print("Make sure your Flask app is running on http://localhost:5000")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    get_pins() 