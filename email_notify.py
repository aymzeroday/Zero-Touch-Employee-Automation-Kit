# email_notify.py
import requests
import os
from msal import ConfidentialClientApplication
from dotenv import load_dotenv

load_dotenv()

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SENDER = os.getenv("SENDER_ADDRESS")  # e.g., admin@example.com

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://graph.microsoft.com/.default"]

app = ConfidentialClientApplication(
    client_id=CLIENT_ID,
    client_credential=CLIENT_SECRET,
    authority=AUTHORITY
)

token = app.acquire_token_for_client(scopes=SCOPE)
if "access_token" not in token:
    raise Exception("Authentication failed.")

headers = {
    "Authorization": f"Bearer {token['access_token']}",
    "Content-Type": "application/json"
}

def render_template(path, replacements):
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()
        for key, value in replacements.items():
            content = content.replace(f"{{{{{key}}}}}", value)
        return content

def send_email(recipient, subject, html_body):
    url = f"https://graph.microsoft.com/v1.0/users/{SENDER}/sendMail"
    payload = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "HTML",
                "content": html_body
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": recipient
                    }
                }
            ]
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
