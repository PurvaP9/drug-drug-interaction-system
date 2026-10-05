
import gradio as gr

from src.data_loader import load_data
from src.ocr_engine import extract_text_from_image
from src.drug_extractor import extract_drugs_from_text
from src.interaction_engine import (
    create_interaction_lookup,
    check_interactions
)
from src.explanation import add_explanations


# Load data
interactions_df, known_drug_names = load_data()

# Create interaction lookup
interaction_lookup = create_interaction_lookup(
    interactions_df
)


def analyze_prescription(image):

    # OCR
    text = extract_text_from_image(image)

    # Extract medicines
    detected_drugs = extract_drugs_from_text(
        text,
        known_drug_names
    )

    # Check interactions
    interactions = check_interactions(
        detected_drugs,
        interaction_lookup
    )

    # Add explanations
    interactions = add_explanations(
        interactions
    )

    return {
        "ocr_text": text,
        "detected_drugs": detected_drugs,
        "interactions": interactions
    }


def run_analysis(image):

    if image is None:
        return (
            "Please upload a prescription image.",
            "No analysis available."
        )

    result = analyze_prescription(image)

    detected_drugs = result["detected_drugs"]
    interactions = result["interactions"]

    # Detected medicines
    if detected_drugs:

        drugs_text = "\n".join(
            f"✓ {drug.title()}"
            for drug in detected_drugs
        )

    else:

        drugs_text = "No medicines were detected."


    # Known interactions
    known_interactions = [
        item
        for item in interactions
        if item["Level"].lower() != "unknown"
    ]

    unknown_count = sum(
        1
        for item in interactions
        if item["Level"].lower() == "unknown"
    )


    # Format interactions
    interaction_lines = []

    for item in known_interactions:

        drug_1 = item["Drug_1"].title()
        drug_2 = item["Drug_2"].title()
        level = item["Level"].lower()
        explanation = item["Explanation"]

        if level == "major":
            label = "🔴 MAJOR"

        elif level == "moderate":
            label = "🟠 MODERATE"

        elif level == "minor":
            label = "🟡 MINOR"

        else:
            label = level.upper()

        interaction_lines.append(
            f"### {label}\n"
            f"**{drug_1} + {drug_2}**\n\n"
            f"{explanation}\n"
        )


    if interaction_lines:

        interaction_text = "\n".join(
            interaction_lines
        )

    else:

        interaction_text = (
            "### No known interactions found\n\n"
            "No interaction records were found for "
            "these medicine pairs in the available database."
        )


    # Summary
    interaction_text += (
        "\n\n---\n"
        f"**Interactions found:** "
        f"{len(known_interactions)}\n\n"
        f"**Pairs without interaction information:** "
        f"{unknown_count}"
    )


    return (
        drugs_text,
        interaction_text
    )


# Gradio interface
with gr.Blocks(
    title="Drug–Drug Interaction Checker"
) as demo:

    gr.Markdown(
        """
        # 💊 Drug–Drug Interaction Checker

        Upload a prescription image to identify medicines
        and check for known drug–drug interactions.
        """
    )

    image_input = gr.Image(
        type="pil",
        label="Upload Prescription"
    )

    analyze_button = gr.Button(
        "🔍 Analyze Prescription",
        variant="primary"
    )

    gr.Markdown("## Detected Medicines")

    drugs_output = gr.Markdown()

    gr.Markdown("## Interactions Found")

    interactions_output = gr.Markdown()

    gr.Markdown(
        """
        ---

        **Disclaimer:** This tool is for educational and
        informational purposes only. It does not replace
        professional medical advice.
        """
    )

    analyze_button.click(
        fn=run_analysis,
        inputs=image_input,
        outputs=[
            drugs_output,
            interactions_output
        ]
    )


if __name__ == "__main__":
    demo.launch()
