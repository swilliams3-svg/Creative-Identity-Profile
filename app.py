# app.py

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
import io
import random

st.set_page_config(page_title="Creative Identity Profile", layout="centered")

# --- TRAIT DEFINITIONS ---
traits = ["Openness", "Flexibility", "Imagination", "Curiosity", "Risk-taking", "Persistence"]

# --- INTERPRETATIONS ---
interpretations = {
    "Openness": {
        "low": "You may prefer structure and routine, but this can sometimes limit experimentation.",
        "medium": "You balance tradition with novelty, exploring some new ideas while valuing the familiar.",
        "high": "You thrive on novelty, curiosity, and exploring unconventional ideas."
    },
    "Flexibility": {
        "low": "You may prefer sticking with known solutions, but risk missing alternative perspectives.",
        "medium": "You adapt when necessary, though sometimes lean on familiar approaches.",
        "high": "You easily shift perspectives and adapt ideas, reframing challenges creatively."
    },
    "Imagination": {
        "low": "You may find it challenging to think beyond practical or immediate concerns.",
        "medium": "You sometimes generate new ideas but often within realistic boundaries.",
        "high": "You frequently generate vivid, original, and playful ideas."
    },
    "Curiosity": {
        "low": "You may be satisfied with existing knowledge and less likely to question assumptions.",
        "medium": "You show curiosity selectively, diving deeper only into certain areas.",
        "high": "You are naturally inquisitive, asking questions and exploring new topics with enthusiasm."
    },
    "Risk-taking": {
        "low": "You prefer safety and predictability, avoiding uncertain outcomes.",
        "medium": "You sometimes take risks but usually after careful consideration.",
        "high": "You embrace uncertainty and are willing to take bold risks for new possibilities."
    },
    "Persistence": {
        "low": "You may give up quickly when challenges arise, limiting idea development.",
        "medium": "You persevere when motivated, though setbacks can discourage you.",
        "high": "You keep pushing forward despite difficulties, developing ideas fully."
    }
}

# --- GROWTH ACTIVITIES ---
activities = {
    "Openness": "Try exposing yourself to unfamiliar art, music, or literature. Journal your reactions.",
    "Flexibility": "Practice brainstorming multiple solutions for one problem each day.",
    "Imagination": "Engage in creative play — draw, invent stories, or imagine 'what if' scenarios.",
    "Curiosity": "Ask 'why' five times when exploring a new idea to uncover deeper insights.",
    "Risk-taking": "Challenge yourself with a small but meaningful risk each week.",
    "Persistence": "Break down a long-term creative project into smaller, achievable milestones."
}

# --- QUESTIONS ---
questions = {
    "Openness": [
        "I enjoy trying out new experiences.",
        "I like to challenge conventional ways of thinking.",
        "I find inspiration in diverse fields (art, science, etc.).",
        "I actively seek novelty in my life."
    ],
    "Flexibility": [
        "I can change direction easily when circumstances shift.",
        "I am comfortable considering opposing viewpoints.",
        "I often find alternative uses for familiar objects.",
        "I adapt quickly to new challenges."
    ],
    "Imagination": [
        "I often visualize ideas vividly in my mind.",
        "I enjoy creating stories, scenarios, or fantasies.",
        "I use daydreaming as a source of inspiration.",
        "I think of unusual connections between unrelated ideas."
    ],
    "Curiosity": [
        "I ask a lot of questions about how things work.",
        "I enjoy learning about unfamiliar subjects.",
        "I pursue knowledge even if it doesn’t relate to my work.",
        "I wonder about things most people take for granted."
    ],
    "Risk-taking": [
        "I enjoy stepping into the unknown.",
        "I am comfortable with uncertain outcomes.",
        "I would rather try and fail than not try at all.",
        "I take bold steps even without full information."
    ],
    "Persistence": [
        "I keep working on problems even when they are difficult.",
        "I don’t give up easily on long-term projects.",
        "I push through challenges to complete creative work.",
        "I am determined to achieve my creative goals."
    ]
}
# --- FUNCTIONS ---

def calculate_scores(responses):
    """Average scores per trait."""
    scores = {}
    for trait in traits:
        scores[trait] = np.mean(responses[trait])
    return scores

def generate_chart(scores):
    """Radar chart with legend below chart."""
    labels = list(scores.keys())
    values = list(scores.values())

    num_vars = len(labels)

    # repeat first value to close radar circle
    values += values[:1]
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    ax.plot(angles, values, color="blue", linewidth=2)
    ax.fill(angles, values, color="blue", alpha=0.25)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_ylim(0, 5)

    # Legend below chart
    plt.legend(
        labels,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.05),
        ncol=3,
        fontsize=8,
        frameon=False
    )

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)
    return buf

def determine_archetype(scores):
    """Pick main + secondary archetype based on highest scores."""
    sorted_traits = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    main_trait, main_score = sorted_traits[0]
    sub_trait, sub_score = sorted_traits[1]

    archetypes = {
        "Openness": "The Explorer",
        "Flexibility": "The Adapter",
        "Imagination": "The Dreamer",
        "Curiosity": "The Seeker",
        "Risk-taking": "The Adventurer",
        "Persistence": "The Maker"
    }

    return {
        "main": {"trait": main_trait, "score": main_score, "name": archetypes[main_trait]},
        "sub": {"trait": sub_trait, "score": sub_score, "name": archetypes[sub_trait]}
    }
# --- PDF GENERATION ---

def create_pdf(scores, archetype, chart_buf):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Page 1: Chart
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(30, 30, 120)
    pdf.cell(0, 10, "Your Creative Identity Profile", ln=True, align="C")

    pdf.image(chart_buf, x=30, y=40, w=150)
    pdf.ln(140)

    pdf.set_font("Helvetica", "I", 12)
    pdf.cell(0, 10, "Radar chart of your creative traits", ln=True, align="C")

    # Page 2+: Archetypes and Traits
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 10, "Your Creative Archetypes", ln=True)

    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 8,
        f"Main Archetype: {archetype['main']['name']} ({archetype['main']['trait']})\n"
        f"Sub-Archetype: {archetype['sub']['name']} ({archetype['sub']['trait']})\n"
    )
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 10, "Trait Insights & Growth Activities", ln=True)

    for trait, score in scores.items():
        pdf.ln(5)
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(0, 8, f"{trait}: {score:.1f}/5", ln=True)

        # Interpretation
        if score <= 2:
            interpretation = interpretations[trait]["low"]
        elif score == 3:
            interpretation = interpretations[trait]["medium"]
        else:
            interpretation = interpretations[trait]["high"]

        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 6, f"Insight: {interpretation}")

        # Growth activity
        pdf.set_font("Helvetica", "I", 10)
        pdf.set_text_color(80, 80, 80)
        pdf.multi_cell(0, 6, f"Try this: {activities[trait]}")
        pdf.set_text_color(0, 0, 0)

    return pdf


# --- STREAMLIT APP BODY ---

st.title("🌟 Creative Identity Profile")
st.write("Discover your creative strengths through 6 core traits.")

responses = {trait: [] for trait in traits}
total_questions = sum(len(qs) for qs in questions.values())
progress = 0
q_index = 0

# Ask questions
for trait, qs in questions.items():
    st.subheader(trait)
    for q in qs:
        q_index += 1
        responses[trait].append(
            st.radio(
                f"{q} ({q_index}/{total_questions})",
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: {
                    1: "1 - Strongly Disagree",
                    2: "2 - Disagree",
                    3: "3 - Neutral",
                    4: "4 - Agree",
                    5: "5 - Strongly Agree"
                }[x],
                key=f"{trait}_{q_index}"
            )
        )
        st.progress(q_index / total_questions)

if st.button("Generate My Profile"):
    scores = calculate_scores(responses)
    chart_buf = generate_chart(scores)
    archetype = determine_archetype(scores)

    # Show results in app
    st.subheader("🌈 Your Archetypes")
    st.write(f"**Main Archetype:** {archetype['main']['name']} ({archetype['main']['trait']})")
    st.write(f"**Sub-Archetype:** {archetype['sub']['name']} ({archetype['sub']['trait']})")

    st.image(chart_buf, caption="Your Creative Profile", use_container_width=True)

    st.subheader("🔎 Trait Insights")
    for trait, score in scores.items():
        if score <= 2:
            interpretation = interpretations[trait]["low"]
        elif score == 3:
            interpretation = interpretations[trait]["medium"]
        else:
            interpretation = interpretations[trait]["high"]

        st.write(f"**{trait} ({score:.1f}/5):** {interpretation}")
        st.caption(f"💡 Try this: {activities[trait]}")

    # Create downloadable PDF
    pdf = create_pdf(scores, archetype, chart_buf)
    pdf_bytes = pdf.output(dest="S").encode("latin-1", "ignore")

    st.download_button(
        label="📥 Download My Creative Profile (PDF)",
        data=pdf_bytes,
        file_name="creative_identity_profile.pdf",
        mime="application/pdf"
    )

