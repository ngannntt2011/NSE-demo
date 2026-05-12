import time
from flask import request
import sys
import os

# Đảm bảo in được emoji trên Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from servers import server

# Cấu hình phòng thủ
failed_attempts = {}
MAX_ATTEMPTS = 5
LOCKOUT_TIME = 3  # Giây (Rate limiting mỗi request sai)

def lockout_page(username):
    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Account Locked</title>
        <style>
            body {{ background: #1a1a2e; color: white; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
            .card {{ background: rgba(255,0,0,0.1); padding: 40px; border-radius: 20px; border: 1px solid #ff4444; text-align: center; }}
            h1 {{ color: #ff4444; }}
            .btn {{ display: inline-block; margin-top: 20px; padding: 10px 20px; background: #ff4444; color: white; text-decoration: none; border-radius: 10px; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🛡️ Security Alert</h1>
            <p>Account <strong>{username}</strong> has been LOCKED.</p>
            <p>Too many failed attempts (5/5). Please contact admin.</p>
            <a href="/" class="btn">Back to Login</a>
        </div>
    </body>
    </html>
    '''

def login_with_lockout():
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    # 1. Kiểm tra xem tài khoản có đang bị khóa không
    if failed_attempts.get(username, 0) >= MAX_ATTEMPTS:
        print(f" [🛡️ ] DEFENSE: Blocked request for locked account: {username}")
        time.sleep(LOCKOUT_TIME) # Rate limiting
        return lockout_page(username)

    # 2. Kiểm tra thông tin đăng nhập
    success = username in server.users and server.users[username] == password

    if not success:
        # Tăng số lần thử sai
        failed_attempts[username] = failed_attempts.get(username, 0) + 1
        print(f" [🛡️ ] DEFENSE: Failed attempt {failed_attempts[username]}/{MAX_ATTEMPTS} for {username}")
        time.sleep(LOCKOUT_TIME) # Ép attacker chờ đợi (Rate limiting)
        return server.login_response(username, False, message=f"Invalid credentials. Attempt {failed_attempts[username]}/{MAX_ATTEMPTS}")
    else:
        # Reset nếu đúng
        failed_attempts[username] = 0
        return server.login_response(username, True)

# Ghi đè hàm login của server gốc
server.app.view_functions['login'] = login_with_lockout

if __name__ == "__main__":
    print("="*60)
    print(" 🛡️  DEFENSE 1: BRUTE FORCE & DICTIONARY PROTECTION")
    print(" Mechanisms: Account Lockout + Rate Limiting")
    print("="*60)
    server.app.run(port=5000)
