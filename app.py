import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth

st.set_page_config(page_title="Creative Identity Profile", layout="centered")

# --------------------------
# Questions (Creative + Big Five)
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
# Colour palettes (distinct)
# --------------------------
creative_colors = {
    "Originality": "#D7263D",
    "Curiosity": "#FF9A56",
    "Risk-Taking": "#FFB400",
    "Imagination": "#8E44AD",
    "Discipline": "#2E86AB",
    "Collaboration": "#1B998B",
}

big5_colors = {
    "Openness": "#084887",
    "Conscientiousness": "#05668D",
    "Extraversion": "#028090",
    "Agreeableness": "#00A896",
    "Neuroticism": "#02C39A",
}

# --------------------------
# Simple summaries (High/Medium/Low)
# --------------------------
def make_summaries(traits):
    s = {}
    for t in traits:
        s[t] = {
            "High": f"You score high on {t}. This suggests it is a relative strength — something you rely on in creative situations.",
            "Medium": f"You have a moderate level of {t}. You can bring this trait into play depending on context.",
            "Low": f"This appears to be a growth area. You may benefit from targeted practice to strengthen {t.lower()}."
        }
    return s

creative_summaries = make_summaries(creative_traits.keys())
big5_summaries = make_summaries(big_five_traits.keys())

# --------------------------
# Helper functions
# --------------------------
def get_level(score):
    # score between 1 and 5
    if score >= 4.0:
        return "High"
    elif score >= 2.5:
        return "Medium"
    else:
        return "Low"


def wrap_text(c, text, x, y, max_width, font="Helvetica", font_size=10, leading=12):
    c.setFont(font, font_size)
    words = text.split()
    line = ""
    for word in words:
        test_line = f"{line} {word}".strip()
        if stringWidth(test_line, font, font_size) <= max_width:
            line = test_line
        else:
            c.drawString(x, y, line)
            y -= leading
            line = word
    if line:
        c.drawString(x, y, line)
        y -= leading
    return y


def ensure_space(c, y, needed, width, height, margin=50):
    if y - needed < margin:
        c.showPage()
        return height - margin
    return y

# --------------------------
# Archetype definitions
# --------------------------
archetype_library = {
    "Originality": {"name": "The Innovator", "description": "Generates unusual and novel ideas; enjoys originality.", "improvement": "Try deliberate idea-combining exercises and constraints to channel novelty into useful outcomes."},
    "Curiosity": {"name": "The Explorer", "description": "Seeks knowledge and new experiences; asks questions.", "improvement": "Schedule time for deliberate exploration and cross-domain learning to broaden perspectives."},
    "Risk-Taking": {"name": "The Adventurer", "description": "Comfortable testing boundaries and experimenting.", "improvement": "Start with small experiments to build confidence and learn from manageable failures."},
    "Imagination": {"name": "The Dreamer", "description": "Envisions possibilities and uses rich mental imagery.", "improvement": "Use visualization and scenario-play to refine and test imagined ideas."},
    "Discipline": {"name": "The Builder", "description": "Brings ideas to completion through structure and persistence.", "improvement": "Adopt micro-goals and routines to maintain momentum on long projects."},
    "Collaboration": {"name": "The Connector", "description": "Thrives on social exchange and co-creation.", "improvement": "Practice structured feedback cycles and role-rotations to deepen collaborative skills."}
}

# --------------------------
# PDF generation function
# --------------------------
def create_pdf(
    creative_scores,
    big5_scores,
    archetypes_data,
    creative_summaries,
    big5_summaries,
    chart_buf_creative,
    chart_buf_big5,
    creative_colors,
    big5_colors,
    academic_text,
    references
):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    width, height = A4
    margin = 50

    # --- Intro / Science Page ---
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, height - 60, "The Science Behind the Creative Identity & Personality Profile")
    y = height - 100
    y = wrap_text(c, academic_text.split('

', 1)[0], margin, y, max_width=width - 2*margin, font_size=11, leading=14)

    # write the sections (we'll write the full academic_text split by double newlines)
    parts = academic_text.split('

')
    # start from second paragraph
    for part in parts[1:]:
        title_line = part.split('
',1)[0]
        content = part[len(title_line):].strip()
        if title_line.strip():
            c.setFont("Helvetica-Bold", 12)
            y -= 8
            y = ensure_space(c, y, 80, width, height, margin)
            c.drawString(margin, y, title_line)
            y -= 16
        if content:
            y = ensure_space(c, y, 80, width, height, margin)
            y = wrap_text(c, content, margin+10, y, max_width=width - 2*(margin+10), font_size=10, leading=13)

    c.showPage()

    # --- Results Page ---
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, height - 40, "Creative Identity & Personality Profile: Results")
    y = height - 80

    # Draw charts
    try:
        img1 = ImageReader(chart_buf_creative)
        img2 = ImageReader(chart_buf_big5)
        chart_w = 220
        chart_h = 220
        c.drawImage(img1, margin, y - chart_h, width=chart_w, height=chart_h, preserveAspectRatio=True, mask='auto')
        c.drawImage(img2, margin + chart_w + 40, y - chart_h, width=chart_w, height=chart_h, preserveAspectRatio=True, mask='auto')
    except Exception:
        pass

    y = y - chart_h - 20

    # Archetypes
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, "Your Creative Archetypes")
    y -= 18
    for label, arch in archetypes_data.items():
        c.setFont("Helvetica-Bold", 11)
        trait = arch['trait']
        hexc = creative_colors.get(trait, "#000000")
        r, g, b = [int(hexc.lstrip('#')[i:i+2], 16)/255 for i in (0,2,4)]
        c.setFillColorRGB(r, g, b)
        c.drawString(margin+10, y, f"{label}: {arch['name']}")
        c.setFillColorRGB(0,0,0)
        c.setFont("Helvetica", 10)
        y = wrap_text(c, arch['description'] if label != 'Growth Area' else arch['improvement'], margin+20, y-12, max_width=width - 2*(margin+20), font_size=9, leading=12)
        y -= 6
        y = ensure_space(c, y, 60, width, height, margin)

    # Creative Trait Insights
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, "Creative Trait Insights")
    y -= 18
    for trait, score in creative_scores.items():
        y = ensure_space(c, y, 60, width, height, margin)
        level = get_level(score)
        hexc = creative_colors.get(trait, "#000000")
        r, g, b = [int(hexc.lstrip('#')[i:i+2], 16)/255 for i in (0,2,4)]
        c.setFont("Helvetica-Bold", 10)
        c.setFillColorRGB(r,g,b)
        c.drawString(margin+10, y, f"{trait} ({level}) — {score:.2f}/5")
        c.setFillColorRGB(0,0,0)
        c.setFont("Helvetica", 9)
        y = wrap_text(c, creative_summaries[trait][level], margin+20, y-12, max_width=width - 2*(margin+20), font_size=9, leading=12)
        y -= 6

    # Big Five Trait Insights
    y = ensure_space(c, y, 120, width, height, margin)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, "Big Five Trait Insights")
    y -= 18
    for trait, score in big5_scores.items():
        y = ensure_space(c, y, 60, width, height, margin)
        level = get_level(score)
        hexc = big5_colors.get(trait, "#000000")
        r, g, b = [int(hexc.lstrip('#')[i:i+2], 16)/255 for i in (0,2,4)]
        c.setFont("Helvetica-Bold", 10)
        c.setFillColorRGB(r,g,b)
        c.drawString(margin+10, y, f"{trait} ({level}) — {score:.2f}/5")
        c.setFillColorRGB(0,0,0)
        c.setFont("Helvetica", 9)
        y = wrap_text(c, big5_summaries[trait][level], margin+20, y-12, max_width=width - 2*(margin+20), font_size=9, leading=12)
        y -= 6

    c.showPage()

    # Academic / References page
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, height - 40, "Academic Foundations & References")
    y = height - 80
    for ref in references:
        y = ensure_space(c, y, 40, width, height, margin)
        y = wrap_text(c, u"• " + ref, margin+10, y, max_width=width - 2*(margin+10), font_size=10, leading=13)

    c.save()
    buf.seek(0)
    return buf

# --------------------------
# Radar plotting (returns buffer)
# --------------------------
def plot_radar(scores, title, fill_color, line_color):
    labels = list(scores.keys())
    values = list(scores.values())
    values += values[:1]
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(polar=True))
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_rlabel_position(180 / len(labels))
    ax.plot(angles, values, color=line_color, linewidth=2)
    ax.fill(angles, values, color=fill_color, alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_ylim(1,5)
    ax.set_yticks([1,2,3,4,5])
    ax.set_yticklabels(['1','2','3','4','5'])
    ax.set_title(title, pad=15)

    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    return buf

# --------------------------
# Streamlit App Flow
# --------------------------
if "page" not in st.session_state:
    st.session_state.page = "intro"

# keys for questions (ensures consistent session state keys)
all_questions = []
for t, qs in creative_traits.items():
    for i, q in enumerate(qs):
        all_questions.append((t, q, f"q_cre_{t}_{i}"))
for t, qs in big_five_traits.items():
    for i, q in enumerate(qs):
        all_questions.append((t, q, f"q_big_{t}_{i}"))

# ensure default values exist
for _t, _q, _k in all_questions:
    if _k not in st.session_state:
        st.session_state[_k] = 3

if st.session_state.page == "intro":
    st.title("Creative Identity & Personality Profile")
    st.markdown("""
    This quiz integrates validated psychological frameworks with applied creativity theory, providing a structured but engaging way to reflect on creative strengths and tendencies.

    • Answer each statement using the 1–5 scale (1 = Strongly Disagree, 5 = Strongly Agree).
    • The report combines measures of creative traits with the Big Five personality model.
    """)
    if st.button("Start Quiz"):
        st.session_state.page = "quiz"
        st.experimental_rerun()

elif st.session_state.page == "quiz":
    st.header("Quiz")
    with st.form("quiz_form"):
        st.subheader("Creative Traits")
        for t, qs in creative_traits.items():
            st.markdown(f"**{t}**")
            for i, q in enumerate(qs):
                key = f"q_cre_{t}_{i}"
                st.radio(q, (1,2,3,4,5), key=key, horizontal=True)

        st.subheader("Big Five Traits")
        for t, qs in big_five_traits.items():
            st.markdown(f"**{t}**")
            for i, q in enumerate(qs):
                key = f"q_big_{t}_{i}"
                st.radio(q, (1,2,3,4,5), key=key, horizontal=True)

        submitted = st.form_submit_button("Submit")
        if submitted:
            st.session_state.page = "results"
            st.experimental_rerun()

else:  # results
    st.header("Your Results")

    # compute scores
    creative_scores = {}
    for t, qs in creative_traits.items():
        vals = [st.session_state[f"q_cre_{t}_{i}"] for i in range(len(qs))]
        creative_scores[t] = float(np.mean(vals))

    big5_scores = {}
    for t, qs in big_five_traits.items():
        vals = [st.session_state[f"q_big_{t}_{i}"] for i in range(len(qs))]
        big5_scores[t] = float(np.mean(vals))

    # archetype mapping
    sorted_creative = sorted(creative_scores.items(), key=lambda x: x[1], reverse=True)
    primary_trait, _ = sorted_creative[0]
    secondary_trait, _ = sorted_creative[1]
    growth_trait, _ = sorted(creative_scores.items(), key=lambda x: x[1])[0]

    archetypes_data = {
        "Primary Archetype": {"trait": primary_trait, "name": archetype_library[primary_trait]['name'], "description": archetype_library[primary_trait]['description']},
        "Secondary Archetype": {"trait": secondary_trait, "name": archetype_library[secondary_trait]['name'], "description": archetype_library[secondary_trait]['description']},
        "Growth Area": {"trait": growth_trait, "name": archetype_library[growth_trait]['name'], "description": archetype_library[growth_trait]['description'], "improvement": archetype_library[growth_trait]['improvement']}
    }

    # show archetypes
    cols = st.columns(3)
    labels = ["Primary Archetype", "Secondary Archetype", "Growth Area"]
    for col, lab in zip(cols, labels):
        with col:
            data = archetypes_data[lab]
            col.markdown(f"### {lab}")
            col.markdown(f"**{data['name']}**")
            col.write(data['description'])
            if lab == 'Growth Area':
                col.write("Improvement suggestion:")
                col.write(data['improvement'])

    # plot charts and keep buffers
    chart_buf_cre = plot_radar(creative_scores, "Creative Traits", fill_color='#E56B6F', line_color='#C5283D')
    chart_buf_big = plot_radar(big5_scores, "Big Five", fill_color='#4DA1A9', line_color='#05668D')

    st.subheader("Charts")
    c1, c2 = st.columns(2)
    with c1:
        st.image(chart_buf_big)
    with c2:
        st.image(chart_buf_cre)

    # show trait summaries
    st.subheader("Creative Trait Insights")
    for trait, score in creative_scores.items():
        level = get_level(score)
        st.markdown(f"**{trait}** — {level} ({score:.2f}/5)")
        st.write(creative_summaries[trait][level])

    st.subheader("Big Five Insights")
    for trait, score in big5_scores.items():
        level = get_level(score)
        st.markdown(f"**{trait}** — {level} ({score:.2f}/5)")
        st.write(big5_summaries[trait][level])

    # Academic section in app (collapsible)
    academic_text = """
The Creative Identity & Personality Profile was designed by drawing upon established research in both creativity studies and personality psychology. The quiz integrates validated psychological frameworks with applied creativity theory, providing participants with a structured but engaging way to reflect on their creative strengths and tendencies.

Creative Traits
Research shows that creativity is not a single skill, but a combination of dispositions, habits, and mindsets (Runco & Jaeger, 2012; Amabile, 1996; Sternberg, 2006). Six traits were selected for this quiz, each reflecting well-documented components of creative behaviour:

Originality – the ability to generate novel and unconventional ideas (Guilford, 1950).
Curiosity – openness to questioning and exploring new concepts (Kashdan et al., 2004).
Risk-Taking – willingness to tolerate uncertainty and possible failure (Beghetto, 2009).
Imagination – capacity for mental imagery and envisioning possibilities (Vygotsky, 2004).
Discipline – persistence, effort, and self-regulation in creative work (Torrance, 1974).
Collaboration – social interaction and exchange as enablers of creativity (Sawyer, 2012).

The quiz items for these traits are inspired by creativity assessments such as the Torrance Tests of Creative Thinking (TTCT), Amabile’s Consensual Assessment Technique, and contemporary studies on creative personality characteristics.

Big Five Personality Dimensions
The second foundation of the quiz is the Big Five Personality Model (Costa & McCrae, 1992), one of the most extensively validated models in psychology. The five dimensions—Openness, Conscientiousness, Extraversion, Agreeableness, and Neuroticism—are consistently linked with life outcomes, behaviour, and creativity.

Among these, Openness to Experience is most strongly correlated with creative thinking and divergent idea generation (Feist, 1998). Conscientiousness supports sustained effort and organisation in creative projects, while Extraversion, Agreeableness, and Neuroticism influence collaborative style, emotional resilience, and social creativity (Puryear, Kettler & Rinn, 2017).

Archetypes and Feedback
To make psychological feedback more engaging and applicable, the quiz uses creative archetypes (e.g., The Innovator, The Dreamer, The Explorer). Archetype-based feedback is grounded in narrative psychology and coaching practice, translating abstract psychological data into identities that are easier to relate to and apply in personal growth contexts (McAdams, 1993).

Trait scores are grouped into three categories (High, Medium, Low), reflecting established reporting practices in self-assessment psychology. This approach allows participants to situate themselves along a continuum, rather than being assigned fixed labels.

Why Self-Report?
While no single tool can capture the full complexity of creativity, self-report questionnaires are widely used in both psychological research and applied contexts. They allow individuals to reflect on their experiences and tendencies, and when combined with validated frameworks, they provide reliable insight into personality and creative behaviour (Silvia et al., 2012).

Conclusion
This quiz sits at the intersection of creativity research and personality psychology. By combining trait-based creativity insights with the Big Five model, it provides participants with a nuanced profile of their creative identity—balancing novelty, imagination, and risk-taking with personality dispositions that shape how creativity is expressed and developed.

References
Amabile, T. M. (1996). Creativity in Context. Westview Press.
Beghetto, R. A. (2009). Correlates of intellectual risk taking in elementary school science. Journal of Research in Science Teaching, 46(2), 210–223.
Costa, P. T., & McCrae, R. R. (1992). Revised NEO Personality Inventory (NEO-PI-R) and NEO Five-Factor Inventory (NEO-FFI) professional manual. Psychological Assessment Resources.
Feist, G. J. (1998). A meta-analysis of personality in scientific and artistic creativity. Personality and Social Psychology Review, 2(4), 290–309.
Guilford, J. P. (1950). Creativity. American Psychologist, 5(9), 444–454.
Kashdan, T. B., Rose, P., & Fincham, F. D. (2004). Curiosity and exploration: Facilitating positive subjective experiences and personal growth opportunities. Journal of Personality Assessment, 82(3), 291–305.
McAdams, D. P. (1993). The Stories We Live By: Personal Myths and the Making of the Self. Guilford Press.
Puryear, J. S., Kettler, T., & Rinn, A. N. (2017). Relationships of personality to differential conceptions of creativity: A systematic review. Psychology of Aesthetics, Creativity, and the Arts, 11(1), 59–68.
Runco, M. A., & Jaeger, G. J. (2012). The standard definition of creativity. Creativity Research Journal, 24(1), 92–96.
Sawyer, R. K. (2012). Explaining Creativity: The Science of Human Innovation (2nd ed.). Oxford University Press.
Silvia, P. J., Kaufman, J. C., & Pretz, J. E. (2012). The Cambridge Handbook of Creativity Assessment. In J. C. Kaufman & R. J. Sternberg (Eds.), The Cambridge Handbook of Creativity (pp. 635–661). Cambridge University Press.
Sternberg, R. J. (2006). The Nature of Creativity. Cambridge University Press.
Torrance, E. P. (1974). Torrance Tests of Creative Thinking: Norms-technical manual. Personnel Press.
Vygotsky, L. S. (2004). Imagination and Creativity in Childhood. Journal of Russian and East European Psychology, 42(1), 7–97.
"""
    references = [
        "Amabile, T. M. (1996). Creativity in Context. Westview Press.",
        "Beghetto, R. A. (2009). Correlates of intellectual risk taking in elementary school science. Journal of Research in Science Teaching, 46(2), 210–223.",
        "Costa, P. T., & McCrae, R. R. (1992). Revised NEO Personality Inventory (NEO-PI-R) and NEO Five-Factor Inventory (NEO-FFI) professional manual. Psychological Assessment Resources.",
        "Feist, G. J. (1998). A meta-analysis of personality in scientific and artistic creativity. Personality and Social Psychology Review, 2(4), 290–309.",
        "Guilford, J. P. (1950). Creativity. American Psychologist, 5(9), 444–454.",
        "Kashdan, T. B., Rose, P., & Fincham, F. D. (2004). Curiosity and exploration. Journal of Personality Assessment, 82(3), 291–305.",
        "McAdams, D. P. (1993). The Stories We Live By: Personal Myths and the Making of the Self. Guilford Press.",
        "Puryear, J. S., Kettler, T., & Rinn, A. N. (2017). Relationships of personality to differential conceptions of creativity. Psychology of Aesthetics, Creativity, and the Arts, 11(1), 59–68.",
        "Runco, M. A., & Jaeger, G. J. (2012). The standard definition of creativity. Creativity Research Journal, 24(1), 92–96.",
        "Sawyer, R. K. (2012). Explaining Creativity: The Science of Human Innovation (2nd ed.). Oxford University Press.",
        "Silvia, P. J., Kaufman, J. C., & Pretz, J. E. (2012). The Cambridge Handbook of Creativity Assessment. Cambridge University Press.",
        "Sternberg, R. J. (2006). The Nature of Creativity. Cambridge University Press.",
        "Torrance, E. P. (1974). Torrance Tests of Creative Thinking. Personnel Press.",
        "Vygotsky, L. S. (2004). Imagination and Creativity in Childhood. Journal of Russian and East European Psychology, 42(1), 7–97."
    ]

    # create PDF buffer
    pdf_buf = create_pdf(
        creative_scores,
        big5_scores,
        archetypes_data,
        creative_summaries,
        big5_summaries,
        chart_buf_cre,
        chart_buf_big,
        creative_colors,
        big5_colors,
        academic_text,
        references
    )

    st.download_button("Download full PDF report", pdf_buf.getvalue(), "creative_identity_profile.pdf", "application/pdf")

    # option to restart
    if st.button("Retake Quiz"):
        # reset numeric answers to default 3
        for _t, _q, _k in all_questions:
            st.session_state[_k] = 3
        st.session_state.page = "intro"
        st.experimental_rerun()
