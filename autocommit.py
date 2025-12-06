#wizard auto commit tools 
import os 
import datetime 
import subprocess
import random
import time 

REPO_PATH = r"E:/Code/Github/autocommit"
os.chdir(REPO_PATH)

options = [
    "Update something, but forgot what it is.",
    "Just making sure everything is up to date.",
    "Small adjustments. Don't ask what.",
    "Fixing things that may or may not be broken.",
    "Code is temporary, commits are forever.",
    "Random tweak because why not.",
    "This commit is 100% necessary. Probably.",
    "Refactoring… in spirit.",
    "Improved the code by looking at it.",
    "Added some magic.",
    "Optimized absolutely nothing.",
    "Made everything worse, but in a good way.",
    "This is fine. Everything is fine.",
    "Updated the thing with the stuff.",
    "Auto-commit strikes again.",
    "Chaos-driven development.",
    "I promise this does something.",
    "Slight improvement. Maybe.",
    "Fixed an issue no one knew existed.",
    "Commit now, understand later.",
    "Accidentally improved performance.",
    "Oops. Typed something. Keeping it.",
    "I don’t remember changing anything.",
    "Blind fix #1",
    "Blind fix #2",
    "If this breaks, it wasn’t me.",
    "If this works, I’m a genius.",
    "More changes for the commit gods.",
    "Ssshhhh… it’s a secret commit.",
    "Adding professionalism.",
    "Removed a bug. Or added one.",
    "Totally important commit.",
    "Making GitHub greener.",
    "Just feeding the contribution graph.",
    "Touched a file. That counts.",
    "Slightly more chaos added.",
    "Practicing my commit skills.",
    "Commit committed committing commits.",
    "Everything's made up and the changes don’t matter.",
    "I swear this was necessary.",
    "I'm not sure what this is.",
    "Adding stability? Possibly?",
    "Pushing this so future me suffers.",
    "Future me will hate this.",
    "If it works, don’t question it.",
    "Probably fine.",
    "This commit does exactly nothing.",
    "Fixing something that annoyed me.",
    "Looks cleaner. Trust me.",
    "You didn’t see anything.",
    "Breaking things since 2024.",
    "Optimized the unoptimizable.",
    "More tests? No. More commits.",
    "Commit ritual complete.",
    "Coding at 3AM be like.",
    "Meh, good enough.",
    "Git forced me to do this.",
    "Adding commits for emotional support.",
    "1% improvement. Maybe.",
    "I refuse to explain this commit.",
    "Auto-commit run #404",
    "Accidental improvement.",
    "Added comments that explain nothing.",
    "Documentation? Nah.",
    "Look busy, commit often.",
    "It worked locally.",
    "It's not a bug, it's a feature.",
    "Fixed a typo. Probably introduced three.",
    "Commit before everything explodes.",
    "Making progress... I think.",
    "Don’t worry about this commit.",
    "Done is better than perfect.",
    "The code works. I don’t know why.",
    "The code doesn’t work. I don’t know why.",
    "Debugging is my cardio.",
    "I fix, therefore I am.",
    "Too tired to explain.",
    "Commit now cry later.",
    "Every day is chaos day.",
    "At this point, I accept my fate.",
    "Pls work. Pls.",
    "I regret everything.",
    "This commit is brought to you by coffee.",
    "It’s 2AM. I tried my best.",
    "Send help.",
    "Not broken, just creatively functioning.",
    "Today’s mood: semicolon missing.",
    "Everything is pain.",
    "Life is a bug.",
    "Commit made under extreme stress.",
    "One line changed, five brain cells lost."
]

def do_commit():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = random.choice(options)

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
        print(f"Done at {timestamp}")
    else:
        print("No changes, nothing to commit")

def random_daily_commit(min_commits=0, max_commits=7):
    num_commits = random.randint(min_commits, max_commits)
    commit_times = sorted(random.sample(range(0, 24*60*60), num_commits))

    for commit_time in commit_times:
        now = datetime.datetime.now()
        commit_datetime = now.replace(
            hour=0, minute=0, second=0, microsecond=0
        ) + datetime.timedelta(seconds=commit_time)

        wait_seconds = (commit_datetime - now).total_seconds()
        if wait_seconds > 0:
            time.sleep(wait_seconds)

        do_commit()

# 15% chance to skip today's commits
if random.random() < 0.15:
    print("Off and GoodBye World!")
    exit()

if __name__ == "__main__":
    random_daily_commit()
    print("All commits for today are done!")