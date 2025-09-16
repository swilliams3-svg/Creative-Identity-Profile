import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
import random
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# --------------------------
# Page Setup
# --------------------------
st.set_page_config(page_title="Creative Identity Profile", layout="centered")

# --------------------------
# Creative Traits & Big Five
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
# Trait Descriptors (High/Medium/Low)
# --------------------------
trait_descriptions = {
    "Originality": {
        "High": "You thrive on breaking patterns and offering unique perspectives. Others see you as someone who sparks fresh ideas.",
        "Medium": "You sometimes bring new perspectives but balance this with practical solutions.",
        "Low": "You tend to stick with tried-and-tested methods. Practicing brainstorming can boost originality."
    },
    "Curiosity": {
        "High": "You constantly seek new knowledge, experiences, and perspectives, discovering connections others miss.",
        "Medium": "You’re open to learning, though sometimes within familiar boundaries.",
        "Low": "You may prefer routine over exploration. Try a beginner’s mindset to reignite curiosity."
    },
    "Risk-Taking": {
        "High": "You embrace uncertainty, which fuels bold and experimental creativity.",
        "Medium": "You’re cautious but occasionally step into the unknown.",
        "Low": "You avoid risks. Taking small, low-stakes risks can build confidence."
    },
    "Imagination": {
        "High": "You can easily envision possibilities and think beyond what exists.",
        "Medium": "You sometimes think creatively but balance this with realism.",
        "Low": "You prefer concrete facts. Try exercises like free drawing or mind-mapping to build imagination."
    },
    "Discipline": {
        "High": "You bring structure and persistence to creative work, excelling at polished outcomes.",
        "Medium": "You’re fairly consistent but sometimes struggle with follow-through.",
        "Low": "You may find it hard to stay focused. Break goals into smaller steps."
    },
    "Collaboration": {
        "High": "You thrive in teamwork, feedback, and co-creation, bringing out the best in others.",
        "Medium": "You balance independent work with occasional collaboration.",
        "Low": "You prefer working alone. Sharing even half-formed ideas can be valuable."
    }
}

# Archetypes
archetypes = {
    "Originality": ("The Innovator", "Divergent Thinker", "Practice brainstorming multiple solutions to boost originality."),
    "Curiosity": ("The Explorer", "Openness-driven Creative", "Adopt a beginner’s mindset and ask simple questions."),
    "Risk-Taking": ("The Adventurer", "Tolerance for Uncertainty", "Start with small risks before taking big creative leaps."),
    "Imagination": ("The Dreamer", "Imaginative Creator", "Use free drawing, mind-mapping, or 'what if' scenarios."),
    "Discipline": ("The Builder", "Conscientious Creator", "Break goals into smaller, manageable steps."),
    "Collaboration": ("The Connector", "Socially-Driven Creative", "Share ideas early with trusted peers.")
}

# --------------------------
# Session State
# --------------------------
if "page" not in st.session_state:
    st.session_state.page = "intro"
if "responses" not in st.session_state:
    st.session_state.responses = {}

# --------------------------
# Intro Page
# --------------------------
if st.session_state.page == "intro":
    st.title("Creative Identity & Personality Profile")
    st.markdown("""
    Welcome to the **Creative Identity Profile** quiz.  
    This tool helps you explore your **creative traits** and **personality dimensions**.  

    - You will respond to **33 statements** on a 1–5 scale.  
    - At the end, you’ll receive:  
      - A **radar chart** of your scores  
      - **Personalised trait summaries**  
      - Your **archetype, sub-archetype, and growth area**  
      - A downloadable **PDF report**  

    Ready to discover your creative identity?
    """)
    if st.button("Start Quiz"):
        st.session_state.page = "quiz"
        st.rerun()

# --------------------------
# Quiz Page
# --------------------------
elif st.session_state.page == "quiz":
    st.header("Quiz Questions")

    questions = []
    for trait, qs in {**creative_traits, **big_five_traits}.items():
        for q in qs:
            questions.append((trait, q))
    random.shuffle(questions)

    with st.form("quiz_form"):
        for trait, q in questions:
            key = f"{trait}_{q}"
            st.session_state.responses[key] = st.radio(
                q,
                ["1 Strongly Disagree", "2 Disagree", "3 Neutral", "4 Agree", "5 Strongly Agree"],
                horizontal=True,
                key=key,
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

    # Compute scores
    creative_scores = {t: np.mean([int(st.session_state.responses[f"{t}_{q}"][0]) for q in qs]) for t, qs in creative_traits.items()}
    bigfive_scores = {t: np.mean([int(st.session_state.responses[f"{t}_{q}"][0]) for q in qs]) for t, qs in big_five_traits.items()}

    # Radar chart
    def radar_chart(scores, title, color):
        labels = list(scores.keys())
        values = list(scores.values())
        values += values[:1]
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
        ax.plot(angles, values, color=color, linewidth=2)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels)
        ax.set_yticklabels([])
        ax.set_title(title, size=14, weight="bold", pad=20)
        st.pyplot(fig)

        buf = io.BytesIO()
        fig.savefig(buf, format="PNG")
        buf.seek(0)
        return buf

    st.subheader("Big Five Personality Dimensions")
    chart_buf_big5 = radar_chart(bigfive_scores, "Big Five", "#05668D")

    st.subheader("Creative Traits")
    chart_buf_creative = radar_chart(creative_scores, "Creative Traits", "#C5283D")

    # Trait Descriptions + Archetypes
    st.subheader("Trait Insights")
    for trait, score in creative_scores.items():
        level = "High" if score >= 4 else "Medium" if score >= 3 else "Low"
        desc = trait_descriptions[trait][level]
        archetype, sub, growth = archetypes[trait]

        st.markdown(f"""
        **{trait} ({level})**  
        *{desc}*  

        **Archetype:** {archetype}  
        **Sub-Archetype:** {sub}  
        **Growth Area:** {growth}  
        """)

    # Academic Article
    with open("creative_identity_academic_article.txt", "r", encoding="utf-8") as f:
        academic_article = f.read()
    with st.expander("📖 The Science Behind the Creative Identity & Personality Profile"):
        st.markdown(academic_article, unsafe_allow_html=True)

    # PDF Export
    def create_pdf():
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=A4)
        width, height = A4

        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(width/2, height - 40, "Creative Identity & Personality Profile")

        img1 = ImageReader(chart_buf_creative)
        img2 = ImageReader(chart_buf_big5)
        chart_size = 200
        c.drawImage(img1, 60, height - 280, width=chart_size, height=chart_size)
        c.drawImage(img2, 300, height - 280, width=chart_size, height=chart_size)

        y = height - 320
        c.setFont("Helvetica", 12)
        for trait, score in creative_scores.items():
            level = "High" if score >= 4 else "Medium" if score >= 3 else "Low"
            desc = trait_descriptions[trait][level]
            archetype, sub, growth = archetypes[trait]
            text = f"{trait} ({level})\n{desc}\nArchetype: {archetype}\nSub-Archetype: {sub}\nGrowth Area: {growth}\n"
            for line in text.split("\n"):
                c.drawString(60, y, line)
                y -= 15
                if y < 100:
                    c.showPage()
                    y = height - 60

        c.save()
        buf.seek(0)
        return buf

    pdf_buf = create_pdf()
    st.download_button("Download Full Report (PDF)", data=pdf_buf, file_name="Creative_Identity_Profile.pdf", mime="application/pdf")
