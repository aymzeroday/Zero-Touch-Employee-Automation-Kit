import os
import json
import requests
from msal import ConfidentialClientApplication
from dotenv import load_dotenv
from email_notify import send_email, render_template
from notifier import notify_all

load_dotenv()

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://graph.microsoft.com/.default"]

with open("config.json") as f:
    CONFIG = json.load(f)

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

def get_user_manager(upn):
    url = f"https://graph.microsoft.com/v1.0/users/{upn}/manager"
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.json().get("mail")
    return None

if __name__ == "__main__":
    display_name = os.getenv("ONBOARD_NAME") or input("Enter full name: ")
    username = os.getenv("ONBOARD_USERNAME") or input("Enter username (without domain): ")
    domain = os.getenv("ONBOARD_DOMAIN") or input("Enter domain (e.g. example.com): ")
    user_principal_name = f"{username}@{domain}"

    print("Creating user...")
    user_id = create_user(display_name, user_principal_name, username)
    print(f"User created: {user_id}")

    print("Adding to groups...")
    add_user_to_groups(user_id)

    print("Assigning license...")
    assign_license(user_id)

    print("Sending welcome email to user...")
    html = render_template("templates/welcome_email.html", {
        "name": display_name,
        "upn": user_principal_name,
        "password": CONFIG["default_password"],
        "logo_url": CONFIG["logo_url"]
    })
    send_email(user_principal_name, "Welcome to the Team!", html)

    print("Notifying manager...")
    manager_email = get_user_manager(user_principal_name)
    if manager_email:
        send_email(manager_email, f"{display_name} has joined your team", html)

    print("Notifying Slack/Teams...")
    notify_all(f"✅ User onboarded: *{display_name}* ({user_principal_name})")

    print("✅ Onboarding complete.")
