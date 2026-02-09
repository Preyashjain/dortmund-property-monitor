#!/usr/bin/env python3
"""
Quick Start Version - Uses environment variables for security
Set your email credentials as environment variables before running
"""

import os
import sys

# Check if environment variables are set
required_vars = ['EMAIL_ADDRESS', 'EMAIL_PASSWORD']
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    print("⚠️  Missing required environment variables:")
    for var in missing_vars:
        print(f"   - {var}")
    print("\nSet them before running:")
    print("  export EMAIL_ADDRESS='your_email@gmail.com'")
    print("  export EMAIL_PASSWORD='your_app_password'")
    print("\nOr run with:")
    print("  EMAIL_ADDRESS='your@email.com' EMAIL_PASSWORD='password' python quick_start.py")
    sys.exit(1)

# Import the main monitor
from dortmund_property_monitor import DortmundPropertyMonitor

def main():
    email_config = {
        'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
        'smtp_port': int(os.getenv('SMTP_PORT', '587')),
        'from_email': os.getenv('EMAIL_ADDRESS'),
        'password': os.getenv('EMAIL_PASSWORD'),
        'to_email': os.getenv('TO_EMAIL', os.getenv('EMAIL_ADDRESS'))
    }
    
    monitor = DortmundPropertyMonitor(email_config)
    
    # Get check interval from environment or use 5 minutes default
    interval = int(os.getenv('CHECK_INTERVAL_MINUTES', '5'))
    
    monitor.run_monitor(interval_minutes=interval)

if __name__ == "__main__":
    main()
