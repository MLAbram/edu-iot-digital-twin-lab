import os
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load Environment Variables (Database Credentials)
load_dotenv()

# --- TERMINAL INSTRUCTION ---
print("\n📊 Launching Visual Intelligence Dashboard...")
print("👉 Note: This will open a new tab in your default web browser.\n")

def get_db_engine():
    """Creates a SQLAlchemy engine for secure, modern database access."""
    db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    return create_engine(db_url)

def create_dashboard():
    """Queries the database and generates an interactive Plotly trend chart."""
    try:
        # 1. Establish Connection & Fetch Data
        engine = get_db_engine()
        
        # We query the sensor_data table (Week 4 Standard Schema)
        query = """
            SELECT temperature, aud_insert_ts 
            FROM edu_iot_digital_twin_lab.sensor_data 
            ORDER BY aud_insert_ts DESC 
            LIMIT 100;
        """
        
        # Pandas uses the engine to "slurp" the data into a DataFrame
        df = pd.read_sql_query(query, engine)

        if df.empty:
            print("📭 No records found. Move the Wokwi slider to generate data first!")
            return

        # 2. Construct the Plotly Line Chart
        # We use 'plotly_dark' for a high-tech "Control Room" aesthetic
        fig = px.line(
            df, 
            x='aud_insert_ts', 
            y='temperature', 
            title='🛰️ IoT Digital Twin: Real-Time Temperature Telemetry',
            labels={'aud_insert_ts': 'Timestamp', 'temperature': 'Temperature (°C)'},
            markers=True,
            template='plotly_dark' 
        )

        # 3. Add Strategic Threshold Line
        # Aligned with our 30.0°C alarm threshold for curriculum consistency
        fig.add_hline(
            y=30.0, 
            line_dash="dot", 
            line_color="red", 
            annotation_text="Critical Threshold (30°C)",
            annotation_position="top left"
        )

        # 4. Final Layout Refinements
        fig.update_layout(
            hovermode="x unified",
            title_font_size=24,
            xaxis_title="Time of Reading",
            yaxis_title="Degrees Celsius (°C)"
        )

        # 5. Execute Visualization
        print("✅ Data retrieved successfully. Rendering chart...")
        fig.show()

    except Exception as e:
        print(f"❌ Visualization Error: {e}")

if __name__ == "__main__":
    create_dashboard()