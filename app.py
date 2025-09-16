import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
import random
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

st.set_page_config(page_title="Creative Identity Profile", layout="centered")

# --------------------------
# Creative Traits
# --------------------------
creative_traits = {
    "Openness": [
        "I enjoy exploring new ideas and perspectives.",
        "I am curious about how things work.",
        "I like experimenting with new activities."
    ],
    "Divergent Thinking": [
        "I can think of many different solutions to a problem.",
        "I enjoy brainstorming unusual ideas.",
        "I often find alternative uses for everyday objects."
    ],
    "Risk Taking": [
        "I am comfortable taking risks in order to achieve something new.",
        "I am not afraid of failure when trying something different.",
        "I take on challenges even when the outcome is uncertain."
    ],
    "Persistence": [
        "I keep working on ideas even when they are difficult.",
        "I don’t give up easily when faced with obstacles.",
        "I try different approaches if one doesn’t work."
    ],
    "Curiosity": [
        "I love asking questions to learn more.",
        "I am interested in discovering how things work.",
        "I enjoy exploring unfamiliar topics."
    ],
    "Imagination": [
        "I often create mental images or stories in my head.",
        "I enjoy daydreaming and fantasy.",
        "I can easily picture things that don’t exist yet."
    ]
}

# --------------------------
# Big Five Personality Dimensions
# --------------------------
bigfive_traits = {
    "Openness": [
        "I am full of ideas.",
        "I enjoy artistic and creative experiences.",
        "I value new ways of doing things."
    ],
    "Conscientiousness": [
        "I pay attention to details.",
        "I like to be prepared and organised.",
        "I follow through on commitments."
    ],
    "Extraversion": [
        "I am the life of the party.",
        "I feel comfortable around people.",
        "I start conversations easily."
    ],
    "Agreeableness": [
        "I sympathise with others’ feelings.",
        "I take time out for others.",
        "I feel others’ emotions."
    ],
    "Neuroticism": [
        "I get stressed out easily.",
        "I worry about many things.",
        "I often feel anxious or nervous."
    ]
}

# --------------------------
# Trait Descriptions (Creative)
# --------------------------
trait_descriptions = {
    "Openness": {
        "high": "You are highly open-minded, imaginative, and value novelty.",
        "medium": "You balance traditional and creative approaches.",
        "low": "You prefer routine and familiarity."
    },
    "Divergent Thinking": {
        "high": "You generate many unique ideas and solutions.",
        "medium": "You sometimes think outside the box.",
        "low": "You prefer conventional and straightforward solutions."
    },
    "Risk Taking": {
        "high": "You embrace uncertainty and challenge.",
        "medium": "You take calculated risks when needed.",
        "low": "You prefer security and stability."
    },
    "Persistence": {
        "high": "You push through challenges and setbacks.",
        "medium": "You stay committed but may let go if needed.",
        "low": "You may move on quickly if things get tough."
    },
    "Curiosity": {
        "high": "You are deeply inquisitive and eager to learn.",
        "medium": "You are curious but also practical.",
        "low": "You are content without exploring beyond the familiar."
    },
    "Imagination": {
        "high": "You often visualise possibilities beyond reality.",
        "medium": "You enjoy creative thoughts occasionally.",
        "low": "You focus more on tangible and realistic matters."
    }
}

# --------------------------
# Trait Descriptions (Big Five)
# --------------------------
bigfive_descriptions = {
    "Openness": {
        "high": "You are highly open to new experiences, imaginative, and curious.",
        "medium": "You are moderately open, balancing creativity with practicality.",
        "low": "You prefer routine and familiar experiences over novelty."
    },
    "Conscientiousness": {
        "high": "You are very organized, dependable, and goal-oriented.",
        "medium": "You are reasonably conscientious but sometimes flexible with rules.",
        "low": "You are more spontaneous and less bound by schedules or structure."
    },
    "Extraversion": {
        "high": "You are outgoing, energetic, and thrive in social interactions.",
        "medium": "You enjoy some social activities but also value quiet time.",
        "low": "You are reserved, prefer solitude, and recharge alone."
    },
    "Agreeableness": {
        "high": "You are cooperative, empathetic, and value positive relationships.",
        "medium": "You are generally agreeable but balance your needs with others.",
        "low": "You are more competitive, direct, and value independence over harmony."
    },
    "Neuroticism": {
        "high": "You may often feel stressed, anxious, or emotionally sensitive.",
        "medium": "You experience some emotional ups and downs but generally cope well.",
        "low": "You remain calm, resilient, and emotionally stable under stress."
    }
}

# --------------------------
# Archetypes (simplified)
# --------------------------
archetypes = {
    "The Visionary": "You thrive on imagination and forward-thinking ideas.",
    "The Explorer": "You are driven by curiosity and love of discovery.",
    "The Maker": "You bring ideas to life with persistence and craft.",
    "The Dreamer": "You see possibilities others might overlook."
}

# --------------------------
# Color Palette
# --------------------------
palette = {
    "Openness": "#1f77b4",
    "Divergent Thinking": "#ff7f0e",
    "Risk Taking": "#2ca02c",
    "Persistence": "#d62728",
    "Curiosity": "#9467bd",
    "Imagination": "#8c564b",
    "Conscientiousness": "#e377c2",
    "Extraversion": "#7f7f7f",
    "Agreeableness": "#bcbd22",
    "Neuroticism": "#17becf"
}

# --------------------------
# Helper Functions
# --------------------------
def calculate_scores(responses, traits):
    scores = {t: 0 for t in traits}
    total_items = {t: len(qs) for t, qs in traits.items()}
    for t, qs in traits.items():
        for q in qs:
            scores[t] += responses.get(q, 0)
    for t in scores:
        max_score = total_items[t] * 5
        scores[t] = int((scores[t] / max_score) * 100)
    return scores

# Radar chart with colours
def radar_chart(trait_scores, title):
    labels = list(trait_scores.keys())
    values = list(trait_scores.values())
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(polar=True))

    for i, label in enumerate(labels):
        ax.plot([angles[i], angles[i+1]], [values[i], values[i+1]],
                color=palette[label], linewidth=2)
        ax.fill([angles[i], angles[i+1], angles[i]],
                [values[i], values[i+1], 0],
                color=palette[label], alpha=0.25)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_yticklabels([])
    ax.set_title(title, size=12, weight="bold", y=1.1)

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf

# --------------------------
# App Layout
# --------------------------
st.title("Creative Identity Profile")
st.write("Answer the questions to explore your creative identity and personality profile.")

if "responses" not in st.session_state:
    st.session_state.responses = {}

# --------------------------
# Quiz Page
# --------------------------
elif st.session_state.page == "quiz":
    st.header("Quiz Questions")

    questions = []
    for trait, qs in {**creative_traits, **big_five_traits}.items():
        for q in qs:
            questions.append((trait, q))
    random.shuffle(questions)

    with st.form("quiz_form"):
        for trait, q in questions:
            key = f"{trait}_{q}"
            st.session_state.responses[key] = st.radio(
                q,
                ["1 Strongly Disagree", "2 Disagree", "3 Neutral", "4 Agree", "5 Strongly Agree"],
                horizontal=True,
                key=key
            )
        submitted = st.form_submit_button("Submit Quiz")
        if submitted:
            st.session_state.page = "results"
            st.rerun()


# --------------------------
# Results
# --------------------------
if st.button("Show Results"):
    creative_perc = calculate_scores(st.session_state.responses, creative_traits)
    bigfive_perc = calculate_scores(st.session_state.responses, bigfive_traits)

    # Archetype selection
    archetype = random.choice(list(archetypes.keys()))
    st.subheader("Your Main Archetype")
    st.write(f"**{archetype}:** {archetypes[archetype]}")

    # Growth area (lowest creative trait)
    lowest_trait = min(creative_perc, key=creative_perc.get)
    st.subheader("Growth Trait")
    st.write(f"**{lowest_trait}:** {trait_descriptions[lowest_trait]['low']}")

    # Charts side by side
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Big Five Personality Dimensions")
        st.image(radar_chart(bigfive_perc, "Big Five"))
    with col2:
        st.subheader("Creative Traits")
        st.image(radar_chart(creative_perc, "Creative Traits"))

    # Detailed trait scores
    st.subheader("Detailed Trait Scores")
    for t, p in creative_perc.items():
        if p >= 67:
            st.write(f"**{t}:** {p}% → {trait_descriptions[t]['high']}")
        elif p >= 34:
            st.write(f"**{t}:** {p}% → {trait_descriptions[t]['medium']}")
        else:
            st.write(f"**{t}:** {p}% → {trait_descriptions[t]['low']}")

    for t, p in bigfive_perc.items():
        if p >= 67:
            st.write(f"**{t}:** {p}% → {bigfive_descriptions[t]['high']}")
        elif p >= 34:
            st.write(f"**{t}:** {p}% → {bigfive_descriptions[t]['medium']}")
        else:
            st.write(f"**{t}:** {p}% → {bigfive_descriptions[t]['low']}")

    # --------------------------
    # PDF Export
    # --------------------------
    buf_big5 = radar_chart(bigfive_perc, "Big Five")
    buf_creative = radar_chart(creative_perc, "Creative Traits")

    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, height - 40, "Creative Identity Profile")

    c.setFont("Helvetica", 12)
    c.drawString(40, height - 80, f"Main Archetype: {archetype} - {archetypes[archetype]}")
    c.drawString(40, height - 110, f"Growth Trait: {lowest_trait} - {trait_descriptions[lowest_trait]['low']}")

    # Place charts side by side
    img_big5 = ImageReader(buf_big5)
    img_creative = ImageReader(buf_creative)
    c.drawImage(img_big5, 40, height/2, width/2 - 60, height/3)
    c.drawImage(img_creative, width/2 + 20, height/2, width/2 - 60, height/3)

    # Detailed scores
    y = height/2 - 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "Detailed Trait Scores")
    y -= 30
    c.setFont("Helvetica", 10)
    for t, p in {**creative_perc, **bigfive_perc}.items():
        if t in trait_descriptions:
            if p >= 67:
                desc = trait_descriptions[t]["high"]
            elif p >= 34:
                desc = trait_descriptions[t]["medium"]
            else:
                desc = trait_descriptions[t]["low"]
        elif t in bigfive_descriptions:
            if p >= 67:
                desc = bigfive_descriptions[t]["high"]
            elif p >= 34:
                desc = bigfive_descriptions[t]["medium"]
            else:
                desc = bigfive_descriptions[t]["low"]
        else:
            desc = ""
        c.drawString(40, y, f"{t}: {p}% → {desc}")
        y -= 20

    c.showPage()
    c.save()

    st.download_button(
        "Download PDF",
        data=pdf_buffer.getvalue(),
        file_name="creative_identity_profile.pdf",
        mime="application/pdf"
    )
