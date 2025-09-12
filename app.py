import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
from PIL import Image
import io

st.set_page_config(page_title="Creative Identity Profile", layout="centered")

# --------------------------
# Questionnaire
# --------------------------
st.title("🎨 Creative Identity Profile")
st.write("Answer the following questions to discover your creative profile.")

questions = {
    "Openness": [
        "I enjoy exploring new ideas and perspectives.",
        "I actively seek out new experiences.",
        "I adapt easily to unfamiliar situations."
    ],
    "Risk-taking": [
        "I feel comfortable making decisions in uncertain situations.",
        "I am willing to take risks to achieve my goals.",
        "I see failure as part of the learning process."
    ],
    "Resilience": [
        "I recover quickly after setbacks.",
        "I keep going even when things get tough.",
        "I see obstacles as opportunities to grow."
    ],
    "Collaboration": [
        "I enjoy working with others on creative projects.",
        "I value diverse perspectives in group work.",
        "I actively contribute to team brainstorming sessions."
    ],
    "Divergent Thinking": [
        "I can generate multiple solutions to a problem.",
        "I often come up with unusual or original ideas.",
        "I enjoy thinking outside the box."
    ],
    "Convergent Thinking": [
        "I can evaluate different ideas to find the best solution.",
        "I enjoy analyzing ideas for practicality and effectiveness.",
        "I like narrowing down options to make clear decisions."
    ]
}

responses = {}
with st.form("creative_form"):
    for trait, qs in questions.items():
        st.subheader(trait)
        for q in qs:
            responses[q] = st.slider(q, 1, 5, 3, key=q)
    submitted = st.form_submit_button("See My Creative Profile")

# --------------------------
# Radar Chart Function
# --------------------------
def radar_chart(scores):
    labels = list(scores.keys())
    values = list(scores.values())
    num_vars = len(labels)

    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    ax.plot(angles, values, color="black", linewidth=1)
    ax.fill(angles, values, color="grey", alpha=0.1)

    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_ylim(0, 5)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    plt.tight_layout(rect=[0, 0.05, 1, 1])

    buf = io.BytesIO()
    plt.savefig(buf, format="PNG")
    buf.seek(0)
    plt.close(fig)

    # Two outputs: numpy array for Streamlit, buffer for PDF
    img_array = np.array(Image.open(buf))
    buf.seek(0)
    return img_array, buf

# --------------------------
# PDF Creation
# --------------------------
def create_pdf(scores, main_trait, chart_buf):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Creative Identity Profile", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Helvetica", "", 12)
    pdf.multi_cell(0, 10, f"Your dominant creative trait is: {main_trait}")
    pdf.ln(5)

    for trait, score in scores.items():
        pdf.multi_cell(0, 10, f"{trait}: {score:.2f}/5")

    pdf.ln(10)
    pdf.image(chart_buf, x=40, w=130)

    return pdf.output(dest="S").encode("latin-1")

# --------------------------
# Results
# --------------------------
if submitted:
    # Calculate trait averages
    trait_scores = {trait: np.mean([responses[q] for q in qs]) for trait, qs in questions.items()}
    main_trait = max(trait_scores, key=trait_scores.get)

    st.subheader("Your Results")
    st.write(f"🌟 Your dominant creative trait is **{main_trait}**")

    # Chart
    img_array, chart_buf = radar_chart(trait_scores)
    st.image(img_array, caption="Your Creative Trait Profile", use_container_width=True)

    # PDF
    pdf_bytes = create_pdf(trait_scores, main_trait, chart_buf)
    st.download_button(
        "📥 Download Your Personalised PDF Report",
        data=pdf_bytes,
        file_name="Creative_Identity_Report.pdf",
        mime="application/pdf"
    )


