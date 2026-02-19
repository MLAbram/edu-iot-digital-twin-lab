## 🛰️ Week 6: The "Command & Control" Capstone
To achieve Bi-Directional Control, we have to flip the script. Until now, the ESP32 has been a "Talker" (Publisher) and the Bridge has been a "Listener" (Subscriber). Now, your Digital Twin will do both.

---

## 🎯 Learning Objectives
* **Bi-Directional Communication:** Transform the ESP32 from a "Sensor" into an "Actuator" that responds to web commands.
* **State Management:** Implement flags to handle complex logic overrides between local sensing and remote control.
* **Multi-Tenant Security:** Apply unique **Namespaces** to prevent cross-device topic hijacking.
* **Production Hardening:** Secure your "secrets" using environment shields and the Principle of Least Privilege.

---

## ⚖️ Step 1: Clone Wokwi Work
> [!TIP]
> Pro-Tip: To keep this guide open while watching the videos, **Right-Click** the links below and select "**Open link in new tab**" (or use Ctrl/Cmd + Click).

1. **Website:** [Wokwi](https://wokwi.com/)
2. Open your **Week 5** project (edu-iot-digital-twin-celsius-lab-week-5).
3. Make a copy by clicking on the **down arrow** next to the grayed-out Save button. (If your Save button is red, click to save first).
4. Select **Save a copy** and name it: edu-iot-digital-twin-celsius-lab-week-6.

---

## 🏢 Step 2: The Real-World Scenario
We’ll frame this as the "Remote Override" system.

* **The Problem:** Your "Digital Twin" detects a high-temp alarm. You’ve checked your dashboard and realize it’s a sensor glitch or a controlled maintenance event.
* **The Solution:** You need to "silence" the alarm remotely so the red LED stops flashing on-site without physically traveling to the hardware.

---

## 📡 Step 3: The ESP32 "Listener" Update
We need to add a **Callback** Function to your sketch.ino. This is like giving the ESP32 a "mailing address" where it can receive instructions from the web.

Update your Week 6 sketch.ino with the following logic:
```cpp
// --- LIBRARIES ---
#include <WiFi.h>
#include <PubSubClient.h>
#include "DHTesp.h"
#include <ArduinoJson.h>

// --- SETTINGS & SECURITY ---
const char* ssid = "Wokwi-GUEST";
const char* password = "";
const char* mqtt_server = "broker.hivemq.com";

// UNIQUE NAMESPACE: In the real world, this prevents "Topic Hijacking"
const char* DATA_TOPIC = "edu/iot/temp/student01";
const char* COMMAND_TOPIC = "edu/iot/commands/student01";

const int LED_PIN = 2;
float lastTemp = 0;
float threshold = 0.5;
float ALARM_THRESHOLD = 30.0;
bool remoteOverride = false;  // New flag to track remote silences

WiFiClient espClient;
PubSubClient client(espClient);
DHTesp dht;

// --- 1. THE CALLBACK: The "Inbox" for our ESP32 ---
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("📩 Incoming Command on [");
  Serial.print(topic);
  Serial.println("]");

  // Convert the raw bytes into a readable string
  String message = "";
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  Serial.println("Message: " + message);

  // LOGIC: If the dashboard sends "RESET", we silence the alarm locally
  if (message == "RESET_ALARM") {
    remoteOverride = true; 
    digitalWrite(LED_PIN, LOW);
    Serial.println("🛑 REMOTE OVERRIDE: Alarm silenced by Dashboard.");
  }
  
  if (message == "ENABLE_ALARM") {
    remoteOverride = false;
    Serial.println("🟢 ALARM SYSTEM: Re-enabled.");
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  
  // --- 2. THE LISTENER SETUP ---
  // We must tell the MQTT client which function to run when a message arrives
  client.setCallback(callback);
  dht.setup(15, DHTesp::DHT22);
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
    // We give the client a unique name based on our topic for security
    if (client.connect("ESP32_Student_01")) {
      Serial.println("connected");
      // --- 3. THE SUBSCRIPTION ---
      // Once connected, we MUST subscribe to our command topic to hear the dashboard
      client.subscribe(COMMAND_TOPIC);
      Serial.println("📡 Subscribed to Command Topic");
    } else {
      delay(5000);
    }
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop(); // CRITICAL: This checks for incoming messages!

  float currentTemp = dht.getTemperature();
  
  // --- Local Alarm Logic (Modified with Remote Override) ---
  if (currentTemp > ALARM_THRESHOLD && !remoteOverride) { 
    digitalWrite(LED_PIN, HIGH); 
  } else if (currentTemp <= ALARM_THRESHOLD) {
    // Auto-reset the override if the temperature drops back to safe levels
    remoteOverride = false;
    digitalWrite(LED_PIN, LOW);
  }

  // --- Report by Exception Logic ---
  if (abs(currentTemp - lastTemp) >= threshold) {
    StaticJsonDocument<200> doc;
    doc["temp"] = currentTemp;
    doc["hum"] = dht.getHumidity();
    doc["status"] = (remoteOverride) ? "SILENCED" : "ACTIVE";

    char buffer[256];
    serializeJson(doc, buffer);
    client.publish(DATA_TOPIC, buffer);
    lastTemp = currentTemp;
    Serial.println("📡 Smart Data Sent.");
  }
  delay(2000); 
}
```

##💡 Logic Highlights
Unique Namespaces: Using /student01 in the topic path is the first step toward Multi-Tenancy.
* **The remoteOverride Flag:** This state-management approach prevents the loop() from immediately turning the LED back on after a reset.
* **client.loop():** Without this line, the callback() will never trigger. It is the "heartbeat" of your inbound commands.

---

## 🎮 Step 4: Building the Control Center (Bi-Directional)
We now upgrade our Streamlit Dashboard to include "Remote Actuation" buttons.

This block of code was added to your Streamlit script. This creates a button that, when clicked, publishes the RESET_ALARM command to your unique namespace.
```python
import paho.mqtt.client as mqtt 
from paho.mqtt.enums import CallbackAPIVersion 

# --- NEW: MQTT SETUP FOR COMMANDS ---
client = mqtt.Client(CallbackAPIVersion.VERSION2)
client.connect("broker.hivemq.com", 1883, 60)

# --- REMOTE CONTROL SECTION (In the Sidebar) ---
st.sidebar.header("🕹️ Remote Actuation")

COMMAND_TOPIC = "edu/iot/commands/student01"

if st.sidebar.button("🚨 Reset Local Alarm"):
    # This sends a command BACK to the physical hardware!
    client.publish(COMMAND_TOPIC, "RESET_ALARM")
    st.sidebar.success("Command Sent: Resetting LED...")
    
if st.sidebar.button("🟢 Re-enable System"):
    client.publish(COMMAND_TOPIC, "ENABLE_ALARM")
    st.sidebar.info("Command Sent: System Armed.")
```

---

## 🛡️ Step 5: Security & Best Practices
Most IoT tutorials ignore security. Professional IoT requires moving beyond "hobbyist" habits toward **Production-Ready** standards.

1. **Topic Isolation:** By using unique namespaces (.../student01), we prevent "Topic Hijacking" where one user accidentally controls another's device.
2. **The .gitignore Shield:** Ensure your .gitignore includes .env. Pushing database credentials to GitHub allows bots to compromise your system in seconds.
3. **Least Privilege:** In production, your database user should only have INSERT and SELECT rights, never DROP TABLE or Superuser access.

---

## 🎨 Step 6: The "Out-of-the-Box" Challenge
To graduate, your Capstone Digital Twin must include at least one of the following creative "hacks":
* **Custom Logic:** Send a JSON command to change the ALARM_THRESHOLD variable remotely.
* **Visual Flair:** Use Streamlit columns and metric cards to create a professional Telemetry UI.
* **External Alert:** Connect a Discord Webhook to notify a team when a breach lasts longer than 60 seconds.

---

## 🏁 The "Moment of Truth" Testing Sequence
1. **Terminal 1:** Run your Bridge (python bridge_v2.py).
2. **Terminal 2:** Run your Dashboard (streamlit run dashboard_v3.py).
3. **Wokwi:** Start the simulation and slide the temperature to **35°C+**.

**The Action:**
* Wait for the **Red LED** to turn on in Wokwi.
* Click "**Reset Local Alarm**" in your Streamlit Sidebar.
* Watch the **Wokwi Serial Monitor**. If it says 🛑 REMOTE OVERRIDE and the LED turns off, you have successfully closed the loop!

---

## 🎓 Graduation: Capstone Complete! 🛰️
Congratulations! You have transitioned from a "Passive Observer" to an "**Active Controller**."

**Final Architecture Review:**
* **Edge Intelligence:** Using "Report by Exception" to save bandwidth.
* **Smart Data:** Using JSONB to future-proof your storage.
* **Remote Actuation:** Implementing overrides to control hardware globally.
* **Production Security:** Moving toward Namespace Isolation and Credential Management.