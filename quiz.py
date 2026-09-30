# quiz.py
# The main program. Run this file to take a short quiz and see your
# mastery scores update per topic.

import random
from questions import QUESTION_BANK
from mastery import (
    load_mastery,
    update_mastery,
    print_summary,
    get_score,
    recommended_difficulty,
    is_recall_check,
)

TOPICS = ["arrays", "linked_lists", "stacks", "queues"]


def pick_question(topic, difficulty, already_asked):
    """
    Find a question matching this topic and difficulty that hasn't
    been asked yet this session. Falls back to any unused question on
    the topic if no exact difficulty match is available (keeps the
    MVP working even with a small question bank).
    """
    exact_matches = [
        q for q in QUESTION_BANK
        if q["topic"] == topic and q["difficulty"] == difficulty and q["question"] not in already_asked
    ]
    if exact_matches:
        return random.choice(exact_matches)

    fallback_matches = [
        q for q in QUESTION_BANK
        if q["topic"] == topic and q["question"] not in already_asked
    ]
    if fallback_matches:
        return random.choice(fallback_matches)

    return None  # every question on this topic has already been asked


def ask_question(q, is_recall):
    """Show one question, get the student's answer, return True if correct."""
    label = "🔁 RECALL CHECK" if is_recall else "📘 learning"
    print(f"\n[{q['topic']} - {q['difficulty']}] {label}")
    print(q["question"])
    for key, option_text in q["options"].items():
        print(f"  {key}) {option_text}")

    answer = input("Your answer: ").strip().upper()

    if answer == q["answer"]:
        print("✅ Correct!")
        return True
    else:
        correct_text = q["options"][q["answer"]]
        print(f"❌ Not quite. The correct answer was {q['answer']}) {correct_text}")
        return False


def main():
    mastery = load_mastery()
    already_asked = set()

    print("🎓 Welcome to your Data Structures practice session!")
    print("Questions will adapt to your current mastery in each topic.\n")

    # Ask one question per topic, at a difficulty matched to current mastery
    for topic in TOPICS:
        score = get_score(mastery, topic)
        difficulty = recommended_difficulty(score)
        q = pick_question(topic, difficulty, already_asked)

        if q is None:
            continue  # skip if we've run out of unique questions for this topic

        recall_check = is_recall_check(mastery, topic)

        already_asked.add(q["question"])
        was_correct = ask_question(q, recall_check)
        mastery = update_mastery(mastery, topic, was_correct, is_recall=recall_check)

    print_summary(mastery)


if __name__ == "__main__":
    main()