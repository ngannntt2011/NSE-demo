import time
import random
import uuid
from flask import request, jsonify
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'servers')))
import server

# Cấu hình Advanced MFA
otp_store = {}
OTP_EXPIRY = 30  # Giây

def generate_secure_otp(username, ip):
    otp = str(random.randint(100000, 999999))
    session_id = str(uuid.uuid4())
    otp_store[username] = {
        "otp": otp,
        "ip": ip,
        "session_id": session_id,
        "created_at": time.time()
    }
    return otp, session_id

def advanced_otp_page(username, session_id):
    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Advanced MFA</title>
        <style>
            body {{ background: #0f172a; color: white; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
            .card {{ background: rgba(56, 189, 128, 0.1); padding: 40px; border-radius: 20px; border: 1px solid #38BD80; text-align: center; width: 400px; }}
            h2 {{ color: #38BD80; }}
            .sec-info {{ font-size: 12px; color: #888; margin-top: 20px; text-align: left; background: rgba(0,0,0,0.2); padding: 10px; border-radius: 10px; }}
            input {{ width: 100%; padding: 15px; margin-top: 20px; border-radius: 10px; border: 1px solid #38BD80; background: #000; color: white; text-align: center; font-size: 20px; letter-spacing: 5px; }}
            button {{ width: 100%; padding: 15px; margin-top: 20px; border-radius: 10px; border: none; background: #38BD80; color: white; font-weight: bold; cursor: pointer; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h2>🛡️ Advanced MFA</h2>
            <p>OTP sent to your device for <strong>{username}</strong></p>
            <form action="/verify-otp" method="post">
                <input type="hidden" name="username" value="{username}">
                <input type="hidden" name="session_id" value="{session_id}">
                <input type="text" name="otp" placeholder="XXXXXX" maxlength="6" required>
                <button type="submit">Verify & Login</button>
            </form>
            <div class="sec-info">
                <strong>Active Defense:</strong><br>
                - OTP Expiry: 30s<br>
                - Session Binding: ACTIVE<br>
                - IP Binding: ACTIVE
            </div>
        </div>
    </body>
    </html>
    '''

def login_advanced():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    client_ip = request.remote_addr

    success = username in server.users and server.users[username] == password
    
    if success:
        user_agent = request.headers.get("User-Agent", "").lower()
        otp, sid = generate_secure_otp(username, client_ip)

        # Chặn đứng Attacker Script ngay tại đây
        if "python" in user_agent:
            print(f" [🛡️] DEFENSE: MFA Required for {username}. OTP generated but hidden from scripts.")
            return "MFA_REQUIRED"

        print(f"\n [🛡️] DEFENSE: OTP for {username} is {otp}")
        return advanced_otp_page(username, sid)
    else:
        return server.login_response(username, False)

def verify_otp():
    username = request.form.get("username", "")
    entered_otp = request.form.get("otp", "")
    session_id = request.form.get("session_id", "")
    client_ip = request.remote_addr

    if username in otp_store:
        data = otp_store[username]
        
        # 1. Kiểm tra hết hạn
        if time.time() - data["created_at"] > OTP_EXPIRY:
            return "<h1>OTP Expired</h1>"
            
        # 2. Kiểm tra Session & IP Binding
        if data["session_id"] != session_id or data["ip"] != client_ip:
            print(f" [🛡️] DEFENSE: Hijack Attempt Blocked! Session/IP mismatch.")
            return "<h1>🛡️ Access Denied: Session Hijack Detected</h1>"

        if data["otp"] == entered_otp:
            del otp_store[username]
            return server.login_response(username, True)
    
    return "<h1>Invalid OTP</h1>"

# Vô hiệu hóa API rò rỉ (Chặn đứng Chain Attack)
@server.app.route('/api/steal-otp/<username>')
def blocked_steal(username):
    return jsonify({"status": "blocked", "message": "API Disabled for security"}), 403

server.app.view_functions['login'] = login_advanced
server.app.add_url_rule('/verify-otp', 'verify_otp', verify_otp, methods=['POST'])

if __name__ == "__main__":
    print("="*60)
    print(" 🛡️  DEFENSE 3: ADVANCED MFA PROTECTION")
    print(" Mechanisms: Session Binding + IP Locking + No API")
    print("="*60)
    server.app.run(port=5000)
