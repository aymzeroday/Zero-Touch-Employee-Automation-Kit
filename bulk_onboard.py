import csv
import os
import json
import requests
from msal import ConfidentialClientApplication
from dotenv import load_dotenv

load_dotenv()

# === Auth config ===
TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://graph.microsoft.com/.default"]

# === Load config ===
with open("config.json") as f:
    CONFIG = json.load(f)

# === Token setup ===
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

# === Core Functions ===
def create_user(display_name, user_principal_name, mail_nickname):
    url = "https://graph.microsoft.com/v1.0/users"
    data = {
        "accountEnabled": True,
        "displayName": display_name,
        "mailNickname": mail_nickname,
        "userPrincipalName": user_principal_name,
        "passwordProfile": {
            "forceChangePasswordNextSignIn": True,
            "password": CONFIG["default_password"]
        }
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["id"]

def add_user_to_groups(user_id):
    for group_id in CONFIG["groups"]:
        url = f"https://graph.microsoft.com/v1.0/groups/{group_id}/members/$ref"
        data = {
            "@odata.id": f"https://graph.microsoft.com/v1.0/directoryObjects/{user_id}"
        }
        r = requests.post(url, headers=headers, json=data)
        r.raise_for_status()

def assign_license(user_id):
    url = f"https://graph.microsoft.com/v1.0/users/{user_id}/assignLicense"
    data = {
        "addLicenses": [
            {
                "skuId": CONFIG["license_sku_id"]
            }
        ],
        "removeLicenses": []
    }
    r = requests.post(url, headers=headers, json=data)
    r.raise_for_status()

# === Bulk Processor ===
def process_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            full_name = row["Full Name"].strip()
            username = row["Username"].strip()
            domain = row["Domain"].strip()
            upn = f"{username}@{domain}"
            mail_nickname = username

            try:
                print(f"🔧 Onboarding: {full_name} ({upn})...")
                user_id = create_user(full_name, upn, mail_nickname)
                add_user_to_groups(user_id)
                assign_license(user_id)
                print(f"✅ Success: {full_name}\n")
            except Exception as e:
                print(f"❌ Failed: {full_name} — {e}\n")

# === Run ===
if __name__ == "__main__":
    process_csv("users.csv")
