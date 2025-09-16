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
    "Curiosity": "#6D9DC5",
    "Imagination": "#A267AC",
    "Openness": "#05668D",
    "Conscientiousness": "#88AB75",
    "Extraversion": "#E2C044",
    "Agreeableness": "#5E60CE",
    "Neuroticism": "#C44536"
}

# --------------------------
# Expanded Trait Descriptions
# --------------------------
trait_descriptions = {
    "Curiosity": {
        "high": "You are deeply curious and thrive on exploring new ideas, concepts, and experiences. You actively seek novelty and are energized by learning opportunities.",
        "medium": "You are moderately curious, enjoying new ideas when they arise but also comfortable with the familiar.",
        "low": "You prefer predictability and routine, and you may be less motivated by novelty or new experiences."
    },
    "Imagination": {
        "high": "Your imagination is vivid and expansive. You enjoy creative problem-solving, storytelling, and envisioning new possibilities.",
        "medium": "You use your imagination when needed but often balance it with practicality.",
        "low": "You rely more on concrete facts and practical approaches, preferring realistic thinking over abstract ideas."
    },
    "Openness": {
        "high": "You are highly open to new experiences, perspectives, and ways of thinking. You embrace diversity and are comfortable with change.",
        "medium": "You are somewhat open — you enjoy some new ideas and experiences but balance them with familiarity.",
        "low": "You prefer stability, routine, and familiar approaches, and may resist change or unconventional ideas."
    },
    "Conscientiousness": {
        "high": "You are highly organized, disciplined, and dependable. You take commitments seriously and follow through on tasks.",
        "medium": "You are reasonably conscientious, balancing structure with flexibility.",
        "low": "You prefer a relaxed approach to life, may dislike rigid schedules, and value freedom over structure."
    },
    "Extraversion": {
        "high": "You are outgoing, sociable, and energized by being around people. You thrive in group settings and enjoy engaging with others.",
        "medium": "You enjoy social interaction but also value quiet time to recharge.",
        "low": "You are more reserved, preferring meaningful one-on-one interactions or solitude over large groups."
    },
    "Agreeableness": {
        "high": "You are warm, compassionate, and cooperative. You value harmony and prioritize others’ needs alongside your own.",
        "medium": "You balance your own needs with those of others, showing kindness while maintaining boundaries.",
        "low": "You are more assertive and direct, often prioritizing honesty and goals over pleasing others."
    },
    "Neuroticism": {
        "high": "You experience emotions intensely and may be sensitive to stress. This sensitivity can bring self-awareness and depth to your perspective.",
        "medium": "You sometimes feel stress or negative emotions but generally cope well.",
        "low": "You are calm, emotionally stable, and resilient under pressure, rarely feeling overwhelmed."
    }
}

growth_tips = {
    "Curiosity": "Try asking more open-ended questions in conversations or reading about a topic outside your usual interests.",
    "Imagination": "Engage in creative activities such as drawing, writing, or brainstorming wild ideas without judgment.",
    "Openness": "Challenge yourself by trying something new each week — a food, activity, or perspective.",
    "Conscientiousness": "Set small, achievable goals and celebrate progress to build momentum.",
    "Extraversion": "Push yourself to engage in one more social activity than usual this week.",
    "Agreeableness": "Practice active listening and empathy in conversations to strengthen connections.",
    "Neuroticism": "Experiment with mindfulness or journaling to manage stress more effectively."
}

# --------------------------
# Traits & Questions
# --------------------------
creative_traits = {
    "Curiosity": [
        "I enjoy exploring new ideas and perspectives.",
        "I actively seek out new experiences.",
        "I like to ask questions to deepen my understanding."
    ],
    "Imagination": [
        "I enjoy daydreaming or imagining possibilities.",
        "I can easily visualize things in my mind.",
        "I like thinking about things that don’t yet exist."
    ]
}

bigfive_traits = {
    "Openness": [
        "I am open to trying new experiences.",
        "I enjoy reflecting on abstract concepts.",
        "I like exploring new and unusual ideas."
    ],
    "Conscientiousness": [
        "I follow through on my commitments.",
        "I like to keep things organized.",
        "I work hard to achieve my goals."
    ],
    "Extraversion": [
        "I feel energized by being around people.",
        "I enjoy group conversations and activities.",
        "I like to be the center of attention."
    ],
    "Agreeableness": [
        "I value cooperation and harmony.",
        "I am considerate of others' feelings.",
        "I try to avoid conflict when possible."
    ],
    "Neuroticism": [
        "I often feel anxious or stressed.",
        "I worry about things going wrong.",
        "I find it hard to stay calm under pressure."
    ]
}

# --------------------------
# Radar Chart Function
# --------------------------
def radar_chart(data, title):
    labels = list(data.keys())
    values = list(data.values())
    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(polar=True))
    ax.fill(angles, values, alpha=0.25)
    ax.plot(angles, values, linewidth=2)

    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_title(title, size=14, weight='bold', pad=20)

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)
    return buf

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

    - You’ll answer statements on a 1–5 scale.  
    - The quiz is based on established research in creativity and psychology.  
    - At the end, you’ll get a personalised profile, archetype, and growth insights.  
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
    for trait, qs in {**creative_traits, **bigfive_traits}.items():
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
        for t, qs in bigfive_traits.items()
    }

    creative_perc = {t: round((s - 1) / 4 * 100) for t, s in creative_scores.items()}
    bigfive_perc = {t: round((s - 1) / 4 * 100) for t, s in bigfive_scores.items()}

    # Radar charts side by side
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Big Five Personality Dimensions")
        chart_buf_big5 = radar_chart(bigfive_perc, "Big Five")
        st.image(chart_buf_big5)
    with col2:
        st.subheader("Creative Traits")
        chart_buf_creative = radar_chart(creative_perc, "Creative Traits")
        st.image(chart_buf_creative)

    # Trait scores + descriptors
    st.subheader("Your Trait Scores")

    st.markdown("#### Creative Traits")
    for t, p in creative_perc.items():
        st.write(f"**{t}:** {p}%")
        if p >= 67:
            st.write(trait_descriptions[t]["high"])
        elif p >= 34:
            st.write(trait_descriptions[t]["medium"])
        else:
            st.write(trait_descriptions[t]["low"])

    st.markdown("#### Big Five Personality Dimensions")
    for t, p in bigfive_perc.items():
        st.write(f"**{t}:** {p}%")
        if p >= 67:
            st.write(trait_descriptions[t]["high"])
        elif p >= 34:
            st.write(trait_descriptions[t]["medium"])
        else:
            st.write(trait_descriptions[t]["low"])

    # Archetype + Growth Trait
    st.subheader("Your Archetype & Growth Trait")
    sorted_traits = sorted(creative_perc.items(), key=lambda x: x[1], reverse=True)
    top_trait, top_score = sorted_traits[0]
    sub_trait, sub_score = sorted_traits[1]
    st.write(f"**Primary Archetype:** {top_trait} ({top_score}%)")
    st.write(f"**Sub-Archetype:** {sub_trait} ({sub_score}%)")

    all_traits = {**creative_perc, **bigfive_perc}
    lowest_trait = min(all_traits, key=all_traits.get)
    lowest_score = all_traits[lowest_trait]
    st.markdown(f"**Growth Trait:** {lowest_trait} ({lowest_score}%)")
    st.write(trait_descriptions[lowest_trait]["low"])
    st.write(f"💡 Growth Tip: {growth_tips[lowest_trait]}")

    # Academic Section
    with st.expander("The Science Behind the Creative Identity & Personality Profile"):
        with open("academic_article.txt", "r") as f:
            st.markdown(f.read())

    # PDF Export
    def create_pdf():
        buf = io.BytesIO()
        pdf = canvas.Canvas(buf, pagesize=A4)
        width, height = A4

        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(50, height - 50, "Creative Identity Profile Report")

        y = height - 100
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y, "Creative Traits")
        pdf.setFont("Helvetica", 10)
        y -= 20
        for t, p in creative_perc.items():
            pdf.drawString(50, y, f"{t}: {p}%")
            y -= 15
            if p >= 67:
                text = trait_descriptions[t]["high"]
            elif p >= 34:
                text = trait_descriptions[t]["medium"]
            else:
                text = trait_descriptions[t]["low"]
            for line in text.split(". "):
                pdf.drawString(70, y, line.strip())
                y -= 15

        y -= 20
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y, "Big Five Personality Dimensions")
        pdf.setFont("Helvetica", 10)
        y -= 20
        for t, p in bigfive_perc.items():
            pdf.drawString(50, y, f"{t}: {p}%")
            y -= 15
            if p >= 67:
                text = trait_descriptions[t]["high"]
            elif p >= 34:
                text = trait_descriptions[t]["medium"]
            else:
                text = trait_descriptions[t]["low"]
            for line in text.split(". "):
                pdf.drawString(70, y, line.strip())
                y -= 15

        y -= 20
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y, "Growth Trait")
        pdf.setFont("Helvetica", 10)
        y -= 20
        pdf.drawString(50, y, f"{lowest_trait}: {lowest_score}%")
        y -= 15
        for line in trait_descriptions[lowest_trait]["low"].split(". "):
            pdf.drawString(70, y, line.strip())
            y -= 15
        pdf.drawString(70, y, f"Growth Tip: {growth_tips[lowest_trait]}")

        pdf.save()
        buf.seek(0)
        return buf

    pdf_buf = create_pdf()
    st.download_button("Download Full Report (PDF)", data=pdf_buf, file_name="Creative_Identity_Profile.pdf", mime="application/pdf")

