# Week 4: The Intelligence Engine 🧠

Data is only valuable if it drives action. Today, we transform your "Digital Twin" into an active monitor that alerts you when things get too hot.

## 🎯 Learning Objectives
* Connect Python to PostgreSQL for summary reports.
* Trigger real-time Email Alerts based on data thresholds.
* Visualize your data trends (Bonus).

## 🛠️ Step 1: Environment Updates
> [!TIP]
> Ensure you have copied your .env file from Week-3 into your Week-4 folder so your script can connect to the database and email server.

You will need one new library for the Bonus visualization. In your **SandboxEnvironment**, run:
```bash
pip install plotly pandas
```

## 📧 Step 2: Email Configuration
> [!TIP]
> **Note:** For Gmail users, you must generate an App Password under your Google Account security settings. Your regular login password will result in an 'Authentication Failed' error.

To send alerts, your Python script needs "permission" to use an email account.

Create a Gmail App Password (or use an SMTP service like SendGrid).

Add these to your .env file:

```bash
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECEIVER=your_personal_email@gmail.com
```

## 🐍 Step 3: The Analytics Script (analytics.py)
This script acts as your System Auditor. Unlike the Bridge (which is a passive listener), this script is "On-Demand"—it actively interrogates your database to analyze past performance and check if any critical thresholds were crossed while you weren't looking.

**Key Features of the Code:**
* **Aggregate Reporting:** Uses SQL to find the Min, Max, and Avg temperature.
* **Threshold Monitoring:** Checks for any record > 70°C.
* **Email Dispatch:** Automatically sends an alert if the threshold is breached.

**How to Validate this Script:**
* **[HiveMQ Web Client](https://www.hivemq.com/demos/websocket-client/):** Ensure your client is running. 
* **[Wokwi](https://wokwi.com/):** Ensure your simulation is running and you have sent at least one "hot" reading (>70°C) via the slider.
* **.env File:** Ensure your EMAIL_SENDER and EMAIL_PASSWORD (App Password) are correctly set.
* **Run it:** Execute python analytics.py in your SandboxEnvironment.

## 📊 Step 4: The "Summary" Logic
Your script uses a SQL `INTERVAL` to look at the last 24 hours of data. This provides a professional "Daily Status Report."

> [!TIP]
> **Tinker's Note:** If you just started your simulation and want to see results immediately, you can change the time window in your `analytics.py` script. 
> Find the line: `WHERE aud_insert_ts > NOW() - INTERVAL '24 hours';`
> Try changing it to `'1 hour'` or even `'5 minutes'` to see how the averages change based on your most recent "Slider" movements!

## 🚦 Step 5: Validation & Execution Sequence
To successfully test the "Smart Data" pipeline, you must follow this specific order. This ensures the "landing pad" is ready before the data starts flying.

1. The Database (The Foundation)
* **Action:** Run the SQL script from Step 1 in pgAdmin.
* **Verification:** Refresh your tables list in the curriculum_iot_digital_twin_lab schema. You should see smart_sensor_data.

2. The Smart Bridge (The Courier)
* **Action:** Open a terminal in your Week-5 folder and run:
```bash
python bridge_v2.py
```
* **Verification:** You should see: 🚀 Smart Bridge active. Listening for JSON on: curriculum/iot/smart_data.

3. The Wokwi Simulation (The Source)
* **Action:** Start your Wokwi simulation.
* **Verification:** Check the Wokwi Serial Monitor. It should show Connected to MQTT.

4. The "Delta" Test (The Proof of Logic)
This is where we verify the Report by Exception logic:
* **Test A (No Change):** Leave the temperature slider alone. The Python terminal should remain silent. This confirms we are saving bandwidth!
* **Test B (The Change):** Move the slider by at least 1°C.
* **Verification:** The Python terminal should immediately display: 📥 Received JSON: {'temp': ..., 'hum': ..., 'uptime': ...} followed by a success message.

## 🛠️ Step 6: Troubleshooting Checklist
* **No data appearing?** Ensure the MQTT_TOPIC in bridge_v2.py exactly matches the topic in your sketch.ino.
* **JSON Error?** Make sure you added the ArduinoJson library in the Wokwi Library Manager tab.
* **Database Error?** Confirm your .env file is present in the Week-5 folder.

---

## 🌟 BONUS #1: Visualizing the Twin 📈
Inside the Bonus/ folder, you will find a script using Plotly. This turns your database into a high-end interactive graph that you can view in your browser.

## 🌟 BONUS #2: The 24/7 Watchman 🛡️
Want your analytics script to run automatically like the bridge? You can turn it into a persistent monitor by wrapping your main execution in a loop.

1. Import the `time` library at the top of `analytics.py`.
2. Update the bottom of your script to look like this:

```python
if __name__ == "__main__":
    while True:
        run_analytics()
        print("😴 Sleeping for 1 minute before next check...")
        time.sleep(60) # Checks the database every 60 seconds
```

---

## 💡 Why This Matters
**Actionable Intelligence**
In a real-world startup, you can't afford to hire someone to watch a screen 24/7. By building this "Intelligence Engine," you have created a system that only bothers you when there is an actual problem.

**Data Governance**
Using SQL aggregates (AVG, MIN, MAX) directly in the database is far more efficient than pulling all the data into Python. This is how you build systems that can scale to millions of rows without slowing down.