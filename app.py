import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors

st.set_page_config(page_title="Creative Identity Profile", layout="centered")

# --------------------------
# Colour Palette
# --------------------------
palette = {
    "Originality": "#F94144",
    "Curiosity": "#F8961E",
    "Risk-Taking": "#F9C74F",
    "Imagination": "#90BE6D",
    "Discipline": "#577590",
    "Collaboration": "#43AA8B",
    "Openness": "#277DA1",
    "Conscientiousness": "#F3722C",
    "Extraversion": "#4D908E",
    "Agreeableness": "#F9844A",
    "Neuroticism": "#9A031E",
}

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
# Archetypes
# --------------------------
archetypes = {
    "Innovator": ["High Originality", "High Curiosity"],
    "Explorer": ["High Curiosity", "High Risk-Taking"],
    "Dreamer": ["High Imagination"],
    "Maker": ["High Discipline"],
    "Connector": ["High Collaboration"],
}

sub_archetypes = {
    "Visionary Innovator": "Pairs high Originality with strong Imagination.",
    "Practical Innovator": "Combines Originality with high Discipline.",
    "Adventurous Explorer": "Exploration with risk-taking courage.",
    "Collaborative Dreamer": "Imaginative but thrives in group work.",
    "Grounded Maker": "Disciplined and conscientious creative.",
}

# --------------------------
# Trait Summaries & Tips
# --------------------------
def trait_summary(score):
    if score >= 4.2:
        return "High – a strong defining aspect of your profile."
    elif score >= 3:
        return "Medium – present, but with room for development."
    else:
        return "Low – a potential area for growth."

def improvement_tip(trait):
    tips = {
        "Originality": "Try brainstorming exercises or idea journals.",
        "Curiosity": "Engage in diverse reading or ask more 'why' questions.",
        "Risk-Taking": "Experiment with small, low-stakes risks.",
        "Imagination": "Practice visualisation or creative writing.",
        "Discipline": "Set structured goals and deadlines.",
        "Collaboration": "Seek feedback or join creative groups.",
        "Openness": "Expose yourself to new cultures and perspectives.",
        "Conscientiousness": "Use task lists and project planning tools.",
        "Extraversion": "Join groups or practice public speaking.",
        "Agreeableness": "Practice active listening and empathy.",
        "Neuroticism": "Develop stress-management and mindfulness routines."
    }
    return tips.get(trait, "")

# --------------------------
# PDF Helper
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
    This quiz gives you insights into both your **creative traits** and your **personality profile**.

    - Answer on a **1–5 scale** (1 = Strongly Disagree, 5 = Strongly Agree).  
    - Based on research in creativity & personality psychology.  
    - Get a personalised **profile with charts, archetypes, and growth tips**.  
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

    # Scores
    creative_scores = {t: np.mean([st.session_state.responses[f"{t}_{q}"] for q in qs]) for t, qs in creative_traits.items()}
    bigfive_scores = {t: np.mean([st.session_state.responses[f"{t}_{q}"] for q in qs]) for t, qs in big_five_traits.items()}

    # Radar chart function
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

        for i, (trait, val) in enumerate(scores.items()):
            color = palette.get(trait, "#000000")
            ax.plot([angles[i], angles[i]], [0, val], color=color, linewidth=2)
            ax.scatter(angles[i], val, color=color, s=50)

        ax.plot(angles, values, color="#333333", linewidth=1, linestyle="dashed")
        ax.fill(angles, values, color="#cccccc", alpha=0.1)
        ax.set_title(title, size=14, weight="bold", pad=20)
        st.pyplot(fig)

        buf = io.BytesIO()
        fig.savefig(buf, format="PNG")
        buf.seek(0)
        return buf

    # Show charts
    st.subheader("Big Five Personality Dimensions")
    chart_buf_big5 = radar_chart(bigfive_scores, "Big Five")

    st.subheader("Creative Traits")
    chart_buf_creative = radar_chart(creative_scores, "Creative Traits")

    # Trait summaries
    st.markdown("### Trait Summaries")
    for trait, score in {**creative_scores, **bigfive_scores}.items():
        st.markdown(f"**{trait}** ({score:.1f}) – {trait_summary(score)}  \n_Tip: {improvement_tip(trait)}_")

    # Archetype mapping
    st.markdown("### Your Archetype")
    top_creative = max(creative_scores, key=creative_scores.get)
    if creative_scores[top_creative] >= 4:
        main_arch = [a for a, cond in archetypes.items() if f"High {top_creative}" in cond]
        if main_arch:
            st.write(f"Primary Archetype: **{main_arch[0]}**")
            for sub, desc in sub_archetypes.items():
                if top_creative in desc:
                    st.write(f"- Sub-Archetype: *{sub}* → {desc}")

    # PDF Generation
    def create_pdf():
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=A4)
        width, height = A4

        # Title
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(width/2, height - 40, "Creative Identity & Personality Profile")

        # Charts
        img1 = ImageReader(chart_buf_creative)
        img2 = ImageReader(chart_buf_big5)
        c.drawImage(img1, 60, height - 280, width=200, height=200, mask='auto')
        c.drawImage(img2, 300, height - 280, width=200, height=200, mask='auto')

        # Trait summaries
        c.showPage()
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, "Trait Summaries & Tips")
        c.setFont("Helvetica", 10)
        y = height - 80
        for trait, score in {**creative_scores, **bigfive_scores}.items():
            col = colors.HexColor(palette.get(trait, "#000000"))
            c.setFillColor(col)
            c.drawString(50, y, f"{trait} ({score:.1f}) – {trait_summary(score)}")
            c.setFillColor(colors.black)
            y -= 14
            c.drawString(70, y, f"Tip: {improvement_tip(trait)}")
            y -= 20
            if y < 80:
                c.showPage()
                y = height - 80

        c.showPage()
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width/2, height - 40, "The Science Behind the Profile")
        c.setFont("Helvetica", 10)
        academic_text = """This profile combines creativity research (Guilford, Torrance, Amabile, Sternberg, Runco) with the Big Five model (Costa & McCrae, 1992). It integrates personality psychology with applied creativity studies to provide reflective insights."""
        wrap_text(c, academic_text.split("\n"), 60, height - 70, width - 100, 12)

        c.showPage()
        c.save()
        buf.seek(0)
        return buf

    pdf_buf = create_pdf()
    st.download_button("Download Full Report (PDF)", data=pdf_buf, file_name="Creative_Identity_Profile.pdf", mime="application/pdf")
