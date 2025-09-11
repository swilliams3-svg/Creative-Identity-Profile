import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF

# ----------------------------
# 1. ARCHETYPE FUNCTION
# ----------------------------
def assign_profile(traits, preferences):
    if traits["Imagination"] > 12 and preferences["Artistic"] > 10:
        return "Visionary Dreamer", (
            "You thrive on imagination and artistic exploration.",
            "Lean into surreal art, free writing, and future-scenario thinking."
        )
    elif traits["Curiosity"] > 12 and preferences["Scientific"] > 10:
        return "Analytical Builder", (
            "You are driven by curiosity and analysis.",
            "Experiment with data-driven creativity and puzzles."
        )
    elif traits["Risk-taking"] > 12 and preferences["Practical"] > 10:
        return "Bold Experimenter", (
            "You embrace uncertainty and hands-on learning.",
            "Prototype fast, fail smart, and iterate."
        )
    elif traits["Social Sensitivity"] > 12 and preferences["Social"] > 10:
        return "Collaborative Connector", (
            "You thrive on co-creation and empathy.",
            "Facilitate group brainstorming and collective design."
        )
    else:
        return "Balanced Creator", (
            "You draw on multiple creative strengths.",
            "Experiment with different creative modes to see what sticks."
        )

# ----------------------------
# 2. PDF EXPORT FUNCTION
# ----------------------------
def create_pdf(profile_name, profile_desc, profile_growth, traits, preferences):
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
    pdf.cell(200, 10, "Traits:", ln=True)
    for k, v in traits.items():
        pdf.cell(200, 10, f"{k}: {v}", ln=True)

    pdf.ln(5)
    pdf.cell(200, 10, "Preferences:", ln=True)
    for k, v in preferences.items():
        pdf.cell(200, 10, f"{k}: {v}", ln=True)

    return pdf

# ----------------------------
# 3. STREAMLIT APP
# ----------------------------
st.title("✨ Creative Identity Profile ✨")
st.write("Discover your creative archetype and get tailored growth suggestions.")

# Trait sliders
traits = {
    "Imagination": st.slider("Imagination", 1, 15, 7),
    "Curiosity": st.slider("Curiosity", 1, 15, 7),
    "Risk-taking": st.slider("Risk-taking", 1, 15, 7),
    "Persistence": st.slider("Persistence", 1, 15, 7),
    "Social Sensitivity": st.slider("Social Sensitivity", 1, 15, 7),
}

# Preference sliders
preferences = {
    "Artistic": st.slider("Artistic", 1, 15, 7),
    "Scientific": st.slider("Scientific", 1, 15, 7),
    "Practical": st.slider("Practical", 1, 15, 7),
    "Social": st.slider("Social", 1, 15, 7),
}

# Get archetype
profile_name, (profile_desc, profile_growth) = assign_profile(traits, preferences)

st.subheader(f"🌟 Your Creative Archetype: {profile_name}")
st.write(profile_desc)
st.write("**Growth suggestion:**", profile_growth)

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
    pdf = create_pdf(profile_name, profile_desc, profile_growth, traits, preferences)
    pdf_output = "Creative_Identity_Report.pdf"
    pdf.output(pdf_output)
    with open(pdf_output, "rb") as f:
        st.download_button("⬇️ Download Report", f, file_name=pdf_output)

