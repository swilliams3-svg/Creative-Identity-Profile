import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
import io
import random
import tempfile

st.set_page_config(page_title="Creative Identity Profile", layout="centered")

# ---- TRAIT DEFINITIONS ----
traits = ["Openness", "Flexibility", "Imagination", "Curiosity", "Risk-taking", "Persistence"]

trait_colors = {
    "Openness": (0, 102, 204),
    "Flexibility": (0, 153, 76),
    "Imagination": (153, 51, 255),
    "Curiosity": (255, 153, 51),
    "Risk-taking": (220, 20, 60),
    "Persistence": (100, 100, 100),
}

questions = {
    "Openness": [
        "I enjoy exploring new ideas and perspectives.",
        "I am open to experiences that challenge my worldview.",
        "I actively seek out different forms of art, culture, or knowledge.",
        "I adapt my thinking when presented with new evidence."
    ],
    "Flexibility": [
        "I can easily adapt when plans change unexpectedly.",
        "I generate multiple solutions to a problem.",
        "I shift my perspective when faced with challenges.",
        "I feel comfortable working outside my comfort zone."
    ],
    "Imagination": [
        "I often visualize ideas vividly in my mind.",
        "I enjoy creating stories, images, or scenarios in my head.",
        "I use mental imagery to solve problems creatively.",
        "I see possibilities that others may overlook."
    ],
    "Curiosity": [
        "I ask questions to deepen my understanding.",
        "I seek out new knowledge beyond what is required.",
        "I am fascinated by how things work.",
        "I enjoy exploring unfamiliar subjects or areas."
    ],
    "Risk-taking": [
        "I am willing to try new things, even if I might fail.",
        "I embrace uncertainty in creative projects.",
        "I see failure as a learning opportunity.",
        "I enjoy experimenting with untested ideas."
    ],
    "Persistence": [
        "I keep working on projects even when they are difficult.",
        "I see challenges as opportunities to grow.",
        "I do not give up easily when facing setbacks.",
        "I am determined to bring my ideas to life."
    ]
}

# ---- INTERPRETATIONS ----
interpretations = {
    "Openness": {
        "low": "You may prefer stability, but risk missing creative opportunities.",
        "medium": "You balance stability with curiosity. Consider widening perspectives.",
        "high": "You thrive on novelty and diverse ideas, fueling creative growth."
    },
    "Flexibility": {
        "low": "You may rely on fixed routines, which can limit adaptability.",
        "medium": "You adapt sometimes, but could explore alternative solutions more often.",
        "high": "You quickly shift and adapt, a key strength for creativity."
    },
    "Imagination": {
        "low": "You may focus on practical details but miss visionary possibilities.",
        "medium": "You use imagination occasionally, but there’s room for dreaming bigger.",
        "high": "You vividly imagine and create, fueling originality and innovation."
    },
    "Curiosity": {
        "low": "You may avoid exploring, which can limit inspiration.",
        "medium": "You sometimes question and explore. Push further into discovery.",
        "high": "You constantly question and explore, sparking new ideas and insights."
    },
    "Risk-taking": {
        "low": "You prefer safety, but may miss bold creative leaps.",
        "medium": "You sometimes take risks, but could embrace uncertainty more.",
        "high": "You embrace challenges and thrive on bold experimentation."
    },
    "Persistence": {
        "low": "You may abandon ideas too quickly, limiting achievement.",
        "medium": "You show effort, but consistency will boost success.",
        "high": "You persevere through setbacks, ensuring creative ideas come alive."
    }
}

# ---- GROWTH ACTIVITIES ----
activities = {
    "Openness": "Try exposing yourself to a completely new culture, genre, or field weekly.",
    "Flexibility": "Practice 'What if?' scenarios to reframe challenges in different ways.",
    "Imagination": "Engage in free drawing or story-creation sessions without constraints.",
    "Curiosity": "Commit to asking 'why' five times when faced with a problem.",
    "Risk-taking": "Try one new activity this week that pushes you outside your comfort zone.",
    "Persistence": "Set a small creative goal and commit to finishing it, no matter what."
}

# ---- SAFE TEXT WRAPPER ----
def safe_text(text):
    return text.encode("latin-1", "ignore").decode("latin-1")

# --- FUNCTIONS ---
def calculate_scores(responses):
    scores = {}
    for trait in traits:
        scores[trait] = np.mean(responses[trait])
    return scores

def generate_chart(scores):
    labels = list(scores.keys())
    values = list(scores.values())
    num_vars = len(labels)

    values += values[:1]
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    for trait, color in trait_colors.items():
        idx = labels.index(trait)
        ax.plot(
            [angles[idx], angles[idx]],
            [0, scores[trait]],
            color=np.array(color) / 255,
            linewidth=2,
            label=trait
        )
        ax.fill_between(
            [angles[idx], angles[idx]],
            [0, scores[trait]],
            [0, 0],
            color=np.array(color) / 255,
            alpha=0.25
        )

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_ylim(0, 5)

    fig.legend(
        labels,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.1),
        ncol=3,
        fontsize=8,
        frameon=False
    )

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)
    return buf

def determine_archetype(scores):
    sorted_traits = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    main_trait, main_score = sorted_traits[0]
    sub_trait, sub_score = sorted_traits[1]

    archetypes = {
        "Openness": "The Explorer",
        "Flexibility": "The Adapter",
        "Imagination": "The Dreamer",
        "Curiosity": "The Seeker",
        "Risk-taking": "The Adventurer",
        "Persistence": "The Maker"
    }

    return {
        "main": {"trait": main_trait, "score": main_score, "name": archetypes[main_trait]},
        "sub": {"trait": sub_trait, "score": sub_score, "name": archetypes[sub_trait]}
    }

def create_pdf(scores, archetype, chart_buf):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Page 1
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(30, 30, 120)
    pdf.cell(0, 10, safe_text("Your Creative Identity Profile"), ln=True, align="C")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
        tmpfile.write(chart_buf.getbuffer())
        tmp_path = tmpfile.name
    pdf.image(tmp_path, x=30, y=40, w=150)
    pdf.ln(160)
    pdf.set_font("Helvetica", "I", 12)
    pdf.cell(0, 10, safe_text("Radar chart of your creative traits"), ln=True, align="C")

    # Page 2+
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 10, safe_text("Your Creative Archetypes"), ln=True)

    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 8, safe_text(
        f"Main Archetype: {archetype['main']['name']} ({archetype['main']['trait']})\n"
        f"Sub-Archetype: {archetype['sub']['name']} ({archetype['sub']['trait']})\n"
    ))
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 10, safe_text("Trait Insights & Growth Activities"), ln=True)

    for trait, score in scores.items():
        pdf.ln(5)
        r, g, b = trait_colors[trait]
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(r, g, b)
        pdf.cell(0, 8, safe_text(f"{trait}: {score:.1f}/5"), ln=True)

        if score <= 2:
            interpretation = interpretations[trait]["low"]
        elif score == 3:
            interpretation = interpretations[trait]["medium"]
        else:
            interpretation = interpretations[trait]["high"]

        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(0, 6, safe_text(f"Insight: {interpretation}"))

        pdf.set_font("Helvetica", "I", 10)
        pdf.set_text_color(80, 80, 80)
        pdf.multi_cell(0, 6, safe_text(f"Try this: {activities[trait]}"))
        pdf.set_text_color(0, 0, 0)

    return pdf

# ---- STREAMLIT APP ----
st.title("✨ Creative Identity Profile ✨")
st.write("Discover your creative strengths across six key traits.")

responses = {trait: [] for trait in traits}

with st.form("creativity_test"):
    for trait in traits:
        st.subheader(trait)
        q_list = questions[trait][:]
        random.shuffle(q_list)
        for q in q_list:
            responses[trait].append(st.radio(
                q,
                [1, 2, 3, 4, 5],
                horizontal=True,
                index=2,
                key=f"{trait}_{q}"
            ))
    submitted = st.form_submit_button("Generate My Profile")

if submitted:
    scores = calculate_scores(responses)
    chart_buf = generate_chart(scores)
    archetype = determine_archetype(scores)

    st.subheader("📊 Your Results")
    st.image(chart_buf, caption="Radar Chart of Creative Traits", use_container_width=True)

    st.write(f"**Main Archetype:** {archetype['main']['name']} ({archetype['main']['trait']})")
    st.write(f"**Sub-Archetype:** {archetype['sub']['name']} ({archetype['sub']['trait']})")

    st.subheader("🔍 Trait Insights")
    for trait, score in scores.items():
        if score <= 2:
            interpretation = interpretations[trait]["low"]
        elif score == 3:
            interpretation = interpretations[trait]["medium"]
        else:
            interpretation = interpretations[trait]["high"]

        st.markdown(f"**{trait} ({score:.1f}/5):** {interpretation}")
        st.caption(f"💡 Try this: {activities[trait]}")

    # PDF download
    pdf = create_pdf(scores, archetype, chart_buf)
    pdf_bytes = pdf.output(dest="S").encode("latin-1", "ignore")
    st.download_button(
        label="📥 Download My Creative Identity Report (PDF)",
        data=pdf_bytes,
        file_name="creative_identity_profile.pdf",
        mime="application/pdf"
    )

