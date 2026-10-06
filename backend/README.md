# LED Test Backend

REST API FastAPI untuk menyimpan device dan riwayat status LED pada MariaDB.
Dependency Python dan virtual environment dikelola menggunakan
[`uv`](https://docs.astral.sh/uv/). Project ini tidak memerlukan Docker.

## Quick Start

Jalankan seluruh command berikut dari folder `backend`:

```bash
cd backend
```

Pastikan Python 3.12+, `uv`, dan MariaDB sudah tersedia. Sinkronkan dependency:

```bash
uv sync
```

Buat database dan user development dengan membuka prompt MariaDB:

```bash
sudo mariadb
```

Jalankan SQL berikut:

```sql
CREATE DATABASE IF NOT EXISTS led_test
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'led_user'@'localhost'
  IDENTIFIED BY 'led_password';

GRANT ALL PRIVILEGES ON led_test.* TO 'led_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

Jalankan migrasi database:

```bash
uv run alembic upgrade head
```

Jalankan server development:

```bash
uv run fastapi dev
```

Server tersedia di `http://127.0.0.1:8000`. Buka dokumentasi Swagger di
`http://127.0.0.1:8000/docs`.

Verifikasi koneksi API dan database dari terminal lain:

```bash
curl http://127.0.0.1:8000/health
```

Respons yang berhasil:

```json
{"status":"ok","database":"connected"}
```

Jalankan smoke test untuk memeriksa health check, pembuatan device, dan status LED:

```bash
uv run python scripts/smoke_test.py
```

## Layanan

| Layanan | Alamat |
| --- | --- |
| FastAPI | `http://127.0.0.1:8000` |
| Dokumentasi API | `http://127.0.0.1:8000/docs` |
| Apache/PHP | `http://127.0.0.1` |
| MariaDB | `127.0.0.1:3306` |

## Persiapan Native

Untuk environment Arch Linux, paket utama yang dibutuhkan adalah `mariadb`,
`apache`, `php`, `php-apache`, dan ekstensi MySQL untuk PHP.

Periksa layanan:

```bash
systemctl status mariadb
systemctl status httpd
```

Jika belum aktif:

```bash
sudo systemctl enable --now mariadb httpd
```

Konfigurasi database development menggunakan nilai berikut:

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
`src/backend/database.py`.

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

## Troubleshooting

Jika `/health` mengembalikan HTTP 503, pastikan MariaDB aktif dan kredensial
database sesuai dengan `src/backend/database.py`:

```bash
sudo systemctl start mariadb
mariadb -u led_user -p led_test
```

Jika tabel belum ditemukan, jalankan ulang migrasi dari folder `backend`:

```bash
uv run alembic upgrade head
```

Jika port 8000 sedang digunakan, pilih port lain:

```bash
uv run fastapi dev --port 8001
```
