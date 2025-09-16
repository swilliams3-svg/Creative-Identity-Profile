import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors

st.set_page_config(page_title="Creative Identity Profile", layout="centered")

# ------------------------------------
# Colour Palette
# ------------------------------------
creative_colors = {
    "Originality": "#E63946",
    "Curiosity": "#F4A261",
    "Risk-Taking": "#2A9D8F",
    "Imagination": "#9D4EDD",
    "Discipline": "#264653",
    "Collaboration": "#E9C46A",
}
big5_colors = {
    "Openness": "#4D908E",
    "Conscientiousness": "#577590",
    "Extraversion": "#F3722C",
    "Agreeableness": "#90BE6D",
    "Neuroticism": "#F94144",
}

# ------------------------------------
# Archetypes
# ------------------------------------
archetypes = {
    "Originality": {
        "name": "The Innovator",
        "label": "Divergent Thinker",
        "summary_high": "You thrive on breaking patterns and offering unique perspectives. Others see you as someone who sparks fresh ideas and challenges conventional thinking.",
        "growth": "Practice brainstorming multiple solutions to a problem. Quantity often leads to originality.",
    },
    "Curiosity": {
        "name": "The Explorer",
        "label": "Openness-driven Creative",
        "summary_high": "You are constantly seeking new knowledge, experiences, and perspectives. Your open-mindedness helps you discover connections others miss.",
        "growth": "Adopt a beginner’s mindset. Ask simple questions even about familiar things to reignite curiosity.",
    },
    "Risk-Taking": {
        "name": "The Adventurer",
        "label": "Tolerance for Uncertainty",
        "summary_high": "You’re willing to step into the unknown and embrace uncertainty, which fuels bold and experimental creativity.",
        "growth": "Start with small, low-stakes risks to build confidence before taking bigger creative leaps.",
    },
    "Imagination": {
        "name": "The Dreamer",
        "label": "Imaginative Creator",
        "summary_high": "You can easily envision possibilities and think beyond what currently exists. Creativity flourishes through imagery, storytelling, and future-focused thinking.",
        "growth": "Engage in exercises like free drawing, mind-mapping, or writing 'what if' scenarios.",
    },
    "Discipline": {
        "name": "The Builder",
        "label": "Conscientious Creator",
        "summary_high": "You bring structure, persistence, and focus to creative work. You excel at turning ideas into finished, polished outcomes.",
        "growth": "Break goals into smaller steps and set deadlines to encourage consistent progress.",
    },
    "Collaboration": {
        "name": "The Connector",
        "label": "Socially-Driven Creative",
        "summary_high": "You value teamwork, feedback, and co-creation. You bring out the best in others and thrive in collaborative environments.",
        "growth": "Share even half-formed ideas with peers — collaboration doesn’t require perfection.",
    },
}

# ------------------------------------
# Question Bank (33 questions)
# ------------------------------------
creative_traits = {
    "Originality": [
        "I enjoy producing novel and unconventional ideas.",
        "I often think of alternative solutions others might not consider.",
        "I value uniqueness in my work and thinking.",
    ],
    "Curiosity": [
        "I like questioning and exploring new concepts.",
        "I seek out opportunities to learn new things.",
        "I am curious about how things work.",
    ],
    "Risk-Taking": [
        "I am comfortable with uncertainty when exploring ideas.",
        "I don’t mind failing if it means trying something new.",
        "I take creative risks in my projects.",
    ],
    "Imagination": [
        "I often visualize possibilities in my mind.",
        "I enjoy daydreaming and thinking about new scenarios.",
        "I use mental imagery when solving problems.",
    ],
    "Discipline": [
        "I can stay focused on creative projects until completion.",
        "I put structured effort into developing my ideas.",
        "I persist with my work even when it is challenging.",
    ],
    "Collaboration": [
        "I value feedback from others in my creative process.",
        "I enjoy exchanging ideas with others.",
        "I often co-create with peers or colleagues.",
    ],
}
big5_traits = {
    "Openness": [
        "I enjoy exploring new ideas and perspectives.",
        "I am open to different experiences and viewpoints.",
        "I like engaging with abstract or imaginative ideas.",
    ],
    "Conscientiousness": [
        "I pay attention to details when working.",
        "I follow through with my plans and goals.",
        "I like being organized in my daily life.",
    ],
    "Extraversion": [
        "I feel energized when interacting with people.",
        "I enjoy group activities and conversations.",
        "I like being in social situations.",
    ],
    "Agreeableness": [
        "I am considerate of others’ needs and feelings.",
        "I value cooperation over competition.",
        "I try to maintain harmony in groups.",
    ],
    "Neuroticism": [
        "I often feel stressed or anxious in daily life.",
        "I can become easily worried about problems.",
        "I sometimes struggle to remain calm under pressure.",
    ],
}

# ------------------------------------
# Helper Functions
# ------------------------------------
def get_level(score):
    if score >= 4: return "High"
    elif score >= 2.5: return "Medium"
    else: return "Low"

def radar_chart(scores, palette, title):
    labels = list(scores.keys())
    values = list(scores.values())
    values += values[:1]
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
    for i, trait in enumerate(labels):
        ax.fill([angles[i], angles[i+1], 0], [values[i], values[i+1], 0],
                color=palette[trait], alpha=0.2)
    ax.plot(angles, values, color="black", linewidth=1.5)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_yticklabels([])
    ax.set_title(title, size=14, weight="bold", pad=20)
    st.pyplot(fig)

    buf = io.BytesIO()
    fig.savefig(buf, format="PNG")
    buf.seek(0)
    return buf

# ------------------------------------
# Session State
# ------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "intro"
if "responses" not in st.session_state:
    st.session_state.responses = {}

# ------------------------------------
# Intro Page
# ------------------------------------
if st.session_state.page == "intro":
    st.title("Creative Identity & Personality Profile")
    st.markdown("""
    Welcome!  
    This quiz explores both your **creative traits** and the **Big Five personality dimensions**.  

    - Answer **33 questions** on a 1–5 scale (1 = Strongly Disagree, 5 = Strongly Agree).  
    - Get insights into your creativity, personality, and unique **archetype identity**.  
    - Download a **personalised PDF report** at the end.  
    """)
    if st.button("Start Quiz"):
        st.session_state.page = "quiz"
        st.rerun()

# ------------------------------------
# Quiz Page
# ------------------------------------
elif st.session_state.page == "quiz":
    st.header("Quiz Questions")
    with st.form("quiz_form"):
        for trait, questions in {**creative_traits, **big5_traits}.items():
            st.subheader(trait)
            for q in questions:
                key = f"{trait}_{q}"
                st.session_state.responses[key] = st.radio(
                    q, [1, 2, 3, 4, 5], horizontal=True, key=key
                )
        submitted = st.form_submit_button("Submit Quiz")
        if submitted:
            st.session_state.page = "results"
            st.rerun()

# ------------------------------------
# Results Page
# ------------------------------------
elif st.session_state.page == "results":
    st.title("Your Creative Identity Profile")

    # Scores
    creative_scores = {t: np.mean([st.session_state.responses[f"{t}_{q}"] for q in qs]) for t, qs in creative_traits.items()}
    big5_scores = {t: np.mean([st.session_state.responses[f"{t}_{q}"] for q in qs]) for t, qs in big5_traits.items()}

    # Archetypes
    sorted_traits = sorted(creative_scores.items(), key=lambda x: x[1], reverse=True)
    primary_trait, sub_trait = sorted_traits[0][0], sorted_traits[1][0]
    st.subheader("Your Archetypes")
    for trait in [primary_trait, sub_trait]:
        arch = archetypes[trait]
        col = creative_colors[trait]
        st.markdown(f"""
        <div style="border:2px solid {col}; border-radius:12px; padding:12px; margin-bottom:10px;">
        <h4 style="color:{col}; margin:0;">{arch['name']} ({trait})</h4>
        <em>{arch['label']}</em><br>
        <p>{arch['summary_high'] if get_level(creative_scores[trait])=='High' else arch['growth']}</p>
        </div>
        """, unsafe_allow_html=True)

    # Charts
    st.subheader("Radar Charts")
    chart_buf_creative = radar_chart(creative_scores, creative_colors, "Creative Traits")
    chart_buf_big5 = radar_chart(big5_scores, big5_colors, "Big Five Personality")

    # Summaries
    st.subheader("Trait Insights")
    for trait, score in creative_scores.items():
        st.markdown(f"**{trait} ({get_level(score)}) — {score:.2f}/5**")
    for trait, score in big5_scores.items():
        st.markdown(f"**{trait} ({get_level(score)}) — {score:.2f}/5**")

    # Science
    with st.expander("The Science Behind the Profile"):
        st.markdown("Full academic explanation and references go here...")

    # PDF
    def create_pdf():
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=A4)
        width, height = A4

        # Cover
        c.setFont("Helvetica-Bold", 22)
        c.drawCentredString(width/2, height-100, "Creative Identity & Personality Profile")
        c.showPage()

        # Charts
        img1, img2 = ImageReader(chart_buf_creative), ImageReader(chart_buf_big5)
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width/2, height-40, "Radar Charts")
        c.drawImage(img1, 60, height-320, width=200, height=200)
        c.drawImage(img2, 300, height-320, width=200, height=200)
        c.showPage()

        # Archetypes
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width/2, height-40, "Your Archetypes")
        y = height-100
        for trait in [primary_trait, sub_trait]:
            arch = archetypes[trait]
            col = colors.HexColor(creative_colors[trait])
            c.setFillColor(col)
            c.rect(60, y-60, width-120, 60, stroke=1, fill=0)
            c.setFont("Helvetica-Bold", 12)
            c.drawString(70, y-40, f"{arch['name']} ({trait}) – {arch['label']}")
            c.setFont("Helvetica", 10)
            c.setFillColor(colors.black)
            text = arch['summary_high'] if get_level(creative_scores[trait])=="High" else arch['growth']
            c.drawString(70, y-55, text)
            y -= 80
        c.showPage()

        # Summaries
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width/2, height-40, "Trait Insights")
        y = height-80
        for trait, score in {**creative_scores, **big5_scores}.items():
            col = creative_colors.get(trait, big5_colors.get(trait))
            c.setFillColor(colors.HexColor(col))
            c.setFont("Helvetica-Bold", 12)
            c.drawString(60, y, f"{trait} ({get_level(score)}) — {score:.2f}/5")
            c.setFillColor(colors.black)
            y -= 20
            if y < 80:
                c.showPage()
                y = height-80
        c.showPage()

        # Science
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width/2, height-40, "The Science Behind the Profile")
        c.setFont("Helvetica", 10)
        c.drawString(60, height-80, "Academic explanation and references here...")
        c.save()
        buf.seek(0)
        return buf

    pdf_buf = create_pdf()
    st.download_button("Download Full Report (PDF)", data=pdf_buf,
                       file_name="Creative_Identity_Profile.pdf",
                       mime="application/pdf")
