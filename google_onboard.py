import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv
from notifier import notify_all
import os

load_dotenv()

with open("config.json") as f:
    CONFIG = json.load(f)

SERVICE_ACCOUNT_FILE = CONFIG["google_service_account_file"]
DELEGATED_ADMIN = CONFIG["google_delegated_admin"]
DOMAIN = CONFIG["google_domain"]
ORG_UNIT = CONFIG["google_org_unit"]
PASSWORD = CONFIG["default_password"]

SCOPES = [
    "https://www.googleapis.com/auth/admin.directory.user",
    "https://www.googleapis.com/auth/admin.directory.group"
]

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
delegated_creds = creds.with_subject(DELEGATED_ADMIN)

service = build("admin", "directory_v1", credentials=delegated_creds)

def create_google_user(full_name, username):
    email = f"{username}@{DOMAIN}"
    user_info = {
        "name": {
            "givenName": full_name.split()[0],
            "familyName": full_name.split()[-1]
        },
        "password": PASSWORD,
        "primaryEmail": email,
        "orgUnitPath": ORG_UNIT
    }

    service.users().insert(body=user_info).execute()
    print(f"✅ Google Workspace user created: {email}")
    notify_all(f"✅ GWS user onboarded: *{full_name}* ({email})")

if __name__ == "__main__":
    full_name = os.getenv("ONBOARD_NAME") or input("Enter full name: ")
    username = os.getenv("ONBOARD_USERNAME") or input("Enter username (without domain): ")
    create_google_user(full_name, username)
