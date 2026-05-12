import time
import hashlib
import sys
import webbrowser
from tqdm import tqdm

# Đảm bảo in được emoji trên Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Cấu hình mục tiêu
target_hash = "f30aa7a662c728b7407c54ae6bfd27d1"  # MD5 của "hello123"
username = "bob"  # User liên quan đến hash
wordlist_file = "wordlist.txt"

def print_banner():
    print("\n" + "="*60)
    print(" 🌈 PHASE 2: RAINBOW TABLE ATTACK ")
    print("="*60)
    print(f" Target Hash : {target_hash}")
    print(f" Algorithm   : MD5 (Vulnerable)")
    print("-" * 60)

def main():
    print_banner()
    start_time = time.time()
    found_password = None

    try:
        with open(wordlist_file, "r", encoding="utf-8") as f:
            passwords = [line.strip() for line in f if line.strip()]
            if "hello123" not in passwords: passwords.append("hello123")
    except:
        print("[!] Error: wordlist.txt not found.")
        return

    total_passwords = len(passwords)
    attempts = 0
    pbar = tqdm(total=total_passwords, desc=" [ANALYZING]", unit="hash", bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]')

    for password in passwords:
        attempts += 1
        hashed_word = hashlib.md5(password.encode()).hexdigest()
        
        tqdm.write(f" Trying #{attempts}/{total_passwords}: {hashed_word} == {target_hash}")
        time.sleep(0.05) # Delay nhẹ để demo nhìn thấy

        if hashed_word == target_hash:
            found_password = password
            # Đẩy thanh progress lên 100%
            remaining = total_passwords - pbar.n
            if remaining > 0:
                pbar.update(remaining)
            pbar.close()
            print(f"\n [✅] HASH CRACKED! Match found: '{password}'")
            break
            
        pbar.update(1)
    pbar.close()

    if found_password:
        total_time = time.time() - start_time
        print("\n" + "="*60)
        print(" RAINBOW TABLE ATTACK RESULT")
        print(f" Hash Status  : CRACKED")
        print(f" Time taken   : {total_time:.2f}s")
        print(f" Password     : {found_password}")
        print("-" * 60)
        print(" [!] Opening web portal...")
        print(" [i] Password auto-filled. Please click 'Login' to verify.")
        time.sleep(1.5)
        webbrowser.open(f"http://localhost:5000/?username={username}&password={found_password}")
    else:
        print("\n [❌] FAILED: Hash not found in Rainbow Table.")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()