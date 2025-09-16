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
# Trait Descriptions (expanded + personalised)
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
# Example Question Data
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
# Quiz State
# --------------------------
if "page" not in st.session_state:
    st.session_state.page = "quiz"
if "responses" not in st.session_state:
    st.session_state.responses = {}

# --------------------------
# Quiz Page
# --------------------------
if st.session_state.page == "quiz":
    st.title("Creative Identity Profile")

    q_index = 0
    for trait, questions in {**creative_traits, **bigfive_traits}.items():
        for q in questions:
            st.radio(
                q,
                ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"],
                key=f"q{q_index}"
            )
            q_index += 1

    if st.button("Submit"):
        st.session_state.page = "results"
        st.experimental_rerun()

# --------------------------
# Results Page
# --------------------------
elif st.session_state.page == "results":
    st.title("Your Results")

    # Fake percentages for demo purposes
    creative_perc = {t: random.randint(20, 95) for t in creative_traits}
    bigfive_perc = {t: random.randint(20, 95) for t in bigfive_traits}

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

    # Archetype section
    st.subheader("Your Archetype")
    sorted_traits = sorted(creative_perc.items(), key=lambda x: x[1], reverse=True)
    top_trait, top_score = sorted_traits[0]
    sub_trait, sub_score = sorted_traits[1]
    st.write(f"**Primary Archetype:** {top_trait} ({top_score}%)")
    st.write(f"**Sub-Archetype:** {sub_trait} ({sub_score}%)")

    # Growth Trait section
    st.subheader("Your Growth Trait")
    all_traits = {**creative_perc, **bigfive_perc}
    lowest_trait = min(all_traits, key=all_traits.get)
    lowest_score = all_traits[lowest_trait]
    st.write(f"**{lowest_trait}:** {lowest_score}%")
    st.write(trait_descriptions[lowest_trait]["low"])
    st.write(f"💡 Growth Tip: {growth_tips[lowest_trait]}")
  
# --------------------------
# Academic Section
# --------------------------
with st.expander("The Science Behind the Creative Identity & Personality Profile"):
    with open("academic_section.txt", "r") as f:
        st.markdown(f.read())

    # PDF Export
    if st.button("Download PDF Report"):
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4)
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
        buffer.seek(0)

        st.download_button(
            label="Download Report",
            data=buffer,
            file_name="creative_identity_profile.pdf",
            mime="application/pdf"
        )

