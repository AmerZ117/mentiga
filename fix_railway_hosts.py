#!/usr/bin/env python3
"""
Fix Railway Hosts Configuration
This script helps set the correct ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS for Railway deployment
"""

import subprocess
import sys

def set_railway_variables():
    """Set the correct environment variables for Railway"""
    print("🔧 Setting Railway environment variables...")
    
    # Variables to set
    variables = {
        'ALLOWED_HOSTS': 'localhost,127.0.0.1,mentigaeva.up.railway.app',
        'CSRF_TRUSTED_ORIGINS': 'https://mentigaeva.up.railway.app',
        'DEBUG': 'False'
    }
    
    for key, value in variables.items():
        try:
            print(f"Setting {key}...")
            subprocess.run(['railway', 'variables', 'set', f'{key}={value}'], check=True)
            print(f"✅ {key} set successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to set {key}: {e}")
            return False
        except FileNotFoundError:
            print("❌ Railway CLI not found. Please install it first:")
            print("   npm install -g @railway/cli")
            return False
    
    print("\n✅ All environment variables set successfully!")
    print("\n🔄 Now redeploy your application:")
    print("   railway up")
    return True

def main():
    print("🚂 Railway Host Configuration Fix")
    print("=" * 40)
    
    if set_railway_variables():
        print("\n🎉 Configuration updated successfully!")
        print("Your application should now work at: https://mentigaeva.up.railway.app")
    else:
        print("\n❌ Failed to update configuration")
        sys.exit(1)

if __name__ == "__main__":
    main()
