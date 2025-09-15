import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
import random

st.set_page_config(page_title="Creative Identity Profile", layout="centered")

# --------------------------
# Creative Traits (6 traits x 3 questions)
# --------------------------
creative_traits = {
    "Originality": [
        "I often come up with ideas that others consider unusual.",
        "I enjoy finding new ways to do things.",
        "My ideas are often different from those around me."
    ],
    "Curiosity": [
        "I enjoy exploring new topics or activities.",
        "I like asking questions to understand how things work.",
        "I am eager to learn about unfamiliar subjects."
    ],
    "Risk Taking": [
        "I am comfortable with uncertainty in creative work.",
        "I try bold approaches, even if they might fail.",
        "I take chances to push creative boundaries."
    ],
    "Imagination": [
        "I enjoy picturing possibilities that don’t yet exist.",
        "I use my imagination to come up with creative ideas.",
        "I often create mental images of new possibilities."
    ],
    "Discipline": [
        "I can stay focused when working on creative tasks.",
        "I keep going until a creative project is complete.",
        "I work consistently to develop my creative ideas."
    ],
    "Collaboration": [
        "I like sharing ideas with others.",
        "I enjoy building on other people’s ideas.",
        "I find teamwork sparks my creativity."
    ]
}

creative_colors = {
    "Originality": "#1f77b4",
    "Curiosity": "#ff7f0e",
    "Risk Taking": "#2ca02c",
    "Imagination": "#9467bd",
    "Discipline": "#d62728",
    "Collaboration": "#8c564b"
}

creative_summaries = {
    "Originality": {
        "High": "You thrive on producing unusual and fresh ideas.",
        "Medium": "You balance originality with practicality.",
        "Low": "You prefer tried-and-tested ideas over unusual ones."
    },
    "Curiosity": {
        "High": "You are naturally inquisitive and love to explore.",
        "Medium": "You enjoy learning but may not always seek it out.",
        "Low": "You prefer familiar subjects and routines."
    },
    "Risk Taking": {
        "High": "You embrace uncertainty and bold approaches.",
        "Medium": "You take risks selectively when they feel safe.",
        "Low": "You prefer safe and predictable paths."
    },
    "Imagination": {
        "High": "You often envision possibilities beyond the present.",
        "Medium": "You can imagine new ideas but sometimes keep them practical.",
        "Low": "You prefer concrete facts over imagination."
    },
    "Discipline": {
        "High": "You stay committed and see projects through.",
        "Medium": "You balance focus with flexibility.",
        "Low": "You may struggle to sustain effort on long projects."
    },
    "Collaboration": {
        "High": "You thrive in group work and value shared creativity.",
        "Medium": "You enjoy collaboration but also work well alone.",
        "Low": "You prefer to work independently."
    }
}

# --------------------------
# Big Five Traits (5 traits x 3 questions)
# --------------------------
big5_traits = {
    "Openness": [
        "I enjoy trying new experiences.",
        "I have a broad range of interests.",
        "I like exploring unfamiliar ideas."
    ],
    "Conscientiousness": [
        "I pay attention to details.",
        "I like to be organized.",
        "I follow through on commitments."
    ],
    "Extraversion": [
        "I feel energized by social interaction.",
        "I start conversations easily.",
        "I am talkative around others."
    ],
    "Agreeableness": [
        "I take time out for others.",
        "I sympathize with others’ feelings.",
        "I value cooperation in groups."
    ],
    "Neuroticism": [
        "I often feel anxious about things.",
        "I get upset easily.",
        "I worry about many things."
    ]
}

big5_colors = {
    "Openness": "#17becf",
    "Conscientiousness": "#bcbd22",
    "Extraversion": "#7f7f7f",
    "Agreeableness": "#e377c2",
    "Neuroticism": "#8c564b"
}

big5_summaries = {
    "Openness": {
        "High": "You are imaginative and embrace novelty.",
        "Medium": "You like some variety but also familiarity.",
        "Low": "You prefer tradition and routine."
    },
    "Conscientiousness": {
        "High": "You are disciplined and structured.",
        "Medium": "You balance order with flexibility.",
        "Low": "You prefer spontaneity over rigid routines."
    },
    "Extraversion": {
        "High": "You gain energy from social interactions.",
        "Medium": "You enjoy people but also value alone time.",
        "Low": "You prefer quiet and independence."
    },
    "Agreeableness": {
        "High": "You are empathetic and cooperative.",
        "Medium": "You balance kindness with assertiveness.",
        "Low": "You are direct and value self-interest."
    },
    "Neuroticism": {
        "High": "You are sensitive to stress and emotions.",
        "Medium": "You experience stress occasionally but manage it.",
        "Low": "You are calm and emotionally steady."
    }
}

# --------------------------
# Archetypes
# --------------------------
archetypes = {
    "Originality": ("The Innovator", "You generate fresh and unusual ideas."),
    "Curiosity": ("The Explorer", "You thrive on learning and discovery."),
    "Risk Taking": ("The Adventurer", "You embrace bold moves and uncertainty."),
    "Imagination": ("The Visionary", "You envision possibilities others miss."),
    "Discipline": ("The Builder", "You bring ideas to life with persistence."),
    "Collaboration": ("The Connector", "You excel in creative teamwork.")
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

    fig, ax = plt.subplots(figsize=(5,5), subplot_kw=dict(polar=True))
    ax.plot(angles, values, linewidth=1.5, color="black")
    ax.fill(angles, values, alpha=0.1, color="gray")

    for i, (trait, score) in enumerate(scores.items()):
        ax.scatter(angles[i], score, color=colors[trait], s=60, zorder=10)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylim(0,5)
    plt.title(title, size=12, weight="bold")

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)
    return buf

# --------------------------
# Streamlit App
# --------------------------
st.title("Creative Identity & Personality Profile")

if "all_questions" not in st.session_state:
    all_questions = []
    for trait, qs in {**creative_traits, **big5_traits}.items():
        for q in qs:
            all_questions.append((trait, q))
    random.shuffle(all_questions)
    st.session_state.all_questions = all_questions
    st.session_state.responses = {}
    st.session_state.current_q = 0

all_questions = st.session_state.all_questions
responses = st.session_state.responses
current_q = st.session_state.current_q
total_qs = len(all_questions)

if current_q == 0:
    st.markdown("## Welcome to the Creative Identity Quiz 🎨")
    st.markdown(
        "This short quiz explores your **creative traits** and **personality dimensions**. "
        "Answer honestly – there are no right or wrong answers! "
        "At the end, you'll see your creative profile, archetypes, and personalised feedback."
    )

if current_q < total_qs:
    trait, question = all_questions[current_q]
    key = f"{trait}_{current_q}"
    st.markdown(f"**Q{current_q+1}/{total_qs}: {question}**")

    options = [1,2,3,4,5]
    default_index = options.index(responses[key]) if key in responses else None
    answer = st.radio("Select your answer:", options, horizontal=True, index=default_index, key=key)
    responses[key] = answer

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back", disabled=current_q == 0):
            st.session_state.current_q -= 1
            st.rerun()
    with col2:
        answered = key in responses and responses[key] is not None
        if st.button("Next Question ➡️", disabled=not answered):
            st.session_state.current_q += 1
            st.rerun()
else:
    st.success("All questions complete — here are your results!")

    creative_scores = {t:0 for t in creative_traits}
    creative_counts = {t:0 for t in creative_traits}
    big5_scores = {t:0 for t in big5_traits}
    big5_counts = {t:0 for t in big5_traits}

    for key, val in responses.items():
        if val:
            trait = key.split("_")[0]
            if trait in creative_scores:
                creative_scores[trait] += val
                creative_counts[trait] += 1
            if trait in big5_scores:
                big5_scores[trait] += val
                big5_counts[trait] += 1

    for t in creative_scores:
        creative_scores[t] /= creative_counts[t]
    for t in big5_scores:
        big5_scores[t] /= big5_counts[t]

    col1, col2 = st.columns(2)
    with col1:
        st.image(radar_chart(creative_scores, creative_colors, "Creative Traits"), use_container_width=True)
    with col2:
        st.image(radar_chart(big5_scores, big5_colors, "Big Five Traits"), use_container_width=True)

    st.subheader("Your Creative Archetypes")
    sorted_traits = sorted(creative_scores.items(), key=lambda x: x[1], reverse=True)
    main_trait, sub_trait, weakest_trait = sorted_traits[0][0], sorted_traits[1][0], sorted_traits[-1][0]

    for label, trait in [("Main Archetype", main_trait), ("Sub-Archetype", sub_trait), ("Growth Area", weakest_trait)]:
        archetype_name, archetype_desc = archetypes[trait]
        st.markdown(
            f"<div style='background-color:{creative_colors[trait]}20; padding:0.7rem; border-radius:10px; margin:0.7rem 0;'>"
            f"<span style='color:{creative_colors[trait]}; font-weight:bold'>{label}: {archetype_name}</span><br>"
            f"<i>{archetype_desc}</i></div>", unsafe_allow_html=True
        )

    st.subheader("Creative Trait Insights")
    for trait, score in creative_scores.items():
        level = get_level(score)
        summary = creative_summaries[trait][level]
        st.markdown(
            f"<div style='background-color:{creative_colors[trait]}20; padding:0.5rem; border-radius:8px; margin:0.5rem 0;'>"
            f"<span style='color:{creative_colors[trait]}; font-weight:bold'>{trait} ({level})</span> — {score:.2f}/5<br>"
            f"<i>{summary}</i></div>", unsafe_allow_html=True
        )

    st.subheader("Big Five Trait Insights")
    for trait, score in big5_scores.items():
        level = get_level(score)
        summary = big5_summaries[trait][level]
        st.markdown(
            f"<div style='background-color:{big5_colors[trait]}20; padding:0.5rem; border-radius:8px; margin:0.5rem 0;'>"
            f"<span style='color:{big5_colors[trait]}; font-weight:bold'>{trait} ({level})</span> — {score:.2f}/5<br>"
            f"<i>{summary}</i></div>", unsafe_allow_html=True
        )

