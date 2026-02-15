# Week 1: The Virtual Edge & Local Logic 🌡️

In this first lab, you will build the "sensing" part of your Digital Twin. You will use a virtual ESP32 and a DHT22 sensor to monitor environmental conditions.

## 🎯 Learning Objectives
* Interface with a digital temperature and humidity sensor (DHT22).
* Write C++/Arduino logic to process sensor data.
* Implement "Edge Intelligence" by triggering an alert (LED) locally.

## 🛠️ Step 1: The Wokwi Circuit
1.  Go to [Wokwi.com](https://wokwi.com) and start a new **ESP32** project. If prompted for featured templates, select the **ESP32** starter template. 
2. Save as curriculum-iot-digital-twin-celsius-lab-week-1.
3.  **Add Components:** Click the **"+"** button and add:
    * **DHT22** (Temperature & Humidity Sensor)
    * **LED** (Red)
    * **Resistor** (Set to 220 Ohms)
4.  **Wiring:**
    * **DHT22:** dht1:VCC to **ESP32** esp:3V3 | dht1:GND to **ESP32** esp:GND.1 | dht1:SDA to **ESP32** esp:15.
    * **LED:** Long leg (Anode) led1:A to **ESP32** esp:D2 | Short leg (Cathode) led1:C to r1:1 of the Resistor | r1:2 from the Resistor to **ESP32** esp:GND.2.

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
```

---

## 🧪 Step 3: Testing
Click the Play button in Wokwi.

If prompted to install DHT sensor library for ESPx library, click the link to install.

Click on the DHT22 sensor while the simulation is running.

Use the slider to change the temperature.

Observe: Does the Red LED turn on when you go above 30°C? Check the Serial Monitor at the bottom to see the real-time data logs.

---

## 🌟 BONUS: Unit Conversion (Fahrenheit)
Now that you have the basic circuit working in Celsius, let’s adapt the project for a US-based environment. 

### 🎯 Learning Objective
* Perform mathematical data transformation at the "Edge."
* Understand the difference between metric sensor data and localized user requirements.

### 💻 Step 1: The Logic Update
In your code, we need to convert the raw Celsius data into Fahrenheit. Update your `loop()` function to include the conversion formula:

```cpp
void loop() {
  TempAndHumidity data = dhtSensor.getTempAndHumidity();
  
  // Convert Celsius to Fahrenheit using the library helper
  float tempF = dhtSensor.toFahrenheit(data.temperature);
  
  Serial.println("Temp: " + String(tempF, 2) + "°F");
  
  // Update your logic for Fahrenheit (e.g., 86°F is roughly 30°C)
  if (tempF > 86) {
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
  }

  delay(2000);
}
```

🧪 Step 2: Verification
Click Play in Wokwi.

Adjust the DHT22 slider.

Observe: Your Serial Monitor should now display temperatures in °F.

Confirm: Does the Red LED illuminate when the temperature crosses 86°F?

💡 Why this matters
In a professional Digital Twin setup, sensors often speak in one "language" (Metric), but the dashboard needs to speak another (Imperial). Handling this conversion on the ESP32 is called Edge Processing—it saves the central server from having to do the math later!