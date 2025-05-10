
# 🛠️ Zero-Touch Employee Automation Kit

Automate onboarding and offboarding across Azure AD, Google Workspace, Slack, and more. Ideal for IT & HR teams tired of repetitive account provisioning.

## 🔍 Features

✅ Azure AD user creation  
✅ Assign Microsoft 365 licenses & groups  
✅ Slack onboarding/offboarding alerts  
✅ Welcome/Exit emails via Outlook or Gmail  
✅ Supports Google Workspace (Pro)  
✅ Extensible: Jira, GitHub, Notion, more

---

## 🧩 Scripts Included

| File              | Description                                       |
|-------------------|---------------------------------------------------|
| `azure_onboard.py`  | Creates user in Azure AD, assigns licenses         |
| `azure_offboard.py` | Disables user, revokes licenses                   |
| `slack_notify.py`   | Sends messages to manager/team                    |
| `email_notify.py`   | Auto-emails welcome/exit message                  |
| `config.json`       | Define user roles, groups, license templates      |
| `main.py`           | Central runner – plug in any sequence             |

---

## ⚙️ Requirements

- Python 3.10+
- Access to Microsoft Graph API (Azure App with appropriate permissions)
- Optional:
  - Slack App Token
  - Google Admin SDK access
  - SMTP/Gmail for notifications

---

## 🚀 Quick Start

```bash
git clone https://github.com/yourname/employee-automation-kit.git
cd employee-automation-kit
pip install -r requirements.txt
python main.py
```
---

## 📞 Need Help?

**Custom integrations, config, or enterprise setup?**  
Email me: [aymzeroday@gmail.com](mailto:aymzeroday@gmail.com)  
Or message me on [LinkedIn](https://linkedin.com/in/ahmad-yasser-b06636202)

---

> ⚠️ For security, always test in a sandbox tenant before deploying in production.
