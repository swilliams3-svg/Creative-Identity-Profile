import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
import random
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

st.set_page_config(page_title="Creative Identity Profile", layout="centered")

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER
from io import BytesIO

# --------------------------
# Academic PDF function
# --------------------------
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
import io

def create_academic_pdf():
    buffer = io.BytesIO()

    # Set up document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=50,
        rightMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    # Define styles
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

    # Read the academic text file
    with open("academic_article.txt", "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                story.append(Spacer(1, 12))
            elif line.startswith("# "):  # Main heading
                story.append(Paragraph(line[2:], styles["title"]))
            elif line.startswith("## "):  # Subheading
                story.append(Paragraph(line[3:], styles["heading"]))
            else:
                story.append(Paragraph(line, styles["body"]))

    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer


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
# Shared Button Styling (Intro + Quiz Nav)
# --------------------------
import random

gradients = [
    "linear-gradient(90deg, #7b2ff7, #f107a3)",  # Purple gradient (imagination)
    "linear-gradient(90deg, #06beb6, #48b1bf)",  # Teal/blue (flow)
    "linear-gradient(90deg, #ff6a00, #ee0979)",  # Coral/pink (playfulness)
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

    /* PDF Download button styling */
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
    </style>
""", unsafe_allow_html=True)

# Custom CSS for progress bar (grey)
st.markdown("""
    <style>
    /* Target Streamlit progress bar */
    .stProgress > div > div > div > div {
        background-color: #b0b0b0; /* soft grey */
    }
    </style>
""", unsafe_allow_html=True)


# --------------------------
# Page Flow Setup
# --------------------------
if "page" not in st.session_state:
    st.session_state.page = "intro"

# --------------------------
# Intro Page
# --------------------------
if st.session_state.page == "intro":
    st.title("Creative Personality Profile")

    st.markdown("""
    Welcome to the **Creative Identity & Personality Profile**.  
    This short self-reflection quiz combines insights from creativity research and the **Big Five personality framework**.  
    """)

    # What to Expect
    col1, col2 = st.columns([1, 5])
    with col1:
        st.markdown("-")
    with col2:
        st.subheader("What to Expect")
        st.markdown("""
        - **33 short statements**, answered one at a time.  
        - Each uses a **1–5 scale** (*Strongly Disagree → Strongly Agree*).  
        - Takes about **5–7 minutes** to complete.  
        - No right or wrong answers — just be honest about what feels true for you.  
        """)

    # What You’ll Get
    col1, col2 = st.columns([1, 5])
    with col1:
        st.markdown("-")
    with col2:
        st.subheader("What You’ll Get")
        st.markdown("""
        - A personalised profile of your **creative traits** and **personality traits**.  
        - A **visual breakdown** of your results (radar charts).  
        - Your **creative archetype** and growth areas.  
        - Practical **tips** to develop your creativity further.  
        """)

    # Why This Matters
    col1, col2 = st.columns([1, 5])
    with col1:
        st.markdown("-")
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

    # --------------------------
    # Start Quiz Button (only on intro page)
    # --------------------------
    import random

    gradients = [
        "linear-gradient(90deg, #7b2ff7, #f107a3)",  # Purple gradient (imagination)
        "linear-gradient(90deg, #06beb6, #48b1bf)",  # Teal/blue (flow)
        "linear-gradient(90deg, #ff6a00, #ee0979)",  # Coral/pink (playfulness)
    ]

    chosen_gradient = random.choice(gradients)

    st.markdown(f"""
        <style>
        div.stButton > button:first-child {{
            background: {chosen_gradient};
            color: white;
            border-radius: 12px;
            height: 3em;
            width: 100%;
            font-size: 18px;
            font-weight: bold;
            transition: 0.3s;
            border: none;
        }}
        div.stButton > button:first-child:hover {{
            filter: brightness(1.1);
            transform: scale(1.03);
        }}
        </style>
    """, unsafe_allow_html=True)

    if st.button("Start Quiz", key="start_quiz"):
        # Reset state if retaking
        st.session_state.responses = {}
        if "shuffled_questions" in st.session_state:
            del st.session_state.shuffled_questions
        st.session_state.current_question = 0
        st.session_state.page = "quiz"
        st.rerun()


# --------------------------
# Quiz Page (one question per page)
# --------------------------
elif st.session_state.page == "quiz":

    # Shuffle questions once at the start
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

    # Progress bar
    st.progress((current_index + 1) / total_questions)

    # Display question (without trait name)
    widget_key = f"{trait}_{q_text}"

    # Ensure previous answer is kept if user goes back
    prev_answer = st.session_state.responses.get(widget_key, None)
    response = st.radio(
        q_text,
        ["1 Strongly Disagree", "2 Disagree", "3 Neutral", "4 Agree", "5 Strongly Agree"],
        horizontal=True,
        index=None if prev_answer is None else 
              ["1 Strongly Disagree", "2 Disagree", "3 Neutral", "4 Agree", "5 Strongly Agree"].index(prev_answer),
        key=widget_key
    )
    st.session_state.responses[widget_key] = response

   # Quiz navigation buttons
col1, col2, col3 = st.columns([1, 2, 1])  # adjust ratios if needed

with col1:
    if st.session_state.current_question > 0:
        if st.button("⬅️ Back"):
            st.session_state.current_question -= 1
            st.rerun()

with col2:
    st.empty()  # keeps spacing clean in the middle

with col3:
    if st.session_state.current_question < len(st.session_state.shuffled_questions) - 1:
        if st.button("Next ➡️"):
            st.session_state.current_question += 1
            st.rerun()
    else:
        if st.button("Finish ➡️"):
            st.session_state.page = "results"
            st.rerun()






