import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
import random
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

st.set_page_config(page_title="Creative Identity Profile", layout="centered")

# --------------------------
# Colours
# --------------------------
palette = {
    "Originality": "#E56B6F",
    "Curiosity": "#6D9DC5",
    "Risk-Taking": "#F4A259",
    "Imagination": "#A267AC",
    "Discipline": "#4DA1A9",
    "Collaboration": "#C5283D",
    "Openness": "#05668D",
    "Conscientiousness": "#88AB75",
    "Extraversion": "#E2C044",
    "Agreeableness": "#5E60CE",
    "Neuroticism": "#C44536"
}

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
# Trait Descriptions (High/Med/Low)
# --------------------------
trait_descriptions = {
    "Originality": {
        "high": "You thrive on breaking patterns and offering unique perspectives.",
        "medium": "You occasionally show originality but balance it with conventional approaches.",
        "low": "You prefer tried-and-tested methods over generating novel ideas."
    },
    "Curiosity": {
        "high": "You are constantly seeking new knowledge and experiences.",
        "medium": "You are curious when prompted but don’t always explore further.",
        "low": "You are less driven to question or seek out new experiences."
    },
    "Risk-Taking": {
        "high": "You embrace uncertainty and are willing to take creative risks.",
        "medium": "You sometimes take risks but often prefer security.",
        "low": "You prefer safe, predictable routes and avoid uncertainty."
    },
    "Imagination": {
        "high": "You easily envision new possibilities and future scenarios.",
        "medium": "You imagine ideas sometimes but often remain practical.",
        "low": "You focus more on concrete realities than imaginative possibilities."
    },
    "Discipline": {
        "high": "You bring persistence and structure to creative projects.",
        "medium": "You stay disciplined when motivated but can lose focus.",
        "low": "You often find it hard to sustain focus and follow-through."
    },
    "Collaboration": {
        "high": "You thrive in teamwork and enjoy co-creating with others.",
        "medium": "You collaborate when needed but also value independence.",
        "low": "You prefer working alone and rely less on group dynamics."
    },
    "Openness": {
        "high": "You are highly open to new experiences and perspectives.",
        "medium": "You are moderately open, balancing curiosity with practicality.",
        "low": "You prefer familiar routines and are less inclined to explore new ideas."
    },
    "Conscientiousness": {
        "high": "You are highly disciplined and organized in your approach.",
        "medium": "You are reasonably conscientious but can be flexible when needed.",
        "low": "You may struggle with organization and long-term follow-through."
    },
    "Extraversion": {
        "high": "You feel energized by social interactions and group settings.",
        "medium": "You are moderately outgoing but also value time alone.",
        "low": "You prefer quiet, solitary activities over social engagements."
    },
    "Agreeableness": {
        "high": "You are highly cooperative, empathetic, and value harmony.",
        "medium": "You are somewhat agreeable, balancing your needs with others.",
        "low": "You tend to be more competitive and prioritize your own perspective."
    },
    "Neuroticism": {
        "high": "You are highly sensitive to stress and may experience emotional ups and downs.",
        "medium": "You experience occasional stress but generally manage well.",
        "low": "You are calm, resilient, and rarely feel overwhelmed by stress."
    }
}

# --------------------------
# Archetypes
# --------------------------
archetypes = {
    "Originality": ("The Innovator", "Divergent Thinker", "Practice brainstorming multiple solutions."),
    "Curiosity": ("The Explorer", "Openness-driven Creative", "Adopt a beginner’s mindset, asking simple questions."),
    "Risk-Taking": ("The Adventurer", "Tolerance for Uncertainty", "Start with small, low-stakes risks to build confidence."),
    "Imagination": ("The Dreamer", "Imaginative Creator", "Engage in exercises like mind-mapping or ‘what if’ scenarios."),
    "Discipline": ("The Builder", "Conscientious Creator", "Break goals into smaller steps and set clear deadlines."),
    "Collaboration": ("The Connector", "Socially-Driven Creative", "Share even half-formed ideas to invite feedback and growth.")
}

# --------------------------
# Session State Initialisation
# --------------------------
if "page" not in st.session_state:
    st.session_state.page = "intro"
if "responses" not in st.session_state:
    st.session_state.responses = {}

# --------------------------
# Page Routing
# --------------------------
page = st.session_state.page

if page == "intro":
    st.title("Creative Identity & Personality Profile")
    st.markdown("""
    Welcome to the **Creative Identity & Personality Profile**.  
    This quiz explores both your **creative traits** and your **Big Five personality traits**.  

    - You’ll answer **33 statements** on a 1–5 scale.  
    - The quiz is based on established research in creativity and psychology.  
    - At the end, you’ll get a personalised profile, archetype, and tips.  
    """)
    if st.button("Start Quiz"):
        st.session_state.page = "quiz"
        st.rerun()

elif page == "quiz":
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

    # Calculate scores
    creative_scores = {
        t: np.mean([int(st.session_state.responses[f"{t}_{q}"][0]) for q in qs])
        for t, qs in creative_traits.items()
    }
    bigfive_scores = {
        t: np.mean([int(st.session_state.responses[f"{t}_{q}"][0]) for q in qs])
        for t, qs in big_five_traits.items()
    }

    creative_perc = {t: round((s - 1) / 4 * 100) for t, s in creative_scores.items()}
    bigfive_perc = {t: round((s - 1) / 4 * 100) for t, s in bigfive_scores.items()}

    # --------------------------
    # Radar Charts
    # --------------------------
    def radar_chart(scores, title):
        labels = list(scores.keys())
        values = list(scores.values())
        values += values[:1]
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels)
        ax.set_yticklabels([])
        ax.set_title(title, size=14, weight="bold", pad=20)

        for i, label in enumerate(labels):
            val = values[i]
            ax.plot([angles[i], angles[i+1]], [val, values[i+1]], color=palette[label], linewidth=2)

        st.pyplot(fig)

        buf = io.BytesIO()
        fig.savefig(buf, format="PNG")
        buf.seek(0)
        return buf

    st.subheader("Big Five Personality Dimensions")
    chart_buf_big5 = radar_chart(bigfive_perc, "Big Five")

    st.subheader("Creative Traits")
    chart_buf_creative = radar_chart(creative_perc, "Creative Traits")

    # --------------------------
    # Archetypes and Growth Area
    # --------------------------
    sorted_traits = sorted(creative_perc.items(), key=lambda x: x[1], reverse=True)
    main_trait, sub_trait, lowest_trait = sorted_traits[0][0], sorted_traits[1][0], sorted_traits[-1][0]

    st.markdown(f"### Main Archetype: {archetypes[main_trait][0]} ({archetypes[main_trait][1]})")
    st.write(f"**{main_trait}: {creative_perc[main_trait]}%** — {trait_descriptions[main_trait]['high']}")
    st.write(f"**Growth Tip:** {archetypes[main_trait][2]}")

    st.markdown(f"### Sub-Archetype: {archetypes[sub_trait][0]} ({archetypes[sub_trait][1]})")
    st.write(f"**{sub_trait}: {creative_perc[sub_trait]}%** — {trait_descriptions[sub_trait]['medium']}")
    st.write(f"**Growth Tip:** {archetypes[sub_trait][2]}")

    st.markdown(f"### Growth Area: {lowest_trait}")
    st.write(f"**{lowest_trait}: {creative_perc[lowest_trait]}%** — {trait_descriptions[lowest_trait]['low']}")
    st.write(f"**Growth Tip:** {archetypes[lowest_trait][2]}")

    # --------------------------
    # List of Traits
    # --------------------------
    st.subheader("Your Trait Scores")
    for t, p in creative_perc.items():
        st.write(f"**{t}:** {p}%")
    for t, p in bigfive_perc.items():
        st.write(f"**{t}:** {p}%")

    # --------------------------
    # Academic Section
    # --------------------------
with st.expander("The Science Behind the Creative Identity & Personality Profile"):
    with open("academic_section.txt", "r") as f:
        st.markdown(f.read())

    # --------------------------
    # PDF Generation
    # --------------------------
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

        c.showPage()
        c.setFont("Helvetica-Bold", 14)
        c.drawString(40, height - 60, "Archetypes and Growth Area")

        c.setFont("Helvetica", 12)
        c.drawString(40, height - 100, f"Main Archetype: {archetypes[main_trait][0]} ({archetypes[main_trait][1]})")
        c.drawString(40, height - 120, f"Sub-Archetype: {archetypes[sub_trait][0]} ({archetypes[sub_trait][1]})")
        c.drawString(40, height - 140, f"Growth Area: {lowest_trait}")

        c.showPage()
        c.setFont("Helvetica-Bold", 14)
        c.drawString(40, height - 60, "Your Trait Scores")
        y = height - 100
        for t, p in {**creative_perc, **bigfive_perc}.items():
            c.drawString(40, y, f"{t}: {p}%")
            y -= 20

        c.save()
        buf.seek(0)
        return buf

    pdf_buf = create_pdf()
    st.download_button("Download Full Report (PDF)", data=pdf_buf, file_name="Creative_Identity_Profile.pdf", mime="application/pdf")

