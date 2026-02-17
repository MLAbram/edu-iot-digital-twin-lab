import os
import psycopg2
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# Load credentials
load_dotenv()

# --- CONFIGURATION ---
THRESHOLD_TEMP = 70.0  # Alert if temp is above this

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

def send_email_alert(temp):
    msg = EmailMessage()
    # Units restored to °C per your design
    msg.set_content(f"🚨 ALERT: Your IoT Digital Twin has detected a high temperature of {temp}°C!")
    msg['Subject'] = f"CRITICAL HEAT ALERT: {temp}°C"
    msg['From'] = os.getenv("EMAIL_SENDER")
    msg['To'] = os.getenv("EMAIL_RECEIVER")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_PASSWORD"))
            smtp.send_message(msg)
        print("📧 Email alert sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def run_analytics():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # 1. FETCH AGGREGATES
        query_stats = """
            SELECT 
                ROUND(AVG(temperature)::numeric, 2) as avg_temp,
                MAX(temperature) as max_temp,
                MIN(temperature) as min_temp,
                COUNT(*) as total_readings
            FROM curriculum_iot_digital_twin_lab.sensor_data
            WHERE aud_insert_ts > NOW() - INTERVAL '24 hours';
        """
        cur.execute(query_stats)
        row = cur.fetchone()
        
        # Logic fix: ensures the script doesn't crash if the time window is empty
        if row and row[3] > 0: 
            avg_t, max_t, min_t, count = row
            
            print("\n--- 📊 24-HOUR STATUS REPORT ---")
            print(f"Total Readings: {count}")
            print(f"Average Temp:   {avg_t}°C")
            print(f"Maximum Temp:   {max_t}°C")
            print(f"Minimum Temp:   {min_t}°C")
            print("--------------------------------\n")

            # 2. THRESHOLD CHECK
            cur.execute("SELECT temperature FROM curriculum_iot_digital_twin_lab.sensor_data ORDER BY aud_insert_ts DESC LIMIT 1;")
            latest_temp = cur.fetchone()[0]

            if latest_temp > THRESHOLD_TEMP:
                print(f"⚠️  WARNING: High temperature detected! ({latest_temp}°C)")
                send_email_alert(latest_temp)
            else:
                print(f"✅ Status: Normal ({latest_temp}°C)")
        else:
            print("📭 No data found in the selected time window. Move the Wokwi slider and try again!")

        cur.close()
        conn.close()

    except Exception as e:
        print(f"❌ Database Error: {e}")

if __name__ == "__main__":
    run_analytics()