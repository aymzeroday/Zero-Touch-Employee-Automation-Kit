import os
import subprocess
import argparse
import datetime
from colorama import init, Fore, Style

# Init colorama for Windows
init(autoreset=True)

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def log_action(action, status):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {action}: {status}\n"
    with open(os.path.join(LOG_DIR, "automation.log"), "a") as log_file:
        log_file.write(entry)

def run_script(script_name):
    try:
        print(Fore.YELLOW + f"▶ Running {script_name}...\n")
        subprocess.run(["python", script_name], check=True)
        log_action(script_name, "SUCCESS")
        print(Fore.GREEN + f"✅ {script_name} completed.\n")
    except subprocess.CalledProcessError as e:
        log_action(script_name, f"ERROR: {e}")
        print(Fore.RED + f"❌ {script_name} failed. Check logs.\n")

def menu():
    print(Fore.CYAN + "\n=== Zero-Touch Employee Automation Kit ===\n")
    print(Fore.WHITE + "[1] Onboard new user")
    print("[2] Offboard user")
    print("[3] Exit\n")
    return input("Choose an option: ").strip()

def handle_cli_args():
    parser = argparse.ArgumentParser(description="Employee Automation CLI")
    parser.add_argument("--bulk", choices=["onboard", "offboard"], help="Run bulk operation via CSV")
    return parser.parse_args()

def bulk_handler(mode):
    script = f"bulk_{mode}.py"
    if os.path.exists(script):
        run_script(script)
    else:
        print(Fore.RED + f"⚠️ Bulk script {script} not found.")

if __name__ == "__main__":
    args = handle_cli_args()

    if args.bulk:
        bulk_handler(args.bulk)
        exit(0)

    while True:
        clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
        clear()
        choice = menu()

        if choice == "1":
            run_script("azure_onboard.py")
        elif choice == "2":
            run_script("azure_offboard.py")
        elif choice == "3":
            print(Fore.BLUE + "👋 Exiting. Goodbye.")
            break
        else:
            print(Fore.RED + "❌ Invalid choice. Press Enter to try again.")
            input()
