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
from reportlab.lib.utils import ImageReader

# --------------------------
# Page config
# --------------------------
st.set_page_config(page_title="Creative Identity Profile", layout="centered")

# --------------------------
# --------------------------
# Academic PDF function
# --------------------------
def create_academic_pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=50,
        rightMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = {
        "title": ParagraphStyle(
            "title",
            fontSize=16,
            leading=20,
            alignment=TA_CENTER,
            spaceAfter=12,
            underline=True,
            fontName="Helvetica-Bold"
        ),
        "heading": ParagraphStyle(
            "heading",
            fontSize=13,
            leading=16,
            alignment=TA_LEFT,
            spaceBefore=10,
            spaceAfter=6,
            underline=True,
            fontName="Helvetica-Bold"
        ),
        "body": ParagraphStyle(
            "body",
            fontSize=11,
            leading=14,
            alignment=TA_LEFT,
            spaceAfter=6,
            fontName="Helvetica"
        ),
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
    except:
        story.append(Paragraph("Academic article file not found.", styles["body"]))

    doc.build(story)
    buffer.seek(0)
    return buffer

# --------------------------
# Results PDF function
# --------------------------
def create_results_pdf(creative_perc, bigfive_perc, trait_descriptions, archetypes, chart_buf_creative, chart_buf_big5):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = {
        "title": ParagraphStyle(
            "title",
            fontSize=18,
            leading=22,
            alignment=TA_CENTER,
            spaceAfter=12,
            fontName="Helvetica-Bold"
        ),
        "subtitle": ParagraphStyle(
            "subtitle",
            fontSize=14,
            leading=18,
            alignment=TA_LEFT,
            spaceAfter=8,
            fontName="Helvetica-Bold"
        ),
        "body": ParagraphStyle(
            "body",
            fontSize=11,
            leading=14,
            alignment=TA_LEFT,
            spaceAfter=6,
            fontName="Helvetica"
        ),
    }

    story = []

    # Title
    story.append(Paragraph("Your Creative Identity Profile", styles["title"]))
    story.append(Spacer(1, 12))

    # Charts side by side
    img_creative = Image(chart_buf_creative, width=250, height=250)
    img_big5 = Image(chart_buf_big5, width=250, height=250)
    chart_table = Table([[img_creative, img_big5]], colWidths=[270, 270])
    story.append(chart_table)
    story.append(Spacer(1, 12))

    # Archetypes
    sorted_traits = sorted(creative_perc.items(), key=lambda x: x[1], reverse=True)
    top_trait, sub_trait, lowest_trait = sorted_traits[0][0], sorted_traits[1][0], sorted_traits[-1][0]
    top_score, sub_score, low_score = sorted_traits[0][1], sorted_traits[1][1], sorted_traits[-1][1]

    def add_archetype(trait, score, title_label):
        if score >= 67:
            desc = trait_descriptions[trait]["high"]
        elif score >= 34:
            desc = trait_descriptions[trait]["medium"]
        else:
            desc = trait_descriptions[trait]["low"]
        story.append(Paragraph(f"{title_label}: {archetypes[trait][0]} ({archetypes[trait][1]})", styles["subtitle"]))
        story.append(Paragraph(desc, styles["body"]))
        story.append(Paragraph(f"<b>Growth Tip:</b> {archetypes[trait][2]}", styles["body"]))
        story.append(Spacer(1, 8))

    add_archetype(top_trait, top_score, "Primary Archetype")
    add_archetype(sub_trait, sub_score, "Sub-Archetype")
    add_archetype(lowest_trait, low_score, "Growth Area")

    story.append(Spacer(1, 12))
    story.append(Paragraph("Trait Scores", styles["subtitle"]))

    for t, p in creative_perc.items():
        story.append(Paragraph(f"{t}: {p}%", styles["body"]))
        if p >= 67:
            story.append(Paragraph(trait_descriptions[t]["high"], styles["body"]))
        elif p >= 34:
            story.append(Paragraph(trait_descriptions[t]["medium"], styles["body"]))
        else:
            story.append(Paragraph(trait_descriptions[t]["low"], styles["body"]))
        story.append(Spacer(1, 4))

    for t, p in bigfive_perc.items():
        story.append(Paragraph(f"{t}: {p}%", styles["body"]))
        if p >= 67:
            story.append(Paragraph(trait_descriptions[t]["high"], styles["body"]))
        elif p >= 34:
            story.append(Paragraph(trait_descriptions[t]["medium"], styles["body"]))
        else:
            story.append(Paragraph(trait_descriptions[t]["low"], styles["body"]))
        story.append(Spacer(1, 4))

    doc.build(story)
    buffer.seek(0)
    return buffer

# --------------------------
# Colour palette
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
# Creative traits
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
# Big Five traits
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
# Reverse-coded items
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
        "high": "You thrive on breaking patterns and offering unique perspectives. Others often see you as a source of fresh, unconventional ideas.",
        "medium": "You sometimes show originality but balance it with conventional approaches, depending on the situation.",
        "low": "You prefer tried-and-tested methods over generating novel ideas, valuing familiarity over experimentation."
    },
    "Curiosity": {
        "high": "You are constantly seeking new knowledge and experiences. You love questioning and exploring beyond the obvious.",
        "medium": "You are curious when prompted but don’t always explore further without external motivation.",
        "low": "You are less driven to question or seek out new experiences, preferring stability and routine."
    },
    "Risk-Taking": {
        "high": "You embrace uncertainty and are willing to take creative risks, seeing setbacks as part of the journey.",
        "medium": "You sometimes take risks but often prefer security, weighing potential downsides before acting.",
        "low": "You prefer safe, predictable routes and avoid uncertainty whenever possible."
    },
    "Imagination": {
        "high": "You easily envision new possibilities and future scenarios. Your ability to think beyond the present helps you innovate.",
        "medium": "You imagine ideas sometimes but often remain practical and grounded in the here-and-now.",
        "low": "You focus more on concrete realities than imaginative possibilities, preferring clarity over abstraction."
    },
    "Discipline": {
        "high": "You bring persistence and structure to creative projects, often ensuring ideas reach completion.",
        "medium": "You stay disciplined when motivated but can lose focus if enthusiasm drops.",
        "low": "You often find it hard to sustain focus and follow-through, which can stall projects."
    },
    "Collaboration": {
        "high": "You thrive in teamwork and enjoy co-creating with others, seeing group input as energising.",
        "medium": "You collaborate when needed but also value independence and personal space.",
        "low": "You prefer working alone and rely less on group dynamics for creativity."
    },
    "Openness": {
        "high": "You are highly receptive to new experiences and perspectives, thriving in environments that encourage growth.",
        "medium": "You are somewhat open to new experiences but prefer familiar territory for security.",
        "low": "You resist change and prefer predictable, familiar approaches over new perspectives."
    },
    "Conscientiousness": {
        "high": "You are dependable, organized, and detail-oriented, which supports long-term goals and achievements.",
        "medium": "You show conscientiousness when motivated but don’t always stay consistent.",
        "low": "You struggle with structure and consistency, often preferring spontaneity."
    },
    "Extraversion": {
        "high": "You are highly energized by social interaction and seek out group experiences.",
        "medium": "You enjoy socializing but also value time alone to recharge.",
        "low": "You are more reserved and often prefer solitary or small-group settings."
    },
    "Agreeableness": {
        "high": "You are cooperative, empathetic, and considerate, often putting group harmony above personal preference.",
        "medium": "You are agreeable in many cases but still assert your own needs when necessary.",
        "low": "You are less concerned with harmony and prioritize your own goals or principles."
    },
    "Neuroticism": {
        "high": "You often feel strong emotions such as stress or worry, which can shape how you react under pressure.",
        "medium": "You sometimes feel anxious or stressed but can usually manage your emotions.",
        "low": "You are emotionally stable, resilient, and less prone to anxiety or negative moods."
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
# Button gradients and styles
# --------------------------
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
# Initialize session_state
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
    st.subheader("What to Expect")
    st.markdown("""
    - **33 short statements**, answered one at a time.  
    - Each uses a **1–5 scale** (*Strongly Disagree → Strongly Agree*).  
    - Takes about **5–7 minutes** to complete.  
    - No right or wrong answers — just be honest about what feels true for you.  
    """)
    st.subheader("What You’ll Get")
    st.markdown("""
    - A personalised profile of your **creative traits** and **personality traits**.  
    - A **visual breakdown** of your results (radar charts).  
    - Your **creative archetype** and growth areas.  
    - Practical **tips** to develop your creativity further.  
    """)
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
    if st.button("Start Quiz", key="start_quiz"):
        st.session_state.current_question = 0
        st.session_state.page = "quiz"
        st.rerun()

# --------------------------
# Quiz Page
# --------------------------
elif st.session_state.page == "quiz":
    # Shuffle questions once
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
    progress = int((current_index + 1) / total_questions * 100)
    st.progress(progress / 100)

    # Radio buttons
    answer = st.radio(
        q_text,
        ["1", "2", "3", "4", "5"],
        index=2,
        key=f"q_{current_index}"
    )

    # Save response
    st.session_state.responses[current_index] = answer

    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        if st.button("Next", key=f"next_{current_index}"):
            if current_index + 1 < total_questions:
                st.session_state.current_question += 1
            else:
                st.session_state.page = "results"
            st.rerun()
    with col1:
        if current_index > 0:
            if st.button("Back", key=f"back_{current_index}"):
                st.session_state.current_question -= 1
                st.rerun()

# --------------------------
# Results Page
# --------------------------
elif st.session_state.page == "results":
    st.title("Your Creative Identity Profile")
    responses = st.session_state.responses

    # Convert responses to numeric values
    creative_scores = {trait: [] for trait in creative_traits}
    bigfive_scores = {trait: [] for trait in big_five_traits}

    for idx, (trait, _) in enumerate(st.session_state.shuffled_questions):
        val = int(responses[idx])
        # Check reverse coding
        if idx % 3 in reverse_items.get(trait, []):
            val = 6 - val
        if trait in creative_traits:
            creative_scores[trait].append(val)
        else:
            bigfive_scores[trait].append(val)

    creative_avg = {k: int(np.mean(v) / 5 * 100) for k, v in creative_scores.items()}
    bigfive_avg = {k: int(np.mean(v) / 5 * 100) for k, v in bigfive_scores.items()}

    # Radar chart
    def radar_chart(scores, title):
        labels = list(scores.keys())
        values = list(scores.values())
        N = len(labels)
        angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
        values += values[:1]
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(5,5), subplot_kw=dict(polar=True))
        ax.plot(angles, values, 'o-', linewidth=2)
        ax.fill(angles, values, alpha=0.25)
        ax.set_thetagrids(np.degrees(angles[:-1]), labels)
        ax.set_ylim(0, 100)
        ax.set_title(title)
        return fig

    fig_creative = radar_chart(creative_avg, "Creative Traits")
    fig_big5 = radar_chart(bigfive_avg, "Big Five Traits")

    # Save charts to buffers
    chart_buf_creative = io.BytesIO()
    chart_buf_big5 = io.BytesIO()
    fig_creative.savefig(chart_buf_creative, format='PNG', bbox_inches='tight')
    fig_big5.savefig(chart_buf_big5, format='PNG', bbox_inches='tight')
    chart_buf_creative.seek(0)
    chart_buf_big5.seek(0)
    plt.close('all')

    st.pyplot(fig_creative)
    st.pyplot(fig_big5)

    # Download buttons
    results_pdf_buffer = create_results_pdf(creative_avg, bigfive_avg, trait_descriptions, archetypes, chart_buf_creative, chart_buf_big5)
    st.download_button("Download Results PDF", results_pdf_buffer, file_name="creative_profile_results.pdf", mime="application/pdf")

    academic_pdf_buffer = create_academic_pdf()
    st.download_button("Download Academic PDF", academic_pdf_buffer, file_name="creative_profile_academic.pdf", mime="application/pdf")
