#!/usr/bin/env python3
"""
Migration script to create birth_records table
This will run automatically on Render deployment
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from sqlalchemy import text

def create_birth_records_table():
    """Create the birth_records table using SQLAlchemy"""
    with app.app_context():
        try:
            # Check if the table already exists
            result = db.session.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'birth_record'
                );
            """))
            
            table_exists = result.scalar()
            
            if not table_exists:
                # Create the birth_records table
                db.session.execute(text("""
                    CREATE TABLE birth_record (
                        id SERIAL PRIMARY KEY,
                        patient_id INTEGER NOT NULL,
                        baby_gender VARCHAR(10) NOT NULL,
                        date_of_birth DATE NOT NULL,
                        birth_type VARCHAR(50) NOT NULL,
                        birth_location VARCHAR(200) NOT NULL,
                        notes TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (patient_id) REFERENCES "user" (id) ON DELETE CASCADE
                    );
                """))
                
                # Create index on patient_id for better query performance
                db.session.execute(text("""
                    CREATE INDEX idx_birth_record_patient_id 
                    ON birth_record (patient_id);
                """))
                
                # Create index on date_of_birth for date-based queries
                db.session.execute(text("""
                    CREATE INDEX idx_birth_record_date_of_birth 
                    ON birth_record (date_of_birth);
                """))
                
                db.session.commit()
                print("✅ Birth records table created successfully!")
            else:
                print("ℹ️  Birth records table already exists!")
                
            print("📋 Table structure:")
            print("   - id (SERIAL PRIMARY KEY)")
            print("   - patient_id (INTEGER, FOREIGN KEY to user.id)")
            print("   - baby_gender (VARCHAR(10) - Male, Female, Other)")
            print("   - date_of_birth (DATE)")
            print("   - birth_type (VARCHAR(50) - Vaginal, Cesarean, etc.)")
            print("   - birth_location (VARCHAR(200))")
            print("   - notes (TEXT)")
            print("   - created_at (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
            print("🔗 Foreign key constraint: patient_id → user.id (CASCADE DELETE)")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error creating birth records table: {str(e)}")
            raise

if __name__ == "__main__":
    create_birth_records_table() 