import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import io
import random
from fpdf import FPDF
import os

st.set_page_config(page_title="Creative Identity Profile", layout="centered")

# --------------------------
# Traits (original 6) with questions
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

# Colours for each trait
trait_colors = {
    "Openness": "tab:blue",
    "Risk-taking": "tab:red",
    "Resilience": "tab:green",
    "Collaboration": "tab:orange",
    "Divergent Thinking": "tab:purple",
    "Convergent Thinking": "tab:brown"
}

# Archetype metadata + suggestions for growth
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
# Utilities
# --------------------------
def clean_text(text: str) -> str:
    if text is None:
        return ""
    return str(text).encode("latin-1", "replace").decode("latin-1")

def get_level(score: float) -> str:
    if score >= 4:
        return "High"
    elif score >= 2.5:
        return "Medium"
    else:
        return "Low"

# --------------------------
# Radar chart (multi-colour)
# --------------------------
def radar_chart(scores: dict) -> io.BytesIO:
    labels = list(scores.keys())
    values = list(scores.values())
    num_vars = len(labels)

    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))

    # draw each trait segment in its colour
    for i, trait in enumerate(labels):
        start_angle = angles[i]
        end_angle = angles[i+1]
        ax.plot([start_angle, end_angle],
                [values[i], values[i+1]],
                color=trait_colors[trait], linewidth=3)
        ax.fill([start_angle, end_angle, end_angle, start_angle],
                [0, 0, values[i+1], values[i]],
                alpha=0.2, color=trait_colors[trait])

    ax.set_ylim(0,5)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_yticks([1,2,3,4,5])
    ax.set_yticklabels(["1","2","3","4","5"])

    plt.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)
    return buf

# --------------------------
# Bar chart
# --------------------------
def bar_chart(scores: dict) -> io.BytesIO:
    fig, ax = plt.subplots(figsize=(6,4))
    traits = list(scores.keys())
    values = list(scores.values())
    ax.bar(traits, values, color=[trait_colors[t] for t in traits])
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
# PDF creation
# --------------------------
def create_pdf(scores: dict, main_trait: str, chart_buf: io.BytesIO, bar_buf: io.BytesIO) -> bytes:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    chart_path = "chart_temp.png"
    bar_path = "bar_temp.png"
    with open(chart_path, "wb") as f:
        f.write(chart_buf.getbuffer())
    with open(bar_path, "wb") as f:
        f.write(bar_buf.getbuffer())

    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, clean_text("Creative Identity Profile"), ln=True, align="C")
    pdf.ln(6)
    try:
        pdf.image(chart_path, x=30, y=30, w=150)
        pdf.ln(120)
        pdf.image(bar_path, x=30, w=150)
    except Exception:
        pass

    sorted_traits = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    main = sorted_traits[0][0]
    sub = sorted_traits[1][0]
    weakest = sorted_traits[-1][0]

    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, clean_text("Your Creative Archetypes"), ln=True)
    pdf.ln(4)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 8, clean_text(f"Main Archetype: {archetypes[main]['name']}"))
    pdf.multi_cell(0, 8, clean_text(archetypes[main]['description']))
    pdf.ln(4)
    pdf.multi_cell(0, 8, clean_text(f"Sub-Archetype: {archetypes[sub]['name']}"))
    pdf.multi_cell(0, 8, clean_text(archetypes[sub]['description']))
    pdf.ln(4)
    pdf.multi_cell(0, 8, clean_text(f"To grow your weaker area ({weakest}): {archetypes[weakest]['improvement']}"))

    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, clean_text("Trait Insights"), ln=True)
    pdf.ln(4)
    pdf.set_font("Arial", "", 12)
    for trait, score in scores.items():
        level = get_level(score)
        pdf.multi_cell(0, 8, clean_text(f"{trait} ({level}): {score:.2f}/5"))

    for path in [chart_path, bar_path]:
        try:
            os.remove(path)
        except OSError:
            pass

    return pdf.output(dest="S").encode("latin-1", "replace")

# --------------------------
# Streamlit UI
# --------------------------
st.title("Creative Identity Profile")
st.write("Please respond to each statement on a 1–5 scale: 1 = Strongly Disagree … 5 = Strongly Agree.")

if "all_questions" not in st.session_state:
    all_questions = []
    for trait, qs in traits.items():
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
for i, (trait, question) in enumerate(all_questions, 1):
    key = f"{trait}_{i}"
    index_val = (responses[key] - 1) if responses[key] else None
    responses[key] = st.radio(f"Q{i}/{total_qs}: {question}", [1,2,3,4,5], horizontal=True,
                              index=index_val, key=key)
    if responses[key] is not None:
        answered += 1

st.progress(answered / total_qs)

if answered == total_qs:
    st.success("Questionnaire complete — here are your results:")

    scores = {trait: 0.0 for trait in traits}
    counts = {trait: 0 for trait in traits}
    for key, val in responses.items():
        if val is not None:
            trait = key.split("_")[0]
            scores[trait] += val
            counts[trait] += 1
    for trait in scores:
        scores[trait] = (scores[trait] / counts[trait]) if counts[trait] else 0.0

    chart_buf = radar_chart(scores)
    bar_buf = bar_chart(scores)
    st.image(chart_buf.getvalue(), caption="Your Creative Trait Profile (Radar)", use_container_width=True)
    st.image(bar_buf.getvalue(), caption="Your Creative Trait Scores (Bar)", use_container_width=True)

    sorted_traits = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    main_trait = sorted_traits[0][0]
    sub_trait = sorted_traits[1][0]
    weakest_trait = sorted_traits[-1][0]

    st.subheader("Your Creative Archetype")
    st.write(f"Main Archetype: **{archetypes[main_trait]['name']}**")
    st.write(archetypes[main_trait]['description'])
    st.write(f"Sub-Archetype: **{archetypes[sub_trait]['name']}**")
    st.write(archetypes[sub_trait]['description'])

    st.subheader("Ways to grow")
    st.write(f"Weaker area: **{weakest_trait}** — {archetypes[weakest_trait]['improvement']}")

    st.subheader("Trait Insights")
    for trait, score in scores.items():
        level = get_level(score)
        st.write(f"**{trait} ({level})** — {score:.2f}/5")

    pdf_bytes = create_pdf(scores, main_trait, chart_buf, bar_buf)
    st.download_button(
        "Download your personalised PDF report",
        data=pdf_bytes,
        file_name="Creative_Identity_Report.pdf",
        mime="application/pdf"
    )

else:
    missed = [q for (trait, q), (k, v) in zip(all_questions, responses.items()) if v is None]
    if missed:
        st.warning(f"You still have {len(missed)} unanswered questions.")
