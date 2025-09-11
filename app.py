import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF

st.set_page_config(page_title="Creative Identity Profile", layout="centered")

st.title("🎨 Creative Identity Profile")
st.write("Answer the questions to explore your creative archetype and traits.")

# --------------------------------------------------
# Questions per trait
# --------------------------------------------------
questions = {
    "Imagination": [
        "I often see possibilities where others don’t.",
        "I enjoy daydreaming and imagining new worlds.",
        "I like to create stories, images, or concepts.",
        "I can think of unusual uses for common objects."
    ],
    "Curiosity": [
        "I often ask ‘why’ and ‘how’ questions.",
        "I enjoy learning about new topics.",
        "I like exploring unfamiliar ideas.",
        "I read widely to discover new things."
    ],
    "Risk-taking": [
        "I am comfortable trying new and uncertain things.",
        "I often experiment without worrying about failure.",
        "I like pushing boundaries or breaking rules.",
        "I am willing to take bold steps in creative work."
    ],
    "Persistence": [
        "I keep working even when ideas don’t come easily.",
        "I don’t give up easily on creative challenges.",
        "I can stay focused on a project for a long time.",
        "I see setbacks as opportunities to improve."
    ],
    "Social Sensitivity": [
        "I can sense how others feel about ideas.",
        "I collaborate well with others.",
        "I value listening as much as sharing ideas.",
        "I often adapt ideas to suit group needs."
    ]
}

# --------------------------------------------------
# Archetype mapping
# --------------------------------------------------
archetype_extras = {
    "Visionary Dreamer": {
        "Strengths": "Sees possibilities others miss; highly imaginative and forward-looking.",
        "Blind Spots": "May lose focus or struggle to turn visions into reality.",
        "Practices": "Prototype your ideas quickly; use deadlines to stay grounded."
    },
    "Analytical Builder": {
        "Strengths": "Thorough, logical, and persistent problem solver.",
        "Blind Spots": "Risk of over-analysis or slow progress.",
        "Practices": "Balance deep thinking with moments of playful brainstorming."
    },
    "Bold Experimenter": {
        "Strengths": "Thrives in uncertainty; fearless in trying new things.",
        "Blind Spots": "Can act without enough planning; high failure risk.",
        "Practices": "Structure experiments to learn quickly from outcomes."
    },
    "Resilient Maker": {
        "Strengths": "Determined, disciplined, and able to overcome obstacles.",
        "Blind Spots": "May become rigid or burn out under pressure.",
        "Practices": "Pair persistence with reflection and rest."
    },
    "Collaborative Connector": {
        "Strengths": "Empathetic, cooperative, and able to amplify others’ ideas.",
        "Blind Spots": "Risk of prioritizing others’ voices over your own.",
        "Practices": "Balance collaboration with expressing your unique vision."
    },
    "Inquisitive Explorer": {
        "Strengths": "Curious, questioning, and energized by discovery.",
        "Blind Spots": "May scatter attention without producing results.",
        "Practices": "Narrow focus sometimes to turn curiosity into concrete output."
    },
    "Imaginative Storyteller": {
        "Strengths": "Creative with narrative, symbolism, and envisioning worlds.",
        "Blind Spots": "Risk of being overly abstract or impractical.",
        "Practices": "Translate ideas into practical projects or experiences."
    },
    "Fearless Challenger": {
        "Strengths": "Challenges conventions and disrupts the status quo.",
        "Blind Spots": "Can be confrontational or reckless.",
        "Practices": "Use discernment to choose battles worth fighting."
    },
    "Empathic Creator": {
        "Strengths": "Deeply attuned to people’s needs; creates with compassion.",
        "Blind Spots": "May hesitate to push bold ideas for fear of conflict.",
        "Practices": "Pair empathy with assertiveness to maximize impact."
    },
    "Strategic Innovator": {
        "Strengths": "Combines curiosity with risk-taking; acts decisively.",
        "Blind Spots": "May move too quickly without depth or refinement.",
        "Practices": "Pause for reflection before executing new ideas."
    },
    "Grounded Realist": {
        "Strengths": "Balanced across traits; integrates imagination and persistence steadily.",
        "Blind Spots": "May avoid extremes and miss bold breakthroughs.",
        "Practices": "Push outside comfort zones to spark fresh discoveries."
    },
    "Playful Improviser": {
        "Strengths": "Spontaneous, fun, and adaptable in group creativity.",
        "Blind Spots": "Can lack structure; ideas may fade quickly.",
        "Practices": "Capture playful sparks and turn them into lasting outcomes."
    }
}

# --------------------------------------------------
# Functions
# --------------------------------------------------
def assign_profile(traits):
    sorted_traits = sorted(traits.items(), key=lambda x: x[1], reverse=True)
    top_trait, _ = sorted_traits[0]
    second_trait, _ = sorted_traits[1]

    if top_trait == "Imagination" and second_trait == "Curiosity":
        return "Visionary Dreamer"
    elif top_trait == "Curiosity" and second_trait == "Persistence":
        return "Analytical Builder"
    elif top_trait == "Risk-taking" and second_trait == "Imagination":
        return "Bold Experimenter"
    elif top_trait == "Social Sensitivity" and second_trait == "Persistence":
        return "Collaborative Connector"
    elif top_trait == "Curiosity" and second_trait == "Risk-taking":
        return "Strategic Innovator"
    elif top_trait == "Imagination" and second_trait == "Social Sensitivity":
        return "Playful Improviser"

    if top_trait == "Imagination":
        return "Imaginative Storyteller"
    elif top_trait == "Curiosity":
        return "Inquisitive Explorer"
    elif top_trait == "Risk-taking":
        return "Fearless Challenger"
    elif top_trait == "Persistence":
        return "Resilient Maker"
    elif top_trait == "Social Sensitivity":
        return "Empathic Creator"

    return "Grounded Realist"

def create_pdf(profile_name, traits, chart_file):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Creative Identity Report", ln=True, align="C")
    pdf.ln(10)

    # Profile
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"Profile: {profile_name}")
    if profile_name in archetype_extras:
        extra = archetype_extras[profile_name]
        pdf.multi_cell(0, 10, f"Strengths: {extra['Strengths']}")
        pdf.multi_cell(0, 10, f"Blind Spots: {extra['Blind Spots']}")
        pdf.multi_cell(0, 10, f"Growth Practices: {extra['Practices']}")

    pdf.ln(10)

    # Insert radar chart
    pdf.cell(200, 10, "Your Creative Trait Profile:", ln=True)
    pdf.image(chart_file, x=40, w=120)

    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "Trait Scores", ln=True)
    pdf.set_font("Arial", size=12)
    for k, v in traits.items():
        pdf.multi_cell(0, 10, f"{k}: {v}/20")

    return pdf

# --------------------------------------------------
# Streamlit UI
# --------------------------------------------------
scores = {trait: 0 for trait in questions}

with st.form("quiz_form"):
    for trait, qs in questions.items():
        st.subheader(trait)
        for q in qs:
            scores[trait] += st.slider(q, 1, 5, 3, key=q)
    submitted = st.form_submit_button("See My Profile")

if submitted:
    profile = assign_profile(scores)

    st.subheader("Your Creative Identity")
    st.write(f"**{profile}**")

    # Radar chart
    labels = list(scores.keys())
    values = list(scores.values())
    values += values[:1]
    angles = np.linspace(0, 2 * np.pi, len(labels) + 1, endpoint=True)

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, values, "o-", linewidth=2)
    ax.fill(angles, values, alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_yticklabels([])
    chart_file = "radar_chart.png"
    plt.savefig(chart_file, bbox_inches="tight")
    st.pyplot(fig)

    # Export PDF
    if st.button("📄 Export Report as PDF"):
        pdf = create_pdf(profile, scores, chart_file)
        pdf_output = "Creative_Identity_Report.pdf"
        pdf.output(pdf_output)
        with open(pdf_output, "rb") as f:
            st.download_button("⬇️ Download Report", f, file_name=pdf_output)

