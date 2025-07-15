#!/usr/bin/env python3
"""
Script to manually verify an admin account
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Admin, User
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

def verify_admin_account(email, password):
    """Verify an admin account by email and password"""
    print(f"🔍 Looking for admin account: {email}")
    
    with app.app_context():
        try:
            # First check Admin table
            admin = Admin.query.filter_by(email=email).first()
            
            if admin:
                print(f"✅ Found admin in Admin table: {admin.email}")
                print(f"📊 Current verification status: {admin.is_verified}")
                
                # Verify password
                if check_password_hash(admin.password, password):
                    print("✅ Password is correct")
                    
                    # Set verification to True
                    admin.is_verified = True
                    db.session.commit()
                    print("✅ Admin account verified successfully!")
                    return True
                else:
                    print("❌ Password is incorrect")
                    return False
            else:
                print("⚠️  Admin not found in Admin table")
                
                # Check User table
                user = User.query.filter_by(email=email, role='admin').first()
                if user:
                    print(f"✅ Found admin in User table: {user.email}")
                    print(f"📊 Current verification status: {user.is_verified}")
                    
                    # Verify password
                    if check_password_hash(user.password, password):
                        print("✅ Password is correct")
                        
                        # Set verification to True
                        user.is_verified = True
                        db.session.commit()
                        print("✅ Admin account verified successfully!")
                        return True
                    else:
                        print("❌ Password is incorrect")
                        return False
                else:
                    print("❌ Admin account not found in either table")
                    return False
                    
        except Exception as e:
            print(f"❌ Error verifying admin: {e}")
            db.session.rollback()
            return False

def create_admin_if_not_exists(email, password, name="Admin User"):
    """Create admin account if it doesn't exist"""
    print(f"🔧 Creating admin account: {email}")
    
    with app.app_context():
        try:
            # Check if admin exists in Admin table
            existing_admin = Admin.query.filter_by(email=email).first()
            if existing_admin:
                print("✅ Admin already exists in Admin table")
                return existing_admin
            
            # Check if admin exists in User table
            existing_user = User.query.filter_by(email=email, role='admin').first()
            if existing_user:
                print("✅ Admin already exists in User table")
                return existing_user
            
            # Create new admin in Admin table
            admin = Admin(
                email=email,
                password=generate_password_hash(password),
                name=name,
                phone='+23212345678',
                is_verified=True,  # Auto-verify
                created_at=datetime.utcnow()
            )
            
            db.session.add(admin)
            db.session.commit()
            
            print("✅ Admin account created and verified successfully!")
            return admin
            
        except Exception as e:
            print(f"❌ Error creating admin: {e}")
            db.session.rollback()
            return None

def list_all_admins():
    """List all admin accounts"""
    print("\n📊 Listing all admin accounts:")
    
    with app.app_context():
        try:
            # Check Admin table
            admin_count = Admin.query.count()
            print(f"📋 Admin table has {admin_count} records:")
            
            admins = Admin.query.all()
            for admin in admins:
                print(f"  👤 {admin.email} (Verified: {admin.is_verified})")
            
            # Check User table for admin users
            user_admin_count = User.query.filter_by(role='admin').count()
            print(f"\n📋 User table has {user_admin_count} admin users:")
            
            user_admins = User.query.filter_by(role='admin').all()
            for user in user_admins:
                print(f"  👤 {user.email} (Verified: {user.is_verified})")
                
        except Exception as e:
            print(f"❌ Error listing admins: {e}")

def main():
    """Main function"""
    email = "alusinekuyateh6@gmail.com"
    password = "Admin123"
    
    print("🚀 Admin Account Verification Tool")
    print("=" * 50)
    
    # Step 1: List existing admins
    list_all_admins()
    
    # Step 2: Try to verify existing account
    print(f"\n🔐 Attempting to verify account: {email}")
    if verify_admin_account(email, password):
        print("✅ Verification successful!")
    else:
        print("⚠️  Account not found or password incorrect")
        print("🔧 Creating new admin account...")
        create_admin_if_not_exists(email, password, "Alusine Kuyateh")
    
    # Step 3: List admins again to confirm
    print("\n" + "=" * 50)
    list_all_admins()
    
    print("\n🎉 Admin verification process completed!")
    print(f"📧 You can now login with: {email}")
    print(f"🔑 Password: {password}")

if __name__ == "__main__":
    main() 