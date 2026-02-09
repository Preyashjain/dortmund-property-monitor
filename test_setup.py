#!/usr/bin/env python3
"""
Test script to verify the Dortmund Property Monitor setup
"""

import sys
import io

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def test_imports():
    """Test that all required modules are available"""
    print("Testing imports...")
    try:
        import requests
        print("  [OK] requests")
    except ImportError:
        print("  [FAIL] requests - run: pip install requests")
        return False
    
    try:
        from bs4 import BeautifulSoup
        print("  [OK] beautifulsoup4")
    except ImportError:
        print("  [FAIL] beautifulsoup4 - run: pip install beautifulsoup4")
        return False
    
    return True

def test_config():
    """Test that config.py exists and has required fields"""
    print("\nTesting configuration...")
    try:
        from config import EMAIL_CONFIG
        required_fields = ['smtp_server', 'smtp_port', 'from_email', 'password', 'to_email']
        for field in required_fields:
            if field in EMAIL_CONFIG:
                if field == 'password':
                    print(f"  [OK] {field}: {'*' * len(EMAIL_CONFIG[field])}")
                else:
                    print(f"  [OK] {field}: {EMAIL_CONFIG[field]}")
            else:
                print(f"  [FAIL] Missing: {field}")
                return False
        return True
    except ImportError:
        print("  [FAIL] config.py not found - please create it from config_template.py")
        return False

def test_website_access():
    """Test that we can access the STWDO website"""
    print("\nTesting website access...")
    import requests
    url = "https://www.stwdo.de/wohnen/aktuelle-wohnangebote"
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        print(f"  [OK] Website accessible (Status: {response.status_code})")
        print(f"  [OK] Response size: {len(response.content)} bytes")
        return True
    except requests.RequestException as e:
        print(f"  [FAIL] Cannot access website: {e}")
        return False

def test_email_connection():
    """Test SMTP connection (without sending)"""
    print("\nTesting email connection...")
    import smtplib
    try:
        from config import EMAIL_CONFIG
        server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'], timeout=10)
        server.starttls()
        server.login(EMAIL_CONFIG['from_email'], EMAIL_CONFIG['password'])
        server.quit()
        print("  [OK] SMTP connection successful")
        print("  [OK] Login successful")
        return True
    except smtplib.SMTPAuthenticationError:
        print("  [FAIL] Authentication failed - check email/password")
        print("     For Gmail, use an App Password, not your regular password")
        return False
    except Exception as e:
        print(f"  [FAIL] SMTP error: {e}")
        return False

def test_scraping():
    """Test the property scraping functionality"""
    print("\nTesting property scraping...")
    try:
        from dortmund_property_monitor import DortmundPropertyMonitor
        from config import EMAIL_CONFIG
        
        monitor = DortmundPropertyMonitor(EMAIL_CONFIG)
        properties = monitor.fetch_properties()
        
        print(f"  [OK] Scraper initialized")
        print(f"  [OK] Found {len(properties)} properties")
        
        if properties:
            print(f"\n  Sample property:")
            prop = properties[0]
            print(f"    Title: {prop.get('title', 'N/A')[:50]}...")
            print(f"    Link: {prop.get('link', 'N/A')[:60]}...")
        
        return True
    except Exception as e:
        print(f"  [FAIL] Scraping error: {e}")
        return False

def main():
    print("=" * 60)
    print("DORTMUND PROPERTY MONITOR - SETUP TEST")
    print("=" * 60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Configuration", test_config()))
    results.append(("Website Access", test_website_access()))
    results.append(("Email Connection", test_email_connection()))
    results.append(("Property Scraping", test_scraping()))
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"  {name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\nAll tests passed! You can now run:")
        print("   python dortmund_property_monitor.py")
        return 0
    else:
        print("\nSome tests failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
