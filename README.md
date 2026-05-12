# 🛡️ NSE Password Attack & Defense Simulation Demo

Dự án này mô phỏng các kỹ thuật tấn công mật khẩu phổ biến và các biện pháp phòng thủ tương ứng. Đây là môi trường lab phục vụ mục đích giáo dục và nghiên cứu an ninh mạng.

---

## 🛠️ Hướng dẫn thiết lập (Setup)

Làm theo các bước sau để thiết lập môi trường trên máy tính mới:

### 1. Cài đặt Python
Đảm bảo máy tính đã cài đặt **Python 3.8** trở lên. Kiểm tra bằng lệnh:
```bash
python --version
```

### 2. Tải mã nguồn
Clone kho lưu trữ về máy:
```bash
git clone https://github.com/ngannntt2011/NSE-demo.git
cd NSE-demo
```

### 3. Tạo môi trường ảo (Virtual Environment)
Việc này giúp quản lý thư viện độc lập, tránh xung đột hệ thống:

**Trên Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**Trên macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Cài đặt thư viện cần thiết
```bash
pip install -r requirements.txt
```

---

## 🚀 Hướng dẫn chạy Demo

Mỗi kịch bản yêu cầu chạy **1 Server** (để mô phỏng mục tiêu) và **1 Attack Script** (để thực hiện tấn công).

### Giai đoạn 1: Brute Force (Vét cạn)
*   **Mở Terminal 1 (Server):** `python server_bruteforce.py`
*   **Mở Terminal 2 (Attack):** `python attack_bruteforce.py`
*   *Mục tiêu:* Tìm ra mật khẩu ngắn bằng cách thử mọi tổ hợp ký tự.

### Giai đoạn 2: Rainbow Table (Bảng cầu vồng)
*   **Mở Terminal 1 (Server):** `python server.py`
*   **Mở Terminal 2 (Attack):** `python rainbow_attack.py`
*   *Mục tiêu:* Bẻ khóa mã băm (hash) MD5 không có muối (salt).

### Giai đoạn 3: Dictionary Attack (Tấn công từ điển)
*   **Mở Terminal 1 (Server):** `python server.py`
*   **Mở Terminal 2 (Attack):** `python attack_dictionary.py`
*   *Mục tiêu:* Thử các mật khẩu phổ biến từ tệp `wordlist.txt`.

### Giai đoạn 4: Credential Stuffing (Nhồi thông tin)
*   **Mở Terminal 1 (Server):** `python server.py`
*   **Mở Terminal 2 (Attack):** `python attack_credential.py`
*   *Mục tiêu:* Sử dụng dữ liệu rò rỉ từ `leaked_credentials.txt` để đăng nhập vào hệ thống khác.

### Giai đoạn 5: Advanced Chain Attack (Tấn công chuỗi + Bypass MFA)
*   **Mở Terminal 1 (Server):** `python server_chain_mfa_bypass.py`
*   **Mở Terminal 2 (Attack):** `python attack_chain_mfa_bypass.py`
*   *Mục tiêu:* Kết hợp nhồi thông tin và đánh cắp OTP thông qua lỗ hổng API để chiếm quyền điều khiển tài khoản.

---

## 🛡️ Demo các biện pháp phòng thủ

Sau khi demo tấn công, bạn có thể chạy các server đã được cấu hình phòng thủ để thấy sự khác biệt:

1.  **Phòng thủ Brute Force:** `python server_defense_brute_dict.py` (Khóa tài khoản sau 5 lần sai).
2.  **Phòng thủ Rainbow Table:** `python server_defense_rainbow.py` (Sử dụng Salting + Key Stretching).
3.  **Phòng thủ MFA nâng cao:** `python server_defense_advanced_mfa.py` (Session Binding + IP Locking).

---

## 📁 Cấu trúc thư mục chính
*   `server.py`: Server đăng nhập cơ bản.
*   `attack_*.py`: Các kịch bản tấn công.
*   `server_defense_*.py`: Các kịch bản phòng thủ.
*   `static/`: Chứa hình ảnh giao diện.
*   `wordlist.txt`: Danh sách mật khẩu mẫu.
*   `leaked_credentials.txt`: Dữ liệu rò rỉ giả định.

---
⚠️ **Cảnh báo:** Chỉ sử dụng mã nguồn này cho mục đích học tập. Việc tấn công các hệ thống khi chưa được phép là vi phạm pháp luật.
