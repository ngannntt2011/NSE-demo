import time
import hashlib
import sys
import webbrowser
import bcrypt
from tqdm import tqdm

# Đảm bảo in được emoji trên Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Cấu hình mục tiêu MỚI (Nhắm vào Alice và mã băm Bcrypt)
# Đây là mã băm Bcrypt, không phải MD5
target_hash = "$2b$12$R9h/cIPz0gi.URNNX3kh2OPST9/zBJa9A0NQi/hYjW.u.7q.Z.GKi" 
username = "alice"
wordlist_file = "data/wordList.txt"

def print_banner():
    print("\n" + "="*60)
    print(" 🌈 PHASE 2: RAINBOW TABLE ATTACK (Updated for Bcrypt)")
    print("="*60)
    print(f" Target Hash : {target_hash[:30]}...")
    print(f" Algorithm   : Bcrypt (High Security)")
    print("-" * 60)

def main():
    print_banner()
    start_time = time.time()
    found_password = None

    try:
        with open(wordlist_file, "r", encoding="utf-8") as f:
            passwords = [line.strip() for line in f if line.strip()]
    except:
        print("[!] Error: data/wordList.txt not found.")
        return

    total_passwords = len(passwords)
    attempts = 0
    pbar = tqdm(total=total_passwords, desc=" [ANALYZING]", unit="hash", bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]')

    for password in passwords:
        attempts += 1
        # Kẻ tấn công vẫn dùng MD5 để thử (vì chúng tưởng server dùng MD5)
        hashed_word = hashlib.md5(password.encode()).hexdigest()
        
        tqdm.write(f" Comparing: MD5({password}) -> {hashed_word} vs Bcrypt Target")
        time.sleep(0.05)

        # So sánh MD5 với Bcrypt -> Chắc chắn không bao giờ khớp
        if hashed_word == target_hash:
            found_password = password
            pbar.close()
            break
            
        pbar.update(1)
    pbar.close()

    total_time = time.time() - start_time
    print("\n" + "="*60)
    print(" RAINBOW TABLE ATTACK RESULT")
    
    if found_password:
        print(f" Hash Status  : CRACKED")
        print(f" Password     : {found_password}")
    else:
        print(f" Hash Status  : ❌ FAILED (Defense is too strong)")
        print(f" Reason       : Bcrypt hashes cannot be cracked with MD5 Rainbow Tables.")
        print(f" Time taken   : {total_time:.2f}s")
    
    print("="*60 + "\n")

if __name__ == "__main__":
    main()