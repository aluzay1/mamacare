#!/usr/bin/env python3
"""
Test script for FHIR-compliant patient registration
This script demonstrates the updated MamaCare patient registration with full FHIR compliance.
"""

import requests
import json
from datetime import datetime, date

# Configuration
API_BASE_URL = "http://localhost:5000"

def test_patient_registration():
    """Test the FHIR-compliant patient registration endpoint"""
    
    # Sample patient data for testing
    patient_data = {
        "email": "jane.doe@example.com",
        "name": "Jane Marie Doe",
        "given_name": "Jane",
        "middle_name": "Marie",
        "family_name": "Doe",
        "gender": "female",
        "date_of_birth": "1990-05-15",
        "phone": "+232123456789",
        "address_line": "123 Main Street",
        "city": "Freetown",
        "state": "Western Area",
        "country": "Sierra Leone",
        "marital_status": "married",
        "language": "en",
        "nationality": "Sierra Leonean",
        "blood_type": "O+",
        "allergies": ["penicillin", "aspirin"],
        "medications": ["folic_acid", "prenatal_vitamins"],
        "emergency_contact_name": "John Doe",
        "emergency_contact_phone": "+232987654321",
        "emergency_contact_relationship": "spouse",
        
        # Pregnancy-related fields (only for females)
        "pregnancy_status": "pregnant",
        "previous_pregnancies": 1,
        "lmp_date": "2024-01-15",
        "multiple_pregnancy": "no",
        "risk_level": "low",
        "risk_factors": ["age"],
        "blood_pressure": "120/80",
        "hemoglobin": 12.5,
        "blood_sugar": 95,
        "weight": 65.5,
        "prenatal_vitamins": "yes",
        "pregnancy_complications": ["gestational_diabetes"],
        "emergency_hospital": "Connaught Hospital",
        "birth_plan": "Natural birth with epidural if needed. Partner to be present during labor."
    }
    
    print("Testing FHIR-compliant patient registration...")
    print("=" * 60)
    print(f"API Endpoint: {API_BASE_URL}/api/patient/register")
    print(f"Request Method: POST")
    print(f"Content-Type: application/json")
    print()
    
    print("Sample Request Payload:")
    print(json.dumps(patient_data, indent=2))
    print()
    
    try:
        # Make the API request
        response = requests.post(
            f"{API_BASE_URL}/api/patient/register",
            headers={"Content-Type": "application/json"},
            json=patient_data,
            timeout=30
        )
        
        print(f"Response Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print()
        
        if response.status_code == 201:
            result = response.json()
            print("✅ Registration Successful!")
            print("Response Data:")
            print(json.dumps(result, indent=2))
            print()
            
            print("📋 Generated FHIR Resources:")
            if 'fhir_resources_created' in result:
                for resource in result['fhir_resources_created']:
                    print(f"  • {resource}")
            print()
            
            print("🔑 Access Information:")
            print(f"  • Patient ID: {result.get('patient_id')}")
            print(f"  • FHIR ID: {result.get('fhir_id')}")
            print(f"  • PIN: {result.get('pin')}")
            print(f"  • Email Sent: {result.get('email_sent')}")
            
        else:
            print("❌ Registration Failed!")
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Could not connect to the API server.")
        print("Make sure the Flask application is running on http://localhost:5000")
    except requests.exceptions.Timeout:
        print("❌ Timeout Error: Request timed out.")
    except Exception as e:
        print(f"❌ Unexpected Error: {str(e)}")

def generate_curl_command():
    """Generate a curl command for testing"""
    
    sample_data = {
        "email": "jane.doe@example.com",
        "name": "Jane Marie Doe",
        "given_name": "Jane",
        "middle_name": "Marie",
        "family_name": "Doe",
        "gender": "female",
        "date_of_birth": "1990-05-15",
        "phone": "+232123456789",
        "address_line": "123 Main Street",
        "city": "Freetown",
        "state": "Western Area",
        "country": "Sierra Leone",
        "marital_status": "married",
        "language": "en",
        "nationality": "Sierra Leonean",
        "blood_type": "O+",
        "allergies": ["penicillin", "aspirin"],
        "medications": ["folic_acid", "prenatal_vitamins"],
        "emergency_contact_name": "John Doe",
        "emergency_contact_phone": "+232987654321",
        "emergency_contact_relationship": "spouse",
        "pregnancy_status": "pregnant",
        "previous_pregnancies": 1,
        "lmp_date": "2024-01-15",
        "multiple_pregnancy": "no",
        "risk_level": "low",
        "risk_factors": ["age"],
        "blood_pressure": "120/80",
        "hemoglobin": 12.5,
        "blood_sugar": 95,
        "weight": 65.5,
        "prenatal_vitamins": "yes",
        "pregnancy_complications": ["gestational_diabetes"],
        "emergency_hospital": "Connaught Hospital",
        "birth_plan": "Natural birth with epidural if needed. Partner to be present during labor."
    }
    
    print("Curl Command for Testing:")
    print("=" * 60)
    print()
    
    curl_command = f"""curl -X POST {API_BASE_URL}/api/patient/register \\
  -H "Content-Type: application/json" \\
  -d '{json.dumps(sample_data)}'"""
    
    print(curl_command)
    print()

def show_fhir_resources():
    """Show the FHIR resources that would be created"""
    
    print("FHIR Resources Created:")
    print("=" * 60)
    print()
    
    resources = [
        {
            "resource": "Patient",
            "description": "Main patient resource with custom extensions",
            "extensions": [
                "Blood Type",
                "Nationality", 
                "Pregnancy Status",
                "LMP Date",
                "Due Date",
                "Gestational Age",
                "Multiple Pregnancy",
                "Risk Level",
                "Previous Pregnancies",
                "Prenatal Vitamins",
                "Emergency Hospital"
            ]
        },
        {
            "resource": "Observation",
            "description": "Clinical measurements",
            "codes": [
                "LOINC 55284-4 (Blood pressure panel)",
                "LOINC 718-7 (Hemoglobin)",
                "LOINC 2339-0 (Glucose)",
                "LOINC 29463-7 (Body weight)"
            ]
        },
        {
            "resource": "AllergyIntolerance",
            "description": "Patient allergies",
            "coding": "SNOMED CT 419199007"
        },
        {
            "resource": "MedicationStatement",
            "description": "Current medications",
            "coding": "RxNorm"
        },
        {
            "resource": "Condition",
            "description": "Pregnancy complications and risk factors",
            "coding": "SNOMED CT 77386006"
        },
        {
            "resource": "CarePlan",
            "description": "Birth plan",
            "category": "Pregnancy care plan"
        }
    ]
    
    for resource in resources:
        print(f"📋 {resource['resource']}")
        print(f"   Description: {resource['description']}")
        if 'extensions' in resource:
            print(f"   Extensions: {', '.join(resource['extensions'])}")
        if 'codes' in resource:
            print(f"   Codes: {', '.join(resource['codes'])}")
        if 'coding' in resource:
            print(f"   Coding: {resource['coding']}")
        if 'category' in resource:
            print(f"   Category: {resource['category']}")
        print()

if __name__ == "__main__":
    print("MamaCare FHIR-Compliant Patient Registration Test")
    print("=" * 60)
    print()
    
    # Show FHIR resources
    show_fhir_resources()
    
    # Generate curl command
    generate_curl_command()
    
    # Test registration
    test_patient_registration() 