import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
import io

# ------------------------------
# Define traits and questions
# ------------------------------
TRAITS = {
    "Openness": [
        "I enjoy trying out new artistic experiences.",
        "I often think about abstract concepts.",
        "I am curious about many different things.",
    ],
    "Conscientiousness": [
        "I like to have a clear plan before starting tasks.",
        "I am thorough in my work.",
        "I follow through with commitments I make.",
    ],
    "Extraversion": [
        "I enjoy being the center of attention.",
        "I feel energized when around other people.",
        "I like to take the lead in group situations.",
    ],
    "Agreeableness": [
        "I am considerate of others’ feelings.",
        "I like to cooperate rather than compete.",
        "I am sympathetic towards others.",
    ],
    "Neuroticism": [
        "I often feel anxious or worried.",
        "I can become stressed easily.",
        "I sometimes struggle to control my emotions.",
    ],
}

# ------------------------------
# Helper functions
# ------------------------------
def calculate_scores(responses):
    scores = {}
    for trait, qs in TRAITS.items():
        answers = [responses[q] for q in qs if q in responses]
        scores[trait] = np.mean(answers) if answers else 0
    return scores

def trait_level(score):
    if score >= 4:
        return "High"
    elif score >= 2.5:
        return "Moderate"
    else:
        return "Low"

def create_radar_chart(scores):
    labels = list(scores.keys())
    values = list(scores.values())
    values += values[:1]
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, values, "o-", linewidth=2)
    ax.fill(angles, values, alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_ylim(0, 5)

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)
    return buf

def create_pdf(scores, main_trait, chart_buf):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Creative Identity Profile", ln=True, align="C")

    pdf.set_font("Arial", "", 12)
    pdf.ln(10)
    pdf.multi_cell(0, 10, f"Your strongest trait: {main_trait}")

    pdf.ln(5)
    for trait, score in scores.items():
        level = trait_level(score)
        pdf.multi_cell(0, 10, f"{trait} ({level}): {score:.2f}/5")

    # Insert radar chart
    pdf.ln(10)
    chart_path = "radar_chart.png"
    with open(chart_path, "wb") as f:
        f.write(chart_buf.getbuffer())
    pdf.image(chart_path, x=30, w=150)

    return pdf.output(dest="S").encode("latin-1")

# ------------------------------
# Streamlit UI
# ------------------------------
st.title("🎨 Creative Identity Profile")

responses = {}
with st.form("questionnaire"):
    for trait, questions in TRAITS.items():
        st.subheader(trait)
        for q in questions:
            responses[q] = st.slider(q, 1, 5, 3)
    submitted = st.form_submit_button("Submit")

if submitted:
    scores = calculate_scores(responses)
    main_trait = max(scores, key=scores.get)
    chart_buf = create_radar_chart(scores)

    st.success(f"Your strongest trait is **{main_trait}**")

    st.image(chart_buf, caption="Your Creative Identity Radar Chart")

    pdf_bytes = create_pdf(scores, main_trait, chart_buf)

    st.download_button(
        "📥 Download Your Personalised PDF Report",
        data=pdf_bytes,
        file_name="Creative_Identity_Report.pdf",
        mime="application/pdf",
    )

