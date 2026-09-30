# quiz.py
# The main program. Run this file to take a short quiz and see your
# mastery scores update per topic.

import random
from questions import QUESTION_BANK
from mastery import load_mastery, update_mastery, print_summary


def ask_question(q):
    """Show one question, get the student's answer, return True if correct."""
    print(f"\n[{q['topic']} - {q['difficulty']}]")
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

    # Shuffle so it's not always the same order every run
    questions = QUESTION_BANK.copy()
    random.shuffle(questions)

    # For the MVP, just ask 5 questions per session
    session_questions = questions[:5]

    print("🎓 Welcome to your Data Structures practice session!")
    print(f"You'll get {len(session_questions)} questions this round.\n")

    for q in session_questions:
        was_correct = ask_question(q)
        mastery = update_mastery(mastery, q["topic"], was_correct)

    print_summary(mastery)


if __name__ == "__main__":
    main()
