
def get_explanation(level):

    explanations = {
        "major":
            "This is classified as a major interaction. "
            "The combination may require immediate medical attention "
            "or professional medical advice.",

        "moderate":
            "This is classified as a moderate interaction. "
            "The combination may require monitoring or consultation "
            "with a healthcare professional.",

        "minor":
            "This is classified as a minor interaction. "
            "The interaction is generally considered lower risk, "
            "but appropriate monitoring may still be required.",

        "unknown":
            "No interaction information was found for this pair "
            "in the available database. This does not necessarily "
            "mean that no interaction exists."
    }

    return explanations.get(
        level.lower(),
        "No explanation is available for this interaction level."
    )


def add_explanations(interactions):

    results = []

    for interaction in interactions:

        level = interaction["Level"]

        results.append({
            "Drug_1": interaction["Drug_1"],
            "Drug_2": interaction["Drug_2"],
            "Level": level,
            "Explanation": get_explanation(level)
        })

    return results
