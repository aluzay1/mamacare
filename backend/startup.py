#!/usr/bin/env python3
"""
Startup script for Render deployment
This script will be run before the main application starts
"""

import os
import sys
import time

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def run_startup_checks():
    """Run all startup checks and initialization"""
    print("🚀 MamaCare Startup Script")
    print("=" * 50)
    
    # Check environment variables
    print("🔍 Checking environment variables...")
    required_vars = ['DATABASE_URL']
    for var in required_vars:
        if os.environ.get(var):
            print(f"✅ {var}: Set")
        else:
            print(f"❌ {var}: Not set")
    
    # Wait for database to be ready
    print("\n⏳ Waiting for database to be ready...")
    time.sleep(5)  # Give database time to start
    
    try:
        # Import app components
        from app import app, db
        from create_default_admin import create_default_admin
        
        with app.app_context():
            # Create database tables
            print("🔧 Creating database tables...")
            db.create_all()
            print("✅ Database tables created")
            
            # Create default admin
            print("\n👤 Creating default admin...")
            create_default_admin()
            
            print("\n🎉 Startup completed successfully!")
            return True
            
    except Exception as e:
        print(f"❌ Startup failed: {e}")
        return False

if __name__ == "__main__":
    success = run_startup_checks()
    if not success:
        sys.exit(1) 