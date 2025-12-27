# wizard auto commit tools — v4 (Behavioral Intelligence Edition)
# Author: Acceleratorer
# Version: v4.1.0
# --------------------------------------------------
# Behavioral systems:
# - Burnout accumulation & recovery
# - Smart vacation triggering
# - Cooldown after vacation
# - Human-like commit rhythm
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
LOCK_TIMEOUT_SEC = 90

# ---------- Burnout ----------
BURNOUT_INCREASE = 0.12
BURNOUT_RECOVERY = 0.08

# ---------- Vacation ----------
BASE_VACATION_RATE = 0.003
MAX_VACATION_RATE = 0.03
VACATION_DAYS = (1, 3)
COOLDOWN_DAYS = (2, 4)

# ---------- Time personality ----------
TIME_WEIGHTS = {
    "night": 0.1,
    "morning": 0.6,
    "afternoon": 1.0,
    "evening": 0.8,
}

WEEKDAY_MULTIPLIER = 1.2
WEEKEND_MULTIPLIER = 0.6

DEFAULT_MESSAGES = [
    "Minor cleanup",
    "Refactor logic",
    "Improve readability",
    "Fix small edge case",
    "General improvement",
    "Small optimization",
    "Touching file to feel productive",
    "Commit achieved. Dignity lost.",
    "Future me will hate this",
    "Too tired to explain",
    "Optimized absolutely nothing",
    "This commit is 100% necessary. Probably.",
]

# =================================================


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


# ================= LOCK ===========================

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


# ================= STATS ==========================

def load_json(path, default):
    if path.exists():
        return json.loads(path.read_text())
    return default


def save_json(path, data):
    path.write_text(json.dumps(data, indent=2))


# ================= BEHAVIOR =======================

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


# ================= BURNOUT ========================

def update_burnout(stats, committed):
    today = dt.date.today()
    burnout = stats.get("burnout", 0.0)

    if committed:
        burnout += BURNOUT_INCREASE
    else:
        burnout -= BURNOUT_RECOVERY

    stats["burnout"] = max(0.0, min(1.0, burnout))
    stats["last_active_day"] = today.isoformat()

    log(f"Burnout updated → {stats['burnout']:.2f}")


# ================= VACATION =======================

def vacation_probability(stats):
    burnout = stats.get("burnout", 0.0)
    return BASE_VACATION_RATE + burnout * (MAX_VACATION_RATE - BASE_VACATION_RATE)


def maybe_start_vacation(stats):
    today = dt.date.today()

    # Active vacation
    if stats.get("vacation_until"):
        if today <= dt.date.fromisoformat(stats["vacation_until"]):
            return
        stats["vacation_until"] = None

    # Cooldown
    if stats.get("cooldown_until"):
        if today <= dt.date.fromisoformat(stats["cooldown_until"]):
            return
        stats["cooldown_until"] = None

    prob = vacation_probability(stats)
    roll = random.random()

    log(f"Vacation roll={roll:.3f}, prob={prob:.3f}")

    if roll < prob:
        days = random.randint(*VACATION_DAYS)
        until = today + dt.timedelta(days=days)
        stats["vacation_until"] = until.isoformat()

        cd = random.randint(*COOLDOWN_DAYS)
        stats["cooldown_until"] = (until + dt.timedelta(days=cd)).isoformat()

        log(f"Vacation started {days} days, cooldown {cd} days")


def in_vacation(stats):
    until = stats.get("vacation_until")
    if not until:
        return False
    return dt.date.today() <= dt.date.fromisoformat(until)


def should_commit(stats):
    if in_vacation(stats):
        log("Vacation active. Skip commit.")
        return False

    if daily_commit_count(stats) >= MAX_COMMITS_PER_DAY:
        return False

    multiplier = WEEKEND_MULTIPLIER if is_weekend() else WEEKDAY_MULTIPLIER
    burnout_penalty = 1.0 - stats.get("burnout", 0.0) * 0.6

    probability = (1 - BASE_SKIP_RATE) * time_weight() * multiplier * burnout_penalty
    decision = random.random() < probability

    log(f"Commit prob={probability:.2f}, decision={decision}")
    return decision


# ================= MESSAGES =======================

def load_messages():
    history = load_json(MSG_HISTORY_FILE, {})
    if history:
        return list(Counter(history).elements())
    return DEFAULT_MESSAGES


def record_message(msg):
    history = load_json(MSG_HISTORY_FILE, {})
    history[msg] = history.get(msg, 0) + 1
    save_json(MSG_HISTORY_FILE, history)


# ================= GIT ============================

def ensure_diff():
    ts = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    HEARTBEAT_FILE.write_text(f"update at {ts}\n")


def do_commit(stats):
    ensure_diff()
    run(["git", "add", "."])

    msg = random.choice(load_messages())
    run(["git", "commit", "-m", msg], check=False)
    run(["git", "push"])

    record_commit(stats)
    record_message(msg)
    update_burnout(stats, committed=True)

    log(f"Committed: {msg}")


# ================= MAIN ===========================

if __name__ == "__main__":
    os.chdir(REPO_PATH)
    setup_logging()
    log("Task started (v4.1)")

    if not acquire_lock():
        sys.exit(0)

    stats = load_json(
        STATS_FILE,
        {
            "daily_commits": {},
            "burnout": 0.0,
            "vacation_until": None,
            "cooldown_until": None,
            "last_active_day": None,
        },
    )

    try:
        maybe_start_vacation(stats)

        if should_commit(stats):
            do_commit(stats)
        else:
            update_burnout(stats, committed=False)
            log("No commit this run")

    except Exception as e:
        log(f"Fatal error: {e}", logging.ERROR)

    finally:
        save_json(STATS_FILE, stats)
        release_lock()
        log("Task finished (v4.1)")

