import streamlit as st
import matplotlib.pyplot as plt
import io
from fpdf import FPDF

# -----------------------
# Archetype definitions
# -----------------------
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
# Questionnaire
# -----------------------
questions = {
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

# -----------------------
# PDF Generator
# -----------------------
def create_pdf(scores, archetype, chart_buf):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Page 1: Chart
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 10, "Creative Identity Profile", ln=True, align="C")
    pdf.ln(10)

    chart_path = "chart.png"
    with open(chart_path, "wb") as f:
        f.write(chart_buf.getvalue())
    pdf.image(chart_path, x=30, y=40, w=150)

    # Page 2: Archetype
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

    # Page 3: Trait Insights
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

    # ✅ FIXED for fpdf (v1.x)
    return pdf.output(dest="S").encode("latin-1")

# -----------------------
# Streamlit App
# -----------------------
st.set_page_config(page_title="Creative Identity Profile", layout="centered")

st.title("✨ Creative Identity Profile")
st.write("Answer the questions to discover your creative archetype.")

# Questionnaire
responses = {}
for trait, qs in questions.items():
    st.subheader(trait)
    trait_scores = []
    for q in qs:
        score = st.radio(q, [1, 2, 3, 4, 5], horizontal=True, key=f"{trait}_{q}")
        trait_scores.append(score)
    responses[trait] = trait_scores

if st.button("Submit"):
    scores = {trait: sum(vals) / len(vals) for trait, vals in responses.items()}
    main_trait = max(scores, key=scores.get)

    st.subheader("Your Main Archetype")
    st.write(f"**{archetypes[main_trait]['name']}** — {archetypes[main_trait]['description']}")

    # Radar chart
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    labels = list(scores.keys())
    values = list(scores.values())
    angles = [n / float(len(labels)) * 2 * 3.14159 for n in range(len(labels))]
    values += values[:1]
    angles += angles[:1]
    ax.plot(angles, values, linewidth=2, linestyle="solid")
    ax.fill(angles, values, alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_yticklabels([])
    st.pyplot(fig)

    # Save chart buffer
    chart_buf = io.BytesIO()
    fig.savefig(chart_buf, format="png")
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

