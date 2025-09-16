import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

# --------------------------
# Streamlit Page Config
# --------------------------
st.set_page_config(page_title="Creative Identity Profile", layout="centered")

# --------------------------
# Color Palette
# --------------------------
TRAIT_COLORS = {
    "Originality": "red",
    "Curiosity": "blue",
    "Risk-Taking": "green",
    "Imagination": "purple",
    "Discipline": "orange",
    "Collaboration": "brown",
    "Openness": "darkblue",
    "Conscientiousness": "darkgreen",
    "Extraversion": "darkred",
    "Agreeableness": "darkorange",
    "Neuroticism": "darkviolet",
}

# --------------------------
# Creative Traits & Big Five
# --------------------------
creative_traits = {
    "Originality": [
        "I enjoy producing ideas that are unique or unusual.",
        "People often describe my ideas as original.",
        "I like to approach problems in unconventional ways."
    ],
    "Curiosity": [
        "I enjoy exploring new ideas and perspectives.",
        "I often ask questions about how things work.",
        "I seek out new experiences and learning opportunities."
    ],
    "Risk-Taking": [
        "I am comfortable with uncertainty in my work.",
        "I am willing to take risks to pursue creative ideas.",
        "I don’t mind failing if it means learning something new."
    ],
    "Imagination": [
        "I often picture ideas vividly in my mind.",
        "I enjoy imagining possibilities beyond the present.",
        "I use mental imagery to explore creative solutions."
    ],
    "Discipline": [
        "I can stay focused on creative work over long periods.",
        "I make structured plans to reach creative goals.",
        "I follow through with projects until completion."
    ],
    "Collaboration": [
        "I enjoy working creatively with others.",
        "I value feedback on my creative ideas.",
        "I thrive when exchanging ideas in groups."
    ],
}

big_five_traits = {
    "Openness": [
        "I enjoy thinking about abstract ideas.",
        "I am curious about many different things.",
        "I have a vivid imagination."
    ],
    "Conscientiousness": [
        "I like to be organized.",
        "I follow through with my commitments.",
        "I pay attention to details."
    ],
    "Extraversion": [
        "I feel energized by social interactions.",
        "I am talkative and expressive.",
        "I enjoy being the center of attention."
    ],
    "Agreeableness": [
        "I am considerate of others’ feelings.",
        "I like to cooperate rather than compete.",
        "I am empathetic toward people around me."
    ],
    "Neuroticism": [
        "I often feel anxious or worried.",
        "I can get stressed easily.",
        "I often feel insecure or vulnerable."
    ],
}

# --------------------------
# Archetypes & Growth Tips
# --------------------------
archetypes = {
    "Originality": {
        "Archetype": "The Innovator",
        "Sub-Archetype": "Divergent Thinker",
        "SummaryHigh": "You thrive on breaking patterns and offering unique perspectives. Others see you as someone who sparks fresh ideas and challenges conventional thinking.",
        "GrowthTipLow": "Practice brainstorming multiple solutions to a problem. Quantity often leads to originality."
    },
    "Curiosity": {
        "Archetype": "The Explorer",
        "Sub-Archetype": "Openness-driven Creative",
        "SummaryHigh": "You are constantly seeking new knowledge, experiences, and perspectives. Your open-mindedness helps you discover connections others miss.",
        "GrowthTipLow": "Try adopting a beginner’s mindset. Ask simple questions even about familiar things to reignite curiosity."
    },
    "Risk-Taking": {
        "Archetype": "The Adventurer",
        "Sub-Archetype": "Tolerance for Uncertainty",
        "SummaryHigh": "You’re willing to step into the unknown and embrace uncertainty, which fuels bold and experimental creativity.",
        "GrowthTipLow": "Start with small, low-stakes risks in your projects to build confidence before taking bigger creative leaps."
    },
    "Imagination": {
        "Archetype": "The Dreamer",
        "Sub-Archetype": "Imaginative Creator",
        "SummaryHigh": "You can easily envision possibilities and think beyond what currently exists. Your creativity flourishes through imagery, storytelling, and future-focused thinking.",
        "GrowthTipLow": "Engage in creative exercises like free drawing, mind-mapping, or writing 'what if' scenarios to expand imaginative thinking."
    },
    "Discipline": {
        "Archetype": "The Builder",
        "Sub-Archetype": "Conscientious Creator",
        "SummaryHigh": "You bring structure, persistence, and focus to creative work. You excel at turning ideas into finished, polished outcomes.",
        "GrowthTipLow": "Break creative goals into smaller, manageable steps and set deadlines to encourage consistent progress."
    },
    "Collaboration": {
        "Archetype": "The Connector",
        "Sub-Archetype": "Socially-Driven Creative",
        "SummaryHigh": "You value teamwork, feedback, and co-creation. You bring out the best in others and thrive in collaborative environments.",
        "GrowthTipLow": "Share even half-formed ideas with trusted peers — collaboration doesn’t require perfection to be valuable."
    }
}

# --------------------------
# References
# --------------------------
references = """
Amabile, T. M. (1996). Creativity in Context. Boulder, CO: Westview Press.<br/>
Boden, M. A. (2004). The Creative Mind: Myths and Mechanisms (2nd ed.). London: Routledge.<br/>
Dacey, J., & Lennon, K. (1998). Understanding Creativity: The Interplay of Biological, Psychological, and Social Factors. San Francisco: Jossey-Bass.<br/>
Fauconnier, G., & Turner, M. (2002). The Way We Think: Conceptual Blending and the Mind's Hidden Complexities. New York: Basic Books.<br/>
Finke, R. A., Ward, T. B., & Smith, S. M. (1992). Creative Cognition: Theory, Research, and Applications. Cambridge, MA: MIT Press.<br/>
Guilford, J. P. (1950). Creativity. American Psychologist, 5(9), 444–454.<br/>
Runco, M. A. (2007). Creativity: Theories and Themes—Research, Development, and Practice. San Diego, CA: Elsevier.<br/>
Sternberg, R. J. (Ed.). (1999). Handbook of Creativity. Cambridge: Cambridge University Press.<br/>
Torrance, E. P. (1974). Torrance Tests of Creative Thinking. Lexington, MA: Personnel Press.<br/>
Weisberg, R. W. (2006). Creativity: Understanding Innovation in Problem Solving, Science, Invention, and the Arts. Hoboken, NJ: Wiley.<br/>
"""

# --------------------------
# Helper: Radar Chart
# --------------------------
def create_radar_chart(trait_scores, title):
    labels = list(trait_scores.keys())
    values = list(trait_scores.values())

    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
    for i, (trait, score) in enumerate(trait_scores.items()):
        color = TRAIT_COLORS.get(trait, "black")
        ax.plot([angles[i], angles[i]], [0, score], color=color, linewidth=2)

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    ax.set_ylim(0, 5)
    ax.set_title(title, size=14, weight="bold")
    return fig

# --------------------------
# Main App
# --------------------------
st.title("Creative Identity & Personality Profile")

st.write("Please answer the following questions on a scale of 1 (Strongly Disagree) to 5 (Strongly Agree).")

responses = {}
for trait, questions in {**creative_traits, **big_five_traits}.items():
    st.subheader(trait)
    for q in questions:
        responses[q] = st.radio(q, [1, 2, 3, 4, 5], horizontal=True, index=2, key=q)

if st.button("Submit"):
    # Average scores
    trait_scores = {}
    for trait, questions in {**creative_traits, **big_five_traits}.items():
        trait_scores[trait] = np.mean([responses[q] for q in questions])

    # Split for radar charts
    creative_scores = {k: trait_scores[k] for k in creative_traits}
    bigfive_scores = {k: trait_scores[k] for k in big_five_traits}

    st.subheader("Results")

    # Radar Charts
    st.pyplot(create_radar_chart(creative_scores, "Creative Traits"))
    st.pyplot(create_radar_chart(bigfive_scores, "Big Five Personality"))

    # Archetypes & Growth
    st.subheader("Archetypes & Growth Areas")
    for trait, score in creative_scores.items():
        arch = archetypes[trait]
        st.markdown(f"**{trait}** – {arch['Archetype']} ({arch['Sub-Archetype']})")
        if score >= 3.5:
            st.write(arch["SummaryHigh"])
        else:
            st.write(arch["GrowthTipLow"])

    # References
    st.subheader("References")
    st.markdown(references, unsafe_allow_html=True)

    # --------------------------
    # PDF Export
    # --------------------------
    def generate_pdf(trait_scores, creative_scores, bigfive_scores):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []

        story.append(Paragraph("Creative Identity & Personality Profile", styles["Title"]))
        story.append(Spacer(1, 12))

        # Creative Archetypes
        story.append(Paragraph("Archetypes & Growth Areas", styles["Heading2"]))
        for trait, score in creative_scores.items():
            arch = archetypes[trait]
            story.append(Paragraph(f"<b>{trait}</b> – {arch['Archetype']} ({arch['Sub-Archetype']})", styles["Normal"]))
            if score >= 3.5:
                story.append(Paragraph(arch["SummaryHigh"], styles["Normal"]))
            else:
                story.append(Paragraph(arch["GrowthTipLow"], styles["Normal"]))
            story.append(Spacer(1, 6))

        # References
        story.append(Spacer(1, 12))
        story.append(Paragraph("References", styles["Heading2"]))
        story.append(Paragraph(references, ParagraphStyle(name="Refs", fontSize=9, leading=12)))

        doc.build(story)
        pdf = buffer.getvalue()
        buffer.close()
        return pdf

    pdf = generate_pdf(trait_scores, creative_scores, bigfive_scores)
    st.download_button("Download Full Report (PDF)", data=pdf, file_name="creative_identity_profile.pdf", mime="application/pdf")
