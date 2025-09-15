import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
import random
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

st.set_page_config(page_title="Creative Identity Profile", layout="centered")

# --------------------------
# Traits & Questions
# --------------------------
creative_traits = {
    "Openness": [
        "I enjoy exploring new ideas and perspectives.",
        "I like to imagine possibilities beyond what I know.",
        "I am curious about many different things."
    ],
    "Risk-taking": [
        "I am willing to take risks in my creative work.",
        "I don’t mind uncertainty when trying new approaches.",
        "I experiment with ideas even if they might fail."
    ],
    "Resilience": [
        "I keep trying even after setbacks in creative tasks.",
        "I can adapt when my ideas don’t work as planned.",
        "I learn from mistakes and keep moving forward."
    ],
    "Collaboration": [
        "I enjoy sharing ideas with others.",
        "Working with others helps me improve creatively.",
        "I value feedback in developing my ideas."
    ],
    "Divergent Thinking": [
        "I can come up with many different ideas for a problem.",
        "I enjoy brainstorming unusual or original solutions.",
        "I think of multiple ways to use common objects."
    ],
    "Convergent Thinking": [
        "I can narrow down options to find the best idea.",
        "I enjoy refining and improving ideas.",
        "I evaluate which solutions are most effective."
    ]
}

big5_traits = {
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
    ],
    "Openness": [   # Big Five Openness
        "I enjoy trying new activities and experiences.",
        "I have a broad range of interests.",
        "I am curious about many different things."
    ]
}

creative_colors = {
    "Openness": "#1f77b4",
    "Risk-taking": "#ff7f0e",
    "Resilience": "#2ca02c",
    "Collaboration": "#9467bd",
    "Divergent Thinking": "#d62728",
    "Convergent Thinking": "#8c564b"
}

big5_colors = {
    "Conscientiousness": "#ff7f0e",
    "Extraversion": "#2ca02c",
    "Agreeableness": "#9467bd",
    "Neuroticism": "#d62728",
    "Openness": "#1f77b4"
}

creative_summaries = {
    "Openness": {
        "High": "You thrive on imagination and curiosity.",
        "Medium": "You balance curiosity with focus and practicality.",
        "Low": "You prefer familiar ideas and structured approaches."
    },
    "Risk-taking": {
        "High": "You embrace uncertainty and new experiences.",
        "Medium": "You take chances when the stakes feel right.",
        "Low": "You prefer safer choices and calculated steps."
    },
    "Resilience": {
        "High": "You bounce back quickly and learn from setbacks.",
        "Medium": "You recover from challenges with some effort.",
        "Low": "You may find setbacks discouraging but can grow with support."
    },
    "Collaboration": {
        "High": "You thrive in teamwork and draw on diverse ideas.",
        "Medium": "You enjoy working with others but also value independence.",
        "Low": "You prefer to work solo and rely on your own vision."
    },
    "Divergent Thinking": {
        "High": "You generate many original and unusual ideas.",
        "Medium": "You can think of multiple solutions, though sometimes within bounds.",
        "Low": "You prefer straightforward solutions and focus on clarity."
    },
    "Convergent Thinking": {
        "High": "You excel at refining ideas and making decisions.",
        "Medium": "You balance idea generation with structured evaluation.",
        "Low": "You may struggle with narrowing options and making choices."
    }
}

big5_summaries = {
    "Conscientiousness": {
        "High": "You are disciplined, structured, and value order.",
        "Medium": "You balance organization with flexibility.",
        "Low": "You prefer spontaneity and may avoid strict routines."
    },
    "Extraversion": {
        "High": "You gain energy from social interaction.",
        "Medium": "You enjoy company but also value alone time.",
        "Low": "You prefer quiet environments and independence."
    },
    "Agreeableness": {
        "High": "You are empathetic and value harmony with others.",
        "Medium": "You can be cooperative but also assertive when needed.",
        "Low": "You are direct and prioritize your own views."
    },
    "Neuroticism": {
        "High": "You are sensitive to stress and emotions.",
        "Medium": "You experience occasional stress but manage it.",
        "Low": "You are calm, stable, and less affected by stress."
    },
    "Openness": {
        "High": "You are imaginative and embrace new experiences.",
        "Medium": "You enjoy some novelty but also value familiarity.",
        "Low": "You prefer tradition and familiar ways of thinking."
    }
}

archetypes = {
    "Openness": {"name": "The Explorer", "description": "You thrive on curiosity and imagination.", "improvement": "Capture ideas after exploration sprints."},
    "Risk-taking": {"name": "The Adventurer", "description": "You embrace uncertainty and push boundaries.", "improvement": "Test risky ideas in small steps."},
    "Resilience": {"name": "The Perseverer", "description": "You persist through challenges and learn from failure.", "improvement": "Reflect on lessons and note wins."},
    "Collaboration": {"name": "The Connector", "description": "You spark ideas in groups and value perspectives.", "improvement": "Balance collaboration with solo time."},
    "Divergent Thinking": {"name": "The Visionary", "description": "You generate many original ideas.", "improvement": "Rank and refine your best ideas."},
    "Convergent Thinking": {"name": "The Strategist", "description": "You refine and structure ideas into action.", "improvement": "Loosen constraints sometimes for novelty."}
}

# --------------------------
# Helpers
# --------------------------
def get_level(score: float) -> str:
    if score >= 4: return "High"
    elif score >= 2.5: return "Medium"
    else: return "Low"

def radar_chart(scores: dict, colors: dict, title="") -> io.BytesIO:
    labels = list(scores.keys())
    num_vars = len(labels)
    angles = np.linspace(0, 2*np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]
    values = list(scores.values())
    values += values[:1]
    fig, ax = plt.subplots(figsize=(5,5), subplot_kw=dict(polar=True))
    ax.plot(angles, values, color="black", linewidth=1.5)
    ax.fill(angles, values, color="gray", alpha=0.1)
    for i, (trait, score) in enumerate(scores.items()):
        ax.scatter(angles[i], score, color=colors[trait], s=60, zorder=10, label=trait)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylim(0,5)
    ax.set_yticks([1,2,3,4,5])
    ax.set_yticklabels(["1","2","3","4","5"])
    plt.title(title, size=11, weight="bold")
    ax.legend(bbox_to_anchor=(1.1, 1.05), fontsize=7)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)
    return buf

def create_pdf(creative_scores, big5_scores, main_trait, sub_trait, weakest_trait):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    width, height = A4
    y = height - inch
    c.setFont("Helvetica-Bold", 16)
    c.drawString(inch, y, "Creative Identity & Personality Profile")
    y -= 0.5*inch
    c.setFont("Helvetica", 12)
    for trait, score in creative_scores.items():
        level = get_level(score)
        c.drawString(inch, y, f"{trait}: {score:.2f}/5 ({level})")
        y -= 0.3*inch
    y -= 0.2*inch
    for trait, score in big5_scores.items():
        level = get_level(score)
        c.drawString(inch, y, f"{trait}: {score:.2f}/5 ({level})")
        y -= 0.3*inch
    y -= 0.5*inch
    c.setFont("Helvetica-Bold", 14)
    c.drawString(inch, y, f"Main Archetype: {archetypes[main_trait]['name']}")
    y -= 0.3*inch
    c.setFont("Helvetica", 12)
    c.drawString(inch, y, archetypes[main_trait]["description"])
    y -= 0.5*inch
    c.setFont("Helvetica-Bold", 14)
    c.drawString(inch, y, f"Sub-Archetype: {archetypes[sub_trait]['name']}")
    y -= 0.3*inch
    c.setFont("Helvetica", 12)
    c.drawString(inch, y, archetypes[sub_trait]["description"])
    y -= 0.5*inch
    c.setFont("Helvetica-Bold", 14)
    c.drawString(inch, y, f"Growth Area: {archetypes[weakest_trait]['name']}")
    y -= 0.3*inch
    c.setFont("Helvetica", 12)
    c.drawString(inch, y, archetypes[weakest_trait]["improvement"])
    c.showPage()
    c.save()
    buf.seek(0)
    return buf

# --------------------------
# App State
# --------------------------
if "page" not in st.session_state: st.session_state.page = 0
if "responses" not in st.session_state: st.session_state.responses = {}

all_questions = []
for trait, qs in {**creative_traits, **big5_traits}.items():
    for q in qs: all_questions.append((trait, q))
total_qs = len(all_questions)

# --------------------------
# UI Flow
# --------------------------
st.title("Creative Identity & Personality Profile")

page = st.session_state.page
responses = st.session_state.responses

if page < total_qs:
    st.markdown("Please rate each statement on a 1–5 scale: **1 = Strongly Disagree · 5 = Strongly Agree**")
    trait, question = all_questions[page]
    st.subheader(f"Question {page+1} of {total_qs}")
    resp_key = f"resp_{page}"
    responses[resp_key] = st.radio(
        question, [1,2,3,4,5],
        horizontal=True,
        key=resp_key,
        index=(responses.get(resp_key, 0)-1) if responses.get(resp_key) else 0
    )
    col1, col2 = st.columns([1,1])
    with col1:
        if page > 0 and st.button("Back"):
            st.session_state.page -= 1
            st.rerun()
    with col2:
        if responses[resp_key]:
            if st.button("Next Question"):
                st.session_state.page += 1
                st.rerun()
    answered = sum(v is not None for v in responses.values())
    st.progress(answered/total_qs)

else:
    st.subheader("✅ All questions complete — here are your results!")
    # Scores
    creative_scores = {t:0 for t in creative_traits}
    creative_counts = {t:0 for t in creative_traits}
    big5_scores = {t:0 for t in big5_traits}
    big5_counts = {t:0 for t in big5_traits}
    for i,(trait,_) in enumerate(all_questions):
        val = responses.get(f"resp_{i}")
        if val:
            if trait in creative_scores:
                creative_scores[trait]+=val; creative_counts[trait]+=1
            if trait in big5_scores:
                big5_scores[trait]+=val; big5_counts[trait]+=1
    for t in creative_scores: creative_scores[t]/=creative_counts[t]
    for t in big5_scores: big5_scores[t]/=big5_counts[t]

    c1,c2 = st.columns(2)
    with c1: st.image(radar_chart(creative_scores, creative_colors, "Creative Traits"), use_container_width=True)
    with c2: st.image(radar_chart(big5_scores, big5_colors, "Big Five Traits"), use_container_width=True)

    sorted_traits = sorted(creative_scores.items(), key=lambda x:x[1], reverse=True)
    main_trait, sub_trait, weakest_trait = sorted_traits[0][0], sorted_traits[1][0], sorted_traits[-1][0]

    st.subheader("Your Creative Archetypes")
    for label, trait in [("Main Archetype", main_trait), ("Sub-Archetype", sub_trait), ("Growth Area", weakest_trait)]:
        content = archetypes[trait]["description"] if label!="Growth Area" else archetypes[trait]["improvement"]
        st.markdown(
            f"<div style='background-color:{creative_colors[trait]}20; padding:0.7rem; border-radius:10px; margin:0.7rem 0;'>"
            f"<span style='color:{creative_colors[trait]}; font-weight:bold'>{label}: {archetypes[trait]['name']}</span><br>"
            f"<i>{content}</i></div>", unsafe_allow_html=True
        )

    st.subheader("Creative Trait Insights")
    for trait,score in creative_scores.items():
        level=get_level(score); summary=creative_summaries[trait][level]
        st.markdown(
            f"<div style='background-color:{creative_colors[trait]}20; padding:0.5rem; border-radius:8px; margin:0.5rem 0;'>"
            f"<span style='color:{creative_colors[trait]}; font-weight:bold'>{trait} ({level})</span> — {score:.2f}/5<br>"
            f"<i>{summary}</i></div>", unsafe_allow_html=True
        )

    st.subheader("Big Five Trait Insights")
    for trait,score in big5_scores.items():
        level=get_level(score); summary=big5_summaries[trait][level]
        st.markdown(
            f"<div style='background-color:{big5_colors[trait]}20; padding:0.5rem; border-radius:8px; margin:0.5rem 0;'>"
            f"<span style='color:{big5_colors[trait]}; font-weight:bold'>{trait} ({level})</span> — {score:.2f}/5<br>"
            f"<i>{summary}</i></div>", unsafe_allow_html=True
        )

    pdf_buf=create_pdf(creative_scores,big5_scores,main_trait,sub_trait,weakest_trait)
    st.download_button("📄 Download PDF", data=pdf_buf, file_name="Creative_Profile.pdf", mime="application/pdf")
