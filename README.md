# ESP32 LED Control

Project IoT untuk mengontrol dua LED melalui Blynk menggunakan ESP32. Status
WiFi, koneksi Blynk, alamat IP, kekuatan sinyal, dan kondisi LED ditampilkan
pada OLED SSD1306.

Repository ini juga menyertakan backend FastAPI dan MariaDB untuk menyimpan
device serta riwayat status LED.

## Fitur

- Kontrol LED merah pada GPIO 18 melalui Blynk Virtual Pin V0.
- Kontrol LED kuning pada GPIO 19 melalui Blynk Virtual Pin V1.
- OLED SSD1306 I2C pada GPIO 21 dan GPIO 22.
- Status WiFi dan Blynk diperbarui secara real-time pada OLED.
- Reconnect Blynk otomatis tanpa menghentikan tampilan OLED.
- Simulasi ESP32 menggunakan Wokwi dan PlatformIO.
- REST API FastAPI dengan database MariaDB.
- Migrasi database menggunakan Alembic.

## Struktur Project

```text
.
|-- backend/          # FastAPI, Alembic, MariaDB, dan halaman PHP
|-- include/          # Header lokal dan kredensial firmware
|-- src/main.cpp      # Firmware ESP32
|-- diagram.json      # Rangkaian Wokwi
|-- platformio.ini    # Konfigurasi PlatformIO dan library
`-- wokwi.toml        # Lokasi firmware untuk Wokwi
```

## Rangkaian

| Komponen | Pin ESP32 |
| --- | --- |
| LED merah | GPIO 18 |
| LED kuning | GPIO 19 |
| OLED SDA | GPIO 21 |
| OLED SCL | GPIO 22 |
| OLED VCC | 3V3 |
| OLED GND | GND |

## Menjalankan Firmware

Prasyarat:

- Visual Studio Code atau Code OSS
- Extension PlatformIO IDE
- Extension Wokwi Simulator
- Akun dan device Blynk

Buat file `include/secrets.h`:

```cpp
#pragma once

#define BLYNK_AUTH_TOKEN "token-device-blynk"
#define WIFI_SSID "Wokwi-GUEST"
#define WIFI_PASSWORD ""
```

Sesuaikan nilai token dan WiFi dengan environment yang digunakan.

Build firmware dari terminal:

```bash
~/.platformio/penv/bin/platformio run
```

Di editor, firmware juga dapat di-build melalui **PlatformIO: Build**. Setelah
build berhasil, jalankan **Wokwi: Start Simulator**.

Dashboard Blynk memerlukan dua datastream bertipe Integer dengan rentang `0`
sampai `1`:

| Datastream | Fungsi |
| --- | --- |
| V0 | LED merah |
| V1 | LED kuning |

## Menjalankan Backend

Panduan lengkap instalasi MariaDB, migrasi, menjalankan FastAPI, dan mencoba
endpoint tersedia di [`backend/README.md`](backend/README.md).

Quick start setelah MariaDB dikonfigurasi:

```bash
cd backend
uv sync
uv run alembic upgrade head
uv run fastapi dev
```

Backend tersedia di `http://127.0.0.1:8000` dan dokumentasi interaktifnya di
`http://127.0.0.1:8000/docs`.
