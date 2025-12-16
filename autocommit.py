import os
import sys
import datetime as dt
import subprocess
import random
import logging
from pathlib import Path

# ===================== CONFIG =====================
REPO_PATH = Path(r"E:/Code/Github/autocommit")
PYTHON = sys.executable  # resolved interpreter

SKIP_RATE = 0.15          # 15% chance to skip
FORCE_HEARTBEAT = True   # ensure there is always a diff
LOCK_TIMEOUT_SEC = 60    # stale lock protection

LOG_FILE = REPO_PATH / "autocommit.log"
HEARTBEAT_FILE = REPO_PATH / "heartbeat.txt"
LOCK_FILE = REPO_PATH / ".autocommit.lock"

COMMIT_MESSAGES = [
    "Update something, but forgot what it is",
    "Just making sure everything is up to date",
    "Small adjustments. Don’t ask what",
    "Fixing things that may or may not be broken",
    "Code is temporary, commits are forever",
    "Random tweak because why not",
    "This commit is 100% necessary. Probably.",
    "Refactoring… in spirit",
    "Improved the code by looking at it",
    "Added some magic",
    "Optimized absolutely nothing",
    "Made everything worse, but in a good way",
    "If this breaks, it wasn’t me",
    "If this works, I’m a genius",
    "Future me will hate this",
    "Commit now, cry later",
    "I regret everything",
    "Too tired to explain",
    "Quantum entanglement fixed",
    "Patched the matrix.exe",
    "Stabilized quantum bug",
    "Optimizing chaos engine",
    "Enhanced entropy protocol",
    "I’ve seen things… terrible things",
    "Don’t touch this file. Ever again",
    "Fixed it, I think. Maybe. Probably not.",
    "We don't talk about this commit",
    "Fixed bug in a parallel universe",
    "Improved speed by 3667%* (*not really)",
    "Self-healing code enabled",
    "Optimized the unoptimizable",
    "Nobody knows what this does, including me",
    "99 problems but a commit ain’t one",
    "Bug removed… I think",
    "This commit brought to you by caffeine",
    "Touching file to feel productive",
    "Commit achieved. Dignity lost.",
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
    """Run a command in repo, capture output for logging."""
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
        raise RuntimeError(f"Command failed: {' '.join(cmd)}")
    return res


def acquire_lock():
    """Prevent overlapping runs."""
    if LOCK_FILE.exists():
        age = dt.datetime.now().timestamp() - LOCK_FILE.stat().st_mtime
        if age < LOCK_TIMEOUT_SEC:
            log("Another run is in progress. Exit.")
            return False
        else:
            log("Stale lock detected. Overwriting lock.")
    LOCK_FILE.write_text(str(os.getpid()))
    return True


def release_lock():
    try:
        LOCK_FILE.unlink(missing_ok=True)
    except Exception:
        pass


def build_commit_message():
    base = random.choice(COMMIT_MESSAGES)
    tag = random.randint(10000, 99999)
    return f"{base} #{tag}"


def ensure_diff():
    if not FORCE_HEARTBEAT:
        return
    ts = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    HEARTBEAT_FILE.write_text(f"update at {ts}\n", encoding="utf-8")


def has_changes():
    res = run(["git", "status", "--porcelain"], check=False)
    return bool(res.stdout.strip())


def do_commit():
    ensure_diff()

    if not has_changes():
        log("Nothing to commit. Exit.")
        return

    msg = build_commit_message()

    run(["git", "add", "."]) 
    res = run(["git", "commit", "-m", msg], check=False)

    if res.returncode != 0:
        log("Commit failed or nothing to commit.", logging.WARNING)
        return

    run(["git", "push"]) 
    log(f"Committed & pushed: {msg}")


def maybe_commit():
    if random.random() < SKIP_RATE:
        log("Skip by probability.")
        return
    do_commit()


if __name__ == "__main__":
    os.chdir(REPO_PATH)
    setup_logging()

    log("Task started")

    if not acquire_lock():
        sys.exit(0)

    try:
        maybe_commit()
    except Exception as e:
        log(f"Fatal error: {e}", logging.ERROR)
    finally:
        release_lock()
        log("Task finished")
