import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.utils import ImageReader

st.set_page_config(page_title="Creative Identity Profile", layout="centered")

# --------------------------
# Creative Traits
# --------------------------
creative_traits = {
    "Originality": [
        "I often come up with ideas that others don’t think of.",
        "I enjoy finding new ways to solve problems.",
        "I like to put a unique spin on familiar things."
    ],
    "Flexibility": [
        "I can easily see different perspectives on a situation.",
        "I enjoy trying out new methods.",
        "I adapt well when things change unexpectedly."
    ],
    "Elaboration": [
        "I like to add detail to my ideas to make them stronger.",
        "I expand on ideas to see where they can go.",
        "I enjoy developing initial thoughts into full concepts."
    ],
    "Risk-Taking": [
        "I don’t mind going against the crowd with my ideas.",
        "I’m willing to try things even if they might fail.",
        "I embrace uncertainty in creative projects."
    ],
    "Openness": [
        "I enjoy exploring unusual or unconventional ideas.",
        "I am open to feedback and new perspectives.",
        "I actively seek out novel experiences."
    ],
    "Curiosity": [
        "I ask a lot of questions about how things work.",
        "I like learning about topics outside my main interests.",
        "I am fascinated by new discoveries."
    ]
}

# --------------------------
# Big Five Traits (fixed key for Openness)
# --------------------------
big5_traits = {
    "Conscientiousness": [
        "I like to keep things organized.",
        "I pay attention to details.",
        "I get chores done right away."
    ],
    "Extraversion": [
        "I feel comfortable around people.",
        "I start conversations.",
        "I don’t mind being the center of attention."
    ],
    "Agreeableness": [
        "I am interested in other people’s problems.",
        "I sympathize with others’ feelings.",
        "I take time out for others."
    ],
    "Neuroticism": [
        "I often feel anxious about things.",
        "I get upset easily.",
        "I worry about many things."
    ],
    "Openness_Big5": [
        "I enjoy trying new activities and experiences.",
        "I have a broad range of interests.",
        "I am curious about many different things."
    ]
}

# --------------------------
# Summaries (shortened for brevity here — fill with full text if you had it before)
# --------------------------
creative_summaries = {t: {"High": "High summary", "Medium": "Medium summary", "Low": "Low summary"} for t in creative_traits}
big5_summaries = {t: {"High": "High summary", "Medium": "Medium summary", "Low": "Low summary"} for t in big5_traits}

# --------------------------
# Utility functions
# --------------------------
def get_level(score):
    if score >= 3.67: return "High"
    elif score >= 2.34: return "Medium"
    else: return "Low"

def radar_chart(scores, colors, title):
    labels = list(scores.keys())
    values = list(scores.values())
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]
    fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(polar=True))
    ax.plot(angles, values, "o-", linewidth=2)
    ax.fill(angles, values, alpha=0.25)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_title(title, size=12, weight="bold")
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf

def create_pdf(creative_scores, big5_scores, creative_summaries, big5_summaries,
               chart_buf_creative, chart_buf_big5):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    width, height = A4
    styles = getSampleStyleSheet()
    normal = styles["Normal"]

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, height - 40, "Creative Identity & Personality Profile")

    img1 = ImageReader(chart_buf_creative)
    img2 = ImageReader(chart_buf_big5)
    c.drawImage(img1, 60, height - 280, width=200, height=200, mask='auto')
    c.drawImage(img2, 300, height - 280, width=200, height=200, mask='auto')

    y = height - 320
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "Creative Trait Insights")
    y -= 20
    for trait, score in creative_scores.items():
        level = get_level(score)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, f"{trait} ({level}) — {score:.2f}/5")
        y -= 12
        p = Paragraph(creative_summaries[trait][level], normal)
        w, h = p.wrap(width-100, 200)
        p.drawOn(c, 60, y-h)
        y -= (h+10)

    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "Big Five Trait Insights")
    y -= 20
    for trait, score in big5_scores.items():
        display_trait = trait.replace("_Big5", "")
        level = get_level(score)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, f"{display_trait} ({level}) — {score:.2f}/5")
        y -= 12
        p = Paragraph(big5_summaries[trait][level], normal)
        w, h = p.wrap(width-100, 200)
        p.drawOn(c, 60, y-h)
        y -= (h+10)

    c.showPage()
    c.save()
    buf.seek(0)
    return buf

# --------------------------
# Build all questions
# --------------------------
all_questions = []
for trait, qs in creative_traits.items():
    for q in qs:
        all_questions.append((trait, q))
for trait, qs in big5_traits.items():
    for q in qs:
        all_questions.append((trait, q))

total_qs = len(all_questions)  # should be 33

# --------------------------
# Session state
# --------------------------
if "responses" not in st.session_state:
    st.session_state.responses = [None] * total_qs
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "show_results" not in st.session_state:
    st.session_state.show_results = False

# --------------------------
# Main flow
# --------------------------
if not st.session_state.show_results:
    current_q = st.session_state.current_q
    trait, question = all_questions[current_q]

    st.markdown(f"**Question {current_q+1} of {total_qs}**")
    st.progress((current_q+1) / total_qs)

    options = [1, 2, 3, 4, 5]
    answer = st.radio(
        question,
        options,
        horizontal=True,
        index=None if st.session_state.responses[current_q] is None else options.index(st.session_state.responses[current_q]),
        key=f"q_{current_q}"
    )
    st.session_state.responses[current_q] = answer if answer else None

    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("Back", disabled=current_q==0):
            st.session_state.current_q -= 1
            st.rerun()
    with col2:
        if st.button("Next", disabled=st.session_state.responses[current_q] is None):
            if current_q + 1 < total_qs:
                st.session_state.current_q += 1
                st.rerun()
            else:
                st.session_state.show_results = True
                st.rerun()
else:
    st.title("Your Results")
    responses = [r for r in st.session_state.responses if r is not None]

    creative_scores = {t: [] for t in creative_traits}
    big5_scores = {t: [] for t in big5_traits}

    for i, (trait, _) in enumerate(all_questions):
        score = st.session_state.responses[i]
        if trait in creative_scores:
            creative_scores[trait].append(score)
        elif trait in big5_scores:
            big5_scores[trait].append(score)

    creative_scores = {t: np.mean(v) for t, v in creative_scores.items()}
    big5_scores = {t: np.mean(v) for t, v in big5_scores.items()}

    st.subheader("Creative Traits")
    st.write(creative_scores)
    st.subheader("Big Five Traits")
    st.write({t.replace("_Big5", ""): s for t, s in big5_scores.items()})

    chart_buf_creative = radar_chart(creative_scores, None, "Creative Traits")
    chart_buf_big5 = radar_chart(big5_scores, None, "Big Five Traits")

    pdf_buf = create_pdf(creative_scores, big5_scores, creative_summaries, big5_summaries, chart_buf_creative, chart_buf_big5)
    st.download_button("Download Your Full Profile (PDF)", pdf_buf, file_name="creative_identity_profile.pdf", mime="application/pdf")

