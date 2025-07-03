#!/usr/bin/env python3
"""
Manual migration script to create admin table and migrate existing admin users
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Admin, User
from werkzeug.security import generate_password_hash
from datetime import datetime

def create_admin_table():
    """Create the admin table"""
    print("🔧 Creating admin table...")
    
    with app.app_context():
        try:
            # Create all tables (this will create the admin table)
            db.create_all()
            print("✅ Admin table created successfully")
            return True
        except Exception as e:
            print(f"❌ Error creating admin table: {e}")
            return False

def migrate_existing_admins():
    """Migrate existing admin users from user table to admin table"""
    print("\n🔄 Migrating existing admin users...")
    
    with app.app_context():
        try:
            # Find all admin users in the user table
            admin_users = User.query.filter_by(role='admin').all()
            
            if not admin_users:
                print("📊 No existing admin users found to migrate")
                return True
            
            print(f"📊 Found {len(admin_users)} admin users to migrate")
            
            migrated_count = 0
            for user in admin_users:
                # Check if admin already exists in admin table
                existing_admin = Admin.query.filter_by(email=user.email).first()
                if existing_admin:
                    print(f"⚠️  Admin with email {user.email} already exists in admin table")
                    continue
                
                # Create new admin record
                new_admin = Admin(
                    email=user.email,
                    password=user.password,  # Keep the same hashed password
                    name=user.name,
                    phone=user.phone,
                    address=user.address,
                    is_verified=user.is_verified,
                    created_at=user.created_at
                )
                
                db.session.add(new_admin)
                migrated_count += 1
                print(f"✅ Migrated admin: {user.email}")
            
            # Commit the changes
            db.session.commit()
            print(f"✅ Successfully migrated {migrated_count} admin users")
            
            return True
            
        except Exception as e:
            print(f"❌ Error migrating admin users: {e}")
            db.session.rollback()
            return False

def remove_admin_users_from_user_table():
    """Remove admin users from the user table after migration"""
    print("\n🗑️  Removing admin users from user table...")
    
    with app.app_context():
        try:
            # Count admin users before deletion
            admin_count = User.query.filter_by(role='admin').count()
            
            if admin_count == 0:
                print("📊 No admin users found in user table to remove")
                return True
            
            # Delete admin users from user table
            User.query.filter_by(role='admin').delete()
            db.session.commit()
            
            print(f"✅ Removed {admin_count} admin users from user table")
            return True
            
        except Exception as e:
            print(f"❌ Error removing admin users: {e}")
            db.session.rollback()
            return False

def create_default_admin():
    """Create a default admin user if no admins exist"""
    print("\n👤 Creating default admin user...")
    
    with app.app_context():
        try:
            # Check if any admins exist
            admin_count = Admin.query.count()
            
            if admin_count > 0:
                print(f"📊 {admin_count} admin(s) already exist, skipping default admin creation")
                return True
            
            # Create default admin
            default_admin = Admin(
                email="admin@mamacare.com",
                password=generate_password_hash("admin123"),
                name="Default Admin",
                phone="+232123456789",
                is_verified=True,
                created_at=datetime.utcnow()
            )
            
            db.session.add(default_admin)
            db.session.commit()
            
            print("✅ Default admin created successfully")
            print("📧 Email: admin@mamacare.com")
            print("🔑 Password: admin123")
            print("⚠️  Please change the password after first login!")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating default admin: {e}")
            db.session.rollback()
            return False

def verify_migration():
    """Verify the migration was successful"""
    print("\n🔍 Verifying migration...")
    
    with app.app_context():
        try:
            # Check admin table
            admin_count = Admin.query.count()
            print(f"✅ Admin table has {admin_count} records")
            
            # Check user table for admin users
            user_admin_count = User.query.filter_by(role='admin').count()
            print(f"📊 User table has {user_admin_count} admin users (should be 0)")
            
            if user_admin_count == 0:
                print("✅ Migration verification successful!")
                return True
            else:
                print("⚠️  Warning: Some admin users still exist in user table")
                return False
                
        except Exception as e:
            print(f"❌ Error verifying migration: {e}")
            return False

def main():
    """Main migration function"""
    print("🚀 Starting Admin Table Migration")
    print("=" * 50)
    
    # Step 1: Create admin table
    if not create_admin_table():
        print("❌ Failed to create admin table")
        return
    
    # Step 2: Migrate existing admins
    if not migrate_existing_admins():
        print("❌ Failed to migrate existing admins")
        return
    
    # Step 3: Remove admin users from user table
    if not remove_admin_users_from_user_table():
        print("❌ Failed to remove admin users from user table")
        return
    
    # Step 4: Create default admin if needed
    if not create_default_admin():
        print("❌ Failed to create default admin")
        return
    
    # Step 5: Verify migration
    if not verify_migration():
        print("❌ Migration verification failed")
        return
    
    print("\n" + "=" * 50)
    print("✅ Admin Table Migration Completed Successfully!")
    print("\n📋 Migration Summary:")
    print("- Admin table created")
    print("- Existing admin users migrated")
    print("- Admin users removed from user table")
    print("- Default admin created (if needed)")
    print("- Migration verified")
    print("\n🎉 Your admin data is now properly separated!")

if __name__ == "__main__":
    main() 