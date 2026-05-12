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

**Lưu ý:** Tất cả các lệnh dưới đây nên được chạy từ **thư mục gốc** (`NSE-demo/`).

Mỗi kịch bản yêu cầu chạy **1 Server** (để mô phỏng mục tiêu) và **1 Attack Script** (để thực hiện tấn công).

### Giai đoạn 1: Brute Force (Vét cạn)
*   **Server:** `python servers/server_bruteforce.py`
*   **Attack:** `python attacks/attack_bruteforce.py`

### Giai đoạn 2: Rainbow Table (Bảng cầu vồng)
*   **Server:** `python servers/server.py`
*   **Attack:** `python attacks/rainbow_attack.py`

### Giai đoạn 3: Dictionary Attack (Tấn công từ điển)
*   **Server:** `python servers/server.py`
*   **Attack:** `python attacks/attack_dictionary.py`

### Giai đoạn 4: Credential Stuffing (Nhồi thông tin)
*   **Server:** `python servers/server.py`
*   **Attack:** `python attacks/attack_credential.py`

### Giai đoạn 5: Advanced Chain Attack (Tấn công chuỗi + Bypass MFA)
*   **Server:** `python servers/server_chain_mfa_bypass.py`
*   **Attack:** `python attacks/attack_chain_mfa_bypass.py`

---

## 🛡️ Demo các biện pháp phòng thủ

Sau khi demo tấn công, bạn có thể chạy các server đã được cấu hình phòng thủ để thấy sự khác biệt:

1.  **Phòng thủ Brute Force:** `python defense/server_defense_brute_dict.py`
2.  **Phòng thủ Rainbow Table:** `python defense/server_defense_rainbow.py`
3.  **Phòng thủ MFA nâng cao:** `python defense/server_defense_advanced_mfa.py`

---

## 📁 Cấu trúc thư mục dự án
*   `servers/`: Chứa các máy chủ mô phỏng lỗ hổng.
*   `attacks/`: Chứa các script thực hiện tấn công.
*   `defense/`: Chứa các giải pháp phòng thủ nâng cao.
*   `data/`: Chứa cơ sở dữ liệu mẫu (`wordlist`, `credentials`) và công cụ test hash.
*   `static/`: Chứa tài nguyên giao diện (hình ảnh).

---
⚠️ **Cảnh báo:** Chỉ sử dụng mã nguồn này cho mục đích học tập. Việc tấn công các hệ thống khi chưa được phép là vi phạm pháp luật.
