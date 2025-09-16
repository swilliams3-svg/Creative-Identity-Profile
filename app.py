import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# --------------------------
# Page Setup
# --------------------------
st.set_page_config(page_title="Creative Identity Profile", layout="centered")

# --------------------------
# Creative Traits & Questions
# --------------------------
creative_traits = {
    "Originality": [
        "I enjoy producing novel and unconventional ideas.",
        "I often think of alternative solutions others might not consider.",
        "I value uniqueness in my work and thinking."
    ],
    "Curiosity": [
        "I like questioning and exploring new concepts.",
        "I seek out opportunities to learn new things.",
        "I am curious about how things work."
    ],
    "Risk-Taking": [
        "I am comfortable with uncertainty when exploring ideas.",
        "I don’t mind failing if it means trying something new.",
        "I take creative risks in my projects."
    ],
    "Imagination": [
        "I often visualize possibilities in my mind.",
        "I enjoy daydreaming and thinking about new scenarios.",
        "I use mental imagery when solving problems."
    ],
    "Discipline": [
        "I can stay focused on creative projects until completion.",
        "I put structured effort into developing my ideas.",
        "I persist with my work even when it is challenging."
    ],
    "Collaboration": [
        "I value feedback from others in my creative process.",
        "I enjoy exchanging ideas with others.",
        "I often co-create with peers or colleagues."
    ]
}

# --------------------------
# Big Five Traits & Questions
# --------------------------
big_five_traits = {
    "Openness": [
        "I enjoy exploring new ideas and perspectives.",
        "I am open to different experiences and viewpoints.",
        "I like engaging with abstract or imaginative ideas."
    ],
    "Conscientiousness": [
        "I pay attention to details when working.",
        "I follow through with my plans and goals.",
        "I like being organized in my daily life."
    ],
    "Extraversion": [
        "I feel energized when interacting with people.",
        "I enjoy group activities and conversations.",
        "I like being in social situations."
    ],
    "Agreeableness": [
        "I am considerate of others’ needs and feelings.",
        "I value cooperation over competition.",
        "I try to maintain harmony in groups."
    ],
    "Neuroticism": [
        "I often feel stressed or anxious in daily life.",
        "I can become easily worried about problems.",
        "I sometimes struggle to remain calm under pressure."
    ]
}

# --------------------------
# Colour Palettes
# --------------------------
creative_colors = {
    "Originality": "#E63946",
    "Curiosity": "#F1A208",
    "Risk-Taking": "#43AA8B",
    "Imagination": "#577590",
    "Discipline": "#FF6B6B",
    "Collaboration": "#6A4C93"
}

big5_colors = {
    "Openness": "#264653",
    "Conscientiousness": "#2A9D8F",
    "Extraversion": "#E9C46A",
    "Agreeableness": "#F4A261",
    "Neuroticism": "#E76F51"
}

# --------------------------
# Archetypes
# --------------------------
archetypes = {
    "Originality": {
        "archetype": "The Innovator",
        "sub": "Divergent Thinker",
        "high": "You thrive on breaking patterns and offering unique perspectives.",
        "low": "Practice brainstorming multiple solutions — quantity can spark originality."
    },
    "Curiosity": {
        "archetype": "The Explorer",
        "sub": "Openness-driven Creative",
        "high": "You are constantly seeking new knowledge, experiences, and perspectives.",
        "low": "Adopt a beginner’s mindset — ask simple questions to reignite curiosity."
    },
    "Risk-Taking": {
        "archetype": "The Adventurer",
        "sub": "Tolerance for Uncertainty",
        "high": "You embrace uncertainty and take bold creative leaps.",
        "low": "Start with small, low-stakes risks to build confidence."
    },
    "Imagination": {
        "archetype": "The Dreamer",
        "sub": "Imaginative Creator",
        "high": "You easily envision possibilities and think beyond what exists.",
        "low": "Try mind-mapping, free drawing, or 'what if' exercises to expand imagination."
    },
    "Discipline": {
        "archetype": "The Builder",
        "sub": "Conscientious Creator",
        "high": "You bring structure, persistence, and follow-through to creative work.",
        "low": "Break goals into smaller steps with deadlines to stay consistent."
    },
    "Collaboration": {
        "archetype": "The Connector",
        "sub": "Socially-Driven Creative",
        "high": "You thrive in teamwork and bring out the best in others.",
        "low": "Share early ideas with peers — collaboration thrives on openness."
    }
}

# --------------------------
# Trait Summaries
# --------------------------
creative_summaries = {
    "Originality": "Originality reflects your ability to generate new and unique ideas.",
    "Curiosity": "Curiosity highlights your desire to explore, learn, and seek novelty.",
    "Risk-Taking": "Risk-taking captures how comfortable you are with uncertainty and experimentation.",
    "Imagination": "Imagination measures your capacity to think in mental images and possibilities.",
    "Discipline": "Discipline reflects your persistence, focus, and ability to complete projects.",
    "Collaboration": "Collaboration shows how much you value teamwork and co-creation."
}

big5_summaries = {
    "Openness": "Openness is linked to creativity, imagination, and an appreciation for novelty.",
    "Conscientiousness": "Conscientiousness reflects organization, persistence, and responsibility.",
    "Extraversion": "Extraversion highlights energy gained from social interactions and assertiveness.",
    "Agreeableness": "Agreeableness represents empathy, cooperation, and kindness.",
    "Neuroticism": "Neuroticism measures emotional stability, stress sensitivity, and anxiety."
}

# --------------------------
# Session State
# --------------------------
if "page" not in st.session_state:
    st.session_state.page = "intro"
if "responses" not in st.session_state:
    st.session_state.responses = {}

# --------------------------
# Radar Chart Function
# --------------------------
def radar_chart(scores, title, palette):
    labels = list(scores.keys())
    values = list(scores.values())
    values += values[:1]
    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(5,5), subplot_kw=dict(polar=True))
    ax.plot(angles, values, color="black", linewidth=1, linestyle="dotted")

    for i, (label, value) in enumerate(scores.items()):
        ax.plot([angles[i], angles[i]], [0, value], color=palette[label], linewidth=2)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_yticklabels([])
    ax.set_title(title, size=14, weight="bold", pad=20)
    st.pyplot(fig)

    buf = io.BytesIO()
    fig.savefig(buf, format="PNG")
    buf.seek(0)
    return buf

# --------------------------
# Intro Page
# --------------------------
if st.session_state.page == "intro":
    st.title("Creative Identity & Personality Profile")
    st.markdown("""
    This quiz gives you insight into your **creative traits** and **personality profile**.  
    It combines creativity research with the Big Five model to provide your **archetypes, sub-archetypes, and growth areas**.
    """)
    if st.button("Start Quiz"):
        st.session_state.page = "quiz"
        st.rerun()

# --------------------------
# Quiz Page
# --------------------------
elif st.session_state.page == "quiz":
    st.header("Quiz Questions")

    all_questions = []
    for trait, qs in {**creative_traits, **big_five_traits}.items():
        for q in qs:
            all_questions.append((trait, q))
    random.shuffle(all_questions)

    with st.form("quiz_form"):
        for trait, q in all_questions:
            key = f"{trait}_{q}"
            st.session_state.responses[key] = st.radio(
                q,
                ["1 Strongly Disagree", "2 Disagree", "3 Neutral", "4 Agree", "5 Strongly Agree"],
                horizontal=True,
                key=key
            )
        submitted = st.form_submit_button("Submit Quiz")
        if submitted:
            st.session_state.page = "results"
            st.rerun()

# --------------------------
# Results Page
# --------------------------
elif st.session_state.page == "results":
    st.title("Your Creative Identity Profile")

    creative_scores = {t: np.mean([int(st.session_state.responses[f"{t}_{q}"][0]) for q in qs]) for t, qs in creative_traits.items()}
    big5_scores = {t: np.mean([int(st.session_state.responses[f"{t}_{q}"][0]) for q in qs]) for t, qs in big_five_traits.items()}

    # Radar Charts
    st.subheader("Creative Traits")
    chart_buf_creative = radar_chart(creative_scores, "Creative Traits", creative_colors)

    st.subheader("Big Five Personality Dimensions")
    chart_buf_big5 = radar_chart(big5_scores, "Big Five", big5_colors)

    # Trait Summaries
    st.subheader("Trait Summaries")
    for trait, score in creative_scores.items():
        st.markdown(f"**{trait} ({score:.1f})** – {creative_summaries[trait]}")

    for trait, score in big5_scores.items():
        st.markdown(f"**{trait} ({score:.1f})** – {big5_summaries[trait]}")

    # Archetypes
    st.subheader("Your Creative Archetypes")
    for trait, score in creative_scores.items():
        arch = archetypes[trait]
        if score >= 3.5:
            st.markdown(f"**{arch['archetype']} ({arch['sub']})** – {arch['high']}")
        else:
            st.markdown(f"**Growth Area ({arch['sub']})** – {arch['low']}")

    # Academic Section
    try:
        with open("academic_article.txt", "r", encoding="utf-8") as f:
            academic_article = f.read()
    except FileNotFoundError:
        academic_article = "⚠️ Academic article file not found. Please make sure creative_identity_academic_article.txt is in the same folder."

    with st.expander("The Science Behind the Creative Identity & Personality Profile"):
        st.markdown(academic_article, unsafe_allow_html=True)

    # PDF Export
    def create_pdf():
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=A4)
        width, height = A4

        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(width/2, height - 40, "Creative Identity & Personality Profile")

        # Radar charts
        img1 = ImageReader(chart_buf_creative)
        img2 = ImageReader(chart_buf_big5)
        chart_size = 200
        c.drawImage(img1, 60, height - 280, width=chart_size, height=chart_size, preserveAspectRatio=True, mask='auto')
        c.drawImage(img2, 300, height - 280, width=chart_size, height=chart_size, preserveAspectRatio=True, mask='auto')

        c.showPage()

        # Trait summaries
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width/2, height - 40, "Trait Summaries")
        c.setFont("Helvetica", 10)
        text_obj = c.beginText(60, height - 70)
        for trait, score in creative_scores.items():
            text_obj.textLine(f"{trait} ({score:.1f}) – {creative_summaries[trait]}")
        for trait, score in big5_scores.items():
            text_obj.textLine(f"{trait} ({score:.1f}) – {big5_summaries[trait]}")
        c.drawText(text_obj)

        c.showPage()

        # Academic article
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width/2, height - 40, "The Science Behind the Creative Identity & Personality Profile")
        c.setFont("Helvetica", 10)
        text_obj = c.beginText(60, height - 70)
        for line in academic_article.split("\n"):
            text_obj.textLine(line)
        c.drawText(text_obj)

        c.showPage()
        c.save()
        buf.seek(0)
        return buf

    pdf_buf = create_pdf()
    st.download_button("Download Full Report (PDF)", data=pdf_buf, file_name="Creative_Identity_Profile.pdf", mime="application/pdf")
