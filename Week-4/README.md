# Week 4: The Intelligence Engine 🧠
Data is only valuable if it drives action. Today, we transform your "Digital Twin" into an active monitor that alerts you when things get too hot.

---

## 🎯 Learning Objectives
* **Database Interrogation:** Connect Python to PostgreSQL for summary reports.
* **Real-time Actuation:** Trigger Email Alerts based on data thresholds.
* **Modern Visualization:** Turn raw rows into interactive trend charts.

---

## 🛠️ Step 1: Environment Updates
> [!IMPORTANT]
> **Credential Check:** Ensure you have copied your .env file from Week 3 into your Week 4 folder. Your script cannot speak to the database or the email server without it.

To support modern data standards and 2026-compliant visualizations, run the following in your **SandboxEnvironment**:
```bash
pip install plotly pandas sqlalchemy
```

---

## 📧 Step 2: Email Configuration
To send alerts, your Python script needs "permission" to use an email account.

> [!TIP]
> **Gmail Users:** You cannot use your regular login password. You must generate an **App Password** under your Google Account security settings.

Update your .env file with these keys:
```bash
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECEIVER=your_personal_email@gmail.com
```

---

## 🐍 Step 3: The Analytics Script (analytics.py)
This script acts as your **System Auditor**. Unlike the Bridge (which is a passive listener), this script is "On-Demand"—it actively interrogates your database to analyze past performance and check if any critical thresholds were crossed while you weren't looking.

**Core Functionality:**
* **Aggregate Reporting:** Uses SQL to find the Min, Max, and Avg temperature.
* **Threshold Monitoring:** Identifies if any record has breached your safety limit (e.g., > 30°C).
* **Email Dispatch:** Automatically sends an alert if the threshold is breached.

**Validation Checklist:**
* **[Wokwi](https://wokwi.com/):** Ensure your simulation is running and you have sent at least one "Hot" reading via the slider.
* **Database:** Verify your Bridge is running and saving data.
* **Execution:** Run python analytics.py in your terminal.

---

## 📊 Step 4: The "Summary" Logic
Your script uses a SQL `INTERVAL` to look at the last 24 hours of data. This provides a professional "Daily Status Report."

> [!TIP]
> **Tinker's Note:** If you just started your simulation and want to see results immediately, you can change the time window in your `analytics.py` script. 
> **Find:** `WHERE aud_insert_ts > NOW() - INTERVAL '24 hours';`
> **Change to:** '5 minutes' to see how your recent "Slider" movements affect the averages!

---

## 🌟 BONUS: The 24/7 Watchman 🛡️
Want your analytics script to run automatically like a professional monitoring service? Wrap your execution in a loop.

1. Import the `time` library at the top of `analytics.py`.
2. Update the bottom of your script:

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