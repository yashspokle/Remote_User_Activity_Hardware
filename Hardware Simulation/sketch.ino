#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <DHT.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

// =====================
// WIFI
// =====================

const char* ssid = "Wokwi-GUEST";
const char* password = "";

// CHANGE THIS
const char* serverUrl =
"https://public-lights-show.loca.lt/";

// =====================
// PINS
// =====================

#define PIR_PIN 18
#define BUTTON_PIN 4

#define DHT_PIN 5
#define DHT_TYPE DHT22

#define BUZZER_PIN 14

#define LED_LOW 25
#define LED_MEDIUM 26
#define LED_HIGH 27

// =====================

DHT dht(DHT_PIN, DHT_TYPE);
Adafruit_MPU6050 mpu;

// =====================

void connectWiFi() {

  WiFi.begin(ssid, password);

  Serial.print("Connecting");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi Connected");
  Serial.println(WiFi.localIP());
}

// =====================

void setup() {

  Serial.begin(115200);

  pinMode(PIR_PIN, INPUT);

  pinMode(BUTTON_PIN, INPUT_PULLUP);

  pinMode(LED_LOW, OUTPUT);
  pinMode(LED_MEDIUM, OUTPUT);
  pinMode(LED_HIGH, OUTPUT);

  pinMode(BUZZER_PIN, OUTPUT);

  dht.begin();

  Wire.begin(21,22);

  if(!mpu.begin()) {
    Serial.println("MPU6050 Not Found");
    while(true);
  }

  connectWiFi();
}

// =====================

void loop() {

  // ---------------------
  // PIR
  // ---------------------

  bool presence =
  digitalRead(PIR_PIN);

  String presenceStatus =
  presence ? "Present" : "Absent";

  // ---------------------
  // Button
  // ---------------------

  bool touch =
  !digitalRead(BUTTON_PIN);

  String touchActivity =
  touch ? "Active" : "Inactive";

  // ---------------------
  // DHT22
  // ---------------------

  float temperature =
  dht.readTemperature();

  float humidity =
  dht.readHumidity();

  // ---------------------
  // MPU6050
  // ---------------------

  sensors_event_t a, g, temp;

  mpu.getEvent(&a, &g, &temp);

  float movementScore =
  sqrt(
    a.acceleration.x * a.acceleration.x +
    a.acceleration.y * a.acceleration.y +
    a.acceleration.z * a.acceleration.z
  );

  // ---------------------
  // Risk Engine
  // ---------------------

  int risk = 0;

  if(!presence)
    risk += 25;

  if(!touch)
    risk += 20;

  if(movementScore > 12)
    risk += 35;

  if(temperature > 35)
    risk += 10;

  String riskLevel;

  if(risk <= 30)
    riskLevel = "Low";

  else if(risk <= 60)
    riskLevel = "Medium";

  else
    riskLevel = "High";

  // ---------------------
  // LEDs
  // ---------------------

  digitalWrite(LED_LOW, LOW);
  digitalWrite(LED_MEDIUM, LOW);
  digitalWrite(LED_HIGH, LOW);

  if(risk <= 30) {

    digitalWrite(LED_LOW, HIGH);
    noTone(BUZZER_PIN);

  }
  else if(risk <= 60) {

    digitalWrite(LED_MEDIUM, HIGH);
    noTone(BUZZER_PIN);

  }
  else {

    digitalWrite(LED_HIGH, HIGH);

    tone(BUZZER_PIN,1000);
  }

  // ---------------------
  // Serial Monitor
  // ---------------------

  Serial.println("==========");

  Serial.println(
    "Presence: " + presenceStatus
  );

  Serial.println(
    "Touch: " + touchActivity
  );

  Serial.println(
    "Temp: " + String(temperature)
  );

  Serial.println(
    "Humidity: " + String(humidity)
  );

  Serial.println(
    "Movement: " + String(movementScore)
  );

  Serial.println(
    "Risk: " + String(risk)
  );

  Serial.println(
    "Level: " + riskLevel
  );

  // ---------------------
  // Send To Flask
  // ---------------------

  if(WiFi.status() == WL_CONNECTED) {

    HTTPClient http;

    http.begin(serverUrl);

    http.addHeader(
      "Content-Type",
      "application/json"
    );

    String payload =
      "{"
      "\"device_id\":\"Endpoint01\","
      "\"presence_status\":\"" + presenceStatus + "\","
      "\"touch_activity\":\"" + touchActivity + "\","
      "\"movement_score\":" + String(movementScore,2) + ","
      "\"temperature\":" + String(temperature,2) + ","
      "\"humidity\":" + String(humidity,2) + ","
      "\"risk_score\":" + String(risk) + ","
      "\"risk_level\":\"" + riskLevel + "\""
      "}";

    int responseCode =
    http.POST(payload);

    Serial.print("HTTP: ");
    Serial.println(responseCode);

    http.end();
  }

  delay(5000);
}