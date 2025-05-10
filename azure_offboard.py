import os
import requests
import json
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

def get_user_id(upn):
    url = f"https://graph.microsoft.com/v1.0/users/{upn}"
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()["id"]

def disable_user(upn):
    url = f"https://graph.microsoft.com/v1.0/users/{upn}"
    data = {
        "accountEnabled": False
    }
    r = requests.patch(url, headers=headers, json=data)
    r.raise_for_status()

def remove_licenses(upn):
    url = f"https://graph.microsoft.com/v1.0/users/{upn}/assignLicense"
    data = {
        "addLicenses": [],
        "removeLicenses": [CONFIG["license_sku_id"]]
    }
    r = requests.post(url, headers=headers, json=data)
    r.raise_for_status()

def remove_from_all_groups(user_id):
    url = f"https://graph.microsoft.com/v1.0/users/{user_id}/memberOf"
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    groups = r.json()["value"]

    for group in groups:
        if group["@odata.type"] == "#microsoft.graph.group":
            group_id = group["id"]
            delete_url = f"https://graph.microsoft.com/v1.0/groups/{group_id}/members/{user_id}/$ref"
            del_req = requests.delete(delete_url, headers=headers)
            del_req.raise_for_status()

def get_user_manager(upn):
    url = f"https://graph.microsoft.com/v1.0/users/{upn}/manager"
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.json().get("mail")
    return None

if __name__ == "__main__":
    upn = input("Enter user's UPN (e.g. jdoe@example.com): ")

    print("Disabling account...")
    disable_user(upn)

    print("Removing licenses...")
    remove_licenses(upn)

    print("Removing from groups...")
    user_id = get_user_id(upn)
    remove_from_all_groups(user_id)

    print("Sending exit email...")
    html = render_template("templates/exit_email.html", {
        "upn": upn,
        "logo_url": CONFIG["logo_url"]
    })

    send_email("it-team@example.com", f"User {upn} Offboarded", html)

    manager_email = get_user_manager(upn)
    if manager_email:
        send_email(manager_email, f"{upn} offboarded", html)

    print("Notifying Slack/Teams...")
    notify_all(f"⚠️ User offboarded: *{upn}*")

    print("✅ Offboarding complete.")
