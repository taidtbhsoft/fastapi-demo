from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from .config import settings
from typing import List, Optional
from pydantic import EmailStr
from . import schemas
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
conf = ConnectionConfig(
    MAIL_USERNAME = settings.mail_username,
    MAIL_PASSWORD = settings.mail_password,
    MAIL_FROM = settings.mail_from,
    MAIL_PORT = settings.mail_port,
    MAIL_SERVER = settings.mail_server,
    MAIL_FROM_NAME= settings.mail_from_name,
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True,
)

async def send_email_async(subject: str = '', email_to: list[EmailStr] = [], body: str = '') -> bool:
    if len(email_to) == 0:
        return False
    try:
        message = MessageSchema(
            subject=subject,
            recipients=email_to,
            body=body,
            subtype='html'
        )

        fm = FastMail(conf)
        await fm.send_message(message)
        print("Send Email Successfully")
        return True
    except Exception as e:
        print("Error Send Email")
        return False
