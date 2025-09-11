import streamlit as st
import random
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
import io

# -------------------------------
# Utility to clean text (remove unsupported chars)
# -------------------------------
def clean_text(text):
    return text.encode("latin-1", "ignore").decode("latin-1")

# -------------------------------
# Traits, questions, extras
# -------------------------------
traits = {
    "Openness": [
        "I enjoy trying out new experiences.",
        "I actively seek variety in my daily life.",
        "I feel excited by exploring unfamiliar ideas.",
        "I am drawn to new artistic or cultural experiences."
    ],
    "Curiosity": [
        "I often wonder about how things work.",
        "I like asking questions to deepen my understanding.",
        "I explore different perspectives before forming opinions.",
        "I enjoy discovering surprising connections between ideas."
    ],
    "Imagination": [
        "I often picture alternative realities or scenarios.",
        "I like to create stories or mental images in my mind.",
        "I can easily visualize things that don’t exist yet.",
        "I get inspired by daydreams or fantasies."
    ],
    "Risk-Taking": [
        "I feel comfortable taking chances with uncertain outcomes.",
        "I see failure as an opportunity to learn.",
        "I’m willing to experiment even without guarantees.",
        "I don’t let fear of mistakes hold me back."
    ],
    "Persistence": [
        "I keep working on ideas even when progress is slow.",
        "I see creative challenges as puzzles to be solved.",
        "I bounce back after setbacks.",
        "I stay focused until I complete my projects."
    ]
}

trait_extras = {
    "Openness": {
        "Meaning": "How receptive you are to novelty and diversity of thought.",
        "Growth": "Expose yourself to new cultures, arts, and fields outside your comfort zone."
    },
    "Curiosity": {
        "Meaning": "Your drive to ask questions and seek understanding.",
        "Growth": "Practice active questioning — ask 'why' and 'what if' daily."
    },
    "Imagination": {
        "Meaning": "The capacity to generate novel mental images and ideas.",
        "Growth": "Engage in creative exercises like mind-mapping or storytelling."
    },
    "Risk-Taking": {
        "Meaning": "Your willingness to take intellectual and practical risks.",
        "Growth": "Frame risks as experiments — learn from outcomes rather than fearing them."
    },
    "Persistence": {
        "Meaning": "Your grit in pushing ideas into reality.",
        "Growth": "Break projects into milestones to maintain momentum."
    }
}

archetype_extras = {
    "The Visionary": {
        "Strengths": "Sees possibilities others miss, future-oriented, inspiring.",
        "Blind Spots": "May overlook practical details.",
        "Practices": "Balance big ideas with concrete planning."
    },
    "The Explorer": {
        "Strengths": "Curious, adaptable, thrives on discovery.",
        "Blind Spots": "Can be scattered or unfocused.",
        "Practices": "Set small goals to direct your explorations."
    },
    "The Maker": {
        "Strengths": "Hands-on, persistent, brings ideas into form.",
        "Blind Spots": "Can get stuck in perfectionism.",
        "Practices": "Embrace iteration and progress over perfection."
    },
    "The Challenger": {
        "Strengths": "Asks tough questions, disrupts old patterns.",
        "Blind Spots": "May be confrontational or resistant.",
        "Practices": "Channel disruption into constructive change."
    }
}

# -------------------------------
# Radar chart generator
# -------------------------------
def generate_radar_chart(trait_scores):
    labels = list(trait_scores.keys())
    values = list(trait_scores.values())
    values += values[:1]  # loop back to start

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
    ax.plot(angles, values, color="blue", linewidth=2)
    ax.fill(angles, values, color="skyblue", alpha=0.4)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=10)

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)
    return buf

# -------------------------------
# PDF generator (landscape with banner)
# -------------------------------
def create_pdf(profile_name, traits, chart_buf):
    pdf = FPDF(orientation="L", unit="mm", format="A4")
    pdf.add_page()

    # Banner
    pdf.set_fill_color(50, 100, 200)  # blue banner
    pdf.rect(0, 0, 297, 20, "F")
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 12, clean_text("🌟 Creative Identity Report 🌟"), align="C", ln=True)
    pdf.set_text_color(0, 0, 0)

    # Radar chart
    if chart_buf:
        chart_file = "chart.png"
        with open(chart_file, "wb") as f:
            f.write(chart_buf.getbuffer())
        pdf.image(chart_file, x=15, y=40, w=120)

    # Archetype and traits (right side)
    pdf.set_xy(150, 40)
    pdf.set_font("Helvetica", 'B', 14)
    pdf.multi_cell(120, 8, clean_text("Your Creative Archetype"))
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(120, 6, clean_text(f"Profile: {profile_name}"))

    if profile_name in archetype_extras:
        extra = archetype_extras[profile_name]
        pdf.multi_cell(120, 6, clean_text(f"Strengths: {extra['Strengths']}"))
        pdf.multi_cell(120, 6, clean_text(f"Blind Spots: {extra['Blind Spots']}"))
        pdf.multi_cell(120, 6, clean_text(f"Growth Practices: {extra['Practices']}"))

    pdf.ln(2)
    pdf.set_font("Helvetica", 'B', 12)
    pdf.multi_cell(120, 6, clean_text("Trait Scores & Growth Tips"))

    pdf.set_font("Helvetica", size=10)
    for trait, score in traits.items():
        pdf.set_font("Helvetica", 'B', 10)
        pdf.multi_cell(120, 5, clean_text(f"{trait}: {score}/20"))
        if trait in trait_extras:
            pdf.set_font("Helvetica", size=10)
            pdf.multi_cell(120, 5, clean_text(f"Meaning: {trait_extras[trait]['Meaning']}"))
            pdf.multi_cell(120, 5, clean_text(f"Growth: {trait_extras[trait]['Growth']}"))

    # Footer
    pdf.set_xy(15, 190)
    pdf.set_font("Helvetica", 'I', 10)
    pdf.multi_cell(0, 6, clean_text("🌱 Keep Creating! Every idea is a seed — what will you grow today?"), align="C")

    return pdf

# -------------------------------
# Streamlit app
# -------------------------------
st.set_page_config(page_title="Creative Identity Profile", layout="wide")
st.title("🌟 Creative Identity Profile")
st.write("Discover your creative strengths across 5 key traits.")

# Shuffle questions
questions = []
for trait, qs in traits.items():
    for q in qs:
        questions.append((trait, q))
random.shuffle(questions)

responses = {}
progress = 0

# Questionnaire
for i, (trait, q) in enumerate(questions, 1):
    st.markdown(f"**Q{i}. {q}**")
    responses[(trait, q)] = st.radio(
        "Select your response:",
        [1, 2, 3, 4, 5],
        horizontal=True,
        key=f"q{i}"
    )
    progress = int(i / len(questions) * 100)
    st.progress(progress)

if st.button("Generate My Profile"):
    trait_scores = {trait: 0 for trait in traits.keys()}
    for (trait, q), score in responses.items():
        trait_scores[trait] += score

    # Assign archetype
    top_trait = max(trait_scores, key=trait_scores.get)
    if top_trait == "Openness":
        profile = "The Visionary"
    elif top_trait == "Curiosity":
        profile = "The Explorer"
    elif top_trait == "Imagination":
        profile = "The Maker"
    elif top_trait == "Risk-Taking":
        profile = "The Challenger"
    else:
        profile = "The Maker"

    st.subheader("🌟 Your Creative Archetype:")
    st.write(f"**{profile}** — {archetype_extras[profile]['Strengths']}")

    # Chart
    chart_buf = generate_radar_chart(trait_scores)
    st.image(chart_buf, caption="Your Creative Profile", use_column_width=True)

    # PDF
    pdf = create_pdf(profile, trait_scores, chart_buf)
    pdf_bytes = pdf.output(dest="S").encode("latin-1", "ignore")
    st.download_button(
        "📥 Download Your Full Report",
        data=pdf_bytes,
        file_name="creative_identity_report.pdf",
        mime="application/pdf"
    )

