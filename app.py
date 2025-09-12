import streamlit as st
import random
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
import io

# --- TRAITS & QUESTIONS ---
traits = {
    "Curiosity": [
        "I enjoy exploring new ideas even if they seem unusual.",
        "I ask a lot of questions about how things work.",
        "I actively seek out new experiences.",
        "I like to investigate problems from multiple angles."
    ],
    "Imagination": [
        "I often think in mental images or stories.",
        "I enjoy coming up with unusual uses for common things.",
        "I can easily picture alternatives in my mind.",
        "I like daydreaming about possibilities."
    ],
    "Risk-Taking": [
        "I’m comfortable with uncertainty when trying new things.",
        "I take risks in my work or hobbies to test ideas.",
        "I see mistakes as part of experimentation.",
        "I like challenging conventional wisdom."
    ],
    "Persistence": [
        "I keep working on ideas even when they get difficult.",
        "I don’t give up easily when problems arise.",
        "I’m motivated to finish projects I start.",
        "I see obstacles as challenges to overcome."
    ],
    "Openness": [
        "I value opinions that differ from my own.",
        "I’m receptive to unusual or novel approaches.",
        "I like collaborating with people who think differently.",
        "I enjoy trying things outside of my comfort zone."
    ]
}

growth_tips = {
    "Curiosity": "Practice asking 'why' and 'what if' questions daily.",
    "Imagination": "Try free writing or sketching to spark new ideas.",
    "Risk-Taking": "Start with small experiments outside your comfort zone.",
    "Persistence": "Break projects into small milestones to stay motivated.",
    "Openness": "Seek feedback from people with different perspectives."
}

# --- RANDOMIZE QUESTIONS ---
all_questions = []
for trait, qs in traits.items():
    for q in qs:
        all_questions.append((trait, q))
random.shuffle(all_questions)

# --- STREAMLIT UI ---
st.title("🌟 Creative Identity Profile")
st.write("Rate each statement on a scale of 1–5: **1 = strongly disagree, 5 = strongly agree**")

# Progress bar
responses = {}
progress = 0
for i, (trait, q) in enumerate(all_questions, 1):
    responses[f"q{i}"] = st.radio(
        f"Q{i}. {q}",
        options=[1, 2, 3, 4, 5],
        horizontal=True,
        key=f"q{i}"
    )
    progress = i / len(all_questions)
    st.progress(progress)

# --- RESULTS ---
if len(responses) == len(all_questions):
    st.subheader("✅ Questionnaire Complete")

    # Calculate trait averages
    scores = {trait: 0 for trait in traits}
    counts = {trait: 0 for trait in traits}
    for (trait, _), key in zip(all_questions, responses.keys()):
        scores[trait] += responses[key]
        counts[trait] += 1
    for trait in scores:
        scores[trait] /= counts[trait]

    # Identify top trait
    main_trait = max(scores, key=scores.get)

    st.write(f"**Your leading creative trait is:** 🌟 {main_trait}")
    st.write(f"💡 Growth Tip: {growth_tips[main_trait]}")

    # --- Radar Chart ---
    fig1, ax1 = plt.subplots(figsize=(5,5), subplot_kw={'polar': True})
    categories = list(scores.keys())
    values = list(scores.values())
    angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]
    ax1.plot(angles, values, "o-", linewidth=2, label="Scores")
    ax1.fill(angles, values, alpha=0.25)
    ax1.set_xticks(angles[:-1])
    ax1.set_xticklabels(categories)
    ax1.set_yticks([1, 2, 3, 4, 5])
    st.pyplot(fig1)

    # --- Bar Chart ---
    fig2, ax2 = plt.subplots(figsize=(6,4))
    ax2.bar(scores.keys(), scores.values(), color="skyblue")
    ax2.set_ylim(0,5)
    ax2.set_ylabel("Average Score")
    st.pyplot(fig2)

    # --- PDF CREATION ---
    def create_pdf(scores, main_trait, chart_bufs):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Page 1: Radar Chart
        pdf.add_page()
        pdf.set_font("Helvetica", 'B', 16)
        pdf.cell(0, 10, "Creative Identity Profile", ln=True, align="C")
        pdf.ln(10)
        pdf.image(chart_bufs[0], x=30, y=40, w=150)

        # Page 2: Bar Chart
        pdf.add_page()
        pdf.set_font("Helvetica", 'B', 14)
        pdf.cell(0, 10, "Trait Scores", ln=True, align="C")
        pdf.ln(10)
        pdf.image(chart_bufs[1], x=30, y=40, w=150)

        # Page 3: Results & Growth
        pdf.add_page()
        pdf.set_font("Helvetica", 'B', 14)
        pdf.cell(0, 10, f"Your Leading Trait: {main_trait}", ln=True)
        pdf.set_font("Helvetica", '', 12)
        pdf.multi_cell(0, 8, f"Growth Tip: {growth_tips[main_trait]}")
        pdf.ln(10)
        for trait, value in scores.items():
            pdf.multi_cell(0, 8, f"{trait}: {value:.2f}/5")
            pdf.multi_cell(0, 8, f"Tip: {growth_tips[trait]}")
            pdf.ln(5)

        return bytes(pdf.output(dest="S"))

    # Save both charts as buffers
    radar_buf = io.BytesIO()
    fig1.savefig(radar_buf, format="PNG")
    radar_buf.seek(0)

    bar_buf = io.BytesIO()
    fig2.savefig(bar_buf, format="PNG")
    bar_buf.seek(0)

    # Create PDF
    pdf_bytes = create_pdf(scores, main_trait, [radar_buf, bar_buf])
    st.download_button("📥 Download Your Creative Identity Report",
                       data=pdf_bytes,
                       file_name="creative_identity.pdf",
                       mime="application/pdf")

