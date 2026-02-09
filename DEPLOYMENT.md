# Deployment Guide for Dortmund Property Monitor

## Prerequisites: Push to GitHub

### Step 1: Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `dortmund-property-monitor`
3. Description: "Automated property monitor for Dortmund real estate listings"
4. Choose "Public" (required for free Render deployment)
5. Click "Create repository"

### Step 2: Push Your Code
```bash
# Initialize git (run in your project directory)
cd "E:\flutter project\Alert System"
git init
git add .
git commit -m "Initial commit: Dortmund property monitor"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/dortmund-property-monitor.git
git push -u origin main
```

### Step 3: Add GitHub Secrets (Optional)
If using GitHub Actions for scheduled runs:
1. Go to your repository → Settings → Secrets and variables → Actions
2. Add secrets: `EMAIL_ADDRESS`, `EMAIL_PASSWORD`, `TO_EMAIL`

---

## Option 1: Run Locally (Windows)

### Quick Start
1. Double-click `run_monitor.bat` to start the monitor
2. Keep the window open - it will check every 5 minutes
3. Press `Ctrl+C` to stop

### Run in Background (Windows Task Scheduler)
1. Open Task Scheduler (search "Task Scheduler" in Start menu)
2. Click "Create Basic Task"
3. Name: "Dortmund Property Monitor"
4. Trigger: "When the computer starts"
5. Action: "Start a program"
6. Program: `pythonw.exe`
7. Arguments: `"E:\flutter project\Alert System\dortmund_property_monitor.py"`
8. Start in: `E:\flutter project\Alert System`
9. Check "Open Properties dialog" and set "Run whether user is logged on or not"

---

## Option 2: Deploy with Docker

### Prerequisites
- Docker Desktop installed

### Steps
```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## Option 3: Deploy to Free Cloud Services

### A) PythonAnywhere (Recommended - Free)

1. Create account at https://www.pythonanywhere.com
2. Go to "Files" tab, upload:
   - `dortmund_property_monitor.py`
   - `config.py`
   - `requirements.txt`
3. Open a Bash console and run:
   ```bash
   pip install --user -r requirements.txt
   ```
4. Go to "Tasks" tab
5. Create a scheduled task (free tier: 1 daily task)
   - For more frequent checks, upgrade to paid plan

### B) Railway.app (Free tier available)

1. Create account at https://railway.app
2. Connect your GitHub repository
3. Add environment variables:
   - `EMAIL_ADDRESS`
   - `EMAIL_PASSWORD`
   - `SMTP_SERVER`
   - `SMTP_PORT`
4. Deploy automatically

### C) Render.com (Free tier available)

1. Create account at https://render.com
2. Create new "Background Worker"
3. Connect GitHub repository
4. Set environment variables
5. Deploy

### D) Google Cloud Run (Free tier)

1. Install Google Cloud CLI
2. Build and push Docker image:
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT/property-monitor
   ```
3. Deploy as Cloud Run job with scheduled trigger

---

## Option 4: Run on a VPS (DigitalOcean, Linode, etc.)

### Using systemd (Linux)

1. Copy files to server
2. Create service file `/etc/systemd/system/property-monitor.service`:
   ```ini
   [Unit]
   Description=Dortmund Property Monitor
   After=network.target

   [Service]
   Type=simple
   User=your_user
   WorkingDirectory=/path/to/app
   ExecStart=/usr/bin/python3 dortmund_property_monitor.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

3. Enable and start:
   ```bash
   sudo systemctl enable property-monitor
   sudo systemctl start property-monitor
   ```

---

## Environment Variables

If using environment variables instead of `config.py`:

| Variable | Description | Default |
|----------|-------------|---------|
| `EMAIL_ADDRESS` | Your email address | Required |
| `EMAIL_PASSWORD` | App password | Required |
| `SMTP_SERVER` | SMTP server | smtp.gmail.com |
| `SMTP_PORT` | SMTP port | 587 |
| `TO_EMAIL` | Alert recipient | Same as EMAIL_ADDRESS |
| `CHECK_INTERVAL_MINUTES` | Check frequency | 5 |

---

## Monitoring & Logs

- Check `seen_properties.json` for tracked properties
- Monitor console output for status updates
- Email alerts are sent when new properties are found

---

## Troubleshooting

### No emails received
1. Check spam folder
2. Verify app password is correct
3. Ensure 2FA is enabled on Gmail
4. Test with `python test_setup.py`

### Script crashes
1. Check internet connection
2. Verify website is accessible
3. Check Python version (3.8+ required)

### Too many/few alerts
- Adjust `CHECK_INTERVAL_MINUTES` in the script
- Currently checks every 5 minutes
