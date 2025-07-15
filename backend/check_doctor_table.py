#!/usr/bin/env python3
import os
import sys
from app import app, db, Doctor

def check_doctor_table():
    with app.app_context():
        try:
            # Check if the doctor table exists
            result = db.engine.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'doctor')")
            table_exists = result.fetchone()[0]
            
            if table_exists:
                print("✅ Doctor table exists")
                
                # Check table structure
                result = db.engine.execute("""
                    SELECT column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns 
                    WHERE table_name = 'doctor'
                    ORDER BY ordinal_position
                """)
                
                print("\n📋 Doctor table structure:")
                for row in result:
                    print(f"  - {row[0]}: {row[1]} (nullable: {row[2]}, default: {row[3]})")
                
                # Check if there are any existing doctors
                doctor_count = Doctor.query.count()
                print(f"\n👥 Number of existing doctors: {doctor_count}")
                
                # Try to create a test doctor
                print("\n🧪 Testing doctor creation...")
                try:
                    test_doctor = Doctor(
                        name="Test Doctor",
                        license_number="TEST123",
                        email="test@example.com",
                        phone="+23212345678",
                        professional_type="Medical Doctor",
                        specialization="Test",
                        hospital_affiliation="Test Hospital",
                        pin="123456"
                    )
                    db.session.add(test_doctor)
                    db.session.commit()
                    print("✅ Test doctor created successfully")
                    
                    # Clean up
                    db.session.delete(test_doctor)
                    db.session.commit()
                    print("✅ Test doctor cleaned up")
                    
                except Exception as e:
                    print(f"❌ Error creating test doctor: {str(e)}")
                    db.session.rollback()
                
            else:
                print("❌ Doctor table does not exist")
                
        except Exception as e:
            print(f"❌ Error checking doctor table: {str(e)}")

if __name__ == "__main__":
    check_doctor_table() 