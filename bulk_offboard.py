import csv
import os
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

# === MSAL Token ===
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
def get_user_id(upn):
    url = f"https://graph.microsoft.com/v1.0/users/{upn}"
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()["id"]

def disable_user(upn):
    url = f"https://graph.microsoft.com/v1.0/users/{upn}"
    data = { "accountEnabled": False }
    r = requests.patch(url, headers=headers, json=data)
    r.raise_for_status()

def remove_licenses(upn):
    url = f"https://graph.microsoft.com/v1.0/users/{upn}/assignLicense"
    data = {
        "addLicenses": [],
        "removeLicenses": ["ENTER_SKU_ID"]  # Replace with actual
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

# === Bulk Processor ===
def process_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            upn = row["UPN"].strip()
            try:
                print(f"🔒 Offboarding: {upn}...")
                disable_user(upn)
                remove_licenses(upn)
                user_id = get_user_id(upn)
                remove_from_all_groups(user_id)
                print(f"✅ Success: {upn}\n")
            except Exception as e:
                print(f"❌ Failed: {upn} — {e}\n")

# === Run ===
if __name__ == "__main__":
    process_csv("users_offboard.csv")
