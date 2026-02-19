## 🌉 Week 3: The Data Bridge
Until now, your data has been "volatile"—as soon as you close the HiveMQ website, the history is gone. This week, we build a Python bridge to capture that data and save it permanently into a **PostgreSQL** database.

---

## 🎯 Learning Objectives
* **MQTT Subscription:** Write a Python script to "harvest" real-time data from the cloud.
* **Credential Management:** Use .env files to keep your database passwords off the internet.
* **Persistent Storage:** Design a professional schema with microsecond precision.

## 🛠️ Step 1: Database & Schema Setup
Before running the code, we need to create a professional data structure. Open **pgAdmin 4** or your terminal and run the following commands:

```sql
-- 1. Create the central database
CREATE DATABASE curriculum;

-- 2. Connect to the 'curriculum' database, then create the schema
CREATE SCHEMA curriculum_iot_digital_twin_lab;

-- 3. Create the table with audit-ready timestamps
CREATE TABLE curriculum_iot_digital_twin_lab.sensor_data (
    id SERIAL PRIMARY KEY,
    temperature FLOAT,
    unit VARCHAR(1),
    aud_insert_ts TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP NOT NULL
);
```

---

## 📦 Step 2: Setting up the Sandbox (Virtual Environment)
> [!IMPORTANTP]
> Why use a venv? Modern Linux and macOS systems prevent you from installing libraries globally to protect the operating system. We create a "Sandbox" specifically for this project.

**Follow these steps in your terminal:**
1. **Install the Tooling:** sudo apt install python3-venv
2. **Create your Sandbox:** python3 -m venv .venv
3. **Activate it:** source .venv/bin/activate
(You should now see (.venv) appear at the beginning of your prompt!)
4. **Install the Stack:**
```bash
pip install paho-mqtt psycopg2 python-dotenv
```

---

## 🛡️ Step 3: Security & Credential Management
Create a file in your **Week-3** folder titled .env. This file holds your "Secrets."

Add the following and update the DB_PASS **to your actual password**:
```bash
DB_NAME=curriculum
DB_USER=postgres
DB_PASS=your_secret_password
DB_HOST=localhost
DB_PORT=5432
```

---

## 🐍 Step 4: The Python Bridge Code (bridge.py)
This script acts as the "**Subscriber**" that listens to the broker and writes every incoming reading to your database. **This file is located in the root of the Week 3 folder.**

---

## 🧪 Step 5: Verification
* [ ] **Wokwi:** Is your simulation running and sending data?
* [ ] **Bridge:** Does the terminal say ✅ Record successfully committed?
* [ ] **Persistence:** In pgAdmin, run: SELECT * FROM curriculum_iot_digital_twin_lab.sensor_data;. Do you see your data?

---

## 💡 Why This Matters
**Data Persistence**
A dashboard only shows you "now." By building this bridge, you are creating a **Historical Narrative**. This allows an entrepreneur to analyze trends and perform predictive maintenance.

**Professional Security**
By using .env files, you are practicing **Credential Management**. Hard-coding passwords into your scripts is the #1 cause of major data breaches. You are building like a pro from Day 1.