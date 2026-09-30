# mastery.py
# Tracks how well the student is doing on each topic, and saves it
# to a JSON file so progress persists between sessions.

import json
import os
from datetime import datetime, timezone

MASTERY_FILE = "mastery_data.json"

# How long since a topic was last tested before we treat the next
# question on it as a "recall check" instead of normal practice.
#
# For real use, this should be something like 20 * 3600 (20 hours) or
# 24 * 3600 (1 day), so recall is genuinely tested after time has
# passed. It's set low here (60 seconds) so you can actually see the
# feature working today without waiting a full day between tests.
RECALL_GAP_SECONDS = 60


def load_mastery():
    """Load saved mastery scores from disk, or start fresh if none exist."""
    if os.path.exists(MASTERY_FILE):
        with open(MASTERY_FILE, "r") as f:
            return json.load(f)
    return {}


def save_mastery(mastery):
    """Write the current mastery scores to disk."""
    with open(MASTERY_FILE, "w") as f:
        json.dump(mastery, f, indent=2)


def _blank_topic():
    return {
        "correct": 0,
        "total": 0,
        "recall": {"correct": 0, "total": 0},
        "last_tested": None,
    }


def seconds_since_last_test(mastery, topic):
    """Return how many seconds since this topic was last tested, or None if never."""
    if topic not in mastery or mastery[topic].get("last_tested") is None:
        return None
    last = datetime.fromisoformat(mastery[topic]["last_tested"])
    now = datetime.now(timezone.utc)
    return (now - last).total_seconds()


def is_recall_check(mastery, topic, gap_seconds=RECALL_GAP_SECONDS):
    """
    True if this topic was tested before AND enough time has passed
    that answering it again counts as testing recall, not first-pass
    learning.
    """
    elapsed = seconds_since_last_test(mastery, topic)
    return elapsed is not None and elapsed >= gap_seconds


def update_mastery(mastery, topic, correct, is_recall=False):
    """
    Update a topic's mastery after answering one question.

    'correct'/'total' track overall performance (same as before).
    'recall' tracks performance specifically on questions answered
    after a time gap — i.e. genuine memory recall, not just having
    just learned it a moment ago.
    """
    if topic not in mastery:
        mastery[topic] = _blank_topic()
    else:
        # Backfill any keys missing from older data so this never crashes
        # on a file saved before recall-tracking existed.
        mastery[topic].setdefault("recall", {"correct": 0, "total": 0})
        mastery[topic].setdefault("last_tested", None)

    mastery[topic]["total"] += 1
    if correct:
        mastery[topic]["correct"] += 1

    if is_recall:
        mastery[topic]["recall"]["total"] += 1
        if correct:
            mastery[topic]["recall"]["correct"] += 1

    mastery[topic]["last_tested"] = datetime.now(timezone.utc).isoformat()

    save_mastery(mastery)
    return mastery


def get_score(mastery, topic):
    """Return a topic's mastery as a percentage (0-100)."""
    if topic not in mastery or mastery[topic]["total"] == 0:
        return 0
    return round((mastery[topic]["correct"] / mastery[topic]["total"]) * 100)


def recommended_difficulty(score):
    """
    Decide which difficulty to serve next, based on current mastery %.

    - Below 40%: student is still struggling, stick to easy questions
    - 40-75%: developing understanding, medium questions
    - Above 75%: doing well, push with hard questions

    These thresholds are a simple starting point and can be tuned later
    as you get real usage data.
    """
    if score < 40:
        return "easy"
    elif score < 75:
        return "medium"
    else:
        return "hard"


def print_summary(mastery):
    """Print a readable summary of mastery across all topics."""
    print("\n📊 Your mastery so far:")
    if not mastery:
        print("  (no questions answered yet)")
        return
    for topic, stats in mastery.items():
        score = get_score(mastery, topic)
        line = f"  {topic:15s}: {score}%  ({stats['correct']}/{stats['total']} correct)"

        recall = stats.get("recall", {"correct": 0, "total": 0})
        if recall["total"] > 0:
            recall_pct = round((recall["correct"] / recall["total"]) * 100)
            line += f"   | recall: {recall_pct}% ({recall['correct']}/{recall['total']})"

        print(line)