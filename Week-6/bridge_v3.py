import os
import json
import smtplib
from email.message import EmailMessage
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
import psycopg2
from dotenv import load_dotenv

# Load our credentials
load_dotenv()

# --- SETTINGS ---
MQTT_BROKER = "broker.hivemq.com"
MQTT_TOPIC = "curriculum/iot/commands/student01" 
ALARM_THRESHOLD = 30.0  # Matches our ESP32 LED setting

def send_email_alert(temp):
    """
    Sends an emergency email when the threshold is breached.
    """
    msg = EmailMessage()
    msg.set_content(f"🚨 ALERT: Your Digital Twin detected a temperature of {temp}°C, which exceeds your {ALARM_THRESHOLD}°C limit!")
    msg['Subject'] = f"IOT CRITICAL ALERT: {temp}°C"
    msg['From'] = os.getenv("EMAIL_SENDER")
    msg['To'] = os.getenv("EMAIL_RECEIVER")

    try:
        # Connect to Gmail's secure server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_PASSWORD"))
            smtp.send_message(msg)
        print("📧 Email alert sent successfully!")
    except Exception as e:
        print(f"❌ Email failed to send: {e}")

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
        # 1. Decode and Parse
        payload_str = msg.payload.decode()
        data = json.loads(payload_str)
        print(f"📥 Received: {data}")

        # 2. Store in the SMART table
        conn = get_db_connection()
        cur = conn.cursor()
        query = "INSERT INTO curriculum_iot_digital_twin_lab.smart_sensor_data (payload) VALUES (%s)"
        cur.execute(query, (json.dumps(data),))
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Stored in Database.")

        # 3. Intelligence: Check if we need to send an email
        # We use .get() to safely check the 'temp' key in the JSON
        current_temp = data.get("temp", 0)
        
        if current_temp > ALARM_THRESHOLD:
            print(f"⚠️ THRESHOLD BREACHED: {current_temp}°C. Sending email...")
            send_email_alert(current_temp)

    except Exception as e:
        print(f"❌ Error processing message: {e}")

# --- START THE BRIDGE ---
client = mqtt.Client(CallbackAPIVersion.VERSION2)
client.on_message = on_message
client.connect(MQTT_BROKER, 1883, 60)
client.subscribe(MQTT_TOPIC)

print(f"🚀 Week 5 Bridge & Alerter is LIVE on {MQTT_TOPIC}")
print("Press Ctrl+C to stop the bridge.")
client.loop_forever()