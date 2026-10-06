# LED Test Backend

Backend FastAPI dengan stack web development native: Apache, PHP, dan MariaDB.
Dependency Python dan virtual environment dikelola menggunakan
[`uv`](https://docs.astral.sh/uv/). Project ini tidak memerlukan Docker.

## Layanan

| Layanan | Alamat |
| --- | --- |
| FastAPI | `http://127.0.0.1:8000` |
| Dokumentasi API | `http://127.0.0.1:8000/docs` |
| Apache/PHP | `http://127.0.0.1` |
| MariaDB | `127.0.0.1:3306` |

## Persiapan Native

Mesin pengembangan ini menggunakan CachyOS/Arch Linux. Paket utama yang
dibutuhkan adalah `mariadb`, `apache`, `php`, `php-apache`, dan ekstensi MySQL
untuk PHP. Layanan MariaDB dan Apache sudah diaktifkan pada mesin ini.

Periksa layanan:

```bash
systemctl status mariadb
systemctl status httpd
```

Jika belum aktif:

```bash
sudo systemctl enable --now mariadb httpd
```

Database aplikasi telah disiapkan dengan nilai berikut:

```text
Database: led_test
User: led_user
Password: led_password
Host: 127.0.0.1
Port: 3306
```

Untuk development lokal, sinkronkan dependency dan jalankan migrasi:

```bash
uv sync
uv run alembic upgrade head
uv run fastapi dev
```

Konfigurasi koneksi development berada pada konstanta `DATABASE_URL` di
`src/backend/database.py`. Jangan gunakan password default tersebut untuk
deployment production.

## Struktur Database

Migrasi Alembic membuat tabel `devices`:

| Kolom | Tipe | Keterangan |
| --- | --- | --- |
| `id` | integer | Primary key, auto-increment |
| `name` | varchar | Nama device |

Tabel `led_statuses` menyimpan riwayat status setiap device:

| Kolom | Tipe | Keterangan |
| --- | --- | --- |
| `id` | integer | Primary key, auto-increment |
| `id_device` | integer | Foreign key ke `devices.id` |
| `status_led` | boolean | Status LED, wajib diisi |
| `timestamp` | datetime | Otomatis memakai waktu database |

Jalankan migrasi setiap kali mengambil perubahan schema:

```bash
uv run alembic upgrade head
```

Buat migrasi baru setelah mengubah model:

```bash
uv run alembic revision --autogenerate -m "deskripsi perubahan"
```

## API Device dan LED

Buat device terlebih dahulu:

```bash
curl -X POST http://127.0.0.1:8000/devices \
  -H "Content-Type: application/json" \
  -d '{"name": "ESP32 Ruang Utama"}'
```

Ambil daftar device:

```bash
curl http://127.0.0.1:8000/devices
```

Simpan status LED:

```bash
curl -X POST http://127.0.0.1:8000/led-statuses \
  -H "Content-Type: application/json" \
  -d '{"id_device": 1, "status_led": true}'
```

Ambil riwayat status terbaru:

```bash
curl http://127.0.0.1:8000/led-statuses
```

Periksa koneksi API dan database:

```bash
curl http://127.0.0.1:8000/health
```

## Perintah `uv`

Aktivasi virtual environment tidak diperlukan. Selalu jalankan tool Python
melalui `uv run`:

```bash
uv run python --version
uv add nama-package
uv add --dev nama-package
```

Jika tetap ingin aktivasi manual:

```bash
# Bash atau Zsh
source .venv/bin/activate

# Fish
source .venv/bin/activate.fish
```

PowerShell di Windows:

```powershell
.venv\Scripts\Activate.ps1
```
