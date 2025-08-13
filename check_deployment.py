#!/usr/bin/env python3
"""
Deployment Status Checker for Django KPI Project
"""

import subprocess
import sys
import time
from pathlib import Path

def check_railway_status():
    """Check Railway deployment status"""
    try:
        result = subprocess.run(['railway', 'status'], capture_output=True, text=True, check=True)
        print("🚂 Railway Status:")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to get Railway status: {e}")
        return False
    except FileNotFoundError:
        print("❌ Railway CLI not found. Please install it first:")
        print("   npm install -g @railway/cli")
        return False

def check_railway_logs():
    """Check Railway deployment logs"""
    try:
        result = subprocess.run(['railway', 'logs'], capture_output=True, text=True, check=True)
        print("📋 Recent Logs:")
        print(result.stdout)
        return True
    except subprocess.CmdProcessError as e:
        print(f"❌ Failed to get Railway logs: {e}")
        return False

def test_local_app():
    """Test the local application"""
    print("🔍 Testing local application...")
    
    try:
        # Test Django settings
        result = subprocess.run(['python', 'manage.py', 'check'], capture_output=True, text=True, check=True)
        print("✅ Django settings check passed")
        
        # Test migrations
        result = subprocess.run(['python', 'manage.py', 'showmigrations'], capture_output=True, text=True, check=True)
        print("✅ Migrations check passed")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Local app test failed: {e.stderr}")
        return False

def generate_secret_key():
    """Generate a new Django secret key"""
    try:
        result = subprocess.run(['python', '-c', 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'], 
                              capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        import secrets
        return secrets.token_urlsafe(50)

def main():
    print("🔍 Django KPI Deployment Status Checker")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path('manage.py').exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    print("\n📋 Available checks:")
    print("1. Test local application")
    print("2. Check Railway status")
    print("3. Check Railway logs")
    print("4. Generate secret key")
    print("5. Run all checks")
    print("6. Exit")
    
    while True:
        choice = input("\nSelect an action (1-6): ").strip()
        
        if choice == '1':
            test_local_app()
        elif choice == '2':
            check_railway_status()
        elif choice == '3':
            check_railway_logs()
        elif choice == '4':
            secret_key = generate_secret_key()
            print(f"🔑 New secret key: {secret_key}")
            print("💡 Add this to your Railway environment variables as SECRET_KEY")
        elif choice == '5':
            print("🔄 Running all checks...")
            test_local_app()
            print()
            check_railway_status()
            print()
            check_railway_logs()
        elif choice == '6':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please select 1-6.")

if __name__ == "__main__":
    main()
