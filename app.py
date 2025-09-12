import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
import io

# -------------------
# Questionnaire setup
# -------------------
st.title("🧩 Creative Identity Profile")

st.write("Please answer all questions to discover your creative identity.")

questions = {
    "Openness": [
        "I enjoy trying new and different things.",
        "I am curious about how things work.",
        "I like to think about abstract ideas.",
    ],
    "Conscientiousness": [
        "I like to plan things carefully before doing them.",
        "I pay attention to details.",
        "I follow through with my commitments.",
    ],
    "Extraversion": [
        "I feel energized when I spend time with others.",
        "I am talkative and outgoing.",
        "I like being the center of attention.",
    ],
    "Agreeableness": [
        "I try to be considerate and kind to others.",
        "I am cooperative rather than competitive.",
        "I sympathize with others’ feelings.",
    ],
    "Neuroticism": [
        "I often feel anxious or worried.",
        "I get stressed out easily.",
        "I feel vulnerable in difficult situations.",
    ],
}

options = ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]

# Store responses
responses = {}

for trait, qs in questions.items():
    st.subheader(trait)
    for i, q in enumerate(qs):
        key = f"{trait}_{i}"
        responses[key] = st.radio(q, options, index=None, key=key, horizontal=True)

# -------------------
# Results processing
# -------------------
if st.button("See My Results"):
    if None in [responses[q] for q in responses]:
        st.warning("⚠️ Please answer all questions before viewing results.")
    else:
        scores = {}
        for trait, qs in questions.items():
            vals = []
            for i in range(len(qs)):
                key = f"{trait}_{i}"
                vals.append(options.index(responses[key]) + 1)
            scores[trait] = np.mean(vals)

        # Find main trait
        main_trait = max(scores, key=scores.get)

        st.success(f"Your strongest trait is **{main_trait}**!")

        # Radar chart
        fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))

        labels = list(scores.keys())
        values = list(scores.values())
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        values += values[:1]
        angles += angles[:1]

        ax.plot(angles, values, "o-", linewidth=2)
        ax.fill(angles, values, alpha=0.25)
        ax.set_thetagrids(np.degrees(angles[:-1]), labels)
        ax.set_ylim(0, 5)

        st.pyplot(fig)

        # -------------------
        # PDF generation
        # -------------------
        def create_pdf(scores, main_trait, chart_buf):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "Creative Identity Profile", ln=True, align="C")

            pdf.set_font("Arial", "", 12)
            pdf.ln(10)
            pdf.cell(0, 10, f"Your strongest trait: {main_trait}", ln=True)

            pdf.ln(5)
            for trait, score in scores.items():
                if score >= 4:
                    level = "High"
                elif score >= 3:
                    level = "Moderate"
                else:
                    level = "Low"
                pdf.multi_cell(0, 10, f"{trait} ({level}): {score:.2f}/5")

            pdf.ln(10)
            pdf.cell(0, 10, "Radar Chart:", ln=True)

            # Insert chart
            pdf.image(chart_buf, x=30, w=150)

            return pdf.output(dest="S").encode("latin-1")

        # Save chart to buffer
        chart_buf = "radar_chart.png"
        fig.savefig(chart_buf)

        pdf_bytes = create_pdf(scores, main_trait, chart_buf)

        st.download_button(
            "📥 Download Your Personalised PDF Report",
            data=pdf_bytes,
            file_name="Creative_Identity_Report.pdf",
            mime="application/pdf",
        )



