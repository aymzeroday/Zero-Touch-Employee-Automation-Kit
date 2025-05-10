# Zero-Touch Employee Automation Kit 🚀

A fully automated, cross-platform onboarding/offboarding system for Azure AD and Google Workspace — with Slack/Teams alerts, email notifications, a secure web dashboard, and bulk CSV upload support.

## 🔧 Features

✅ Azure AD onboarding & offboarding  
✅ Google Workspace onboarding & offboarding  
✅ Manual onboarding form (Web UI)  
✅ Bulk CSV upload with per-user status  
✅ Real-time Slack + Microsoft Teams alerts  
✅ Email notifications (welcome & exit)  
✅ Log viewer with color-coded results  
✅ Secure Flask dashboard with login  
✅ Environment-based config (.env + config.json)

---

## 🖼️ Screenshots

- Dashboard Home  
- Manual Form  
- Bulk Upload  
- Results Table  
- Login Page  

*(Add images in `assets/` and link here)*

---

## 📦 Folder Structure

<!-- ```
employee-automation-kit/
├── main.py
├── .env.example
├── config.json
├── requirements.txt
├── azure_onboard.py
├── azure_offboard.py
├── google_onboard.py
├── google_offboard.py
├── email_notify.py
├── notifier.py
├── logs/
│   └── automation.log
├── templates/
│   ├── welcome_email.html
│   └── exit_email.html
├── dashboard/
│   ├── app.py
│   ├── uploads/
│   └── templates/
│       ├── index.html
│       ├── login.html
│       ├── onboard.html
│       ├── bulk_upload.html
│       └── bulk_results.html
``` -->

---

## ⚙️ Setup

### 1. Clone the Repo

```bash
git clone https://github.com/yourorg/employee-automation-kit.git
cd employee-automation-kit
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Configure

- Copy `.env.example` → `.env` and fill values  
- Update `config.json` with Azure/GWS settings

### 4. Run CLI or Dashboard

#### CLI

```bash
python main.py
```

#### Web Dashboard

```bash
cd dashboard
python app.py
```

---

## 🛂 .env Configuration

```env
ADMIN_USERNAME=admin
ADMIN_PASSWORD=StrongPass123
SENDER_ADDRESS=it@example.com
SLACK_WEBHOOK=https://hooks.slack.com/...
TEAMS_WEBHOOK=https://outlook.office.com/webhook/...
```

---

## 🧠 config.json Example

```json
{
  "default_password": "TempPass@123",
  "groups": ["group-guid-1", "group-guid-2"],
  "license_sku_id": "your-azure-license-guid",
  "logo_url": "https://yourcompany.com/logo.png",
  "google_service_account_file": "credentials.json",
  "google_delegated_admin": "admin@yourcompany.com",
  "google_domain": "yourcompany.com",
  "google_org_unit": "/Employees"
}
```

---

## 📁 CSV Upload Format

```csv
Full Name,Username,Domain,Platform
Alice Smith,asmith,example.com,azure
Bob Jones,bjones,example.com,google
```

---

## ✅ Next Up (Future Features)

- Role-based onboarding templates  
- Approval workflow  
- Asset management tracking  
- Slack command bot (e.g. `/onboard`)  
- HRMS sync (BambooHR, Sheets, etc.)

---

## 📄 License

MIT — built with love by Ahmad.

---

## 💬 Need Help?

Open an issue or [contact me](mailto:aymzeroday@gmail.com) if you’re stuck.
