# Week 0: Environment Setup 🛠️

> [!TIP]
> **Navigating this Repository:** 
> * **Preview:** The formatted view you are reading now.
> * **Code:** The raw text and files for each lab.
> * **Blame:** Don't let the name scare you! In the dev world, "Blame" is a bit of legacy humor. Think of it as **"Authorship"** or **"Praise"**—it allows you to see the history of every line of code so you can understand the *why* behind the *what*.

To participate in this lab, you need a functional development environment. Follow the instructions below for your specific Operating System.

---

### 📺 Video Installation Guides
> [!TIP]
> **Pro-Tip:** To keep this guide open while watching the videos, **Right-Click** the links below and select **"Open link in new tab"** (or use Ctrl/Cmd + Click).

If you prefer a visual walkthrough, click the links below for a curated search of the latest tutorials for your specific system:

| Tool | Windows | macOS | Linux |
| :--- | :--- | :--- | :--- |
| **Python** | [YouTube Search](https://www.youtube.com/results?search_query=how+to+install+python+on+windows) | [YouTube Search](https://www.youtube.com/results?search_query=how+to+install+python+on+mac+homebrew) | [YouTube Search](https://www.youtube.com/results?search_query=how+to+install+python+on+ubuntu+linux) |
| **PostgreSQL** | [YouTube Search](https://www.youtube.com/results?search_query=install+postgresql+and+pgadmin+on+windows) | [YouTube Search](https://www.youtube.com/results?search_query=install+postgresql+and+pgadmin+on+mac) | [YouTube Search](https://www.youtube.com/results?search_query=install+postgresql+and+pgadmin+on+linux) |

---

## 🛠️ Step 1: The Project Architecture (Directory Setup)
Before writing a single line of code, we must build a professional "Sandbox." This ensures your global computer settings remain clean while your IoT project has exactly the tools it needs to run.

**The Gold Standard Structure**
You will create a parent folder for the entire course, with a dedicated "engine room" for your Python packages.

1. **Create the Root Directory:** Create a folder named edu-iot-digital-twin-lab.
2. **Create the Sandbox:** Inside that folder, create a nested folder named PythonSandbox.
3. **The Logic Rule:**
   * **Packages:** All library installations (via pip) will live safely inside PythonSandbox.
   * **Code:** All of your .py scripts (Bridge, Analytics, Dashboards) must be saved in the root of edu-iot-digital-twin-lab.

**Visualizing Your Workspace**
Your folder structure should look exactly like this:
```text
edu-iot-digital-twin-lab/       <-- Save your .py scripts here
└── PythonSandbox/              <-- Your Virtual Environment (The Engine)
```

> [!TIP]
> Why this matters: In production environments, we never install libraries "globally." By nesting your PythonSandbox, you create a portable, isolated environment. If you ever need to move your project to a new computer, your "Engine" moves with your "Code."

---

## 🐍 Step 2: Python 3.x Installation
Python is the "bridge" we will use to move data from the cloud to our database.

### 🪟 Windows
1. Download the installer from [python.org](https://www.python.org/downloads/).
2. **IMPORTANT:** Check the box **"Add Python to PATH"** before clicking "Install Now."
3. Open **Command Prompt** and type `python --version` to verify.

### 🍎 macOS
1. Install [Homebrew](https://brew.sh/) if you haven't already.
2. Open **Terminal** and type: `brew install python`
3. Verify by typing `python3 --version`.

### 🐧 Linux (Ubuntu/Debian)
1. Open **Terminal** and type: 
   `sudo apt update && sudo apt install python3 python3-pip`
2. Verify by typing `python3 --version`.

**Activating the Engine**
Once your folders are created, you must "start" the engine to begin installing your tools.

From your terminal, navigate inside edu-iot-digital-twin-lab and run:
1. **Initialize the Sandbox:**
```bash
python3 -m venv PythonSandbox
```
2. **Activate the Environment:**
* **Windows:** PythonSandbox\Scripts\activate
* **macOS/Linux:** source PythonSandbox/bin/activate

> [!IMPORTANT]
> The Prompt Check: Once activated, your terminal prompt will show (PythonSandbox). This is your confirmation that you are now working inside the shielded environment.

---

## 🐘 Step 3: PostgreSQL & pgAdmin 4
PostgreSQL is where we will store our historical sensor data.

### 🪟 Windows
1. Download the installer from [EnterpriseDB](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads).
2. Follow the wizard. **Record the password** you set for the `postgres` user.

### 🍎 macOS
1. Use Homebrew: `brew install postgresql@16`
2. Download the [pgAdmin 4 GUI](https://www.pgadmin.org/download/pgadmin-4-macos/) separately to manage your data visually.

### 🐧 Linux
1. Type: `sudo apt install postgresql postgresql-contrib`
2. Install pgAdmin via their [official apt repo](https://www.pgadmin.org/download/pgadmin-4-apt/).

---

## 🛠️ Step 4: Visual Studio Code (All OS)
VS Code is our primary workspace for writing Python and managing our GitHub repository.

1. Download the correct version for your OS from [code.visualstudio.com](https://code.visualstudio.com/).
2. Open VS Code, go to the **Extensions** view (Ctrl+Shift+X), and install:
   * **Python** (by Microsoft)
   * **Pylance** (for better code completion)

---

## 🛠️ Step 5: Wokwi Account Setup
Wokwi allows us to simulate hardware without needing physical wires.

1. Create a free account at [Wokwi](https://wokwi.com/).
2. Sign in so you can save your projects and share them in your repository.

---

## 📂 Step 6: Initialize Your Local Workspace

Now that your tools are installed, you need a local place to save your code and sync it with GitHub. You have two options:

### **Option A: Clone the Repository (Recommended)**
If you are comfortable with Git, cloning this repository is the fastest way to get the structure. Open your terminal/VS Code and run:
```bash
git clone [https://github.com/ApexISStrategy/edu-iot-digital-twin-lab.git](https://github.com/ApexISStrategy/edu-iot-digital-twin-lab.git)
cd edu-iot-digital-twin-lab
```

### **Option B: Manual Setup**

If you prefer to build the structure manually as we go:

Create a folder on your computer named edu-iot-digital-twin-lab.

Open this folder in Visual Studio Code or your favorite programming IDE.

Create your first sub-folders: Week-0, Week-1, and so on.

> [!TIP]
> Why this matters: Having a dedicated local directory allows you to use the VS Code Source Control tab to "Commit" and "Push" your work to your own GitHub profile. This builds your professional portfolio as you learn!

---

## 🛠️ Environment Check
Ensure you are working from the root of your project and your sandbox is active:
1. **Open Terminal:** Navigate to edu-iot-digital-twin-lab.
2. **Activate:** * source PythonSandbox/bin/activate (Mac/Linux)
   * PythonSandbox\Scripts\activate (Windows)
3. **Verify:** You should see (PythonSandbox) at the start of your command line.

---

## 🔐 Security Reminder
If you will saving this project to your Github, confirm you have a `.gitignore` file in the root of your folder.

### Security: Never upload your database credentials
.env

### Environment: Keep the workspace clean
SandboxEnvironment/
.venv/
env/
venv/

### Python: Ignore temporary cache files
__pycache__/
*.py[cod]
*$py.class

---

## ✅ Final Verification
Open your terminal (or Command Prompt) and run:
1. `python --version` (or `python3 --version`)
2. `pip --version` (or `pip3 --version`)

If both return a version number, you are ready for Week 1!
