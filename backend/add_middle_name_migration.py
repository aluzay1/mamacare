#!/usr/bin/env python3
"""
Migration script to add middle_name field to User table
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from sqlalchemy import text

def add_middle_name_column():
    """Add middle_name column to User table if it doesn't exist"""
    with app.app_context():
        try:
            # Check if column already exists
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'user' AND column_name = 'middle_name'
            """))
            
            if not result.fetchone():
                # Add the column
                db.session.execute(text("ALTER TABLE \"user\" ADD COLUMN middle_name VARCHAR(100)"))
                db.session.commit()
                print("✅ Successfully added middle_name column to User table")
            else:
                print("ℹ️  middle_name column already exists in User table")
                
        except Exception as e:
            print(f"❌ Error adding middle_name column: {str(e)}")
            db.session.rollback()
            raise

if __name__ == "__main__":
    print("🔄 Starting migration to add middle_name column...")
    add_middle_name_column()
    print("✅ Migration completed successfully!") 