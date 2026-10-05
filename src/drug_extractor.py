
import re


def extract_drugs_from_text(text, known_drug_names):

    text = text.lower()

    words = re.findall(
        r"[a-z]+",
        text
    )

    detected_drugs = []

    for word in words:

        if word in known_drug_names:
            detected_drugs.append(word)

    detected_drugs = sorted(
        set(detected_drugs)
    )

    return detected_drugs
