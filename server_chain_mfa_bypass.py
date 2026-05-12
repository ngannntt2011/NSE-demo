import time
import random
from flask import request, jsonify

import server

# ========================================================
# VULNERABLE MFA SERVER - Chain Attack Demo
# Lỗ hổng:
#   1. OTP không bind vào session → ai cũng có thể submit
#   2. OTP không hết hạn (no expiration)
#   3. OTP có thể bị reuse nhiều lần
#   4. Không kiểm tra IP/device binding
# ========================================================

# Global OTP storage (VULNERABLE: no session binding, no expiry)
otp_store = {}  # username -> {"otp": "123456", "created_at": time}

def generate_otp(username):
    """Tạo OTP mới cho user (VULNERABLE: lưu global, không bind session)"""
    otp = str(random.randint(100000, 999999))
    otp_store[username] = {
        "otp": otp,
        "created_at": time.time(),
        "used": False  # Tracking nhưng KHÔNG enforce
    }
    return otp


def otp_page(username):
    """Trang nhập OTP - hiển thị khi password đúng"""
    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>MFA Verification - Chain Attack Demo</title>
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; }}
            body {{
                min-height: 100vh; display: flex; justify-content: center; align-items: center;
                background: linear-gradient(135deg, rgba(30, 20, 60, 0.92), rgba(20, 40, 80, 0.95)),
                            url('/static/cyber_bg.jpg') no-repeat center center/cover;
                font-family: "Segoe UI", sans-serif; color: white;
            }}
            .otp-card {{
                width: 440px; padding: 44px 36px; border-radius: 28px;
                background: rgba(255, 255, 255, 0.08); backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.15);
                box-shadow: 0 24px 60px rgba(0, 0, 0, 0.45);
                text-align: center; animation: slideUp 0.6s cubic-bezier(.22,.68,0,1);
            }}
            @keyframes slideUp {{
                from {{ opacity: 0; transform: translateY(30px) scale(0.96); }}
                to {{ opacity: 1; transform: translateY(0) scale(1); }}
            }}
            .shield-icon {{
                width: 72px; height: 72px; border-radius: 50%; display: flex;
                align-items: center; justify-content: center; margin: 0 auto 22px;
                background: linear-gradient(135deg, rgba(255, 165, 0, 0.25), rgba(255, 100, 0, 0.15));
                border: 1.5px solid rgba(255, 165, 0, 0.5);
                box-shadow: 0 0 30px rgba(255, 165, 0, 0.15);
                animation: pulse 2s ease-in-out infinite;
            }}
            @keyframes pulse {{
                0%, 100% {{ box-shadow: 0 0 20px rgba(255, 165, 0, 0.15); }}
                50% {{ box-shadow: 0 0 35px rgba(255, 165, 0, 0.3); }}
            }}
            .shield-icon svg {{ width: 32px; height: 32px; fill: #FFA500; }}
            h2 {{ color: #FFD700; font-size: 22px; margin-bottom: 8px; letter-spacing: 0.5px; }}
            .subtitle {{ color: #b8c8d8; font-size: 13px; margin-bottom: 24px; line-height: 1.6; }}
            .user-badge {{
                display: inline-block; padding: 6px 16px; border-radius: 20px;
                background: rgba(255, 165, 0, 0.12); border: 1px solid rgba(255, 165, 0, 0.3);
                color: #FFD700; font-size: 13px; font-weight: 600; margin-bottom: 22px;
            }}
            .otp-input-wrap {{ position: relative; margin-bottom: 20px; }}
            input[type="text"] {{
                width: 100%; padding: 16px; border-radius: 14px;
                border: 1.5px solid rgba(255, 255, 255, 0.15);
                background: rgba(0, 0, 0, 0.25); color: white;
                font-size: 24px; font-weight: 700; text-align: center;
                letter-spacing: 8px; outline: none; transition: all 0.3s;
            }}
            input[type="text"]:focus {{
                border-color: #FFA500;
                box-shadow: 0 0 16px rgba(255, 165, 0, 0.25);
            }}
            input[type="text"]::placeholder {{
                color: #667788; font-size: 16px; letter-spacing: 3px;
            }}
            .verify-btn {{
                width: 100%; padding: 15px; border-radius: 14px; border: none;
                background: linear-gradient(135deg, #FF8C00, #FFA500);
                color: white; font-weight: 700; font-size: 15px;
                cursor: pointer; transition: all 0.3s;
                box-shadow: 0 8px 24px rgba(255, 140, 0, 0.25);
            }}
            .verify-btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 12px 28px rgba(255, 140, 0, 0.35);
            }}
            .warning-tag {{
                margin-top: 24px; padding: 10px 16px; border-radius: 10px;
                background: rgba(255, 0, 0, 0.08); border: 1px solid rgba(255, 80, 80, 0.25);
                font-size: 11px; color: #ff9999; line-height: 1.5;
            }}
            .warning-tag .vuln {{ color: #ff6666; font-weight: 700; }}
        </style>
    </head>
    <body>
        <div class="otp-card">
            <div class="shield-icon">
                <svg viewBox="0 0 24 24"><path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 10.99h7c-.53 4.12-3.28 7.79-7 8.94V12H5V6.3l7-3.11v8.8z"/></svg>
            </div>
            <h2>MFA Verification</h2>
            <p class="subtitle">A 6-digit verification code has been sent to your device</p>
            <div class="user-badge">👤 {username}</div>
            <form action="/verify-otp" method="post">
                <input type="hidden" name="username" value="{username}">
                <div class="otp-input-wrap">
                    <input type="text" name="otp" placeholder="● ● ● ● ● ●" maxlength="6" required autocomplete="off">
                </div>
                <button type="submit" class="verify-btn">🔐 Verify & Login</button>
            </form>
            <div class="warning-tag">
                ⚠️ <span class="vuln">[VULNERABLE]</span> This server has NO OTP expiration,
                NO session binding, and allows OTP reuse — for demo purposes only.
            </div>
        </div>
    </body>
    </html>
    '''


# ---- API endpoint: Attacker dùng để "đánh cắp" OTP ----
@server.app.route('/api/steal-otp/<username>', methods=['GET'])
def steal_otp(username):
    """
    VULNERABLE ENDPOINT: Mô phỏng việc OTP bị đánh cắp
    (phishing page, SIM swap, malware trên device, man-in-the-middle...)
    Trong thực tế, attacker lấy OTP qua:
      - Phishing page giả mạo trang nhập OTP
      - SIM swapping để nhận SMS OTP
      - Malware đọc notification/SMS
      - Real-time phishing proxy (evilginx2)
    """
    if username in otp_store:
        data = otp_store[username]
        return jsonify({
            "status": "stolen",
            "username": username,
            "otp": data["otp"],
            "created_at": data["created_at"],
            "age_seconds": round(time.time() - data["created_at"], 1),
            "method": "phishing / SIM swap / malware interception"
        })
    return jsonify({"status": "no_otp", "username": username}), 404


# ---- API endpoint: Attacker submit OTP bị đánh cắp ----
@server.app.route('/api/submit-otp', methods=['POST'])
def api_submit_otp():
    """
    VULNERABLE: Cho phép submit OTP qua API không cần session
    Không kiểm tra: IP, device fingerprint, session token
    """
    data = request.get_json() or {}
    username = data.get("username", "")
    otp = data.get("otp", "")

    if username in otp_store and otp_store[username]["otp"] == otp:
        # OTP đúng → account takeover thành công!
        print(f"\n{'!'*60}")
        print(f"  [CRITICAL] ACCOUNT TAKEOVER: {username}")
        print(f"  OTP '{otp}' was stolen and submitted via API")
        print(f"  No session binding → Attack SUCCESS")
        print(f"{'!'*60}\n")
        # VULNERABLE: không clear OTP → có thể reuse
        return jsonify({
            "status": "success",
            "message": "Account takeover successful!",
            "username": username,
            "access": "full_account_access"
        })
    return jsonify({"status": "failed", "message": "Invalid OTP"}), 401


def login_with_vulnerable_mfa():
    """Login handler: password check → nếu đúng thì yêu cầu OTP (có lỗ hổng)"""
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    success = username in server.users and server.users[username] == password

    if success:
        user_agent = request.headers.get("User-Agent", "")

        # Tạo OTP cho user (VULNERABLE: global storage, no binding)
        otp = generate_otp(username)

        if "python" in user_agent.lower():
            # Request từ attack script → trả về MFA required
            print(f"[MFA] Password correct for '{username}' → OTP generated: {otp}")
            return f'''<html><body>
                <p>MFA_REQUIRED - Security Verification needed</p>
                <p>OTP has been sent to user device</p>
                <p>Username: {username}</p>
            </body></html>'''

        # Request từ browser → hiện trang OTP
        print(f"\n{'='*50}")
        print(f"  [MFA] OTP for {username}: {otp}")
        print(f"  [VULN] No expiry, no session binding!")
        print(f"{'='*50}\n")
        return otp_page(username)
    else:
        return server.login_response(username, False)


def verify_otp_handler():
    """Verify OTP từ form browser (VULNERABLE)"""
    username = request.form.get("username", "")
    entered_otp = request.form.get("otp", "")

    if username in otp_store and otp_store[username]["otp"] == entered_otp:
        age = time.time() - otp_store[username]["created_at"]
        print(f"[MFA] OTP verified for {username} (age: {age:.1f}s)")
        # VULNERABLE: không xóa OTP → có thể reuse
        return server.login_response(username, True,
            message="Authentication successful. MFA verification passed.")
    else:
        expected = otp_store.get(username, {}).get("otp", "N/A")
        print(f"[MFA] Invalid OTP for {username} (entered: {entered_otp}, expected: {expected})")
        return server.login_response(username, False,
            message="OTP verification failed. Invalid code.")


# Ghi đè login handler
server.app.view_functions['login'] = login_with_vulnerable_mfa

# Thêm route verify-otp
server.app.add_url_rule('/verify-otp', 'verify_otp', verify_otp_handler, methods=['POST'])

if __name__ == "__main__":
    print("=" * 60)
    print("  CHAIN ATTACK DEMO - VULNERABLE MFA SERVER")
    print("  Vulnerabilities:")
    print("    • OTP has NO expiration")
    print("    • OTP is NOT bound to session/IP")
    print("    • OTP can be reused multiple times")
    print("    • OTP can be stolen via /api/steal-otp/<user>")
    print("    • OTP can be submitted via /api/submit-otp")
    print("=" * 60)
    server.app.run(port=5000)
