import os
import smtplib
import time
from email.message import EmailMessage
from dotenv import load_dotenv
from sqlalchemy import create_engine, text # <--- Modernized connection engine

# Load credentials from .env
load_dotenv()

# --- CONFIGURATION ---
# Industry Standard: Set thresholds as constants for easy tuning
THRESHOLD_TEMP = 30.0  # Alert threshold (matches our Week 6 Lab)

def get_db_engine():
    """Creates a SQLAlchemy engine for 2026-compliant database interaction."""
    db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    return create_engine(db_url)

def send_email_alert(temp):
    """Dispatches a critical alert via Gmail SMTP."""
    msg = EmailMessage()
    msg.set_content(f"🚨 ALERT: Your IoT Digital Twin has detected a high temperature of {temp}°C!")
    msg['Subject'] = f"CRITICAL HEAT ALERT: {temp}°C"
    msg['From'] = os.getenv("EMAIL_SENDER")
    msg['To'] = os.getenv("EMAIL_RECEIVER")

    try:
        # Using SSL for secure transport on Port 465
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_PASSWORD"))
            smtp.send_message(msg)
        print("📧 Email alert sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def run_analytics():
    """Main intelligence loop: Queries DB, calculates stats, and triggers alerts."""
    print("\n🔍 Interrogating Digital Twin Records...")
    
    try:
        engine = get_db_engine()
        
        # We use a context manager (with) to ensure the connection closes automatically
        with engine.connect() as conn:
            
            # 1. FETCH AGGREGATES (Calculating 'The Big Picture')
            # We use SQLAlchemy text() for safe SQL execution
            query_stats = text("""
                SELECT 
                    ROUND(AVG((payload->>'temp')::numeric), 2) as avg_temp,
                    MAX((payload->>'temp')::numeric) as max_temp,
                    MIN((payload->>'temp')::numeric) as min_temp,
                    COUNT(*) as total_readings
                FROM edu_iot_digital_twin_lab.smart_sensor_data
                WHERE aud_insert_ts > NOW() - INTERVAL '24 hours';
            """)
            
            result = conn.execute(query_stats)
            row = result.fetchone()
            
            # Defensive Programming: Ensure we have data before calculating
            if row and row.total_readings > 0: 
                avg_t, max_t, min_t, count = row
                
                print("\n" + "="*35)
                print("📊 24-HOUR STRATEGIC REPORT")
                print("="*35)
                print(f"Total Readings: {count}")
                print(f"Average Temp:   {avg_t}°C")
                print(f"Maximum Temp:   {max_t}°C")
                print(f"Minimum Temp:   {min_t}°C")
                print("-" * 35)

                # 2. LATEST READING CHECK (The 'Real-Time' Pulse)
                query_latest = text("""
                    SELECT (payload->>'temp')::numeric 
                    FROM edu_iot_digital_twin_lab.smart_sensor_data 
                    ORDER BY aud_insert_ts DESC 
                    LIMIT 1;
                """)
                latest_temp = conn.execute(query_latest).scalar()

                if latest_temp > THRESHOLD_TEMP:
                    print(f"⚠️  CRITICAL: High temperature detected! ({latest_temp}°C)")
                    send_email_alert(latest_temp)
                else:
                    print(f"✅ SYSTEM HEALTH: Normal ({latest_temp}°C)")
            else:
                print("📭 No data found in the last 24 hours. Move the Wokwi slider!")

    except Exception as e:
        print(f"❌ Database/Analytics Error: {e}")

if __name__ == "__main__":
    # Instruction for the student
    print("\n🚀 Intelligence Engine is running.")
    print("👉 Press Ctrl+C to stop the monitor.")
    
    # Optional: Wrap in a loop if the student wants a 'Watchman'
    run_analytics()