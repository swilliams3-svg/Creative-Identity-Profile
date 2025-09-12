import streamlit as st
import matplotlib.pyplot as plt
import io
from fpdf import FPDF

# --------------------------
# Archetypes & Descriptions
# --------------------------
archetypes = {
    "Explorer": {
        "name": "Explorer",
        "description": "Curious, adventurous, and driven by discovery. You thrive when exploring new ideas and perspectives.",
        "improvement": "Practice finishing projects, not just starting them. Set goals for deeper exploration."
    },
    "Dreamer": {
        "name": "Dreamer",
        "description": "Imaginative, visionary, and future-oriented. You love thinking of possibilities and creative solutions.",
        "improvement": "Balance dreaming with practical planning. Try turning one idea into a concrete step."
    },
    "Maker": {
        "name": "Maker",
        "description": "Hands-on, practical, and experimental. You learn by doing and enjoy bringing ideas into tangible form.",
        "improvement": "Work on reflecting before building. Practice patience and documenting your process."
    },
    "Connector": {
        "name": "Connector",
        "description": "Collaborative, empathetic, and socially attuned. You shine when working with others and sharing creativity.",
        "improvement": "Balance collaboration with independent work. Protect your own creative energy too."
    }
}

# --------------------------
# Questionnaire
# --------------------------
questions = {
    "Explorer": [
        "I enjoy discovering new ideas and perspectives.",
        "I often seek out new experiences and adventures.",
        "I find inspiration in the unknown.",
        "I like to challenge assumptions and think differently.",
        "I actively seek learning opportunities."
    ],
    "Dreamer": [
        "I often imagine possibilities beyond the present.",
        "I get excited by creative visions of the future.",
        "I enjoy brainstorming imaginative solutions.",
        "I like thinking about 'what if' scenarios.",
        "I am energized by visionary goals."
    ],
    "Maker": [
        "I enjoy working with my hands or experimenting.",
        "I like creating things from scratch.",
        "I learn best through practice and making.",
        "I often prototype or test ideas quickly.",
        "I feel most satisfied when I bring ideas into reality."
    ],
    "Connector": [
        "I enjoy collaborating with others on creative projects.",
        "I thrive on sharing ideas with people.",
        "I get inspired by social connections.",
        "I value empathy and understanding in creativity.",
        "I believe creativity grows best in community."
    ]
}

# --------------------------
# Helpers
# --------------------------
def clean_text(text):
    """Ensure text is safe for fpdf (latin-1 only)."""
    return text.encode("latin-1", "replace").decode("latin-1")

def get_trait_level(score):
    if score < 2:
        return "Low"
    elif score < 3.5:
        return "Moderate"
    else:
        return "High"

def calculate_scores(responses):
    scores = {}
    for trait, qs in questions.items():
        trait_scores = [responses[q] for q in qs]
        scores[trait] = sum(trait_scores) / len(qs)
    return scores

def create_chart(scores):
    fig, ax = plt.subplots(figsize=(6, 4))
    traits = list(scores.keys())
    values = list(scores.values())
    ax.bar(traits, values, color="skyblue")
    ax.set_ylim(0, 5)
    ax.set_ylabel("Average Score (1-5)")
    ax.set_title("Creative Trait Profile")
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return buf

def create_pdf(scores, main_trait, chart_buf):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Title
    pdf.cell(200, 10, clean_text("Your Creative Identity Profile"), ln=True, align="C")
    pdf.ln(10)

    # Main Archetype
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, clean_text(f"Main Archetype: {archetypes[main_trait]['name']}"), ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, clean_text(archetypes[main_trait]["description"]))
    pdf.multi_cell(0, 10, clean_text("How to grow: " + archetypes[main_trait]["improvement"]))
    pdf.ln(5)

    # Scores
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Your Scores:", ln=True)
    pdf.set_font("Arial", size=12)
    for trait, score in scores.items():
        level = get_trait_level(score)
        pdf.multi_cell(0, 10, clean_text(f"{trait} ({level}): {score:.2f}/5"))

    pdf.ln(5)

    # Chart
    chart_buf.seek(0)
    pdf.image(chart_buf, x=10, y=None, w=180)

    return pdf.output(dest="S").encode("latin-1", "replace")

# --------------------------
# Streamlit App
# --------------------------
st.title("🌟 Creative Identity Profile")

st.write("Answer the questions below to discover your dominant creative archetype.")

responses = {}
with st.form("questionnaire"):
    for trait, qs in questions.items():
        st.subheader(trait)
        for q in qs:
            responses[q] = st.radio(q, [1, 2, 3, 4, 5], horizontal=True, index=2)
    submitted = st.form_submit_button("Submit")

if submitted:
    scores = calculate_scores(responses)
    main_trait = max(scores, key=scores.get)

    # Show results
    st.subheader("Your Creative Profile Results")
    st.write(f"**Main Archetype: {archetypes[main_trait]['name']}**")
    st.write(archetypes[main_trait]["description"])
    st.info(f"💡 How to grow: {archetypes[main_trait]['improvement']}")

    # Show chart
    chart_buf = create_chart(scores)
    st.image(chart_buf, caption="Your Creative Trait Profile", use_container_width=True)

    # Offer PDF download
    pdf_bytes = create_pdf(scores, main_trait, chart_buf)
    st.download_button(
        label="📄 Download Your Creative Profile (PDF)",
        data=pdf_bytes,
        file_name="creative_profile.pdf",
        mime="application/pdf",
    )
