#!/usr/bin/env python3
"""
Script to create a default verified admin account
This will be called during application startup
"""

import os
from app import app, db, Admin, User
from werkzeug.security import generate_password_hash
from datetime import datetime

def create_default_admin():
    """Create a default admin account if none exists"""
    
    # Default admin credentials
    DEFAULT_ADMIN_EMAIL = "alusinekuyateh6@gmail.com"
    DEFAULT_ADMIN_PASSWORD = "Admin123"
    DEFAULT_ADMIN_NAME = "Alusine Kuyateh"
    DEFAULT_ADMIN_PHONE = "+23212345678"
    
    # Allow override via environment variables
    admin_email = os.environ.get('DEFAULT_ADMIN_EMAIL', DEFAULT_ADMIN_EMAIL)
    admin_password = os.environ.get('DEFAULT_ADMIN_PASSWORD', DEFAULT_ADMIN_PASSWORD)
    admin_name = os.environ.get('DEFAULT_ADMIN_NAME', DEFAULT_ADMIN_NAME)
    admin_phone = os.environ.get('DEFAULT_ADMIN_PHONE', DEFAULT_ADMIN_PHONE)
    
    with app.app_context():
        try:
            # Check if any verified admin exists
            verified_admin_count = Admin.query.filter_by(is_verified=True).count()
            
            if verified_admin_count > 0:
                print(f"✅ {verified_admin_count} verified admin(s) already exist, skipping default admin creation")
                return True
            
            # Check if the specific admin already exists
            existing_admin = Admin.query.filter_by(email=admin_email).first()
            if existing_admin:
                print(f"✅ Admin {admin_email} already exists")
                # Verify the existing admin
                if not existing_admin.is_verified:
                    existing_admin.is_verified = True
                    db.session.commit()
                    print(f"✅ Admin {admin_email} verified successfully")
                return True
            
            # Create new default admin
            new_admin = Admin(
                email=admin_email,
                password=generate_password_hash(admin_password),
                name=admin_name,
                phone=admin_phone,
                is_verified=True,  # Auto-verify the default admin
                created_at=datetime.utcnow()
            )
            
            db.session.add(new_admin)
            db.session.commit()
            
            print("✅ Default admin created successfully!")
            print(f"📧 Email: {admin_email}")
            print(f"🔑 Password: {admin_password}")
            print(f"👤 Name: {admin_name}")
            print("✅ Status: Verified")
            print("⚠️  Please change the password after first login!")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating default admin: {e}")
            db.session.rollback()
            return False

def list_all_admins():
    """List all admin accounts for verification"""
    with app.app_context():
        try:
            # Check Admin table
            admin_count = Admin.query.count()
            print(f"\n📊 Admin table has {admin_count} records:")
            
            admins = Admin.query.all()
            for admin in admins:
                print(f"  👤 {admin.email} (Verified: {admin.is_verified})")
            
            # Check User table for admin users
            user_admin_count = User.query.filter_by(role='admin').count()
            print(f"\n📊 User table has {user_admin_count} admin users:")
            
            user_admins = User.query.filter_by(role='admin').all()
            for user in user_admins:
                print(f"  👤 {user.email} (Verified: {user.is_verified})")
                
        except Exception as e:
            print(f"❌ Error listing admins: {e}")

if __name__ == "__main__":
    print("🚀 Creating Default Admin Account")
    print("=" * 50)
    
    # Create default admin
    success = create_default_admin()
    
    if success:
        # List all admins to confirm
        list_all_admins()
        print("\n🎉 Default admin setup completed!")
    else:
        print("\n❌ Failed to create default admin") 