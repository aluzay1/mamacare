#!/usr/bin/env python3
"""
Script to fix admin access issues by creating a proper admin account
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Admin, User
from werkzeug.security import generate_password_hash
from datetime import datetime

def create_default_admin():
    """Create a default admin in the Admin table"""
    print("🔧 Creating default admin in Admin table...")
    
    with app.app_context():
        try:
            # Check if admin already exists in Admin table
            existing_admin = Admin.query.filter_by(email='admin@mamacare.com').first()
            if existing_admin:
                print("✅ Admin already exists in Admin table")
                return existing_admin
            
            # Create new admin in Admin table
            admin = Admin(
                email='admin@mamacare.com',
                password=generate_password_hash('admin123'),
                name='Default Admin',
                phone='+23212345678',
                is_verified=True,  # Auto-verify the first admin
                created_at=datetime.utcnow()
            )
            
            db.session.add(admin)
            db.session.commit()
            
            print("✅ Default admin created successfully in Admin table")
            print("📧 Email: admin@mamacare.com")
            print("🔑 Password: admin123")
            print("✅ Status: Verified")
            
            return admin
            
        except Exception as e:
            print(f"❌ Error creating admin: {e}")
            db.session.rollback()
            return None

def verify_existing_admin():
    """Verify an existing admin account"""
    print("\n🔍 Checking for existing admin accounts...")
    
    with app.app_context():
        try:
            # Check Admin table
            admin_count = Admin.query.count()
            print(f"📊 Admin table has {admin_count} records")
            
            # Check User table for admin users
            user_admin_count = User.query.filter_by(role='admin').count()
            print(f"📊 User table has {user_admin_count} admin users")
            
            if admin_count == 0:
                print("⚠️  No admins found in Admin table")
                return False
            else:
                admins = Admin.query.all()
                for admin in admins:
                    print(f"👤 Admin: {admin.email} (Verified: {admin.is_verified})")
                return True
                
        except Exception as e:
            print(f"❌ Error checking admins: {e}")
            return False

def auto_verify_first_admin():
    """Auto-verify the first admin if no verified admins exist"""
    print("\n🔐 Auto-verifying first admin...")
    
    with app.app_context():
        try:
            # Check if any verified admins exist
            verified_admins = Admin.query.filter_by(is_verified=True).count()
            
            if verified_admins == 0:
                # Get the first admin and verify them
                first_admin = Admin.query.first()
                if first_admin:
                    first_admin.is_verified = True
                    db.session.commit()
                    print(f"✅ Auto-verified admin: {first_admin.email}")
                    return True
                else:
                    print("⚠️  No admin accounts found to verify")
                    return False
            else:
                print(f"✅ {verified_admins} verified admin(s) already exist")
                return True
                
        except Exception as e:
            print(f"❌ Error auto-verifying admin: {e}")
            db.session.rollback()
            return False

def main():
    """Main function to fix admin access"""
    print("🚀 Fixing Admin Access Issues")
    print("=" * 50)
    
    # Step 1: Create default admin if needed
    admin = create_default_admin()
    if not admin:
        print("❌ Failed to create default admin")
        return
    
    # Step 2: Auto-verify first admin
    if not auto_verify_first_admin():
        print("❌ Failed to auto-verify admin")
        return
    
    # Step 3: Verify the setup
    if not verify_existing_admin():
        print("❌ Admin verification failed")
        return
    
    print("\n" + "=" * 50)
    print("✅ Admin Access Fixed Successfully!")
    print("\n📋 You can now login with:")
    print("📧 Email: admin@mamacare.com")
    print("🔑 Password: admin123")
    print("\n🎉 Try logging in to the admin dashboard now!")

if __name__ == "__main__":
    main() 