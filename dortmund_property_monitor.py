import os
import logging
import smtplib
from email.mime.text import MIMEText

# Configure logger
logging.basicConfig(level=logging.INFO)

# Email configuration with environment variables
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# Validate email configuration
if not all([EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD]):
    logging.error('Email configuration is not valid. Please check your environment variables.\n')
    raise ValueError('Invalid email configuration.')

# Function to send an email

def send_email(subject, body, to_email):
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = EMAIL_HOST_USER
        msg['To'] = to_email

        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        logging.error(f'Failed to send email: {e}')
        raise

# Retry logic
import time

max_retries = 3
retry_delay = 5

def fetch_data(url):
    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.warning(f'Attempt {attempt + 1} failed: {e}')
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                logging.error('All attempts to fetch data failed.')
                raise

# Main monitoring function

if __name__ == '__main__':
    # Assuming url and to_email are already defined
    url = 'http://example.com/data'
    to_email = 'recipient@example.com'

    try:
        data = fetch_data(url)
        logging.info('Data fetched successfully.')
        send_email('Dortmund Property Monitor Update', 'Data fetched: ' + str(data), to_email)
    except Exception as e:
        logging.error(f'An error occurred: {e}')