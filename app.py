import streamlit as st
import random
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Creative Identity Profile", layout="centered")

# --------------------------
# Trait Definitions
# --------------------------
creative_traits = ["Curiosity", "Imagination", "Risk-taking", "Persistence", "Collaboration", "Openness"]
bigfive_traits = ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"]

creative_colors = {
    "Curiosity": "#FF6F61",
    "Imagination": "#6B5B95",
    "Risk-taking": "#88B04B",
    "Persistence": "#FFA500",
    "Collaboration": "#009B77",
    "Openness": "#6495ED"
}

bigfive_colors = {
    "Openness": "#1f77b4",
    "Conscientiousness": "#ff7f0e",
    "Extraversion": "#2ca02c",
    "Agreeableness": "#d62728",
    "Neuroticism": "#9467bd"
}

# --------------------------
# Questions
# --------------------------
questions = {
    "Curiosity": [
        "I enjoy exploring new ideas.",
        "I often ask questions about how things work."
    ],
    "Imagination": [
        "I often come up with unusual ideas.",
        "I enjoy activities that let me create something new."
    ],
    "Risk-taking": [
        "I am willing to try new approaches even if they might fail.",
        "I feel comfortable taking chances in creative projects."
    ],
    "Persistence": [
        "I keep working on a problem until I find a solution.",
        "I don’t give up easily when faced with obstacles."
    ],
    "Collaboration": [
        "I enjoy working with others on creative projects.",
        "I listen to and build on other people’s ideas."
    ],
    "Openness": [
        "I am open to experiences that are different from my own.",
        "I am willing to consider ideas that challenge my beliefs."
    ],
    "Conscientiousness": [
        "I like to plan and organise tasks carefully.",
        "I follow through with commitments I make."
    ],
    "Extraversion": [
        "I feel energised when spending time with others.",
        "I enjoy being the centre of attention."
    ],
    "Agreeableness": [
        "I try to be considerate and kind to others.",
        "I value cooperation over competition."
    ],
    "Neuroticism": [
        "I often feel worried or anxious.",
        "I get stressed easily when things don’t go as planned."
    ]
}

# Shuffle questions
all_questions = []
for trait, qs in questions.items():
    for q in qs:
        all_questions.append((trait, q))
random.shuffle(all_questions)

# --------------------------
# Summaries
# --------------------------
creative_summaries = {
    "Curiosity": {
        "High": "You are highly curious and love exploring new ideas.",
        "Medium": "You are curious at times but may not always dive deeply.",
        "Low": "You tend to prefer the familiar over exploring new ideas."
    },
    "Imagination": {
        "High": "You have a vivid imagination and often think outside the box.",
        "Medium": "You sometimes use imagination in your thinking.",
        "Low": "You rely more on practical approaches than imaginative ones."
    },
    "Risk-taking": {
        "High": "You embrace risk and are open to failure as part of creativity.",
        "Medium": "You take risks occasionally when comfortable.",
        "Low": "You prefer safe approaches and avoid unnecessary risks."
    },
    "Persistence": {
        "High": "You stay determined until challenges are solved.",
        "Medium": "You keep trying but may step back if things get tough.",
        "Low": "You may find it difficult to keep going when faced with obstacles."
    },
    "Collaboration": {
        "High": "You thrive in teamwork and creative collaboration.",
        "Medium": "You collaborate when needed but may prefer independence.",
        "Low": "You often prefer working alone on creative projects."
    },
    "Openness": {
        "High": "You are highly open to new experiences and perspectives.",
        "Medium": "You are open sometimes but still prefer familiar paths.",
        "Low": "You value stability and consistency over new experiences."
    }
}

bigfive_summaries = {
    "Openness": {
        "High": "You are imaginative and open to trying new things.",
        "Medium": "You are somewhat open but also value routine.",
        "Low": "You prefer familiar routines and traditional ideas."
    },
    "Conscientiousness": {
        "High": "You are organised, reliable, and self-disciplined.",
        "Medium": "You are somewhat organised but not always consistent.",
        "Low": "You are spontaneous and may struggle with organisation."
    },
    "Extraversion": {
        "High": "You are outgoing, energetic, and enjoy socialising.",
        "Medium": "You enjoy company but also need time alone.",
        "Low": "You are more reserved and prefer quieter settings."
    },
    "Agreeableness": {
        "High": "You are compassionate and cooperative.",
        "Medium": "You are sometimes cooperative but also assertive.",
        "Low": "You tend to be more competitive or critical."
    },
    "Neuroticism": {
        "High": "You may feel emotions strongly and experience stress easily.",
        "Medium": "You experience some ups and downs but manage them.",
        "Low": "You tend to remain calm and resilient under pressure."
    }
}

# --------------------------
# Questionnaire
# --------------------------
st.header("Questionnaire")
responses = {}
total_qs = len(all_questions)

for i, (trait, question) in enumerate(all_questions, 1):
    key = f"{trait}_{i}"
    responses.setdefault(key, None)

    # Show question text (red if unanswered)
    if responses[key] is None:
        st.markdown(
            f"<p style='color:red; font-weight:bold'>Q{i}/{total_qs}: {question}</p>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(f"Q{i}/{total_qs}: {question}")

    # Radio without label
    responses[key] = st.radio(
        label="", 
        options=[1,2,3,4,5],
        horizontal=True,
        index=(responses[key] - 1) if responses[key] else None,
        key=key
    )

# --------------------------
# Submit
# --------------------------
if st.button("Submit"):
    # Calculate scores
    scores = {t: [] for t in creative_traits + bigfive_traits}
    for key, val in responses.items():
        if val is not None:
            trait = key.split("_")[0]
            scores[trait].append(val)
    avg_scores = {t: np.mean(vals) if vals else 0 for t, vals in scores.items()}

    st.header("Your Results")

    # Creative Results
    st.subheader("Creative Traits")
    for trait in creative_traits:
        score = avg_scores[trait]
        if score >= 4:
            level = "High"
        elif score >= 2.5:
            level = "Medium"
        else:
            level = "Low"
        summary = creative_summaries[trait][level]
        st.markdown(
            f"<div style='background-color:{creative_colors[trait]}20; padding:0.5rem; border-radius:8px; margin:0.5rem 0;'>"
            f"<span style='color:{creative_colors[trait]}; font-weight:bold'>{trait} ({level})</span> — {score:.2f}/5<br>"
            f"<i>{summary}</i></div>",
            unsafe_allow_html=True
        )

    # Big Five Results
    st.subheader("Big Five Traits")
    for trait in bigfive_traits:
        score = avg_scores[trait]
        if score >= 4:
            level = "High"
        elif score >= 2.5:
            level = "Medium"
        else:
            level = "Low"
        summary = bigfive_summaries[trait][level]
        st.markdown(
            f"<div style='background-color:{bigfive_colors[trait]}20; padding:0.5rem; border-radius:8px; margin:0.5rem 0;'>"
            f"<span style='color:{bigfive_colors[trait]}; font-weight:bold'>{trait} ({level})</span> — {score:.2f}/5<br>"
            f"<i>{summary}</i></div>",
            unsafe_allow_html=True
        )

    # Radar Chart
    st.subheader("Radar Chart")
    labels = creative_traits + bigfive_traits
    values = [avg_scores[t] for t in labels]
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))
    for trait in labels:
        vals = [avg_scores[trait]] * (len(labels)+1)
        ax.plot(angles, vals, label=trait, color=creative_colors.get(trait, bigfive_colors.get(trait)))
    ax.fill(angles, values, alpha=0.1)
    ax.set_yticks([1,2,3,4,5])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.legend(bbox_to_anchor=(1.1, 1.05))
    st.pyplot(fig)
