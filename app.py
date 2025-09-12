import streamlit as st
import matplotlib.pyplot as plt
import io
from fpdf import FPDF

# -------------------------------
# Archetypes and Questions
# -------------------------------
ARCHETYPES = {
    "Explorer": [
        "I enjoy experimenting with new ideas and approaches.",
        "I actively seek out new experiences.",
        "I see creativity as a way to discover the unknown."
    ],
    "Visionary": [
        "I often imagine future possibilities.",
        "I connect abstract ideas into bigger pictures.",
        "I think about long-term impact when being creative."
    ],
    "Inventor": [
        "I like solving practical problems in novel ways.",
        "I often build or design new things.",
        "I enjoy finding clever fixes to everyday challenges."
    ],
    "Artist": [
        "I express myself through creative outlets.",
        "I value beauty, style, or aesthetics.",
        "I enjoy making things that evoke emotions."
    ],
    "Connector": [
        "I collaborate to spark new ideas.",
        "I enjoy learning from diverse perspectives.",
        "I thrive when bouncing ideas with others."
    ],
    "Analyst": [
        "I use logic and evidence in my creativity.",
        "I enjoy breaking problems into smaller parts.",
        "I like evaluating ideas critically before acting."
    ]
}

TRAIT_COLORS = {
    "Explorer": "#1f77b4",
    "Visionary": "#ff7f0e",
    "Inventor": "#2ca02c",
    "Artist": "#d62728",
    "Connector": "#9467bd",
    "Analyst": "#8c564b",
}

# -------------------------------
# Store responses
# -------------------------------
if "responses" not in st.session_state:
    st.session_state.responses = {
        f"{arch}_{i+1}": None for arch in ARCHETYPES for i in range(len(ARCHETYPES[arch]))
    }

responses = st.session_state.responses
all_questions = [(arch, q) for arch, qs in ARCHETYPES.items() for q in qs]
total_qs = len(all_questions)

# -------------------------------
# App UI
# -------------------------------
st.title("🌀 Creative Identity Profile")
st.write("Answer honestly: **1 = Strongly Disagree** to **5 = Strongly Agree**")

completed = 0
for arch, qs in ARCHETYPES.items():
    st.subheader(arch)
    for i, q in enumerate(qs, start=1):
        key = f"{arch}_{i}"
        prev_val = responses[key]
        responses[key] = st.radio(
            q,
            options=[1, 2, 3, 4, 5],
            index=(prev_val - 1) if prev_val else None,
            horizontal=True,
            key=key,
        )
        if responses[key]:
            completed += 1

progress = completed / total_qs
st.progress(progress)

# -------------------------------
# Process results
# -------------------------------
if completed == total_qs:
    st.success("✅ All questions answered!")

    scores = {
        arch: sum(responses[f"{arch}_{i+1}"] for i in range(len(qs))) / len(qs)
        for arch, qs in ARCHETYPES.items()
    }

    main_trait = max(scores, key=scores.get)
    st.subheader("🌟 Your Creative Identity")
    st.write(f"Your strongest trait is **{main_trait}** with a score of {scores[main_trait]:.2f}/5.")

    # Bar chart
    fig, ax = plt.subplots()
    ax.bar(scores.keys(), scores.values(), color=[TRAIT_COLORS[a] for a in scores.keys()])
    ax.set_ylabel("Average Score")
    ax.set_title("Your Creative Profile")
    plt.xticks(rotation=45)
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    st.image(buf)

    # -------------------------------
    # PDF Generator
    # -------------------------------
    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 14)
            self.cell(0, 10, "Creative Identity Report", ln=True, align="C")
            self.ln(10)

    def create_pdf(scores, main_trait, chart_buf):
        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.multi_cell(0, 10, f"Your strongest trait: {main_trait}\n")

        for trait, score in scores.items():
            level = "High" if score >= 4 else "Moderate" if score >= 2.5 else "Low"
            pdf.multi_cell(0, 10, f"{trait} ({level}): {score:.2f}/5")

        # Chart
        pdf.ln(10)
        chart_buf.seek(0)
        pdf.image(chart_buf, x=10, y=None, w=pdf.w - 20)

        # Return as bytes
        return pdf.output(dest="S").encode("latin-1")

    pdf_bytes = create_pdf(scores, main_trait, buf)

    st.download_button(
        "📥 Download Your Personalised PDF Report",
        data=pdf_bytes,
        file_name="Creative_Identity_Report.pdf",
        mime="application/pdf",
    )
else:
    st.warning("⚠️ Please answer all questions before viewing your profile.")


