# wizard auto commit tools — v4 (Behavioral Intelligence Edition)
# Author: Acceleratorer
# Version: v4.0.0
# --------------------------------------------------
# Key features:
# - Human-like commit rhythm (time + weekday)
# - Weekend / workday personality
# - Vacation & cooldown modes
# - Commit heatmap-ready analytics
# - Message learning (weighted history)
# - Safe Task Scheduler execution

import os
import sys
import json
import random
import logging
import subprocess
import datetime as dt
from pathlib import Path
from collections import Counter

# ===================== CONFIG =====================
REPO_PATH = Path(r"E:/Code/Github/autocommit")

LOG_FILE = REPO_PATH / "autocommit.log"
STATS_FILE = REPO_PATH / "commit_stats.json"
MSG_HISTORY_FILE = REPO_PATH / "message_history.json"
HEARTBEAT_FILE = REPO_PATH / "heartbeat.txt"
LOCK_FILE = REPO_PATH / ".autocommit.lock"

MAX_COMMITS_PER_DAY = 5
BASE_SKIP_RATE = 0.12
VACATION_RATE = 0.04
VACATION_DAYS = (2, 6)
LOCK_TIMEOUT_SEC = 90

# Time-of-day weights
TIME_WEIGHTS = {
    "night": 0.1,     # 00–06
    "morning": 0.6,   # 06–11
    "afternoon": 0.9, # 12–17
    "evening": 0.7,   # 18–23
}

# Weekday personality
WEEKDAY_MULTIPLIER = 1.0
WEEKEND_MULTIPLIER = 0.6

DEFAULT_MESSAGES = [
    "Minor cleanup",
    "Refactor logic",
    "Improve readability",
    "Update internal flow",
    "Fix small edge case",
    "Code maintenance",
    "General improvement",
    "Small optimization",
]
# ==================================================


def setup_logging():
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )


def log(msg, level=logging.INFO):
    logging.log(level, msg)


def run(cmd, check=True):
    res = subprocess.run(
        cmd,
        cwd=REPO_PATH,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if res.stdout:
        log(res.stdout.strip())
    if res.stderr:
        log(res.stderr.strip(), logging.WARNING)
    if check and res.returncode != 0:
        raise RuntimeError("Command failed")
    return res


# -------------------- LOCK ------------------------

def acquire_lock():
    if LOCK_FILE.exists():
        age = dt.datetime.now().timestamp() - LOCK_FILE.stat().st_mtime
        if age < LOCK_TIMEOUT_SEC:
            log("Another run in progress. Exit.")
            return False
    LOCK_FILE.write_text(str(os.getpid()))
    return True


def release_lock():
    LOCK_FILE.unlink(missing_ok=True)


# -------------------- STATS -----------------------

def load_json(path, default):
    if path.exists():
        return json.loads(path.read_text())
    return default


def save_json(path, data):
    path.write_text(json.dumps(data, indent=2))


# ----------------- BEHAVIOR -----------------------

def time_weight():
    h = dt.datetime.now().hour
    if h < 6:
        return TIME_WEIGHTS["night"]
    if h < 12:
        return TIME_WEIGHTS["morning"]
    if h < 18:
        return TIME_WEIGHTS["afternoon"]
    return TIME_WEIGHTS["evening"]


def is_weekend():
    return dt.datetime.now().weekday() >= 5


def daily_commit_count(stats):
    today = dt.date.today().isoformat()
    return stats["daily_commits"].get(today, 0)


def record_commit(stats):
    today = dt.date.today().isoformat()
    stats["daily_commits"][today] = stats["daily_commits"].get(today, 0) + 1


def in_vacation(stats):
    until = stats.get("vacation_until")
    if not until:
        return False
    return dt.date.today() <= dt.date.fromisoformat(until)


def maybe_start_vacation(stats):
    if random.random() < VACATION_RATE:
        days = random.randint(*VACATION_DAYS)
        until = dt.date.today() + dt.timedelta(days=days)
        stats["vacation_until"] = until.isoformat()
        log(f"Vacation mode enabled until {until}")


def should_commit(stats):
    if in_vacation(stats):
        log("Vacation active. Skip.")
        return False

    if daily_commit_count(stats) >= MAX_COMMITS_PER_DAY:
        log("Daily commit limit reached.")
        return False

    multiplier = WEEKEND_MULTIPLIER if is_weekend() else WEEKDAY_MULTIPLIER
    probability = (1 - BASE_SKIP_RATE) * time_weight() * multiplier

    decision = random.random() < probability
    log(f"Commit probability={probability:.2f}, decision={decision}")
    return decision


# ----------------- MESSAGES -----------------------

def load_messages():
    history = load_json(MSG_HISTORY_FILE, {})
    if history:
        weighted = Counter(history)
        return list(weighted.elements())
    return DEFAULT_MESSAGES


def record_message(msg):
    history = load_json(MSG_HISTORY_FILE, {})
    history[msg] = history.get(msg, 0) + 1
    save_json(MSG_HISTORY_FILE, history)


# ------------------- GIT --------------------------

def ensure_diff():
    ts = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    HEARTBEAT_FILE.write_text(f"update at {ts}\n")


def do_commit(stats):
    ensure_diff()
    run(["git", "add", "."])

    messages = load_messages()
    msg = random.choice(messages)

    run(["git", "commit", "-m", msg], check=False)
    run(["git", "push"])

    record_commit(stats)
    record_message(msg)
    log(f"Committed: {msg}")


# ------------------- MAIN -------------------------

if __name__ == "__main__":
    os.chdir(REPO_PATH)
    setup_logging()
    log("Task started (v4)")

    if not acquire_lock():
        sys.exit(0)

    stats = load_json(STATS_FILE, {"daily_commits": {}, "vacation_until": None})

    try:
        maybe_start_vacation(stats)
        if should_commit(stats):
            do_commit(stats)
        else:
            log("No commit this run")
    except Exception as e:
        log(f"Fatal error: {e}", logging.ERROR)
    finally:
        save_json(STATS_FILE, stats)
        release_lock()
        log("Task finished (v4)")
