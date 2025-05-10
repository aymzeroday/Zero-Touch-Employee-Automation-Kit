import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv
from notifier import notify_all

load_dotenv()

with open("config.json") as f:
    CONFIG = json.load(f)

SERVICE_ACCOUNT_FILE = CONFIG["google_service_account_file"]
DELEGATED_ADMIN = CONFIG["google_delegated_admin"]
DOMAIN = CONFIG["google_domain"]

SCOPES = [
    "https://www.googleapis.com/auth/admin.directory.user"
]

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
delegated_creds = creds.with_subject(DELEGATED_ADMIN)

service = build("admin", "directory_v1", credentials=delegated_creds)

def suspend_google_user(email):
    service.users().update(
        userKey=email,
        body={"suspended": True}
    ).execute()
    print(f"⚠️ Suspended Google user: {email}")
    notify_all(f"⚠️ GWS user offboarded: *{email}*")

if __name__ == "__main__":
    username = input("Username to suspend (without domain): ")
    email = f"{username}@{DOMAIN}"
    suspend_google_user(email)
