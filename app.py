import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
import random
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors

# --------------------------
# Page setup
# --------------------------
st.set_page_config(page_title="Creative Identity Profile", layout="centered")

# --------------------------
# Colours / gradients
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

gradients = [
    "linear-gradient(90deg, #7b2ff7, #f107a3)",
    "linear-gradient(90deg, #06beb6, #48b1bf)",
    "linear-gradient(90deg, #ff6a00, #ee0979)"
]
chosen_gradient = random.choice(gradients)

st.markdown(f"""
<style>
div.stButton > button {{
    background: {chosen_gradient};
    color: white;
    border-radius: 12px;
    height: 2.5em;
    min-width: 8em;
    font-size: 16px;
    font-weight: bold;
    transition: 0.3s;
    border: none;
    margin: 0.2em;
}}
div.stButton > button:hover {{
    filter: brightness(1.1);
    transform: scale(1.03);
}}
div.stDownloadButton > button {{
    background: {chosen_gradient};
    color: white;
    border-radius: 12px;
    height: 2.8em;
    min-width: 12em;
    font-size: 16px;
    font-weight: bold;
    transition: 0.3s;
    border: none;
    margin-top: 1em;
}}
div.stDownloadButton > button:hover {{
    filter: brightness(1.1);
    transform: scale(1.03);
}}
.stProgress > div > div > div > div {{
    background-color: #b0b0b0;
}}
</style>
""", unsafe_allow_html=True)

# --------------------------
# Creative Traits
# --------------------------
creative_traits = {
    "Originality": [
        "I often find myself suggesting unusual or unexpected solutions.",
        "I often think of alternative solutions others might not consider.",
        "I value uniqueness in my work and thinking."
    ],
    "Curiosity": [
        "I ask questions even when I’m not sure there’s an easy answer.",
        "I seek out opportunities to learn new things.",
        "I am curious about how things work."
    ],
    "Risk-Taking": [
        "I am comfortable with uncertainty when exploring ideas.",
        "I sometimes avoid new ideas because they might not work.",  # reverse-coded
        "I take creative risks in my projects."
    ],
    "Imagination": [
        "I often picture possibilities in my mind before I try them out.",
        "I enjoy daydreaming and thinking about new scenarios.",
        "I use mental imagery when solving problems."
    ],
    "Discipline": [
        "I can stay focused on creative projects until completion.",
        "I put structured effort into developing my ideas.",
        "I find it difficult to stay focused on creative projects for a long time."  # reverse-coded
    ],
    "Collaboration": [
        "When working with others, I build on their ideas as much as I share my own.",
        "I enjoy exchanging ideas with others.",
        "I often co-create with peers or colleagues."
    ]
}

# --------------------------
# Big Five Traits
# --------------------------
big_five_traits = {
    "Openness": [
        "I enjoy exploring new ideas and perspectives.",
        "I enjoy exploring new art, music, or ideas, even if they’re unfamiliar.",
        "I prefer sticking to familiar routines over trying new experiences."  # reverse-coded
    ],
    "Conscientiousness": [
        "I pay attention to details when working.",
        "I make detailed plans before starting a task.",
        "I often leave tasks unfinished."  # reverse-coded
    ],
    "Extraversion": [
        "I feel energized when interacting with people.",
        "I enjoy group activities and conversations.",
        "I usually prefer being alone rather than in social situations."  # reverse-coded
    ],
    "Agreeableness": [
        "I am considerate of others’ needs and feelings.",
        "I try to see things from other people’s perspectives during disagreements.",
        "I sometimes put my own needs before others’."  # reverse-coded
    ],
    "Neuroticism": [
        "I often feel stressed or anxious in daily life.",
        "I can become easily worried about problems.",
        "I remain calm even when under pressure."  # reverse-coded
    ]
}

# --------------------------
# Reverse-coded mapping
# --------------------------
reverse_items = {
    "Originality": [],
    "Curiosity": [],
    "Risk-Taking": [1],
    "Imagination": [],
    "Discipline": [2],
    "Collaboration": [],
    "Openness": [2],
    "Conscientiousness": [2],
    "Extraversion": [2],
    "Agreeableness": [2],
    "Neuroticism": [2]
}

# --------------------------
# Trait descriptions
# --------------------------
trait_descriptions = {
    "Originality": {
        "high": "You thrive on breaking patterns and offering unique perspectives.",
        "medium": "You sometimes show originality but balance it with conventional approaches.",
        "low": "You prefer tried-and-tested methods over generating novel ideas."
    },
    "Curiosity": {
        "high": "You are constantly seeking new knowledge and experiences.",
        "medium": "You are curious when prompted but don’t always explore further without external motivation.",
        "low": "You are less driven to question or seek out new experiences."
    },
    "Risk-Taking": {
        "high": "You embrace uncertainty and are willing to take creative risks.",
        "medium": "You sometimes take risks but often prefer security.",
        "low": "You prefer safe, predictable routes and avoid uncertainty."
    },
    "Imagination": {
        "high": "You easily envision new possibilities and future scenarios.",
        "medium": "You imagine ideas sometimes but often remain practical and grounded.",
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
        "high": "You are highly receptive to new experiences and perspectives.",
        "medium": "You are somewhat open but prefer familiar territory.",
        "low": "You resist change and prefer predictable approaches."
    },
    "Conscientiousness": {
        "high": "You are dependable, organized, and detail-oriented.",
        "medium": "You show conscientiousness when motivated but not always consistent.",
        "low": "You struggle with structure and consistency."
    },
    "Extraversion": {
        "high": "You are highly energized by social interaction.",
        "medium": "You enjoy socializing but also value time alone.",
        "low": "You are more reserved and often prefer solitary settings."
    },
    "Agreeableness": {
        "high": "You are cooperative, empathetic, and considerate.",
        "medium": "You are agreeable in many cases but assert own needs when necessary.",
        "low": "You are less concerned with harmony and prioritize your own goals."
    },
    "Neuroticism": {
        "high": "You often feel strong emotions such as stress or worry.",
        "medium": "You sometimes feel anxious but can usually manage emotions.",
        "low": "You are emotionally stable and less prone to anxiety."
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
# PDF creation functions
# --------------------------
def create_academic_pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=50, rightMargin=50, topMargin=50, bottomMargin=50)
    styles = {
        "title": ParagraphStyle("title", fontSize=16, leading=20, alignment=TA_CENTER, spaceAfter=12, underline=True, fontName="Helvetica-Bold"),
        "heading": ParagraphStyle("heading", fontSize=13, leading=16, alignment=TA_LEFT, spaceBefore=10, spaceAfter=6, underline=True, fontName="Helvetica-Bold"),
        "body": ParagraphStyle("body", fontSize=11, leading=14, alignment=TA_LEFT, spaceAfter=6, fontName="Helvetica")
    }
    story = []
    try:
        with open("academic_article.txt", "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    story.append(Spacer(1, 12))
                elif line.startswith("# "):
                    story.append(Paragraph(line[2:], styles["title"]))
                elif line.startswith("## "):
                    story.append(Paragraph(line[3:], styles["heading"]))
                else:
                    story.append(Paragraph(line, styles["body"]))
    except FileNotFoundError:
        story.append(Paragraph("Academic article not found.", styles["body"]))
    doc.build(story)
    buffer.seek(0)
    return buffer

def create_results_pdf(creative_perc, bigfive_perc, trait_descriptions, archetypes, chart_buf_creative, chart_buf_big5):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40)
    styles = {
        "title": ParagraphStyle("title", fontSize=18, leading=22, alignment=TA_CENTER, spaceAfter=12, fontName="Helvetica-Bold"),
        "subtitle": ParagraphStyle("subtitle", fontSize=14, leading=18, alignment=TA_LEFT, spaceAfter=8, fontName="Helvetica-Bold"),
        "body": ParagraphStyle("body", fontSize=11, leading=14, alignment=TA_LEFT, spaceAfter=6, fontName="Helvetica")
    }
    story = []
    story.append(Paragraph("Your Creative Identity Profile", styles["title"]))
    story.append(Spacer(1, 12))
    # Charts
    img_creative = Image(chart_buf_creative, width=250, height=250)
    img_big5 = Image(chart_buf_big5, width=250, height=250)
    chart_table = Table([[img_creative, img_big5]], colWidths=[270, 270])
    story.append(chart_table)
    story.append(Spacer(1, 12))
    # Archetypes and traits
    for trait, perc in creative_perc.items():
        story.append(Paragraph(f"{trait}: {perc}%", styles["subtitle"]))
        if perc >= 67:
            story.append(Paragraph(trait_descriptions[trait]["high"], styles["body"]))
        elif perc >= 34:
            story.append(Paragraph(trait_descriptions[trait]["medium"], styles["body"]))
        else:
            story.append(Paragraph(trait_descriptions[trait]["low"], styles["body"]))
        story.append(Spacer(1, 6))
    for trait, perc in bigfive_perc.items():
        story.append(Paragraph(f"{trait}: {perc}%", styles["subtitle"]))
        if perc >= 67:
            story.append(Paragraph(trait_descriptions[trait]["high"], styles["body"]))
        elif perc >= 34:
            story.append(Paragraph(trait_descriptions[trait]["medium"], styles["body"]))
        else:
            story.append(Paragraph(trait_descriptions[trait]["low"], styles["body"]))
        story.append(Spacer(1, 6))
    doc.build(story)
    buffer.seek(0)
    return buffer

# --------------------------
# Page state
# --------------------------
if "page" not in st.session_state:
    st.session_state.page = "intro"
if "responses" not in st.session_state:
    st.session_state.responses = {}

# --------------------------
# Intro Page
# --------------------------
if st.session_state.page == "intro":
    st.title("Creative Personality Profile")
    col1, col2 = st.columns([1, 5])
    with col2:
        st.subheader("What to Expect")
        st.markdown("""
        - **33 short statements**, answered one at a time.  
        - Each uses a **1–5 scale** (*Strongly Disagree → Strongly Agree*).  
        - Takes about **5–7 minutes** to complete.  
        - No right or wrong answers — just be honest about what feels true for you.
        """)
    col1, col2 = st.columns([1, 5])
    with col2:
        st.subheader("What You’ll Get")
        st.markdown("""
        - A personalised profile of your **creative traits** and **personality traits**.  
        - A **visual breakdown** of your results (radar charts).  
        - Your **creative archetype** and growth areas.  
        - Practical **tips** to develop your creativity further.
        """)
    col1, col2 = st.columns([1, 5])
    with col2:
        st.subheader("Why This Matters")
        st.markdown("""
        Creativity and personality shape how you **approach challenges, generate ideas, and collaborate**.  
        By understanding your unique profile, you can:  
        - Play to your strengths.  
        - Recognise and improve growth areas.  
        - Gain deeper insight into your personal and professional identity.
        """)
    st.markdown("---")
    st.markdown("Take your time, reflect honestly, and enjoy discovering your creative identity.")
    if st.button("Start Quiz"):
        st.session_state.current_question = 0
        st.session_state.page = "quiz"
        st.rerun()

# --------------------------
# Quiz Page
# --------------------------
elif st.session_state.page == "quiz":
    if "shuffled_questions" not in st.session_state:
        questions = []
        for trait, qs in {**creative_traits, **big_five_traits}.items():
            for q in qs:
                questions.append((trait, q))
        random.shuffle(questions)
        st.session_state.shuffled_questions = questions
        st.session_state.current_question = 0

    total_questions = len(st.session_state.shuffled_questions)
    current_index = st.session_state.current_question
    trait, q_text = st.session_state.shuffled_questions[current_index]

    st.header("Quiz")
    st.markdown(f"**Question {current_index + 1} of {total_questions}**")
    st.progress((current_index + 1) / total_questions)

    widget_key = f"{trait}_{q_text}"
    prev_answer = st.session_state.responses.get(widget_key, None)
    response = st.radio(
        q_text,
        ["1 Strongly Disagree", "2 Disagree", "3 Neutral", "4 Agree", "5 Strongly Agree"],
        horizontal=True,
        index=None if prev_answer is None else ["1 Strongly Disagree","2 Disagree","3 Neutral","4 Agree","5 Strongly Agree"].index(prev_answer),
        key=widget_key
    )
    st.session_state.responses[widget_key] = response

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.session_state.current_question > 0:
            if st.button("Back"):
                st.session_state.current_question -= 1
                st.rerun()
    with col3:
        if widget_key in st.session_state.responses and st.session_state.responses[widget_key]:
            if st.session_state.current_question < total_questions - 1:
                if st.button("Next"):
                    st.session_state.current_question += 1
                    st.rerun()
            else:
                if st.button("Finish"):
                    st.session_state.page = "results"
                    st.rerun()

# --------------------------
# Results Page
# --------------------------
elif st.session_state.page == "results":
    st.title("Your Creative Identity Profile")

    # --------------------------
    # Score calculation
    # --------------------------
    def calculate_scores(traits, responses):
        scores = {}
        for trait, qs in traits.items():
            trait_values = []
            for i, q in enumerate(qs):
                key = f"{trait}_{q}"
                if key not in responses:
                    continue
                val = int(responses[key][0])
                if trait in reverse_items and i in reverse_items[trait]:
                    val = 6 - val
                trait_values.append(val)
            if trait_values:
                scores[trait] = np.mean(trait_values)
            else:
                scores[trait] = 0
        return scores

    creative_scores = calculate_scores(creative_traits, st.session_state.responses)
    bigfive_scores = calculate_scores(big_five_traits, st.session_state.responses)

    creative_perc = {k: round(v/5*100) for k,v in creative_scores.items()}
    bigfive_perc = {k: round(v/5*100) for k,v in bigfive_scores.items()}

    # --------------------------
    # Radar chart
    # --------------------------
    def radar_chart(scores_dict, title):
        categories = list(scores_dict.keys())
        values = list(scores_dict.values())
        values += values[:1]  # complete loop
        N = len(categories)
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]
        fig, ax = plt.subplots(figsize=(4,4), subplot_kw=dict(polar=True))
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        plt.xticks(angles[:-1], categories)
        ax.plot(angles, values, linewidth=2, linestyle='solid', color="#E56B6F")
        ax.fill(angles, values, alpha=0.25, color="#E56B6F")
        return fig

    fig_creative = radar_chart(list(creative_scores.values()), "Creative Traits")
    fig_big5 = radar_chart(list(bigfive_scores.values()), "Big Five")

    st.pyplot(fig_creative)
    st.pyplot(fig_big5)

    # --------------------------
    # Download PDFs
    # --------------------------
    st.markdown("### Download Your Reports")
    results_pdf = create_results_pdf(creative_perc, bigfive_perc, trait_descriptions, archetypes, io.BytesIO(), io.BytesIO())
    st.download_button("Download Results PDF", data=results_pdf, file_name="creative_profile.pdf", mime="application/pdf")

    academic_pdf = create_academic_pdf()
    st.download_button("Download Academic Article PDF", data=academic_pdf, file_name="academic_article.pdf", mime="application/pdf")
