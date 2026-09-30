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

st.markdown(
    """
    <style>
        :root {
            --bg: #0f172a;
            --panel: rgba(15, 23, 42, 0.75);
            --panel-soft: rgba(30, 41, 59, 0.7);
            --card: rgba(15, 23, 42, 0.95);
            --primary: #8b5cf6;
            --primary-soft: #a78bfa;
            --accent: #22c55e;
            --warning: #f59e0b;
            --danger: #ef4444;
            --text: #e2e8f0;
            --muted: #a5b4cf;
            --border: rgba(148, 163, 184, 0.22);
        }

        .stApp {
            background: radial-gradient(circle at top left, rgba(139, 92, 246, 0.18), transparent 28%),
                        radial-gradient(circle at bottom right, rgba(34, 197, 94, 0.12), transparent 22%),
                        #020817;
            color: var(--text);
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1100px;
        }

        .hero {
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.22), rgba(34, 197, 94, 0.12));
            border: 1px solid var(--border);
            border-radius: 22px;
            padding: 1.5rem 1.5rem 1rem 1.5rem;
            margin-bottom: 1.25rem;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.35);
        }

        .hero-badge {
            display: inline-block;
            padding: 0.35rem 0.7rem;
            border-radius: 999px;
            background: rgba(167, 139, 250, 0.16);
            border: 1px solid rgba(167, 139, 250, 0.35);
            color: #ddd6fe;
            font-size: 0.72rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            font-weight: 700;
            margin-bottom: 0.8rem;
        }

        h1 {
            font-size: 2.5rem !important;
            margin-bottom: 0.2rem !important;
        }

        .subtitle {
            color: var(--muted);
            font-size: 1.02rem;
            margin-bottom: 0;
        }

        .metric-card {
            background: rgba(15, 23, 42, 0.58);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 1rem 1.1rem;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.03);
        }

        .stat-label {
            color: var(--muted);
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        .stat-value {
            font-size: 1.8rem;
            font-weight: 800;
            margin-top: 0.25rem;
            color: var(--text);
        }

        .pill {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.4rem 0.8rem;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 700;
            margin-bottom: 0.8rem;
        }

        .pill-learning {
            background: rgba(59, 130, 246, 0.12);
            border: 1px solid rgba(96, 165, 250, 0.35);
            color: #bfdbfe;
        }

        .pill-recall {
            background: rgba(245, 158, 11, 0.12);
            border: 1px solid rgba(251, 191, 36, 0.35);
            color: #fde68a;
        }

        .question-card {
            background: rgba(15, 23, 42, 0.72);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 1.4rem 1.3rem;
            margin-top: 1rem;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.2);
        }

        .topic-tag {
            display: inline-block;
            background: rgba(34, 197, 94, 0.12);
            border: 1px solid rgba(34, 197, 94, 0.35);
            color: #bbf7d0;
            padding: 0.35rem 0.7rem;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            text-transform: capitalize;
        }

        .question-title {
            font-size: 1.55rem !important;
            line-height: 1.4;
            margin-top: 0.5rem !important;
            margin-bottom: 0.9rem !important;
        }

        .answer-option {
            background: rgba(15, 23, 42, 0.75);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 0.65rem 0.9rem;
            margin: 0.45rem 0;
        }

        .result-box {
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 1rem 1.2rem;
            margin-top: 1rem;
            background: rgba(15, 23, 42, 0.7);
        }

        .success-box {
            border-color: rgba(34, 197, 94, 0.45);
            background: rgba(34, 197, 94, 0.08);
        }

        .error-box {
            border-color: rgba(239, 68, 68, 0.45);
            background: rgba(239, 68, 68, 0.08);
        }

        .summary-card {
            background: rgba(15, 23, 42, 0.72);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 1rem 1.1rem;
            margin-bottom: 1rem;
        }

        .summary-topic {
            font-size: 1.1rem;
            font-weight: 700;
            text-transform: capitalize;
            margin-bottom: 0.3rem;
        }

        .stButton > button {
            border-radius: 12px !important;
            font-weight: 700 !important;
            padding: 0.7rem 1.2rem !important;
            background: linear-gradient(135deg, #8b5cf6, #a78bfa) !important;
            border: none !important;
            color: white !important;
            box-shadow: 0 8px 18px rgba(139, 92, 246, 0.35) !important;
        }

        .stButton > button:hover {
            filter: brightness(1.08);
        }

        .secondary-button > button {
            background: rgba(15, 23, 42, 0.8) !important;
            border: 1px solid rgba(148, 163, 184, 0.32) !important;
            box-shadow: none !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


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

st.markdown(
    """
    <div class="hero">
        <div class="hero-badge">Adaptive Learning</div>
        <h1>🎓 Plato</h1>
        <p class="subtitle">Data Structures Tutor for steady progress, smarter recall, and faster mastery.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.write("### Session overview")
    answered = sum(
        stats.get("total", 0)
        for stats in st.session_state.mastery.values()
        if isinstance(stats, dict)
    )
    st.metric("Questions answered", answered)

    mastery_score = 0
    if st.session_state.mastery:
        topic_scores = [get_score(st.session_state.mastery, topic) for topic in TOPICS]
        mastery_score = round(sum(topic_scores) / len(topic_scores)) if topic_scores else 0
    st.metric("Avg. mastery", f"{mastery_score}%")
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("### Topics")
    for topic in TOPICS:
        score = get_score(st.session_state.mastery, topic)
        st.caption(f"{topic.replace('_', ' ').title()} · {score}%")
        st.progress(score / 100)

# ---------- Quiz in progress ----------
if st.session_state.index < len(st.session_state.session):
    item = st.session_state.session[st.session_state.index]
    q = item["question"]
    is_recall = item["is_recall"]

    total_questions = len(st.session_state.session) if st.session_state.session else 1
    progress_value = st.session_state.index / total_questions

    st.progress(progress_value, text=f"Question {st.session_state.index + 1} of {total_questions}")

    label = "🔁 Recall check" if is_recall else "📘 Learning"
    pill_class = "pill-recall" if is_recall else "pill-learning"
    st.markdown(f'<div class="pill {pill_class}">{label}</div>', unsafe_allow_html=True)
    st.caption(f"Topic: {q['topic']} · Difficulty: {q['difficulty']}")

    st.markdown(
        """
        <div class="question-card">
            <div class="topic-tag">{topic}</div>
            <div class="question-title">{question}</div>
        </div>
        """.format(topic=q["topic"], question=q["question"]),
        unsafe_allow_html=True,
    )

    option_keys = list(q["options"].keys())

    if not st.session_state.answered:
        choice = st.radio(
            "Choose an answer:",
            option_keys,
            index=None,
            key=f"radio_{st.session_state.index}",
            format_func=lambda key: f"{key}) {q['options'][key]}",
        )

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Submit answer", disabled=(choice is None), use_container_width=True):
                correct = choice == q["answer"]
                st.session_state.mastery = update_mastery(
                    st.session_state.mastery, q["topic"], correct, is_recall=is_recall
                )
                st.session_state.answered = True
                st.session_state.was_correct = correct
                st.rerun()

    else:
        if st.session_state.was_correct:
            st.markdown(
                """
                <div class="result-box success-box">
                    <h3 style='margin:0 0 0.3rem 0; color:#bbf7d0;'>✅ Correct!</h3>
                    <div style='color:#dcfce7;'>Nice work — keep the momentum going.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            correct_text = q["options"][q["answer"]]
            st.markdown(
                f"""
                <div class="result-box error-box">
                    <h3 style='margin:0 0 0.3rem 0; color:#fecaca;'>❌ Not quite</h3>
                    <div style='color:#fee2e2;'>The correct answer was <strong>{q['answer']}) {correct_text}</strong>.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Next question ➡️", use_container_width=True):
                st.session_state.index += 1
                st.session_state.answered = False
                st.session_state.selected = None
                st.rerun()

# ---------- Session complete: show summary ----------
else:
    st.markdown(
        """
        <div class="hero" style="margin-top: 1rem;">
            <div class="hero-badge">Session complete</div>
            <h2>🎉 Great job</h2>
            <p class="subtitle">You finished this adaptive practice run. Here's how your mastery is shaping up.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    mastery = st.session_state.mastery
    for topic in TOPICS:
        stats = mastery.get(topic)
        if not stats:
            continue

        score = get_score(mastery, topic)
        recall = stats.get("recall", {"correct": 0, "total": 0})

        st.markdown(
            """
            <div class="summary-card">
                <div class="summary-topic">{topic}</div>
                <div>{score}% ({correct}/{total} correct)</div>
            </div>
            """.format(
                topic=topic,
                score=score,
                correct=stats["correct"],
                total=stats["total"],
            ),
            unsafe_allow_html=True,
        )
        st.progress(score / 100)

        if recall["total"] > 0:
            recall_pct = round((recall["correct"] / recall["total"]) * 100)
            st.caption(f"Recall performance: {recall_pct}% ({recall['correct']}/{recall['total']})")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Start another session", use_container_width=True):
            start_new_session()
            st.rerun()
    with col2:
        st.button("Close", use_container_width=True, disabled=True)
