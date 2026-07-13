# 🐳 Docker Setup - Remove Sudo Requirement

## Problem

Service BIRT menggunakan `sudo docker-compose` yang meminta password. Ini menyebabkan:
- Service tidak bisa start otomatis
- Log viewer error karena permission

## Solution: Add User to Docker Group

Tambahkan user Anda ke docker group agar bisa jalankan Docker tanpa sudo.

### Step 1: Add User to Docker Group

```bash
sudo usermod -aG docker $USER
```

### Step 2: Logout dan Login Kembali

**Option A: Reboot (Recommended)**
```bash
sudo reboot
```

**Option B: Logout/Login**
- Logout dari session sekarang
- Login kembali

**Option C: Apply Group Change Immediately (Session Only)**
```bash
newgrp docker
```

### Step 3: Verify

Test apakah sudah bisa jalankan docker tanpa sudo:

```bash
docker ps
```

Kalau berhasil (tidak minta sudo password), berarti sudah OK! ✅

### Step 4: Update Service BIRT

```bash
# Update service command untuk remove sudo
python manage.py shell

# Di shell:
from dashboard.models import Service
birt = Service.objects.get(name='Service BIRT Runtime Engine')
birt.command = 'docker-compose up -d'  # Remove sudo
birt.save()
exit()
```

Atau via Admin Panel:
1. Buka http://127.0.0.1:8000/admin/
2. Edit "Service BIRT Runtime Engine"
3. Ubah command dari `sudo docker-compose up -d` ke `docker-compose up -d`
4. Save

### Step 5: Test

```bash
# Restart Django server
python manage.py runserver
```

Sekarang service BIRT bisa:
- ✅ Start tanpa password prompt
- ✅ Stop dengan benar
- ✅ View logs tanpa error

---

## Alternative: Keep Using Sudo (Not Recommended)

Kalau tetap mau pakai sudo, perlu setup passwordless sudo untuk docker:

```bash
# Edit sudoers
sudo visudo

# Add line (ganti USERNAME dengan username Anda):
USERNAME ALL=(ALL) NOPASSWD: /usr/bin/docker-compose

# Save and exit
```

Tapi cara ini **tidak recommended** karena:
- Security risk (sudo tanpa password)
- Logs tetap butuh permission

**Better solution: Add user to docker group** ✅

---

## Troubleshooting

**Error: permission denied while trying to connect to Docker daemon**
- User belum masuk docker group
- Belum logout/login setelah add ke group

**Error: docker-compose command not found**
- Install docker-compose: `sudo apt install docker-compose`
- Atau pakai Docker Compose V2: `docker compose up -d`

**Logs masih error**
- Pastikan service stop dulu, lalu start lagi setelah fix sudo issue
- Clear logs: Klik button "🗑️ Clear Logs"

---

Setelah setup ini, semua Docker services akan jalan smooth tanpa sudo! 🎉
