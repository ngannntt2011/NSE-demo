import hashlib
import time
import sys

# Đảm bảo in được emoji trên Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def demo_secure_hash():
    password = "password123"
    
    # 1. MD5 thông thường (Hacker bẻ được dễ dàng)
    insecure_hash = hashlib.md5(password.encode()).hexdigest()
    
    # 2. Secure Hash (MD5 + Salt + Multi-Iterations)
    salt = "NSE_DEMO_2024_@#" # Chuỗi muối ngẫu nhiên
    
    # Băm 1000 lần (Key Stretching - Mô phỏng Bcrypt)
    secure_hash = password
    for _ in range(1000):
        secure_hash = hashlib.md5((secure_hash + salt).encode()).hexdigest()

    print("\n" + "="*60)
    print(" 🛡️  DEFENSE 2: RAINBOW TABLE PROTECTION")
    print("="*60)
    print(f" Raw Password   : {password}")
    print("-" * 60)
    print(f" [❌] Insecure MD5 Hash : {insecure_hash}")
    print("   -> Status: Vulnerable to Rainbow Table Attack")
    print("-" * 60)
    print(f" [✅] Secure Salted Hash : {secure_hash}")
    print("   -> Status: IMMUNE to standard Rainbow Tables")
    print("   -> Technique: Salting + Key Stretching (1000 rounds)")
    print("=" * 60)
    print("\n [i] Hướng dẫn demo: ")
    print(" 1. Cho giáo viên thấy bảng Rainbow Table MD5 tìm được 'password123'.")
    print(" 2. Show mã băm Secure và thách thức hacker dùng bảng cũ để tìm mật khẩu.")
    print(" 3. Giải thích: Vì có 'Muối' ngẫu nhiên, mã băm này không tồn tại trên bất kỳ bảng tra cứu nào.")

if __name__ == "__main__":
    demo_secure_hash()
