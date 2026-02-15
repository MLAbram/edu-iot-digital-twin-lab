# Week 0: Environment Setup 🛠️

> [!TIP]
> **Navigating this Repository:** 
> * **Preview:** The formatted view you are reading now.
> * **Code:** The raw text and files for each lab.
> * **Blame:** Don't let the name scare you! In the dev world, "Blame" is a bit of legacy humor. Think of it as **"Authorship"** or **"Praise"**—it allows you to see the history of every line of code so you can understand the *why* behind the *what*.

To participate in this lab, you need a functional development environment. Follow the instructions below for your specific Operating System.

---

## 1. Browser Simulator (All OS)
* **Action:** Create a free account at [Wokwi.com](https://wokwi.com).
* **Note:** This works entirely in the browser (Chrome, Edge, or Firefox recommended). No installation is required.

---

### 📺 Video Installation Guides
If you prefer a visual walkthrough, click the links below for a curated search of the latest tutorials for your specific system:

| Tool | Windows | macOS | Linux |
| :--- | :--- | :--- | :--- |
| **Python** | [Watch Search](https://www.youtube.com/results?search_query=how+to+install+python+on+windows+11) | [Watch Search](https://www.youtube.com/results?search_query=how+to+install+python+on+mac+homebrew) | [Watch Search](https://www.youtube.com/results?search_query=how+to+install+python+on+ubuntu+linux) |
| **PostgreSQL** | [Watch Search](https://www.youtube.com/results?search_query=install+postgresql+and+pgadmin+on+windows) | [Watch Search](https://www.youtube.com/results?search_query=install+postgresql+and+pgadmin+on+mac) | [Watch Search](https://www.youtube.com/results?search_query=install+postgresql+and+pgadmin+on+linux) |

---

## 2. Python 3.x Installation

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

---

## 3. PostgreSQL & pgAdmin 4

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

## 4. Visual Studio Code (All OS)
1. Download the correct version for your OS from [code.visualstudio.com](https://code.visualstudio.com/).
2. Open VS Code, go to the **Extensions** view (Ctrl+Shift+X), and install:
   * **Python** (by Microsoft)
   * **Pylance** (for better code completion)

---

## ✅ Final Verification
Open your terminal (or Command Prompt) and run:
1. `python --version` (or `python3 --version`)
2. `pip --version` (or `pip3 --version`)

If both return a version number, you are ready for Week 1!