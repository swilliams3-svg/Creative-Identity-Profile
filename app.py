import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF

# ----------------------------
# 1. ARCHETYPE FUNCTION
# ----------------------------
def assign_profile(traits):
    # sort traits from highest to lowest
    sorted_traits = sorted(traits.items(), key=lambda x: x[1], reverse=True)
    top_trait, top_score = sorted_traits[0]
    second_trait, second_score = sorted_traits[1]

    # Two-trait archetypes
    if top_trait == "Imagination" and second_trait == "Curiosity":
        return ("Visionary Dreamer",
                "You see possibilities others don’t. You love exploring 'what ifs' and imagining bold futures.",
                "Ground your visions by sketching or prototyping them.",
                top_trait, second_trait)
    elif top_trait == "Curiosity" and second_trait == "Persistence":
        return ("Analytical Builder",
                "You dig deep, ask hard questions, and keep working until solutions appear.",
                "Balance analysis with playful exploration.",
                top_trait, second_trait)
    elif top_trait == "Risk-taking" and second_trait == "Imagination":
        return ("Bold Experimenter",
                "You embrace uncertainty and jump into new ideas with courage.",
                "Structure your experiments to learn quickly from failure.",
                top_trait, second_trait)
    elif top_trait == "Social Sensitivity" and second_trait == "Persistence":
        return ("Collaborative Connector",
                "You thrive in groups, amplifying and shaping ideas with empathy.",
                "Make space to share your own voice alongside supporting others.",
                top_trait, second_trait)
    elif top_trait == "Curiosity" and second_trait == "Risk-taking":
        return ("Strategic Innovator",
                "You explore new fields and act decisively on discoveries.",
                "Balance speed with deeper reflection before moving on.",
                top_trait, second_trait)
    elif top_trait == "Imagination" and second_trait == "Social Sensitivity":
        return ("Playful Improviser",
                "You love spontaneous creativity, games, and improvisation with others.",
                "Add structure to channel playful sparks into lasting results.",
                top_trait, second_trait)

    # Single-trait archetypes
    if top_trait == "Imagination":
        return ("Imaginative Storyteller",
                "You love narrative, symbolism, and creating new worlds.",
                "Transform stories into action or products.",
                top_trait, second_trait)
    elif top_trait == "Curiosity":
        return ("Inquisitive Explorer",
                "You are energized by questions, new information, and discovery.",
                "Narrow focus at times to turn curiosity into creations.",
                top_trait, second_trait)
    elif top_trait == "Risk-taking":
        return ("Fearless Challenger",
                "You thrive on breaking rules and disrupting the status quo.",
                "Learn when to take calculated risks versus when to pause.",
                top_trait, second_trait)
    elif top_trait == "Persistence":
        return ("Resilient Maker",
                "You stick with creative work through obstacles and setbacks.",
                "Pair persistence with reflection to avoid burnout.",
                top_trait, second_trait)
    elif top_trait == "Social Sensitivity":
        return ("Empathic Creator",
                "You tune into people’s needs and create with empathy at the core.",
                "Pair empathy with boldness to push ideas further.",
                top_trait, second_trait)

    # Balanced fallback
    return ("Grounded Realist",
            "You integrate imagination, persistence, and empathy in steady ways.",
            "Push beyond comfort zones to discover new strengths.",
            top_trait, second_trait)

# ----------------------------
# 2. PDF EXPORT FUNCTION
# ----------------------------
def create_pdf(profile_name, profile_desc, profile_growth, traits, top_trait, second_trait):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Creative Identity Report", ln=True, align="C")

    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.multi_cell(0, 10, f"Profile: {profile_name}")
    pdf.multi_cell(0, 10, f"Description: {profile_desc}")
    pdf.multi_cell(0, 10, f"Growth Suggestion: {profile_growth}")

    pdf.ln(10)
    pdf.multi_cell(0, 10, f"Your strongest traits were: {top_trait} and {second_trait}.")

    pdf.ln(10)
    pdf.cell(200, 10, "Trait Scores:", ln=True)
    for k, v in traits.items():
        pdf.cell(200, 10, f"{k}: {v}", ln=True)

    return pdf

# ----------------------------
# 3. STREAMLIT APP
# ----------------------------
st.title("✨ Creative Identity Profile ✨")
st.write("Answer each question on a scale from 1 (Strongly Disagree) to 5 (Strongly Agree).")

# --- IMAGINATION ---
st.subheader("Imagination")
i1 = st.radio("I enjoy inventing new stories or ideas.", [1,2,3,4,5], horizontal=True)
i2 = st.radio("I often picture possibilities others don’t see.", [1,2,3,4,5], horizontal=True)
i3 = st.radio("I like to imagine alternative futures.", [1,2,3,4,5], horizontal=True)
i4 = st.radio("I use daydreaming to explore new ideas.", [1,2,3,4,5], horizontal=True)
imagination_score = i1+i2+i3+i4

# --- CURIOSITY ---
st.subheader("Curiosity")
c1 = st.radio("I like asking questions to understand how things work.", [1,2,3,4,5], horizontal=True)
c2 = st.radio("I get excited when learning something new.", [1,2,3,4,5], horizontal=True)
c3 = st.radio("I often investigate topics that spark my interest.", [1,2,3,4,5], horizontal=True)
c4 = st.radio("I enjoy exploring subjects outside my expertise.", [1,2,3,4,5], horizontal=True)
curiosity_score = c1+c2+c3+c4

# --- RISK-TAKING ---
st.subheader("Risk-taking")
r1 = st.radio("I’m comfortable trying things without knowing the outcome.", [1,2,3,4,5], horizontal=True)
r2 = st.radio("I see mistakes as part of learning.", [1,2,3,4,5], horizontal=True)
r3 = st.radio("I would rather try something new than repeat what works.", [1,2,3,4,5], horizontal=True)
r4 = st.radio("I take on challenges even when success isn’t guaranteed.", [1,2,3,4,5], horizontal=True)
risk_score = r1+r2+r3+r4

# --- PERSISTENCE ---
st.subheader("Persistence")
p1 = st.radio("I keep working on problems even when they’re frustrating.", [1,2,3,4,5], horizontal=True)
p2 = st.radio("I don’t give up easily when stuck.", [1,2,3,4,5], horizontal=True)
p3 = st.radio("I believe effort matters more than talent.", [1,2,3,4,5], horizontal=True)
p4 = st.radio("I push through difficulties until I find a solution.", [1,2,3,4,5], horizontal=True)
persistence_score = p1+p2+p3+p4

# --- SOCIAL SENSITIVITY ---
st.subheader("Social Sensitivity")
s1 = st.radio("I notice how others are feeling.", [1,2,3,4,5], horizontal=True)
s2 = st.radio("I adapt my ideas when working with a group.", [1,2,3,4,5], horizontal=True)
s3 = st.radio("I enjoy collaborating and building on others’ ideas.", [1,2,3,4,5], horizontal=True)
s4 = st.radio("I try to make sure everyone feels included in discussions.", [1,2,3,4,5], horizontal=True)
social_score = s1+s2+s3+s4

# Collect scores
traits = {
    "Imagination": imagination_score,
    "Curiosity": curiosity_score,
    "Risk-taking": risk_score,
    "Persistence": persistence_score,
    "Social Sensitivity": social_score,
}

# Archetype
profile_name, profile_desc, profile_growth, top_trait, second_trait = assign_profile(traits)

st.subheader(f"🌟 Your Creative Archetype: {profile_name}")
st.write(profile_desc)
st.write("**Growth suggestion:**", profile_growth)
st.write(f"Your strongest traits were: {top_trait} and {second_trait}.")

# ----------------------------
# 4. RADAR CHART
# ----------------------------
labels = list(traits.keys())
values = list(traits.values())
angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
values += values[:1]
angles += angles[:1]

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
ax.plot(angles, values, "o-", linewidth=2)
ax.fill(angles, values, alpha=0.25)
ax.set_yticklabels([])
ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels)
st.pyplot(fig)

# ----------------------------
# 5. EXPORT PDF
# ----------------------------
if st.button("📄 Export Report as PDF"):
    pdf = create_pdf(profile_name, profile_desc, profile_growth, traits, top_trait, second_trait)
    pdf_output = "Creative_Identity_Report.pdf"
    pdf.output(pdf_output)
    with open(pdf_output, "rb") as f:
        st.download_button("⬇️ Download Report", f, file_name=pdf_output)
