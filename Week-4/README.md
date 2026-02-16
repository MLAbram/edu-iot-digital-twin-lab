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

```Plaintext
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECEIVER=your_personal_email@gmail.com
```

## 🐍 Step 3: The Analytics Script (analytics.py)
This script will "interrogate" your database and act as your 24/7 watchman. This script is designed to be the "Intelligence Engine" of the project. It doesn't just sit and wait for messages; it actively queries the database to see what has happened over time and makes decisions based on that history.

**Key Features of the Code:**
* **Aggregate Reporting:** Uses SQL to find the Min, Max, and Avg temperature.
* **Threshold Monitoring:** Checks for any record > 90°F.
* **Email Dispatch:** Automatically sends an alert if the threshold is breached.

**How to Validate this Script:**
* Wokwi: Ensure your simulation is running and you have sent at least one "hot" reading (>90°F) via the slider.
* .env File: Ensure your EMAIL_SENDER and EMAIL_PASSWORD (App Password) are correctly set.
* Run it: Execute python analytics.py in your SandboxEnvironment.

## 📊 Step 4: The "Summary" Logic
Your script uses a SQL `INTERVAL` to look at the last 24 hours of data. This provides a professional "Daily Status Report."

> [!TIP]
> **Tinker's Note:** If you just started your simulation and want to see results immediately, you can change the time window in your `analytics.py` script. 
> Find the line: `WHERE aud_insert_ts > NOW() - INTERVAL '24 hours';`
> Try changing it to `'1 hour'` or even `'5 minutes'` to see how the averages change based on your most recent "Slider" movements!

---

## 🌟 BONUS: Visualizing the Twin 📈
Inside the Bonus/ folder, you will find a script using Plotly. This turns your database into a high-end interactive graph that you can view in your browser.


---

### **A Quick Note for the Professor**
Teaching students about **SMTP (Simple Mail Transfer Protocol)** and **App Passwords** is a vital security lesson. It reinforces why we use `.env` files—because you *never* want your email password sitting in a public GitHub repository.

**How does this structure sound? If you’re ready, I can draft the full `analytics.py` script so you can validate the email alert yourself!**