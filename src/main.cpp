#define BLYNK_TEMPLATE_ID "TMPL6QM1O3dGF"
#define BLYNK_TEMPLATE_NAME "LED Control"

#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Arduino.h>
#include <BlynkSimpleEsp32.h>
#include <Wire.h>

#include "secrets.h"

constexpr uint8_t RED_LED_PIN = 18;
constexpr uint8_t YELLOW_LED_PIN = 19;
constexpr uint8_t OLED_SDA_PIN = 21;
constexpr uint8_t OLED_SCL_PIN = 22;
constexpr uint8_t OLED_ADDRESS = 0x3C;
constexpr int OLED_WIDTH = 128;
constexpr int OLED_HEIGHT = 64;
constexpr unsigned long DISPLAY_INTERVAL_MS = 500;
constexpr unsigned long RECONNECT_INTERVAL_MS = 5000;

Adafruit_SSD1306 display(OLED_WIDTH, OLED_HEIGHT, &Wire, -1);

bool redLedOn = false;
bool yellowLedOn = false;
bool oledReady = false;
unsigned long lastDisplayUpdate = 0;
unsigned long lastReconnectAttempt = 0;

// Menampilkan status koneksi, alamat IP, sinyal, dan kondisi kedua LED.
void showSystemStatus() {
  if (!oledReady) {
    return;
  }

  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setTextSize(1);

  display.setCursor(28, 0);
  display.println("IOT MONITOR");
  display.drawLine(0, 9, 127, 9, SSD1306_WHITE);

  display.setCursor(0, 13);
  display.print("WiFi : ");
  display.println(WiFi.status() == WL_CONNECTED ? "CONNECTED" : "OFFLINE");

  display.setCursor(0, 23);
  display.print("Blynk: ");
  display.println(Blynk.connected() ? "ONLINE" : "OFFLINE");

  display.setCursor(0, 34);
  display.print("IP   : ");
  if (WiFi.status() == WL_CONNECTED) {
    display.println(WiFi.localIP());
  } else {
    display.println("-");
  }

  display.setCursor(0, 45);
  display.print("RSSI : ");
  if (WiFi.status() == WL_CONNECTED) {
    display.print(WiFi.RSSI());
    display.println(" dBm");
  } else {
    display.println("-");
  }

  display.setCursor(0, 56);
  display.print("R:");
  display.print(redLedOn ? "ON" : "OFF");
  display.print("  Y:");
  display.print(yellowLedOn ? "ON" : "OFF");

  display.display();
}

// Menampilkan progress singkat saat perangkat dinyalakan.
void showBootAnimation() {
  display.setTextColor(SSD1306_WHITE);

  for (uint8_t progress = 0; progress <= 100; progress += 10) {
    display.clearDisplay();
    display.setTextSize(2);
    display.setCursor(21, 10);
    display.println("LED IOT");
    display.setTextSize(1);
    display.setCursor(37, 34);
    display.print("BOOT ");
    display.print(progress);
    display.print('%');
    display.drawRect(13, 50, 102, 9, SSD1306_WHITE);
    display.fillRect(16, 53, progress * 96 / 100, 3, SSD1306_WHITE);
    display.display();
    delay(60);
  }
}

// V0 menerima nilai tombol LED merah dari dashboard Blynk.
BLYNK_WRITE(V0) {
  redLedOn = param.asInt() == 1;
  digitalWrite(RED_LED_PIN, redLedOn ? HIGH : LOW);
  showSystemStatus();
}

// V1 menerima nilai tombol LED kuning dari dashboard Blynk.
BLYNK_WRITE(V1) {
  yellowLedOn = param.asInt() == 1;
  digitalWrite(YELLOW_LED_PIN, yellowLedOn ? HIGH : LOW);
  showSystemStatus();
}

// Ambil kembali nilai terakhir kedua tombol setelah Blynk tersambung.
BLYNK_CONNECTED() {
  Blynk.syncVirtual(V0, V1);
}

void setup() {
  Serial.begin(115200);

  pinMode(RED_LED_PIN, OUTPUT);
  pinMode(YELLOW_LED_PIN, OUTPUT);
  digitalWrite(RED_LED_PIN, LOW);
  digitalWrite(YELLOW_LED_PIN, LOW);

  Wire.begin(OLED_SDA_PIN, OLED_SCL_PIN);
  if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDRESS)) {
    Serial.println("OLED tidak ditemukan");
  } else {
    oledReady = true;
    showBootAnimation();
  }

  // Koneksi dibuat non-blocking agar OLED tetap menunjukkan status OFFLINE.
  WiFi.mode(WIFI_STA);
  WiFi.setAutoReconnect(true);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Blynk.config(BLYNK_AUTH_TOKEN);
  showSystemStatus();
}

void loop() {
  const unsigned long now = millis();

  if (WiFi.status() == WL_CONNECTED) {
    if (Blynk.connected()) {
      Blynk.run();
    } else if (now - lastReconnectAttempt >= RECONNECT_INTERVAL_MS) {
      lastReconnectAttempt = now;
      Blynk.connect(1000);
    }
  }

  if (now - lastDisplayUpdate >= DISPLAY_INTERVAL_MS) {
    lastDisplayUpdate = now;
    showSystemStatus();
  }
}
