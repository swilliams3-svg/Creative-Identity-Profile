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
        "I like to imagine possibilities beyond what I know.",
        "I am curious about many different things."
    ],
    "Risk-taking": [
        "I am willing to take risks in my creative work.",
        "I don’t mind uncertainty when trying new approaches.",
        "I experiment with ideas even if they might fail."
    ],
    "Resilience": [
        "I keep trying even after setbacks in creative tasks.",
        "I can adapt when my ideas don’t work as planned.",
        "I learn from mistakes and keep moving forward."
    ],
    "Collaboration": [
        "I enjoy sharing ideas with others.",
        "Working with others helps me improve creatively.",
        "I value feedback in developing my ideas."
    ],
    "Divergent Thinking": [
        "I can come up with many different ideas for a problem.",
        "I enjoy brainstorming unusual or original solutions.",
        "I think of multiple ways to use common objects."
    ],
    "Convergent Thinking": [
        "I can narrow down options to find the best idea.",
        "I enjoy refining and improving ideas.",
        "I evaluate which solutions are most effective."
    ]
}

creative_colors = {
    "Openness": "#1f77b4",
    "Risk-taking": "#ff7f0e",
    "Resilience": "#2ca02c",
    "Collaboration": "#9467bd",
    "Divergent Thinking": "#d62728",
    "Convergent Thinking": "#8c564b"
}

creative_summaries = {
    "Openness": {
        "High": "You thrive on imagination and curiosity.",
        "Medium": "You balance curiosity with focus and practicality.",
        "Low": "You prefer familiar ideas and structured approaches."
    },
    "Risk-taking": {
        "High": "You embrace uncertainty and new experiences.",
        "Medium": "You take chances when the stakes feel right.",
        "Low": "You prefer safer choices and calculated steps."
    },
    "Resilience": {
        "High": "You bounce back quickly and learn from setbacks.",
        "Medium": "You recover from challenges with some effort.",
        "Low": "You may find setbacks discouraging but can grow with support."
    },
    "Collaboration": {
        "High": "You thrive in teamwork and draw on diverse ideas.",
        "Medium": "You enjoy working with others but also value independence.",
        "Low": "You prefer to work solo and rely on your own vision."
    },
    "Divergent Thinking": {
        "High": "You generate many original and unusual ideas.",
        "Medium": "You can think of multiple solutions, though sometimes within bounds.",
        "Low": "You prefer straightforward solutions and focus on clarity."
    },
    "Convergent Thinking": {
        "High": "You excel at refining ideas and making decisions.",
        "Medium": "You balance idea generation with structured evaluation.",
        "Low": "You may struggle with narrowing options and making choices."
    }
}

# --------------------------
# Archetypes
# --------------------------
archetypes = {
    "Openness": {
        "name": "The Explorer",
        "description": "You thrive on curiosity and imagination. Explorers see possibilities everywhere, though sometimes risk being unfocused.",
        "improvement": "Try short 'exploration sprints' followed by reflection to capture the best ideas."
    },
    "Risk-taking": {
        "name": "The Adventurer",
        "description": "You embrace uncertainty and push boundaries, though sometimes risk overexposure.",
        "improvement": "Test risky ideas with small experiments before big commitments."
    },
    "Resilience": {
        "name": "The Perseverer",
        "description": "You persist through challenges and learn from failure.",
        "improvement": "After setbacks, reflect on lessons and note small wins to keep momentum."
    },
    "Collaboration": {
        "name": "The Connector",
        "description": "You spark ideas in groups and value diverse perspectives.",
        "improvement": "Balance collaboration with solo time to develop your own voice."
    },
    "Divergent Thinking": {
        "name": "The Visionary",
        "description": "You generate many original ideas and unusual connections.",
        "improvement": "Use ranking criteria to pick the most promising ideas to develop further."
    },
    "Convergent Thinking": {
        "name": "The Strategist",
        "description": "You refine and structure ideas into action.",
        "improvement": "Occasionally loosen constraints to allow more unusual ideas."
    }
}

# --------------------------
# Big Five Traits (fixed Openness key)
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
    "Openness_Big5": [   # renamed
        "I enjoy trying new activities and experiences.",
        "I have a broad range of interests.",
        "I am curious about many different things."
    ]
}

big5_colors = {
    "Conscientiousness": "#ff7f0e",
    "Extraversion": "#2ca02c",
    "Agreeableness": "#9467bd",
    "Neuroticism": "#d62728",
    "Openness_Big5": "#1f77b4"
}

big5_summaries = {
    "Conscientiousness": {
        "High": "You are disciplined, structured, and value order.",
        "Medium": "You balance organization with flexibility.",
        "Low": "You prefer spontaneity and may avoid strict routines."
    },
    "Extraversion": {
        "High": "You gain energy from social interaction.",
        "Medium": "You enjoy company but also value alone time.",
        "Low": "You prefer quiet environments and independence."
    },
    "Agreeableness": {
        "High": "You are empathetic and value harmony with others.",
        "Medium": "You can be cooperative but also assertive when needed.",
        "Low": "You are direct and prioritize your own views."
    },
    "Neuroticism": {
        "High": "You are sensitive to stress and emotions.",
        "Medium": "You experience occasional stress but manage it.",
        "Low": "You are calm, stable, and less affected by stress."
    },
    "Openness_Big5": {   # renamed
        "High": "You are imaginative and embrace new experiences.",
        "Medium": "You enjoy some novelty but also value familiarity.",
        "Low": "You prefer tradition and familiar ways of thinking."
    }
}

# --------------------------
# Helpers
# --------------------------
def get_level(score: float) -> str:
    if score >= 4:
        return "High"
    elif score >= 2.5:
        return "Medium"
    else:
        return "Low"

def radar_chart(scores: dict, colors: dict, title="") -> io.BytesIO:
    labels = list(scores.keys())
    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]
    values = list(scores.values())
    values += values[:1]

    fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))
    ax.plot(angles, values, linewidth=1.5, color="black")
    ax.fill(angles, values, alpha=0.05, color="gray")

    for i, (trait, score) in enumerate(scores.items()):
        ax.plot([angles[i], angles[i+1]], [score, values[i+1]],
                color=colors[trait], linewidth=3)
        ax.scatter(angles[i], score, color=colors[trait], s=60, zorder=10, label=trait)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([t.replace("_Big5", "") for t in labels], fontsize=9)
    ax.set_ylim(0,5)
    ax.set_yticks([1,2,3,4,5])
    ax.set_yticklabels(["1","2","3","4","5"])
    plt.title(title, size=12, weight="bold")
    ax.legend(bbox_to_anchor=(1.15, 1.1))

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)
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

total_questions = len(questions)  # should be 33 now

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
    choice = st.radio(
        question,
        options=[1, 2, 3, 4, 5],
        format_func=lambda x: f"{x} - {'Strongly Disagree' if x==1 else 'Strongly Agree' if x==5 else ''}",
        index=None,  # no default
        key=f"q{st.session_state.page}"
    )

    if st.button("Next"):
        if choice is None:
            st.warning("⚠️ Please select an option before continuing.")
        else:
            st.session_state.answers[st.session_state.page] = (trait, choice)
            st.session_state.page += 1

# --------------------------
# Results Page
# --------------------------
else:
    st.title("Your Creative Identity Profile")

    # compute average per trait
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

    # radar charts
    st.subheader("Visual Profiles")
    ccol1, ccol2 = st.columns(2)
    with ccol1:
        st.image(radar_chart(creative_scores, creative_colors, "Creative Traits"))
    with ccol2:
        st.image(radar_chart(big5_scores, big5_colors, "Big Five Traits"))

    # summaries
    st.subheader("Trait Insights")
    for trait, score in creative_scores.items():
        level = get_level(score)
        st.markdown(f"**{trait}** ({score:.1f}) — {creative_summaries[trait][level]}")

    for trait, score in big5_scores.items():
        label = trait.replace("_Big5","")
        level = get_level(score)
        st.markdown(f"**{label}** ({score:.1f}) — {big5_summaries[trait][level]}")

    # archetypes
    st.subheader("Your Archetypes")
    top_trait = max(creative_scores, key=creative_scores.get)
    archetype = archetypes[top_trait]
    st.markdown(f"### {archetype['name']} ({top_trait})")
    st.markdown(archetype["description"])
    st.markdown(f"**Growth tip:** {archetype['improvement']}")

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
