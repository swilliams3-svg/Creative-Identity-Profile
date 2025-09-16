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
# Creative Traits
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
# Big Five Traits
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

# Use a different palette so they don’t look linked to Creative traits
big5_colors = {
    "Openness": "#17becf",
    "Conscientiousness": "#bcbd22",
    "Extraversion": "#e377c2",
    "Agreeableness": "#7f7f7f",
    "Neuroticism": "#ff9896"
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
# PDF Report Generator
# --------------------------
def create_pdf(creative_scores, big5_scores, archetypes_results,
               creative_summaries, big5_summaries,
               chart_buf_creative, chart_buf_big5):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
    from reportlab.lib import colors

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40, leftMargin=40,
        topMargin=50, bottomMargin=40
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="CenterTitle", alignment=1, fontSize=16, spaceAfter=12))
    styles.add(ParagraphStyle(name="SectionHeading", fontSize=13, spaceAfter=8, textColor=colors.HexColor("#333333")))
    styles.add(ParagraphStyle(name="BodyText", fontSize=10, leading=14))

    story = []

    # Title
    story.append(Paragraph("Creative Identity Profile", styles["CenterTitle"]))
    story.append(Spacer(1, 12))

    # --- Creative Traits Section ---
    story.append(Paragraph("Creative Traits", styles["SectionHeading"]))
    for trait, score in creative_scores.items():
        level = get_level(score)
        summary = creative_summaries[trait][level]
        story.append(Paragraph(f"<b>{trait}</b>: {score:.1f} ({level})", styles["BodyText"]))
        story.append(Paragraph(summary, styles["BodyText"]))
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 12))
    story.append(Image(chart_buf_creative, width=250, height=250))
    story.append(Spacer(1, 12))

    # --- Big Five Section ---
    story.append(Paragraph("Big Five Personality Traits", styles["SectionHeading"]))
    for trait, score in big5_scores.items():
        level = get_level(score)
        summary = big5_summaries[trait][level]
        story.append(Paragraph(f"<b>{trait}</b>: {score:.1f} ({level})", styles["BodyText"]))
        story.append(Paragraph(summary, styles["BodyText"]))
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 12))
    story.append(Image(chart_buf_big5, width=250, height=250))
    story.append(Spacer(1, 12))

    # --- Archetypes ---
    story.append(Paragraph("Creative Archetypes", styles["SectionHeading"]))
    for arch, desc in archetypes_results.items():
        story.append(Paragraph(f"<b>{arch}</b>: {desc}", styles["BodyText"]))
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 12))

    # --- Academic Background Section ---
    story.append(Paragraph("The Science Behind the Quiz", styles["SectionHeading"]))
    academic_text = """
    This quiz is informed by established research in creativity and psychology.
    It integrates <b>divergent and convergent thinking</b> (Guilford, 1950), 
    <b>the Big Five personality model</b> (McCrae & Costa, 1999), 
    and <b>creative identity frameworks</b> (Amabile, 1996; Sternberg, 2006).
    Divergent thinking reflects the ability to generate multiple ideas, 
    while convergent thinking involves evaluating and refining ideas.
    Both are essential components of the creative process.
    """
    story.append(Paragraph(academic_text, styles["BodyText"]))
    story.append(Spacer(1, 12))

    doc.build(story)
    buffer.seek(0)
    return buffer

# --------------------------
# Streamlit App Navigation
# --------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Quiz", "Results"])
# --------------------------
# Results Page
# --------------------------
if page == "Results":
    st.title("✨ Your Creative Identity Profile")

    # --- Calculate Scores (placeholder values for demo) ---
    creative_scores = {trait: np.random.uniform(1, 5) for trait in creative_traits.keys()}
    big5_scores = {trait: np.random.uniform(1, 5) for trait in big5_traits.keys()}
    archetypes_results = {
        "Explorer": "You thrive on novelty and discovery.",
        "Innovator": "You enjoy creating unique solutions.",
        "Visionary": "You imagine future possibilities."
    }

    # --- Generate Charts ---
    chart_buf_creative = radar_chart(creative_scores, creative_colors, "Creative Traits")
    chart_buf_big5 = radar_chart(big5_scores, big5_colors, "Big Five Traits")

    # --- Display Results ---
    st.subheader("Creative Traits")
    st.image(chart_buf_creative)

    for trait, score in creative_scores.items():
        level = get_level(score)
        summary = creative_summaries[trait][level]
        st.markdown(f"**{trait}:** {score:.1f} ({level})")
        st.write(summary)

    st.subheader("Big Five Traits")
    st.image(chart_buf_big5)

    for trait, score in big5_scores.items():
        level = get_level(score)
        summary = big5_summaries[trait][level]
        st.markdown(f"**{trait}:** {score:.1f} ({level})")
        st.write(summary)

    st.subheader("Creative Archetypes")
    for arch, desc in archetypes_results.items():
        st.markdown(f"**{arch}:** {desc}")

    # --- Generate PDF ---
    pdf_buf = create_pdf(
        creative_scores,
        big5_scores,
        archetypes_results,
        creative_summaries,
        big5_summaries,
        chart_buf_creative,
        chart_buf_big5
    )

    # --- Collapsible Report Section ---
    with st.expander("📄 View Your Full Report", expanded=False):
        st.write(
            "Here is your personalised **Creative Identity Profile**. "
            "You can preview the results above and download a professional PDF report below."
        )

        st.download_button(
            label="📥 Download Your Report",
            data=pdf_buf.getvalue(),  # must be bytes
            file_name="creative_identity_profile.pdf",
            mime="application/pdf"
        )
