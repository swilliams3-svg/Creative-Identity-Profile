import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
from io import BytesIO
from PIL import Image

# ---------------------------
# PDF creation
# ---------------------------
def create_pdf(scores, main_trait, chart_buf):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)

    pdf.cell(200, 10, "Creative Identity Report", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"Your main creative trait is: {main_trait}")

    pdf.ln(5)
    pdf.set_font("Arial", size=11)
    for trait, (score, level) in scores.items():
        pdf.multi_cell(0, 10, f"{trait} ({level}): {score:.2f}/5")

    # Add chart image to PDF
    chart_buf.seek(0)
    image = Image.open(chart_buf)
    img_bytes = BytesIO()
    image.save(img_bytes, format="PNG")
    img_bytes.seek(0)
    pdf.image(img_bytes, x=10, y=None, w=180)

    return pdf.output(dest="S").encode("latin-1")


# ---------------------------
# Example data
# ---------------------------
scores = {
    "Curiosity": (4.2, "High"),
    "Imagination": (3.7, "Moderate"),
    "Persistence": (4.8, "Very High"),
    "Risk-Taking": (2.9, "Low"),
}
main_trait = "Persistence"

# ---------------------------
# Make chart
# ---------------------------
fig, ax = plt.subplots()
traits = list(scores.keys())
values = [s[0] for s in scores.values()]
ax.bar(traits, values, color="skyblue")
ax.set_ylim(0, 5)
ax.set_ylabel("Score (out of 5)")
ax.set_title("Creative Trait Profile")

chart_buf = BytesIO()
plt.savefig(chart_buf, format="png")
plt.close(fig)

# ---------------------------
# Streamlit UI
# ---------------------------
st.title("Creative Identity Profile")

# ✅ Display chart safely
chart_buf.seek(0)
image = Image.open(chart_buf)
st.image(image, caption="Your Creative Trait Profile", use_container_width=True)

# ✅ Generate PDF
pdf_bytes = create_pdf(scores, main_trait, chart_buf)

# ✅ Download button
st.download_butto_


