# Django Service Manager

Web-based microservices manager untuk Ubuntu/Linux menggunakan Django. Kelola semua services dengan sekali klik!

## ✨ Features

- ▶️ **Start/Stop Individual Service** - Control per service
- 🚀 **Start All / Stop All** - Jalankan atau stop semua services sekaligus
- 🔄 **Restart Service** - Restart tanpa stop manual
- 📋 **Real-time Logs** - Lihat output terminal dari setiap service
- 📊 **Live Status** - Auto-refresh status setiap 5 detik
- 🎯 **Process Management** - Kill child processes otomatis
- 📁 **Working Directory Support** - Jalankan dari directory manapun
- 🌐 **Port/URL Tracking** - Quick access ke service URLs
- ⚙️ **Django Admin Integration** - Manage services dari admin panel

**Compatible with:**
- Go services (`go run`)
- Docker Compose
- NPM/Node.js (`npm run dev`)
- Python services
- Bash scripts

---

## 🚀 Quick Start

### 1. Setup Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Database Migration

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Admin User

```bash
python manage.py createsuperuser
```

### 5. Setup Your Services (PENTING!)

**Option A: Auto Setup (Recommended)**
```bash
python manage.py setup_services
```

**Option B: Manual via Admin Panel**
- Buka http://127.0.0.1:8000/admin/
- Tambahkan services manual

### 6. Run Server

```bash
python manage.py runserver
```

---

## 📖 URLs

- **Dashboard:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/

---

## 🎯 How to Use

1. **Buka Dashboard** - Akses http://127.0.0.1:8000/
2. **Start Services:**
   - Klik **▶ Start** untuk individual service
   - Klik **▶ Start All** untuk start semua services
3. **Stop Services:**
   - Klik **⏹ Stop** untuk individual service  
   - Klik **⏹ Stop All** untuk stop semua services
4. **Restart:** Klik **🔄 Restart** untuk restart service
5. **View Logs:** Klik **📋 Logs** untuk lihat output terminal real-time

---

## ⚙️ Service Configuration

Edit services di **Admin Panel** dengan fields:

- **Name:** Nama service (contoh: "Service Proxy")
- **Command:** Command untuk jalankan (contoh: `go run main.go`)
- **Working Dir:** Directory path (contoh: `~/Documents/project/service-proxy`)
- **Port/URL:** Optional URL untuk quick access
- **Order:** Urutan tampilan di dashboard

---

## 💡 Tips

- Services dengan **PID** = service sedang running
- **Auto-refresh** setiap 5 detik untuk update status
- **Confirmation dialog** sebelum start/stop all
- **Process cleanup** otomatis termasuk child processes
- **Log viewer** punya auto-scroll untuk follow logs real-time
- **Logs** tersimpan di folder `logs/` dan bisa di-clear
- Untuk Docker services pakai `-d` flag agar tidak blocking

---

## 🛠️ Troubleshooting

**Service tidak start?**
- Cek working directory path sudah benar
- Pastikan command bisa dijalankan manual di terminal
- Cek permission untuk execute command

**PID masih muncul tapi service mati?**
- Dashboard akan auto-clean PID yang sudah mati
- Atau klik Stop untuk force clean

**Sudo command?**
- Untuk command yang butuh sudo, tambahkan di command field
- Example: `sudo docker-compose up -d`

---

## 📝 Example Services

Dari script Anda yang sudah ada:

| Service | Command | Working Dir |
|---------|---------|-------------|
| Service Collection | `go run cmd/web/main.go` | `~/Documents/ilham/Work_Samb/service-collection` |
| Service Proxy | `go run main.go` | `~/Documents/ilham/Work_Samb/service-proxy` |
| Service Proxy Frontend | `npm run dev` | `~/Documents/ilham/Work_Samb/service-proxy/public` |
| Service Master | `go run cmd/web/main.go` | `~/Documents/ilham/Work_Samb/service-master` |
| Service Identity Access | `go run main.go` | `~/Documents/ilham/Work_Samb/service-identity-access` |
| Service Print | `go run cmd/web/main.go` | `~/Documents/ilham/Work_Samb/service-print` |
| Service SDK | `docker-compose up -d` | `~/Documents/ilham/Work_Samb/service_sdk` |
| Service BIRT | `sudo docker-compose up -d` | `~/Documents/ilham/Work_Samb/service-birt-runtime-engine` |

---

## 🎨 Features Highlight

- **Dark UI** dengan Bootstrap 5
- **Color-coded status** (green = running, red = stopped)
- **Responsive design** 
- **Icons** untuk better UX
- **Smart process management** dengan psutil

---

## 🤝 Contributing

Feel free to improve! Ini tool internal untuk mempermudah development microservices.

---

Made with ❤️ for easier microservices management