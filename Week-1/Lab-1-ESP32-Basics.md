# Week 1: The Virtual Edge & Local Logic 🌡️

In this first lab, you will build the "sensing" part of your Digital Twin. You will use a virtual ESP32 and a DHT22 sensor to monitor environmental conditions.

## 🎯 Learning Objectives
* Interface with a digital temperature and humidity sensor (DHT22).
* Write C++/Arduino logic to process sensor data.
* Implement "Edge Intelligence" by triggering an alert (LED) locally.

## 🛠️ Step 1: The Wokwi Circuit
1.  Go to [Wokwi.com](https://wokwi.com) and start a new **ESP32** project.
2.  **Add Components:** Click the **"+"** button and add:
    * **DHT22** (Temperature & Humidity Sensor)
    * **LED** (Red)
    * **Resistor** (Set to 220 Ohms)
3.  **Wiring:**
    * **DHT22:** VCC to ESP32 **3V3** | GND to ESP32 **GND** | SDA to ESP32 **GPIO 15**.
    * **LED:** Long leg (Anode) to ESP32 **GPIO 2** | Short leg (Cathode) to Resistor | Resistor to **GND**.

## 💻 Step 2: The Code
Copy the code below into the `sketch.ino` tab in Wokwi. This code reads the temperature and turns on the "Critical Alert" LED if the temperature exceeds 30°C.

```cpp
#include "DHTesp.h"

const int DHT_PIN = 15;
const int LED_PIN = 2;
DHTesp dhtSensor;

void setup() {
  Serial.begin(115200);
  dhtSensor.setup(DHT_PIN, DHTesp::DHT22);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  TempAndHumidity  data = dhtSensor.getTempAndHumidity();
  Serial.println("Temp: " + String(data.temperature, 2) + "°C");
  
  // Local Edge Logic
  if (data.temperature > 30) {
    digitalWrite(LED_PIN, HIGH); // Alarm ON
  } else {
    digitalWrite(LED_PIN, LOW);  // Alarm OFF
  }

  delay(2000); // Wait 2 seconds between readings
}