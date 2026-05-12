import hashlib
import time
import sys
import os
from flask import request

# Đảm bảo in được emoji trên Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Thiết lập đường dẫn để import từ thư mục servers
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from servers import server

SALT = "NSE_DEMO_2024_@#"

def generate_secure_hash(password):
    # Hàm băm bảo mật: MD5 + Salt + 1000 vòng lặp
    secure_hash = password
    for _ in range(1000):
        secure_hash = hashlib.md5((secure_hash + SALT).encode()).hexdigest()
    return secure_hash

# 2. Database giả lập lưu mật khẩu đã băm
secure_db = {"alice": generate_secure_hash("aa12")}

def secure_login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    
    if username in secure_db:
        # So sánh mã băm thay vì text thuần
        success = generate_secure_hash(password) == secure_db[username]
        return server.login_response(username, success)
    return server.login_response(username, False)

# 3. Ghi đè logic đăng nhập cũ
server.app.view_functions['login'] = secure_login

if __name__ == "__main__":
    print("\n" + "="*60)
    print(" 🛡️  DEFENSE 2: RAINBOW TABLE PROTECTION SERVER")
    print(" Status: Running on http://localhost:5000")
    print("="*60)
    
    # 4. Chạy server thực sự trên port 5000
    server.app.run(port=5000)
