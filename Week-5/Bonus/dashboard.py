import streamlit as st
import pandas as pd
import psycopg2
import json
import os
from dotenv import load_dotenv

# --- 1. SETUP & PAGE CONFIG ---
load_dotenv()
st.set_page_config(page_title="IoT Digital Twin v2", page_icon="🛰️", layout="wide")

st.title("🛰️ Smart Sensor Dashboard (JSONB Edition)")
st.markdown("This dashboard pulls live **JSONB** payloads from PostgreSQL and flattens them into a real-time view.")

# --- 2. DATABASE CONNECTION ---
def get_data():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        
        # We query the 'payload' column and the timestamp
        query = """
            SELECT payload, aud_insert_ts 
            FROM curriculum_iot_digital_twin_lab.smart_sensor_data 
            ORDER BY aud_insert_ts DESC 
            LIMIT 50
        """
        # Read into a dataframe
        df_raw = pd.read_sql_query(query, conn)
        conn.close()

        if df_raw.empty:
            return pd.DataFrame()

        # MAGIC STEP: Flatten the JSON 'payload' column into individual columns (temp, hum, uptime)
        # This turns {"temp": 25} into a column named 'temp'
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

# Fetch data
df = get_data()

if not df.empty:
    # A. Display Metrics (The latest reading)
    latest = df.iloc[0]
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Temp", f"{latest['temp']}°C")
    col2.metric("Humidity", f"{latest['hum']}%")
    col3.metric("System Uptime", f"{latest['uptime']}s")

    # B. Visualizing the Trend
    st.subheader("Temperature Trend")
    # We set the index to the timestamp so the chart plots correctly over time
    chart_data = df.set_index('aud_insert_ts')[['temp']]
    st.line_chart(chart_data)

    # C. Raw Data Table
    st.subheader("Latest JSON Payloads")
    st.dataframe(df, use_container_width=True)

else:
    st.warning("No data found in the 'smart_sensor_data' table. Start your bridge and move the Wokwi slider!")

# --- 4. THE AUTO-REFRESH (Advanced Bonus) ---
# This tiny line tells Streamlit to rerun the script every 10 seconds automatically
# st.empty() 
# st.runtime.legacy_caching.clear_cache() # Optional for older versions