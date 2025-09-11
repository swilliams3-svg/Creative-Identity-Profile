import streamlit as st
import random
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
import io

# -------------------------------
# Utility: clean text for PDF
# -------------------------------
def clean_text(text):
    return text.encode("latin-1", "ignore").decode("latin-1")

# -------------------------------
# Trait definitions
# -------------------------------
traits = {
    "Openness": [
        "I enjoy exploring new ideas, even if they seem unusual.",
        "I often seek out new experiences.",
        "I like trying new creative methods.",
        "I embrace change and variety in life."
    ],
    "Curiosity": [
        "I frequently ask questions to deepen understanding.",
        "I enjoy researching topics that interest me.",
        "I like discovering how things work.",
        "I investigate ideas beyond the obvious."
    ],
    "Imagination": [
        "I often picture things in my mind vividly.",
        "I like inventing stories or scenarios.",
        "I can see possibilities beyond what exists.",
        "I use mental imagery to solve problems."
    ],
    "Persistence": [
        "I keep working on ideas, even if they seem difficult.",
        "I don’t give up easily when exploring something new.",
        "I return to problems until I solve them.",
        "I show determination when developing ideas."
    ],
    "Risk-Taking": [
        "I don’t mind making mistakes if it leads to new ideas.",
        "I take risks when trying creative approaches.",
        "I feel comfortable with uncertainty.",
        "I try new things even if they might fail."
    ]
}

trait_extras = {
    "Openness": {
        "Meaning": "Being receptive to new experiences and ideas.",
        "Growth": "Experiment with unfamiliar art forms, music, or writing.",
        "Activities": "🔹 Visit an art gallery and reflect on pieces you wouldn’t normally notice.\n🔹 Try a cuisine you’ve never eaten before."
    },
    "Curiosity": {
        "Meaning": "Asking questions and seeking knowledge.",
        "Growth": "Keep a daily log of questions that spark your interest.",
        "Activities": "🔹 Dedicate 10 minutes a day to researching something unrelated to your work.\n🔹 Play 'Why?' by asking 'why' five times in a row about something ordinary."
    },
    "Imagination": {
        "Meaning": "Visualizing possibilities and thinking beyond the obvious.",
        "Growth": "Practice daydreaming exercises and creative storytelling.",
        "Activities": "🔹 Rewrite the ending of a film or book.\n🔹 Imagine alternative uses for everyday objects."
    },
    "Persistence": {
        "Meaning": "Sticking with challenges until you find solutions.",
        "Growth": "Break big creative projects into small achievable tasks.",
        "Activities": "🔹 Commit to a 30-day micro-project (like a photo a day).\n🔹 Track your creative progress visually on a calendar."
    },
    "Risk-Taking": {
        "Meaning": "Courage to try new things despite uncertainty.",
        "Growth": "Reframe failure as learning in your creative journey.",
        "Activities": "🔹 Try improvisational theatre or storytelling.\n🔹 Share unfinished work with someone for feedback."
    }
}

# Score interpretations
def interpret_trait(trait, score):
    if score <= 8:
        return f"Low {trait}: You may prefer stability but might miss creative opportunities."
    elif 9 <= score <= 14:
        return f"Moderate {trait}: You sometimes tap into this trait but could grow further."
    else:
        return f"High {trait}: This is one of your creative strengths."

# Archetypes
archetypes = {
    "Visionary": ["Openness", "Imagination"],
    "Explorer": ["Curiosity", "Risk-Taking"],
    "Maker": ["Persistence", "Imagination"],
    "Challenger": ["Risk-Taking", "Openness"],
    "Scholar": ["Curiosity", "Persistence"]
}

archetype_extras = {
    "Visionary": {"Strengths": "Sees future possibilities and inspires others.",
                  "Blind Spots": "Ideas may be impractical without grounding.",
                  "Practices": "Balance dreams with actionable steps."},
    "Explorer": {"Strengths": "Loves adventure and experimentation.",
                 "Blind Spots": "May lose focus jumping between ideas.",
                 "Practices": "Set goals to channel curiosity productively."},
    "Maker": {"Strengths": "Turns visions into tangible outcomes.",
              "Blind Spots": "May overwork or get stuck on details.",
              "Practices": "Celebrate progress, not just completion."},
    "Challenger": {"Strengths": "Breaks norms, sparks innovation.",
                   "Blind Spots": "Can be disruptive without solutions.",
                   "Practices": "Direct energy toward constructive change."},
    "Scholar": {"Strengths": "Deep understanding and thoughtful creativity.",
                "Blind Spots": "Risk of analysis paralysis.",
                "Practices": "Balance study with creative action."}
}

# -------------------------------
# Radar Chart (color-coded)
# -------------------------------
def create_radar_chart(trait_scores):
    labels = list(trait_scores.keys())
    values = list(trait_scores.values())
    values += values[:1]
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    colors = ["green", "orange", "purple", "red", "blue"]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    ax.plot(angles, values, linewidth=2, linestyle='solid')
    ax.fill(angles, values, 'b', alpha=0.1)

    for i, label in enumerate(labels):
        ax.plot([angles[i], angles[i]], [0, values[i]], color=colors[i], linewidth=2)
        ax.scatter(angles[i], values[i], color=colors[i], s=80, label=label)

    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    plt.legend(loc="upper right", bbox_to_anchor=(1.2, 1.1))

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return buf

# -------------------------------
# PDF Report (multi-page allowed)
# -------------------------------
def create_pdf(profile_name, traits, chart_buf, secondary=None):
    pdf = FPDF(orientation="L", unit="mm", format="A4")

    # Page 1 - Banner + Chart
    pdf.add_page()
    pdf.set_fill_color(70, 130, 180)
    pdf.rect(0, 0, 297, 20, "F")
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 10, clean_text("⭐ Creative Identity Report ⭐"), ln=True, align="C")
    pdf.ln(15)
    pdf.set_text_color(0, 0, 0)

    if chart_buf:
        chart_file = "chart.png"
        with open(chart_file, "wb") as f:
            f.write(chart_buf.getbuffer())
        pdf.image(chart_file, x=60, y=40, w=170)

    # Page 2+ - Archetype + Traits
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, clean_text("Your Creative Archetype"), ln=True, align="C")
    pdf.set_font("Helvetica", size=11)
    pdf.ln(5)
    pdf.multi_cell(0, 6, clean_text(f"Main Profile: {profile_name}"))
    if secondary:
        pdf.multi_cell(0, 6, clean_text(f"Secondary Influence: {secondary}"))

    if profile_name in archetype_extras:
        extra = archetype_extras[profile_name]
        pdf.ln(5)
        pdf.multi_cell(0, 6, clean_text(f"Strengths: {extra['Strengths']}"))
        pdf.multi_cell(0, 6, clean_text(f"Blind Spots: {extra['Blind Spots']}"))
        pdf.multi_cell(0, 6, clean_text(f"Growth Practices: {extra['Practices']}"))

    pdf.ln(5)
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 8, clean_text("Trait Scores, Insights & Growth Ideas"), ln=True)

    for trait, score in traits.items():
        pdf.set_font("Helvetica", 'B', 11)
        pdf.multi_cell(0, 6, clean_text(f"{trait}: {score}/20"))
        pdf.set_font("Helvetica", size=10)
        pdf.multi_cell(0, 5, clean_text(interpret_trait(trait, score)))
        if trait in trait_extras:
            pdf.multi_cell(0, 5, clean_text(f"Meaning: {trait_extras[trait]['Meaning']}"))
            pdf.multi_cell(0, 5, clean_text(f"Growth: {trait_extras[trait]['Growth']}"))
            pdf.multi_cell(0, 5, clean_text(f"Suggested Activities:\n{trait_extras[trait]['Activities']}"))
        pdf.ln(4)

    pdf.ln(5)
    pdf.set_font("Helvetica", 'I', 10)
    pdf.multi_cell(0, 6, clean_text("🌱 Keep Creating! Every idea is a seed — what will you grow today?"), align="C")

    return pdf

# -------------------------------
# Streamlit App
# -------------------------------
st.set_page_config(page_title="Creative Identity Profile", layout="centered")
st.markdown("<h1 style='text-align:center; color: #4682B4;'>✨ Creative Identity Profile ✨</h1>", unsafe_allow_html=True)

# Shuffle questions
all_questions = [(trait, q) for trait, qs in traits.items() for q in qs]
random.shuffle(all_questions)

responses = {}
progress = 0
total_questions = len(all_questions)
messages = ["🚀 Let’s go!", "💡 You’re unlocking insights!", "🌟 Halfway there!", "🔥 Keep going, almost done!", "🎉 Last question!"]

for i, (trait, question) in enumerate(all_questions, 1):
    st.write(f"**Q{i}. {question}**")
    response = st.radio("Select your response", 
                        ["1 - Strongly Disagree", "2 - Disagree", "3 - Neutral", "4 - Agree", "5 - Strongly Agree"], 
                        horizontal=True, key=f"q{i}")
    responses.setdefault(trait, []).append(int(response[0]))
    progress = i / total_questions
    st.progress(progress, text=messages[min(i*len(messages)//total_questions, len(messages)-1)])

if st.button("Generate My Creative Profile"):
    trait_scores = {trait: sum(scores) for trait, scores in responses.items()}
    top_traits = sorted(trait_scores, key=trait_scores.get, reverse=True)[:2]

    profile = "Unique Creator"
    secondary = None
    for arch, arch_traits in archetypes.items():
        if set(top_traits) == set(arch_traits):
            profile = arch

    # find secondary if close
    second_best = sorted(trait_scores, key=trait_scores.get, reverse=True)[2]
    for arch, arch_traits in archetypes.items():
        if second_best in arch_traits and profile != arch:
            secondary = arch

    chart_buf = create_radar_chart(trait_scores)

    # Show chart + archetype info on webpage
    st.image(chart_buf, caption="Your Creative Profile", use_container_width=True)
    st.subheader(f"🎭 Your Creative Archetype: {profile}")
    if secondary:
        st.write(f"✨ Secondary Influence: {secondary}")

    if profile in archetype_extras:
        st.write(f"**Strengths:** {archetype_extras[profile]['Strengths']}")
        st.write(f"**Blind Spots:** {archetype_extras[profile]['Blind Spots']}")
        st.write(f"**Growth Practices:** {archetype_extras[profile]['Practices']}")

    # Show interpretations on webpage
    for trait, score in trait_scores.items():
        st.write(f"**{trait} ({score}/20):** {interpret_trait(trait, score)}")

    # Generate PDF
    pdf = create_pdf(profile, trait_scores, chart_buf, secondary)
    pdf_bytes = pdf.output(dest="S").encode("latin-1", "ignore")

    st.download_button(
        "📥 Download My Creative Report",
        data=pdf_bytes,
        file_name="Creative_Identity_Report.pdf",
        mime="application/pdf"
    )

