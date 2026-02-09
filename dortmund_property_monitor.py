#!/usr/bin/env python3
"""
Dortmund Property Alert System
Monitors STWDO website for new Dortmund properties and sends email alerts
"""

import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import json
import os
import sys
import io
from datetime import datetime

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

class DortmundPropertyMonitor:
    def __init__(self, email_config):
        self.url = "https://www.stwdo.de/wohnen/aktuelle-wohnangebote#residential-offer-list"
        self.email_config = email_config
        self.seen_properties = self.load_seen_properties()
        
    def load_seen_properties(self):
        """Load previously seen properties from file"""
        if os.path.exists('seen_properties.json'):
            with open('seen_properties.json', 'r') as f:
                return set(json.load(f))
        return set()
    
    def save_seen_properties(self):
        """Save seen properties to file"""
        with open('seen_properties.json', 'w') as f:
            json.dump(list(self.seen_properties), f)
    
    def fetch_properties(self):
        """Fetch and parse properties from the website"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(self.url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            properties = []
            
            # Find all property listings (adjust selectors based on actual HTML structure)
            property_items = soup.find_all('div', class_='property-item') or \
                           soup.find_all('article') or \
                           soup.find_all('div', class_='offer')
            
            for item in property_items:
                # Extract property details
                title = item.find('h2') or item.find('h3') or item.find('h4')
                location = item.find(string=lambda text: text and 'Dortmund' in text)
                
                if title:
                    title_text = title.get_text(strip=True)
                    
                    # Check if it's a Dortmund property
                    full_text = item.get_text()
                    if 'Dortmund' in full_text or 'dortmund' in full_text.lower():
                        # Extract additional details
                        details = {
                            'title': title_text,
                            'text': full_text[:500],  # First 500 chars
                            'link': self.extract_link(item),
                            'timestamp': datetime.now().isoformat()
                        }
                        
                        # Create unique ID for property
                        property_id = f"{title_text}_{details['link']}"
                        details['id'] = property_id
                        
                        properties.append(details)
            
            return properties
            
        except requests.RequestException as e:
            print(f"Error fetching properties: {e}")
            return []
    
    def extract_link(self, item):
        """Extract link from property item"""
        link = item.find('a', href=True)
        if link:
            href = link['href']
            if href.startswith('http'):
                return href
            else:
                return f"https://www.stwdo.de{href}"
        return self.url
    
    def send_email_alert(self, new_properties):
        """Send email alert for new properties"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"🏠 New Dortmund Property Alert - {len(new_properties)} found!"
            msg['From'] = self.email_config['from_email']
            msg['To'] = self.email_config['to_email']
            
            # Create email body
            html_body = self.create_email_html(new_properties)
            text_body = self.create_email_text(new_properties)
            
            msg.attach(MIMEText(text_body, 'plain'))
            msg.attach(MIMEText(html_body, 'html'))
            
            # Send email
            with smtplib.SMTP(self.email_config['smtp_server'], 
                            self.email_config['smtp_port']) as server:
                server.starttls()
                server.login(self.email_config['from_email'], 
                           self.email_config['password'])
                server.send_message(msg)
            
            print(f"✅ Email sent successfully for {len(new_properties)} properties")
            return True
            
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            return False
    
    def create_email_html(self, properties):
        """Create HTML email body"""
        html = """
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; }
                .property { 
                    border: 1px solid #ddd; 
                    padding: 15px; 
                    margin: 10px 0;
                    border-radius: 5px;
                    background-color: #f9f9f9;
                }
                .property h3 { color: #0066cc; margin-top: 0; }
                .property a { color: #0066cc; text-decoration: none; }
                .property a:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <h2>🏠 New Dortmund Properties Available!</h2>
            <p>Found {} new property listing(s) in Dortmund:</p>
        """.format(len(properties))
        
        for prop in properties:
            html += f"""
            <div class="property">
                <h3>{prop['title']}</h3>
                <p><strong>Found:</strong> {prop['timestamp']}</p>
                <p><a href="{prop['link']}" target="_blank">View Property Details →</a></p>
            </div>
            """
        
        html += """
            <hr>
            <p style="color: #666; font-size: 12px;">
                This is an automated alert from your Dortmund Property Monitor.
            </p>
        </body>
        </html>
        """
        return html
    
    def create_email_text(self, properties):
        """Create plain text email body"""
        text = f"NEW DORTMUND PROPERTIES ALERT\n"
        text += f"{'='*50}\n\n"
        text += f"Found {len(properties)} new property listing(s) in Dortmund:\n\n"
        
        for i, prop in enumerate(properties, 1):
            text += f"{i}. {prop['title']}\n"
            text += f"   Link: {prop['link']}\n"
            text += f"   Found: {prop['timestamp']}\n\n"
        
        text += f"{'='*50}\n"
        text += "This is an automated alert from your Dortmund Property Monitor.\n"
        return text
    
    def check_for_new_properties(self):
        """Main function to check for new properties and send alerts"""
        print(f"\n🔍 Checking for new properties... [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
        
        properties = self.fetch_properties()
        
        if not properties:
            print("   No properties found or error occurred")
            return
        
        # Filter new properties
        new_properties = []
        for prop in properties:
            if prop['id'] not in self.seen_properties:
                new_properties.append(prop)
                self.seen_properties.add(prop['id'])
        
        if new_properties:
            print(f"   🎉 Found {len(new_properties)} NEW Dortmund properties!")
            self.send_email_alert(new_properties)
            self.save_seen_properties()
        else:
            print(f"   No new properties (checked {len(properties)} total)")
    
    def run_monitor(self, interval_minutes=5):
        """Run the monitor continuously"""
        print("="*60)
        print("🏠 DORTMUND PROPERTY MONITOR STARTED")
        print("="*60)
        print(f"Monitoring: {self.url}")
        print(f"Check interval: {interval_minutes} minutes")
        print(f"Email alerts to: {self.email_config['to_email']}")
        print("="*60)
        
        while True:
            try:
                self.check_for_new_properties()
                sleep_seconds = interval_minutes * 60
                print(f"   ⏰ Next check in {interval_minutes} minutes...\n")
                time.sleep(sleep_seconds)
            except KeyboardInterrupt:
                print("\n\n👋 Monitor stopped by user")
                break
            except Exception as e:
                print(f"   ⚠️  Unexpected error: {e}")
                print("   Continuing in 1 minute...")
                time.sleep(60)


def main():
    # Try to import config, fall back to defaults
    try:
        from config import EMAIL_CONFIG
        email_config = EMAIL_CONFIG
        print("✅ Loaded email configuration from config.py")
    except ImportError:
        # Fallback configuration
        email_config = {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'from_email': 'your_email@gmail.com',
            'password': 'your_app_password',
            'to_email': 'your_email@gmail.com'
        }
        print("⚠️  Using default config - please create config.py")
    
    # Create and run monitor
    monitor = DortmundPropertyMonitor(email_config)
    monitor.run_monitor(interval_minutes=5)


if __name__ == "__main__":
    main()
