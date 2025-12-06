import os 
import datetime 
import subprocess

REPO_PATH = r"E:/Code/Github/autocommit"

os.chdir(REPO_PATH)

with open ("log.txt", "a") as log_file:
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file.write(f"Autocommit at {timestamp}\n")
    
subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", f"Autocommit {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"])
subprocess.run(["git", "push"])
