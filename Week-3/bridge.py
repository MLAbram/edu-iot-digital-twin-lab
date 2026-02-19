import os
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
import psycopg2
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()

# --- TERMINAL INSTRUCTION ---
print("\n🚀 IoT Bridge is active. Listening for data...")
print("👉 Press Ctrl+C in this terminal to stop the Bridge.\n")

# Database Connection Logic
def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

# MQTT Broker Settings
MQTT_BROKER = "broker.hivemq.com"
MQTT_TOPIC = "edu/iot/temp"

def on_message(client, userdata, msg):
    try:
        # 1. Decode the payload from the broker
        temp_value = float(msg.payload.decode())
        print(f"📥 Telemetry Received: {temp_value}°C")
        
        # 2. Connect and Insert into the professional Schema
        conn = get_db_connection()
        cur = conn.cursor()
        
        # aud_insert_ts is handled automatically by the DB Default
        query = """
            INSERT INTO edu_iot_digital_twin_lab.sensor_data (temperature, unit) 
            VALUES (%s, 'C')
        """
        
        cur.execute(query, (temp_value,))
        conn.commit()
        
        cur.close()
        conn.close()
        print("✅ Record successfully committed to PostgreSQL.")
        
    except Exception as e:
        print(f"❌ Processing Error: {e}")

# Initialize MQTT Client with 2026 API standards
client = mqtt.Client(CallbackAPIVersion.VERSION2)
client.on_message = on_message

client.connect(MQTT_BROKER, 1883, 60)
client.subscribe(MQTT_TOPIC)

# Start the continuous listening loop
client.loop_forever()