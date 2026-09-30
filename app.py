# app.py
# A Streamlit UI for the quiz engine with modern, beautiful design
# Run with: streamlit run app.py

import random
import streamlit as st
import pandas as pd
from datetime import datetime

from questions import QUESTION_BANK
from mastery import (
    load_mastery,
    update_mastery,
    get_score,
    recommended_difficulty,
    is_recall_check,
)

TOPICS = ["arrays", "linked_lists", "stacks", "queues"]

# Configure page
st.set_page_config(
    page_title="Plato — Data Structures Tutor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful UI
st.markdown("""
    <style>
    /* Main theme colors */
    :root {
        --primary-color: #6366f1;
        --secondary-color: #ec4899;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --danger-color: #ef4444;
        --light-bg: #f8fafc;
        --dark-text: #1e293b;
    }
    
    /* Overall styling */
    .main {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #6366f1 0%, #ec4899 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(99, 102, 241, 0.2);
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
    }
    
    .header-subtitle {
        font-size: 1rem;
        opacity: 0.9;
        margin: 0.5rem 0 0 0;
    }
    
    /* Question card */
    .question-card {
        background: white;
        border-left: 5px solid #6366f1;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        margin-bottom: 1.5rem;
    }
    
    /* Topic badge */
    .topic-badge {
        display: inline-block;
        background: #e0e7ff;
        color: #6366f1;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    .difficulty-easy {
        background: #d1fae5;
        color: #059669;
    }
    
    .difficulty-medium {
        background: #fef3c7;
        color: #b45309;
    }
    
    .difficulty-hard {
        background: #fee2e2;
        color: #991b1b;
    }
    
    /* Progress section */
    .progress-section {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    /* Stats cards */
    .stats-card {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .stats-value {
        font-size: 2rem;
        font-weight: 700;
        color: #6366f1;
        margin-bottom: 0.25rem;
    }
    
    .stats-label {
        font-size: 0.9rem;
        color: #64748b;
        font-weight: 600;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #6366f1 100%);
        color: white;
        border: none;
        padding: 0.7rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #4f46e5 100%);
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.3);
        transform: translateY(-2px);
    }
    
    /* Feedback messages */
    .success-message {
        background: #ecfdf5;
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 8px;
        color: #065f46;
        margin-bottom: 1rem;
    }
    
    .error-message {
        background: #fef2f2;
        border-left: 4px solid #ef4444;
        padding: 1rem;
        border-radius: 8px;
        color: #7f1d1d;
        margin-bottom: 1rem;
    }
    
    /* Recall badge */
    .recall-badge {
        display: inline-block;
        background: #fbbf24;
        color: #78350f;
        padding: 0.3rem 0.6rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
    }
    
    .learning-badge {
        display: inline-block;
        background: #93c5fd;
        color: #0c2d6b;
        padding: 0.3rem 0.6rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)


def pick_question(topic, difficulty, already_asked):
    """Match topic+difficulty, fall back if needed."""
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
    """Pick one adaptive question per topic."""
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


# Initialize state on first load
if "session" not in st.session_state:
    start_new_session()

# Header
st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🎓 Plato</h1>
        <p class="header-subtitle">Master Data Structures through Adaptive Learning</p>
    </div>
""", unsafe_allow_html=True)

# Quiz in progress
if st.session_state.index < len(st.session_state.session):
    item = st.session_state.session[st.session_state.index]
    q = item["question"]
    is_recall = item["is_recall"]

    # Progress bar with info
    col1, col2 = st.columns([3, 1])
    with col1:
        progress_value = st.session_state.index / len(st.session_state.session)
        st.progress(progress_value)
    with col2:
        st.metric("Question", f"{st.session_state.index + 1}/{len(st.session_state.session)}")

    # Question metadata
    col1, col2, col3 = st.columns(3)
    with col1:
        badge_type = "🔁 Recall Check" if is_recall else "📘 Learning"
        st.markdown(f"**{badge_type}**")
    with col2:
        st.markdown(f"**Topic:** `{q['topic'].title()}`")
    with col3:
        difficulty_color = {
            "easy": "🟢 Easy",
            "medium": "🟡 Medium",
            "hard": "🔴 Hard"
        }
        st.markdown(f"**Difficulty:** {difficulty_color.get(q['difficulty'], q['difficulty'])}")

    # Question card
    st.markdown(f"""
        <div class="question-card">
            <h2 style="margin-top: 0; color: #1e293b;">
                {q["question"]}
            </h2>
        </div>
    """, unsafe_allow_html=True)

    # Answer options
    option_labels = [f"{key}) {text}" for key, text in q["options"].items()]

    if not st.session_state.answered:
        st.markdown("### Choose your answer:")
        choice = st.radio(
            "Select an answer",
            option_labels,
            index=None,
            key=f"radio_{st.session_state.index}",
            label_visibility="collapsed"
        )

        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("✓ Submit Answer", disabled=(choice is None), use_container_width=True):
                chosen_key = choice.split(")")[0]
                correct = chosen_key == q["answer"]

                st.session_state.mastery = update_mastery(
                    st.session_state.mastery, q["topic"], correct, is_recall=is_recall
                )
                st.session_state.answered = True
                st.session_state.was_correct = correct
                st.rerun()

    else:
        # Show feedback
        if st.session_state.was_correct:
            st.markdown("""
                <div class="success-message">
                    <h3 style="margin-top: 0;">✅ Correct!</h3>
                    <p style="margin-bottom: 0;">Great job! You're building mastery.</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            correct_text = q["options"][q["answer"]]
            st.markdown(f"""
                <div class="error-message">
                    <h3 style="margin-top: 0;">❌ Not quite right</h3>
                    <p style="margin-bottom: 0;">The correct answer was <strong>{q["answer"]}) {correct_text}</strong></p>
                </div>
            """, unsafe_allow_html=True)

        # Next button
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("➡️ Next Question", use_container_width=True):
                st.session_state.index += 1
                st.session_state.answered = False
                st.session_state.selected = None
                st.rerun()

# Session complete
else:
    st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <h1 style="font-size: 3rem; margin-bottom: 0.5rem;">🎉 Session Complete!</h1>
            <p style="font-size: 1.2rem; color: #64748b;">Review your mastery progress below</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 📊 Your Mastery Progress")

    # Create stats overview
    mastery = st.session_state.mastery
    cols = st.columns(len(TOPICS))

    for idx, topic in enumerate(TOPICS):
        stats = mastery.get(topic)
        if not stats:
            continue

        score = get_score(mastery, topic)
        with cols[idx]:
            st.markdown(f"""
                <div class="stats-card">
                    <div class="stats-value">{score}%</div>
                    <div class="stats-label">{topic.replace('_', ' ').title()}</div>
                    <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 0.5rem;">
                        {stats['correct']}/{stats['total']} correct
                    </div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Detailed breakdown
    st.markdown("### 📈 Detailed Breakdown")

    for topic in TOPICS:
        stats = mastery.get(topic)
        if not stats:
            continue

        score = get_score(mastery, topic)
        recall = stats.get("recall", {"correct": 0, "total": 0})

        with st.expander(f"**{topic.title()}** — {score}% mastery", expanded=False):
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Overall Performance**")
                st.progress(score / 100)
                st.markdown(f"✓ {stats['correct']} correct out of {stats['total']} attempts")

            with col2:
                if recall["total"] > 0:
                    recall_pct = round((recall["correct"] / recall["total"]) * 100)
                    st.markdown("**Recall Performance**")
                    st.progress(recall_pct / 100)
                    st.markdown(f"✓ {recall['correct']} correct out of {recall['total']} recall checks")
                else:
                    st.markdown("*No recall checks yet for this topic*")

    st.markdown("---")

    # Action buttons
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("🔄 Start New Session", use_container_width=True):
            start_new_session()
            st.rerun()

    with col2:
        if st.button("📥 Export Progress", use_container_width=True):
            # Create export data
            export_data = []
            for topic in TOPICS:
                stats = mastery.get(topic, {})
                if stats:
                    recall = stats.get("recall", {"correct": 0, "total": 0})
                    export_data.append({
                        "Topic": topic.title(),
                        "Score (%)": get_score(mastery, topic),
                        "Correct": stats.get("correct", 0),
                        "Total": stats.get("total", 0),
                        "Recall (%)": round((recall["correct"] / recall["total"]) * 100) if recall["total"] > 0 else 0
                    })

            df = pd.DataFrame(export_data)
            csv = df.to_csv(index=False)
            st.download_button(
                label="📊 Download CSV",
                data=csv,
                file_name=f"plato_progress_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
