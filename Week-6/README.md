## Week 6: The "Command & Control" Logic
To achieve Bi-Directional Control, we have to flip the script. Until now, the ESP32 has been a "Talker" (Publisher) and the Bridge has been a "Listener" (Subscriber). Now, the ESP32 needs to do both.

Step 1: The Real-World Scenario
We’ll frame this as the "Remote Override" system.

The Problem: Your "Digital Twin" detects a high-temp alarm. You’ve checked your dashboard and realize it’s a sensor glitch or a controlled burn. You need to "silence" the alarm remotely so the red LED stops flashing on-site.

Step 2: The ESP32 "Listener" Update
We need to add a Callback Function to your sketch.ino. This is like giving the ESP32 a "mailing address" where it can receive instructions.

Here is the updated code. Notice the new COMMAND_TOPIC and the logic inside the callback and reconnect functions. Here is the logic to add to your Week 6 sketch.ino:
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
// Change 'student01' to your unique name or ID
const char* DATA_TOPIC = "curriculum/iot/temp/student01";
const char* COMMAND_TOPIC = "curriculum/iot/commands/student01";

const int LED_PIN = 2;
float lastTemp = 0;
float threshold = 0.5;
float ALARM_THRESHOLD = 30.0;
bool remoteOverride = false; // New flag to track remote silences

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
  
  // LOGIC: Re-enable the alarm system
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
  client.loop(); // This line is CRITICAL—it checks for incoming callback messages!

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

---

**The "Security & Logic" Highlights:**
* **Unique Namespaces:** Using student01 in the topic path is the first step toward Multi-Tenancy (supporting many users on one broker).
* **The remoteOverride Flag:** This is a professional way to handle state. It prevents the loop() from immediately turning the LED back on as soon as you turn it off.
* **client.loop():** I’ve added a comment here because many students forget this. Without this line, the callback() will never trigger.

**The "Out-of-the-Box" Challenge:**
* _"We are using simple text like 'RESET_ALARM' for our commands. How could we use JSON for commands to change the ALARM_THRESHOLD variable remotely?"_

---

## 🎮 Step 2: Building the Control Center (Bi-Directional)
In this step, we upgrade our Streamlit Dashboard to include a "Remote Reset" button. This button will send a message backward through the MQTT broker to your ESP32.

The "Control" Code for dashboard_v3.py
Add this block to your Streamlit script. This creates a button that, when clicked, publishes the RESET_ALARM command to your unique namespace.
```python
# --- REMOTE CONTROL SECTION ---
st.sidebar.header("🕹️ Remote Actuation")

# 1. Define the Command Topic (Must match your ESP32 exactly!)
COMMAND_TOPIC = "curriculum/iot/commands/student01"

if st.sidebar.button("🚨 Reset Local Alarm"):
    # We use our existing MQTT client to publish a command
    # This is "Actuation" — controlling physical hardware from the web!
    client.publish(COMMAND_TOPIC, "RESET_ALARM")
    st.sidebar.success("Command Sent: Resetting LED...")
    
if st.sidebar.button("🟢 Re-enable System"):
    client.publish(COMMAND_TOPIC, "ENABLE_ALARM")
    st.sidebar.info("Command Sent: System Armed.")
```

## 🛡️ Step 3: Security & Best Practices (The "Professional" Layer)
Most IoT tutorials ignore security. In this lab, we are moving toward Production-Ready standards.

1. **Topic Isolation (Namespace Security)**
In Week 2, we used a shared topic. In a real-world company, this would be a disaster—every employee would be controlling every machine.

* **The Solution:** We now use .../student01. This ensures that your "Command" only reaches your specific device.

2. **The .gitignore Shield**
You have sensitive data in your .env file (Database passwords, Email credentials).

* **The Task:** Ensure your .gitignore file includes the line .env.
* **The Consequence:** If you push your .env to GitHub, bots will find your credentials in seconds and potentially compromise your database or email account.

3. **Least Privilege Principle**
When you connected your Python bridge to PostgreSQL, did you use a "Superuser" account?

* **The Lesson:** In production, we create a specific user who only has permission to INSERT into one specific table. If that account is compromised, the rest of your database remains safe.

## 🎨 Step 4: The "Out-of-the-Box" Creative Challenge
You have the foundation. Now, it’s time to make this system your own. To graduate from this course, your Capstone Digital Twin must include at least one of the following creative "hacks":
* **Custom Logic:** Change the ALARM_THRESHOLD remotely by sending a JSON command from the dashboard (e.g., {"new_limit": 35.5}).
* **Visual Flair:** Use Streamlit "columns" and "metric cards" to create a dashboard that looks like a SpaceX control room.
* **External Alert:** Connect a Discord Webhook so that when the temperature stays high for more than 1 minute, your entire team gets a message on their phones.

**Final Validation Sequence**
* **Flash:** Upload the new "Listener" code to Wokwi.
* **Launch:** Run your bridge_v2.py (to keep the database recording).
* **Control:** Run streamlit run dashboard_v3.py.

**The Test:**
* Crank the Wokwi slider to 40°C. The Red LED turns on.
* Go to your Dashboard and click "Reset Local Alarm".
* Did the LED turn off in Wokwi? If so, you have achieved Bi-Directional Control!