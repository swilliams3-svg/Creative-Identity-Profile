import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

st.set_page_config(page_title="Creative Identity Profile", layout="wide")

# --------------------------
# QUESTIONS (33 total)
# --------------------------
questions = {
    # Creative Traits
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

    # Big Five
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
# COLORS
# --------------------------
creative_colors = {
    "Originality": "#1f77b4",
    "Curiosity": "#ff7f0e",
    "Risk Taking": "#2ca02c",
    "Imagination": "#9467bd",
    "Discipline": "#d62728",
    "Collaboration": "#8c564b",
}

big5_colors = {
    "Openness": "#1f77b4",
    "Conscientiousness": "#ff7f0e",
    "Extraversion": "#2ca02c",
    "Agreeableness": "#9467bd",
    "Neuroticism": "#d62728",
}

# --------------------------
# SESSION STATE
# --------------------------
if "page" not in st.session_state:
    st.session_state.page = 0
if "responses" not in st.session_state:
    st.session_state.responses = {}

# --------------------------
# BUILD QUESTION LIST
# --------------------------
all_questions = []
for trait, qs in questions.items():
    for q in qs:
        all_questions.append((trait, q))

total_qs = len(all_questions)

# --------------------------
# QUIZ FLOW
# --------------------------
page = st.session_state.page
responses = st.session_state.responses

if page < total_qs:
    # Intro heading
    if page == 0:
        st.markdown("### Welcome to the Creative Identity Profile Quiz")
        st.write("This quiz explores both **creative traits** and the **Big Five personality traits**. "
                 "Answer each question honestly on a scale of 1–5, then view your results at the end.")

    # Current question
    trait, question = all_questions[page]
    st.markdown(f"**Question {page+1} of {total_qs}**")
    resp_key = f"resp_{page}"
    current_val = responses.get(resp_key, None)

    responses[resp_key] = st.radio(
        question,
        [1, 2, 3, 4, 5],
        horizontal=True,
        index=current_val - 1 if current_val else 0,
        key=resp_key
    )

    # Custom navigation buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        if page > 0:
            if st.button("Back", key="back_btn"):
                st.session_state.page -= 1
                st.rerun()
    with col2:
        if responses[resp_key] is not None:
            if st.button("Next Question", key="next_btn"):
                st.session_state.page += 1
                st.rerun()

    # Progress bar
    answered = sum(v is not None for v in responses.values())
    st.progress(answered / total_qs)

else:
    # --------------------------
    # RESULTS PAGE
    # --------------------------
    st.title("Your Creative Identity Profile")

    # Calculate scores
    scores = {trait: [] for trait in questions}
    for i, (trait, q) in enumerate(all_questions):
        if f"resp_{i}" in responses and responses[f"resp_{i}"] is not None:
            scores[trait].append(responses[f"resp_{i}"])

    avg_scores = {trait: np.mean(vals) if vals else 0 for trait, vals in scores.items()}

    # Display results summary
    st.subheader("Trait Scores")
    for trait, score in avg_scores.items():
        st.markdown(f"**{trait}**: {score:.2f}/5")

    # --------------------------
    # RADAR CHARTS SIDE BY SIDE
    # --------------------------
    creative_traits = list(creative_colors.keys())
    big5_traits = list(big5_colors.keys())

    def plot_radar(traits, scores, colors, title):
        labels = traits
        values = [scores[t] for t in traits]
        angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
        values += values[:1]
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(polar=True))
        ax.plot(angles, values, "o-", linewidth=2, color="black")
        ax.fill(angles, values, alpha=0.1, color="gray")

        for i, t in enumerate(traits):
            ax.plot([angles[i], angles[i]], [0, values[i]], color=colors[t], linewidth=3)
            ax.scatter(angles[i], values[i], color=colors[t], s=60, zorder=10, label=t)

        ax.set_thetagrids(np.degrees(angles[:-1]), labels)
        ax.set_ylim(0, 5)
        ax.set_title(title, size=12, pad=20)
        ax.legend(bbox_to_anchor=(1.2, 1.1))
        return fig

    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(plot_radar(creative_traits, avg_scores, creative_colors, "Creative Traits"))
    with col2:
        st.pyplot(plot_radar(big5_traits, avg_scores, big5_colors, "Big Five Traits"))

    # --------------------------
    # PDF Download
    # --------------------------
    def create_pdf():
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        c.setFont("Helvetica-Bold", 14)
        c.drawString(1*inch, height-1*inch, "Creative Identity Profile Results")

        y = height - 1.5*inch
        for trait, score in avg_scores.items():
            c.setFont("Helvetica", 12)
            c.drawString(1*inch, y, f"{trait}: {score:.2f}/5")
            y -= 0.3*inch

        c.showPage()
        c.save()
        buffer.seek(0)
        return buffer

    pdf_buffer = create_pdf()
    st.download_button("📄 Download PDF", data=pdf_buffer, file_name="creative_identity_profile.pdf", mime="application/pdf")

