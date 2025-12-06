import os 
import datetime 
import subprocess

REPO_PATH = r"E:/Code/Github/autocommit"
os.chdir(REPO_PATH)

#Generate timestamp and log it
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
commit.msg = f"Autocommit {timestamp}"

#Write timestamp log 
with open("automatic_commit_log.txt", "a") as f:
    f.write(f"{commit.msg}\n")

#Git add, commit and push, like operation automatically
subprocess.run(["git", "add", "."], check = True)

commit = subprocess.run(["git", "commit", "-m", commit.msg], check = False)
if commit.returncode == 0:
    subprocess.run(["git", "push"], check = True)
    print("Changes committed and pushed successfully.")
else:
    print("No changes to commit.") #goodbye world

subprocess.run(["git", "commit", "-m", f"Autocommit {datetime.datetime.now()}"], check = True)
subprocess.run(["git", "push"], check = True)