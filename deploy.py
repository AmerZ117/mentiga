#!/usr/bin/env python3
"""
Deployment helper script for Django KPI project
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return None

def check_requirements():
    """Check if all required files exist"""
    required_files = [
        'requirements.txt',
        'Procfile',
        'runtime.txt',
        'config/settings.py',
        'manage.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required files found")
    return True

def collect_static():
    """Collect static files"""
    return run_command("python manage.py collectstatic --noinput", "Collecting static files")

def run_migrations():
    """Run database migrations"""
    return run_command("python manage.py migrate", "Running database migrations")

def create_superuser():
    """Create a superuser interactively"""
    print("👤 Creating superuser...")
    try:
        subprocess.run("python manage.py createsuperuser", shell=True, check=True)
        print("✅ Superuser created successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to create superuser")
        return False

def generate_secret_key():
    """Generate a new Django secret key"""
    from django.core.management.utils import get_random_secret_key
    return get_random_secret_key()

def main():
    print("🚀 Django KPI Deployment Helper")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path('manage.py').exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Menu
    while True:
        print("\n📋 Available actions:")
        print("1. Collect static files")
        print("2. Run database migrations")
        print("3. Create superuser")
        print("4. Generate new secret key")
        print("5. Run all deployment tasks")
        print("6. Exit")
        
        choice = input("\nSelect an action (1-6): ").strip()
        
        if choice == '1':
            collect_static()
        elif choice == '2':
            run_migrations()
        elif choice == '3':
            create_superuser()
        elif choice == '4':
            secret_key = generate_secret_key()
            print(f"🔑 New secret key: {secret_key}")
            print("💡 Add this to your environment variables as SECRET_KEY")
        elif choice == '5':
            print("🔄 Running all deployment tasks...")
            if collect_static() and run_migrations():
                print("✅ All deployment tasks completed successfully!")
                create_superuser()
        elif choice == '6':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please select 1-6.")

if __name__ == "__main__":
    main()
