#!/usr/bin/env python3
"""
Railway Deployment Helper for Django KPI Project
"""

import os
import subprocess
import sys
from pathlib import Path

def check_railway_cli():
    """Check if Railway CLI is installed"""
    try:
        result = subprocess.run(['railway', '--version'], capture_output=True, text=True)
        return True
    except FileNotFoundError:
        return False

def install_railway_cli():
    """Install Railway CLI"""
    print("📦 Installing Railway CLI...")
    try:
        subprocess.run(['npm', 'install', '-g', '@railway/cli'], check=True)
        print("✅ Railway CLI installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install Railway CLI")
        print("💡 Please install Node.js first from https://nodejs.org/")
        return False

def generate_secret_key():
    """Generate a new Django secret key"""
    try:
        import django
        from django.core.management.utils import get_random_secret_key
        return get_random_secret_key()
    except ImportError:
        # Fallback if Django is not installed
        import secrets
        return secrets.token_urlsafe(50)

def create_railway_project():
    """Create a new Railway project"""
    print("🚀 Creating Railway project...")
    try:
        subprocess.run(['railway', 'init'], check=True)
        print("✅ Railway project created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create Railway project: {e}")
        return False

def set_environment_variables():
    """Set environment variables for Railway"""
    print("🔧 Setting environment variables...")
    
    secret_key = generate_secret_key()
    
    # Set environment variables
    env_vars = {
        'SECRET_KEY': secret_key,
        'DEBUG': 'False',
        'ALLOWED_HOSTS': 'localhost,127.0.0.1'
    }
    
    for key, value in env_vars.items():
        try:
            subprocess.run(['railway', 'variables', 'set', f'{key}={value}'], check=True)
            print(f"✅ Set {key}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to set {key}")
    
    return True

def deploy_to_railway():
    """Deploy the application to Railway"""
    print("🚀 Deploying to Railway...")
    try:
        subprocess.run(['railway', 'up'], check=True)
        print("✅ Deployment successful!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Deployment failed: {e}")
        return False

def show_deployment_url():
    """Show the deployment URL"""
    try:
        result = subprocess.run(['railway', 'status'], capture_output=True, text=True, check=True)
        print("🌐 Your deployment URL:")
        print(result.stdout)
    except subprocess.CalledProcessError:
        print("❌ Could not get deployment status")

def main():
    print("🚂 Railway Deployment Helper")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path('manage.py').exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Check if Railway CLI is installed
    if not check_railway_cli():
        print("❌ Railway CLI not found")
        choice = input("Would you like to install Railway CLI? (y/n): ").strip().lower()
        if choice == 'y':
            if not install_railway_cli():
                sys.exit(1)
        else:
            print("💡 Please install Railway CLI manually:")
            print("   npm install -g @railway/cli")
            sys.exit(1)
    
    # Menu
    while True:
        print("\n📋 Available actions:")
        print("1. Generate new secret key")
        print("2. Create Railway project")
        print("3. Set environment variables")
        print("4. Deploy to Railway")
        print("5. Show deployment status")
        print("6. Run complete deployment")
        print("7. Exit")
        
        choice = input("\nSelect an action (1-7): ").strip()
        
        if choice == '1':
            secret_key = generate_secret_key()
            print(f"🔑 New secret key: {secret_key}")
            print("💡 Add this to your Railway environment variables as SECRET_KEY")
        elif choice == '2':
            create_railway_project()
        elif choice == '3':
            set_environment_variables()
        elif choice == '4':
            deploy_to_railway()
        elif choice == '5':
            show_deployment_url()
        elif choice == '6':
            print("🔄 Running complete deployment...")
            if create_railway_project() and set_environment_variables() and deploy_to_railway():
                print("✅ Complete deployment successful!")
                show_deployment_url()
        elif choice == '7':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please select 1-7.")

if __name__ == "__main__":
    main()
