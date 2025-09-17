import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
import random
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO

st.set_page_config(page_title="Creative Identity Profile", layout="centered")

# --------------------------
# Academic PDF function
# --------------------------
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
trait_descriptions = { ... }  # Keep your existing descriptions here

# --------------------------
# Archetypes
# --------------------------
archetypes = { ... }  # Keep your existing archetypes here

# --------------------------
# Shared Button Styling
# --------------------------
gradients = [
    "linear-gradient(90deg, #7b2ff7, #f107a3)",
    "linear-gradient(90deg, #06beb6, #48b1bf)",
    "linear-gradient(90deg, #ff6a00, #ee0979)",
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
    st.markdown("Welcome to the **Creative Identity & Personality Profile**. This short self-reflection quiz combines insights from creativity research and the **Big Five personality framework**.")
    if st.button("Start Quiz", key="start_quiz"):
        st.session_state.responses = {}
        if "shuffled_questions" in st.session_state:
            del st.session_state.shuffled_questions
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

    # Navigation buttons aligned
    col1, col2, col3, col4 = st.columns([1, 3, 0.5, 1])
    with col1:
        if st.session_state.current_question > 0:
            if st.button("⬅️ Back"):
                st.session_state.current_question -= 1
                st.rerun()
    with col2: st.empty()
    with col3:
        if st.session_state.current_question < total_questions - 1:
            if st.button("Next ➡️"):
                st.session_state.current_question += 1
                st.rerun()
        else:
            if st.button("Finish ➡️"):
                st.session_state.page = "results"
                st.rerun()
    with col4: st.empty()

elif st.session_state.page == "results":
    st.title("Your Creative Identity Profile")

    # --------------------------
    # Calculate Scores
    # --------------------------
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
    # Radar Chart Function
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
        plt.close(fig)
        return buf

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Creative Traits")
        chart_buf_creative = radar_chart(creative_perc, "Creative Traits")
    with col2:
        st.subheader("Big Five")
        chart_buf_big5 = radar_chart(bigfive_perc, "Big Five")

    # --------------------------
    # Archetypes Cards
    # --------------------------
    sorted_traits = sorted(creative_perc.items(), key=lambda x: x[1], reverse=True)
    top_trait, sub_trait, lowest_trait = sorted_traits[0][0], sorted_traits[1][0], sorted_traits[-1][0]
    top_score, sub_score, low_score = sorted_traits[0][1], sorted_traits[1][1], sorted_traits[-1][1]

    def archetype_card(trait, title, description, tip):
        color = palette.get(trait, "#7b2ff7")  # fallback purple
        return f"""
        <div style="
            background: {color};
            padding: 1.2em;
            border-radius: 12px;
            margin-bottom: 1.2em;
            text-align: left;
            color: white;
            font-size: 16px;
            font-weight: normal;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
        ">
            <h3 style="margin-top:0; font-size:20px; font-weight:bold;">{title}</h3>
            <p style="margin:0.4em 0;">{description}</p>
            <p style="margin:0.4em 0;"><b>Growth Tip:</b> {tip}</p>
        </div>
        """

    # Primary Archetype
    if top_score >= 67:
        desc = trait_descriptions[top_trait]["high"]
    elif top_score >= 34:
        desc = trait_descriptions[top_trait]["medium"]
    else:
        desc = trait_descriptions[top_trait]["low"]

    st.markdown(archetype_card(
        top_trait,
        f"🌟 Primary Archetype: {archetypes[top_trait][0]} ({archetypes[top_trait][1]})",
        desc,
        archetypes[top_trait][2]
    ), unsafe_allow_html=True)

    # Sub-Archetype
    if sub_score >= 67:
        desc = trait_descriptions[sub_trait]["high"]
    elif sub_score >= 34:
        desc = trait_descriptions[sub_trait]["medium"]
    else:
        desc = trait_descriptions[sub_trait]["low"]

    st.markdown(archetype_card(
        sub_trait,
        f"✨ Sub-Archetype: {archetypes[sub_trait][0]} ({archetypes[sub_trait][1]})",
        desc,
        archetypes[sub_trait][2]
    ), unsafe_allow_html=True)

    # Growth Area
    st.markdown(archetype_card(
        lowest_trait,
        f"🌱 Growth Area: {lowest_trait}",
        trait_descriptions[lowest_trait]["low"],
        archetypes[lowest_trait][2]
    ), unsafe_allow_html=True)

    # --------------------------
    # Trait Scores List
    # --------------------------
    st.subheader("Your Trait Scores")
    for t, p in creative_perc.items():
        st.write(f"**{t}:** {p}%")
        if p >= 67:
            st.write(trait_descriptions[t]["high"])
        elif p >= 34:
            st.write(trait_descriptions[t]["medium"])
        else:
            st.write(trait_descriptions[t]["low"])

    for t, p in bigfive_perc.items():
        st.write(f"**{t}:** {p}%")
        if p >= 67:
            st.write(trait_descriptions[t]["high"])
        elif p >= 34:
            st.write(trait_descriptions[t]["medium"])
        else:
            st.write(trait_descriptions[t]["low"])

    # --------------------------
    # Academic PDF Download
    # --------------------------
    st.markdown("### Academic Research")
    st.markdown("You can download the full academic background behind this quiz as a PDF:")

    academic_pdf = create_academic_pdf()
    st.download_button(
        "Download Academic PDF",
        data=academic_pdf,
        file_name="academic_research.pdf",
        mime="application/pdf",
    )

