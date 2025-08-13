#!/usr/bin/env python3
"""
Quick Railway Deployment Script for Django KPI Project
This script will guide you through the entire deployment process.
"""

import os
import subprocess
import sys
import webbrowser
from pathlib import Path

def print_header():
    print("🚂 Railway Quick Deploy for Django KPI")
    print("=" * 50)
    print("This script will help you deploy your KPI system to Railway")
    print()

def check_prerequisites():
    """Check if all prerequisites are met"""
    print("🔍 Checking prerequisites...")
    
    # Check if we're in the right directory
    if not Path('manage.py').exists():
        print("❌ Please run this script from the project root directory")
        return False
    
    # Check if required files exist
    required_files = ['requirements.txt', 'Procfile', 'runtime.txt']
    missing_files = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    print("✅ All prerequisites met!")
    return True

def generate_secret_key():
    """Generate a new Django secret key"""
    try:
        import secrets
        return secrets.token_urlsafe(50)
    except ImportError:
        import random
        import string
        return ''.join(random.choices(string.ascii_letters + string.digits, k=50))

def create_github_repo_instructions():
    """Provide instructions for creating GitHub repository"""
    print("\n📝 Step 1: Create GitHub Repository")
    print("-" * 40)
    print("1. Go to https://github.com/new")
    print("2. Repository name: mentiga-kpi-system")
    print("3. Make it Public")
    print("4. Don't initialize with README")
    print("5. Click 'Create repository'")
    
    input("\nPress Enter when you've created the repository...")
    
    repo_url = input("Enter your repository URL (e.g., https://github.com/username/mentiga-kpi-system): ").strip()
    return repo_url

def setup_git(repo_url):
    """Set up Git repository and push to GitHub"""
    print("\n🔧 Step 2: Setting up Git repository")
    print("-" * 40)
    
    try:
        # Initialize git
        subprocess.run(['git', 'init'], check=True)
        print("✅ Git repository initialized")
        
        # Add all files
        subprocess.run(['git', 'add', '.'], check=True)
        print("✅ Files added to git")
        
        # Commit
        subprocess.run(['git', 'commit', '-m', 'Initial commit - Django KPI system'], check=True)
        print("✅ Initial commit created")
        
        # Set main branch
        subprocess.run(['git', 'branch', '-M', 'main'], check=True)
        print("✅ Main branch set")
        
        # Add remote
        subprocess.run(['git', 'remote', 'add', 'origin', repo_url], check=True)
        print("✅ Remote origin added")
        
        # Push to GitHub
        subprocess.run(['git', 'push', '-u', 'origin', 'main'], check=True)
        print("✅ Code pushed to GitHub")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git operation failed: {e}")
        return False
    except FileNotFoundError:
        print("❌ Git not found. Please install Git first:")
        print("   Download from: https://git-scm.com/download/win")
        return False

def install_railway_cli():
    """Install Railway CLI"""
    print("\n📦 Step 3: Installing Railway CLI")
    print("-" * 40)
    
    try:
        # Check if npm is available
        subprocess.run(['npm', '--version'], check=True, capture_output=True)
        
        # Install Railway CLI
        subprocess.run(['npm', 'install', '-g', '@railway/cli'], check=True)
        print("✅ Railway CLI installed successfully")
        return True
        
    except subprocess.CalledProcessError:
        print("❌ Failed to install Railway CLI")
        print("💡 Please install Node.js first from https://nodejs.org/")
        return False
    except FileNotFoundError:
        print("❌ npm not found. Please install Node.js first:")
        print("   Download from: https://nodejs.org/")
        return False

def deploy_to_railway():
    """Deploy to Railway"""
    print("\n🚀 Step 4: Deploying to Railway")
    print("-" * 40)
    
    try:
        # Login to Railway
        print("🔐 Logging into Railway...")
        subprocess.run(['railway', 'login'], check=True)
        print("✅ Logged into Railway")
        
        # Initialize Railway project
        print("🏗️ Initializing Railway project...")
        subprocess.run(['railway', 'init'], check=True)
        print("✅ Railway project initialized")
        
        # Set environment variables
        print("🔧 Setting environment variables...")
        secret_key = generate_secret_key()
        
        env_vars = {
            'SECRET_KEY': secret_key,
            'DEBUG': 'False',
            'ALLOWED_HOSTS': 'localhost,127.0.0.1'
        }
        
        for key, value in env_vars.items():
            subprocess.run(['railway', 'variables', 'set', f'{key}={value}'], check=True)
            print(f"✅ Set {key}")
        
        # Deploy
        print("🚀 Deploying application...")
        subprocess.run(['railway', 'up'], check=True)
        print("✅ Application deployed successfully!")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Railway operation failed: {e}")
        return False
    except FileNotFoundError:
        print("❌ Railway CLI not found. Please install it first.")
        return False

def show_next_steps():
    """Show next steps after deployment"""
    print("\n🎉 Deployment Complete!")
    print("=" * 50)
    print("Your Django KPI system has been deployed to Railway!")
    print()
    print("📋 Next Steps:")
    print("1. Go to Railway dashboard: https://railway.app/dashboard")
    print("2. Click on your project")
    print("3. Go to 'Deployments' tab")
    print("4. Click on the latest deployment")
    print("5. Go to 'Logs' tab")
    print("6. Run these commands:")
    print("   python manage.py migrate")
    print("   python manage.py collectstatic --noinput")
    print("   python manage.py createsuperuser")
    print()
    print("🌐 Your application will be available at the URL shown in Railway dashboard")
    print("🔧 Admin panel: your-url.railway.app/admin/")
    print()
    print("📚 For more help, check: RAILWAY_DEPLOYMENT.md")

def main():
    print_header()
    
    if not check_prerequisites():
        sys.exit(1)
    
    print("🚀 Starting Railway deployment process...")
    print()
    
    # Step 1: Create GitHub repository
    repo_url = create_github_repo_instructions()
    
    # Step 2: Set up Git
    if not setup_git(repo_url):
        print("\n❌ Git setup failed. Please try again.")
        sys.exit(1)
    
    # Step 3: Install Railway CLI
    if not install_railway_cli():
        print("\n❌ Railway CLI installation failed. Please install Node.js and try again.")
        sys.exit(1)
    
    # Step 4: Deploy to Railway
    if not deploy_to_railway():
        print("\n❌ Railway deployment failed. Please check the error messages above.")
        sys.exit(1)
    
    # Show next steps
    show_next_steps()

if __name__ == "__main__":
    main()
