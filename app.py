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
    "Openness": [
        "I enjoy exploring new ideas and experiences.",
        "I have a vivid imagination.",
        "I often imagine possibilities that others don’t."
    ],
    "Risk-taking": [
        "I am comfortable taking chances with new ideas.",
        "I would rather try and fail than not try at all.",
        "I enjoy venturing into the unknown."
    ],
    "Resilience": [
        "I keep going when faced with creative setbacks.",
        "I see mistakes as opportunities to learn.",
        "I stay motivated even when things get tough."
    ],
    "Collaboration": [
        "I enjoy brainstorming with others.",
        "I build on the ideas of those around me.",
        "I value different perspectives in problem solving."
    ],
    "Divergent Thinking": [
        "I can think of many solutions to a problem.",
        "I enjoy finding unusual uses for common things.",
        "I like connecting unrelated concepts."
    ],
    "Convergent Thinking": [
        "I can evaluate which ideas are most useful.",
        "I am good at narrowing options to find the best one.",
        "I make decisions based on logic and evidence."
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
    "Openness": [
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
    ax.plot(angles, values, linewidth=2, color="black")
    ax.fill(angles, values, alpha=0.05, color="gray")

    # Colored segments
    for i, (trait, score) in enumerate(scores.items()):
        ax.plot([angles[i], angles[i+1]], [score, values[i+1]],
                color=colors[trait], linewidth=3)
        ax.scatter(angles[i], score, color=colors[trait], s=60, zorder=10)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylim(0,5)
    ax.set_yticks([1,2,3,4,5])
    ax.set_yticklabels(["1","2","3","4","5"])
    plt.title(title, size=12, weight="bold")
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)
    return buf

# --------------------------
# Streamlit App
# --------------------------
st.title("Creative Identity Profile")
st.write("Please rate each statement on a 1–5 scale: 1 = Strongly Disagree … 5 = Strongly Agree.")

# Shuffle questions once
if "all_questions" not in st.session_state:
    all_questions = []
    for trait, qs in {**creative_traits, **big5_traits}.items():
        for q in qs:
            all_questions.append((trait, q))
    random.shuffle(all_questions)
    st.session_state.all_questions = all_questions

all_questions = st.session_state.all_questions

if "responses" not in st.session_state:
    st.session_state.responses = {f"{trait}_{i}": None for i, (trait, _) in enumerate(all_questions, 1)}

responses = st.session_state.responses
total_qs = len(all_questions)
answered = 0

st.markdown("**Scale reference:** 1 = Strongly Disagree · 5 = Strongly Agree")

# Questions with missed highlighting
for i, (trait, question) in enumerate(all_questions, 1):
    key = f"{trait}_{i}"
    index_val = (responses[key] - 1) if responses[key] else None

    if responses[key] is None:
        q_label = f"⚠️ <span style='color:red; font-weight:bold'>Q{i}/{total_qs}: {question}</span>"
    else:
        q_label = f"Q{i}/{total_qs}: {question}"

    responses[key] = st.radio(
        q_label,
        [1,2,3,4,5],
        horizontal=True,
        index=index_val,
        key=key,
        label_visibility="visible"
    )
    if responses[key] is not None:
        answered += 1

st.progress(answered / total_qs)

# Results
if answered == total_qs:
    st.success("All questions complete — here are your results!")

    # Creative Scores
    creative_scores = {t:0 for t in creative_traits}
    creative_counts = {t:0 for t in creative_traits}
    for key, val in responses.items():
        if val:
            trait = key.split("_")[0]
            if trait in creative_scores:
                creative_scores[trait] += val
                creative_counts[trait] += 1
    for t in creative_scores:
        creative_scores[t] /= creative_counts[t]

    # Big Five Scores
    big5_scores = {t:0 for t in big5_traits}
    big5_counts = {t:0 for t in big5_traits}
    for key, val in responses.items():
        if val:
            trait = key.split("_")[0]
            if trait in big5_scores:
                big5_scores[trait] += val
                big5_counts[trait] += 1
    for t in big5_scores:
        big5_scores[t] /= big5_counts[t]

    # Charts
    c1, c2 = st.columns(2)
    with c1:
        st.image(radar_chart(creative_scores, creative_colors, "Creative Traits"))
    with c2:
        st.image(radar_chart(big5_scores, big5_colors, "Big Five Traits"))

    # Creative Archetypes
    sorted_traits = sorted(creative_scores.items(), key=lambda x: x[1], reverse=True)
    main_trait, sub_trait, weakest_trait = sorted_traits[0][0], sorted_traits[1][0], sorted_traits[-1][0]

    st.subheader("Your Creative Archetypes")
    st.markdown(
        f"<div style='background-color:{creative_colors[main_trait]}20; padding:0.75rem; border-radius:10px;'>"
        f"<b>Main Archetype: {main_trait}</b> — {creative_summaries[main_trait][get_level(creative_scores[main_trait])]}</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<div style='background-color:{creative_colors[sub_trait]}20; padding:0.75rem; border-radius:10px;'>"
        f"<b>Sub-Archetype: {sub_trait}</b> — {creative_summaries[sub_trait][get_level(creative_scores[sub_trait])]}</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<div style='background-color:{creative_colors[weakest_trait]}20; padding:0.75rem; border-radius:10px;'>"
        f"<b>Growth Area: {weakest_trait}</b> — {creative_summaries[weakest_trait][get_level(creative_scores[weakest_trait])]}</div>",
        unsafe_allow_html=True
    )

    # Big Five Archetypes
    sorted_big5 = sorted(big5_scores.items(), key=lambda x: x[1], reverse=True)
    main_big5, sub_big5, weak_big5 = sorted_big5[0][0], sorted_big5[1][0], sorted_big5[-1][0]

    st.subheader("Your Big Five Highlights")
    st.markdown(
        f"<div style='background-color:{big5_colors[main_big5]}20; padding:0.75rem; border-radius:10px;'>"
        f"<b>Dominant Trait: {main_big5}</b> — {big5_summaries[main_big5][get_level(big5_scores[main_big5])]}</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<div style='background-color:{big5_colors[sub_big5]}20; padding:0.75rem; border-radius:10px;'>"
        f"<b>Secondary Trait: {sub_big5}</b> — {big5_summaries[sub_big5][get_level(big5_scores[sub_big5])]}</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<div style='background-color:{big5_colors[weak_big5]}20; padding:0.75rem; border-radius:10px;'>"
        f"<b>Growth Area: {weak_big5}</b> — {big5_summaries[weak_big5][get_level(big5_scores[weak_big5])]}</div>",
        unsafe_allow_html=True
    )
