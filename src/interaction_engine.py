
from itertools import combinations


def create_interaction_lookup(interactions_df):

    interaction_lookup = dict(
        zip(
            zip(
                interactions_df["Drug_1"],
                interactions_df["Drug_2"]
            ),
            interactions_df["Level"]
        )
    )

    return interaction_lookup


def get_interaction(
    drug_1,
    drug_2,
    interaction_lookup
):

    drug_1 = drug_1.lower().strip()
    drug_2 = drug_2.lower().strip()

    pair = tuple(
        sorted([drug_1, drug_2])
    )

    return interaction_lookup.get(
        pair,
        "unknown"
    )


def check_interactions(
    drugs,
    interaction_lookup
):

    cleaned_drugs = sorted(
        set(
            drug.lower().strip()
            for drug in drugs
            if drug.strip()
        )
    )

    drug_pairs = combinations(
        cleaned_drugs,
        2
    )

    results = []

    for drug_1, drug_2 in drug_pairs:

        level = interaction_lookup.get(
            (drug_1, drug_2),
            "unknown"
        )

        results.append({
            "Drug_1": drug_1,
            "Drug_2": drug_2,
            "Level": level
        })

    return results
