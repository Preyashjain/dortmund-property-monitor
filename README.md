# 🏠 Dortmund Property Alert System

Automatically monitor STWDO website for new Dortmund properties and get instant email alerts!

## ⚡ Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up email (choose one method):**

   **Method A - Environment Variables (Most Secure):**
   ```bash
   export EMAIL_ADDRESS='your_email@gmail.com'
   export EMAIL_PASSWORD='your_app_password'
   python quick_start.py
   ```

   **Method B - Edit Script Directly:**
   Edit `dortmund_property_monitor.py` and update the email_config section, then run:
   ```bash
   python dortmund_property_monitor.py
   ```

3. **Done!** The script will check every 5 minutes and email you when new Dortmund properties appear.

## 🔑 Getting Gmail App Password

1. Enable 2-Factor Authentication in your Google Account
2. Go to https://myaccount.google.com/security
3. Click "2-Step Verification" → "App passwords"
4. Generate password for "Mail"
5. Use this 16-character password in the script

## 📚 Full Documentation

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for:
- Detailed setup instructions
- Running as a background service
- Cloud hosting options (free)
- Customization options
- Troubleshooting

## 📧 What You'll Get

When a new property is found, you'll receive an email with:
- Property title
- Direct link to the listing
- Timestamp of when it was found

## 🎯 Features

✅ Checks every 5 minutes (configurable)
✅ Email alerts for new properties
✅ Tracks seen properties (no duplicate alerts)
✅ Beautiful HTML email formatting
✅ Free to run
✅ Easy to customize

## 🛠️ Files

- `dortmund_property_monitor.py` - Main script
- `quick_start.py` - Quick start with environment variables
- `requirements.txt` - Python dependencies
- `SETUP_GUIDE.md` - Detailed documentation
- `seen_properties.json` - Auto-generated tracking file

## 💡 Tips

- Run on a cloud server for 24/7 monitoring
- Adjust check interval in the script
- Add filters for specific criteria (rooms, price, etc.)
- Check spam folder for first alert

## ⚠️ Important

Use an **app-specific password**, not your regular email password!

---

Happy house hunting! 🏡
