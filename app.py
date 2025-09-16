# --------------------------
# Streamlit App
# --------------------------
st.set_page_config(page_title="Creative Identity Profile", layout="centered")

# Session state
if "page" not in st.session_state:
    st.session_state.page = "Intro"
if "creative_answers" not in st.session_state:
    st.session_state.creative_answers = {}
if "big5_answers" not in st.session_state:
    st.session_state.big5_answers = {}

# --------------------------
# Navigation
# --------------------------
page = st.session_state.page

if page == "Intro":
    st.title("✨ Creative Identity Profile ✨")
    st.write(
        "Discover your **creative identity** and how it aligns with your **personality**. "
        "This profile is based on the **Big Five Personality Traits** and research-driven **creativity traits**."
    )
    if st.button("Start the Quiz ➡️"):
        st.session_state.page = "Creative Traits"

# --------------------------
# Creative Traits Page
# --------------------------
elif page == "Creative Traits":
    st.header("🎨 Creative Traits")
    st.write("Answer honestly based on how much you agree with each statement (1 = strongly disagree, 5 = strongly agree).")

    for trait, questions in creative_traits.items():
        st.subheader(trait)
        for i, q in enumerate(questions):
            key = f"{trait}_{i}"
            st.session_state.creative_answers[key] = st.radio(
                q,
                [1,2,3,4,5],
                index=2,
                horizontal=True,
                key=key
            )

    if st.button("Next ➡️"):
        st.session_state.page = "Big Five Traits"

# --------------------------
# Big Five Traits Page
# --------------------------
elif page == "Big Five Traits":
    st.header("🧠 Big Five Personality Traits")
    st.write("Please respond to each statement (1 = strongly disagree, 5 = strongly agree).")

    for trait, questions in big5_traits.items():
        st.subheader(trait)
        for i, q in enumerate(questions):
            key = f"{trait}_{i}"
            st.session_state.big5_answers[key] = st.radio(
                q,
                [1,2,3,4,5],
                index=2,
                horizontal=True,
                key=key
            )

    if st.button("See Results 📊"):
        st.session_state.page = "Results"

# --------------------------
# Results Page
# --------------------------
elif page == "Results":
    st.title("📊 Your Creative Identity Profile")

    # Calculate scores
    creative_scores = {
        trait: np.mean([st.session_state.creative_answers[f"{trait}_{i}"] for i in range(len(questions))])
        for trait, questions in creative_traits.items()
    }
    big5_scores = {
        trait: np.mean([st.session_state.big5_answers[f"{trait}_{i}"] for i in range(len(questions))])
        for trait, questions in big5_traits.items()
    }

    # Generate radar charts
    chart_buf_creative = radar_chart(creative_scores, creative_colors, "Creative Traits")
    chart_buf_big5 = radar_chart(big5_scores, big5_colors, "Big Five Traits")

    # Example archetypes (placeholder logic)
    archetypes_results = {
        "Primary": {"name": "The Explorer", "description": "You thrive on curiosity and new experiences."},
        "Secondary": {"name": "The Visionary", "description": "You see possibilities where others see problems."},
        "Growth Area": {"name": "The Builder", "improvement": "Focus on consistency and structured follow-through."}
    }

    # Display charts
    st.subheader("Radar Charts")
    col1, col2 = st.columns(2)
    with col1:
        st.image(chart_buf_creative, caption="Creative Traits", use_container_width=True)
    with col2:
        st.image(chart_buf_big5, caption="Big Five Traits", use_container_width=True)

    # Archetypes
    st.subheader("Your Creative Archetypes")
    for label, arch in archetypes_results.items():
        if label == "Growth Area":
            st.markdown(f"**{label}: {arch['name']}** — {arch['improvement']}")
        else:
            st.markdown(f"**{label}: {arch['name']}** — {arch['description']}")

    # Creative Traits Summaries
    st.subheader("Creative Trait Insights")
    for trait, score in creative_scores.items():
        level = get_level(score)
        st.markdown(f"**{trait} ({level}) — {score:.2f}/5**")
        st.write(creative_summaries[trait][level])

    # Big Five Summaries
    st.subheader("Big Five Trait Insights")
    for trait, score in big5_scores.items():
        level = get_level(score)
        st.markdown(f"**{trait} ({level}) — {score:.2f}/5**")
        st.write(big5_summaries[trait][level])

    # Academic Context (Collapsible)
    with st.expander("📚 Scientific & Psychological Background"):
        st.write(
            "This profile combines two evidence-based frameworks: "
            "the **Big Five personality model** and research-driven **creativity traits** "
            "(originality, curiosity, imagination, etc.).\n\n"
            "It is inspired by decades of work in psychology and creativity studies "
            "from **Amabile, Guilford, Torrance, Finke, Ward & Smith, Boden, Sternberg, Runco, and others**. "
            "These traits connect with **divergent thinking**, **convergent thinking**, "
            "and applied creativity in everyday practice."
        )

    # Generate PDF
    pdf_buf = create_pdf(
        creative_scores,
        big5_scores,
        archetypes_results,
        creative_summaries,
        big5_summaries,
        chart_buf_creative,
        chart_buf_big5
    )

    # PDF download
    st.download_button(
        label="📥 Download Your Report (PDF)",
        data=pdf_buf,
        file_name="creative_identity_profile.pdf",
        mime="application/pdf"
    )
