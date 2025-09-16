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
    Welcome to the **Creative Identity & Personality Profile**.  
    This quiz explores both your **creative traits** and your **Big Five personality traits**.  

    - You’ll answer **33 statements** on a 1–5 scale.  
    - The quiz is based on established research in creativity and psychology.  
    - At the end, you’ll get a personalised profile, archetype, and tips.  
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
    # Radar Charts side by side
    # --------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Big Five Personality Dimensions")
        chart_buf_big5 = radar_chart(bigfive_perc, "Big Five")

    with col2:
        st.subheader("Creative Traits")
        chart_buf_creative = radar_chart(creative_perc, "Creative Traits")

    # --------------------------
    # Archetypes
    # --------------------------
    sorted_traits = sorted(creative_perc.items(), key=lambda x: x[1], reverse=True)
    main_trait, sub_trait, lowest_trait = sorted_traits[0][0], sorted_traits[1][0], sorted_traits[-1][0]

    st.markdown(f"### Main Archetype: {archetypes[main_trait][0]} ({archetypes[main_trait][1]})")
    st.write(f"Your results suggest that {trait_descriptions[main_trait]['high']}")

    st.markdown(f"### Sub-Archetype: {archetypes[sub_trait][0]} ({archetypes[sub_trait][1]})")
    st.write(f"Your profile also shows that {trait_descriptions[sub_trait]['medium']}")

    st.markdown(f"### Growth Area: {lowest_trait}")
    st.write(f"This area may hold you back at times: {trait_descriptions[lowest_trait]['low']}")
    st.write(f"**Growth Tip:** {archetypes[lowest_trait][2]}")

    # --------------------------
    # Personalised Trait Scores
    # --------------------------
    st.subheader("Your Trait Scores")

    def interpret_score(trait, score):
        if score >= 70:
            return f"You scored {score}% in **{trait}**, which suggests {trait_descriptions.get(trait, {}).get('high', 'a strong ability in this area.')}."
        elif score >= 40:
            return f"You scored {score}% in **{trait}**, showing a balanced approach: {trait_descriptions.get(trait, {}).get('medium', 'sometimes strong, sometimes moderate in this area.')}."
        else:
            return f"You scored {score}% in **{trait}**, which suggests {trait_descriptions.get(trait, {}).get('low', 'this may be a weaker area for you.')}"

    all_scores = {**creative_perc, **bigfive_perc}

    for t, p in all_scores.items():
        st.write(interpret_score(t, p))


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

        buf = io.BytesIO()
        fig.savefig(buf, format="PNG")
        buf.seek(0)
        st.pyplot(fig)
        return buf

    # Put charts side by side
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Big Five")
        chart_buf_big5 = radar_chart(bigfive_perc, "Big Five")

    with col2:
        st.subheader("Creative Traits")
        chart_buf_creative = radar_chart(creative_perc, "Creative Traits")


    # --------------------------
    # Archetypes
    # --------------------------
    sorted_traits = sorted(creative_perc.items(), key=lambda x: x[1], reverse=True)
    main_trait, sub_trait, lowest_trait = sorted_traits[0][0], sorted_traits[1][0], sorted_traits[-1][0]

    st.markdown(f"### Main Archetype: {archetypes[main_trait][0]} ({archetypes[main_trait][1]})")
    st.write(trait_descriptions[main_trait]["high"])
    st.write(f"**Growth Tip:** {archetypes[main_trait][2]}")

    st.markdown(f"### Sub-Archetype: {archetypes[sub_trait][0]} ({archetypes[sub_trait][1]})")
    st.write(trait_descriptions[sub_trait]["medium"])
    st.write(f"**Growth Tip:** {archetypes[sub_trait][2]}")

    st.markdown(f"### Growth Area: {lowest_trait}")
    st.write(trait_descriptions[lowest_trait]["low"])
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
        with open("academic_article.txt", "r") as f:
            st.markdown(f.read())


    # --------------------------
    # PDF Generation
    # --------------------------
    def create_pdf():
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    width, height = A4
    margin = 50

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, height - 40, "Creative Identity & Personality Profile")

    # Charts side by side
    img1 = ImageReader(chart_buf_creative)
    img2 = ImageReader(chart_buf_big5)
    chart_size = 200
    spacing = 80
    c.drawImage(img1, margin, height - 280, width=chart_size, height=chart_size)
    c.drawImage(img2, margin + chart_size + spacing, height - 280, width=chart_size, height=chart_size)

    # Move down below charts
    y = height - 320

    # Archetypes & Growth Area
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, "Archetypes and Growth Area")
    y -= 30

    styles = getSampleStyleSheet()
    normal = styles["Normal"]

    def add_wrapped_text(text, y_start):
        frame = Frame(margin, 60, width - 2*margin, y_start - 60, showBoundary=0)
        story = [Paragraph(text, normal)]
        frame.addFromList(story, c)

    # Main Archetype (no growth tip)
    main_text = (
        f"<b>Main Archetype:</b> {archetypes[main_trait][0]} ({archetypes[main_trait][1]})<br/>"
        f"Your results suggest that {trait_descriptions[main_trait]['high']}"
    )
    add_wrapped_text(main_text, y)
    y -= 100

    # Sub-Archetype (no growth tip)
    sub_text = (
        f"<b>Sub-Archetype:</b> {archetypes[sub_trait][0]} ({archetypes[sub_trait][1]})<br/>"
        f"Your profile also shows that {trait_descriptions[sub_trait]['medium']}"
    )
    add_wrapped_text(sub_text, y)
    y -= 100

    # Growth Area (keep growth tip)
    growth_text = (
        f"<b>Growth Area:</b> {lowest_trait}<br/>"
        f"This area may hold you back at times: {trait_descriptions[lowest_trait]['low']}<br/><br/>"
        f"<b>Growth Tip:</b> {archetypes[lowest_trait][2]}"
    )
    add_wrapped_text(growth_text, y)
    y -= 120

    # Trait Scores (personalised only, no growth tips)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, "Your Trait Scores")
    y -= 25

    def interpret_score(trait, score):
        if score >= 70:
            return f"You scored {score}% in {trait}, which suggests {trait_descriptions.get(trait, {}).get('high', 'a strong ability in this area.')}."
        elif score >= 40:
            return f"You scored {score}% in {trait}, showing a balanced approach: {trait_descriptions.get(trait, {}).get('medium', 'sometimes strong, sometimes moderate in this area.')}."
        else:
            return f"You scored {score}% in {trait}, which suggests {trait_descriptions.get(trait, {}).get('low', 'this may be a weaker area for you.')}"

    # Combine all scores
    all_scores = {**creative_perc, **bigfive_perc}

    for t, p in all_scores.items():
        personalised = interpret_score(t, p)
        add_wrapped_text(personalised, y)
        y -= 60
        if y < 100:
            break

    c.save()
    buf.seek(0)
    return buf



    pdf_buf = create_pdf()
    st.download_button("Download Full Report (PDF)", data=pdf_buf, file_name="Creative_Identity_Profile.pdf", mime="application/pdf")
