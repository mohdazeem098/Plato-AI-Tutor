# app.py
# A Streamlit UI for the same quiz engine from quiz.py, so you get a
# real interface instead of the terminal. Run with: streamlit run app.py

import random
import streamlit as st

from questions import QUESTION_BANK
from mastery import (
    load_mastery,
    update_mastery,
    get_score,
    recommended_difficulty,
    is_recall_check,
)

TOPICS = ["arrays", "linked_lists", "stacks", "queues"]

st.set_page_config(page_title="Plato — Data Structures Tutor", page_icon="🎓")


def pick_question(topic, difficulty, already_asked):
    """Same logic as quiz.py: match topic+difficulty, fall back if needed."""
    exact = [
        q for q in QUESTION_BANK
        if q["topic"] == topic and q["difficulty"] == difficulty and q["question"] not in already_asked
    ]
    if exact:
        return random.choice(exact)

    fallback = [
        q for q in QUESTION_BANK
        if q["topic"] == topic and q["question"] not in already_asked
    ]
    if fallback:
        return random.choice(fallback)

    return None


def build_session(mastery):
    """Pick one adaptive question per topic, same as quiz.py's main loop."""
    already_asked = set()
    session = []

    for topic in TOPICS:
        score = get_score(mastery, topic)
        difficulty = recommended_difficulty(score)
        q = pick_question(topic, difficulty, already_asked)
        if q is None:
            continue

        recall = is_recall_check(mastery, topic)
        already_asked.add(q["question"])
        session.append({"question": q, "is_recall": recall})

    return session


def start_new_session():
    st.session_state.mastery = load_mastery()
    st.session_state.session = build_session(st.session_state.mastery)
    st.session_state.index = 0
    st.session_state.answered = False
    st.session_state.selected = None
    st.session_state.was_correct = None


# ---------- Initialize state on first load ----------
if "session" not in st.session_state:
    start_new_session()

st.title("🎓 Plato — Data Structures Tutor")

# ---------- Quiz in progress ----------
if st.session_state.index < len(st.session_state.session):
    item = st.session_state.session[st.session_state.index]
    q = item["question"]
    is_recall = item["is_recall"]

    st.progress(st.session_state.index / len(st.session_state.session))
    label = "🔁 Recall check" if is_recall else "📘 Learning"
    st.caption(f"{label} · Topic: {q['topic']} · Difficulty: {q['difficulty']}")
    st.subheader(q["question"])

    option_labels = [f"{key}) {text}" for key, text in q["options"].items()]

    if not st.session_state.answered:
        choice = st.radio("Choose an answer:", option_labels, index=None, key=f"radio_{st.session_state.index}")

        if st.button("Submit", disabled=(choice is None)):
            chosen_key = choice.split(")")[0]
            correct = chosen_key == q["answer"]

            st.session_state.mastery = update_mastery(
                st.session_state.mastery, q["topic"], correct, is_recall=is_recall
            )
            st.session_state.answered = True
            st.session_state.was_correct = correct
            st.rerun()

    else:
        if st.session_state.was_correct:
            st.success("✅ Correct!")
        else:
            correct_text = q["options"][q["answer"]]
            st.error(f"❌ Not quite. The correct answer was {q['answer']}) {correct_text}")

        if st.button("Next question ➡️"):
            st.session_state.index += 1
            st.session_state.answered = False
            st.session_state.selected = None
            st.rerun()

# ---------- Session complete: show summary ----------
else:
    st.success("Session complete! 🎉")
    st.subheader("📊 Your mastery so far")

    mastery = st.session_state.mastery
    for topic in TOPICS:
        stats = mastery.get(topic)
        if not stats:
            continue

        score = get_score(mastery, topic)
        st.write(f"**{topic}** — {score}% ({stats['correct']}/{stats['total']} correct)")
        st.progress(score / 100)

        recall = stats.get("recall", {"correct": 0, "total": 0})
        if recall["total"] > 0:
            recall_pct = round((recall["correct"] / recall["total"]) * 100)
            st.caption(f"Recall performance: {recall_pct}% ({recall['correct']}/{recall['total']})")

    if st.button("Start another session"):
        start_new_session()
        st.rerun()
