## 🌐 Week 2: Machine-to-Machine (M2M) Networking
Last week, your ESP32 made decisions locally. This week, we connect it to the internet so it can report its "Digital Twin" telemetry to the cloud.

---

## 🎯 Learning Objectives
* **Virtual Gateway:** Connect the ESP32 to a simulated WiFi network.
* **Pub/Sub Architecture:** Master the Publisher/Subscriber model.
* **Cloud Integration:** Send live temperature data to a Public MQTT Broker.

---

## ⚖️ Step 1: Clone Wokwi Work
1. Open your **Week 1** project.
2. Make a copy by clicking the **down arrow** next to the Save button.
3. Select **Save a copy** and name it: curriculum-iot-digital-twin-celsius-lab-week-2.

---

## 📚 Step 2: Library Management
Wokwi requires specific drivers to "speak" to the internet.
1. Click the **Library Manager** tab (the bin icon).
2. **Add:** PubSubClient (by Nick O'Leary).
3. Ensure **DHT sensor library for ESPx** is still installed.

---

## 💻 Step 3: The Connected Code
Replace your code with the version below. This includes the WiFi "Handshake" and the MQTT "Heartbeat" logic.
```cpp
#include <WiFi.h>
#include <PubSubClient.h>
#include "DHTesp.h"

// WiFi and MQTT Settings
const char* ssid = "Wokwi-GUEST"; // Wokwi's virtual gateway
const char* password = "";
const char* mqtt_server = "broker.hivemq.com";

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
  Serial.println("\n📡 Connecting to WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n✅ WiFi Connected!");
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("🔄 Attempting MQTT connection...");
    // Industry Best Practice: Use a unique Client ID
    if (client.connect("ESP32_Student_ID_99")) { 
      Serial.println("Connected to Broker!");
    } else {
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
  client.loop(); // Keeps the MQTT connection alive

  TempAndHumidity data = dhtSensor.getTempAndHumidity();
  String tempStr = String(data.temperature, 2);
  
  // Publish data to the cloud!
  Serial.println("🛰️ Publishing Telemetry: " + tempStr + "°C");
  client.publish("curriculum/iot/temp", tempStr.c_str());

  delay(5000); // Send data every 5 seconds
}
```

---

## 🧪 Step 4: Verification (The Cloud View)
> [!TIP]
> Pro-Tip: To keep this guide open while navigating to HiveMQ, Right-Click the link below and select "Open link in new tab."

1. Open the [HiveMQ Web Client[(https://www.hivemq.com/demos/websocket-client/)].
2. **Configure Connection:**
  * **Host:** broker.hivemq.com | Port: 8884 | SSL: ✅ Checked
  * **ClientID:** Click "Generate ID".
3. Click **Connect**. (The status light must turn Green).
4. **Subscribe:** Click Add New Topic Subscription and enter curriculum/iot/temp.
5. **Observe:** Adjust the Wokwi slider. Within 5 seconds, your data will appear on the HiveMQ dashboard!

---

## 🛠️ Troubleshooting
* **WiFi OK, but no Data?** Ensure you clicked **Connect** on the HiveMQ site before subscribing.
* **Failed, rc=-2?** This means the Client ID is already in use. Change "ESP32_Student_ID_99" in your code to something unique (like your name).
* **Case Sensitivity:** MQTT topics are exact. Curriculum/Iot is not the same as curriculum/iot.

---

## 🛰️ The "Post Office" Analogy
If you're wondering how a slider in one browser tab moves text in another, think of the HiveMQ Broker as a global Digital Post Office.
1. **The Publisher (Wokwi):** Your ESP32 drops off a letter (the temperature) addressed to a specific "P.O. Box" (the Topic).
2. **The Broker (HiveMQ Cloud):** It catches the letter and checks who is waiting for it.
3. **The Subscriber (Web Client):** Since you "Subscribed" to that P.O. Box, the Post Office delivers the letter to you immediately.

> [!TIP]
> **Why this is powerful:** This is the backbone of the **Internet of Things**. Next week, we will add a **Python Script** as a second subscriber to "catch" these letters and save them forever in a database!