import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
import random

st.set_page_config(page_title="Creative Identity Profile", layout="centered")

# --------------------------
# Creative Traits
# --------------------------
creative_traits = {
    "Originality": [
        "I often come up with ideas that others find unusual.",
        "I enjoy inventing new ways of doing things.",
        "I like to surprise people with unexpected solutions."
    ],
    "Curiosity": [
        "I enjoy exploring new ideas and perspectives.",
        "I like to imagine possibilities beyond what I know.",
        "I am curious about many different things."
    ],
    "Risk Taking": [
        "I am willing to take risks in my creative work.",
        "I don’t mind uncertainty when trying new approaches.",
        "I experiment with ideas even if they might fail."
    ],
    "Imagination": [
        "I like to picture things in my mind vividly.",
        "I often daydream new possibilities.",
        "I enjoy creating stories or scenarios in my head."
    ],
    "Discipline": [
        "I keep working on creative tasks until they are finished.",
        "I can focus for long periods on creative work.",
        "I set goals and follow through with my ideas."
    ],
    "Collaboration": [
        "I enjoy sharing ideas with others.",
        "Working with others helps me improve creatively.",
        "I value feedback in developing my ideas."
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
        "High": "You generate unusual and inventive ideas with ease.",
        "Medium": "You sometimes create original ideas but balance them with practicality.",
        "Low": "You prefer familiar solutions and clear approaches."
    },
    "Curiosity": {
        "High": "You thrive on imagination and curiosity.",
        "Medium": "You balance curiosity with focus and practicality.",
        "Low": "You prefer familiar ideas and structured approaches."
    },
    "Risk Taking": {
        "High": "You embrace uncertainty and new experiences.",
        "Medium": "You take chances when the stakes feel right.",
        "Low": "You prefer safer choices and calculated steps."
    },
    "Imagination": {
        "High": "You vividly picture possibilities and dream big.",
        "Medium": "You use imagination but also rely on logic.",
        "Low": "You focus on realistic and practical ideas."
    },
    "Discipline": {
        "High": "You stay focused and complete creative tasks.",
        "Medium": "You balance persistence with flexibility.",
        "Low": "You may struggle to follow through consistently."
    },
    "Collaboration": {
        "High": "You thrive in teamwork and draw on diverse ideas.",
        "Medium": "You enjoy working with others but also value independence.",
        "Low": "You prefer to work solo and rely on your own vision."
    }
}

# --------------------------
# Archetypes
# --------------------------
archetypes = {
    "Originality": {
        "name": "The Innovator",
        "description": "You excel at producing fresh, unusual ideas.",
        "improvement": "Balance novelty with practical steps for impact."
    },
    "Curiosity": {
        "name": "The Explorer",
        "description": "You thrive on curiosity and imagination.",
        "improvement": "Channel curiosity into focused projects."
    },
    "Risk Taking": {
        "name": "The Adventurer",
        "description": "You embrace uncertainty and push boundaries.",
        "improvement": "Test risky ideas in small steps first."
    },
    "Imagination": {
        "name": "The Dreamer",
        "description": "You see vivid possibilities and envision futures.",
        "improvement": "Pair imagination with structured planning."
    },
    "Discipline": {
        "name": "The Builder",
        "description": "You persevere and bring ideas to completion.",
        "improvement": "Allow space for flexibility and spontaneity."
    },
    "Collaboration": {
        "name": "The Connector",
        "description": "You spark ideas in groups and value diverse perspectives.",
        "improvement": "Balance collaboration with solo reflection."
    }
}

# --------------------------
# Big Five Traits
# --------------------------
big5_traits = {
    "Openness": [
        "I enjoy trying new activities and experiences.",
        "I have a broad range of interests.",
        "I am curious about many different things."
    ],
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
    ]
}

big5_colors = {
    "Openness": "#17becf",
    "Conscientiousness": "#bcbd22",
    "Extraversion": "#e377c2",
    "Agreeableness": "#7f7f7f",
    "Neuroticism": "#8c564b"
}

big5_summaries = {
    "Openness": {
        "High": "You are imaginative and embrace new experiences.",
        "Medium": "You enjoy some novelty but also value familiarity.",
        "Low": "You prefer tradition and familiar ways of thinking."
    },
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

    fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))
    values = list(scores.values())
    values += values[:1]

    ax.plot(angles, values, linewidth=1.5, color="black")
    ax.fill(angles, values, alpha=0.05, color="gray")

    for i, (trait, score) in enumerate(scores.items()):
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
st.write("Answer each statement on a 1–5 scale: 1 = Strongly Disagree … 5 = Strongly Agree.")

# Shuffle questions
if "all_questions" not in st.session_state:
    all_questions = []
    for trait, qs in {**creative_traits, **big5_traits}.items():
        for q in qs:
            all_questions.append((trait, q))
    random.shuffle(all_questions)
    st.session_state.all_questions = all_questions
    st.session_state.current_q = 0
    st.session_state.responses = {}

all_questions = st.session_state.all_questions
current_q = st.session_state.current_q
responses = st.session_state.responses
total_qs = len(all_questions)

if current_q < total_qs:
    trait, question = all_questions[current_q]
    st.markdown(f"**Q{current_q+1}/{total_qs}**")
    st.write(question)

    options = [1,2,3,4,5]
    key = f"{trait}_{current_q}"

    default_index = options.index(responses[key]) if key in responses else None
    answer = st.radio("Select your answer:", options, horizontal=True, index=default_index, key=key)
    if answer:
        responses[key] = answer

    col1, col2 = st.columns([1,1])
    if col1.button("⬅️ Back", disabled=current_q==0):
        st.session_state.current_q -= 1
        st.experimental_rerun()
    if col2.button("➡️ Next Question"):
        if key in responses:
            st.session_state.current_q += 1
            st.experimental_rerun()
else:
    st.success("All questions complete — here are your results!")

    # Scores
    creative_scores = {t:0 for t in creative_traits}
    creative_counts = {t:0 for t in creative_traits}
    big5_scores = {t:0 for t in big5_traits}
    big5_counts = {t:0 for t in big5_traits}

    for key, val in responses.items():
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

    # Charts
    col1, col2 = st.columns(2)
    with col1:
        st.image(radar_chart(creative_scores, creative_colors, "Creative Traits"), use_container_width=True)
    with col2:
        st.image(radar_chart(big5_scores, big5_colors, "Big Five Traits"), use_container_width=True)

    # Archetypes
    sorted_traits = sorted(creative_scores.items(), key=lambda x: x[1], reverse=True)
    main_trait, sub_trait, weakest_trait = sorted_traits[0][0], sorted_traits[1][0], sorted_traits[-1][0]

    st.subheader("Your Creative Archetypes")
    for label, trait in [("Main Archetype", main_trait), ("Sub-Archetype", sub_trait), ("Growth Area", weakest_trait)]:
        if label == "Growth Area":
            content = archetypes[trait]["improvement"]
        else:
            content = archetypes[trait]["description"]
        st.markdown(
            f"<div style='background-color:{creative_colors[trait]}20; padding:0.7rem; border-radius:10px; margin:0.7rem 0;'>"
            f"<span style='color:{creative_colors[trait]}; font-weight:bold'>{label}: {archetypes[trait]['name']}</span><br>"
            f"<i>{content}</i></div>", unsafe_allow_html=True
        )

    # Summaries
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
