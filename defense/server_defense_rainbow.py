import bcrypt
import sys
import os
from flask import request

# Đảm bảo in được emoji trên Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Thiết lập đường dẫn để import từ thư mục servers
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from servers import server

# 1. Cơ sở dữ liệu giả lập lưu mật khẩu đã băm bằng Bcrypt
# Bcrypt tự động tạo Salt và lưu Salt đó ngay trong chuỗi Hash
secure_db = {
    "alice": bcrypt.hashpw("aa12".encode('utf-8'), bcrypt.gensalt())
}

def secure_login_bcrypt():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    
    if username in secure_db:
        # 2. Kiểm tra mật khẩu bằng Bcrypt (bcrypt.checkpw)
        # Nó sẽ tự tách Salt từ hash cũ ra để so sánh
        success = bcrypt.checkpw(password.encode('utf-8'), secure_db[username])
        
        print(f" [🛡️] DEFENSE: Bcrypt verification for {username}")
        print(f"     Stored Bcrypt Hash: {secure_db[username].decode()[:30]}...")
        
        return server.login_response(username, success)
    
    return server.login_response(username, False)

# 3. Ghi đè logic đăng nhập
server.app.view_functions['login'] = secure_login_bcrypt

if __name__ == "__main__":
    print("\n" + "="*60)
    print(" 🛡️  DEFENSE 2: BCRYPT PASSWORD PROTECTION")
    print(" Status: Running on http://localhost:5000")
    print(" Algorithm: Bcrypt (Industry Standard)")
    print("="*60)
    
    # 4. Chạy server thực sự trên port 5001
    server.app.run(port=5000)
