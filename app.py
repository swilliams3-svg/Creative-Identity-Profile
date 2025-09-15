import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import io
import random

st.set_page_config(page_title="Creative Identity Profile", layout="centered")

# --------------------------
# Trait dictionaries (3 questions each)
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

# --------------------------
# Colours
# --------------------------
creative_colors = {
    "Openness": "#17becf",
    "Risk-taking": "#e377c2",
    "Resilience": "#bcbd22",
    "Collaboration": "#8c564b",
    "Divergent Thinking": "#7f7f7f",
    "Convergent Thinking": "#aec7e8"
}

big5_colors = {
    "Conscientiousness": "#ff7f0e",
    "Extraversion": "#2ca02c",
    "Agreeableness": "#9467bd",
    "Neuroticism": "#d62728",
    "Openness": "#1f77b4"
}

# --------------------------
# Archetypes (based on creative traits)
# --------------------------
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

# --------------------------
# Summaries for traits
# --------------------------
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

big5_summaries = {
    "Conscientiousness": {
        "High": "You are organized, disciplined, and reliable.",
        "Medium": "You are reasonably structured but flexible.",
        "Low": "You may prefer spontaneity over strict planning."
    },
    "Extraversion": {
        "High": "You are outgoing and energized by social interaction.",
        "Medium": "You balance sociability with enjoying time alone.",
        "Low": "You may prefer solitude and quiet environments."
    },
    "Agreeableness": {
        "High": "You are compassionate and cooperative.",
        "Medium": "You are kind but balance empathy with assertiveness.",
        "Low": "You may prioritize honesty or independence over harmony."
    },
    "Neuroticism": {
        "High": "You are sensitive to stress and may feel emotions intensely.",
        "Medium": "You sometimes worry but can stay balanced.",
        "Low": "You are calm and resilient under pressure."
    },
    "Openness": {
        "High": "You enjoy variety, curiosity, and creative experiences.",
        "Medium": "You are open to some new things but also value tradition.",
        "Low": "You may prefer routine and familiar experiences."
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

    # plot each trait
    for trait, score in scores.items():
        values = [score] * num_vars
        values += values[:1]
        ax.plot(angles, values, linewidth=2, color=colors[trait], label=trait)
        ax.fill(angles, values, alpha=0.15, color=colors[trait])

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylim(0,5)
    ax.set_yticks([1,2,3,4,5])
    ax.set_yticklabels(["1","2","3","4","5"])
    plt.title(title, size=12, weight="bold")
    ax.legend(bbox_to_anchor=(1.1, 1.1))

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)
    return buf

def bar_chart(scores: dict, colors: dict, title="") -> io.BytesIO:
    labels = list(scores.keys())
    values = list(scores.values())
    fig, ax = plt.subplots(figsize=(5,4))
    ax.bar(labels, values, color=[colors[t] for t in labels])
    ax.set_ylim(0,5)
    ax.set_ylabel("Average Score")
    ax.set_title(title, weight="bold")
    plt.xticks(rotation=30, ha="right")
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

# Shuffle once
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

# Likert scale reference
st.markdown("**Scale reference:** 1 = Strongly Disagree · 2 = Disagree · 3 = Neutral · 4 = Agree · 5 = Strongly Agree")

for i, (trait, question) in enumerate(all_questions, 1):
    key = f"{trait}_{i}"
    index_val = (responses[key] - 1) if responses[key] else None
    responses[key] = st.radio(f"Q{i}/{total_qs}: {question}", [1,2,3,4,5],
                              horizontal=True, index=index_val, key=key)
    if responses[key] is not None:
        answered += 1

st.progress(answered / total_qs)

# Results
if answered == total_qs:
    st.success("All questions complete — here are your results!")

    # Creative trait scores
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

    # Big Five scores
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
        st.image(radar_chart(creative_scores, creative_colors, "Creative Traits"), use_container_width=True)
    with c2:
        st.image(bar_chart(big5_scores, big5_colors, "Big Five Traits"), use_container_width=True)

    # Archetypes
    sorted_traits = sorted(creative_scores.items(), key=lambda x: x[1], reverse=True)
    main_trait, sub_trait, weakest_trait = sorted_traits[0][0], sorted_traits[1][0], sorted_traits[-1][0]

    st.subheader("Your Creative Archetypes")
    st.write(f"**Main Archetype: {archetypes[main_trait]['name']}** — {archetypes[main_trait]['description']}")
    st.write(f"**Sub-Archetype: {archetypes[sub_trait]['name']}** — {archetypes[sub_trait]['description']}")
    st.write(f"**Growth Area ({weakest_trait})** — {archetypes[weakest_trait]['improvement']}")

    # Summary box
    main_color = creative_colors[main_trait]
    st.markdown(
        f"""
        <div style="background-color:{main_color}20; padding:1rem; border-radius:12px; 
                    margin-top:1rem; border: 2px solid {main_color};">
            <h4 style="margin:0; color:{main_color};">Summary</h4>
            <p style="margin:0.5rem 0 0 0;">
                <span style="color:{creative_colors[main_trait]};">
                    <b>Main Archetype:</b> {archetypes[main_trait]['name']} ({main_trait})
                </span><br>
                <span style="color:{creative_colors[sub_trait]};">
                    <b>Sub-Archetype:</b> {archetypes[sub_trait]['name']} ({sub_trait})
                </span><br>
                <span style="color:{creative_colors[weakest_trait]};">
                    <b>Growth Area:</b> {weakest_trait} — {archetypes[weakest_trait]['improvement']}
                </span>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Trait Insights
    st.subheader("Trait Insights")
    st.markdown("**Creative Traits**")
    for trait, score in creative_scores.items():
        level = get_level(score)
        summary = creative_summaries[trait][level]
        st.markdown(
            f"<div style='background-color:{creative_colors[trait]}20; padding:0.5rem; border-radius:8px; margin:0.5rem 0;'>"
            f"<span style='color:{creative_colors[trait]}; font-weight:bold'>{trait} ({level})</span> — {score:.2f}/5<br>"
            f"<i>{summary}</i></div>", unsafe_allow_html=True
        )

    st.markdown("**Big Five Traits**")
    for trait, score in big5_scores.items():
        level = get_level(score)
        summary = big5_summaries[trait][level]
        st.markdown(
            f"<div style='background-color:{big5_colors[trait]}20; padding:0.5rem; border-radius:8px; margin:0.5rem 0;'>"
            f"<span style='color:{big5_colors[trait]}; font-weight:bold'>{trait} ({level})</span> — {score:.2f}/5<br>"
            f"<i>{summary}</i></div>", unsafe_allow_html=True
        )
