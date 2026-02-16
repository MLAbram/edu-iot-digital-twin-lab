# Week 3: The Data Bridge 🌉

Until now, your data has been "volatile"—as soon as you close the HiveMQ website, the history is gone. This week, we build a Python bridge to capture that data and save it permanently into a **PostgreSQL** database.

## 🎯 Learning Objectives
* Write a Python script to subscribe to MQTT data.
* Use environment variables (.env) to protect database credentials.
* Store telemetry data with microsecond precision in a structured schema.

## 🛠️ Step 1: Database & Schema Setup
Before running the code, we need to create a professional data structure. Open **pgAdmin 4** or your terminal and run the following commands:

```sql
-- 1. Create the central database
CREATE DATABASE curriculum;

-- 2. Connect to the 'curriculum' database, then create the schema
CREATE SCHEMA curriculum_iot_digital_twin_lab;

-- 3. Create the table with audit-ready timestamps
CREATE TABLE curriculum_iot_digital_twin_lab.sensor_data (
    id SERIAL PRIMARY KEY,
    temperature FLOAT,
    unit VARCHAR(1),
    aud_insert_ts TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP NOT NULL
);
```

## 📦 Step 2: Environment & Libraries
> [!TIP]
> **Did you receive error: externally-managed-environment** when executing pip install paho-mqtt psycopg2 python-dotenv? This error is actually a "safety feature" of modern Linux distributions. It prevents pip from accidentally breaking the system-level Python that your OS relies on to run. The "Best Practice" solution here is to use a Virtual Environment (venv). This creates an isolated "bubble" specifically for your Week 3 project, so you can install paho-mqtt and psycopg2 without touching the rest of your system.
>
>To keep our project secure and functional, we need to install the necessary tools. You should never save sensitive values in your code that could be open to the public when saving on GitHub, for example. We will use python-dotenv to read the .env file where you will have this sensitive data.
>
>**Step 1:** From the terminal console, type the following command to install paho-mqtt, psycopg2, and python-dotenv:
>```
>sudo apt install python3-venv
>```
>
>**Step 2:** Create your environment
>```
>python3 -m venv .venv
>```
>If you would like a different environment name, modify .venv.
>
>**Step 3:** Activate it
>```
>source .venv/bin/activate
>```
>(You should now see (.venv) appear at the beginning of your terminal prompt!)
>
>**Step 4:** Now install your libraries
>```
>pip install paho-mqtt psycopg2 python-dotenv

pip install paho-mqtt psycopg2 python-dotenv

Create a file in Week-3 folder titled .env. Copy and paste the below: DB_ values and update only the DB_PASS to your password. Save the file. 
```
DB_NAME=curriculum
DB_USER=postgres
DB_PASS=your_secret_password
DB_HOST=localhost
DB_PORT=5432
```
Security Check: Ensure your .gitignore file includes .env so you don't accidentally push your password to GitHub!

## 🐍 Step 3: The Python Bridge Code
Create a file named bridge.py in your Week-3 folder. This script acts as the "Subscriber" that listens to the broker and writes to your database.

```Python
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
        # Decode the temperature from the broker
        temp_value = float(msg.payload.decode())
        print(f"📥 Received: {temp_value}°F")
        
        # Connect and Insert into the specific Schema
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Note: aud_insert_ts is handled automatically by PostgreSQL
        query = """
            INSERT INTO curriculum_iot_digital_twin_lab.sensor_data (temperature, unit) 
            VALUES (%s, 'F')
        """
        
        cur.execute(query, (temp_value,))
        conn.commit()
        
        cur.close()
        conn.close()
        print("✅ Data successfully saved to PostgreSQL.")
        
    except Exception as e:
        print(f"❌ Error processing message: {e}")

# Initialize MQTT Client
client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER, 1883, 60)
client.subscribe(MQTT_TOPIC)

print(f"🚀 Bridge is active. Listening for topic: {MQTT_TOPIC}")
client.loop_forever()
```

## 🧪 Step 4: Verification
Start your [Wokwi](https://wokwi.com/) Simulation (from Week 2).

Run your Python script in VS Code: python bridge.py.

Move the slider in Wokwi.

Go to pgAdmin and run:
SELECT * FROM curriculum_iot_digital_twin_lab.sensor_data;

## 💡 Why This Matters
**Data Persistence**
In the real world, a dashboard only shows you what is happening now. By building this bridge, you are creating a historical record. This allows an entrepreneur to look back at trends, such as: "How hot did the RV get every day last July?"

**Microsecond Precision**
We used timestamp(6) for our aud_insert_ts field. In high-speed IoT environments, multiple sensors might report data at almost the exact same time. Standard seconds aren't enough; we need that microsecond precision to ensure our "Digital Twin" accurately reflects the sequence of events.

**Professional Security**
By using .env files, you are practicing Credential Management. Hard-coding passwords into your scripts is a major security risk. Learning to separate your "secrets" from your "code" is a requirement for any professional developer or tech entrepreneur.