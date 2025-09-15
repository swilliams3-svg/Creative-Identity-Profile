import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

st.set_page_config(page_title="Creative Identity Profile", layout="centered")

# --------------------------
# Creative Traits
# --------------------------
creative_traits = {
    "Originality": [
        "I often come up with ideas that others don’t think of.",
        "I enjoy finding new ways to solve problems.",
        "I like to put a unique spin on familiar things."
    ],
    "Flexibility": [
        "I can approach a problem from many different angles.",
        "I adapt easily when things don’t go as planned.",
        "I enjoy trying different methods to tackle challenges."
    ],
    "Elaboration": [
        "I like to expand on ideas and add details.",
        "I enjoy developing an idea into something more complex.",
        "I can take a simple thought and build on it."
    ],
    "RiskTaking": [
        "I am willing to take risks with my ideas.",
        "I don’t mind if some of my ideas don’t work out.",
        "I like to push boundaries with my creativity."
    ],
    "Curiosity": [
        "I often wonder how things work.",
        "I ask a lot of questions about the world around me.",
        "I enjoy exploring new topics."
    ],
    "Imagination": [
        "I often daydream or imagine scenarios.",
        "I enjoy visualizing things that don’t exist yet.",
        "I can picture ideas clearly in my mind."
    ]
}

# --------------------------
# Big Five Traits (fixed to include Openness_Big5)
# --------------------------
big5_traits = {
    "Conscientiousness": [
        "I like to keep things organized.",
        "I pay attention to details.",
        "I get chores done right away."
    ],
    "Extraversion": [
        "I feel comfortable around people.",
        "I start conversations.",
        "I don’t mind being the center of attention."
    ],
    "Agreeableness": [
        "I am interested in other people’s problems.",
        "I sympathize with others’ feelings.",
        "I take time out for others."
    ],
    "Neuroticism": [
        "I often feel anxious about things.",
        "I get upset easily.",
        "I worry about many things."
    ],
    "Openness_Big5": [   # renamed so no clash with creative traits
        "I enjoy trying new activities and experiences.",
        "I have a broad range of interests.",
        "I am curious about many different things."
    ]
}

# --------------------------
# Colors for Traits
# --------------------------
creative_colors = {
    "Originality": "#e6194b",
    "Flexibility": "#3cb44b",
    "Elaboration": "#ffe119",
    "RiskTaking": "#4363d8",
    "Curiosity": "#f58231",
    "Imagination": "#911eb4"
}

big5_colors = {
    "Conscientiousness": "#ff7f0e",
    "Extraversion": "#2ca02c",
    "Agreeableness": "#9467bd",
    "Neuroticism": "#d62728",
    "Openness_Big5": "#1f77b4"
}

# --------------------------
# Summaries
# --------------------------
creative_summaries = {
    "Originality": {
        "High": "You bring fresh perspectives and new solutions.",
        "Medium": "You balance unique ideas with practicality.",
        "Low": "You prefer established ways of thinking."
    },
    "Flexibility": {
        "High": "You easily shift perspectives and adapt.",
        "Medium": "You adapt when necessary but value consistency.",
        "Low": "You prefer to stick to one method or perspective."
    },
    "Elaboration": {
        "High": "You add rich detail and depth to ideas.",
        "Medium": "You build ideas when needed but keep things simple.",
        "Low": "You prefer to keep ideas straightforward and concise."
    },
    "RiskTaking": {
        "High": "You embrace uncertainty and bold ideas.",
        "Medium": "You take risks occasionally when worthwhile.",
        "Low": "You prefer safe, proven approaches."
    },
    "Curiosity": {
        "High": "You constantly explore and ask questions.",
        "Medium": "You are curious when interested in a topic.",
        "Low": "You prefer to focus on familiar areas."
    },
    "Imagination": {
        "High": "You vividly envision new possibilities.",
        "Medium": "You use imagination in some situations.",
        "Low": "You are more focused on the here and now."
    }
}

big5_summaries = {
    "Conscientiousness": {
        "High": "You are organized and dependable.",
        "Medium": "You are reasonably reliable but flexible.",
        "Low": "You prefer spontaneity over structure."
    },
    "Extraversion": {
        "High": "You are outgoing and energized by others.",
        "Medium": "You enjoy socializing but also need alone time.",
        "Low": "You are reserved and enjoy solitude."
    },
    "Agreeableness": {
        "High": "You are compassionate and cooperative.",
        "Medium": "You balance kindness with assertiveness.",
        "Low": "You are more focused on your own needs."
    },
    "Neuroticism": {
        "High": "You experience emotions intensely and often worry.",
        "Medium": "You sometimes feel stressed but cope well.",
        "Low": "You are calm and resilient under pressure."
    },
    "Openness_Big5": {   # renamed
        "High": "You are imaginative and embrace new experiences.",
        "Medium": "You enjoy some novelty but also value familiarity.",
        "Low": "You prefer tradition and familiar ways of thinking."
    }
}

# --------------------------
# Archetypes
# --------------------------
archetypes = {
    "Originality": {
        "name": "The Innovator",
        "description": "You thrive on fresh ideas and novel solutions.",
        "improvement": "Remember to refine and test your ideas."
    },
    "Flexibility": {
        "name": "The Adapter",
        "description": "You shift easily between different perspectives.",
        "improvement": "Focus your adaptability toward long-term goals."
    },
    "Elaboration": {
        "name": "The Developer",
        "description": "You expand and enrich initial ideas into full projects.",
        "improvement": "Balance detail with efficiency."
    },
    "RiskTaking": {
        "name": "The Challenger",
        "description": "You take bold steps and embrace uncertainty.",
        "improvement": "Evaluate risks carefully to avoid setbacks."
    },
    "Curiosity": {
        "name": "The Explorer",
        "description": "You ask questions and seek new knowledge.",
        "improvement": "Channel curiosity into focused exploration."
    },
    "Imagination": {
        "name": "The Visionary",
        "description": "You vividly imagine possibilities beyond the present.",
        "improvement": "Ground your visions with practical steps."
    }
}

# --------------------------
# Helper Functions
# --------------------------
def get_level(score):
    if score >= 4:
        return "High"
    elif score >= 2.5:
        return "Medium"
    else:
        return "Low"

def radar_chart(scores, colors, title):
    labels = list(scores.keys())
    values = list(scores.values())
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]
    fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(polar=True))
    ax.plot(angles, values, "o-", linewidth=2)
    ax.fill(angles, values, alpha=0.25)
    for i, (angle, label) in enumerate(zip(angles[:-1], labels)):
        ax.text(
            angle, values[i] + 0.2, label.replace("_Big5", ""),  # show clean label
            color=colors[label], ha="center", va="center",
            fontsize=8, weight="bold"
        )
    ax.set_yticklabels([])
    ax.set_xticks([])
    ax.set_title(title, size=12, weight="bold")
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf

# --------------------------
# Quiz Flow
# --------------------------
if "page" not in st.session_state:
    st.session_state.page = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}

all_traits = {**creative_traits, **big5_traits}
questions = []
for trait, qs in all_traits.items():
    for q in qs:
        questions.append((trait, q))

total_questions = len(questions)  # now 33

# --------------------------
# Quiz Page
# --------------------------
if st.session_state.page < total_questions:
    st.title("Creative Identity Profile Quiz")
    st.markdown("""
    Welcome! This quiz will help you explore your **Creative Traits** and **Big Five Personality Traits**.  
    Please answer all questions honestly. There are **33 questions** in total.
    """)

    trait, question = questions[st.session_state.page]
    st.markdown(f"**Question {st.session_state.page+1} of {total_questions}**")
    st.markdown(f"*Trait: {trait.replace('_Big5','')}*")

    # custom answer buttons (keep original style)
    cols = st.columns(5)
    choice = None
    labels = ["1", "2", "3", "4", "5"]
    for i, col in enumerate(cols):
        if col.button(labels[i], key=f"{st.session_state.page}_{i}"):
            choice = i + 1
            st.session_state.answers[st.session_state.page] = (trait, choice)
            st.session_state.page += 1
            st.experimental_rerun()

# --------------------------
# Results Page
# --------------------------
else:
    st.title("Your Creative Identity Profile")

    # compute averages
    creative_scores = {t: 0 for t in creative_traits}
    big5_scores = {t: 0 for t in big5_traits}
    creative_counts = {t: 0 for t in creative_traits}
    big5_counts = {t: 0 for t in big5_traits}

    for _, (trait, score) in st.session_state.answers.items():
        if trait in creative_scores:
            creative_scores[trait] += score
            creative_counts[trait] += 1
        elif trait in big5_scores:
            big5_scores[trait] += score
            big5_counts[trait] += 1

    creative_scores = {t: creative_scores[t]/creative_counts[t] for t in creative_traits}
    big5_scores = {t: big5_scores[t]/big5_counts[t] for t in big5_traits}

    # charts
    st.subheader("Visual Profiles")
    ccol1, ccol2 = st.columns(2)
    with ccol1:
        st.image(radar_chart(creative_scores, creative_colors, "Creative Traits"))
    with ccol2:
        st.image(radar_chart(big5_scores, big5_colors, "Big Five Traits"))

    # trait insights
    st.subheader("Creative Trait Insights")
    for trait, score in creative_scores.items():
        level = get_level(score)
        st.markdown(
            f"<div style='background-color:{creative_colors[trait]}20; padding:0.5rem; border-radius:8px; margin:0.5rem 0;'>"
            f"<span style='color:{creative_colors[trait]}; font-weight:bold'>{trait} ({level})</span> — {score:.2f}/5<br>"
            f"<i>{creative_summaries[trait][level]}</i></div>", unsafe_allow_html=True
        )

    st.subheader("Big Five Trait Insights")
    for trait, score in big5_scores.items():
        label = trait.replace("_Big5", "")
        level = get_level(score)
        st.markdown(
            f"<div style='background-color:{big5_colors[trait]}20; padding:0.5rem; border-radius:8px; margin:0.5rem 0;'>"
            f"<span style='color:{big5_colors[trait]}; font-weight:bold'>{label} ({level})</span> — {score:.2f}/5<br>"
            f"<i>{big5_summaries[trait][level]}</i></div>", unsafe_allow_html=True
        )

    # archetypes
    st.subheader("Your Archetype")
    top_trait = max(creative_scores, key=creative_scores.get)
    archetype = archetypes[top_trait]
    st.markdown(
        f"<div style='background-color:{creative_colors[top_trait]}20; padding:1rem; border-radius:10px; margin:1rem 0;'>"
        f"<h3 style='color:{creative_colors[top_trait]}'>{archetype['name']} ({top_trait})</h3>"
        f"<p>{archetype['description']}</p>"
        f"<b>Growth tip:</b> {archetype['improvement']}</div>",
        unsafe_allow_html=True
    )

    # PDF download
    if st.button("Download PDF Report"):
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=A4)
        width, height = A4

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, "Creative Identity Profile Report")

        c.setFont("Helvetica", 12)
        c.drawString(50, height - 80, "Creative Traits:")
        y = height - 100
        for trait, score in creative_scores.items():
            c.drawString(60, y, f"{trait}: {score:.1f}")
            y -= 20

        y -= 20
        c.drawString(50, y, "Big Five Traits:")
        y -= 20
        for trait, score in big5_scores.items():
            label = trait.replace("_Big5","")
            c.drawString(60, y, f"{label}: {score:.1f}")
            y -= 20

        # charts
        y -= 200
        c.drawString(50, y+180, "Creative Traits Radar")
        img1 = ImageReader(radar_chart(creative_scores, creative_colors, "Creative Traits"))
        c.drawImage(img1, 50, y, width=200, height=200)

        img2 = ImageReader(radar_chart(big5_scores, big5_colors, "Big Five Traits"))
        c.drawImage(img2, 300, y, width=200, height=200)

        c.showPage()
        c.save()
        buf.seek(0)

        st.download_button(
            "⬇️ Download PDF",
            data=buf,
            file_name="creative_identity_profile.pdf",
            mime="application/pdf"
        )
