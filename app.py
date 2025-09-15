import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
import random

# --------------------------
# Trait summaries
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

bigfive_summaries = {
    "Openness": {
        "High": "You are highly curious and imaginative.",
        "Medium": "You balance creativity with practicality.",
        "Low": "You prefer familiar routines and concrete thinking."
    },
    "Conscientiousness": {
        "High": "You are organized and dependable.",
        "Medium": "You balance planning with flexibility.",
        "Low": "You prefer spontaneity over structure."
    },
    "Extraversion": {
        "High": "You are outgoing and energized by social interaction.",
        "Medium": "You enjoy both social time and solitude.",
        "Low": "You are reflective and recharge in quiet spaces."
    },
    "Agreeableness": {
        "High": "You are compassionate and cooperative.",
        "Medium": "You balance empathy with assertiveness.",
        "Low": "You are more direct and value honesty over harmony."
    },
    "Neuroticism": {
        "High": "You are sensitive to stress and emotions.",
        "Medium": "You balance calmness with occasional worry.",
        "Low": "You are emotionally stable and resilient."
    }
}

# --------------------------
# Trait colors
# --------------------------
creative_colors = {
    "Openness": "#6A5ACD",
    "Risk-taking": "#FF4500",
    "Resilience": "#228B22",
    "Collaboration": "#1E90FF",
    "Divergent Thinking": "#FFD700",
    "Convergent Thinking": "#8A2BE2"
}

bigfive_colors = {
    "Openness": "#FF69B4",
    "Conscientiousness": "#20B2AA",
    "Extraversion": "#FFA500",
    "Agreeableness": "#32CD32",
    "Neuroticism": "#DC143C"
}

# --------------------------
# Radar Chart
# --------------------------
def radar_chart(scores: dict, colors: dict, title="") -> io.BytesIO:
    labels = list(scores.keys())
    num_vars = len(labels)
    angles = np.linspace(0, 2*np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    values = list(scores.values())
    values += values[:1]

    fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))
    ax.plot(angles, values, linewidth=2, color="black")
    ax.fill(angles, values, alpha=0.1, color="gray")

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
    ax.legend(bbox_to_anchor=(1.15,1.1))

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)
    return buf

# --------------------------
# Helper functions
# --------------------------
def score_to_level(score):
    if score >= 3.5: return "High"
    elif score >= 2.5: return "Medium"
    else: return "Low"

def archetype_box(title, dominant, secondary, growth, colors):
    st.markdown(
        f"<div style='background-color:#f9f9f9; padding:1rem; border-radius:10px; "
        f"box-shadow:0 2px 6px rgba(0,0,0,0.1); margin-top:1rem'>"
        f"<h4 style='margin-bottom:0.5rem'>{title}</h4>"
        f"<b style='color:{colors[dominant]};'>Dominant:</b> {dominant}<br>"
        f"<b style='color:{colors[secondary]};'>Secondary:</b> {secondary}<br>"
        f"<b style='color:{colors[growth]};'>Growth Area:</b> {growth}"
        f"</div>", unsafe_allow_html=True
    )

# --------------------------
# Streamlit App
# --------------------------
st.title("🎨 Creative Identity & Big Five Profile")

# Example questions (can be expanded)
creative_questions = {
    "Openness": ["I enjoy trying out new ideas.", "I like exploring unusual concepts."],
    "Risk-taking": ["I am comfortable taking chances.", "I embrace uncertainty."],
    "Resilience": ["I bounce back quickly after setbacks.", "I learn from failures easily."],
    "Collaboration": ["I work well with others.", "I enjoy sharing ideas in groups."],
    "Divergent Thinking": ["I can think of many different solutions.", "I often generate unusual ideas."],
    "Convergent Thinking": ["I can refine ideas into practical solutions.", "I focus well when narrowing down options."]
}

bigfive_questions = {
    "Openness": ["I enjoy art, music, or literature.", "I am curious about new things."],
    "Conscientiousness": ["I am always prepared.", "I follow a schedule."],
    "Extraversion": ["I feel comfortable around people.", "I start conversations easily."],
    "Agreeableness": ["I sympathize with others' feelings.", "I take time out for others."],
    "Neuroticism": ["I get stressed easily.", "I often feel blue."]
}

all_questions = [(t,q) for t,qs in {**creative_questions, **bigfive_questions}.items() for q in qs]
random.shuffle(all_questions)

st.header("📝 Questionnaire")
responses = {}
total_qs = len(all_questions)

for i, (trait, question) in enumerate(all_questions, 1):
    key = f"{trait}_{i}"
    responses.setdefault(key, None)

    # Highlight missed in red (no ⚠️)
    if responses[key] is None:
        st.markdown(
            f"<span style='color:red; font-weight:bold'>Q{i}/{total_qs}: {question}</span>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(f"Q{i}/{total_qs}: {question}")

    responses[key] = st.radio(
        "", [1,2,3,4,5],
        horizontal=True,
        index=(responses[key]-1) if responses[key] else None,
        key=key
    )

if st.button("Show Results"):
    creative_scores = {t: np.mean([responses[f"{t}_{i}"] for i,(tt,_) in enumerate(all_questions,1) if tt==t]) for t in creative_questions}
    bigfive_scores = {t: np.mean([responses[f"{t}_{i}"] for i,(tt,_) in enumerate(all_questions,1) if tt==t]) for t in bigfive_questions}

    st.header("🎭 Creative Traits")
    for t, score in creative_scores.items():
        lvl = score_to_level(score)
        st.markdown(
            f"<div style='background-color:{creative_colors[t]}20; padding:0.5rem; border-radius:8px; margin:0.5rem 0;'>"
            f"<span style='color:{creative_colors[t]}; font-weight:bold'>{t} ({lvl})</span> — {score:.2f}/5<br>"
            f"<i>{creative_summaries[t][lvl]}</i></div>", unsafe_allow_html=True
        )

    dom, sec, growth = sorted(creative_scores, key=creative_scores.get, reverse=True)[:2] + [min(creative_scores, key=creative_scores.get)]
    archetype_box("Creative Archetype", dom, sec, growth, creative_colors)

    st.header("🌟 Big Five Traits")
    for t, score in bigfive_scores.items():
        lvl = score_to_level(score)
        st.markdown(
            f"<div style='background-color:{bigfive_colors[t]}20; padding:0.5rem; border-radius:8px; margin:0.5rem 0;'>"
            f"<span style='color:{bigfive_colors[t]}; font-weight:bold'>{t} ({lvl})</span> — {score:.2f}/5<br>"
            f"<i>{bigfive_summaries[t][lvl]}</i></div>", unsafe_allow_html=True
        )

    dom, sec, growth = sorted(bigfive_scores, key=bigfive_scores.get, reverse=True)[:2] + [min(bigfive_scores, key=bigfive_scores.get)]
    archetype_box("Big Five Archetype", dom, sec, growth, bigfive_colors)

    st.header("📊 Radar Charts")
    st.image(radar_chart(creative_scores, creative_colors, "Creative Traits"))
    st.image(radar_chart(bigfive_scores, bigfive_colors, "Big Five Traits"))

