import os
import json
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
import psycopg2
from dotenv import load_dotenv

# Load variables
load_dotenv()

# --- CONSTANTS ---
MQTT_BROKER = "broker.hivemq.com"
MQTT_TOPIC = "curriculum/iot/smart_data"  # New topic for JSON data

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

def on_message(client, userdata, msg):
    try:
        # 1. Parse the incoming JSON string
        payload_str = msg.payload.decode()
        data = json.loads(payload_str)
        print(f"📥 Received JSON: {data}")

        # 2. Insert into the NEW 'smart_sensor_data' table
        conn = get_db_connection()
        cur = conn.cursor()
        
        # We pass the 'data' dictionary directly; psycopg2 handles the JSON conversion for JSONB
        query = """
            INSERT INTO curriculum_iot_digital_twin_lab.smart_sensor_data (payload) 
            VALUES (%s)
        """
        cur.execute(query, (json.dumps(data),))
        
        conn.commit()
        cur.close()
        conn.close()
        print("✅ JSON successfully stored in JSONB column.")

    except json.JSONDecodeError:
        print("❌ Error: Received message was not valid JSON")
    except Exception as e:
        print(f"❌ Error: {e}")

# --- INITIALIZATION ---
client = mqtt.Client(CallbackAPIVersion.VERSION2)
client.on_message = on_message

client.connect(MQTT_BROKER, 1883, 60)
client.subscribe(MQTT_TOPIC)

print(f"🚀 Smart Bridge active. Listening for JSON on: {MQTT_TOPIC}")
client.loop_forever()