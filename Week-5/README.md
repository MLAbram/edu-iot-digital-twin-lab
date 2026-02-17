# Week 5: Smart Data & The JSON Standard 🛰️

Now that we have a stable pipeline, we move from "Simple Data" to "Smart Data." This week focuses on the industry-standard **JSON** format and **Edge Optimization** to make your Digital Twin more efficient.

## 🎯 Learning Objectives
* **JSON Serialization:** Learn to bundle multiple sensor readings into a single packet.
* **Edge Logic:** Implement "Report by Exception" to save bandwidth and power.
* **PostgreSQL JSONB:** Store flexible, schema-less data in a relational database.

---

## 🛠️ Step 1: The Database Migration (SQL)
Before we can ingest JSON, we need to prepare the "landing pad" in PostgreSQL. We will use the `JSONB` data type, which allows for fast, indexed JSON storage.

**Run this in pgAdmin:**

```sql
CREATE TABLE curriculum_iot_digital_twin_lab.smart_sensor_data (
    id SERIAL PRIMARY KEY,
    sensor_id VARCHAR(50) DEFAULT 'ESP32_DEV_01',
    payload JSONB, -- This stores the entire JSON object
    aud_insert_ts TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
```

## ⚙️ Step 2: The "Optimized" Wokwi C++ Logic

**Clone Work**
1. Open curriculum-iot-digital-twin-celsius-lab-week-2. 
2. Make a copy by clicking on the down arrow next to the grayed out Save button. If your Save button is red, click to save first. Select the Save a copy options and name it: curriculum-iot-digital-twin-celsius-lab-week-5.

**Add to Library: ArduinoJson**
To send structured data, you must add the ArduinoJson library in the Wokwi Library Manager. We are also implementing a "Delta" check: the ESP32 will only transmit if the temperature changes by $\pm0.5^\circ\text{C}$.

**sketch.ino Updates**
Replace the code in your sketch.ino with what is below:

```cpp
#include <WiFi.h>
#include <PubSubClient.h>
#include "DHTesp.h"
#include <ArduinoJson.h>

// WiFi and MQTT Settings
const char* ssid = "Wokwi-GUEST";
const char* password = "";
const char* mqtt_server = "broker.hivemq.com";
float lastTemp = 0;
float threshold = 0.5;

WiFiClient espClient;
PubSubClient client(espClient);
DHTesp dhtSensor;

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  dhtSensor.setup(15, DHTesp::DHT22);
}

void setup_wifi() {
  delay(10);
  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi Connected!");
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32_Student_Client")) {
      Serial.println("connected");
    } else {
      delay(5000);
    }
  }
}

void loop() {
  float currentTemp = dht.readTemperature();
  
  // "Report by Exception" Logic
  if (abs(currentTemp - lastTemp) >= threshold) {
    // Create JSON document
    StaticJsonDocument<200> doc;
    doc["temp"] = currentTemp;
    doc["hum"] = dht.readHumidity();
    doc["uptime"] = millis() / 1000;

    char buffer[256];
    serializeJson(doc, buffer);
    
    // Notice the new 'smart_data' topic
    client.publish("curriculum/iot/smart_data", buffer);
    lastTemp = currentTemp;
    Serial.println("📡 Change detected. JSON payload sent!");
  }
  delay(2000); 
}
```

---

## 🌟 BONUS: The "Live" Digital Twin Dashboard 📈
We will swap our static Plotly script for Streamlit, turning your Python code into a real-time web application.
* The Pitch: "Turn your Python script into a real web app in 10 lines of code."
* The Result: A live-updating website that reflects your "Digital Twin" in real-time.
