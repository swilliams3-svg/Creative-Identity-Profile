import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io

# --------------------------
# Creative Traits & Colors
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
# Big Five Traits
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
    "Openness": [   # Big Five Openness
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
    "Openness": "#1f77b4"
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
    "Openness": {
        "High": "You are imaginative and embrace new experiences.",
        "Medium": "You enjoy some novelty but also value familiarity.",
        "Low": "You prefer tradition and familiar ways of thinking."
    }
}

# --------------------------
# Radar Chart (fixed with colors per trait segment)
# --------------------------
def radar_chart(scores: dict, colors: dict, title="") -> io.BytesIO:
    labels = list(scores.keys())
    num_vars = len(labels)

    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))

    values = list(scores.values())
    values += values[:1]

    # Draw polygon outline
    ax.plot(angles, values, linewidth=2, color="black")
    ax.fill(angles, values, alpha=0.05, color="gray")

    # Color each segment + marker
    for i, (trait, score) in enumerate(scores.items()):
        ax.plot([angles[i], angles[i+1]], [score, values[i+1]],
                color=colors[trait], linewidth=3)
        ax.scatter(angles[i], score, color=colors[trait], s=60, zorder=10, label=trait)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=9)
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
# Streamlit App
# --------------------------
st.title("Creative Identity & Personality Profile")

st.header("Creative Traits")
creative_scores = {}
for trait, questions in creative_traits.items():
    st.subheader(trait)
    total = 0
    for q in questions:
        total += st.slider(q, 1, 5, 3, key=f"{trait}_{q}")
    creative_scores[trait] = total / len(questions)

st.header("Big Five Personality Traits")
big5_scores = {}
for trait, questions in big5_traits.items():
    st.subheader(trait)
    total = 0
    for q in questions:
        total += st.slider(q, 1, 5, 3, key=f"{trait}_{q}")
    big5_scores[trait] = total / len(questions)

if st.button("Generate Profile"):
    st.subheader("Radar Charts")
    st.image(radar_chart(creative_scores, creative_colors, "Creative Traits"))
    st.image(radar_chart(big5_scores, big5_colors, "Big Five Traits"))

    st.subheader("Trait Insights (Creative)")
    for trait, score in creative_scores.items():
        level = "High" if score >= 4 else "Medium" if score >= 2.5 else "Low"
        summary = creative_summaries[trait][level]
        st.markdown(
            f"<div style='background-color:{creative_colors[trait]}20; padding:0.5rem; border-radius:8px; margin:0.5rem 0;'>"
            f"<span style='color:{creative_colors[trait]}; font-weight:bold'>{trait} ({level})</span> — {score:.2f}/5<br>"
            f"<i>{summary}</i></div>", unsafe_allow_html=True
        )

    st.subheader("Trait Insights (Big Five)")
    for trait, score in big5_scores.items():
        level = "High" if score >= 4 else "Medium" if score >= 2.5 else "Low"
        summary = big5_summaries[trait][level]
        st.markdown(
            f"<div style='background-color:{big5_colors[trait]}20; padding:0.5rem; border-radius:8px; margin:0.5rem 0;'>"
            f"<span style='color:{big5_colors[trait]}; font-weight:bold'>{trait} ({level})</span> — {score:.2f}/5<br>"
            f"<i>{summary}</i></div>", unsafe_allow_html=True
        )
