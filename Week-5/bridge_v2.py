import os
import json
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
import psycopg2
from dotenv import load_dotenv

# --- SETUP: Load our secret credentials (database passwords, etc.) from the .env file ---
load_dotenv()

# --- CONSTANTS: These are our "Address" settings for the MQTT Broker ---
MQTT_BROKER = "broker.hivemq.com"
MQTT_TOPIC = "curriculum/iot/smart_data"  # This must match the topic used in the ESP32 code

def get_db_connection():
    """
    This function acts as our 'Key' to the database. 
    It pulls the credentials we saved in .env to open a secure connection.
    """
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

def on_message(client, userdata, msg):
    """
    This is the 'Brain' of the script. It runs automatically every time 
    a new message arrives on our MQTT topic.
    """
    try:
        # 1. DECODING: The message arrives as 'bytes' (computer code). 
        # We decode it into a human-readable string first.
        payload_str = msg.payload.decode()
        
        # 2. PARSING: We take that string and turn it into a Python Dictionary (JSON).
        # This allows us to access specific pieces like data['temp'] easily.
        data = json.loads(payload_str)
        print(f"📥 Received JSON: {data}")

        # 3. CONNECTING: Open the door to our PostgreSQL database.
        conn = get_db_connection()
        cur = conn.cursor()
        
        # 4. INSERTING: We prepare our SQL command.
        # We use the 'JSONB' format in PostgreSQL, which is like a digital filing cabinet
        # that can hold any size or shape of JSON data we throw at it.
        query = """
            INSERT INTO curriculum_iot_digital_twin_lab.smart_sensor_data (payload) 
            VALUES (%s)
        """
        
        # We 'dump' the dictionary back into a JSON string format for the database to store.
        cur.execute(query, (json.dumps(data),))
        
        # 5. COMMITTING: Save the changes permanently and close the connection.
        conn.commit()
        cur.close()
        conn.close()
        print("✅ JSON successfully stored in JSONB column.")

    except json.JSONDecodeError:
        # This runs if the message sent by the ESP32 wasn't formatted correctly.
        print("❌ Error: Received message was not valid JSON. Check your ESP32 code!")
    except Exception as e:
        # This catches any other errors, like a database connection failure.
        print(f"❌ Error: {e}")

# --- INITIALIZATION: Setting up the MQTT 'Listener' ---

# Create a new MQTT client using the latest version of the library
client = mqtt.Client(CallbackAPIVersion.VERSION2)

# Tell the client which function to run when a message arrives
client.on_message = on_message

# Connect to the public HiveMQ broker on port 1883
client.connect(MQTT_BROKER, 1883, 60)

# Tell the broker we only want to hear messages sent to our specific 'smart_data' topic
client.subscribe(MQTT_TOPIC)

# Keep the script running forever so it doesn't miss any messages
print(f"🚀 Smart Bridge active. Listening for JSON on: {MQTT_TOPIC}")
print("Press Ctrl+C to stop the bridge.")
client.loop_forever()