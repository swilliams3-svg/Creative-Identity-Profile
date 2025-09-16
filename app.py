import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
import random

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

# Register font for compatibility (especially if we need non-Latin later)
pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))

st.set_page_config(page_title="Creative Identity Profile", layout="centered")

# --------------------------
# Creative Traits Questions
# --------------------------
creative_traits = {
    "Openness": [
        "I enjoy exploring new ideas and perspectives.",
        "I am open to trying new experiences.",
        "I seek out diverse viewpoints."
    ],
    "Curiosity": [
        "I often ask questions to learn more.",
        "I enjoy investigating how things work.",
        "I get excited about discovering new things."
    ],
    "RiskTaking": [
        "I am willing to take risks to pursue ideas.",
        "I am comfortable with uncertainty in projects.",
        "I see mistakes as opportunities to learn."
    ],
    "Imagination": [
        "I often think in images and metaphors.",
        "I create original stories, ideas, or scenarios.",
        "I visualise possibilities beyond the present."
    ],
    "Collaboration": [
        "I enjoy working with others on creative projects.",
        "I value feedback and input from teammates.",
        "I build on others’ ideas to create new ones."
    ],
    "Persistence": [
        "I continue working even when ideas are difficult.",
        "I overcome setbacks in creative projects.",
        "I stay motivated through challenges."
    ],
}

# --------------------------
# Big Five Questions
# --------------------------
big5_traits = {
    "Openness": [
        "I have a vivid imagination.",
        "I enjoy thinking about abstract ideas.",
        "I like to try new and different things."
    ],
    "Conscientiousness": [
        "I pay attention to details.",
        "I like to be organised.",
        "I follow through with my plans."
    ],
    "Extraversion": [
        "I feel comfortable around people.",
        "I am the life of the party.",
        "I talk to a lot of different people at social events."
    ],
    "Agreeableness": [
        "I sympathise with others’ feelings.",
        "I take time out for others.",
        "I make people feel at ease."
    ],
    "Neuroticism": [
        "I get stressed out easily.",
        "I worry about things.",
        "I get upset easily."
    ],
}

# --------------------------
# Colour Palettes
# --------------------------
creative_colors = {
    "Openness": "#FF7F50",        # Coral
    "Curiosity": "#6A5ACD",       # SlateBlue
    "RiskTaking": "#32CD32",      # LimeGreen
    "Imagination": "#FF69B4",     # HotPink
    "Collaboration": "#20B2AA",   # LightSeaGreen
    "Persistence": "#FFA500",     # Orange
}

big5_colors = {
    "Openness": "#1F77B4",          # Navy-ish Blue
    "Conscientiousness": "#2CA02C", # Forest Green
    "Extraversion": "#D62728",      # Dark Red
    "Agreeableness": "#9467BD",     # Deep Purple
    "Neuroticism": "#8C564B",       # Brownish
}

# --------------------------
# Session State Init
# --------------------------
if "page" not in st.session_state:
    st.session_state.page = "Quiz"
if "responses" not in st.session_state:
    st.session_state.responses = {}
# --------------------------
# Helper: Likert Scale Options
# --------------------------
likert_options = {
    "Strongly Disagree": 1,
    "Disagree": 2,
    "Neutral": 3,
    "Agree": 4,
    "Strongly Agree": 5
}

# --------------------------
# Save Response
# --------------------------
def save_response(trait, q_idx, answer):
    st.session_state.responses[(trait, q_idx)] = answer

# --------------------------
# Calculate Scores
# --------------------------
def calculate_scores():
    creative_scores = {trait: 0 for trait in creative_traits}
    big5_scores = {trait: 0 for trait in big5_traits}

    # Tally scores
    for (trait, q_idx), ans in st.session_state.responses.items():
        if trait in creative_traits:
            creative_scores[trait] += likert_options[ans]
        elif trait in big5_traits:
            big5_scores[trait] += likert_options[ans]

    # Normalise
    for trait in creative_scores:
        creative_scores[trait] = creative_scores[trait] / (len(creative_traits[trait]) * 5) * 100
    for trait in big5_scores:
        big5_scores[trait] = big5_scores[trait] / (len(big5_traits[trait]) * 5) * 100

    return creative_scores, big5_scores

# --------------------------
# Radar Chart Function
# --------------------------
def make_radar_chart(scores, trait_colors, title):
    traits = list(scores.keys())
    values = list(scores.values())

    N = len(traits)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))

    ax.fill(angles, values, alpha=0.25, color="grey")
    ax.plot(angles, values, color="black", linewidth=1.5)

    # Add each trait’s color
    for i, trait in enumerate(traits):
        ax.plot(angles[i], values[i], 'o', color=trait_colors[trait], label=trait)

    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(traits, fontsize=10)
    ax.set_title(title, size=14, weight='bold', y=1.1)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", dpi=150)
    plt.close(fig)
    buf.seek(0)
    return buf

# --------------------------
# Academic Summaries (for App inline + PDF end)
# --------------------------
creative_summaries = {
    "Openness": "Linked to divergent thinking and the ability to generate many unique ideas.",
    "Curiosity": "Supports exploration and questioning, often seen as the fuel for creativity.",
    "RiskTaking": "Essential for creative breakthroughs, since innovation often involves uncertainty.",
    "Imagination": "Relates to mental simulation, conceptual blending, and metaphorical thinking.",
    "Collaboration": "Social creativity benefits from diverse perspectives and teamwork.",
    "Persistence": "Sustained effort is often the difference between idea and real innovation.",
}

big5_summaries = {
    "Openness": "Associated with intellectual curiosity, novelty seeking, and artistic interests.",
    "Conscientiousness": "Relates to organisation, reliability, and self-discipline.",
    "Extraversion": "Tied to sociability, assertiveness, and positive emotionality.",
    "Agreeableness": "Reflects empathy, compassion, and cooperation.",
    "Neuroticism": "Represents sensitivity to stress and emotional reactivity.",
}
# --------------------------
# PDF Generation
# --------------------------
def create_pdf(creative_scores, big5_scores, creative_summaries, big5_summaries,
               chart_buf_creative, chart_buf_big5):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="CenterTitle", alignment=TA_CENTER, fontSize=16, leading=20, spaceAfter=15))
    styles.add(ParagraphStyle(name="SubHeading", fontSize=13, leading=16, spaceAfter=10))
    styles.add(ParagraphStyle(name="Body", fontSize=10, leading=14))

    flowables = []

    # Title
    flowables.append(Paragraph("Creative Identity Profile", styles["CenterTitle"]))
    flowables.append(Spacer(1, 12))

    # Radar Charts
    for chart_buf, title in [(chart_buf_creative, "Creative Traits"), (chart_buf_big5, "Big Five Traits")]:
        img = Image(ImageReader(chart_buf), width=400, height=400)
        flowables.append(Paragraph(title, styles["SubHeading"]))
        flowables.append(img)
        flowables.append(Spacer(1, 12))

    # Scores and summaries
    flowables.append(Paragraph("Creative Traits Scores", styles["SubHeading"]))
    for trait, score in creative_scores.items():
        summary = creative_summaries[trait]
        flowables.append(Paragraph(f"<b>{trait}:</b> {score:.1f}% - {summary}", styles["Body"]))
        flowables.append(Spacer(1, 6))

    flowables.append(Spacer(1, 12))
    flowables.append(Paragraph("Big Five Traits Scores", styles["SubHeading"]))
    for trait, score in big5_scores.items():
        summary = big5_summaries[trait]
        flowables.append(Paragraph(f"<b>{trait}:</b> {score:.1f}% - {summary}", styles["Body"]))
        flowables.append(Spacer(1, 6))

    # Academic section at the end
    flowables.append(Spacer(1, 20))
    flowables.append(Paragraph("Scientific Background", styles["SubHeading"]))
    flowables.append(Paragraph(
        "This quiz integrates two major areas of psychology: "
        "the Big Five personality traits (Costa & McCrae, 1992) "
        "and research on creativity, including divergent and convergent thinking, "
        "imagination, persistence, and collaboration (e.g., Runco, Guilford, Amabile, Sternberg). "
        "The Creative Traits are drawn from decades of creativity research, "
        "while the Big Five provides a well-validated model of personality. "
        "Together, they provide a rounded perspective on both the personality foundations "
        "and the creative processes that shape identity.",
        styles["Body"]
    ))

    doc.build(flowables)
    buffer.seek(0)
    return buffer

# --------------------------
# PAGE: Results
# --------------------------
if st.session_state.page == "Results":
    st.title("Your Results")

    creative_scores, big5_scores = calculate_scores()

    # Radar charts
    chart_buf_creative = make_radar_chart(creative_scores, creative_colors, "Creative Traits Profile")
    chart_buf_big5 = make_radar_chart(big5_scores, big5_colors, "Big Five Personality Profile")

    st.image(chart_buf_creative, caption="Creative Traits", use_container_width=True)
    st.image(chart_buf_big5, caption="Big Five Traits", use_container_width=True)

    # Collapsible Creative Traits section
    with st.expander("🎨 Creative Traits Breakdown", expanded=False):
        for trait, score in creative_scores.items():
            st.markdown(f"**{trait}:** {score:.1f}%")
            st.write(creative_summaries[trait])

    # Collapsible Big Five section
    with st.expander("🧠 Big Five Breakdown", expanded=False):
        for trait, score in big5_scores.items():
            st.markdown(f"**{trait}:** {score:.1f}%")
            st.write(big5_summaries[trait])
    # Scientific background in app
    with st.expander("📚 Scientific Background", expanded=False):
        st.write("""
        This profile draws on two streams of psychology:
        - **The Big Five Personality Model** (Costa & McCrae, 1992), one of the most widely validated models of personality.  
        - **Creativity Research** from scholars such as Guilford, Torrance, Runco, Amabile, Sternberg, and Boden, 
          focusing on originality, imagination, curiosity, persistence, and collaboration.  

        By integrating these, the profile provides insights into both the personality foundations 
        and the creative processes shaping your identity.
        """)

    # PDF Download
    pdf_buf = create_pdf(
        creative_scores,
        big5_scores,
        creative_summaries,
        big5_summaries,
        chart_buf_creative,
        chart_buf_big5
    )
    st.download_button(
        "⬇️ Download Full Report (PDF)",
        data=pdf_buf,
        file_name="Creative_Identity_Profile.pdf",
        mime="application/pdf"
    )

# --------------------------
# PAGE: Quiz
# --------------------------
if st.session_state.page == "Quiz":
    st.title("Creative Identity & Personality Quiz")

    questions = st.session_state.questions
    q_index = st.session_state.q_index
    trait, question = questions[q_index]

    st.write(f"**Q{q_index+1}/{len(questions)} — {trait}:** {question}")

    cols = st.columns(5)
    for i, col in enumerate(cols, start=1):
        if col.button(str(i), key=f"q{q_index}_a{i}"):
            st.session_state.responses[q_index] = i
            if q_index + 1 < len(questions):
                st.session_state.q_index += 1
            else:
                st.session_state.page = "Results"
            st.rerun()

    if q_index > 0:
        if st.button("⬅️ Back"):
            st.session_state.q_index -= 1
            st.rerun()
