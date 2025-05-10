import os
import subprocess
import csv
from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

LOG_FILE = os.path.join(os.path.dirname(__file__), '..', 'logs', 'automation.log')
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ADMIN_USER = os.getenv("ADMIN_USERNAME")
ADMIN_PASS = os.getenv("ADMIN_PASSWORD")

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        user = request.form.get("username")
        pwd = request.form.get("password")
        if user == ADMIN_USER and pwd == ADMIN_PASS:
            session["user"] = user
            return redirect(url_for("index"))
        flash("Invalid credentials", "danger")
    return render_template("login.html")

@app.route('/logout')
@login_required
def logout():
    session.pop("user", None)
    flash("Logged out successfully.", "info")
    return redirect(url_for("login"))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/trigger/<script>')
@login_required
def trigger_script(script):
    script_map = {
        "azure_onboard": "azure_onboard.py",
        "azure_offboard": "azure_offboard.py",
        "google_onboard": "google_onboard.py",
        "google_offboard": "google_offboard.py"
    }

    if script in script_map:
        try:
            subprocess.run(["python", script_map[script]], check=True)
        except subprocess.CalledProcessError:
            return f"❌ Failed to run {script}", 500

    return redirect(url_for('index'))

@app.route('/logs')
@login_required
def view_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()[-100:]
    else:
        lines = ["No logs available."]
    return render_template('logs.html', logs=lines)

@app.route('/manual-onboard', methods=['GET', 'POST'])
@login_required
def manual_onboard():
    if request.method == "POST":
        name = request.form["name"]
        username = request.form["username"]
        domain = request.form["domain"]
        platform = request.form["platform"]

        script = "azure_onboard.py" if platform == "azure" else "google_onboard.py"
        env = os.environ.copy()
        env["ONBOARD_NAME"] = name
        env["ONBOARD_USERNAME"] = username
        env["ONBOARD_DOMAIN"] = domain

        try:
            subprocess.run(["python", script], check=True, env=env)
            flash(f"✅ Successfully onboarded {username}@{domain} via {platform.title()}", "success")
        except subprocess.CalledProcessError:
            flash("❌ Script failed. Check logs.", "danger")

        return redirect(url_for('manual_onboard'))

    return render_template("onboard.html")

@app.route('/bulk-upload', methods=['GET', 'POST'])
@login_required
def bulk_upload():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or not file.filename.endswith('.csv'):
            flash("Please upload a valid CSV file.", "danger")
            return redirect(url_for('bulk_upload'))

        path = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
        file.save(path)

        results = []
        with open(path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                name = row.get("Full Name")
                username = row.get("Username")
                domain = row.get("Domain")
                platform = row.get("Platform", "").strip().lower()
                script = "azure_onboard.py" if platform == "azure" else "google_onboard.py"
                env = os.environ.copy()
                env["ONBOARD_NAME"] = name
                env["ONBOARD_USERNAME"] = username
                env["ONBOARD_DOMAIN"] = domain

                try:
                    subprocess.run(["python", script], check=True, env=env)
                    results.append(f"✅ {username}@{domain} via {platform}")
                except subprocess.CalledProcessError:
                    results.append(f"❌ {username}@{domain} failed")

        for msg in results:
            flash(msg, "info")

        return redirect(url_for("bulk_upload"))

    return render_template("bulk_upload.html")

if __name__ == '__main__':
    app.run(debug=True)
