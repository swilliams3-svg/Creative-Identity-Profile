import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
import io

# -------------------------
# Trait definitions
# -------------------------
TRAITS = {
    "Openness": "Curiosity, imagination, and appreciation for new experiences.",
    "Conscientiousness": "Self-discipline, organization, and reliability.",
    "Extraversion": "Sociability, enthusiasm, and assertiveness.",
    "Agreeableness": "Compassion, cooperation, and trust in others.",
    "Neuroticism": "Tendency toward stress, anxiety, and emotional reactivity."
}

QUESTIONS = {
    "Openness": [
        "I enjoy trying out new activities and experiences.",
        "I often think about abstract or complex ideas."
    ],
    "Conscientiousness": [
        "I am always prepared and organized.",
        "I follow through on commitments I make."
    ],
    "Extraversion": [
        "I feel energized by spending time with others.",
        "I am comfortable being the center of attention."
    ],
    "Agreeableness": [
        "I am considerate and kind to almost everyone.",
        "I enjoy helping others, even if it costs me time or energy."
    ],
    "Neuroticism": [
        "I get stressed out easily.",
        "I often feel anxious about the future."
    ]
}

# -------------------------
# PDF generation
# -------------------------
def create_pdf(scores, main_trait, chart_buf):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, "Creative Identity Profile", ln=True, align="C")
    pdf.ln(10)

    for trait, score in scores.items():
        level = "High" if score > 3.5 else "Medium" if score > 2.5 else "Low"
        pdf.multi_cell(0, 10, f"{trait} ({level}): {score:.2f}/5")

    pdf.ln(10)

    # Insert chart
    chart_buf.seek(0)
    pdf.image(chart_buf, x=10, y=None, w=180)

    # ✅ Guarantee bytes for Streamlit
    pdf_bytes = pdf.output(dest="S").encode("latin-1")
    return io.BytesIO(pdf_bytes).getvalue()

# -------------------------
# Questionnaire app
# -------------------------
st.title("✨ Creative Identity Profile")

if "responses" not in st.session_state:
    st.session_state.responses = {}

with st.form("questionnaire"):
    for trait, questions in QUESTIONS.items():
        st.subheader(trait)
        for q in questions:
            st.session_state.responses[q] = st.radio(
                q,
                options=[1, 2, 3, 4, 5],
                index=None,
                key=q
            )
    submitted = st.form_submit_button("Submit")

if submitted:
    # Compute scores
    scores = {}
    for trait, questions in QUESTIONS.items():
        values = [st.session_state.responses[q] for q in questions if st.session_state.responses[q] is not None]
        if values:
            scores[trait] = np.mean(values)
        else:
            scores[trait] = 0

    # Identify main trait
    main_trait = max(scores, key=scores.get)

    st.success(f"Your strongest trait is **{main_trait}** 🎉")

    # Radar chart
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    labels = list(scores.keys())
    values = list(scores.values())
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    ax.plot(angles, values, "o-", linewidth=2)
    ax.fill(angles, values, alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_ylim(0, 5)

    st.pyplot(fig)

    # Save chart to buffer
    chart_buf = io.BytesIO()
    fig.savefig(chart_buf, format="PNG")
    chart_buf.seek(0)

    # Generate PDF
    pdf_bytes = create_pdf(scores, main_trait, chart_buf)

    # Download button
    st.download_button(
        "📥 Download Your Personalised PDF Report",
        data=pdf_bytes,
        file_name="Creative_Identity_Report.pdf",
        mime="application/pdf"
    )


