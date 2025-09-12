import streamlit as st
import random
import matplotlib.pyplot as plt
import io
from fpdf import FPDF

st.set_page_config(page_title="Creative Identity Profile", layout="centered")

# --- TRAITS & QUESTIONS ---
traits = {
    "Openness": [
        "I enjoy exploring new ideas or experiences.",
        "I like to challenge traditional ways of thinking.",
        "I actively seek out novel information.",
        "I enjoy experimenting with unfamiliar activities."
    ],
    "Flexibility": [
        "I can adapt quickly to unexpected changes.",
        "I find it easy to change my perspective.",
        "I can consider multiple solutions to a problem.",
        "I enjoy shifting between different tasks or ideas."
    ],
    "Imagination": [
        "I often create mental pictures or scenarios.",
        "I enjoy daydreaming about possibilities.",
        "I invent stories or ideas in my mind.",
        "I can easily visualize outcomes."
    ],
    "Risk-Taking": [
        "I am willing to try new things even if I might fail.",
        "I take on challenges outside my comfort zone.",
        "I don’t mind uncertainty when exploring ideas.",
        "I would describe myself as adventurous."
    ],
    "Curiosity": [
        "I ask questions to deepen my understanding.",
        "I explore topics just for the joy of learning.",
        "I enjoy investigating how things work.",
        "I like discovering new fields of knowledge."
    ],
    "Persistence": [
        "I continue working on problems even when difficult.",
        "I set goals and work steadily to achieve them.",
        "I try again after experiencing setbacks.",
        "I stay motivated to finish creative tasks."
    ],
    "Sensitivity": [
        "I notice details that others may overlook.",
        "I am strongly affected by art, music, or nature.",
        "I am aware of emotions in myself and others.",
        "I value beauty and expression."
    ],
    "Playfulness": [
        "I enjoy humor and lighthearted thinking.",
        "I like to make tasks fun through creativity.",
        "I can be silly or playful when solving problems.",
        "I use imagination to make everyday life enjoyable."
    ]
}

# Archetype descriptions
archetype_texts = {
    "Openness": "The Explorer – thrives on new ideas and experiences, always searching for novelty.",
    "Flexibility": "The Adapter – comfortable with change and multiple perspectives.",
    "Imagination": "The Visionary – sees possibilities and worlds beyond the present.",
    "Risk-Taking": "The Adventurer – courageous, bold, and not afraid of failure.",
    "Curiosity": "The Seeker – driven by endless questions and the desire to learn.",
    "Persistence": "The Builder – steady, resilient, and committed to completing challenges.",
    "Sensitivity": "The Empath – tuned into emotions, aesthetics, and subtle details.",
    "Playfulness": "The Jester – brings joy, humor, and lightness into creativity."
}

# Growth tips
growth_tips = {
    "Openness": [
        "Try new art forms, cuisines, or travel experiences regularly.",
        "Practice divergent thinking with 'what if?' scenarios.",
        "Keep a dream or idea journal to capture spontaneous inspiration."
    ],
    "Flexibility": [
        "Find multiple solutions to the same problem deliberately.",
        "Play improvisational games or role-play different perspectives.",
        "Rotate routines to build adaptive thinking."
    ],
    "Imagination": [
        "Explore speculative fiction or create 'future world' scenarios.",
        "Use sketches or mind-maps to expand ideas.",
        "Practice visualization exercises daily."
    ],
    "Risk-Taking": [
        "Start with small risks and scale up gradually.",
        "Reframe failure as feedback or data collection.",
        "Study innovators' risk-taking journeys for inspiration."
    ],
    "Curiosity": [
        "Follow 'rabbit holes' and let one question spark another.",
        "Keep a questions journal instead of focusing only on answers.",
        "Approach familiar topics with a beginner's mindset."
    ],
    "Persistence": [
        "Break big creative goals into smaller milestones.",
        "Celebrate progress, not just outcomes.",
        "Work with accountability partners or creative communities."
    ],
    "Sensitivity": [
        "Notice and reflect on emotional or artistic patterns.",
        "Practice deep listening before responding.",
        "Translate personal experiences into creative expression."
    ],
    "Playfulness": [
        "Set aside time for unstructured 'sandbox' creativity.",
        "Engage in puzzles, wordplay, or humor writing.",
        "Use absurdity and humor to reframe challenges."
    ]
}

# --- FUNCTIONS ---

def create_chart(scores):
    fig, ax = plt.subplots(figsize=(8, 5))
    traits_list = list(scores.keys())
    values = list(scores.values())
    colors = plt.cm.tab20.colors[:len(traits_list)]

    ax.bar(traits_list, values, color=colors)
    ax.set_ylim(0, 20)
    ax.set_ylabel("Score (out of 20)")
    ax.set_title("Creative Traits Profile", fontsize=14)
    plt.xticks(rotation=45, ha="right")

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return buf

from fpdf import FPDF

def create_pdf(scores, archetype, chart_buf):
    pdf = FPDF()
    pdf.add_page()

    # Add a Unicode font (DejaVuSans works well with fpdf2)
    pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", size=16)

    # Title
    pdf.set_fill_color(50, 50, 200)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 15, "🌟 Creative Identity Profile", ln=True, align="C", fill=True)

    # Reset text color for content
    pdf.set_text_color(0, 0, 0)
    pdf.ln(10)

    # Archetype section
    pdf.set_font("DejaVu", size=14)
    pdf.multi_cell(0, 10, f"Main Archetype: {archetype}")
    pdf.ln(5)

    # Insert chart (saved as PNG from buffer)
    chart_file = "chart.png"
    with open(chart_file, "wb") as f:
        f.write(chart_buf.getbuffer())
    pdf.image(chart_file, x=30, y=None, w=150)
    pdf.ln(90)

    # Trait scores
    pdf.set_font("DejaVu", size=12)
    pdf.multi_cell(0, 10, "Trait Scores:")
    for trait, value in scores.items():
        pdf.multi_cell(0, 8, f"{trait}: {value}/5")
    pdf.ln(5)

    # Add growth tips page
    pdf.add_page()
    pdf.set_font("DejaVu", size=14)
    pdf.multi_cell(0, 10, "🌱 Growth Tips")
    pdf.ln(5)

    for trait, value in scores.items():
        pdf.set_font("DejaVu", size=12)
        pdf.multi_cell(0, 8, f"{trait}: {value}/5")
        pdf.set_font("DejaVu", size=11)
        if value <= 2:
            pdf.multi_cell(0, 8, f"➡️ Consider developing {trait} further by practicing small, safe experiments.")
        elif value == 3:
            pdf.multi_cell(0, 8, f"➡️ You show balance in {trait}. Try stretching this trait in new settings.")
        else:
            pdf.multi_cell(0, 8, f"➡️ Your strength in {trait} is clear. Use it to inspire and support others.")
        pdf.ln(4)

    # Output as bytes for download
    return pdf.output(dest="S").encode("latin-1", "ignore")


# --- APP LOGIC ---
st.title("⭐ Creative Identity Profile ⭐")
st.write("Welcome! Rate each statement on a scale of 1–5, where **1 = Strongly Disagree** and **5 = Strongly Agree**.")

# Randomize once and store in session_state
if "all_questions" not in st.session_state:
    st.session_state.all_questions = [(trait, q) for trait, qs in traits.items() for q in qs]
    random.shuffle(st.session_state.all_questions)

responses = {}
total_qs = len(st.session_state.all_questions)
answered = 0

for i, (trait, question) in enumerate(st.session_state.all_questions, 1):
    key = f"{trait}_{i}"
    responses[key] = st.radio(
        f"Q{i}/{total_qs}: {question}",
        [1, 2, 3, 4, 5],
        horizontal=True,
        index=None,
        key=key
    )
    if st.session_state[key] is not None:
        answered += 1

# Progress bar
progress = answered / total_qs
st.progress(progress)

if answered == total_qs:
    st.success("✅ Questionnaire complete!")

    # Calculate scores
    scores = {trait: 0 for trait in traits}
    for key, value in responses.items():
        if value:
            trait = key.split("_")[0]
            scores[trait] += value

    main_trait = max(scores, key=scores.get)

    st.subheader(f"Your Creative Archetype: {main_trait}")
    st.write(archetype_texts[main_trait])

    # Show growth tips for top trait
    st.markdown("### 🌱 Growth Suggestions")
    for tip in growth_tips[main_trait]:
        st.markdown(f"- {tip}")

    # Chart
    chart_buf = create_chart(scores)
    st.image(chart_buf, caption="Your Creative Profile", use_container_width=True)

    # Downloadable PDF
    pdf_bytes = create_pdf(scores, main_trait, chart_buf)
    st.download_button(
        label="📥 Download Your Personalised PDF Report",
        data=pdf_bytes,
        file_name="creative_identity_profile.pdf",
        mime="application/pdf"
    )

