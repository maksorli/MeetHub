import os
import smtplib
from email.mime.text import MIMEText

SMTP_HOST = os.getenv("SMTP_HOST", "mailcatcher")
SMTP_PORT = int(os.getenv("SMTP_PORT", 1025))


async def send_email(to_email: str, subject: str, body: str):
    """Отправляет email с заданным адресом, темой и телом письма"""
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = "noreply@example.com"
    msg["To"] = to_email

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.sendmail("noreply@example.com", to_email, msg.as_string())
