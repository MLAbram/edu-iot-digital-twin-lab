import streamlit as st
import pandas as pd
import psycopg2
from sqlalchemy import create_engine  # <--- Added for 2026 Pandas Compliance
import json
import os
import time
from dotenv import load_dotenv

# --- TERMINAL INSTRUCTION ---
print("\n🚀 Dashboard Server is running...")
print("👉 Press Ctrl+C in this terminal to stop the Dashboard.\n")

# --- 1. SETUP & PAGE CONFIG ---
load_dotenv()
st.set_page_config(page_title="IoT Digital Twin v2", page_icon="🛰️", layout="wide")

st.title("🛰️ Smart Sensor Dashboard (JSONB Edition)")
st.markdown("This dashboard pulls live **JSONB** payloads from PostgreSQL and flattens them into a real-time view.")

# --- 2. DATABASE CONNECTION ---
def get_data():
    try:
        # Create a SQLAlchemy engine to satisfy modern Pandas requirements
        db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        engine = create_engine(db_url)
        
        query = """
            SELECT payload, aud_insert_ts 
            FROM curriculum_iot_digital_twin_lab.smart_sensor_data 
            ORDER BY aud_insert_ts DESC 
            LIMIT 50
        """
        
        # FIXED: Use the 'engine' instead of the raw 'conn'
        df_raw = pd.read_sql_query(query, engine)

        if df_raw.empty:
            return pd.DataFrame()

        # MAGIC STEP: Flatten the JSON 'payload' column into individual columns
        df_payload = pd.json_normalize(df_raw['payload'])
        
        # Combine the new columns with the timestamp
        df_final = pd.concat([df_payload, df_raw['aud_insert_ts']], axis=1)
        return df_final
    except Exception as e:
        st.error(f"Database Error: {e}")
        return pd.DataFrame()

# --- 3. THE UI LOGIC ---

# Create a sidebar for controls
with st.sidebar:
    st.header("Dashboard Controls")
    refresh = st.button("🔄 Refresh Data")
    st.info("This dashboard reads directly from the 'smart_sensor_data' table.")
    st.markdown("---")
    st.write("🛑 **To stop the server:**")
    st.write("Go to your terminal and press **Ctrl+C**.")

# Fetch data
df = get_data()

if not df.empty:
    # A. Display Metrics (The latest reading)
    latest = df.iloc[0]
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Temp", f"{latest['temp']}°C")
    col2.metric("Humidity", f"{latest['hum']}%")
    
    # Check if 'uptime' exists in the JSON payload before displaying
    if 'uptime' in latest:
        col3.metric("System Uptime", f"{latest['uptime']}s")
    else:
        col3.metric("System Uptime", "N/A")

    # B. Visualizing the Trend
    st.subheader("Temperature Trend")
    chart_data = df.set_index('aud_insert_ts')[['temp']]
    st.line_chart(chart_data)

    # C. Raw Data Table
    st.subheader("Latest JSON Payloads")
    # FIXED: Replaced use_container_width with width='stretch'
    st.dataframe(df, width='stretch')

else:
    st.warning("No data found in the table. Start your bridge and move the Wokwi slider!")

# --- 4. THE AUTO-REFRESH ---
st.divider()
st.write("⏱️ Next auto-refresh in 10 seconds...")
time.sleep(10)
st.rerun()