# app.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
import random
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

st.set_page_config(page_title="Creative Identity Profile", layout="centered")

# --------------------------
# Likert Labels
# --------------------------
likert_labels = {
    1: "1\nStrongly Disagree",
    2: "2\nDisagree",
    3: "3\nNeutral",
    4: "4\nAgree",
    5: "5\nStrongly Agree",
}
likert_short = {
    1: "1 – Strongly Disagree",
    2: "2 – Disagree",
    3: "3 – Neutral",
    4: "4 – Agree",
    5: "5 – Strongly Agree",
}

# --------------------------
# Creative Traits (FULL)
# --------------------------
creative_traits = {
    "Originality": [
        "I often come up with ideas that others don’t think of.",
        "I enjoy finding new ways to solve problems.",
        "I like to put a unique spin on familiar things."
    ],
    "Curiosity": [
        "I enjoy exploring new ideas and perspectives.",
        "I like to imagine possibilities beyond what I know.",
        "I am curious about many different things."
    ],
    "Risk Taking": [
        "I am willing to take risks in my creative work.",
        "I don’t mind uncertainty when trying new approaches.",
        "I experiment with ideas even if they might fail."
    ],
    "Imagination": [
        "I often create vivid mental images or stories.",
        "I enjoy fantasy or thinking about unreal possibilities.",
        "I can picture things in my head easily."
    ],
    "Discipline": [
        "I can focus on my creative projects until they are finished.",
        "I stick with routines that help my creativity.",
        "I put effort into refining and improving my ideas."
    ],
    "Collaboration": [
        "I enjoy sharing ideas with others.",
        "Working with others helps me improve creatively.",
        "I value feedback in developing my ideas."
    ]
}

creative_colors = {
    "Originality": "#1f77b4",
    "Curiosity": "#ff7f0e",
    "Risk Taking": "#2ca02c",
    "Imagination": "#9467bd",
    "Discipline": "#d62728",
    "Collaboration": "#8c564b"
}

creative_summaries = {
    "Originality": {
        "High": "You thrive on bringing new and different ideas.",
        "Medium": "You balance originality with practicality.",
        "Low": "You prefer proven and familiar approaches."
    },
    "Curiosity": {
        "High": "You are deeply inquisitive and open to exploring ideas.",
        "Medium": "You show curiosity but sometimes within limits.",
        "Low": "You prefer to stick to what you know."
    },
    "Risk Taking": {
        "High": "You embrace uncertainty and experimentation.",
        "Medium": "You take chances when they feel manageable.",
        "Low": "You prefer safe and secure approaches."
    },
    "Imagination": {
        "High": "You often create vivid, creative ideas and stories.",
        "Medium": "You sometimes picture possibilities beyond reality.",
        "Low": "You stay grounded in realistic and practical ideas."
    },
    "Discipline": {
        "High": "You stay focused and finish your creative projects.",
        "Medium": "You sometimes balance discipline with flexibility.",
        "Low": "You may struggle with consistency or follow-through."
    },
    "Collaboration": {
        "High": "You thrive in teamwork and value diverse input.",
        "Medium": "You enjoy collaboration but also work well alone.",
        "Low": "You prefer independence in your creative process."
    }
}

# --------------------------
# Archetypes
# --------------------------
archetypes = {
    "Originality": {
        "name": "The Innovator",
        "description": "You generate unique and unconventional ideas.",
        "improvement": "Balance originality with practical application."
    },
    "Curiosity": {
        "name": "The Explorer",
        "description": "You thrive on curiosity and imagination.",
        "improvement": "Focus your curiosity into projects for impact."
    },
    "Risk Taking": {
        "name": "The Adventurer",
        "description": "You embrace uncertainty and bold ideas.",
        "improvement": "Test bold ideas in smaller steps first."
    },
    "Imagination": {
        "name": "The Dreamer",
        "description": "You think in vivid images and possibilities.",
        "improvement": "Ground imagination with real-world testing."
    },
    "Discipline": {
        "name": "The Maker",
        "description": "You bring creative visions to life with structure.",
        "improvement": "Balance productivity with space for play."
    },
    "Collaboration": {
        "name": "The Connector",
        "description": "You spark ideas in groups and value feedback.",
        "improvement": "Balance collaboration with your own vision."
    }
}

# --------------------------
# Big Five Traits (FULL)
# --------------------------
big5_traits = {
    "Openness": [
        "I enjoy trying new activities and experiences.",
        "I have a broad range of interests.",
        "I am curious about many different things."
    ],
    "Conscientiousness": [
        "I like to keep things organized.",
        "I pay attention to details.",
        "I get chores done right away."
    ],
    "Extraversion": [
        "I feel comfortable around people.",
        "I start conversations.",
        "I don’t mind being the center of attention."
    ],
    "Agreeableness": [
        "I am interested in other people’s problems.",
        "I sympathize with others’ feelings.",
        "I take time out for others."
    ],
    "Neuroticism": [
        "I often feel anxious about things.",
        "I get upset easily.",
        "I worry about many things."
    ]
}

big5_colors = {
    "Openness": "#1f77b4",
    "Conscientiousness": "#ff7f0e",
    "Extraversion": "#2ca02c",
    "Agreeableness": "#9467bd",
    "Neuroticism": "#d62728"
}

big5_summaries = {
    "Openness": {
        "High": "You are imaginative and embrace novelty.",
        "Medium": "You balance new experiences with familiarity.",
        "Low": "You prefer tradition and familiar patterns."
    },
    "Conscientiousness": {
        "High": "You are disciplined, structured, and reliable.",
        "Medium": "You balance organization with flexibility.",
        "Low": "You prefer spontaneity over routine."
    },
    "Extraversion": {
        "High": "You gain energy from social interactions.",
        "Medium": "You enjoy people but also value alone time.",
        "Low": "You prefer quiet and independence."
    },
    "Agreeableness": {
        "High": "You are empathetic and value harmony.",
        "Medium": "You cooperate but can be assertive too.",
        "Low": "You are direct and prioritize your own needs."
    },
    "Neuroticism": {
        "High": "You are sensitive to stress and emotions.",
        "Medium": "You manage stress with occasional struggles.",
        "Low": "You are calm and emotionally steady."
    }
}

# --------------------------
# Helpers
# --------------------------
def get_level(score: float) -> str:
    if score >= 4:
        return "High"
    elif score >= 2.5:
        return "Medium"
    else:
        return "Low"

def hex_to_rgb_float(hexcolor: str):
    hexcolor = hexcolor.lstrip("#")
    r = int(hexcolor[0:2], 16) / 255.0
    g = int(hexcolor[2:4], 16) / 255.0
    b = int(hexcolor[4:6], 16) / 255.0
    return (r, g, b)

def radar_chart(scores: dict, colors: dict, title="") -> io.BytesIO:
    labels = list(scores.keys())
    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    values = [scores[l] for l in labels]
    values += values[:1]

    fig, ax = plt.subplots(figsize=(5,5), subplot_kw=dict(polar=True))
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    ax.plot(angles, values, linewidth=1.5, color="black")
    ax.fill(angles, values, alpha=0.05, color="gray")

    for i, trait in enumerate(labels):
        col = colors.get(trait, "#333333")
        ax.plot([angles[i], angles[i+1]], [values[i], values[i+1]],
                color=col, linewidth=3)
        ax.scatter(angles[i], values[i], color=col, s=60, zorder=10)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylim(0,5)
    ax.set_yticks([1,2,3,4,5])
    ax.set_yticklabels(["1","2","3","4","5"])
    plt.title(title, size=12, weight="bold")
    ax.legend(labels, bbox_to_anchor=(1.15, 1.05), fontsize=7)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=150)
    buf.seek(0)
    plt.close(fig)
    return buf

# --------------------------
# PDF Generator (clean)
# --------------------------
def create_pdf(
    creative_scores,
    big5_scores,
    archetypes_results,
    creative_summaries,
    big5_summaries,
    chart_buf_creative,
    chart_buf_big5
):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            rightMargin=40, leftMargin=40,
                            topMargin=50, bottomMargin=40)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="HeadingCenter", parent=styles["Heading1"], alignment=TA_CENTER))
    styles.add(ParagraphStyle(name="TraitHeading", parent=styles["Heading3"], spaceAfter=6))
    styles.add(ParagraphStyle(name="BodyTextCustom", parent=styles["Normal"], leading=14, alignment=TA_LEFT))

    story = []
    story.append(Paragraph("Creative Identity & Personality Profile", styles["HeadingCenter"]))
    story.append(Spacer(1, 20))

    img1 = Image(chart_buf_creative, width=200, height=200)
    img2 = Image(chart_buf_big5, width=200, height=200)
    story.append(img1)
    story.append(Spacer(1, 12))
    story.append(img2)
    story.append(Spacer(1, 20))

    story.append(Paragraph("Your Creative Archetypes", styles["Heading2"]))
    for label, (trait, arch) in archetypes_results.items():
        content = arch["improvement"] if label == "Growth Area" else arch["description"]
        story.append(Paragraph(f"<b>{label}: {arch['name']}</b>", styles["TraitHeading"]))
        story.append(Paragraph(content, styles["BodyTextCustom"]))
        story.append(Spacer(1, 12))

    story.append(Paragraph("Creative Trait Insights", styles["Heading2"]))
    for trait, score in creative_scores.items():
        level = get_level(score)
        story.append(Paragraph(f"<b>{trait} ({level}) — {score:.2f}/5</b>", styles["TraitHeading"]))
        story.append(Paragraph(creative_summaries[trait][level], styles["BodyTextCustom"]))
        story.append(Spacer(1, 10))

    story.append(Paragraph("Big Five Trait Insights", styles["Heading2"]))
    for trait, score in big5_scores.items():
        level = get_level(score)
        story.append(Paragraph(f"<b>{trait} ({level}) — {score:.2f}/5</b>", styles["TraitHeading"]))
        story.append(Paragraph(big5_summaries[trait][level], styles["BodyTextCustom"]))
        story.append(Spacer(1, 10))

    doc.build(story)
    buf.seek(0)
    return buf.getvalue()

# --------------------------
# Streamlit App
# --------------------------
st.title("Creative Identity & Personality Profile")

if "current_q" not in st.session_state:
    st.session_state.current_q = 0

if "all_questions" not in st.session_state:
    all_questions = []
    for trait, qs in {**creative_traits, **big5_traits}.items():
        for q in qs:
            all_questions.append((trait, q))
    random.shuffle(all_questions)
    st.session_state.all_questions = all_questions

if "responses" not in st.session_state:
    st.session_state.responses = {}

all_questions = st.session_state.all_questions
responses = st.session_state.responses
current_q = st.session_state.current_q
total_qs = len(all_questions)

# --------------------------
# Question Pages
# --------------------------
if current_q < total_qs:
    if current_q == 0:
        st.markdown("## Welcome to the Creative Identity Quiz")
        st.markdown(
            "This quiz explores your **creative traits** and **personality dimensions**. "
            "Please rate each statement on a 1–5 scale: 1 = Strongly Disagree … 5 = Strongly Agree. "
            "Answer honestly – there are no right or wrong answers!"
        )
        st.divider()

    trait, question = all_questions[current_q]
    key = f"{trait}_{current_q}"
    st.markdown(f"**Q{current_q+1}/{total_qs}:** {question}")

    cols = st.columns(5)
    for i, col in enumerate(cols, start=1):
        button_key = f"{key}_btn{i}"
        if col.button(likert_labels[i], key=button_key, use_container_width=True):
            responses[key] = i
            st.session_state.responses = responses
            st.rerun()

    if key in responses and responses[key] is not None:
        st.markdown(f"✅ You selected: **{likert_short[responses[key]]}**")
    else:
        st.markdown("_Please choose an option above to continue._")

    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("Back", disabled=(current_q == 0)):
            st.session_state.current_q -= 1
            st.rerun()
    with col2:
        answered = key in responses and responses[key] is not None
        if st.button("Next Question", disabled=not answered):
            st.session_state.current_q += 1
            st.rerun()

# --------------------------
# Results Page
# --------------------------
else:
    st.success("All questions complete — here are your results!")

    creative_scores = {t:0 for t in creative_traits}
    creative_counts = {t:0 for t in creative_traits}
    big5_scores = {t:0 for t in big5_traits}
    big5_counts = {t:0 for t in big5_traits}

    for key, val in responses.items():
        if val:
            trait = key.split("_")[0]
            if trait in creative_scores:
                creative_scores[trait] += val
                creative_counts[trait] += 1
            if trait in big5_scores:
                big5_scores[trait] += val
                big5_counts[trait] += 1

    for t in creative_scores:
        creative_scores[t] = creative_scores[t] / creative_counts[t] if creative_counts[t] > 0 else 0.0
    for t in big5_scores:
        big5_scores[t] = big5_scores[t] / big5_counts[t] if big5_counts[t] > 0 else 0.0

    c1, c2 = st.columns(2)
    chart_buf_creative = radar_chart(creative_scores, creative_colors, "Creative Traits")
    chart_buf_big5 = radar_chart(big5_scores, big5_colors, "Big Five Traits")
    with c1:
        st.image(chart_buf_creative, use_container_width=True)
    with c2:
        st.image(chart_buf_big5, use_container_width=True)

    sorted_traits = sorted(creative_scores.items(), key=lambda x: x[1], reverse=True)
    if len(sorted_traits) >= 3:
        main_trait, sub_trait, weakest_trait = sorted_traits[0][0], sorted_traits[1][0], sorted_traits[-1][0]
    else:
        keys = list(creative_traits.keys())
        main_trait, sub_trait, weakest_trait = keys[0], keys[1], keys[-1]

    st.subheader("Your Creative Archetypes")
    archetypes_info = {}
    for label, trait in [("Main Archetype", main_trait), ("Sub-Archetype", sub_trait), ("Growth Area", weakest_trait)]:
        content = archetypes[trait]["improvement"] if label == "Growth Area" else archetypes[trait]["description"]
        archetypes_info[label] = (trait, archetypes[trait])
        st.markdown(
            f"<div style='background-color:{creative_colors[trait]}20; padding:0.7rem; border-radius:10px; margin:0.7rem 0;'>"
            f"<span style='color:{creative_colors[trait]}; font-weight:bold'>{label}: {archetypes[trait]['name']}</span><br>"
            f"<i>{content}</i></div>", unsafe_allow_html=True
        )

    st.subheader("Creative Trait Insights")
    for trait, score in creative_scores.items():
        level = get_level(score)
        summary = creative_summaries[trait][level]
        st.markdown(
            f"<div style='background-color:{creative_colors[trait]}20; padding:0.5rem; border-radius:8px; margin:0.5rem 0;'>"
            f"<span style='color:{creative_colors[trait]}; font-weight:bold'>{trait} ({level})</span> — {score:.2f}/5<br>"
            f"<i>{summary}</i></div>", unsafe_allow_html=True
        )

    st.subheader("Big Five Trait Insights")
    for trait, score in big5_scores.items():
        level = get_level(score)
        summary = big5_summaries[trait][
