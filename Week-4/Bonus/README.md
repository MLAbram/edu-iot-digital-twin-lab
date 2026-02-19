## 🌟 Week 4 Bonus #1: Visualizing the Digital Twin 📊
Welcome to the "**Command Center**" phase! While logs and email alerts are vital for monitoring, Visualization is how we communicate complex data trends to stakeholders at a glance.

In this bonus lab, you will transform your PostgreSQL database into an interactive, browser-based telemetry chart.

---

## 🚀 Why This Matters

**1. Professional Data Handling (Pandas)**
In the industry, data scientists rarely use raw loops to process database records. You will use **Pandas**, the gold standard for data manipulation, to "slurp" SQL data directly into a **DataFrame**. This is the foundation of modern Data Science.

**2. Interactive Design**
Static images are for reports; **Interactive Dashboards** are for engineers. By using **Plotly**, you will generate a graph that allows you to:
* **Hover:** See exact timestamps and temperature values.
* **Zoom:** Focus on specific heat spikes.
* **Export:** Save your findings as a high-quality image.

**3. Closing the "Digital Twin" Loop**
When you move the slider in Wokwi and see the line on your graph respond, the concept of a **Digital Twin** becomes tangible. You aren't just looking at numbers; you are looking at a digital reflection of a physical environment.

---

## 🛠️ Setup & Validation

**1. Install Prerequisites**
Inside your **SandboxEnvironment**, you will need to install the visualization toolkit:
```bash
pip install pandas plotly sqlalchemy
```

**Note:** sqlalchemy is the helper library that Pandas uses to communicate efficiently with the PostgreSQL engine.

**2. Run the Visualizer**
Navigate to your folder and execute the dashboard script:

```bash
python dashboard.py
```

**3. The Results**
Your default web browser should automatically open a new tab displaying your **Temperature Trend Telemetry**.

## 🏆 Graduation Check
If you see a dark-themed line graph with a red "Critical Threshold" line at **30°C**, you have successfully completed the entire Week 4 curriculum path!

**You have now built a full-stack pipeline that Senses, Stores, Alerts, and Visualizes.**