import smtplib
from email.mime.text import MIMEText
import os

# Load environment variables from .env file
from dotenv import load_dotenv

load_dotenv()
SMTP_SERVER = "smtp.gmail.com"  # Example: Gmail SMTP
SMTP_PORT = 587
SMTP_USER = os.getenv("SMTP_USER")  # Your email address
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")  # App password or SMTP password


def send_email(to_email: str, subject: str, body: str):
    """Send a simple text email via SMTP."""
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = to_email

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, [to_email], msg.as_string())
