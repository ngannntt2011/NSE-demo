from flask import Flask, request
import server 

app = Flask(__name__)

# Đã đổi mật khẩu sang aa12
users = {
    "alice": "aa12"
}

@app.route("/")
def home():
    return server.home()

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    
    success = username in users and users[username] == password
    return server.login_response(username, success)

if __name__ == "__main__":
    print("="*60)
    print(" VULNERABLE BRUTE FORCE SERVER STARTING...")
    print(" Target: alice / password with 'aa12'")
    print("="*60)
    app.run(port=5000)
