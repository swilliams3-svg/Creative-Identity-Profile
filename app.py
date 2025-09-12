import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import io
from fpdf import FPDF
import random

st.set_page_config(page_title="Creative Identity Profile", layout="centered")

# -----------------------
# Trait definitions
# -----------------------
traits = {
    "Explorer": [
        "I enjoy stepping into the unknown.",
        "I love trying new things, even if they feel risky."
    ],
    "Dreamer": [
        "My imagination often takes me to new worlds.",
        "I enjoy thinking about possibilities beyond the ordinary."
    ],
    "Maker": [
        "I like building or crafting things with my hands or tools.",
        "I enjoy turning ideas into tangible creations."
    ],
    "Connector": [
        "I feel energized when working with others.",
        "I often bring people together to make things happen."
    ],
    "Thinker": [
        "I enjoy analyzing ideas deeply.",
        "I like solving puzzles or intellectual challenges."
    ]
}

# Archetypes
archetypes = {
    "Explorer": {
        "name": "Explorer",
        "description": "You are driven by curiosity and novelty, always seeking new experiences and perspectives."
    },
    "Dreamer": {
        "name": "Dreamer",
        "description": "You have a strong imagination and are inspired by possibilities beyond the ordinary."
    },
    "Maker": {
        "name": "Maker",
        "description": "You love creating tangible things and bringing abstract ideas into reality."
    },
    "Connector": {
        "name": "Connector",
        "description": "You thrive on collaboration and building bridges between people and ideas."
    },
    "Thinker": {
        "name": "Thinker",
        "description": "You enjoy analysis, reflection, and solving problems in creative ways."
    }
}

# -----------------------
# Radar chart
# -----------------------
def radar_chart(scores):
    labels = list(scores.keys())
    values = list(scores.values())
    num_vars = len(labels)

    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, values, linewidth=2, linestyle="solid")
    ax.fill(angles, values, alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 5)

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)  # ✅ make sure buffer is rewinded
    plt.close(fig)
    return buf

# -----------------------
# PDF generator
# -----------------------
def create_pdf(scores, archetype, chart_buf):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    chart_path = "chart.png"
    with open(chart_path, "wb") as f:
        f.write(chart_buf.getbuffer())

    # Page 1
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 10, "Creative Identity Profile", ln=True, align="C")
    pdf.ln(10)
    pdf.image(chart_path, x=30, y=40, w=150)

    # Page 2
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Your Creative Archetype", ln=True)
    pdf.ln(5)
    pdf.set_font("Helvetica", "", 12)
    pdf.multi_cell(0, 10,
                   f"Main Archetype: {archetypes[archetype]['name']}\n\n"
                   f"{archetypes[archetype]['description']}")
    sorted_traits = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    if len(sorted_traits) > 1:
        sub_trait = sorted_traits[1][0]
        pdf.ln(5)
        pdf.multi_cell(0, 10,
                       f"Sub-Archetype: {archetypes[sub_trait]['name']}\n\n"
                       f"{archetypes[sub_trait]['description']}")

    # Page 3
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Trait Insights", ln=True)
    pdf.ln(5)
    pdf.set_font("Helvetica", "", 12)
    for trait, score in scores.items():
        if score >= 4:
            level = "High"
        elif score >= 2.5:
            level = "Medium"
        else:
            level = "Low"
        pdf.multi_cell(0, 10, f"{trait} ({level}): {score:.2f}/5")

    return pdf.output(dest="S").encode("latin-1")

# -----------------------
# Streamlit App
# -----------------------
st.title("🌟 Creative Identity Profile")
st.write("Discover your creative traits, archetype, and ways to grow your creative potential.")

st.info("Answer each statement on a 1–5 scale: 1 = Strongly Disagree … 5 = Strongly Agree.")

# Shuffle questions once
if "all_questions" not in st.session_state:
    all_questions = []
    for trait, qs in traits.items():
        for q in qs:
            all_questions.append((trait, q))
    random.shuffle(all_questions)
    st.session_state.all_questions = all_questions

all_questions = st.session_state.all_questions

if "responses" not in st.session_state:
    st.session_state.responses = {f"{trait}_{i}": None for i, (trait, _) in enumerate(all_questions, 1)}

responses = st.session_state.responses
total_qs = len(all_questions)

answered = 0
for i, (trait, question) in enumerate(all_questions, 1):
    key = f"{trait}_{i}"
    responses[key] = st.radio(
        f"Q{i}/{total_qs}: {question}",
        [1, 2, 3, 4, 5],
        horizontal=True,
        index=(responses[key] - 1) if responses[key] else None,
        key=key
    )
    if responses[key] is not None:
        answered += 1

progress = answered / total_qs
st.progress(progress)

# Results
if answered == total_qs:
    st.success("✅ Questionnaire complete! See your results below:")

    scores = {trait: 0 for trait in traits}
    counts = {trait: 0 for trait in traits}
    for key, val in responses.items():
        if val:
            trait = key.split("_")[0]
            scores[trait] += val
            counts[trait] += 1
    for trait in scores:
        scores[trait] /= counts[trait]

    # Chart
    chart_buf = radar_chart(scores)
    st.image(chart_buf, caption="Your Creative Trait Profile", use_container_width=True)

    # Archetypes
    sorted_traits = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    main_trait = sorted_traits[0][0]
    sub_trait = sorted_traits[1][0]

    st.subheader("🎭 Your Creative Archetype")
    st.write(f"**Main Archetype: {archetypes[main_trait]['name']}**")
    st.write(archetypes[main_trait]['description'])
    st.write(f"**Sub-Archetype: {archetypes[sub_trait]['name']}**")
    st.write(archetypes[sub_trait]['description'])

    # Insights
    st.subheader("📊 Trait Insights")
    for trait, score in scores.items():
        if score >= 4:
            level = "High"
        elif score >= 2.5:
            level = "Medium"
        else:
            level = "Low"
        st.write(f"**{trait} ({level})** – {score:.2f}/5")

    # PDF
    pdf_bytes = create_pdf(scores, main_trait, chart_buf)
    st.download_button("📥 Download Your Personalised PDF Report",
                       data=pdf_bytes, file_name="Creative_Identity_Report.pdf",
                       mime="application/pdf")
