# Week 3: The Data Bridge 🌉

Until now, your data has been "volatile"—as soon as you close the HiveMQ website, the history is gone. Today, we build a Python bridge to save that data forever in a **PostgreSQL** database.

## 🎯 Learning Objectives
* Write a Python script to subscribe to MQTT data.
* Connect Python to a local PostgreSQL database.
* Store "Real-Time" telemetry data for future analysis.

## 🛠️ Step 1: Database Setup
Before running the code, you need a "bucket" to hold the data. Open **pgAdmin 4** or your terminal and run this SQL command:

```sql
-- Run this in pgAdmin or psql
CREATE DATABASE curriculum;

-- Connect to the curriculum database, then run:
CREATE SCHEMA curriculum_iot_digital_twin_lab;

CREATE TABLE curriculum_iot_digital_twin_lab.sensor_data (
    id SERIAL PRIMARY KEY,
    temperature FLOAT,
    unit VARCHAR(1),
    aud_insert_ts TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP NOT NULL
);
```

## Step 2: The Environment Setup
You should never save sensitive values in your code that could be open to the public when saving on GitHub, for example. We will use python-dotenv to read the .env file where you will have this sensitive data.

From the terminal console, type the following command to install paho-mqtt, psycopg2, and python-dotenv:

> pip install paho-mqtt psycopg2 python-dotenv

Create a file in Week-3 folder titled .env. Copy and paste the below: DB_ values and update only the DB_PASS to your password. Save the file. 

DB_NAME=curriculum
DB_USER=postgres
DB_PASS=your_secret_password
DB_HOST=localhost
DB_PORT=5432

## 📦 Step 3: Install Python Libraries
You will need two libraries: paho-mqtt (to talk to the broker) and psycopg2 (to talk to PostgreSQL). Run this in your VS Code terminal:

Bash
pip install paho-mqtt psycopg2

## 🐍 Step 4: The Python Bridge Code
> [!TIP]
> **Warning** Reminder to **never** push your actual database passwords to GitHub! 

Create a file named bridge.py in your Week-3 folder. This script acts like the "Indoor Thermometer Display" from our analogy, but instead of showing the data, it saves it.

import os
import paho.mqtt.client as mqtt
import psycopg2
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Database Connection Logic
def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

# MQTT Settings
MQTT_BROKER = "broker.hivemq.com"
MQTT_TOPIC = "curriculum/iot/temp"

def on_message(client, userdata, msg):
    try:
      temp_value = float(msg.payload.decode())
      print(f"📥 Received: {temp_value}°F")

      # Save to PostgreSQL using the specific Schema
      conn = get_db_connection()
      cur = conn.cursor()
      query = "INSERT INTO curriculum_iot_digital_twin_lab.sensor_data (temperature, unit) VALUES (%s, 'F')"
      cur.execute(query, (temp_value,))
      conn.commit()
      cur.close()
      conn.close()
      except Exception as e:
      print(f"❌ Error: {e}")

client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER, 1883, 60)
client.subscribe(MQTT_TOPIC)

print(f"🚀 Bridge is active. Listening for topic: {MQTT_TOPIC}")
client.loop_forever()

## 🧪 Step 5: Verification
Start your Wokwi Simulation from Week 2.

Run your Python script: python bridge.py.

Move the slider in Wokwi.

Check your database: SELECT * FROM sensor_data;.

---
💡 Why the (6)?
We use timestamp(6) to capture data down to the microsecond. In IoT, devices can send data very quickly. If we used a standard timestamp, two readings might look like they happened at the exact same time. Precision matters when you are building a "Digital Twin" of a real-world system!
