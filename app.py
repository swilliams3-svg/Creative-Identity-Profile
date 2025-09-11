def assign_profile(traits):
    # sort traits from highest to lowest
    sorted_traits = sorted(traits.items(), key=lambda x: x[1], reverse=True)
    top_trait, top_score = sorted_traits[0]
    second_trait, second_score = sorted_traits[1]

    # thresholds (adjustable)
    HIGH = 15

    # Two-trait archetypes
    if top_trait == "Imagination" and second_trait == "Curiosity":
        return ("Visionary Dreamer",
                "You see possibilities others don’t. You love exploring 'what ifs' and imagining bold futures.",
                "Ground your visions by sketching or prototyping them.")
    elif top_trait == "Curiosity" and second_trait == "Persistence":
        return ("Analytical Builder",
                "You dig deep, ask hard questions, and keep working until solutions appear.",
                "Balance analysis with playful exploration.")
    elif top_trait == "Risk-taking" and second_trait == "Imagination":
        return ("Bold Experimenter",
                "You embrace uncertainty and jump into new ideas with courage.",
                "Structure your experiments to learn quickly from failure.")
    elif top_trait == "Social Sensitivity" and second_trait == "Persistence":
        return ("Collaborative Connector",
                "You thrive in groups, amplifying and shaping ideas with empathy.",
                "Make space to share your own voice alongside supporting others.")
    elif top_trait == "Curiosity" and second_trait == "Risk-taking":
        return ("Strategic Innovator",
                "You explore new fields and act decisively on discoveries.",
                "Balance speed with deeper reflection before moving on.")
    elif top_trait == "Imagination" and second_trait == "Social Sensitivity":
        return ("Playful Improviser",
                "You love spontaneous creativity, games, and improvisation with others.",
                "Add structure to channel playful sparks into lasting results.")

    # Single-trait archetypes
    if top_trait == "Imagination":
        return ("Imaginative Storyteller",
                "You love narrative, symbolism, and creating new worlds.",
                "Transform stories into action or products.")
    elif top_trait == "Curiosity":
        return ("Inquisitive Explorer",
                "You are energized by questions, new information, and discovery.",
                "Narrow focus at times to turn curiosity into creations.")
    elif top_trait == "Risk-taking":
        return ("Fearless Challenger",
                "You thrive on breaking rules and disrupting the status quo.",
                "Learn when to take calculated risks versus when to pause.")
    elif top_trait == "Persistence":
        return ("Resilient Maker",
                "You stick with creative work through obstacles and setbacks.",
                "Pair persistence with reflection to avoid burnout.")
    elif top_trait == "Social Sensitivity":
        return ("Empathic Creator",
                "You tune into people’s needs and create with empathy at the core.",
                "Pair empathy with boldness to push ideas further.")

    # Balanced fallback
    return ("Grounded Realist",
            "You integrate imagination, persistence, and empathy in steady ways.",
            "Push beyond comfort zones to discover new strengths.")

