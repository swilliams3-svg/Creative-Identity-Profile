import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import io
from fpdf import FPDF

# -------------------------
# TRAITS + QUESTIONS
# -------------------------
traits = {
    "Explorer": [
        "I enjoy stepping into the unknown and trying new experiences.",
        "I actively seek out new challenges to expand my horizons.",
        "Unfamiliar environments excite me rather than intimidate me.",
        "I often take risks in order to grow and learn.",
        "I feel energized when discovering new perspectives or cultures."
    ],
    "Dreamer": [
        "I often imagine possibilities beyond the present reality.",
        "Daydreaming is an important source of inspiration for me.",
        "I can easily generate original ideas from my imagination.",
        "I enjoy creating worlds, stories, or visions in my mind.",
        "My imagination often feels vivid and limitless."
    ],
    "Maker": [
        "I enjoy bringing ideas into tangible form.",
        "I feel satisfied when I create something concrete or practical.",
        "I like experimenting with materials, tools, or methods to make things.",
        "I often build, craft, or design as a way of expressing creativity.",
        "I learn best by doing and prototyping."
    ],
    "Connector": [
        "I enjoy sharing ideas and collaborating with others.",
        "I thrive when I can inspire or influence people.",
        "Working with others helps me generate new ideas.",
        "I value connecting seemingly unrelated people or concepts.",
        "I feel most creative when brainstorming with a group."
    ],
    "Thinker": [
        "I reflect deeply before taking creative action.",
        "I enjoy analyzing problems from multiple angles.",
        "I ground my creativity in structured thought or logic.",
        "I prefer to refine and improve ideas before acting on them.",
        "I often evaluate ideas critically to find the best solution."
    ]
}

# Archetype descriptions
archetypes = {
    "Explorer": {"name": "Explorer", "description": "You thrive on curiosity, adventure, and discovering new perspectives."},
    "Dreamer": {"name": "Dreamer", "description": "Your imagination fuels your creativity, allowing you to dream big and envision new worlds."},
    "Maker": {"name": "Maker", "description": "You bring ideas into reality, turning concepts into tangible results."},
    "Connector": {"name": "Connector", "description": "Collaboration and communication are at the heart of your creativity."},
    "Thinker": {"name": "Thinker", "description": "Your strength lies in analysis, reflection, and structured problem-solving."}
}

# Suggestions for weaker traits
improvement_suggestions = {
    "Explorer": "Try saying yes to something new once a week.",
    "Dreamer": "Set aside 10 minutes daily for free imagination or journaling.",
    "Maker": "Pick a small project and complete it in a single day.",
    "Connector": "Engage in a creative conversation or brainstorm with someone new.",
    "Thinker": "Pause and reflect before making decisions—write down your reasoning."
}

# -------------------------
# RADAR CHART
# -------------------------
def radar_chart(scores):
    labels = list(scores.keys())
    values = list(scores.values())

    values += values[:1]
    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, values, linewidth=2, linestyle="solid")
    ax.fill(angles, values, alpha=0.25)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)
    return buf

# -------------------------
# PDF CREATION
# -------------------------
def create_pdf(scores, archetype, chart_buf):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Page 1 - Chart
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 10, "Creative Identity Profile", ln=True, align="C")
    pdf.ln(10)

    chart_path = "chart.png"
    with open(chart_path, "wb") as f:
        f.write(chart_buf.getvalue())
    pdf.image(chart_path, x=30, y=40, w=150)

    # Page 2 - Archetypes
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Your Creative Archetypes", ln=True)
    pdf.ln(5)
    pdf.set_font("Helvetica", "", 12)

    sorted_traits = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    main_trait = sorted_traits[0][0]
    sub_trait = sorted_traits[1][0]
    weak_trait = sorted_traits[-1][0]

    pdf.multi_cell(0, 10, f"Main Archetype: {archetypes[main_trait]['name']}\n{archetypes[main_trait]['description']}")
    pdf.ln(5)
    pdf.multi_cell(0, 10, f"Sub-Archetype: {archetypes[sub_trait]['name']}\n{archetypes[sub_trait]['description']}")
    pdf.ln(5)
    pdf.multi_cell(0, 10, f"To grow your weaker side ({weak_trait}), try this: {improvement_suggestions[weak_trait]}")

    # Page 3 - Trait Insights
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

# -------------------------
# STREAMLIT APP
# -------------------------
st.title("🌟 Creative Identity Profile")

st.write("Answer the following questions to discover your creative archetype:")

responses = {}
for trait, questions in traits.items():
    st.subheader(trait)
    responses[trait] = []
    for q in questions:
        responses[trait].append(st.radio(q, options=[1, 2, 3, 4, 5], index=2, horizontal=True))

if st.button("See My Results"):
    scores = {trait: np.mean(vals) for trait, vals in responses.items()}
    chart_buf = radar_chart(scores)

    # Determine archetypes
    sorted_traits = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    main_trait = sorted_traits[0][0]
    sub_trait = sorted_traits[1][0]
    weak_trait = sorted_traits[-1][0]

    # Show chart
    st.image(chart_buf, caption="Your Creative Trait Profile", use_container_width=True)

    # Show results
    st.subheader("✨ Your Results")
    st.write(f"**Main Archetype:** {archetypes[main_trait]['name']} - {archetypes[main_trait]['description']}")
    st.write(f"**Sub-Archetype:** {archetypes[sub_trait]['name']} - {archetypes[sub_trait]['description']}")
    st.write(f"**Weaker Area:** {weak_trait} — {improvement_suggestions[weak_trait]}")

    # PDF download
    pdf_bytes = create_pdf(scores, main_trait, chart_buf)
    st.download_button(
        "📥 Download Your Personalised PDF Report",
        data=pdf_bytes,
        file_name="Creative_Identity_Report.pdf",
        mime="application/pdf"
    )

