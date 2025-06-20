import os
import imaplib
import smtplib
import email
import time
import tempfile
import re
from email.message import EmailMessage
from email.header import decode_header
from pyzbar.pyzbar import decode
from PIL import Image
from google.oauth2 import service_account
from googleapiclient.discovery import build
from base64 import urlsafe_b64decode

IMAP_SERVER = "s176.goserver.host"
IMAP_PORT = 993
SMTP_PORT = int(os.getenv("EMAIL_SMTP_PORT", "465"))
SMTP_SERVER = os.getenv("EMAIL_SMTP_SERVER")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
FOLDER_ID = os.getenv("FOLDER_ID")
SHEET_NAME = os.getenv("SHEET_NAME", "mail_log")
SERVICE_ACCOUNT_FILE = (
    "/etc/secrets/service-account.json"
    if os.path.exists("/etc/secrets/service-account.json")
    else "service-account.json"
)

def get_drive_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/spreadsheets"]
    )
    return build("drive", "v3", credentials=creds), build("sheets", "v4", credentials=creds)

def decode_str(s):
    parts = decode_header(s)
    decoded = ""
    for p, enc in parts:
        decoded += p.decode(enc or "utf-8", errors="ignore") if isinstance(p, bytes) else p
    return decoded
