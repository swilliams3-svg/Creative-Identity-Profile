import streamlit as st
import random
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
from io import BytesIO

st.set_page_config(page_title="Creative Identity Profile", layout="centered")

# ---------------------------
# Style: Hero Banner
# ---------------------------
st.markdown(
    """
    <div style="background-color:#4B9CD3;padding:20px;border-radius:10px;margin-bottom:20px;">
        <h2 style="color:white;text-align:center;">✨ Discover Your Creative Identity ✨</h2>
        <p style="color:white;text-align:center;">
        Explore your imagination, curiosity, and collaboration style.<br>
        Complete the profile below and unlock a personalised PDF report!
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# Questions per trait
# ---------------------------
questions = {
    "Imagination": [
        "I often picture new worlds or scenarios in my mind.",
        "I like to dream big without worrying if it’s realistic.",
        "I can easily imagine different possibilities for the future.",
        "I enjoy activities like daydreaming, sketching, or storytelling."
    ],
    "Curiosity": [
        "I ask a lot of questions about how things work.",
        "I enjoy learning about unfamiliar topics just for fun.",
        "I get excited when I discover something new.",
        "I often explore subjects outside my expertise."
    ],
    "Risk-taking": [
        "I’m willing to try ideas even if they might fail.",
        "I get energy from experimenting with the unknown.",
        "I enjoy stepping outside my comfort zone.",
        "I believe mistakes are part of the creative process."
    ],
    "Persistence": [
        "I keep going with projects even when they get difficult.",
        "I don’t give up easily when faced with challenges.",
        "I’m willing to rework an idea until it feels right.",
        "I see setbacks as opportunities to improve."
    ],
    "Social Sensitivity": [
        "I can sense how others are feeling during group work.",
        "I like to build on ideas shared by others.",
        "I listen carefully to different perspectives.",
        "I feel energized when collaborating with people."
    ]
}

# Shuffle questions
all_questions = [(trait, q) for trait, qs in questions.items() for q in qs]
random.shuffle(all_questions)

# ---------------------------
# Archetypes
# ---------------------------
archetypes = {
    "Imagination": "Visionary Dreamer",
    "Curiosity": "Inquisitive Explorer",
    "Risk-taking": "Bold Experimenter",
    "Persistence": "Resilient Maker",
    "Social Sensitivity": "Collaborative Connector"
}

archetype_extras = {
    "Visionary Dreamer": {
        "Strengths": "Sees endless possibilities, excels at future-oriented thinking.",
        "Blind Spots": "May lose grounding in reality or struggle to execute.",
        "Practices": "Prototype your visions to make them tangible."
    },
    "Inquisitive Explorer": {
        "Strengths": "Endlessly curious, loves questioning and discovering.",
        "Blind Spots": "Can become scattered or unfocused.",
        "Practices": "Set learning goals to balance depth with breadth."
    },
    "Bold Experimenter": {
        "Strengths": "Thrives on uncertainty, embraces trial and error.",
        "Blind Spots": "May overlook risks or jump too quickly.",
        "Practices": "Use structured experiments to channel risk-taking."
    },
    "Resilient Maker": {
        "Strengths": "Determined, keeps pushing through challenges.",
        "Blind Spots": "Can burn out or get stuck in repetition.",
        "Practices": "Balance persistence with reflection and rest."
    },
    "Collaborative Connector": {
        "Strengths": "Empathetic, builds creative energy in groups.",
        "Blind Spots": "Might undervalue personal contributions.",
        "Practices": "Balance supporting others with voicing your own ideas."
    }
}

trait_extras = {
    "Imagination": {
        "Meaning": "Your strength lies in envisioning possibilities.",
        "Growth": "Practice grounding your visions into real experiments."
    },
    "Curiosity": {
        "Meaning": "Your strength lies in exploration and discovery.",
        "Growth": "Focus your curiosity by setting themes for exploration."
    },
    "Risk-taking": {
        "Meaning": "You embrace uncertainty and push creative boundaries.",
        "Growth": "Balance boldness with reflection on outcomes."
    },
    "Persistence": {
        "Meaning": "You have strong resilience and follow-through.",
        "Growth": "Ensure balance by taking breaks and reviewing progress."
    },
    "Social Sensitivity": {
        "Meaning": "You thrive on collaboration and group creativity.",
        "Growth": "Balance group input with expressing your unique ideas."
    }
}

# ---------------------------
# Helpers
# ---------------------------
def clean_text(text: str) -> str:
    return text.encode("latin-1", "ignore").decode("latin-1")

def assign_profile(traits):
    strongest = max(traits, key=traits.get)
    return archetypes.get(strongest, "Balanced Creator")

def create_radar_chart(traits):
    labels = list(traits.keys())
    scores = list(traits.values())

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    scores += scores[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, scores, color="blue", linewidth=2)
    ax.fill(angles, scores, color="skyblue", alpha=0.4)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)
    return buf

def create_pdf(profile_name, traits, chart_buf):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(200, 10, clean_text("Creative Identity Report"), ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Helvetica", size=12)
    pdf.multi_cell(0, 10, clean_text(
        "Welcome to your Creative Identity Report!\n\n"
        "This assessment explores your creative personality across five traits:\n"
        "Imagination, Curiosity, Risk-taking, Persistence, and Social Sensitivity.\n\n"
        "Inside, you’ll discover your creative archetype, reflect on your strengths "
        "and growth opportunities, and get personalised exercises to expand your creative thinking."
    ))
    pdf.add_page()

    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(200, 10, clean_text("Your Creative Archetype"), ln=True)
    pdf.set_font("Helvetica", size=12)
    pdf.multi_cell(0, 10, clean_text(f"Profile: {profile_name}"))

    if profile_name in archetype_extras:
        extra = archetype_extras[profile_name]
        pdf.multi_cell(0, 10, clean_text(f"Strengths: {extra['Strengths']}"))
        pdf.multi_cell(0, 10, clean_text(f"Blind Spots: {extra['Blind Spots']}"))
        pdf.multi_cell(0, 10, clean_text(f"Growth Practices: {extra['Practices']}"))

    if chart_buf:
        chart_file = "chart.png"
        with open(chart_file, "wb") as f:
            f.write(chart_buf.getbuffer())
        pdf.image(chart_file, x=40, w=120)

    pdf.ln(10)
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(200, 10, clean_text("Trait Scores & Growth Tips"), ln=True)
    pdf.set_font("Helvetica", size=12)

    for trait, score in traits.items():
        pdf.ln(5)
        pdf.set_font("Helvetica", 'B', 12)
        pdf.multi_cell(0, 10, clean_text(f"{trait}: {score}/20"))
        if trait in trait_extras:
            pdf.set_font("Helvetica", size=12)
            pdf.multi_cell(0, 10, clean_text(f"Meaning: {trait_extras[trait]['Meaning']}"))
            pdf.multi_cell(0, 10, clean_text(f"Growth: {trait_extras[trait]['Growth']}"))

    return pdf

# ---------------------------
# UI: Questions
# ---------------------------
st.title("Creative Identity Profile")
st.write("Rate each statement from 1 (Not like me) to 5 (Very much like me).")

responses = {}
progress = 0
total_qs = len(all_questions)

for i, (trait, q) in enumerate(all_questions):
    st.write(f"**Question {i+1} of {total_qs}**")
    responses[(trait, q)] = st.radio(
        f"{q}", [1, 2, 3, 4, 5], index=2, horizontal=True, key=f"{trait}_{i}"
    )
    progress = (i+1) / total_qs
    st.progress(progress)

# ---------------------------
# Results
# ---------------------------
if st.button("Submit"):
    trait_scores = {t: 0 for t in questions.keys()}
    for (trait, q), score in responses.items():
        trait_scores[trait] += score

    profile = assign_profile(trait_scores)

    st.markdown(
        f"""
        <div style="border:2px solid #4B9CD3; border-radius:10px; padding:15px; margin:20px 0;">
            <h3 style="color:#4B9CD3;">🌟 Your Creative Archetype: {profile}</h3>
            <p><b>Strengths:</b> {archetype_extras[profile]["Strengths"]}</p>
            <p><b>Blind Spots:</b> {archetype_extras[profile]["Blind Spots"]}</p>
            <p><b>Practices:</b> {archetype_extras[profile]["Practices"]}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    chart_buf = create_radar_chart(trait_scores)
    st.image(chart_buf, caption="Your Creative Profile")

    pdf = create_pdf(profile, trait_scores, chart_buf)
    pdf_bytes = pdf.output(dest="S").encode("latin-1", "ignore")
    st.download_button(
        label="🌟 Download Your Creative Identity Report (PDF)",
        data=pdf_bytes,
        file_name="creative_identity_report.pdf",
        mime="application/pdf"
    )

# ---------------------------
# Closing Inspiration
# ---------------------------
st.markdown("---")
st.markdown(
    """
    <div style="text-align:center; padding:20px;">
        <h3>🌱 Keep Creating!</h3>
        <p>Your creativity is a muscle – the more you use it, the stronger it gets.<br>
        Explore, take risks, and share your ideas with the world.</p>
        <p style="font-style:italic;">Every idea is a seed. What will you grow today?</p>
    </div>
    """,
    unsafe_allow_html=True
)



