import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import io
import random

st.set_page_config(page_title="Creative Identity Profile", layout="centered")

# --------------------------
# Traits with questions
# --------------------------
traits = {
    "Openness": [
        "I enjoy exploring new ideas and experiences.",
        "I often imagine possibilities that others don’t.",
        "I like experimenting with unusual approaches.",
        "I am curious about many different things."
    ],
    "Risk-taking": [
        "I am comfortable taking chances with new ideas.",
        "I don’t mind uncertainty when trying something new.",
        "I would rather try and fail than not try at all.",
        "I enjoy venturing into the unknown."
    ],
    "Resilience": [
        "I keep going when faced with creative setbacks.",
        "I see mistakes as opportunities to learn.",
        "I bounce back quickly after difficulties.",
        "I stay motivated even when things get tough."
    ],
    "Collaboration": [
        "I enjoy brainstorming with others.",
        "I build on the ideas of those around me.",
        "I value different perspectives in problem solving.",
        "I work well in creative teams."
    ],
    "Divergent Thinking": [
        "I can think of many solutions to a problem.",
        "I enjoy finding unusual uses for common things.",
        "I generate lots of ideas quickly.",
        "I like connecting unrelated concepts."
    ],
    "Convergent Thinking": [
        "I can evaluate which ideas are most useful.",
        "I am good at narrowing options to find the best one.",
        "I can turn many ideas into a clear plan.",
        "I make decisions based on logic and evidence."
    ]
}

# Archetypes
archetypes = {
    "Openness": {
        "name": "The Explorer",
        "description": "You thrive on curiosity and imagination. Explorers see possibilities everywhere, though sometimes risk being unfocused.",
        "improvement": "Try allocating short, focused 'exploration sprints' followed by a pause to capture the best ideas."
    },
    "Risk-taking": {
        "name": "The Adventurer",
        "description": "You embrace uncertainty and try new things. Adventurers push boundaries but should manage exposure to unnecessary risk.",
        "improvement": "Set low-cost experiments to test risky ideas before committing significant resources."
    },
    "Resilience": {
        "name": "The Perseverer",
        "description": "You persist through challenges and learn from failure. Perseverers build strength from setbacks.",
        "improvement": "Schedule reflection time after setbacks: note lessons and small wins to maintain momentum."
    },
    "Collaboration": {
        "name": "The Connector",
        "description": "You spark ideas in groups and value diverse perspectives. Connectors thrive in teams but may sometimes overlook their own vision.",
        "improvement": "Block time for solitary work to develop your own voice and deepen ideas before sharing."
    },
    "Divergent Thinking": {
        "name": "The Visionary",
        "description": "You generate many original ideas and enjoy unusual connections. Visionaries excel at imagination but can struggle with focus.",
        "improvement": "Use idea-ranking criteria to select a few promising concepts to develop further."
    },
    "Convergent Thinking": {
        "name": "The Strategist",
        "description": "You refine and structure ideas into action. Strategists provide clarity but can miss chance opportunities by being too selective.",
        "improvement": "Schedule 'wild idea' sessions to intentionally loosen constraints before applying evaluation."
    }
}

# Trait colours
trait_colors = {
    "Openness": "tab:blue",
    "Risk-taking": "tab:red",
    "Resilience": "tab:green",
    "Collaboration": "tab:orange",
    "Divergent Thinking": "tab:purple",
    "Convergent Thinking": "tab:brown"
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

# Radar chart
def radar_chart(scores: dict) -> io.BytesIO:
    labels = list(scores.keys())
    values = list(scores.values())
    num_vars = len(labels)

    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))

    for i, trait in enumerate(labels):
        val_pair = [values[i], values[i+1]] if i < len(labels)-1 else [values[i], values[0]]
        angle_pair = [angles[i], angles[i+1]] if i < len(labels)-1 else [angles[i], angles[0]]
        ax.plot(angle_pair, val_pair, color=trait_colors[trait], linewidth=3)
        ax.fill(angle_pair, val_pair, alpha=0.2, color=trait_colors[trait])

    ax.set_ylim(0,5)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_yticks([1,2,3,4,5])
    ax.set_yticklabels(["1","2","3","4","5"])

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)
    return buf

# Bar chart
def bar_chart(scores: dict) -> io.BytesIO:
    fig, ax = plt.subplots(figsize=(6,4))
    traits_list = list(scores.keys())
    values = list(scores.values())
    ax.bar(traits_list, values, color=[trait_colors[t] for t in traits_list])
    ax.set_ylim(0,5)
    ax.set_ylabel("Score")
    ax.set_title("Trait Scores")
    plt.xticks(rotation=45, ha="right")

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)
    return buf

# --------------------------
# Streamlit UI
# --------------------------
st.title("Creative Identity Profile")
st.write("Please respond to each statement on a 1–5 scale:")

# Shuffle questions once
if "all_questions" not in st.session_state:
    all_questions = []
    for trait, qs in traits.items():
        for q in qs:
            all_questions.append((trait, q))
    random.shuffle(all_questions)
    st.session_state.all_questions = all_questions

all_questions = st.session_state.all_questions

# Store responses
if "responses" not in st.session_state:
    st.session_state.responses = {f"{trait}_{i}": None for i, (trait, _) in enumerate(all_questions, 1)}

responses = st.session_state.responses
total_qs = len(all_questions)

# Show questions
answered = 0
for i, (trait, question) in enumerate(all_questions, 1):
    key = f"{trait}_{i}"
    index_val = (responses[key] - 1) if responses[key] else None
    st.caption("1 = Strongly Disagree · 5 = Strongly Agree")
    responses[key] = st.radio(
        f"Q{i}/{total_qs}: {question}",
        [1,2,3,4,5],
        horizontal=True,
        index=index_val,
        key=key
    )
    if responses[key] is not None:
        answered += 1

# Progress
st.write(f"Progress: {answered}/{total_qs} questions answered")
st.progress(answered / total_qs)

# Warn about missed questions
missed = [q for (trait, q), (k, v) in zip(all_questions, responses.items()) if v is None]
if missed:
    st.warning(f"You have {len(missed)} unanswered question(s). Scroll up to complete them before results will show.")

# Results
if answered == total_qs:
    st.success("Questionnaire complete — here are your results:")

    # aggregate per-trait scores
    scores = {trait: 0.0 for trait in traits}
    counts = {trait: 0 for trait in traits}
    for key, val in responses.items():
        if val is not None:
            trait = key.split("_")[0]
            scores[trait] += val
            counts[trait] += 1
    for trait in scores:
        scores[trait] = (scores[trait] / counts[trait]) if counts[trait] else 0.0

    # Charts side by side
    col1, col2 = st.columns(2)
    with col1:
        st.image(radar_chart(scores).getvalue(), caption="Your Creative Trait Profile", use_container_width=True)
    with col2:
        st.image(bar_chart(scores).getvalue(), caption="Trait Scores", use_container_width=True)

    # Archetypes
    sorted_traits = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    main_trait = sorted_traits[0][0]
    sub_trait = sorted_traits[1][0]
    weakest_trait = sorted_traits[-1][0]

    st.subheader("Your Creative Archetype")
    st.info(f"**Main Archetype: {archetypes[main_trait]['name']}**\n\n{archetypes[main_trait]['description']}")
    st.write(f"Sub-Archetype: **{archetypes[sub_trait]['name']}** — {archetypes[sub_trait]['description']}")

    st.subheader("Ways to grow")
    st.write(f"Weaker area: **{weakest_trait}** — {archetypes[weakest_trait]['improvement']}")

    st.subheader("Trait Insights")
    for trait, score in scores.items():
        level = get_level(score)
        st.markdown(
            f"<span style='color:{trait_colors[trait]}; font-weight:bold'>{trait} ({level})</span> — {score:.2f}/5",
            unsafe_allow_html=True
        )

