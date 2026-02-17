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
// --- LIBRARIES: These are like "Apps" we install to give our ESP32 new powers ---
#include <WiFi.h>           // Connects us to the internet
#include <PubSubClient.h>   // Allows us to speak the MQTT language
#include "DHTesp.h"         // Tells the ESP32 how to read our specific sensor
#include <ArduinoJson.h>    // Allows us to package data into a JSON "envelope"

// --- SETTINGS: The "Phone Numbers" and "Thresholds" for our system ---
const char* ssid = "Wokwi-GUEST";           // The name of our virtual WiFi
const char* password = "";                  // No password needed for Wokwi
const char* mqtt_server = "broker.hivemq.com"; // Our public "Post Office" (Broker)
const int LED_PIN = 2; // Most ESP32s have a built-in LED on Pin 2
const float ALARM_THRESHOLD = 35.0; // --- ALARM SETTING: At what temperature should the Red LED turn on? ---

// --- MEMORY: Variables that help the ESP32 "remember" things ---
float lastTemp = 0;      // We store the last temperature here to compare with the next one
float threshold = 0.5;   // The minimum change required to trigger an update (0.5 degrees)

// --- OBJECTS: These are the digital "tools" we'll use throughout the script ---
WiFiClient espClient;
PubSubClient client(espClient);
DHTesp dht; // We'll just call our sensor tool 'dht'

void setup() {
  // Start the Serial Monitor so we can "see" what the ESP32 is thinking
  Serial.begin(115200);
  
  // Run our custom WiFi connection function (defined below)
  setup_wifi();
  
  // Tell our MQTT tool which server to use and which port (1883 is standard)
  client.setServer(mqtt_server, 1883);
  
  // Connect the sensor to Pin 15 on the ESP32 chip
  dht.setup(15, DHTesp::DHT22);

  // Tell the ESP32 that this pin is an OUTPUT (it sends electricity OUT to light the LED)
  pinMode(LED_PIN, OUTPUT);
}

void setup_wifi() {
  delay(10);
  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  
  // While we are NOT connected, print a dot every half-second
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi Connected!");
}

void reconnect() {
  // This function keeps trying until we are back online with the Broker
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    
    // Give our device a unique ID name for the broker
    if (client.connect("ESP32_Student_Client")) {
      Serial.println("connected");
    } else {
      // If it fails, wait 5 seconds before trying again
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  float currentTemp = dht.getTemperature();
  
  // --- RESTORED: Local Alarm Logic ---
  // The LED still acts as a local "Warning Light" regardless of the JSON data
  // --- Local Alarm Logic using our Setting ---
  if (currentTemp > ALARM_THRESHOLD) { 
    digitalWrite(LED_PIN, HIGH); // Alarm ON
    Serial.println("🚨 LOCAL ALARM: High Temperature Detected!");
  } else {
    digitalWrite(LED_PIN, LOW);  // Alarm OFF
  }

  // --- "Report by Exception" JSON Logic ---
  if (abs(currentTemp - lastTemp) >= threshold) {
    StaticJsonDocument<200> doc;
    doc["temp"] = currentTemp;
    doc["hum"] = dht.getHumidity();
    doc["uptime"] = millis() / 1000;

    char buffer[256];
    serializeJson(doc, buffer);
    
    client.publish("curriculum/iot/temp", buffer);
    lastTemp = currentTemp;
    
    Serial.println("📡 Change detected. JSON payload sent!");
  }

  delay(2000); 
}
```

## 🚦 Step 3: Validation & Execution Sequence
To successfully test the "Smart Data" pipeline, you must follow this specific order. This ensures the "landing pad" is ready before the data starts flying.

1. The "Sanity Check" (Optional but Recommended)
Before running your Python scripts, open the HiveMQ Web Client.
* **Topic:** curriculum/iot/temp
* **Why:** This confirms the "Smart Data" is actually hitting the cloud before you try to process it with Python.

2. The Database (The Foundation)
* **Action:** Run the SQL script from Step 1 in pgAdmin.
* **Verification:** Refresh your tables list in the curriculum_iot_digital_twin_lab schema. You should see smart_sensor_data.

3. The Smart Bridge (The Courier)
* **Action:** Open a terminal in your Week-5 folder and run:
```bash
python bridge_v2.py
```
* **Verification:** You should see: 🚀 Smart Bridge active. Listening for JSON on: curriculum/iot/smart_data.

4. The Wokwi Simulation (The Source)
* **Action:** Start your Wokwi simulation.
* **Verification:** Check the Wokwi Serial Monitor. It should show Connected to MQTT.

5. The "Delta" Test (The Proof of Logic)
This is where we verify the Report by Exception logic:
* **The "Safe" Zone:** Set the Wokwi slider below 35°C.
* **Expectation:** Terminal says "Stored in Database." No email sent. LED is OFF.
* **The "Alarm" Zone:** Set the Wokwi slider above 35°C.
* **Expectation:** LED turns ON instantly. Terminal says "Sending email..." and "Stored in Database."
* **Check your inbox!**
* **Verification:** The Python terminal should immediately display: 📥 Received JSON: {'temp': ..., 'hum': ..., 'uptime': ...} followed by a success message.

## 🛠️ Step 4: Troubleshooting Checklist
* **No data appearing?** Ensure the MQTT_TOPIC in bridge_v2.py exactly matches the topic in your sketch.ino.
* **JSON Error?** Make sure you added the ArduinoJson library in the Wokwi Library Manager tab.
* **Database Error?** Confirm your .env file is present in the Week-5 folder.

---

## 🌟 BONUS: The "Live" Digital Twin Dashboard 📈
We will swap our static Plotly script for Streamlit, turning your Python code into a real-time web application.
* The Pitch: "Turn your Python script into a real web app in 10 lines of code."
* The Result: A live-updating website that reflects your "Digital Twin" in real-time.
