# --------------------------
# Block 1: Imports, Config & Button Styling
# --------------------------
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
import random
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch  # <-- add this
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader


# --------------------------
# Page config
# --------------------------
st.set_page_config(page_title="Creative Identity Profile", layout="centered")

# --------------------------
# Button styling
# --------------------------
gradients = [
    "linear-gradient(90deg, #7b2ff7, #f107a3)",
    "linear-gradient(90deg, #06beb6, #48b1bf)",
    "linear-gradient(90deg, #ff6a00, #ee0979)"
]
chosen_gradient = random.choice(gradients)

st.markdown(f"""
<style>
div.stButton > button {{
    background: {chosen_gradient};
    color: white;
    border-radius: 12px;
    height: 2.5em;
    min-width: 8em;
    font-size: 16px;
    font-weight: bold;
    transition: 0.3s;
    border: none;
    margin: 0.2em;
}}
div.stButton > button:hover {{
    filter: brightness(1.1);
    transform: scale(1.03);
}}
div.stDownloadButton > button {{
    background: {chosen_gradient};
    color: white;
    border-radius: 12px;
    height: 2.8em;
    min-width: 12em;
    font-size: 16px;
    font-weight: bold;
    transition: 0.3s;
    border: none;
    margin-top: 1em;
}}
div.stDownloadButton > button:hover {{
    filter: brightness(1.1);
    transform: scale(1.03);
}}
.stProgress > div > div > div > div {{
    background-color: #b0b0b0;
}}
</style>
""", unsafe_allow_html=True)

# --------------------------
# Session state setup
# --------------------------
if "page" not in st.session_state:
    st.session_state.page = "intro"
if "responses" not in st.session_state:
    st.session_state.responses = {}

# --------------------------
# Block 2: Traits, Descriptions, Archetypes, Palette
# --------------------------

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
# Creative Traits
# --------------------------
creative_traits = {
    "Originality": [
        "I often find myself suggesting unusual or unexpected solutions.",
        "I often think of alternative solutions others might not consider.",
        "I value uniqueness in my work and thinking."
    ],
    "Curiosity": [
        "I ask questions even when I’m not sure there’s an easy answer.",
        "I seek out opportunities to learn new things.",
        "I am curious about how things work."
    ],
    "Risk-Taking": [
        "I am comfortable with uncertainty when exploring ideas.",
        "I sometimes avoid new ideas because they might not work.",  # reverse-coded
        "I take creative risks in my projects."
    ],
    "Imagination": [
        "I often picture possibilities in my mind before I try them out.",
        "I enjoy daydreaming and thinking about new scenarios.",
        "I use mental imagery when solving problems."
    ],
    "Discipline": [
        "I can stay focused on creative projects until completion.",
        "I put structured effort into developing my ideas.",
        "I find it difficult to stay focused on creative projects for a long time."  # reverse-coded
    ],
    "Collaboration": [
        "When working with others, I build on their ideas as much as I share my own.",
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
        "I enjoy exploring new art, music, or ideas, even if they’re unfamiliar.",
        "I prefer sticking to familiar routines over trying new experiences."  # reverse-coded
    ],
    "Conscientiousness": [
        "I pay attention to details when working.",
        "I make detailed plans before starting a task.",
        "I often leave tasks unfinished."  # reverse-coded
    ],
    "Extraversion": [
        "I feel energized when interacting with people.",
        "I enjoy group activities and conversations.",
        "I usually prefer being alone rather than in social situations."  # reverse-coded
    ],
    "Agreeableness": [
        "I am considerate of others’ needs and feelings.",
        "I try to see things from other people’s perspectives during disagreements.",
        "I sometimes put my own needs before others’."  # reverse-coded
    ],
    "Neuroticism": [
        "I often feel stressed or anxious in daily life.",
        "I can become easily worried about problems.",
        "I remain calm even when under pressure."  # reverse-coded
    ]
}

# --------------------------
# Reverse-coded mapping
# --------------------------
reverse_items = {
    "Originality": [],
    "Curiosity": [],
    "Risk-Taking": [1],       # 2nd question reverse-coded
    "Imagination": [],
    "Discipline": [2],        # 3rd question reverse-coded
    "Collaboration": [],
    "Openness": [2],           # 3rd question reverse-coded
    "Conscientiousness": [2],  # 3rd question reverse-coded
    "Extraversion": [2],       # 3rd question reverse-coded
    "Agreeableness": [2],      # 3rd question reverse-coded
    "Neuroticism": [2]         # 3rd question reverse-coded
}

# --------------------------
# Trait Descriptions
# --------------------------
trait_descriptions = {
    "Originality": {
        "high": "You thrive on breaking patterns and offering unique perspectives. Others often see you as a source of fresh, unconventional ideas.",
        "medium": "You sometimes show originality but balance it with conventional approaches, depending on the situation.",
        "low": "You prefer tried-and-tested methods over generating novel ideas, valuing familiarity over experimentation."
    },
    "Curiosity": {
        "high": "You are constantly seeking new knowledge and experiences. You love questioning and exploring beyond the obvious.",
        "medium": "You are curious when prompted but don’t always explore further without external motivation.",
        "low": "You are less driven to question or seek out new experiences, preferring stability and routine."
    },
    "Risk-Taking": {
        "high": "You embrace uncertainty and are willing to take creative risks, seeing setbacks as part of the journey.",
        "medium": "You sometimes take risks but often prefer security, weighing potential downsides before acting.",
        "low": "You prefer safe, predictable routes and avoid uncertainty whenever possible."
    },
    "Imagination": {
        "high": "You easily envision new possibilities and future scenarios. Your ability to think beyond the present helps you innovate.",
        "medium": "You imagine ideas sometimes but often remain practical and grounded in the here-and-now.",
        "low": "You focus more on concrete realities than imaginative possibilities, preferring clarity over abstraction."
    },
    "Discipline": {
        "high": "You bring persistence and structure to creative projects, often ensuring ideas reach completion.",
        "medium": "You stay disciplined when motivated but can lose focus if enthusiasm drops.",
        "low": "You often find it hard to sustain focus and follow-through, which can stall projects."
    },
    "Collaboration": {
        "high": "You thrive in teamwork and enjoy co-creating with others, seeing group input as energising.",
        "medium": "You collaborate when needed but also value independence and personal space.",
        "low": "You prefer working alone and rely less on group dynamics for creativity."
    },
    "Openness": {
        "high": "You are highly receptive to new experiences and perspectives, thriving in environments that encourage growth.",
        "medium": "You are somewhat open to new experiences but prefer familiar territory for security.",
        "low": "You resist change and prefer predictable, familiar approaches over new perspectives."
    },
    "Conscientiousness": {
        "high": "You are dependable, organized, and detail-oriented, which supports long-term goals and achievements.",
        "medium": "You show conscientiousness when motivated but don’t always stay consistent.",
        "low": "You struggle with structure and consistency, often preferring spontaneity."
    },
    "Extraversion": {
        "high": "You are highly energized by social interaction and seek out group experiences.",
        "medium": "You enjoy socializing but also value time alone to recharge.",
        "low": "You are more reserved and often prefer solitary or small-group settings."
    },
    "Agreeableness": {
        "high": "You are cooperative, empathetic, and considerate, often putting group harmony above personal preference.",
        "medium": "You are agreeable in many cases but still assert your own needs when necessary.",
        "low": "You are less concerned with harmony and prioritize your own goals or principles."
    },
    "Neuroticism": {
        "high": "You often feel strong emotions such as stress or worry, which can shape how you react under pressure.",
        "medium": "You sometimes feel anxious or stressed but can usually manage your emotions.",
        "low": "You are emotionally stable, resilient, and less prone to anxiety or negative moods."
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
# Block 3: Helper Functions
# --------------------------

import io
import matplotlib.pyplot as plt
import numpy as np
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors

# --------------------------
# Academic PDF function
# --------------------------
def create_academic_pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=50,
        rightMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = {
        "title": ParagraphStyle(
            "title",
            fontSize=14,
            leading=18,
            alignment=TA_CENTER,
            spaceAfter=10,
            underline=True,
            fontName="Helvetica-Bold"
        ),
        "heading": ParagraphStyle(
            "heading",
            fontSize=12,
            leading=16,
            alignment=TA_LEFT,
            spaceBefore=10,
            spaceAfter=6,
            underline=True,
            fontName="Helvetica-Bold"
        ),
        "body": ParagraphStyle(
            "body",
            fontSize=10,
            leading=14,
            alignment=TA_LEFT,
            spaceAfter=6,
            fontName="Helvetica"
        ),
    }

    story = []
    with open("academic_article.txt", "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                story.append(Spacer(1, 12))
            elif line.startswith("# "):
                story.append(Paragraph(line[2:], styles["title"]))
            elif line.startswith("## "):
                story.append(Paragraph(line[3:], styles["heading"]))
            else:
                story.append(Paragraph(line, styles["body"]))

    doc.build(story)
    buffer.seek(0)
    return buffer

# --------------------------
# PDF-safe radar chart function
# --------------------------
def radar_chart_pdf(scores, title, size_inch=2.6, dpi=200):
    """
    Return a BytesIO PNG of a square radar chart.
    size_inch: figure size in inches (width == height)
    """
    import io
    import matplotlib.pyplot as plt
    import numpy as np

    labels = list(scores.keys())
    values = list(scores.values())
    # close the loop
    values = values + values[:1]
    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles = angles + angles[:1]

    # Create perfectly square figure
    fig = plt.figure(figsize=(size_inch, size_inch))
    ax = fig.add_subplot(111, polar=True)

    # Try to force equal aspect; polar axes sometimes ignore box_aspect,
    # but the main fix is saving without bbox_inches='tight' to preserve square pixels.
    try:
        ax.set_box_aspect(1)
    except Exception:
        try:
            ax.set_aspect('equal')
        except Exception:
            pass

    # Background polygon (faint)
    ax.plot(angles, values, color='grey', linewidth=1, alpha=0.25)
    ax.fill(angles, values, color='grey', alpha=0.05)

    # Draw colored segments & points per trait
    for i, label in enumerate(labels):
        start_ang = angles[i]
        end_ang = angles[i + 1]
        start_val = values[i]
        end_val = values[i + 1]
        ax.plot([start_ang, end_ang], [start_val, end_val], color=palette.get(label, "#888888"), linewidth=2)
        ax.plot(start_ang, start_val, 'o', color=palette.get(label, "#888888"), markersize=6)

    # Axes settings
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_yticklabels([])
    ax.set_ylim(0, 100)
    ax.set_title(title, size=12, weight="bold", pad=12)

    # Save WITHOUT bbox_inches='tight' (keeps the PNG square)
    buf = io.BytesIO()
    fig.savefig(buf, format="PNG", dpi=dpi)
    buf.seek(0)
    plt.close(fig)
    return buf


# --------------------------
# Results PDF
# --------------------------
def create_results_pdf(creative_perc, bigfive_perc, trait_descriptions, archetypes):
    """
    Build a results PDF buffer with:
     - two square radar charts side-by-side,
     - three coloured archetype cards (Primary / Sub / Growth),
     - Creative and Big Five trait lists in two columns.
    """
    from reportlab.lib.units import inch
    from reportlab.lib import colors as rl_colors
    from reportlab.platypus import Paragraph, Spacer, Image, Table, TableStyle
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    import io

    # Page & margins
    left_margin = 40
    right_margin = 40
    top_margin = 40
    bottom_margin = 40

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=left_margin,
        rightMargin=right_margin,
        topMargin=top_margin,
        bottomMargin=bottom_margin
    )

    # Styles
    styles = {
        "title": ParagraphStyle("title", fontSize=18, leading=22, alignment=TA_CENTER, spaceAfter=12, fontName="Helvetica-Bold"),
        "subtitle": ParagraphStyle("subtitle", fontSize=14, leading=18, alignment=TA_LEFT, spaceAfter=8, fontName="Helvetica-Bold"),
        "body": ParagraphStyle("body", fontSize=11, leading=14, alignment=TA_LEFT, spaceAfter=6, fontName="Helvetica"),
        "card_title": ParagraphStyle("card_title", fontSize=12, leading=14, alignment=TA_LEFT, textColor=rl_colors.white, fontName="Helvetica-Bold"),
    }

    story = []
    story.append(Paragraph("Your Creative Identity Profile", styles["title"]))
    story.append(Spacer(1, 8))

    # --- Radar charts (compute available width and choose chart size that fits) ---
    page_width_pts, _ = A4
    content_width_pts = page_width_pts - (left_margin + right_margin)
    # available width per chart if side-by-side (leave small padding)
    max_chart_width_inch = (content_width_pts / 72.0) / 2.0 - 0.25
    # choose chart size (inches) but cap to a reasonable default (2.8 -> fits most A4 layouts)
    chart_inch = min(2.8, max_chart_width_inch if max_chart_width_inch > 1.8 else 2.2)

    chart_buf_creative = radar_chart_pdf(creative_perc, "Creative Traits", size_inch=chart_inch)
    chart_buf_big5 = radar_chart_pdf(bigfive_perc, "Big Five Traits", size_inch=chart_inch)

    img_creative = Image(chart_buf_creative, width=chart_inch * inch, height=chart_inch * inch)
    img_big5 = Image(chart_buf_big5, width=chart_inch * inch, height=chart_inch * inch)

    chart_col_width = chart_inch * inch
    # Center the charts: put them in a table and center the table
    chart_table = Table([[img_creative, img_big5]], colWidths=[chart_col_width, chart_col_width])
    chart_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
    ]))
    story.append(chart_table)
    story.append(Spacer(1, 12))

    # --- Archetype cards (Primary, Sub, Growth) ---
    # determine primary, sub, growth from creative_perc
    sorted_traits = sorted(creative_perc.items(), key=lambda x: x[1], reverse=True)
    top_trait = sorted_traits[0][0]
    sub_trait = sorted_traits[1][0] if len(sorted_traits) > 1 else None
    lowest_trait = sorted_traits[-1][0]

    def add_archetype_card(trait_key, title_text, desc_text, tip_text):
        bg_hex = palette.get(trait_key, "#7b2ff7")
        bg_color = rl_colors.HexColor(bg_hex)
        # Title block with background color
        title_para = Paragraph(title_text, styles["card_title"])
        title_table = Table([[title_para]], colWidths=[content_width_pts - 0])  # full width
        title_table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), bg_color),
            ("LEFTPADDING", (0,0), (-1,-1), 8),
            ("RIGHTPADDING", (0,0), (-1,-1), 8),
            ("TOPPADDING", (0,0), (-1,-1), 6),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ]))
        story.append(title_table)
        story.append(Spacer(1, 4))
        # description and tip (normal body style)
        story.append(Paragraph(desc_text, styles["body"]))
        story.append(Paragraph(f"<b>Growth Tip:</b> {tip_text}", styles["body"]))
        story.append(Spacer(1, 8))

    # Primary
    top_desc = trait_descriptions[top_trait]["high"] if creative_perc[top_trait] >= 67 else \
               trait_descriptions[top_trait]["medium"] if creative_perc[top_trait] >= 34 else \
               trait_descriptions[top_trait]["low"]
    add_archetype_card(top_trait, f"Primary Archetype: {archetypes[top_trait][0]} ({archetypes[top_trait][1]})", top_desc, archetypes[top_trait][2])

    # Sub
    if sub_trait:
        sub_desc = trait_descriptions[sub_trait]["high"] if creative_perc[sub_trait] >= 67 else \
                   trait_descriptions[sub_trait]["medium"] if creative_perc[sub_trait] >= 34 else \
                   trait_descriptions[sub_trait]["low"]
        add_archetype_card(sub_trait, f"Sub-Archetype: {archetypes[sub_trait][0]} ({archetypes[sub_trait][1]})", sub_desc, archetypes[sub_trait][2])

    # Growth
    low_desc = trait_descriptions[lowest_trait]["low"]
    add_archetype_card(lowest_trait, f"Growth Area: {lowest_trait}", low_desc, archetypes[lowest_trait][2])

    story.append(Spacer(1, 8))

    # --- Insert Page Break here to start a new page for traits ---
    story.append(PageBreak())

    # --- Traits: two-column lists for Creative and Big Five on the new page ---
    def trait_table(traits_dict, heading_text):
        story.append(Paragraph(heading_text, styles["subtitle"]))
        traits = list(traits_dict.items())
        mid = (len(traits) + 1) // 2
        left = traits[:mid]
        right = traits[mid:]

        rows = []
        col_w = (content_width_pts / 2.0)

        for i in range(max(len(left), len(right))):
            left_cell = ""
            if i < len(left):
                t, p = left[i]
                desc = trait_descriptions[t]["high"] if p >= 67 else \
                       trait_descriptions[t]["medium"] if p >= 34 else \
                       trait_descriptions[t]["low"]
                left_cell = f"<b>{t}: {p}%</b><br/>{desc}"
            right_cell = ""
            if i < len(right):
                t, p = right[i]
                desc = trait_descriptions[t]["high"] if p >= 67 else \
                       trait_descriptions[t]["medium"] if p >= 34 else \
                       trait_descriptions[t]["low"]
                right_cell = f"<b>{t}: {p}%</b><br/>{desc}"
            rows.append([Paragraph(left_cell, styles["body"]), Paragraph(right_cell, styles["body"])])

        tbl = Table(rows, colWidths=[col_w, col_w], hAlign='LEFT')
        tbl.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0,0), (-1,-1), 6),
            ("RIGHTPADDING", (0,0), (-1,-1), 6),
            ("TOPPADDING", (0,0), (-1,-1), 2),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ]))
        story.append(tbl)
        story.append(Spacer(1, 10))

    # Add the two trait tables to the **second page**
    trait_table(creative_perc, "Creative Traits")
    trait_table(bigfive_perc, "Big Five Traits")

    doc.build(story)
    buffer.seek(0)
    return buffer

# --------------------------
# Score calculation
# --------------------------
def calculate_scores(traits, responses):
    scores = {}
    for trait, qs in traits.items():
        trait_values = []
        for i, q in enumerate(qs):
            key = f"{trait}_{q}"
            if key not in responses:
                continue
            val = int(responses[key][0])
            if trait in reverse_items and i in reverse_items[trait]:
                val = 6 - val
            trait_values.append(val)
        if trait_values:
            scores[trait] = np.mean(trait_values)
    return scores

# --------------------------
# Block 4: Button Styling and Page Flow
# --------------------------

import random
import streamlit as st

# --------------------------
# Button Styling
# --------------------------
gradients = [
    "linear-gradient(90deg, #7b2ff7, #f107a3)",
    "linear-gradient(90deg, #06beb6, #48b1bf)",
    "linear-gradient(90deg, #ff6a00, #ee0979)"
]
chosen_gradient = random.choice(gradients)

st.markdown(f"""
<style>
div.stButton > button {{
    background: {chosen_gradient};
    color: white;
    border-radius: 12px;
    height: 2.5em;
    min-width: 8em;
    font-size: 16px;
    font-weight: bold;
    transition: 0.3s;
    border: none;
    margin: 0.2em;
}}
div.stButton > button:hover {{
    filter: brightness(1.1);
    transform: scale(1.03);
}}
div.stDownloadButton > button {{
    background: {chosen_gradient};
    color: white;
    border-radius: 12px;
    height: 2.8em;
    min-width: 12em;
    font-size: 16px;
    font-weight: bold;
    transition: 0.3s;
    border: none;
    margin-top: 1em;
}}
div.stDownloadButton > button:hover {{
    filter: brightness(1.1);
    transform: scale(1.03);
}}
.stProgress > div > div > div > div {{
    background-color: #b0b0b0;
}}
</style>
""", unsafe_allow_html=True)

# --------------------------
# Page Flow Setup
# --------------------------
if "page" not in st.session_state:
    st.session_state.page = "intro"
if "responses" not in st.session_state:
    st.session_state.responses = {}

# --------------------------
# Intro Page
# --------------------------
if st.session_state.page == "intro":
    st.title("Creative Personality Profile")

    st.subheader("What to Expect")
    st.markdown("""
    - 33 short statements, answered one at a time.  
    - Each uses a 1–5 scale (Strongly Disagree → Strongly Agree).  
    - Takes about 5–7 minutes to complete.  
    - No right or wrong answers — just be honest about what feels true for you.
    """)

    st.subheader("What You’ll Get")
    st.markdown("""
    - A personalised profile of your creative traits and personality traits.  
    - A visual breakdown of your results (radar charts).  
    - Your creative archetype and growth areas.  
    - Practical tips to develop your creativity further.
    """)

    st.subheader("Why This Matters")
    st.markdown("""
    Creativity and personality shape how you approach challenges, generate ideas, and collaborate.  
    By understanding your unique profile, you can:

    - Play to your strengths.  
    - Recognise and improve growth areas.  
    - Gain deeper insight into your personal and professional identity.  

    Take your time, reflect honestly, and enjoy discovering your creative identity.
    """)

    # ✅ Centered gradient "Start Quiz" button
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("Start Quiz", key="intro_start_quiz"):
            st.session_state.current_question = 0
            st.session_state.page = "quiz"
            st.rerun()

    # ✅ Gradient styling for the button
    st.markdown(
        """
        <style>
        div.stButton > button:first-child {
            background: linear-gradient(to right, #ff7e5f, #feb47b);
            color: white;
            font-size: 18px;
            padding: 0.6em 1.2em;
            border-radius: 8px;
            border: none;
            cursor: pointer;
        }
        div.stButton > button:first-child:hover {
            background: linear-gradient(to right, #feb47b, #ff7e5f);
        }
        </style>
        """,
        unsafe_allow_html=True
    )


# --------------------------
# Quiz Page (one question per page)
# --------------------------
elif st.session_state.page == "quiz":

    # Shuffle questions once at the start
    if "shuffled_questions" not in st.session_state:
        questions = []
        for trait, qs in {**creative_traits, **big_five_traits}.items():
            for q in qs:
                questions.append((trait, q))
        random.shuffle(questions)
        st.session_state.shuffled_questions = questions
        st.session_state.current_question = 0

    total_questions = len(st.session_state.shuffled_questions)
    current_index = st.session_state.current_question
    trait, q_text = st.session_state.shuffled_questions[current_index]

    st.header("Quiz")
    st.markdown(f"**Question {current_index + 1} of {total_questions}**")
    st.progress((current_index + 1) / total_questions)

    # Display question
    widget_key = f"{trait}_{q_text}"
    prev_answer = st.session_state.responses.get(widget_key, None)
    response = st.radio(
        q_text,
        ["1 Strongly Disagree", "2 Disagree", "3 Neutral", "4 Agree", "5 Strongly Agree"],
        horizontal=True,
        index=None if prev_answer is None else 
              ["1 Strongly Disagree", "2 Disagree", "3 Neutral", "4 Agree", "5 Strongly Agree"].index(prev_answer),
        key=widget_key
    )
    st.session_state.responses[widget_key] = response

    # Navigation buttons in columns
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.session_state.current_question > 0:
            if st.button("Back"):
                st.session_state.current_question -= 1
                st.rerun()
    with col2:
        st.empty()
    with col3:
        # Enable next/finish only if answered
        if widget_key in st.session_state.responses and st.session_state.responses[widget_key]:
            if st.session_state.current_question < total_questions - 1:
                if st.button("Next"):
                    st.session_state.current_question += 1
                    st.rerun()
            else:
                if st.button("Finish"):
                    st.session_state.page = "results"
                    st.rerun()
        else:
            st.button("Next", disabled=True)

# --------------------------
# Block 5: Results Page
# --------------------------

if st.session_state.page == "results":
    st.title("Your Creative Identity Profile")

    # --------------------------
    # Calculate scores
    # --------------------------
    creative_scores = calculate_scores(creative_traits, st.session_state.responses)
    bigfive_scores = calculate_scores(big_five_traits, st.session_state.responses)

    creative_perc = {t: round((s - 1) / 4 * 100) for t, s in creative_scores.items()}
    bigfive_perc = {t: round((s - 1) / 4 * 100) for t, s in bigfive_scores.items()}

    # --------------------------
    # Display radar charts on page (Streamlit)
    # --------------------------
    def radar_chart(scores, title):
        labels = list(scores.keys())
        values = list(scores.values())
        values += values[:1]
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(5,5), subplot_kw=dict(polar=True))

        # Plot each trait line in its colour
        for i, label in enumerate(labels):
            val = values[i]
            ax.plot([angles[i], angles[i+1]], [val, values[i+1]], color=palette[label], linewidth=2)

        # Axes settings
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels)
        ax.set_yticklabels([])
        ax.set_ylim(0, 100)
        ax.set_title(title, size=14, weight="bold", pad=20)

        st.pyplot(fig)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Creative Traits")
        radar_chart(creative_perc, "Creative Traits")
    with col2:
        st.subheader("Big Five")
        radar_chart(bigfive_perc, "Big Five")

    # --------------------------
    # Trait Scores in Two Columns
    # --------------------------
    st.subheader("Your Trait Scores")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Creative Traits")
        for t, p in creative_perc.items():
            st.markdown(f"**{t}:** {p}%")
            if p >= 67:
                st.markdown(trait_descriptions[t]["high"])
            elif p >= 34:
                st.markdown(trait_descriptions[t]["medium"])
            else:
                st.markdown(trait_descriptions[t]["low"])

    with col2:
        st.markdown("### Big Five Traits")
        for t, p in bigfive_perc.items():
            st.markdown(f"**{t}:** {p}%")
            if p >= 67:
                st.markdown(trait_descriptions[t]["high"])
            elif p >= 34:
                st.markdown(trait_descriptions[t]["medium"])
            else:
                st.markdown(trait_descriptions[t]["low"])

    # --------------------------
    # Archetypes
    # --------------------------
    sorted_traits = sorted(creative_perc.items(), key=lambda x: x[1], reverse=True)
    top_trait, sub_trait, lowest_trait = sorted_traits[0][0], sorted_traits[1][0], sorted_traits[-1][0]
    top_score, sub_score, low_score = sorted_traits[0][1], sorted_traits[1][1], sorted_traits[-1][1]

    def archetype_card(trait, title, description, tip):
        color = palette.get(trait, "#7b2ff7")
        return f"""
        <div style="
            background: {color};
            padding: 0.8em;
            border-radius: 12px;
            margin-bottom: 1em;
            text-align: left;
            color: white;
            font-size: 16px;
            font-weight: normal;
            box-shadow: 0px 4px 8px rgba(0,0,0,0.15);
        ">
            <h3 style="margin-top:0; font-size:18px; font-weight:bold;">{title}</h3>
            <p style="margin:0.3em 0;">{description}</p>
            <p style="margin:0.3em 0;"><b>Growth Tip:</b> {tip}</p>
        </div>
        """

    # Primary Archetype
    if top_score >= 67:
        desc = trait_descriptions[top_trait]["high"]
    elif top_score >= 34:
        desc = trait_descriptions[top_trait]["medium"]
    else:
        desc = trait_descriptions[top_trait]["low"]

    st.markdown(archetype_card(
        top_trait,
        f"Primary Archetype: {archetypes[top_trait][0]} ({archetypes[top_trait][1]})",
        desc,
        archetypes[top_trait][2]
    ), unsafe_allow_html=True)

    # Sub-Archetype
    if sub_score >= 67:
        desc = trait_descriptions[sub_trait]["high"]
    elif sub_score >= 34:
        desc = trait_descriptions[sub_trait]["medium"]
    else:
        desc = trait_descriptions[sub_trait]["low"]

    st.markdown(archetype_card(
        sub_trait,
        f"Sub-Archetype: {archetypes[sub_trait][0]} ({archetypes[sub_trait][1]})",
        desc,
        archetypes[sub_trait][2]
    ), unsafe_allow_html=True)

    # Growth Area
    st.markdown(archetype_card(
        lowest_trait,
        f"Growth Area: {lowest_trait}",
        trait_descriptions[lowest_trait]["low"],
        archetypes[lowest_trait][2]
    ), unsafe_allow_html=True)

    # --------------------------
    # Download PDFs
    # --------------------------
    st.subheader("Download PDFs")
    col1, col2 = st.columns(2)

    with col1:
        results_pdf = create_results_pdf(
            creative_perc,
            bigfive_perc,
            trait_descriptions,
            archetypes
        )
        st.download_button(
            "Download Your Results PDF",
            data=results_pdf,
            file_name="creative_results.pdf",
            mime="application/pdf"
        )

    with col2:
        academic_pdf = create_academic_pdf()
        st.download_button(
            "Download Academic Research PDF",
            data=academic_pdf,
            file_name="academic_research.pdf",
            mime="application/pdf"
        )

