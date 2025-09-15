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
# Creative Traits
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

creative_colors = {
    "Openness": "#1f77b4",
    "Risk-taking": "#ff7f0e",
    "Resilience": "#2ca02c",
    "Collaboration": "#9467bd",
    "Divergent Thinking": "#d62728",
    "Convergent Thinking": "#8c564b"
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

# --------------------------
# Archetypes
# --------------------------
archetypes = {
    "Openness": {
        "name": "The Explorer",
        "description": "You thrive on curiosity and imagination. Explorers see possibilities everywhere, though sometimes risk being unfocused.",
        "improvement": "Try short 'exploration sprints' followed by reflection to capture the best ideas."
    },
    "Risk-taking": {
        "name": "The Adventurer",
        "description": "You embrace uncertainty and push boundaries, though sometimes risk overexposure.",
        "improvement": "Test risky ideas with small experiments before big commitments."
    },
    "Resilience": {
        "name": "The Perseverer",
        "description": "You persist through challenges and learn from failure.",
        "improvement": "After setbacks, reflect on lessons and note small wins to keep momentum."
    },
    "Collaboration": {
        "name": "The Connector",
        "description": "You spark ideas in groups and value diverse perspectives.",
        "improvement": "Balance collaboration with solo time to develop your own voice."
    },
    "Divergent Thinking": {
        "name": "The Visionary",
        "description": "You generate many original ideas and unusual connections.",
        "improvement": "Use ranking criteria to pick the most promising ideas to develop further."
    },
    "Convergent Thinking": {
        "name": "The Strategist",
        "description": "You refine and structure ideas into action.",
        "improvement": "Occasionally loosen constraints to allow more unusual ideas."
    }
}

# --------------------------
# Big Five Traits
# --------------------------
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
    "Openness": [
        "I enjoy trying new activities and experiences.",
        "I have a broad range of interests.",
        "I am curious about many different things."
    ]
}

big5_colors = {
    "Conscientiousness": "#ff7f0e",
    "Extraversion": "#2ca02c",
    "Agreeableness": "#9467bd",
    "Neuroticism": "#d62728",
    "Openness": "#1f77b4"
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

def radar_chart(scores: dict, colors: dict, title="") -> io.BytesIO:
    labels = list(scores.keys())
    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))
    values = list(scores.values())
    values += values[:1]

    ax.plot(angles, values, linewidth=1.5, color="black")
    ax.fill(angles, values, alpha=0.05, color="gray")

    for i, (trait, score) in enumerate(scores.items()):
        ax.plot([angles[i], angles[i+1]], [score, values[i+1]],
                color=colors[trait], linewidth=3)
        ax.scatter(angles[i], score, color=colors[trait], s=60, zorder=10, label=trait)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylim(0,5)
    ax.set_yticks([1,2,3,4,5])
    ax.set_yticklabels(["1","2","3","4","5"])
    plt.title(title, size=12, weight="bold")
    ax.legend(bbox_to_anchor=(1.15, 1.1))

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)
    return buf

# --------------------------
# PDF Generator
# --------------------------
def create_pdf(creative_scores, big5_scores, archetypes_data, creative_summaries, big5_summaries, chart_buf_creative, chart_buf_big5):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, height - 40, "Creative Identity & Personality Profile")

    img1 = ImageReader(chart_buf_creative)
    img2 = ImageReader(chart_buf_big5)
    chart_size = 200
    c.drawImage(img1, 60, height - 280, width=chart_size, height=chart_size, preserveAspectRatio=True, mask='auto')
    c.drawImage(img2, 300, height - 280, width=chart_size, height=chart_size, preserveAspectRatio=True, mask='auto')

    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, height - 320, "Your Creative Archetypes")
    y = height - 340
    for label, (trait, arch) in archetypes_data.items():
        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, y, f"{label}: {arch['name']}")
        c.setFont("Helvetica", 10)
        text = arch['description'] if label != "Growth Area" else arch['improvement']
        c.drawString(60, y-12, text)
        y -= 40

    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "Creative Trait Insights")
    y -= 20
    for trait, score in creative_scores.items():
        level = get_level(score)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, f"{trait} ({level}) — {score:.2f}/5")
        c.setFont("Helvetica", 9)
        c.drawString(60, y-12, creative_summaries[trait][level])
        y -= 30

    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "Big Five Trait Insights")
    y -= 20
    for trait, score in big5_scores.items():
        level = get_level(score)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, f"{trait} ({level}) — {score:.2f}/5")
        c.setFont("Helvetica", 9)
        c.drawString(60, y-12, big5_summaries[trait][level])
        y -= 30

    c.showPage()
    c.save()
    buf.seek(0)
    return buf

# --------------------------
# Streamlit App
# --------------------------
st.title("Creative Identity & Personality Profile")
st.write("This quiz will explore both your creative traits and your Big Five personality traits. "
         "Please rate each statement on a 1–5 scale: 1 = Strongly Disagree … 5 = Strongly Agree.")

# initialise session state
if "all_questions" not in st.session_state:
    all_questions = []
    for trait, qs in {**creative_traits, **big5_traits}.items():
        for q in qs:
            all_questions.append((trait, q))
    random.shuffle(all_questions)
    st.session_state.all_questions = all_questions
    st.session_state.current_q = 0
    st.session_state.responses = {f"{trait}_{i}": None for i, (trait, _) in enumerate(all_questions, 1)}

# separate quiz vs results page
if not st.session_state.get("show_results", False):
    # ------------------
    # Quiz Page
    # ------------------
    all_questions = st.session_state.all_questions
    responses = st.session_state.responses
    current_q = st.session_state.current_q
    total_qs = len(all_questions)

    st.markdown(f"**Question {current_q+1} of {total_qs}**")
    st.progress((current_q+1) / total_qs)

    # Question display with no default
    trait, question = all_questions[current_q]
    key = f"{trait}_{current_q+1}"
    saved_val = responses[key]

    options = [1, 2, 3, 4, 5]
    answer = st.radio(
        question,
        options,
        horizontal=True,
        index=None if saved_val is None else options.index(saved_val),
        key=key
    )
    responses[key] = answer if answer else None

    # Navigation
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("Back", disabled=current_q==0):
            st.session_state.current_q -= 1
            st.rerun()
    with col2:
        answered = responses[key] is not None
        if st.button("Next Question", disabled=not answered):
            if current_q + 1 < total_qs:
                st.session_state.current_q += 1
                st.rerun()
            else:
                # compute results
                creative_scores = {t:0 for t in creative_traits}
                creative_counts = {t:0 for t in creative_traits}
                big5_scores = {t:0 for t in big5_traits}
                big5_counts = {t:0 for t in big5_traits}

                for k, val in responses.items():
                    if val:
                        trait = k.split("_")[0]
                        if trait in creative_scores:
                            creative_scores[trait] += val
                            creative_counts[trait] += 1
                        if trait in big5_scores:
                            big5_scores[trait] += val
                            big5_counts[trait] += 1

                for t in creative_scores:
                    if creative_counts[t] > 0:
                        creative_scores[t] /= creative_counts[t]
                for t in big5_scores:
                    if big5_counts[t] > 0:
                        big5_scores[t] /= big5_counts[t]

                st.session_state.results = (creative_scores, big5_scores)
                st.session_state.show_results = True
                st.rerun()
else:
    # ------------------
    # Results Page
    # ------------------
    creative_scores, big5_scores = st.session_state.results

    st.title("Your Results")
    st.success("All questions complete — here are your results!")

    c1, c2 = st.columns(2)
    with c1:
        st.image(radar_chart(creative_scores, creative_colors, "Creative Traits"), use_container_width=True)
    with c2:
        st.image(radar_chart(big5_scores, big5_colors, "Big Five Traits"), use_container_width=True)

    sorted_traits = sorted(creative_scores.items(), key=lambda x: x[1], reverse=True)
    main_trait, sub_trait, weakest_trait = sorted_traits[0][0], sorted_traits[1][0], sorted_traits[-1][0]

    st.subheader("Your Creative Archetypes")
    for label, trait in [("Main Archetype", main_trait), ("Sub-Archetype", sub_trait), ("Growth Area", weakest_trait)]:
        if label == "Growth Area":
            content = archetypes[trait]["improvement"]
        else:
            content = archetypes[trait]["description"]
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
        summary = big5_summaries[trait][level]
        st.markdown(
            f"<div style='background-color:{big5_colors[trait]}20; padding:0.5rem; border-radius:8px; margin:0.5rem 0;'>"
            f"<span style='color:{big5_colors[trait]}; font-weight:bold'>{trait} ({level})</span> — {score:.2f}/5<br>"
            f"<i>{summary}</i></div>", unsafe_allow_html=True
        )

    # PDF Download
    pdf_buf = create_pdf(
        creative_scores, big5_scores,
        {
            "Main Archetype": (main_trait, archetypes[main_trait]),
            "Sub-Archetype": (sub_trait, archetypes[sub_trait]),
            "Growth Area": (weakest_trait, archetypes[weakest_trait]),
        },
        creative_summaries, big5_summaries,
        radar_chart(creative_scores, creative_colors, "Creative Traits"),
        radar_chart(big5_scores, big5_colors, "Big Five Traits")
    )
    st.download_button("Download Your Full Profile (PDF)", pdf_buf, file_name="creative_identity_profile.pdf", mime="application/pdf")
