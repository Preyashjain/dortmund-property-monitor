# Email Configuration Template
# Copy this to config.py and fill in your details

EMAIL_CONFIG = {
    # Gmail SMTP settings (or use your email provider's settings)
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    
    # Your email credentials
    'from_email': 'your_email@gmail.com',
    'password': 'your_app_specific_password',  # NOT your regular Gmail password!
    
    # Where to send alerts
    'to_email': 'your_email@gmail.com',
}

# Other popular email providers:
# 
# Outlook/Hotmail:
# smtp_server: 'smtp-mail.outlook.com'
# smtp_port: 587
#
# Yahoo:
# smtp_server: 'smtp.mail.yahoo.com'
# smtp_port: 587
#
# GMX:
# smtp_server: 'mail.gmx.net'
# smtp_port: 587
