import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
import random
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors

st.set_page_config(page_title="Creative Identity Profile", layout="centered")

# --------------------------
# Questions (33 total)
# --------------------------
questions = {
    # --- Creative Traits ---
    "Originality": [
        "I often come up with ideas that are different from others.",
        "I enjoy finding unique solutions to problems.",
        "I like expressing myself in unusual or distinctive ways."
    ],
    "Curiosity": [
        "I enjoy exploring new topics just for the sake of learning.",
        "I often ask questions about how things work.",
        "I seek out opportunities to broaden my knowledge."
    ],
    "Risk Taking": [
        "I am comfortable taking chances to try something new.",
        "I am willing to make mistakes in order to learn.",
        "I often push myself outside of my comfort zone."
    ],
    "Imagination": [
        "I often create mental pictures or stories in my mind.",
        "I enjoy activities that let me fantasize or dream.",
        "I can easily picture possibilities beyond what exists."
    ],
    "Discipline": [
        "I set aside regular time to work on creative projects.",
        "I stay focused even when tasks become challenging.",
        "I can finish creative ideas even when motivation fades."
    ],
    "Collaboration": [
        "I enjoy sharing ideas with others when working on projects.",
        "I believe teamwork can enhance creative outcomes.",
        "I listen openly to others’ perspectives when creating."
    ],

    # --- Big Five ---
    "Openness": [
        "I enjoy trying out new activities and experiences.",
        "I am open to different perspectives and ideas.",
        "I appreciate art, music, or literature deeply."
    ],
    "Conscientiousness": [
        "I pay attention to details when working on tasks.",
        "I like to plan things carefully before starting.",
        "I follow through with commitments I make."
    ],
    "Extraversion": [
        "I feel energized by spending time with other people.",
        "I like being the center of attention in groups.",
        "I often start conversations with strangers."
    ],
    "Agreeableness": [
        "I am considerate of other people’s feelings.",
        "I like cooperating with others rather than competing.",
        "I tend to trust people until given a reason not to."
    ],
    "Neuroticism": [
        "I often feel stressed or anxious about small things.",
        "I get upset easily if things don’t go my way.",
        "I frequently worry about the future."
    ],
}

# --------------------------
# Trait Colors
# --------------------------
trait_colors = {
    "Originality": "#1f77b4",
    "Curiosity": "#ff7f0e",
    "Risk Taking": "#2ca02c",
    "Imagination": "#9467bd",
    "Discipline": "#d62728",
    "Collaboration": "#8c564b",
    "Openness": "#e377c2",
    "Conscientiousness": "#7f7f7f",
    "Extraversion": "#bcbd22",
    "Agreeableness": "#17becf",
    "Neuroticism": "#ff9896"
}

# --------------------------
# Helper: Level
# --------------------------
def get_level(score: float) -> str:
    if score >= 4:
        return "High"
    elif score >= 2.5:
        return "Medium"
    else:
        return "Low"

# --------------------------
# Helper: Radar Chart
# --------------------------
def radar_chart(scores: dict, colors: dict, title="") -> io.BytesIO:
    labels = list(scores.keys())
    num_vars = len(labels)

    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    values = list(scores.values())
    values += values[:1]

    ax.plot(angles, values, linewidth=1.5, color="black")
    ax.fill(angles, values, alpha=0.05, color="gray")

    for i, (trait, score) in enumerate(scores.items()):
        ax.plot([angles[i], angles[i+1]], [score, values[i+1]],
                color=colors[trait], linewidth=3)
        ax.scatter(angles[i], score, color=colors[trait], s=60, zorder=10, label=trait)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylim(0, 5)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(["1", "2", "3", "4", "5"])
    plt.title(title, size=12, weight="bold")
    ax.legend(bbox_to_anchor=(1.15, 1.1))

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)
    return buf

# --------------------------
# Streamlit App
# --------------------------
st.title("Creative Identity & Personality Profile")
st.write("This quiz explores both your **creative traits** and your **personality traits (Big Five)**. "
         "Answer honestly on a 1–5 scale. Your results will generate personal insights and visual charts.")

if "page" not in st.session_state:
    st.session_state.page = 0
if "responses" not in st.session_state:
    st.session_state.responses = {}

question_list = []
for trait, qs in questions.items():
    for q in qs:
        question_list.append((trait, q))

total_qs = len(question_list)

# Current question
page = st.session_state.page
if page < total_qs:
    trait, qtext = question_list[page]
    st.subheader(f"Question {page+1} of {total_qs}")
    choice = st.radio(qtext, [1, 2, 3, 4, 5],
                      horizontal=True,
                      key=f"q_{page}",
                      index=None)

    cols = st.columns([1, 1])
    with cols[0]:
        if st.button("⬅ Back", use_container_width=True, disabled=(page == 0)):
            st.session_state.page -= 1
            st.experimental_rerun()
    with cols[1]:
        if st.button("Next Question ➡", use_container_width=True, disabled=(choice is None)):
            st.session_state.responses[page] = (trait, choice)
            st.session_state.page += 1
            st.experimental_rerun()

    # Progress bar
    answered = len(st.session_state.responses)
    st.progress(answered / total_qs)

else:
    st.success("All questions complete — here are your results!")

    # Collect scores
    scores = {t: [] for t in questions}
    for _, (trait, val) in st.session_state.responses.items():
        scores[trait].append(val)
    avg_scores = {t: np.mean(v) for t, v in scores.items()}

    # Split creative vs big five
    creative_scores = {t: avg_scores[t] for t in ["Originality", "Curiosity", "Risk Taking", "Imagination", "Discipline", "Collaboration"]}
    big5_scores = {t: avg_scores[t] for t in ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"]}

    c1, c2 = st.columns(2)
    with c1:
        st.image(radar_chart(creative_scores, trait_colors, "Creative Traits"), use_container_width=True)
    with c2:
        st.image(radar_chart(big5_scores, trait_colors, "Big Five Traits"), use_container_width=True)

    # Trait summaries
    st.subheader("Your Trait Insights")
    for trait, score in avg_scores.items():
        st.markdown(
            f"<div style='background-color:{trait_colors[trait]}20; padding:0.6rem; border-radius:8px; margin:0.4rem 0;'>"
            f"<span style='color:{trait_colors[trait]}; font-weight:bold'>{trait} ({get_level(score)})</span> — {score:.2f}/5"
            f"</div>", unsafe_allow_html=True
        )

    # Download PDF placeholder
    st.info("📄 Downloadable PDF report coming next.")

