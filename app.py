import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
from io import BytesIO

st.set_page_config(page_title="Creative Identity Profile", layout="wide")

# -------------------------------
# Define archetypes and questions
# -------------------------------
ARCHETYPES = {
    "Explorer": [
        "I enjoy experimenting with new creative approaches.",
        "I seek out new experiences and perspectives.",
        "I like to challenge conventional ways of doing things."
    ],
    "Visionary": [
        "I can easily imagine future possibilities.",
        "I often think about big-picture ideas.",
        "I enjoy turning abstract thoughts into plans."
    ],
    "Maker": [
        "I like to create tangible outputs from my ideas.",
        "I take satisfaction in building and crafting.",
        "I prefer practical application over abstract thinking."
    ],
    "Connector": [
        "I enjoy collaborating with others on projects.",
        "I thrive when sharing ideas in groups.",
        "I find inspiration in conversations with others."
    ]
}

# -------------------------------
# Store responses
# -------------------------------
if "responses" not in st.session_state:
    st.session_state.responses = {f"{arch}_{i}": None for arch in ARCHETYPES for i in range(len(ARCHETYPES[arch]))}

responses = st.session_state.responses
all_questions = [(arch, q) for arch, qs in ARCHETYPES.items() for q in qs]
total_qs = len(all_questions)

# -------------------------------
# Questionnaire
# -------------------------------
st.title("🎨 Creative Identity Profile")

st.write("Please answer each question on a scale from 1 (Strongly Disagree) to 5 (Strongly Agree).")

answered = 0
for i, (arch, question) in enumerate(all_questions, 1):
    key = f"{arch}_{i}"
    prev_val = responses[key]

    st.markdown(f"**Q{i}/{total_qs}: {question}**")
    st.caption("Choose: 1 = Strongly Disagree · 2 = Disagree · 3 = Neutral · 4 = Agree · 5 = Strongly Agree")

    responses[key] = st.radio(
        "",
        [1, 2, 3, 4, 5],
        horizontal=True,
        index=(prev_val - 1) if prev_val is not None else None,
        key=key
    )

    if responses[key] is not None:
        answered += 1

progress = answered / total_qs
st.progress(progress)

# -------------------------------
# Process results
# -------------------------------
def calculate_scores(responses):
    scores = {}
    for arch, qs in ARCHETYPES.items():
        vals = [responses[f"{arch}_{i+1}"] for i in range(len(qs)) if responses[f"{arch}_{i+1}"] is not None]
        if vals:
            scores[arch] = np.mean(vals)
    return scores

def classify_score(score):
    if score >= 4.0:
        return "High"
    elif score >= 3.0:
        return "Moderate"
    else:
        return "Low"

# -------------------------------
# PDF generation
# -------------------------------
def create_pdf(scores, main_arch, chart_buf):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Creative Identity Profile Report", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "", 12)
    for arch, score in scores.items():
        level = classify_score(score)
        pdf.multi_cell(0, 10, f"{arch} ({level}): {score:.2f}/5")

    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"Your Dominant Archetype: {main_arch}", ln=True)

    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, "Radar Chart:")
    pdf.ln(5)

    chart_buf.seek(0)
    pdf.image(chart_buf, x=30, w=150)

    return pdf.output(dest="S").encode("latin-1")

# -------------------------------
# Show results when complete
# -------------------------------
if answered == total_qs:
    scores = calculate_scores(responses)
    main_arch = max(scores, key=scores.get)

    st.subheader("✅ Your Results")
    for arch, score in scores.items():
        st.write(f"**{arch}**: {score:.2f}/5 ({classify_score(score)})")

    # Radar chart
    labels = list(scores.keys())
    values = list(scores.values())
    values += values[:1]

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, values, "o-", linewidth=2)
    ax.fill(angles, values, alpha=0.25)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    ax.set_ylim(0, 5)

    chart_buf = BytesIO()
    plt.savefig(chart_buf, format="PNG")
    st.pyplot(fig)

    # PDF download
    pdf_bytes = create_pdf(scores, main_arch, chart_buf)
    st.download_button(
        "📥 Download Your Personalised PDF Report",
        data=pdf_bytes,
        file_name="Creative_Identity_Report.pdf",
        mime="application/pdf"
    )
else:
    st.info("Please complete all questions before viewing your results.")

