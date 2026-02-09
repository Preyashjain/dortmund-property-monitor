# Dortmund Property Alert System - Setup Guide

## 📋 Overview
This system monitors the STWDO website for new Dortmund properties and sends you email alerts automatically every 5 minutes.

## 🔧 Requirements
- Python 3.6 or higher
- Internet connection
- Email account (Gmail recommended)

## 📦 Installation Steps

### 1. Install Python Dependencies
```bash
pip install requests beautifulsoup4
```

Or if you get permission errors:
```bash
pip install --user requests beautifulsoup4
```

### 2. Set Up Email Credentials

#### For Gmail Users:
1. **Enable 2-Factor Authentication** on your Google account
2. **Create an App Password**:
   - Go to https://myaccount.google.com/security
   - Click on "2-Step Verification"
   - Scroll down to "App passwords"
   - Select "Mail" and your device
   - Copy the 16-character password

#### For Other Email Providers:
- Check your provider's SMTP settings
- You may need to enable "less secure apps" or create an app-specific password

### 3. Configure the Script

Edit `dortmund_property_monitor.py` and update the `email_config` dictionary:

```python
email_config = {
    'smtp_server': 'smtp.gmail.com',  # Your SMTP server
    'smtp_port': 587,
    'from_email': 'youremail@gmail.com',  # Your email
    'password': 'your_app_password',  # The app password from step 2
    'to_email': 'youremail@gmail.com'  # Where to send alerts
}
```

## 🚀 Running the Monitor

### Option 1: Run Directly
```bash
python dortmund_property_monitor.py
```

### Option 2: Run in Background (Linux/Mac)
```bash
nohup python dortmund_property_monitor.py &
```

### Option 3: Run as a Service (Recommended for 24/7)

#### On Linux (systemd):
Create `/etc/systemd/system/dortmund-monitor.service`:
```ini
[Unit]
Description=Dortmund Property Monitor
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/script
ExecStart=/usr/bin/python3 /path/to/dortmund_property_monitor.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable dortmund-monitor
sudo systemctl start dortmund-monitor
```

#### On Windows (Task Scheduler):
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger to "When the computer starts"
4. Set action to start the Python script
5. Configure to run whether user is logged in or not

### Option 4: Run on a Cloud Server (Free Options)
- **PythonAnywhere** (free tier available)
- **Heroku** (with scheduler add-on)
- **Google Cloud** (free tier)
- **AWS Lambda** (free tier)

## ⚙️ Customization

### Change Check Interval
In `dortmund_property_monitor.py`, change the last line:
```python
monitor.run_monitor(interval_minutes=5)  # Change 5 to your desired minutes
```

### Modify Email Template
Edit the `create_email_html()` and `create_email_text()` methods to customize the alert format.

### Add Filters
Modify the property detection logic to filter by:
- Number of rooms
- Price range
- Specific districts in Dortmund

## 📊 How It Works

1. **Scraping**: Every 5 minutes, the script visits the STWDO website
2. **Filtering**: It looks for properties containing "Dortmund"
3. **Tracking**: New properties are compared against previously seen ones
4. **Alerting**: If new properties are found, an email is sent
5. **Storage**: Seen properties are saved to `seen_properties.json`

## 🐛 Troubleshooting

### No emails received?
- Check spam/junk folder
- Verify email credentials are correct
- Test SMTP connection:
```python
import smtplib
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('your_email@gmail.com', 'your_password')
print("Success!")
```

### Script crashes?
- Check internet connection
- Verify the website is accessible
- Look at error messages in the console

### Website structure changed?
The website HTML may change. You might need to update the CSS selectors in the `fetch_properties()` method.

## 📁 Files Created

- `seen_properties.json` - Tracks properties you've already been alerted about
- Logs/output in console

## 🛑 Stopping the Monitor

- If running in terminal: Press `Ctrl+C`
- If running as service: `sudo systemctl stop dortmund-monitor`
- If running in background: Find process with `ps aux | grep dortmund` and kill it

## 🔒 Security Notes

- Never commit your email password to version control
- Use app-specific passwords, not your main account password
- Consider using environment variables for sensitive data

## 📧 Support

If the script doesn't work:
1. Check the console output for error messages
2. Verify website is still using the same URL
3. Test with a simple property search manually
4. Adjust CSS selectors if website structure changed

## 🎯 Next Steps

Consider adding:
- SMS alerts via Twilio
- Telegram bot notifications
- Database storage for historical tracking
- Web dashboard to view found properties
- Advanced filtering (price, rooms, size)
