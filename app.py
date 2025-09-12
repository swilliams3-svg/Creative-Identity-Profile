import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF
import io
import datetime

# ---------------------------
# GLOBAL TRAIT COLORS
# ---------------------------
trait_colors = {
    "Openness": "#1f77b4",          # blue
    "Conscientiousness": "#ff7f0e", # orange
    "Extraversion": "#2ca02c",      # green
    "Agreeableness": "#d62728",     # red
    "Neuroticism": "#9467bd",       # purple
    "Risk-taking": "#8c564b",       # brown
    "Imagination": "#e377c2",       # pink
}

# ---------------------------
# SAMPLE QUESTIONS (shortened for demo)
# ---------------------------
questions = {
    "Openness": [
        "I enjoy trying out new artistic experiences.",
        "I am curious about new ideas.",
    ],
    "Conscientiousness": [
        "I like to plan ahead carefully.",
        "I am detail-oriented in my work.",
    ],
    "Extraversion": [
        "I enjoy being the center of attention.",
        "I feel energized when around other people.",
    ],
    "Agreeableness": [
        "I try to be considerate of others’ feelings.",
        "I am cooperative in group settings.",
    ],
    "Neuroticism": [
        "I often feel anxious or worried.",
        "I get stressed easily.",
    ],
    "Risk-taking": [
        "I enjoy taking risks in my projects.",
        "I am comfortable with uncertainty.",
    ],
    "Imagination": [
        "I often think in images and metaphors.",
        "I create vivid mental pictures.",
    ],
}

# ---------------------------
# STREAMLIT APP
# ---------------------------
st.set_page_config(page_title="Creative Identity Profile", layout="wide")
st.title("🎨 Creative Identity Profile")

# Store answers
if "responses" not in st.session_state:
    st.session_state.responses = {trait: [None] * len(qs) for trait, qs in questions.items()}
if "completed" not in st.session_state:
    st.session_state.completed = False

# Questionnaire
if not st.session_state.completed:
    st.header("📝 Questionnaire")

    for trait, qs in questions.items():
        st.markdown(f"**<span style='color:{trait_colors[trait]}'>{trait}</span>**", unsafe_allow_html=True)
        for i, q in enumerate(qs):
            st.session_state.responses[trait][i] = st.radio(
                q,
                options=[None, 1, 2, 3, 4, 5],
                index=0 if st.session_state.responses[trait][i] is None else st.session_state.responses[trait][i],
                horizontal=True,
                key=f"{trait}_{i}",
            )

    if st.button("Finish"):
        # Check unanswered
        unanswered = []
        for trait, ans_list in st.session_state.responses.items():
            for i, ans in enumerate(ans_list):
                if ans is None:
                    unanswered.append((trait, i+1))

        if unanswered:
            st.warning(f"⚠️ You still have unanswered questions: {unanswered}. Please complete all before continuing.")
        else:
            st.session_state.completed = True
            st.experimental_rerun()

# ---------------------------
# RESULTS
# ---------------------------
else:
    st.header("📊 Your Results")

    # Calculate scores
    scores = {trait: np.mean(ans) for trait, ans in st.session_state.responses.items()}
    traits = list(scores.keys())
    values = list(scores.values())

    # Radar chart
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    angles = np.linspace(0, 2 * np.pi, len(traits), endpoint=False).tolist()
    angles += angles[:1]

    for trait in traits:
        vals = [scores[trait]] * len(traits)
        vals += vals[:1]
        ax.plot(angles, vals, color=trait_colors[trait], linewidth=2, label=trait)
        ax.fill(angles, vals, color=trait_colors[trait], alpha=0.1)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(traits, fontsize=10)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(["1", "2", "3", "4", "5"])
    ax.set_ylim(0, 5)
    ax.legend(bbox_to_anchor=(1.1, 1.05))
    st.pyplot(fig)

    # Trait insights
    st.subheader("🔎 Trait Insights")
    for trait, score in scores.items():
        st.markdown(f"- **<span style='color:{trait_colors[trait]}'>{trait}</span>**: {score:.2f}/5",
                    unsafe_allow_html=True)

