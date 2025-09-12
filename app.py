import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
from io import BytesIO

# --------------------------
# Questionnaire Setup
# --------------------------
traits = {
    "Curiosity": [
        "I enjoy exploring new ideas and concepts.",
        "I often ask questions to deepen my understanding.",
        "I like experimenting with new approaches.",
        "I actively seek out new experiences.",
        "I feel energized when learning something unfamiliar."
    ],
    "Imagination": [
        "I often think in images and mental pictures.",
        "I enjoy daydreaming and exploring possibilities.",
        "I can easily picture alternatives to reality.",
        "I often make connections between unrelated things.",
        "I enjoy creative storytelling or fantasizing."
    ],
    "Resilience": [
        "I bounce back quickly after setbacks.",
        "I remain persistent even when tasks are difficult.",
        "I use challenges as opportunities to grow.",
        "I handle criticism constructively.",
        "I adapt easily when circumstances change."
    ],
    "Collaboration": [
        "I enjoy brainstorming with others.",
        "I build on other people’s ideas.",
        "I value diverse perspectives.",
        "I work well in creative teams.",
        "I help others feel included in creative discussions."
    ],
    "Discipline": [
        "I dedicate regular time to practicing my skills.",
        "I follow through on creative projects.",
        "I break big tasks into manageable steps.",
        "I balance inspiration with structured effort.",
        "I set goals and work steadily towards them."
    ],
    "Risk-Taking": [
        "I feel comfortable trying untested ideas.",
        "I see failure as part of the creative process.",
        "I am willing to stand out with unconventional ideas.",
        "I take initiative without knowing the outcome.",
        "I embrace uncertainty when creating something new."
    ]
}

# --------------------------
# Archetype Descriptions & Suggestions
# --------------------------
archetypes = {
    "Curiosity": {
        "description": "You are a **Seeker** – drawn to explore, question, and discover.",
        "suggestions": [
            "Keep a curiosity journal of questions you want to explore.",
            "Attend talks, workshops, or events outside your field.",
            "Pair your curiosity with discipline to turn ideas into action."
        ]
    },
    "Imagination": {
        "description": "You are a **Dreamer** – full of visions, ideas, and creative possibilities.",
        "suggestions": [
            "Translate daydreams into quick sketches, stories, or prototypes.",
            "Use creative constraints to focus your imagination.",
            "Collaborate with grounded thinkers to help shape your visions."
        ]
    },
    "Resilience": {
        "description": "You are a **Warrior** – able to adapt, persist, and grow from challenges.",
        "suggestions": [
            "Reframe failures as learning opportunities.",
            "Practice mindfulness to stay calm under pressure.",
            "Celebrate small wins to fuel long-term motivation."
        ]
    },
    "Collaboration": {
        "description": "You are a **Connector** – thriving in shared creativity and teamwork.",
        "suggestions": [
            "Facilitate brainstorming sessions with diverse groups.",
            "Listen actively and amplify quieter voices.",
            "Balance collaboration with solo time to refine your ideas."
        ]
    },
    "Discipline": {
        "description": "You are a **Builder** – structured, focused, and persistent in your craft.",
        "suggestions": [
            "Set aside daily or weekly practice time.",
            "Break ambitious projects into small achievable steps.",
            "Experiment with flexibility to spark spontaneity."
        ]
    },
    "Risk-Taking": {
        "description": "You are a **Trailblazer** – bold, adventurous, and unafraid of uncertainty.",
        "suggestions": [
            "Experiment with small calculated risks regularly.",
            "Share unfinished ideas for feedback early on.",
            "Pair bold moves with strategies for managing setbacks."
        ]
    }
}

# --------------------------
# Helper Functions
# --------------------------
def calculate_scores(responses):
    scores = {trait: np.mean(values) for trait, values in responses.items()}
    main_trait = max(scores, key=scores.get)
    return scores, main_trait

def plot_radar_chart(scores):
    labels = list(scores.keys())
    values = list(scores.values())
    num_vars = len(labels)

    values += values[:1]
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, values, color="blue", linewidth=2)
    ax.fill(angles, values, color="blue", alpha=0.25)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(["1","2","3","4","5"])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    plt.title("Creative Trait Profile (Radar Chart)")
    return fig

def plot_bar_chart(scores):
    labels = list(scores.keys())
    values = list(scores.values())

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(labels, values, color="skyblue")
    ax.set_ylim(0, 5)
    ax.set_ylabel("Average Score")
    plt.title("Creative Trait Profile (Bar Chart)")
    plt.xticks(rotation=30, ha="right")
    return fig

def create_pdf(scores, main_trait, chart_buf):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Your Creative Identity Profile", ln=True, align="C")

    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.multi_cell(0, 10, f"Your strongest creative trait is: {main_trait}")
    pdf.multi_cell(0, 10, archetypes[main_trait]["description"])

    pdf.ln(5)
    for trait, score in scores.items():
        pdf.multi_cell(0, 10, f"{trait}: {score:.2f}/5")

    # Suggestions
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.multi_cell(0, 10, "Suggestions to strengthen your creative growth:")
    pdf.set_font("Arial", size=12)
    for s in archetypes[main_trait]["suggestions"]:
        pdf.multi_cell(0, 10, f"- {s}")

    # Save chart image
    chart_buf.seek(0)
    with open("chart.png", "wb") as f:
        f.write(chart_buf.read())
    pdf.image("chart.png", x=30, w=150)

    return pdf.output(dest="S").encode("latin-1")

# --------------------------
# Streamlit UI
# --------------------------
st.title("🧠 Creative Identity Profile")

st.write("Answer the questions below to discover your creative strengths.")

responses = {}
for trait, questions in traits.items():
    st.subheader(trait)
    responses[trait] = []
    for q in questions:
        responses[trait].append(st.radio(q, [1, 2, 3, 4, 5], horizontal=True))

if st.button("Show Results"):
    scores, main_trait = calculate_scores(responses)

    st.subheader("Your Creative Archetype")
    st.markdown(f"**{main_trait}** – {archetypes[main_trait]['description']}")

    st.subheader("How to strengthen your creativity:")
    for s in archetypes[main_trait]["suggestions"]:
        st.markdown(f"- {s}")

    chart_type = st.radio("Choose chart type:", ["Radar Chart", "Bar Chart"])

    if chart_type == "Radar Chart":
        fig = plot_radar_chart(scores)
    else:
        fig = plot_bar_chart(scores)

    buf = BytesIO()
    fig.savefig(buf, format="png")
    st.image(buf, caption="Your Creative Trait Profile", use_container_width=True)

    # PDF (locked to radar chart)
    radar_fig = plot_radar_chart(scores)
    chart_buf = BytesIO()
    radar_fig.savefig(chart_buf, format="png")
    pdf_bytes = create_pdf(scores, main_trait, chart_buf)

    st.download_button(
        "📥 Download Your Profile (PDF)",
        data=pdf_bytes,
        file_name="creative_identity_profile.pdf",
        mime="application/pdf"
    )
