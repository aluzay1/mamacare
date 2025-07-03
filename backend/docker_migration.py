#!/usr/bin/env python3
"""
Migration script to be run inside Docker container
"""

import os
import sys
from sqlalchemy import create_engine, text

def run_migration():
    """Run the migration to add doctor columns"""
    
    # Get database URL from environment (Docker setup)
    database_url = os.getenv('DATABASE_URL', 'postgresql://postgres:password@db:5432/mamacare')
    
    print(f"Connecting to database: {database_url}")
    
    try:
        # Create engine
        engine = create_engine(database_url)
        
        # Test connection
        with engine.begin() as conn:
            print("✅ Database connection successful")
            
            # Check existing columns
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'referral_feedback'
                ORDER BY column_name
            """))
            
            existing_columns = [row[0] for row in result]
            print(f"Existing columns: {existing_columns}")
            
            # Define columns to add
            columns_to_add = [
                ('doctor_name', 'VARCHAR(200)'),
                ('doctor_phone', 'VARCHAR(20)'),
                ('doctor_affiliation', 'VARCHAR(200)')
            ]
            
            # Check which columns are missing
            missing_columns = []
            for col_name, col_type in columns_to_add:
                if col_name not in existing_columns:
                    missing_columns.append((col_name, col_type))
                    print(f"Column '{col_name}' is missing")
                else:
                    print(f"Column '{col_name}' already exists")
            
            # Add missing columns
            if missing_columns:
                print(f"\nAdding {len(missing_columns)} missing columns...")
                for col_name, col_type in missing_columns:
                    try:
                        sql = f"ALTER TABLE referral_feedback ADD COLUMN {col_name} {col_type}"
                        print(f"Executing: {sql}")
                        conn.execute(text(sql))
                        print(f"✅ Successfully added column '{col_name}'")
                    except Exception as e:
                        print(f"❌ Error adding column '{col_name}': {e}")
                        continue
                
                print("✅ All changes committed successfully (using engine.begin())")
            else:
                print("✅ All required columns already exist")
            
            # Verify final state
            print("\nVerifying final state...")
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'referral_feedback'
                ORDER BY column_name
            """))
            
            final_columns = [row[0] for row in result]
            print(f"Final columns: {final_columns}")
            
            required_columns = ['doctor_name', 'doctor_phone', 'doctor_affiliation']
            all_present = all(col in final_columns for col in required_columns)
            
            if all_present:
                print("✅ All required doctor columns are present!")
                return True
            else:
                print("❌ Some required columns are still missing")
                return False
                
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("DOCKER MIGRATION SCRIPT")
    print("=" * 60)
    
    success = run_migration()
    
    if success:
        print("\n✅ Migration completed successfully!")
        print("You can now test the referral feedback form.")
    else:
        print("\n❌ Migration failed. Please check the error messages above.")
    
    print("=" * 60) 