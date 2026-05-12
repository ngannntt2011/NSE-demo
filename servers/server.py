from flask import Flask, request

app = Flask(__name__)

users = {
    "alice": "password123",
    "bob": "hello123"
}

@app.route("/")
def home():
    preset_username = request.args.get("username", "")
    preset_password = request.args.get("password", "")
    demo_success = request.args.get("demo_success", "")

    if demo_success == "true":
        return login_response(preset_username, True, message="Simulation: Access granted via attack demo.")

    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NSE Demo Login</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: "Segoe UI", Arial, sans-serif;
            }}

            body {{
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                overflow: hidden;
                background:
                    linear-gradient(rgba(30, 58, 95, 0.72), rgba(30, 58, 95, 0.88)),
                    url('/static/cyber_bg.jpg') no-repeat center center/cover;
                position: relative;
            }}

            body::before {{
                content: "";
                position: absolute;
                inset: 0;
                background:
                    radial-gradient(circle at 20% 20%, rgba(73, 180, 227, 0.18), transparent 25%),
                    radial-gradient(circle at 80% 30%, rgba(61, 130, 215, 0.16), transparent 25%),
                    radial-gradient(circle at 50% 80%, rgba(241, 227, 211, 0.08), transparent 20%);
                animation: floatGlow 8s ease-in-out infinite alternate;
                pointer-events: none;
            }}

            @keyframes floatGlow {{
                0% {{ transform: scale(1) translateY(0px); }}
                100% {{ transform: scale(1.03) translateY(-8px); }}
            }}

            .login-card {{
                position: relative;
                z-index: 1;
                width: 400px;
                padding: 34px 28px 26px;
                border-radius: 24px;
                background: rgba(255, 255, 255, 0.10);
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
                border: 1px solid rgba(255, 255, 255, 0.18);
                box-shadow: 0 18px 50px rgba(0, 0, 0, 0.35);
                color: white;
                animation: cardFade 0.8s ease;
            }}

            @keyframes cardFade {{
                from {{
                    opacity: 0;
                    transform: translateY(20px) scale(0.98);
                }}
                to {{
                    opacity: 1;
                    transform: translateY(0) scale(1);
                }}
            }}

            .icon-wrap {{
                width: 78px;
                height: 78px;
                margin: 0 auto 16px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                background: linear-gradient(135deg, rgba(61,130,215,0.35), rgba(73,180,227,0.25));
                border: 1px solid rgba(255,255,255,0.18);
                box-shadow: 0 8px 25px rgba(0,0,0,0.20);
            }}

            .icon-wrap svg {{
                width: 36px;
                height: 36px;
                fill: #F1E3D3;
            }}

            .title {{
                text-align: center;
                font-size: 28px;
                font-weight: 700;
                color: #F1E3D3;
                letter-spacing: 0.3px;
            }}

            .subtitle {{
                text-align: center;
                font-size: 13px;
                color: #c9d8e1;
                margin-top: 6px;
                margin-bottom: 26px;
            }}

            .form-group {{
                margin-bottom: 18px;
            }}

            label {{
                display: block;
                margin-bottom: 8px;
                font-size: 14px;
                color: #F1E3D3;
            }}

            .input-box {{
                position: relative;
            }}

            .input-icon {{
                position: absolute;
                left: 14px;
                top: 50%;
                transform: translateY(-50%);
                width: 16px;
                height: 16px;
                fill: #F1E3D3;
                opacity: 0.95;
            }}

            input {{
                width: 100%;
                padding: 13px 14px 13px 42px;
                border-radius: 14px;
                border: 1px solid rgba(255,255,255,0.18);
                background: rgba(255,255,255,0.10);
                color: white;
                font-size: 14px;
                outline: none;
                transition: 0.25s ease;
            }}

            input::placeholder {{
                color: #d3dfe6;
            }}

            input:focus {{
                border-color: #49B4E3;
                box-shadow: 0 0 0 4px rgba(73,180,227,0.18);
                background: rgba(255,255,255,0.13);
            }}

            .password-input {{
                padding-right: 50px;
            }}

            .toggle-password {{
                position: absolute;
                right: 12px;
                top: 50%;
                transform: translateY(-50%);
                background: transparent;
                border: none;
                cursor: pointer;
                width: 26px;
                height: 26px;
                display: flex;
                align-items: center;
                justify-content: center;
                opacity: 0;
                pointer-events: none;
                transition: 0.3s ease;
            }}

            .input-box:focus-within .toggle-password,
            .password-input:not(:placeholder-shown) ~ .toggle-password {{
                opacity: 0.95;
                pointer-events: auto;
            }}

            .toggle-password svg {{
                width: 20px;
                height: 20px;
                fill: none;
                stroke: #F1E3D3;
                stroke-width: 2;
                stroke-linecap: round;
                stroke-linejoin: round;
                transition: 0.2s ease;
            }}

            .toggle-password:hover svg {{
                stroke: #49B4E3;
                transform: scale(1.1);
            }}

            .login-btn {{
                width: 100%;
                margin-top: 10px;
                padding: 13px;
                border: none;
                border-radius: 14px;
                cursor: pointer;
                font-size: 15px;
                font-weight: 700;
                color: white;
                background: linear-gradient(90deg, #3D82D7, #49B4E3);
                box-shadow: 0 10px 24px rgba(61,130,215,0.30);
                transition: 0.25s ease;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 12px;
                position: relative;
                overflow: hidden;
            }}

            .login-btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 14px 28px rgba(73,180,227,0.34);
            }}

            .login-btn.loading {{
                pointer-events: none;
                background: linear-gradient(90deg, #2D62A3, #3B91B8);
                color: transparent;
            }}

            .login-btn.loading::after {{
                content: "";
                position: absolute;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
                left: -100%;
                top: 0;
                animation: pulse 1.5s infinite;
            }}

            @keyframes spin {{
                from {{ transform: rotate(0deg); }}
                to {{ transform: rotate(360deg); }}
            }}

            @keyframes pulse {{
                0% {{ left: -100%; }}
                100% {{ left: 100%; }}
            }}

            .spinner {{
                position: absolute;
                width: 20px;
                height: 20px;
                border: 2.5px solid rgba(255,255,255,0.35);
                border-top: 2.5px solid white;
                border-radius: 50%;
                display: none;
                animation: spin 0.8s linear infinite;
                z-index: 2;
            }}

            .login-btn.loading .spinner {{
                display: block;
            }}

            input::-ms-reveal,
            input::-ms-clear {{
                display: none;
            }}

            .scan-line {{
                display: none;
            }}

            .bottom-text {{
                margin-top: 18px;
                text-align: center;
                font-size: 12px;
                color: #d8e3e8;
                opacity: 0.95;
            }}
        </style>
    </head>
    <body>
        <div class="login-card">

            <div class="icon-wrap">
                <svg viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M12 1a5 5 0 0 0-5 5v3H6a2 2 0 0 0-2 2v8a4 4 0 0 0 4 4h8a4 4 0 0 0 4-4v-8a2 2 0 0 0-2-2h-1V6a5 5 0 0 0-5-5zm-3 8V6a3 3 0 0 1 6 0v3H9zm3 3a2 2 0 0 1 1 3.732V18h-2v-2.268A2 2 0 0 1 12 12z"/>
                </svg>
            </div>

            <div class="title">Secure Access</div>
            <div class="subtitle">Cybersecurity Demo Login Portal</div>

            <form action="/login" method="post" onsubmit="showLoading(this)">
                <div class="form-group">
                    <label>Username</label>
                    <div class="input-box">
                        <svg class="input-icon" viewBox="0 0 24 24" aria-hidden="true">
                            <path d="M12 12a5 5 0 1 0-5-5 5 5 0 0 0 5 5zm0 2c-4.418 0-8 2.239-8 5v1h16v-1c0-2.761-3.582-5-8-5z"/>
                        </svg>
                        <input
                            type="text"
                            name="username"
                            placeholder="Enter username"
                            value="{preset_username}"
                        >
                    </div>
                </div>

                <div class="form-group">
                    <label>Password</label>
                    <div class="input-box">
                        <svg class="input-icon" viewBox="0 0 24 24" aria-hidden="true">
                            <path d="M17 8h-1V6a4 4 0 1 0-8 0v2H7a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-8a2 2 0 0 0-2-2zm-7-2a2 2 0 1 1 4 0v2h-4V6z"/>
                        </svg>
                        <input
                            type="password"
                            id="password"
                            name="password"
                            class="password-input"
                            placeholder="Enter password"
                            value="{preset_password}"
                        >
                        <button type="button" class="toggle-password" onclick="togglePassword()" aria-label="Toggle password">
                             <svg id="eyeIcon" viewBox="0 0 24 24" aria-hidden="true">
                                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                                <circle cx="12" cy="12" r="3"></circle>
                            </svg>
                        </button>
                    </div>
                </div>

                <button type="submit" class="login-btn" id="loginBtn">
                    <div class="spinner"></div>
                    <span id="btnText">Login</span>
                </button>
            </form>

            <div class="bottom-text">
                Password Attack Simulation Environment
            </div>
        </div>

        <script>
            function togglePassword() {{
                const passwordInput = document.getElementById("password");
                const eyeIcon = document.getElementById("eyeIcon");

                if (passwordInput.type === "password") {{
                    passwordInput.type = "text";
                    eyeIcon.innerHTML = `
                        <path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"></path>
                        <path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68"></path>
                        <path d="M6.61 6.61A13.52 13.52 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61"></path>
                        <line x1="2" y1="2" x2="22" y2="22"></line>
                    `;
                }} else {{
                    passwordInput.type = "password";
                    eyeIcon.innerHTML = `
                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                        <circle cx="12" cy="12" r="3"></circle>
                    `;
                }}
            }}

            function showLoading(form) {{
                const btn = document.getElementById("loginBtn");
                const text = document.getElementById("btnText");
                btn.classList.add("loading");
                text.textContent = "";
            }}

            window.addEventListener('pageshow', function(event) {{
                const btn = document.getElementById("loginBtn");
                const text = document.getElementById("btnText");
                if (btn && btn.classList.contains("loading")) {{
                    btn.classList.remove("loading");
                    text.textContent = "Login";
                }}
            }});
        </script>
    </body>
    </html>
    '''

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    success = username in users and users[username] == password
    return login_response(username, success)

def login_response(username, success, message=None):
    if success:
        status_title = "Access Granted"
        status_message = message or "Authentication successful. Valid credentials accepted."
        badge_class = "success"
        icon_svg = """
        <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="M9 16.2l-3.5-3.5L4 14.2l5 5 11-11-1.5-1.4z"/>
        </svg>
        """
    else:
        status_title = "Access Denied"
        status_message = message or "Authentication failed. Username or password is incorrect."
        badge_class = "failed"
        icon_svg = """
        <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="M18.3 5.71L12 12l6.3 6.29-1.41 1.41L10.59 13.4 4.29 19.7 2.88 18.29 9.17 12 2.88 5.71 4.29 4.29l6.3 6.3 6.29-6.3z"/>
        </svg>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login Result</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: "Segoe UI", Arial, sans-serif;
            }}

            body {{
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                background:
                    linear-gradient(rgba(30, 58, 95, 0.78), rgba(30, 58, 95, 0.90)),
                    url('/static/cyber_bg.jpg') no-repeat center center/cover;
                color: white;
            }}

            .result-card {{
                width: 420px;
                padding: 34px 28px;
                border-radius: 24px;
                background: rgba(255,255,255,0.10);
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
                border: 1px solid rgba(255,255,255,0.18);
                box-shadow: 0 18px 50px rgba(0, 0, 0, 0.35);
                text-align: center;
                animation: fadeUp 0.5s ease;
            }}

            @keyframes fadeUp {{
                from {{
                    opacity: 0;
                    transform: translateY(18px);
                }}
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}

            .status-icon {{
                width: 82px;
                height: 82px;
                margin: 0 auto 18px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
            }}

            .status-icon.success {{
                background: rgba(56, 189, 128, 0.18);
                border: 1px solid rgba(56, 189, 128, 0.45);
                box-shadow: 0 0 28px rgba(56, 189, 128, 0.18);
            }}

            .status-icon.failed {{
                background: rgba(239, 68, 68, 0.18);
                border: 1px solid rgba(239, 68, 68, 0.45);
                box-shadow: 0 0 28px rgba(239, 68, 68, 0.18);
            }}

            .status-icon svg {{
                width: 36px;
                height: 36px;
                fill: white;
            }}

            .status-title {{
                font-size: 30px;
                font-weight: 700;
                color: #F1E3D3;
                margin-bottom: 10px;
            }}

            .status-message {{
                font-size: 15px;
                line-height: 1.6;
                color: #d7e3ea;
                margin-bottom: 22px;
            }}

            .user-box {{
                margin: 0 auto 24px;
                padding: 14px 16px;
                width: 100%;
                border-radius: 14px;
                background: rgba(255,255,255,0.08);
                border: 1px solid rgba(255,255,255,0.12);
                color: #eaf3f7;
                font-size: 14px;
            }}

            .user-box strong {{
                color: #F1E3D3;
            }}

            .actions {{
                display: flex;
                gap: 12px;
                justify-content: center;
                flex-wrap: wrap;
            }}

            .btn {{
                text-decoration: none;
                padding: 12px 18px;
                border-radius: 12px;
                font-weight: 700;
                font-size: 14px;
                transition: 0.25s ease;
            }}

            .btn-primary {{
                background: linear-gradient(90deg, #3D82D7, #49B4E3);
                color: white;
                box-shadow: 0 10px 24px rgba(61,130,215,0.28);
            }}

            .btn-primary:hover {{
                transform: translateY(-2px);
            }}

            .btn-secondary {{
                background: rgba(255,255,255,0.10);
                color: white;
                border: 1px solid rgba(255,255,255,0.14);
            }}

            .btn-secondary:hover {{
                background: rgba(255,255,255,0.16);
            }}
        </style>
    </head>
    <body>
        <div class="result-card">
            <div class="status-icon {badge_class}">
                {icon_svg}
            </div>

            <div class="status-title">{status_title}</div>
            <div class="status-message">{status_message}</div>

            <div class="user-box">
                <strong>Username:</strong> {username}
            </div>

            <div class="actions">
                <a class="btn btn-primary" href="/">Back to Login</a>
                <a class="btn btn-secondary" href="javascript:history.back()">Try Again</a>
            </div>
        </div>
    </body>
    </html>
    """
if __name__ == "__main__":
    app.run(port=5000)