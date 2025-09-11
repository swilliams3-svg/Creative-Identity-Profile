import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
import io
import random
import tempfile

st.set_page_config(page_title="Creative Identity Profile", layout="centered")

# ---------- SAFE TEXT (no PDF encoding errors) ----------
def safe_text(text):
    return text.encode("latin-1", "ignore").decode("latin-1")

# ---------- TRAITS & QUESTIONS ----------
traits = {
    "Openness": [
        "I enjoy exploring new ideas and experiences.",
        "I am curious about how things work.",
        "I like to imagine possibilities beyond the obvious.",
        "I am comfortable with change and novelty."
    ],
    "Conscientiousness": [
        "I set goals and work towards them consistently.",
        "I like to stay organized in my work.",
        "I can discipline myself to complete creative projects.",
        "I am persistent even when things are difficult."
    ],
    "Extraversion": [
        "I feel energized by working with others.",
        "I enjoy sharing ideas with groups.",
        "I gain inspiration through social interactions.",
        "I like to express myself openly."
    ],
    "Agreeableness": [
        "I value collaboration in creative work.",
        "I consider others’ perspectives when creating.",
        "I am supportive of teammates’ ideas.",
        "I like projects that help or inspire others."
    ],
    "Emotional Range": [
        "I use my emotions as a source of inspiration.",
        "I am sensitive to moods and atmospheres.",
        "My feelings influence how I create.",
        "I find meaning in emotional experiences."
    ],
    "Divergent Thinking": [
        "I can think of many solutions to a problem.",
        "I enjoy combining ideas in unusual ways.",
        "I often imagine alternatives others miss.",
        "I see connections between unrelated things."
    ]
}

trait_colours = {
    "Openness": "skyblue",
    "Conscientiousness": "orange",
    "Extraversion": "green",
    "Agreeableness": "purple",
    "Emotional Range": "red",
    "Divergent Thinking": "brown"
}

# ---------- ARCHETYPES ----------
archetypes = {
    "Openness": {
        "name": "The Explorer",
        "trait": "Openness",
        "description": "You thrive on curiosity and imagination. Explorers embrace novelty, experiment often, and see possibilities others overlook. The risk is scattering focus across too many directions."
    },
    "Conscientiousness": {
        "name": "The Architect",
        "trait": "Conscientiousness",
        "description": "You bring structure and discipline to creativity. Architects excel at executing ideas and turning visions into reality. The risk is becoming rigid or perfectionistic."
    },
    "Extraversion": {
        "name": "The Performer",
        "trait": "Extraversion",
        "description": "You gain energy from sharing creativity with others. Performers inspire, motivate, and lead through expression. The risk is relying too much on external validation."
    },
    "Agreeableness": {
        "name": "The Collaborator",
        "trait": "Agreeableness",
        "description": "You value harmony and collective growth. Collaborators thrive in teamwork, drawing on empathy and cooperation. The risk is holding back your own voice to keep peace."
    },
    "Emotional Range": {
        "name": "The Dreamer",
        "trait": "Emotional Range",
        "description": "You draw deeply from your emotional world. Dreamers turn feelings into art and meaning. The risk is being overwhelmed by moods or over-identifying with emotions."
    },
    "Divergent Thinking": {
        "name": "The Inventor",
        "trait": "Divergent Thinking",
        "description": "You excel at unconventional connections and innovative solutions. Inventors push boundaries of what’s possible. The risk is struggling to refine or implement ideas."
    }
}

# ---------- INTERPRETATIONS ----------
interpretations = {
    "Openness": {
        "low": "You prefer familiarity and may miss novel ideas.",
        "medium": "You balance tradition with exploration.",
        "high": "You thrive on imagination and novelty."
    },
    "Conscientiousness": {
        "low": "You may struggle with consistency.",
        "medium": "You show steady effort but value flexibility.",
        "high": "You are highly disciplined and goal-driven."
    },
    "Extraversion": {
        "low": "You recharge best alone.",
        "medium": "You balance solo and group work.",
        "high": "You thrive in social creative contexts."
    },
    "Agreeableness": {
        "low": "You may prefer independence over collaboration.",
        "medium": "You collaborate but value autonomy.",
        "high": "You strongly value cooperation and harmony."
    },
    "Emotional Range": {
        "low": "You may prefer stability over emotional depth.",
        "medium": "You balance feelings with rationality.",
        "high": "You draw heavily on emotions for creativity."
    },
    "Divergent Thinking": {
        "low": "You prefer practical, conventional solutions.",
        "medium": "You occasionally explore alternatives.",
        "high": "You see endless possibilities and unique ideas."
    }
}

# ---------- ACTIVITIES ----------
activities = {
    "Openness": "Try journaling or exploring new art forms.",
    "Conscientiousness": "Set a creative goal and track progress daily.",
    "Extraversion": "Share ideas in a workshop or group chat.",
    "Agreeableness": "Collaborate on a creative project with a friend.",
    "Emotional Range": "Transform emotions into poetry or music.",
    "Divergent Thinking": "Brainstorm 20 uses for a common object."
}

# ---------- RADAR CHART ----------
def create_radar_chart(scores):
    labels = list(scores.keys())
    values = list(scores.values())
    num_vars = len(labels)

    angles = np.linspace(0, 2*np.pi, num_vars, endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    for i, trait in enumerate(labels):
        color = trait_colours[trait]
        val_segment = [values[i], values[i+1]]
        ang_segment = [angles[i], angles[i+1]]
        ax.plot(ang_segment, val_segment, color=color, linewidth=2)
        ax.fill(ang_segment, val_segment, color=color, alpha=0.25, label=trait)

    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(["1","2","3","4","5"])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=3)
    ax.set_ylim(0, 5)

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)
    return buf

# ---------- PDF ----------
def create_pdf(scores, archetype, chart_buf):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Page 1
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(30, 30, 120)
    pdf.cell(0, 10, safe_text("Your Creative Identity Profile"), ln=True, align="C")

    # Save chart to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
        tmpfile.write(chart_buf.getbuffer())
        tmp_path = tmpfile.name
    pdf.image(tmp_path, x=30, y=40, w=150)

    pdf.ln(160)
    pdf.set_font("Helvetica", "I", 12)
    pdf.cell(0, 10, safe_text("Radar chart of your creative traits"), ln=True, align="C")

    # Page 2
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 10, safe_text("Your Creative Archetypes"), ln=True)

    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 8, safe_text(
        f"Main Archetype: {archetype['main']['name']} ({archetype['main']['trait']})\n"
        f"{archetype['main']['description']}\n\n"
        f"Sub-Archetype: {archetype['sub']['name']} ({archetype['sub']['trait']})\n"
        f"{archetype['sub']['description']}"
    ))
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 10, safe_text("Trait Insights & Growth Activities"), ln=True)

    for trait, score in scores.items():
        pdf.ln(5)
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(0, 8, safe_text(f"{trait}: {score:.1f}/5"), ln=True)

        if score <= 2:
            interpretation = interpretations[trait]["low"]
        elif score == 3:
            interpretation = interpretations[trait]["medium"]
        else:
            interpretation = interpretations[trait]["high"]

        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 6, safe_text(f"Insight: {interpretation}"))

        pdf.set_font("Helvetica", "I", 10)
        pdf.set_text_color(80, 80, 80)
        pdf.multi_cell(0, 6, safe_text(f"Try this: {activities[trait]}"))
        pdf.set_text_color(0, 0, 0)

    return pdf

# ---------- STREAMLIT APP ----------
st.title("🌟 Creative Identity Profile")
st.write("Discover your creative traits, archetype, and ways to grow your creative potential.")

st.markdown("### How to answer")
st.info("Please respond to each statement on a **1–5 scale**:\n\n"
        "1 = Strongly Disagree, 2 = Disagree, 3 = Neutral, 4 = Agree, 5 = Strongly Agree.")

# Randomize questions
all_questions = []
for trait, qs in traits.items():
    for q in qs:
        all_questions.append((trait, q))
random.shuffle(all_questions)

responses = {}
total_qs = len(all_questions)

st.markdown("### Questionnaire")
progress = 0

for i, (trait, question) in enumerate(all_questions, 1):
    responses[f"{trait}_{i}"] = st.radio(
        f"Q{i}/{total_qs}: {question}",
        [1, 2, 3, 4, 5],
        horizontal=True,
        index=None,
        key=f"{trait}_{i}"
    )
    answered = sum(1 for r in responses.values() if r is not None)
    progress = answered / total_qs
    st.progress(progress)

if st.button("Submit"):
    if None in responses.values():
        st.error("Please answer all questions.")
    else:
        # Compute scores
        trait_scores = {t: 0 for t in traits.keys()}
        counts = {t: 0 for t in traits.keys()}
        for key, value in responses.items():
            trait = key.split("_")[0]
            trait_scores[trait] += value
            counts[trait] += 1
        scores = {t: trait_scores[t] / counts[t] for t in traits.keys()}

        # Archetypes
        main_trait = max(scores, key=scores.get)
        sub_trait = sorted(scores, key=scores.get, reverse=True)[1]
        archetype = {"main": archetypes[main_trait], "sub": archetypes[sub_trait]}

        # Chart
        chart_buf = create_radar_chart(scores)
        st.image(chart_buf, caption="Your Creative Profile", use_container_width=True)

        # Results
        st.subheader("✨ Your Archetypes")
        st.write(f"**Main Archetype: {archetype['main']['name']}** ({archetype['main']['trait']})")
        st.write(archetype['main']['description'])
        st.write(f"**Sub-Archetype: {archetype['sub']['name']}** ({archetype['sub']['trait']})")
        st.write(archetype['sub']['description'])

        st.subheader("📊 Trait Insights & Growth Activities")
        for trait, score in scores.items():
            if score <= 2:
                interpretation = interpretations[trait]["low"]
            elif score == 3:
                interpretation = interpretations[trait]["medium"]
            else:
                interpretation = interpretations[trait]["high"]
            st.markdown(f"**{trait}: {score:.1f}/5**")
            st.write(f"_Insight_: {interpretation}")
            st.write(f"_Try this_: {activities[trait]}")

        # PDF download
        pdf = create_pdf(scores, archetype, chart_buf)
        pdf_bytes = pdf.output(dest="S").encode("latin-1", "ignore")
        st.download_button("📥 Download Your Report (PDF)", data=pdf_bytes,
                           file_name="creative_identity_profile.pdf", mime="application/pdf")

