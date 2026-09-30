# mastery.py
# Tracks how well the student is doing on each topic, and saves it
# to a JSON file so progress persists between sessions.

import json
import os

MASTERY_FILE = "mastery_data.json"


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


def update_mastery(mastery, topic, correct):
    """
    Update a topic's mastery after answering one question.

    We track 'correct' and 'total' answers per topic, then calculate
    a percentage score. This is a simple starting model — later this
    can be swapped for something more advanced like Bayesian Knowledge
    Tracing (the pyBKT library) without changing how the rest of the
    app calls this function.
    """
    if topic not in mastery:
        mastery[topic] = {"correct": 0, "total": 0}

    mastery[topic]["total"] += 1
    if correct:
        mastery[topic]["correct"] += 1

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
        print(f"  {topic:15s}: {score}%  ({stats['correct']}/{stats['total']} correct)")