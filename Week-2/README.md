# Week 2: Machine-to-Machine (M2M) Networking 🌐

Last week, your ESP32 made decisions locally. This week, we connect it to the internet so it can report its data to the world.

## 🎯 Learning Objectives
* Connect the virtual ESP32 to a simulated WiFi network.
* Understand the **Publisher/Subscriber** model.
* Send live temperature data to a Public MQTT Broker.

## ⚖️ Step 1: Clone Work
1. Open curriculum-iot-digital-twin-celsius-lab-week-1. 
2. Make a copy by clicking on the down arrow next to the grayed out Save button. If your Save button is red, click to save first. Select the Save a copy options and name it: curriculum-iot-digital-twin-celsius-lab-week-2.

## 🛠️ Step 2: The Wokwi WiFi
Wokwi provides a built-in virtual gateway. You don't need to change your wiring from Week 1! We only need to update the library and the code.

## 📚 Step 3: Add the Library
1. In your Wokwi project, click the **Library Manager** tab (the bin icon).
2. Search for and add: **PubSubClient**.
3. Ensure **DHTesp** is still there from last week.

## 💻 Step 4: The Connected Code
Replace your code with this version. This includes the WiFi and MQTT "handshake" logic. 

*(Note: In Wokwi, the WiFi SSID is always "Wokwi-GUEST" with no password.)*

```cpp
#include <WiFi.h>
#include <PubSubClient.h>
#include "DHTesp.h"

// WiFi and MQTT Settings
const char* ssid = "Wokwi-GUEST";
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
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  TempAndHumidity data = dhtSensor.getTempAndHumidity();
  String tempStr = String(data.temperature, 2);
  
  // Publish data to the cloud!
  Serial.println("Publishing: " + tempStr);
  client.publish("university/iot/temp", tempStr.c_str());

  delay(5000); // Send data every 5 seconds
}
```

## 🧪 Step 5: Verification (The Cloud View)
To see your data leaving Wokwi and hitting the internet, follow these steps:

1.  Open the [HiveMQ Web Client](http://www.hivemq.com/demos/websocket-client/).
2.  Click the **Connect** button (Status should change to "Connected").
3.  Click **Add New Topic Subscription**.
4.  Enter the topic: `curriculum/iot/temp` and click **Subscribe**.
5.  **Observe:** Your Fahrenheit readings should start appearing in the "Messages" log every 5 seconds.

> [!TIP]
> **What to look for:** If you see numbers appearing, congratulations! You have successfully created a "Digital Twin" data stream. Your virtual device is now communicating with a global server.

---

## 🛠️ Troubleshooting (If it's not working)

If your Serial Monitor is showing "WiFi Connected" but you don't see data on the website, check these three things:

* **The Connection Button:** Ensure you clicked the **Connect** button on the HiveMQ website *before* subscribing to the topic. If you aren't connected to the broker, you won't see the messages.
* **The Library Manager:** Double-check that `PubSubClient` is listed in your Wokwi Library Manager. If the library is missing, the code cannot "speak" MQTT.
* **Topic Matching:** MQTT topics are case-sensitive. Ensure `curriculum/iot/temp` in your code perfectly matches what you typed into the HiveMQ subscription box.

> [!CAUTION]
> **Client ID Conflict:** MQTT only allows one connection per "Client ID." If the Serial Monitor says "Failed, rc=-2", it might mean someone else is using the ID `RoadTrip_Student_Device`. Try changing that name in your code to something unique (like your name) and restart the simulation.