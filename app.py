import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import io
from fpdf import FPDF
from PIL import Image

st.set_page_config(page_title="Creative Identity Profile", layout="wide")

# -------------------------
# Questionnaire
# -------------------------
questions = {
    "Imagination": [
        "I often daydream or imagine new possibilities.",
        "I enjoy creating stories, art, or music.",
        "I can think of many solutions to a problem."
    ],
    "Curiosity": [
        "I love exploring new ideas or subjects.",
        "I ask questions to deepen my understanding.",
        "I enjoy learning just for the sake of it."
    ],
    "Risk-taking": [
        "I am willing to try new things even if I might fail.",
        "I enjoy stepping outside of my comfort zone.",
        "I see mistakes as opportunities to learn."
    ],
    "Collaboration": [
        "I enjoy working with others on creative projects.",
        "I value feedback and input from others.",
        "I find it easy to build on other people’s ideas."
    ],
    "Persistence": [
        "I keep working on projects even when they are challenging.",
        "I don’t give up easily when faced with obstacles.",
        "I try different approaches if one doesn’t work."
    ]
}

# -------------------------
# Radar chart function
# -------------------------
def radar_chart(scores):
    traits = list(scores.keys())
    values = list(scores.values())

    N = len(traits)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, values, "o-", linewidth=2)
    ax.fill(angles, values, alpha=0.25)
    ax.set_thetagrids(np.degrees(angles[:-1]), traits)
    ax.set_ylim(0, 5)

    buf = io.BytesIO()
    plt.savefig(buf, format="PNG")
    buf.seek(0)
    plt.close(fig)

    image = Image.open(buf)
    return image, buf

# -------------------------
# PDF generation
# -------------------------
def create_pdf(scores, main_trait, chart_buf):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Creative Identity Profile", ln=1, align="C")

    pdf.set_font("Helvetica", "", 12)
    pdf.ln(10)
    pdf.cell(0, 10, f"Your dominant trait: {main_trait}", ln=1)

    pdf.ln(5)
    pdf.cell(0, 10, "Trait Scores:", ln=1)

    for trait, score in scores.items():
        level = (
            "High" if score >= 4 else
            "Moderate" if score >= 2 else
            "Low"
        )
        pdf.cell(0, 10, f"{trait} ({level}): {score:.2f}/5", ln=1)

    # Add radar chart
    chart_buf.seek(0)
    pdf.image(chart_buf, x=10, y=None, w=pdf.w - 20)

    return pdf.output(dest="S").encode("latin-1")

# -------------------------
# Streamlit UI
# -------------------------
st.title("🎨 Creative Identity Profile")
st.write("Answer the questions below to discover your creative strengths!")

scores = {}
submitted = False

with st.form("questionnaire"):
    for trait, qs in questions.items():
        responses = []
        for q in qs:
            responses.append(st.slider(q, 1, 5, 3, key=f"{trait}_{q}"))
        scores[trait] = np.mean(responses)
    submitted = st.form_submit_button("See My Results")

if submitted:
    # Find dominant trait
    main_trait = max(scores, key=scores.get)

    # Show radar chart
    image, chart_buf = radar_chart(scores)
    img_bytes = io.BytesIO()
    image.save(img_bytes, format="PNG")
    img_bytes.seek(0)
    st.image(img_bytes.getvalue(), caption="Your Creative Trait Profile", use_container_width=True)

    # Show results text
    st.subheader("Your Results")
    for trait, score in scores.items():
        level = (
            "High" if score >= 4 else
            "Moderate" if score >= 2 else
            "Low"
        )
        st.write(f"**{trait} ({level}):** {score:.2f}/5")

    # PDF download
    pdf_bytes = create_pdf(scores, main_trait, chart_buf)
    st.download_button(
        "📥 Download Your Personalised PDF Report",
        data=pdf_bytes,
        file_name="Creative_Identity_Report.pdf",
        mime="application/pdf"
    )



