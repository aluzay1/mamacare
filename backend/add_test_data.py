from app import app, db, Hospital, Doctor
from datetime import datetime

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
        
        try:
            db.session.add(hospital)
            db.session.add(doctor)
            db.session.commit()
            print("Test data added successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error adding test data: {str(e)}")

if __name__ == '__main__':
    add_test_data() 