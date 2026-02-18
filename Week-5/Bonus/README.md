## 🌟 Week 5 Bonus: The Live Digital Twin Web-App 🛰️
Welcome to the "Grand Finale" of your dashboard evolution! In Week 4, we built a static chart. Today, we are moving to **Streamlit**—the industry standard for turning data scripts into professional, interactive web applications in minutes.

## 🚀 Why This Matters
1. 🏎️**Professional UI with "Low Code"**
In a startup environment, speed is everything. Streamlit allows you to build a high-end interface without needing to learn HTML, CSS, or JavaScript. You are now a **Full-Stack IoT Developer**.

2. 🗄️**JSON Normalization**
Storing data as JSONB in PostgreSQL is powerful, but it’s "messy" to look at. This lab teaches you how to **Flatten** or **Normalize** that JSON, turning a single block of text into individual, readable columns like Temperature and Humidity.

3. 📈**Live Decision Support**
By using **Metric Cards**, you provide "at-a-glance" intelligence. You aren't just showing data; you are showing a **Digital Twin** that tells a story about the physical world.

## 🛠️ Setup & Validation
1. Install the Web Framework
Ensure your **SandboxEnvironment** is active and install the Streamlit library:
```bash
pip install streamlit
```

2. **Launch the App**
Navigate to your project root and run:
```bash
streamlit run Bonus/dashboard_v2.py
```
> [!TIP]
> **What happens next?** Streamlit will spin up a local web server and automatically open a new tab in your browser (usually at localhost:8501).

3. **The "Live Twin" Test**
To see the full power of your creation, try this "Side-by-Side" test:
* **Open Wokwi** on one half of your screen.
* **Open your Streamlit Dashboard** on the other half.
* **Move the Wokwi slider.**
* **Watch your Bridge Terminal** confirm the save, then watch the line chart move and the "Metric Cards" update instantly!

## 🏆 Graduation Milestone
If you can see your temperature and humidity displayed in metric cards and a live line chart, you have successfully built a **production-ready IoT pipeline**.

**You have mastered:**
* ✅ Hardware Logic (C++ and Arduino)
* ✅ Communication Protocols (MQTT)
* ✅ Cloud Middleware (Python Bridges)
* ✅ Modern Databases (PostgreSQL & JSONB)
* ✅ Data Visualization (Streamlit)

---

## Final Wrap-Up
You have officially reached the end of the Week 5 curriculum development! Looking back at what you've built:
* **Week 1:** You started with a blinking LED and a "Hello World" circuit.
* **Week 2:** You broke the "tether" and sent that data to the Cloud via MQTT.
* **Week 3:** You built a permanent memory for our Twin using PostgreSQL.
* **Week 4:** You added "Actionable Intelligence" with Email alerts and static graphs.
* **Week 5:** You optimized for the real world with JSON, Edge Logic, and a Live Web Dashboard.

You now have a fully functional **IoT Prototype Stack**. This isn't just a toy; the architecture you've used (MQTT -> Python -> PostgreSQL JSONB -> Streamlit) is exactly how many modern industrial startups build their **Minimum Viable Products (MVPs)**.