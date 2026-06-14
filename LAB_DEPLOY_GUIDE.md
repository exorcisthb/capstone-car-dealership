# 🧪 Deploy bằng IBM SkillsBuild Lab + ngrok

## ⚠️ Lưu ý quan trọng
- **URL sẽ thay đổi mỗi lần restart ngrok** — mỗi session bạn cần chạy lại `bash start_ngrok.sh`
- **Data sẽ bị mất khi session kết thúc** — database là SQLite trong thư mục repo
- **Phù hợp cho demo/screenshots** — không ổn định như Render

---

## 📋 Cách làm (từng bước)

### Bước 1: Mở IBM SkillsBuild Lab

1. Vào lab **"Add Continuous Integration and Continuous Deployment"** (cái bạn đang mở)
2. Mở **Terminal** trong lab
3. Chạy lệnh clone repo (nếu chưa có):

```bash
git clone https://github.com/exorcisthb/xrwvm-fullstack_developer_capstone.git
cd xrwvm-fullstack_developer_capstone
```

### Bước 2: Setup một lần (chạy 1 lần thôi)

```bash
bash lab_setup.sh
```

Script này sẽ tự động:
- Tạo virtual environment
- Cài Python dependencies
- Run migrations + seed data (50 dealers, 8 car makes, test user)
- Tạo user `testuser` / `TestPass123`

### Bước 3: Chạy app mỗi khi cần

```bash
bash start_ngrok.sh
```

### Bước 4: Lấy URL để chụp ảnh

Khi script chạy thành công, bạn sẽ thấy:

```
DEPLOYED URL: https://xxxx-xxxx-xxxx.ngrok-free.app
```

**Lưu URL này** — dùng cho Task 25-28.

---

## 🔧 Cách lấy NGROK_AUTHTOKEN (nếu cần)

### Cách 1: Dùng không cần authtoken (URL không ổn định hơn chút)
- Script sẽ hoạt động mà không cần authtoken
- URL vẫn hoạt động, nhưng có thể bị limit

### Cách 2: Lấy authtoken miễn phí (khuyến nghị)
1. Vào https://dashboard.ngrok.com/get-started/your-authtoken
2. Đăng ký miễn phí bằng email/GitHub
3. Copy authtoken
4. Trong terminal lab, chạy:
```bash
export NGROK_AUTHTOKEN="your_token_here"
```

---

## 📸 Sau khi có URL, làm gì?

### Task 25: Public API (8 điểm)
```
curl https://YOUR_URL.ngrok-free.app/api/dealers
curl https://YOUR_URL.ngrok-free.app/api/carmakes
curl https://YOUR_URL.ngrok-free.app/api/dealers/1/reviews
```

### Task 26: Reviews CRUD (8 điểm)
```
curl -X POST https://YOUR_URL.ngrok-free.app/api/reviews \
  -H "Content-Type: application/json" \
  -d '{"dealer":1,"name":"Test","review_text":"Good!","purchase":true}'
```

### Task 27: User Login/Logout (4 điểm)
```
curl -X POST https://YOUR_URL.ngrok-free.app/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"TestPass123"}'
```

### Task 28: Deployment (4 điểm)
- Chụp ảnh URL đang chạy + ảnh API response

---

## 🔄 Khi muốn restart (session mới)

```bash
cd ~/xrwvm-fullstack_developer_capstone

# Pull code mới nhất
git pull origin main

# Reinstall nếu cần
source .venv/bin/activate
pip install -r server/requirements.txt

# Migrate + seed lại
cd server
python manage.py migrate --noinput
python manage.py seed_data
cd ..

# Chạy app
bash start_ngrok.sh
```

---

## ⚠️ Troubleshooting

### "git: command not found"
Lab đã có git sẵn. Thử:
```bash
which git
```

### "python3: command not found"
```bash
which python
```

### ngrok không hoạt động
- Thử chạy lại `bash start_ngrok.sh`
- Kiểm tra log: `cat ~/ngrok.log`

### Django lỗi
- Kiểm tra log: `cat ~/django.log`
- Chạy lại migrations: `python manage.py migrate`

---

## 📁 Các file trong lab

| File | Mục đích |
|------|----------|
| `lab_setup.sh` | Setup lần đầu (virtualenv, pip, ngrok) |
| `start_ngrok.sh` | Chạy app + tạo public URL |
| `~/deployed_url.txt` | Lưu URL hiện tại |
| `~/django.log` | Django log |
| `~/ngrok.log` | ngrok log |
