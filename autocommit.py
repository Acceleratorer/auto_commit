#wizard auto commit tools 
import os 
import datetime 
import subprocess
import random
import time 

REPO_PATH = r"E:/Code/Github/autocommit"
os.chdir(REPO_PATH)

# commit messages
options = [

    "Update something, but forgot what it is ",
    "Just making sure everything is up to date ",
    "Small adjustments. Don’t ask what ",
    "Fixing things that may or may not be broken ",
    "Code is temporary, commits are forever ",
    "Random tweak because why not ",
    "This commit is 100% necessary. Probably.",
    "Refactoring… in spirit ",
    "Improved the code by looking at it ",
    "Added some magic ",
    "Optimized absolutely nothing ",
    "Made everything worse, but in a good way ",


    "If this breaks, it wasn’t me ",
    "If this works, I’m a genius ",
    "Future me will hate this ",
    "Commit now, cry later ",
    "I regret everything ",
    "Too tired to explain ",

    "Quantum entanglement fixed ",
    "Patched the matrix.exe ",
    "Stabilized quantum bug ",
    "Optimizing chaos engine ",
    "Enhanced entropy protocol ",


    "I’ve seen things… terrible things ",
    "Don’t touch this file. Ever again ",
    "Fixed it, I think. Maybe. Probably not.",
    "We don't talk about this commit ",


    "Fixed bug in a parallel universe ",
    "Improved speed by 3667%* (*not really) ",
    "Self-healing code enabled ",
    "Optimized the unoptimizable ",

    "Nobody knows what this does, including me",
    "99 problems but a commit ain’t one",
    "Bug removed… I think",
    "This commit brought to you by caffeine ",
    "Touching file to feel productive",
    "Commit achieved. Dignity lost.",
]

def build_commit_message():
    base = random.choice(options)
    tag = random.randint(10000, 99999)  # random #12345 tail
    return f"{base} #{tag}"

def do_commit():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = build_commit_message()

    # force change
    with open("heartbeat.txt", "a") as f:
        f.write(f"update at {timestamp}\n")

    # log
    with open("automatic_commit_log.txt", "a") as f:
        f.write(f"{timestamp} - {commit_msg}\n")

    # git ops
    subprocess.run(["git", "add", "."], check=True)
    commit = subprocess.run(
        ["git", "commit", "-m", commit_msg],
        capture_output=True, text=True
    )

    if commit.returncode == 0:
        subprocess.run(["git", "push"], check=True)
        print(f"Done at {timestamp} → {commit_msg}")
    else:
        print("No changes, nothing to commit")

def random_daily_commit(min_commits=0, max_commits=7):
    num_commits = random.randint(min_commits, max_commits)
    commit_times = sorted(random.sample(range(0,24*60*60), num_commits))

    for commit_time in commit_times:
        now = datetime.datetime.now()
        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
        commit_datetime = midnight + datetime.timedelta(seconds=commit_time)

        wait_seconds = (commit_datetime - now).total_seconds()
        if wait_seconds > 0:
            try:
                time.sleep(wait_seconds)
            except:
                pass

        do_commit()

# 15% skip day
if random.random() < 0.15: #change skip rate here 
    print("Off and GoodBye World! (skip day)")
    exit()

if __name__ == "__main__":
    random_daily_commit()
    print("All commits for today are done!")
