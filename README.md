# 🕒 AutoCommit Script (Auto Commit Wizard)

A simple automation script that automatically commits changes to a Git repository using Python and a Windows `.bat` + Task Scheduler setup.

---

## 🚀 Features
- Automatically creates a new Git commit with a timestamp.
- Logs every commit into `automatic_commit_log.txt`.
- Works with Windows Task Scheduler to run at any interval.
- Lightweight and easy to customize.

---

## 📂 Project Structure
E:/Code/Github/autocommit
│── autocommit.py
│── automatic_commit_log.txt
│── run.bat
│── README.md

---

## 🐍 `autocommit.py`

Your Python script handles:
- Generating timestamp
- Logging to file
- Running Git commands

Make sure Git is installed and added to PATH.

---

## 🖥️ Windows Batch File (`run.bat`)

Used to run the script via Task Scheduler:

.bat file
```
@echo off
cd /d "E:\Code\Github\autocommit"
"C:\Users\goddt\AppData\Local\Programs\Python\Python314\python.exe" autocommit.py
pause
```
If you run via Task Scheduler and don't want the window to close, keep the pause.
If running silently → remove pause.

⏰ Setting up Task Scheduler

1/Open Task Scheduler

2/Create Basic Task

3/Trigger → choose Daily / Hourly / Every 5 minutes etc.

4/Action → Start a Program

5/Program/script → Browse → select run.bat

Make sure:

“Run only when user is logged on” is checked if you want the popup terminal.

“Run with highest privileges” is optional.

📝 Commit Log Example

Every run adds a line like:
Autocommit 2025-12-09 12:30:45

✨ Tips

You can set Task Scheduler to run every 1 minute for near real-time commits.

Make sure your repo has correct remote and you already ran:
git remote add origin <your_repo_link>
git branch -M main

❤️ Author

Automation script by Acceleratorer
Simple idea → smooth workflow 😎