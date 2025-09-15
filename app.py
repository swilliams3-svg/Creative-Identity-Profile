import streamlit as st
import random
import matplotlib.pyplot as plt
import numpy as np

# -------------------------
# Question Dictionaries
# -------------------------
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
    ]
}

# Trait descriptions
trait_descriptions = {
    "Openness": "Curious, imaginative, open to new experiences.",
    "Risk-taking": "Comfortable with uncertainty and bold ideas.",
    "Resilience": "Able to bounce back after setbacks.",
    "Collaboration": "Enjoys working with and learning from others.",
    "Divergent Thinking": "Generates many creative possibilities.",
    "Convergent Thinking": "Evaluates and selects the best solutions.",
    "Conscientiousness": "Organised, disciplined, reliable.",
    "Extraversion": "Outgoing, talkative, energised by others.",
    "Agreeableness": "Compassionate and cooperative.",
    "Neuroticism": "Prone to worry, stress, and emotional swings."
}

# Archetypes (simplified example, you can expand)
archetypes = {
    "Openness": {"name": "The Explorer", "description": "You thrive on curiosity and new experiences."},
    "Risk-taking": {"name": "The Adventurer", "description": "You embrace uncertainty and bold ideas."},
    "Resilience": {"name": "The Survivor", "description": "You bounce back and keep creating."},
    "Collaboration": {"name": "The Collaborator", "description": "You build ideas with and through others."},
    "Divergent Thinking": {"name": "The Visionary", "description": "You see endless possibilities."},
    "Convergent Thinking": {"name": "The Strategist", "description": "You refine and focus ideas into reality."}
}

# Encouragement messages
messages = [
    "🚀 Keep going, you're doing great!",
    "✨ Your creativity is shining through!",
    "🌟 Nearly there — exciting insights ahead!"
]

# -------------------------
# Streamlit App
# -------------------------
st.set_page_config(page_title="Creative Identity Quiz", layout="wide")
st.title("🎨 Creative Identity Profile ✨")

# Initialise session state
if "all_questions" not in st.session_state:
    all_questions = []
    for trait, qs in {**creative_traits, **big5_traits}.items():
        for q in qs:
            all_questions.append((trait, q))
    random.shuffle(all_questions)
    st.session_state.all_questions = all_questions
    st.session_state.responses = {}

total_qs = len(st.session_state.all_questions)
answered = len(st.session_state.responses)

# Progress bar
st.progress(answered / total_qs)
st.write(f"Progress: {answered}/{total_qs} questions answered")

# Encouragement
if answered < total_qs:
    st.info(random.choice(messages))

# Ask next unanswered question
for trait, q in st.session_state.all_questions:
    if q not in st.session_state.responses:
        st.subheader(q)
        st.session_state.responses[q] = st.slider("Select your answer:", 1, 5, 3, key=q)
        st.button("Next Question")
        st.stop()

# -------------------------
# Results
# -------------------------
st.balloons()
st.success("🎉 Congratulations! You've completed the quiz 🎉")

# Calculate scores
creative_scores = {trait: 0 for trait in creative_traits}
big5_scores = {trait: 0 for trait in big5_traits}

for trait, q in st.session_state.all_questions:
    score = st.session_state.responses[q]
    if trait in creative_scores:
        creative_scores[trait] += score
    elif trait in big5_scores:
        big5_scores[trait] += score

# Average scores
for trait in creative_scores:
    creative_scores[trait] /= len(creative_traits[trait])
for trait in big5_scores:
    big5_scores[trait] /= len(big5_traits[trait])

# Main creative trait
main_trait = max(creative_scores, key=creative_scores.get)

# Archetype card
st.markdown(
    f"""
    <div style="background-color:#f9f9f9; padding:15px; border-radius:10px; 
    box-shadow: 2px 2px 8px rgba(0,0,0,0.1); margin-bottom:20px;">
    <h3 style="color:#333;">🎭 Main Archetype: {archetypes[main_trait]['name']}</h3>
    <p>{archetypes[main_trait]['description']}</p>
    </div>
    """, unsafe_allow_html=True
)

# Creative traits radar chart
st.subheader("🎨 Creative Traits Radar Chart")
labels = list(creative_scores.keys())
scores = list(creative_scores.values())
angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
scores += scores[:1]
angles += angles[:1]

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#17becf"]

ax.plot(angles, scores, linewidth=2, linestyle='solid', color=colors[0])
ax.fill(angles, scores, alpha=0.25, color=colors[0])
ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels)
ax.set_yticks(range(1, 6))
st.pyplot(fig)

# Big Five bar chart
st.subheader("📊 Big Five Traits")
fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(big5_scores.keys(), big5_scores.values(), color=colors)
ax.set_ylim(0, 5)
ax.set_ylabel("Average Score (1–5)")
st.pyplot(fig)

# Trait descriptions
st.subheader("🧾 Trait Insights")
for trait, score in {**creative_scores, **big5_scores}.items():
    st.markdown(
        f"**{trait} ({score:.2f}/5):** {trait_descriptions.get(trait, '')}"
    )

# Missed questions
missed = [q for (trait, q) in st.session_state.all_questions if q not in st.session_state.responses]
if missed:
    st.warning(f"You missed {len(missed)} questions. Consider reviewing for best results.")


