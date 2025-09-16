import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

st.set_page_config(page_title="Creative Identity Profile", layout="centered")

# --------------------------
# Creative Traits
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

# --------------------------
# Big Five Traits
# --------------------------
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
# PDF Helper for Academic Section
# --------------------------
def wrap_text(c, lines, x, y, max_width, line_height):
    for line in lines:
        words = line.split()
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if c.stringWidth(test_line, "Helvetica", 10) < max_width:
                current_line = test_line
            else:
                c.drawString(x, y, current_line)
                y -= line_height
                current_line = word + " "
        if current_line:
            c.drawString(x, y, current_line)
            y -= line_height
    return y

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
    This quiz is designed to give you insights into both your **creative traits** and your **personality profile**.
    
    - You will answer statements on a **1–5 scale** (1 = Strongly Disagree, 5 = Strongly Agree).
    - The quiz combines research on creativity and personality psychology.
    - At the end, you’ll receive a **personal profile with charts and an archetype description**.
    """)
    if st.button("Start Quiz"):
        st.session_state.page = "quiz"
        st.rerun()

# --------------------------
# Quiz Page
# --------------------------
elif st.session_state.page == "quiz":
    st.header("Quiz Questions")

    with st.form("quiz_form"):
        for trait, questions in {**creative_traits, **big_five_traits}.items():
            st.subheader(trait)
            for q in questions:
                key = f"{trait}_{q}"
                st.session_state.responses[key] = st.radio(
                    q,
                    [1, 2, 3, 4, 5],
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

    # Compute averages
    creative_scores = {t: np.mean([st.session_state.responses[f"{t}_{q}"] for q in qs]) for t, qs in creative_traits.items()}
    bigfive_scores = {t: np.mean([st.session_state.responses[f"{t}_{q}"] for q in qs]) for t, qs in big_five_traits.items()}

    # --------------------------
    # Radar Chart Function
    # --------------------------
    def radar_chart(scores, title, colors):
        labels = list(scores.keys())
        values = list(scores.values())
        values += values[:1]  # close the loop
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
        ax.fill(angles, values, color=colors[0], alpha=0.25)
        ax.plot(angles, values, color=colors[1], linewidth=2)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels)
        ax.set_yticklabels([])
        ax.set_title(title, size=14, weight="bold", pad=20)
        st.pyplot(fig)

        buf = io.BytesIO()
        fig.savefig(buf, format="PNG")
        buf.seek(0)
        return buf

    # Show charts
    st.subheader("Big Five Personality Dimensions")
    chart_buf_big5 = radar_chart(bigfive_scores, "Big Five", colors=("#4DA1A9", "#05668D"))

    st.subheader("Creative Traits")
    chart_buf_creative = radar_chart(creative_scores, "Creative Traits", colors=("#E56B6F", "#C5283D"))

    # --------------------------
    # Academic Section (Collapsible)
    # --------------------------
    with st.expander("The Science Behind the Creative Identity & Personality Profile"):
        st.markdown("This is where the full academic text and references appear.")

    # --------------------------
    # PDF Generation
    # --------------------------
    def create_pdf():
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=A4)
        width, height = A4

        # Title page
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(width/2, height - 40, "Creative Identity & Personality Profile")

        # Radar charts
        img1 = ImageReader(chart_buf_creative)
        img2 = ImageReader(chart_buf_big5)
        chart_size = 200
        c.drawImage(img1, 60, height - 280, width=chart_size, height=chart_size, preserveAspectRatio=True, mask='auto')
        c.drawImage(img2, 300, height - 280, width=chart_size, height=chart_size, preserveAspectRatio=True, mask='auto')

        # Academic / Science Page
        c.showPage()
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width/2, height - 40, "The Science Behind the Creative Identity & Personality Profile")

        c.setFont("Helvetica", 10)
        academic_text = """The Creative Identity & Personality Profile was designed by drawing upon established research in both creativity studies and personality psychology. The quiz integrates validated psychological frameworks with applied creativity theory, providing participants with a structured but engaging way to reflect on their creative strengths and tendencies.

Creative Traits
Research shows that creativity is not a single skill, but a combination of dispositions, habits, and mindsets (Runco & Jaeger, 2012; Amabile, 1996; Sternberg, 2006). Six traits were selected for this quiz, each reflecting well-documented components of creative behaviour:

- Originality – the ability to generate novel and unconventional ideas (Guilford, 1950).
- Curiosity – openness to questioning and exploring new concepts (Kashdan et al., 2004).
- Risk-Taking – willingness to tolerate uncertainty and possible failure (Beghetto, 2009).
- Imagination – capacity for mental imagery and envisioning possibilities (Vygotsky, 2004).
- Discipline – persistence, effort, and self-regulation in creative work (Torrance, 1974).
- Collaboration – social interaction and exchange as enablers of creativity (Sawyer, 2012).

Big Five Personality Dimensions
The second foundation of the quiz is the Big Five Personality Model (Costa & McCrae, 1992), one of the most extensively validated models in psychology. The five dimensions—Openness, Conscientiousness, Extraversion, Agreeableness, and Neuroticism—are consistently linked with life outcomes, behaviour, and creativity.

References
- Amabile, T. M. (1996). Creativity in Context. Westview Press.
- Costa, P. T., & McCrae, R. R. (1992). Revised NEO Personality Inventory. Psychological Assessment Resources.
- Guilford, J. P. (1950). Creativity. American Psychologist.
"""

        wrap_text(c, academic_text.split("\n"), 60, height - 70, width - 100, 12)

        c.showPage()
        c.save()
        buf.seek(0)
        return buf

    pdf_buf = create_pdf()
    st.download_button("Download Full Report (PDF)", data=pdf_buf, file_name="Creative_Identity_Profile.pdf", mime="application/pdf")
