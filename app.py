import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
import random
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# --------------------------
# Config
# --------------------------
st.set_page_config(page_title="Creative Identity Profile", layout="centered")

# --------------------------
# Trait Questions
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
# Archetypes Dictionary
# --------------------------
trait_descriptions = {
    "Originality": {
        "archetype": "The Innovator",
        "scientific": "Divergent Thinker",
        "high": "You thrive on breaking patterns and offering unique perspectives. Others see you as someone who sparks fresh ideas and challenges conventional thinking.",
        "medium": "You sometimes generate original ideas but often balance them with conventional solutions.",
        "low": "You prefer tried-and-tested approaches. Growth comes from practicing brainstorming and idea fluency.",
        "growth": "Practice brainstorming multiple solutions to a problem. Quantity often leads to originality."
    },
    "Curiosity": {
        "archetype": "The Explorer",
        "scientific": "Openness-driven Creative",
        "high": "You are constantly seeking new knowledge, experiences, and perspectives. Your open-mindedness helps you discover connections others miss.",
        "medium": "You are open to new things occasionally but may prefer familiar territory.",
        "low": "You stick to what you know. Growth comes from asking more questions and challenging assumptions.",
        "growth": "Adopt a beginner’s mindset. Ask simple questions even about familiar things."
    },
    "Risk-Taking": {
        "archetype": "The Adventurer",
        "scientific": "Tolerance for Uncertainty",
        "high": "You’re willing to step into the unknown and embrace uncertainty, which fuels bold and experimental creativity.",
        "medium": "You take risks selectively, balancing comfort with occasional leaps.",
        "low": "You avoid uncertainty and prefer safe paths. Growth comes from experimenting in low-stakes situations.",
        "growth": "Start with small, low-stakes risks in your projects to build confidence."
    },
    "Imagination": {
        "archetype": "The Dreamer",
        "scientific": "Imaginative Creator",
        "high": "You can easily envision possibilities and think beyond what exists. Your creativity flourishes through imagery, storytelling, and future-focused thinking.",
        "medium": "You use imagination occasionally but may rely more on logic or facts.",
        "low": "You prefer concrete thinking and struggle with abstract scenarios. Growth comes from engaging in creative exercises.",
        "growth": "Try free drawing, mind-mapping, or writing 'what if' scenarios to expand imagination."
    },
    "Discipline": {
        "archetype": "The Builder",
        "scientific": "Conscientious Creator",
        "high": "You bring structure, persistence, and focus to creative work. You excel at turning ideas into finished, polished outcomes.",
        "medium": "You follow through on some ideas but may struggle with consistency.",
        "low": "You find it difficult to persist with projects. Growth comes from building habits and structure.",
        "growth": "Break creative goals into smaller, manageable steps and set deadlines."
    },
    "Collaboration": {
        "archetype": "The Connector",
        "scientific": "Socially-Driven Creative",
        "high": "You value teamwork, feedback, and co-creation. You bring out the best in others and thrive in collaborative environments.",
        "medium": "You collaborate when needed but may prefer independent work.",
        "low": "You prefer working alone and find group dynamics challenging.",
        "growth": "Share even half-formed ideas with peers—collaboration doesn’t require perfection."
    }
}

# --------------------------
# Color Palette
# --------------------------
trait_colors = {
    "Originality": "#FF6B6B",
    "Curiosity": "#6BCB77",
    "Risk-Taking": "#4D96FF",
    "Imagination": "#FFC300",
    "Discipline": "#B983FF",
    "Collaboration": "#FF8E72",
    "Openness": "#2EC4B6",
    "Conscientiousness": "#E71D36",
    "Extraversion": "#FFD23F",
    "Agreeableness": "#8AC926",
    "Neuroticism": "#6A4C93"
}

# --------------------------
# Helper Functions
# --------------------------
def percentage_score(score):
    return round((score - 1) / 4 * 100)

def categorize(score):
    if score >= 4:
        return "high"
    elif score >= 2.5:
        return "medium"
    else:
        return "low"

def radar_chart(scores, title, palette):
    labels = list(scores.keys())
    values = list(scores.values())
    values += values[:1]  # close the polygon

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))

    # Draw each segment of the polygon in its trait colour
    for i in range(len(labels)):
        ax.plot(
            angles[i:i+2], values[i:i+2],
            color=palette[labels[i]],
            linewidth=2
        )

    # Optional: faint fill under the whole shape in grey (remove if not wanted)
    ax.fill(angles, values, color="lightgrey", alpha=0.15)

    # Setup labels
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
# Session State
# --------------------------
if "page" not in st.session_state:
    st.session_state.page = "intro"
if "responses" not in st.session_state:
    st.session_state.responses = {}

# --------------------------
# Pages
# --------------------------
if st.session_state.page == "intro":
    st.title("Creative Identity & Personality Profile")
    st.markdown("""
    Welcome! This quiz will help you explore your **creative identity** and **personality profile**.  
    You'll answer statements on a **1–5 scale** (1 = Strongly Disagree, 5 = Strongly Agree).  
    At the end, you’ll get a **personalised profile with charts and archetypes**.
    """)
    if st.button("Start Quiz"):
        st.session_state.page = "quiz"
        st.rerun()

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
                ["1 - Strongly Disagree", "2 - Disagree", "3 - Neutral", "4 - Agree", "5 - Strongly Agree"],
                horizontal=True,
                key=key
            )
        submitted = st.form_submit_button("Submit Quiz")
        if submitted:
            st.session_state.page = "results"
            st.rerun()

elif st.session_state.page == "results":
    st.title("Your Creative Identity Profile")

    creative_scores = {
        t: np.mean([int(st.session_state.responses[f"{t}_{q}"][0]) for q in qs])
        for t, qs in creative_traits.items()
    }
    bigfive_scores = {
        t: np.mean([int(st.session_state.responses[f"{t}_{q}"][0]) for q in qs])
        for t, qs in big_five_traits.items()
    }

    st.subheader("Big Five Personality Dimensions")
    chart_buf_big5 = radar_chart(bigfive_scores, "Big Five")

    st.subheader("Creative Traits")
    chart_buf_creative = radar_chart(creative_scores, "Creative Traits")

    # Show trait scores and summaries
    for trait, score in creative_scores.items():
        pct = percentage_score(score)
        category = categorize(score)
        desc = trait_descriptions[trait][category]
        st.markdown(f"### {trait} ({pct}%)")
        st.markdown(f"**Archetype:** {trait_descriptions[trait]['archetype']}  \n"
                    f"**Sub-Archetype:** {trait_descriptions[trait]['scientific']}  \n"
                    f"**Summary:** {desc}  \n"
                    f"**Growth Tip:** {trait_descriptions[trait]['growth']}")

    # Collapsible academic article
    with st.expander("The Science Behind the Creative Identity & Personality Profile"):
        try:
            with open("academic_article.txt", "r") as f:
                article = f.read()
            st.markdown(article)
        except FileNotFoundError:
            st.warning("academic_article.txt not found. Please add it to the app folder.")

    # PDF Generation
    def create_pdf():
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=A4)
        width, height = A4

        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(width/2, height - 40, "Creative Identity & Personality Profile")

        img1 = ImageReader(chart_buf_creative)
        img2 = ImageReader(chart_buf_big5)
        c.drawImage(img1, 60, height - 300, width=200, height=200, preserveAspectRatio=True, mask='auto')
        c.drawImage(img2, 320, height - 300, width=200, height=200, preserveAspectRatio=True, mask='auto')

        c.showPage()
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, "Your Results")

        y = height - 80
        c.setFont("Helvetica", 10)
        for trait, score in creative_scores.items():
            pct = percentage_score(score)
            category = categorize(score)
            desc = trait_descriptions[trait][category]
            text = (f"{trait} ({pct}%)\n"
                    f"Archetype: {trait_descriptions[trait]['archetype']}\n"
                    f"Sub-Archetype: {trait_descriptions[trait]['scientific']}\n"
                    f"Summary: {desc}\n"
                    f"Growth Tip: {trait_descriptions[trait]['growth']}\n")
            for line in text.split("\n"):
                c.drawString(50, y, line)
                y -= 14
            y -= 10
            if y < 100:
                c.showPage()
                y = height - 50

        c.save()
        buf.seek(0)
        return buf

    pdf_buf = create_pdf()
    st.download_button("Download Full Report (PDF)", data=pdf_buf, file_name="Creative_Identity_Profile.pdf", mime="application/pdf")
