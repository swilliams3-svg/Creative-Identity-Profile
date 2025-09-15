import streamlit as st
import random
import matplotlib.pyplot as plt
import numpy as np

# --------------------------
# Initial setup
# --------------------------
st.set_page_config(page_title="Creative Identity Profile", layout="wide")

if "responses" not in st.session_state:
    st.session_state.responses = {}

if "current_q" not in st.session_state:
    st.session_state.current_q = 0

if "questions" not in st.session_state:
    creative_traits = {
        "Divergent Thinking": [
            "I often come up with many different ideas for a problem.",
            "I enjoy thinking of alternative uses for common objects.",
            "I like to brainstorm unusual approaches to challenges."
        ],
        "Risk-taking": [
            "I am willing to take risks to try out new ideas.",
            "I feel comfortable with uncertainty when exploring new projects.",
            "I would rather try something bold than play it safe."
        ],
        "Openness to Experience": [
            "I enjoy exploring new experiences and ideas.",
            "I actively seek out new perspectives.",
            "I am drawn to new artistic or cultural experiences."
        ],
        "Persistence": [
            "I keep working on ideas even when they are challenging.",
            "I continue with projects despite initial failures.",
            "I rarely give up on problems until I find a solution."
        ],
        "Curiosity": [
            "I frequently ask questions about how things work.",
            "I seek to learn about topics outside my area of expertise.",
            "I often investigate things just to satisfy my curiosity."
        ],
        "Tolerance of Ambiguity": [
            "I am comfortable working on tasks without clear solutions.",
            "I enjoy exploring ideas that don’t have definite answers.",
            "I don’t mind when instructions or goals are unclear."
        ]
    }

    big_five = {
        "Openness": [
            "I have a vivid imagination.",
            "I am full of ideas.",
            "I enjoy reflecting on abstract concepts."
        ],
        "Conscientiousness": [
            "I like order.",
            "I follow a schedule.",
            "I pay attention to details."
        ],
        "Extraversion": [
            "I feel comfortable around people.",
            "I start conversations.",
            "I make friends easily."
        ],
        "Agreeableness": [
            "I sympathize with others’ feelings.",
            "I take time out for others.",
            "I am interested in other people’s problems."
        ],
        "Neuroticism": [
            "I often feel blue.",
            "I get stressed out easily.",
            "I worry about things."
        ]
    }

    all_qs = []
    for trait, qs in {**creative_traits, **big_five}.items():
        for q in qs:
            all_qs.append((trait, q))

    random.shuffle(all_qs)
    st.session_state.questions = all_qs

all_questions = st.session_state.questions
total_qs = len(all_questions)

# --------------------------
# Helpers
# --------------------------
def calculate_scores(responses, questions):
    scores = {}
    for trait, _ in questions:
        scores[trait] = []

    for idx, (trait, _) in enumerate(questions):
        key = f"{trait}_{idx}"
        if key in responses and responses[key] is not None:
            scores[trait].append(responses[key])

    avg_scores = {t: (sum(v) / len(v)) if v else 0 for t, v in scores.items()}
    return avg_scores

def radar_chart(scores, title):
    traits = list(scores.keys())
    values = list(scores.values())
    N = len(traits)

    values += values[:1]
    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))
    ax.fill(angles, values, alpha=0.25, color="skyblue")
    ax.plot(angles, values, linewidth=2, color="blue")

    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(traits)
    st.markdown(f"#### {title}")
    st.pyplot(fig)

def show_archetypes(main_trait, sub_trait, growth_trait):
    archetypes = {
        "Divergent Thinking": ("The Visionary", "Sees possibilities everywhere and generates many ideas."),
        "Risk-taking": ("The Explorer", "Brave, bold, and unafraid to step into the unknown."),
        "Openness to Experience": ("The Dreamer", "Drawn to new, imaginative, and creative experiences."),
        "Persistence": ("The Determined", "Keeps pushing ideas forward even through challenges."),
        "Curiosity": ("The Investigator", "Always questioning, learning, and exploring."),
        "Tolerance of Ambiguity": ("The Adaptable", "Comfortable in uncertain, undefined situations.")
    }

    st.markdown("### Your Creative Archetypes")
    for role, trait in [("Main Archetype", main_trait),
                        ("Sub-Archetype", sub_trait),
                        ("Growth Area", growth_trait)]:
        if trait in archetypes:
            title, desc = archetypes[trait]
            st.markdown(
                f"""
                <div style='background-color:#f0f8ff; padding:15px; border-radius:12px; margin-bottom:10px'>
                <b>{role}: {title}</b><br>{desc}
                </div>
                """,
                unsafe_allow_html=True
            )

def show_trait_summaries(scores):
    st.markdown("### Trait Insights")
    for trait, score in scores.items():
        if score >= 4:
            level = "High"
            desc = "You show strong alignment with this trait."
            color = "#d4f5d0"
        elif score >= 2.5:
            level = "Medium"
            desc = "You show a balanced level of this trait."
            color = "#fff3cd"
        else:
            level = "Low"
            desc = "This trait is less expressed for you."
            color = "#f8d7da"

        st.markdown(
            f"""
            <div style='background-color:{color}; padding:12px; border-radius:10px; margin-bottom:6px'>
            <b>{trait} ({level}):</b> {score:.2f}/5<br>{desc}
            </div>
            """,
            unsafe_allow_html=True
        )

# --------------------------
# Quiz flow
# --------------------------
current_q = st.session_state.current_q

if current_q < total_qs:
    trait, question = all_questions[current_q]
    key = f"{trait}_{current_q}"

    st.markdown(f"### Question {current_q+1} of {total_qs}")
    st.write(f"**{question}**")

    options = [1, 2, 3, 4, 5]

    if key in st.session_state.responses and st.session_state.responses[key] in options:
        default_index = options.index(st.session_state.responses[key])
    else:
        default_index = None  # start blank

    answer = st.radio(
        "Select your answer:",
        options,
        horizontal=True,
        index=default_index,
        key=key
    )

    # Navigation buttons
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("Back", disabled=(current_q == 0)):
            st.session_state.current_q -= 1
            st.rerun()
    with col2:
        if st.button("Forward"):
            st.session_state.responses[key] = answer
            st.session_state.current_q += 1
            st.rerun()

# --------------------------
# Results page
# --------------------------
else:
    st.success("✅ All questions complete — here are your results!")

    responses = st.session_state.responses
    scores = calculate_scores(responses, all_questions)

    # Split scores
    creative_traits = ["Divergent Thinking","Risk-taking","Openness to Experience",
                       "Persistence","Curiosity","Tolerance of Ambiguity"]
    big_five = ["Openness","Conscientiousness","Extraversion","Agreeableness","Neuroticism"]

    creative_scores = {t: scores[t] for t in creative_traits}
    big_five_scores = {t: scores[t] for t in big_five}

    # Show charts
    radar_chart(creative_scores, "Creative Traits")
    radar_chart(big_five_scores, "Big Five Personality Traits")

    # Archetypes (main, sub, growth)
    sorted_traits = sorted(creative_scores.items(), key=lambda x: x[1], reverse=True)
    main_trait, sub_trait = sorted_traits[0][0], sorted_traits[1][0]
    growth_trait = sorted_traits[-1][0]
    show_archetypes(main_trait, sub_trait, growth_trait)

    # Summaries
    show_trait_summaries(scores)

    # Questions missed
    missed = [f"Q{i+1}: {q}" for i, (_, q) in enumerate(all_questions)
              if st.session_state.responses.get(f"{all_questions[i][0]}_{i}") is None]

    if missed:
        st.warning("⚠️ You missed some questions:")
        for m in missed:
            st.write(f"- {m}")

