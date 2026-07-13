# 🚀 Setup Guide - Django Service Manager

Setup cepat untuk menggantikan bash script dengan web dashboard.

## Step-by-Step Setup

### 1️⃣ Activate Virtual Environment

```bash
source venv/bin/activate
```

### 2️⃣ Install Dependencies (kalau belum)

```bash
pip install -r requirements.txt
```

### 3️⃣ Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4️⃣ Create Superuser (kalau belum ada)

```bash
python manage.py createsuperuser
# Username: admin
# Email: (tekan enter skip)
# Password: admin (atau password pilihan Anda)
```

### 5️⃣ Setup Services Otomatis

```bash
python manage.py setup_services
```

Command ini akan auto-create 8 services dari bash script Anda:
- Service Collection
- Service Proxy  
- Service Proxy Frontend
- Service Master
- Service Identity Access
- Service Print
- Service SDK
- Service BIRT Runtime Engine

### 6️⃣ Run Django Server

```bash
python manage.py runserver
```

### 7️⃣ Access Dashboard

Buka browser: **http://127.0.0.1:8000/**

---

## 🎯 Cara Pakai

### Start Services
- **Individual:** Klik tombol **▶ Start** di service yang ingin dijalankan
- **Semua:** Klik tombol **▶ Start All** di kanan atas

### Stop Services  
- **Individual:** Klik tombol **⏹ Stop**
- **Semua:** Klik tombol **⏹ Stop All**

### Restart
- Klik tombol **🔄 Restart**

---

## ⚙️ Customization

### Edit Service (Port, Command, dll)

1. Buka **http://127.0.0.1:8000/admin/**
2. Login dengan superuser
3. Klik **Services**
4. Edit service yang mau diubah
5. Save

### Tambah Service Baru

1. Buka Admin Panel
2. Klik **Add Service**
3. Isi fields:
   - **Name:** Nama service
   - **Command:** Command untuk run (contoh: `go run main.go`)
   - **Working dir:** Full path directory (contoh: `~/Documents/project`)
   - **Port/URL:** (Optional) URL untuk quick access
   - **Order:** Urutan tampilan (0 = paling atas)
4. Save

---

## 💡 Tips

- Dashboard **auto-refresh** setiap 5 detik
- Service yang **hijau** = sedang running
- Service yang **merah** = stopped
- Bisa akses URL service langsung dari kolom **Port/URL**

---

## 🔧 Troubleshooting

**Error: ModuleNotFoundError: No module named 'django'**
```bash
# Pastikan venv aktif
source venv/bin/activate
pip install -r requirements.txt
```

**Service tidak mau start**
- Cek working directory path sudah benar
- Test command manual di terminal dari directory tersebut
- Pastikan tidak ada typo di command

**PID stuck tapi service mati**
- Klik **⏹ Stop** untuk cleanup
- Atau refresh page (auto-clean setiap load)

---

Selamat! Anda sekarang bisa manage semua microservices dengan sekali klik browser! 🎉
