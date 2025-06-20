from app import app, db, Hospital, Doctor, User
from datetime import datetime, date
import json

def add_test_data():
    with app.app_context():
        # Add test hospital
        hospital = Hospital(
            name='Test Hospital',
            license_number='HOSP001',
            address='123 Test Street',
            city='Freetown',
            state='Western Area',
            postal_code='12345',
            country='Sierra Leone',
            phone='+23212345678',
            email='test@hospital.com',
            website='www.testhospital.com',
            services='["General Medicine", "Pediatrics", "Obstetrics"]',
            is_verified=True
        )
        
        # Add test doctor
        doctor = Doctor(
            name='Dr. Test Doctor',
            license_number='DOC001',
            specialization='General Medicine',
            email='test@doctor.com',
            phone='+23287654321',
            hospital_affiliation='Test Hospital',
            address='123 Test Street',
            city='Freetown',
            state='Western Area',
            country='Sierra Leone',
            is_verified=True
        )
        
        # Add test female patient with pregnancy data
        test_patient = User(
            name='Sarah Johnson',
            email='sarah@test.com',
            password='hashed_password',
            role='individual',
            phone='+23212345678',
            gender='female',
            date_of_birth=date(1995, 6, 15),
            blood_type='O+',
            address_line='456 Test Avenue',
            city='Freetown',
            state='Western Area',
            country='Sierra Leone',
            marital_status='married',
            language='en',
            nationality='Sierra Leonean',
            allergies='None',
            medications='Prenatal vitamins',
            emergency_contact_name='John Johnson',
            emergency_contact_phone='+23287654321',
            emergency_contact_relationship='Husband',
            pin='123456',  # Test PIN
            # Pregnancy data
            pregnancy_status='pregnant',
            previous_pregnancies=1,
            lmp_date=date(2024, 1, 15),  # January 15, 2024
            due_date=date(2024, 10, 21),  # October 21, 2024
            gestational_age=28,
            multiple_pregnancy='no',
            risk_level='low',
            risk_factors=json.dumps(['None']),
            blood_pressure='120/80',
            hemoglobin=12.5,
            blood_sugar=95.0,
            weight=65.0,
            prenatal_vitamins='Folic acid, Iron supplements',
            pregnancy_complications='None',
            emergency_hospital='Test Hospital',
            birth_plan='Natural birth at Test Hospital'
        )
        
        try:
            db.session.add(hospital)
            db.session.add(doctor)
            db.session.add(test_patient)
            db.session.commit()
            print("Test data added successfully!")
            print(f"Test patient PIN: {test_patient.pin}")
            print(f"Test patient gender: {test_patient.gender}")
        except Exception as e:
            db.session.rollback()
            print(f"Error adding test data: {str(e)}")

if __name__ == '__main__':
    add_test_data() 