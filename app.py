import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

st.set_page_config(page_title="Creative Identity Profile", layout="wide")

# --------------------------
# QUESTIONS (33 total)
# --------------------------
questions = {
    # Creative Traits
    "Originality": [
        "I often come up with ideas that are different from others.",
        "I enjoy finding unique solutions to problems.",
        "I like expressing myself in unusual or distinctive ways."
    ],
    "Curiosity": [
        "I enjoy exploring new topics just for the sake of learning.",
        "I often ask questions about how things work.",
        "I seek out opportunities to broaden my knowledge."
    ],
    "Risk Taking": [
        "I am comfortable taking chances to try something new.",
        "I am willing to make mistakes in order to learn.",
        "I often push myself outside of my comfort zone."
    ],
    "Imagination": [
        "I often create mental pictures or stories in my mind.",
        "I enjoy activities that let me fantasize or dream.",
        "I can easily picture possibilities beyond what exists."
    ],
    "Discipline": [
        "I set aside regular time to work on creative projects.",
        "I stay focused even when tasks become challenging.",
        "I can finish creative ideas even when motivation fades."
    ],
    "Collaboration": [
        "I enjoy sharing ideas with others when working on projects.",
        "I believe teamwork can enhance creative outcomes.",
        "I listen openly to others’ perspectives when creating."
    ],

    # Big Five
    "Openness": [
        "I enjoy trying out new activities and experiences.",
        "I am open to different perspectives and ideas.",
        "I appreciate art, music, or literature deeply."
    ],
    "Conscientiousness": [
        "I pay attention to details when working on tasks.",
        "I like to plan things carefully before starting.",
        "I follow through with commitments I make."
    ],
    "Extraversion": [
        "I feel energized by spending time with other people.",
        "I like being the center of attention in groups.",
        "I often start conversations with strangers."
    ],
    "Agreeableness": [
        "I am considerate of other people’s feelings.",
        "I like cooperating with others rather than competing.",
        "I tend to trust people until given a reason not to."
    ],
    "Neuroticism": [
        "I often feel stressed or anxious about small things.",
        "I get upset easily if things don’t go my way.",
        "I frequently worry about the future."
    ],
}

# --------------------------
# TRAIT INSIGHTS
# --------------------------
trait_insights = {
    "Originality": {
        "High": "You excel at generating unique and unconventional ideas.",
        "Medium": "You balance creative thinking with practical approaches.",
        "Low": "You prefer familiar solutions over novelty."
    },
    "Curiosity": {
        "High": "You have a strong desire to explore and learn.",
        "Medium": "You are interested in learning when it is useful.",
        "Low": "You are more focused on familiar knowledge and routines."
    },
    "Risk Taking": {
        "High": "You embrace uncertainty and new experiences.",
        "Medium": "You are selective about when to take risks.",
        "Low": "You prefer safety and predictability."
    },
    "Imagination": {
        "High": "You frequently picture possibilities beyond the present.",
        "Medium": "You use imagination when needed but remain grounded.",
        "Low": "You are more practical and concrete in thinking."
    },
    "Discipline": {
        "High": "You are structured and committed to creative projects.",
        "Medium": "You maintain some discipline with flexibility.",
        "Low": "You prefer freedom and spontaneity over structure."
    },
    "Collaboration": {
        "High": "You thrive on sharing and co-creating with others.",
        "Medium": "You collaborate when useful but also value independence.",
        "Low": "You prefer working alone to stay in control."
    },
    "Openness": {
        "High": "You welcome new experiences and diverse perspectives.",
        "Medium": "You are open but also cautious with novelty.",
        "Low": "You prefer familiarity and tradition."
    },
    "Conscientiousness": {
        "High": "You are organized, reliable, and goal-focused.",
        "Medium": "You balance planning with flexibility.",
        "Low": "You are spontaneous and less detail-oriented."
    },
    "Extraversion": {
        "High": "You are energized by social interactions.",
        "Medium": "You enjoy company but also value solitude.",
        "Low": "You prefer quiet, reflective environments."
    },
    "Agreeableness": {
        "High": "You are cooperative, empathetic, and compassionate.",
        "Medium": "You balance cooperation with assertiveness.",
        "Low": "You are more focused on your own goals."
    },
    "Neuroticism": {
        "High": "You are more sensitive to stress and emotions.",
        "Medium": "You experience occasional worry or stress.",
        "Low": "You are calm and resilient in most situations."
    },
}

# --------------------------
# ARCHETYPES
# --------------------------
archetypes = {
    "Originality": {
        "Main": "The Innovator",
        "Subs": ["Inventor", "Visionary", "Trendsetter"]
    },
    "Curiosity": {
        "Main": "The Explorer",
        "Subs": ["Seeker", "Learner", "Adventurer"]
    },
    "Risk Taking": {
        "Main": "The Challenger",
        "Subs": ["Pioneer", "Rebel", "Trailblazer"]
    },
    "Imagination": {
        "Main": "The Dreamer",
        "Subs": ["Storyteller", "Artist", "Futurist"]
    },
    "Discipline": {
        "Main": "The Architect",
        "Subs": ["Planner", "Organizer", "Executor"]
    },
    "Collaboration": {
        "Main": "The Connector",
        "Subs": ["Mediator", "Networker", "Partner"]
    },
}

# --------------------------
# COLORS
# --------------------------
creative_colors = {
    "Originality": "#1f77b4",
    "Curiosity": "#ff7f0e",
    "Risk Taking": "#2ca02c",
    "Imagination": "#9467bd",
    "Discipline": "#d62728",
    "Collaboration": "#8c564b",
}

big5_colors = {
    "Openness": "#1f77b4",
    "Conscientiousness": "#ff7f0e",
    "Extraversion": "#2ca02c",
    "Agreeableness": "#9467bd",
    "Neuroticism": "#d62728",
}

answer_colors = {
    1: "#d73027",
    2: "#fc8d59",
    3: "#fee08b",
    4: "#91bfdb",
    5: "#4575b4",
}

# --------------------------
# SESSION STATE
# --------------------------
if "page" not in st.session_state:
    st.session_state.page = 0
if "responses" not in st.session_state:
    st.session_state.responses = {}

# --------------------------
# BUILD QUESTION LIST
# --------------------------
all_questions = []
for trait, qs in questions.items():
    for q in qs:
        all_questions.append((trait, q))

total_qs = len(all_questions)

# --------------------------
# QUIZ FLOW
# --------------------------
page = st.session_state.page
responses = st.session_state.responses

if page < total_qs:
    # Heading
    st.markdown("### Creative Identity Profile Quiz")
    st.write("This quiz explores your **creative traits** and **Big Five personality traits**. "
             "Answer honestly on a scale of 1–5 to receive your personalised profile.")

    # Current question
    trait, question = all_questions[page]
    st.markdown(f"**Question {page+1} of {total_qs}**")
    st.write(question)

    resp_key = f"resp_{page}"
    current_val = responses.get(resp_key, None)

    cols = st.columns(5)
    for i, col in enumerate(cols, 1):
        button_label = str(i)
        if col.button(button_label, key=f"{resp_key}_{i}", help=f"Answer {i}",
                      use_container_width=True):
            st.session_state.responses[resp_key] = i
            st.rerun()
        if current_val == i:
            col.markdown(f"<div style='background-color:{answer_colors[i]}; color:white; text-align:center; "
                         f"padding:4px; border-radius:6px;'>{i}</div>", unsafe_allow_html=True)

    # Navigation
    col1, col2 = st.columns([1, 1])
    with col1:
        if page > 0:
            if st.button("Back", key="back_btn", use_container_width=True):
                st.session_state.page -= 1
                st.rerun()
    with col2:
        if resp_key in responses:
            if st.button("Next Question", key="next_btn", use_container_width=True):
                st.session_state.page += 1
                st.rerun()

    # Progress bar
    answered = sum(v is not None for v in responses.values())
    st.progress(answered / total_qs)

else:
    # --------------------------
    # RESULTS PAGE
    # --------------------------
    st.title("Your Creative Identity Profile")

    # Calculate scores
    scores = {trait: [] for trait in questions}
    for i, (trait, q) in enumerate(all_questions):
        if f"resp_{i}" in responses and responses[f"resp_{i}"] is not None:
            scores[trait].append(responses[f"resp_{i}"])

    avg_scores = {trait: np.mean(vals) if vals else 0 for trait, vals in scores.items()}

    # Display summaries
    for trait, score in avg_scores.items():
        if score >= 4:
            level = "High"
        elif score >= 2.5:
            level = "Medium"
        else:
            level = "Low"

        st.markdown(f"### {trait}: {score:.2f}/5")
        st.write(trait_insights[trait][level])

    # Archetype section with card style
    top_creative = max(creative_colors.keys(), key=lambda t: avg_scores[t])
    archetype = archetypes.get(top_creative, None)
    if archetype:
        st.markdown("---")
        st.subheader("Your Creative Archetype")
        st.markdown(
            f"<div style='background-color:{creative_colors[top_creative]}20; padding:1rem; border-radius:12px;'>"
            f"<span style='color:{creative_colors[top_creative]}; font-weight:bold; font-size:18px;'>{archetype['Main']}</span><br>"
            f"<i>Sub-Archetypes: {', '.join(archetype['Subs'])}</i>"
            f"</div>", unsafe_allow_html=True
        )

    # --------------------------
    # RADAR CHARTS
    # --------------------------
    creative_traits = list(creative_colors.keys())
    big5_traits = list(big5_colors.keys())

    def plot_radar(traits, scores, colors, title):
        labels = traits
        values = [scores[t] for t in traits]
        angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
        values += values[:1]
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(polar=True))
        ax.plot(angles, values, "o-", linewidth=2, color="black")
        ax.fill(angles, values, alpha=0.1, color="gray")

        for i, t in enumerate(traits):
            ax.plot([angles[i], angles[i]], [0, values[i]], color=colors[t], linewidth=3)
            ax.scatter(angles[i], values[i], color=colors[t], s=60, zorder=10, label=t)

        ax.set_thetagrids(np.degrees(angles[:-1]), labels)
        ax.set_ylim(0, 5)
        ax.set_title(title, size=12, pad=20)
        return fig

    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(plot_radar(creative_traits, avg_scores, creative_colors, "Creative Traits"))
    with col2:
        st.pyplot(plot_radar(big5_traits, avg_scores, big5_colors, "Big Five Traits"))

    # --------------------------
    # PDF DOWNLOAD
    # --------------------------
    def create_pdf():
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        c.setFont("Helvetica-Bold", 14)
        c.drawString(1*inch, height-1*inch, "Creative Identity Profile Results")

        y = height - 1.5*inch
        for trait, score in avg_scores.items():
            c.setFont("Helvetica", 12)
            c.drawString(1*inch, y, f"{trait}: {score:.2f}/5")
            y -= 0.3*inch

        if archetype:
            y -= 0.3*inch
            c.setFont("Helvetica-Bold", 12)
            c.drawString(1*inch, y, f"Archetype: {archetype['Main']}")
            y -= 0.3*inch
            c.setFont("Helvetica", 12)
            c.drawString(1*inch, y, "Sub-Archetypes: " + ", ".join(archetype["Subs"]))

        c.showPage()
        c.save()
        buffer.seek(0)
        return buffer

    pdf_buffer = create_pdf()
    st.download_button("📄 Download PDF", data=pdf_buffer,
                       file_name="creative_identity_profile.pdf",
                       mime="application/pdf")
