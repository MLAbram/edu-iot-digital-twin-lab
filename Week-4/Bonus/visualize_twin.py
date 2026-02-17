import os
from sqlalchemy import create_engine
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv

# Load credentials
load_dotenv()

def get_db_engine():
    # Construct the connection string for SQLAlchemy
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASS")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    dbname = os.getenv("DB_NAME")
    
    # Format: postgresql://user:password@host:port/dbname
    url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    return create_engine(url)

def create_dashboard():
    try:
        # 1. Connect and Fetch Data using the Engine
        engine = get_db_engine()
        query = "SELECT temperature, aud_insert_ts FROM curriculum_iot_digital_twin_lab.sensor_data ORDER BY aud_insert_ts DESC LIMIT 100;"
        
        # Pandas uses the engine to "slurp" the data
        df = pd.read_sql_query(query, engine)

        if df.empty:
            print("📭 No data found to visualize. Move the Wokwi slider first!")
            return

        # 2. Create the Plotly Line Chart
        fig = px.line(
            df, 
            x='aud_insert_ts', 
            y='temperature', 
            title='IoT Digital Twin: 100-Point Temperature Trend',
            labels={'aud_insert_ts': 'Time', 'temperature': 'Temperature (°C)'},
            markers=True
        )

        # 3. Add the Critical Threshold line (Matching your README's 70°C)
        fig.add_hline(y=70.0, line_dash="dot", line_color="red", annotation_text="Critical Threshold (70°C)")

        # 4. Open in Browser
        print("📊 Generating dashboard... Check your browser!")
        fig.show()

    except Exception as e:
        print(f"❌ Visualization Error: {e}")

if __name__ == "__main__":
    create_dashboard()