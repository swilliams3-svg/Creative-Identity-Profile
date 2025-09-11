import streamlit as st
import random
from fpdf import FPDF

st.set_page_config(page_title="Creative Identity Profile", layout="centered")

# ---------------------------
# Questions per trait (4 each)
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
# Functions
# ---------------------------
def assign_profile(traits):
    strongest = max(traits, key=traits.get)
    return archetypes.get(strongest, "Balanced Creator")

def create_pdf(profile_name, traits):
    pdf = FPDF()
    pdf.add_page()

    # Intro
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Creative Identity Report", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10,
        "Welcome to your Creative Identity Report!\n\n"
        "This assessment explores your creative personality across five traits:\n"
        "Imagination, Curiosity, Risk-taking, Persistence, and Social Sensitivity.\n\n"
        "Inside, you’ll discover your creative archetype, reflect on your strengths "
        "and growth opportunities, and get personalised exercises to expand your creative thinking."
    )
    pdf.add_page()

    # Archetype
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, "Your Creative Archetype", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"Profile: {profile_name}")

    if profile_name in archetype_extras:
        extra = archetype_extras[profile_name]
        pdf.multi_cell(0, 10, f"Strengths: {extra['Strengths']}")
        pdf.multi_cell(0, 10, f"Blind Spots: {extra['Blind Spots']}")
        pdf.multi_cell(0, 10, f"Growth Practices: {extra['Practices']}")

    # Traits
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, "Trait Scores & Growth Tips", ln=True)
    pdf.set_font("Arial", size=12)

    for trait, score in traits.items():
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.multi_cell(0, 10, f"{trait}: {score}/20")
        if trait in trait_extras:
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, f"Meaning: {trait_extras[trait]['Meaning']}")
            pdf.multi_cell(0, 10, f"Growth: {trait_extras[trait]['Growth']}")

    return pdf

# ---------------------------
# Streamlit UI
# ---------------------------
st.title("🌟 Creative Identity Profile 🌟")
st.write("Rate each statement from 1 (Not like me) to 5 (Very much like me).")

responses = {}
progress = 0
total_qs = len(all_questions)

for i, (trait, q) in enumerate(all_questions):
    st.write(f"**{q}**")
    responses[(trait, q)] = st.radio(
        "", [1,2,3,4,5], index=2, horizontal=True, key=f"{trait}_{i}"
    )
    progress = (i+1) / total_qs
    st.progress(progress)

if st.button("Submit"):
    # Calculate scores
    trait_scores = {t:0 for t in questions.keys()}
    for (trait, q), score in responses.items():
        trait_scores[trait] += score

    profile = assign_profile(trait_scores)

    # Show archetype
    st.subheader("Your Creative Archetype")
    st.write(profile)

    if profile in archetype_extras:
        st.write("**Strengths:**", archetype_extras[profile]["Strengths"])
        st.write("**Blind Spots:**", archetype_extras[profile]["Blind Spots"])
        st.write("**Practices:**", archetype_extras[profile]["Practices"])

    # PDF
    pdf = create_pdf(profile, trait_scores)
    pdf_bytes = pdf.output(dest="S").encode("latin-1")
    st.download_button(
        "📥 Download Your Full Report",
        data=pdf_bytes,
        file_name="creative_identity_report.pdf",
        mime="application/pdf"
    )


