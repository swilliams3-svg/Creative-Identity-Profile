import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
import io
import random

st.set_page_config(page_title="Creative Identity Profile", layout="centered")

# ---------- TRAIT DEFINITIONS ----------
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

# Archetype definitions
archetypes = {
    "Openness": {
        "name": "The Explorer",
        "description": "You thrive on curiosity and imagination. Explorers see possibilities everywhere, though sometimes risk being unfocused."
    },
    "Risk-taking": {
        "name": "The Adventurer",
        "description": "You embrace uncertainty and boldly try new ideas. Adventurers push boundaries but must watch out for unnecessary risks."
    },
    "Resilience": {
        "name": "The Perseverer",
        "description": "You persist through challenges and learn from failure. Perseverers build strength from setbacks, though may struggle to pause and reflect."
    },
    "Collaboration": {
        "name": "The Connector",
        "description": "You spark ideas in groups and value diverse perspectives. Connectors thrive in teams but may sometimes overlook their own vision."
    },
    "Divergent Thinking": {
        "name": "The Visionary",
        "description": "You generate many original ideas and love seeing unusual connections. Visionaries excel at imagination but can find focus difficult."
    },
    "Convergent Thinking": {
        "name": "The Strategist",
        "description": "You refine and structure ideas into action. Strategists provide clarity and direction but may miss opportunities by being too selective."
    }
}

# ---------- FUNCTIONS ----------
def radar_chart(scores):
    labels = list(scores.keys())
    values = list(scores.values())
    num_vars = len(labels)

    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    colors = {
        "Openness": "tab:blue",
        "Risk-taking": "tab:red",
        "Resilience": "tab:green",
        "Collaboration": "tab:purple",
        "Divergent Thinking": "tab:orange",
        "Convergent Thinking": "tab:brown"
    }

    for i, label in enumerate(labels):
        ax.plot(angles[i:i+2], values[i:i+2], color=colors[label], linewidth=2)
        ax.fill(angles[i:i+2], values[i:i+2], color=colors[label], alpha=0.25)

    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_ylim(0, 5)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    ax.legend(labels, loc="lower center", bbox_to_anchor=(0.5, -0.25),
              ncol=3, frameon=False)

    plt.tight_layout(rect=[0, 0.05, 1, 1])

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)
    return buf

def create_pdf(scores, archetype, chart_buf):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    chart_path = "chart.png"
    with open(chart_path, "wb") as f:
        f.write(chart_buf.getbuffer())

    # Page 1: Chart
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 10, "Creative Identity Profile", ln=True, align="C")
    pdf.ln(10)
    pdf.image(chart_path, x=30, y=40, w=150)

    # Page 2: Archetype
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Your Creative Archetype", ln=True)
    pdf.ln(5)
    pdf.set_font("Helvetica", "", 12)
    pdf.multi_cell(0, 10,
                   f"Main Archetype: {archetypes[archetype]['name']}\n\n"
                   f"{archetypes[archetype]['description']}")
    sorted_traits = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    if len(sorted_traits) > 1:
        sub_trait = sorted_traits[1][0]
        pdf.ln(5)
        pdf.multi_cell(0, 10,

