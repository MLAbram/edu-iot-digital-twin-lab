## 🌡️ Week 1: The Virtual Edge & Local Logic
In this first lab, you will build the Sensing Layer of your Digital Twin. You will use a virtual ESP32 and a DHT22 sensor to monitor environmental conditions and make autonomous decisions at the "Edge."

---

## 🎯 Learning Objectives
* **Hardware Interfacing:** Connect a digital DHT22 sensor to a microcontroller.
* **Edge Intelligence:** Write C++ logic to trigger a local alarm (LED).
* **Data Transformation:** Convert raw sensor data into human-readable telemetry.

---

## 🛠️ Step 1: The Wokwi Circuit
> [!TIP]
> **Pro-Tip:** To keep this guide open while building, **Right-Click** the links below and select "**Open link in new tab**."

1.  Go to [Wokwi.com](https://wokwi.com) and start a new **ESP32** project. If prompted for featured templates, select the **ESP32** starter template. 
2. **Save as** edu-iot-digital-twin-celsius-lab-week-1.
3.  **Add Components:** Click the "+" button and add a DHT22, a Red LED, and a Resistor (set to 220 Ohms).
4. **Wiring Guide:** Follow the table below to connect your components.

| Component | From Pin | To ESP32 Pin |
| :--- | :--- | :--- |
| **DHT22** | VCC | 3V3 |
| **DHT22** | SDA | 15 |
| **DHT22** | GND | GND |
| **Red LED** | Anode (Long Leg) | D2 |
| **Red LED** | Cathode (Short) | (Connect to Resistor) |
| **Resistor** | End of Resistor | GND |

---

## 📚 Step 2: Library Management
Microcontrollers need "drivers" to talk to sensors.
1. Click the **Library Manager** tab (the trash bin icon).
2. **Search for and add:** DHT sensor library for ESPx.

---

## 💻 Step 3: The Edge Logic (sketch.ino)
Copy the code below into your Wokwi editor. This script processes environmental data and triggers a Critical Alert if the temperature exceeds 30°C.
```cpp
#include "DHTesp.h"

const int DHT_PIN = 15;
const int LED_PIN = 2; // Most ESP32s have an on-board blue LED here too!
DHTesp dhtSensor;

void setup() {
  Serial.begin(115200);
  dhtSensor.setup(DHT_PIN, DHTesp::DHT22);
  pinMode(LED_PIN, OUTPUT);
  Serial.println("🛰️ Digital Twin Sensing Layer: Online");
}

void loop() {
  TempAndHumidity data = dhtSensor.getTempAndHumidity();
  
  // Output telemetry to the Serial Monitor
  Serial.print("Current Temp: " + String(data.temperature, 2) + "°C | ");
  Serial.println("Humidity: " + String(data.humidity, 1) + "%");
  
  // --- Edge Intelligence: Autonomous Decision ---
  if (data.temperature > 30.0) {
    digitalWrite(LED_PIN, HIGH); // Alarm ON
    Serial.println("⚠️ WARNING: Temperature exceeds safety threshold!");
  } else {
    digitalWrite(LED_PIN, LOW);  // Alarm OFF
  }

  delay(2000); // Wait 2 seconds between readings
}
```

---

## 🧪 Step 4: Testing & Verification
1. Click the **Play** button.
2. Click on the **DHT22 sensor** while the simulation is running.
3. **Adjust the Slider:** Change the temperature.
4. **Observe:** Does the Red LED turn on when you cross 30°C? Check the Serial Monitor at the bottom for the data logs.

---

## 🌟 BONUS: The "Fahrenheit" Pivot
In a global market, your Digital Twin must be adaptable. Let's modify the edge logic for an Imperial-unit environment.

1. **Clone the Lab**
Click the **down arrow** next to the Save button and select **Save a copy**. Name it: edu-iot-digital-twin-fahrenheit-lab-week-1.
2. **Update the Transformation Logic**
Replace your loop() function with this code, which uses the library's built-in conversion helper:
```cpp
void loop() {
  TempAndHumidity data = dhtSensor.getTempAndHumidity();
  
  // Convert Celsius to Fahrenheit at the Edge
  float tempF = dhtSensor.toFahrenheit(data.temperature);
  
  Serial.println("Telemetry: " + String(tempF, 2) + "°F");
  
  // Threshold Pivot: 86°F is the equivalent of 30°C
  if (tempF > 86.0) {
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
  }

  delay(2000);
}
```

## 💡 Why this matters
In professional IoT, we don't send every tiny detail to the cloud. By handling the temperature alert locally (on the ESP32), we ensure the alarm works even if the WiFi goes down. This is called **Edge Computing**.

**Data Transformation**
Sensors usually speak in Metric. Handling unit conversion on the device rather than the server is an efficient way to save "Cloud Computing" costs. You are already thinking like a **Tech Architect**!