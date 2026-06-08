from pathlib import Path

import pandas as pd
from scipy.stats import spearmanr


PROJECT_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "private"
    / "soil_quality_processed_private.csv"
)

OUTPUT_PATH = (
    PROJECT_DIR
    / "tables"
    / "private"
    / "family_indicator_comparison.csv"
)

df = pd.read_csv(DATA_PATH)

response_vars = [
    "Prod_rel_pct",
    "Prod_rel_ha_pct",
]

indicator_families = {
    "phosphorus_availability": [
        "PM1_mg_dm3",
        "PM1_per_Clay",
        "log_PM1_per_Clay",
    ],
    "integrated_enzyme_activity": [
        "GMea",
        "GMea_per_Clay",
        "log_GMea_per_Clay",
        "Ativ_Enzimat_Total",
        "Ativ_Enzim_por_MO",
        "qGMea",
    ],
    "beta_glucosidase": [
        "Beta_glic",
        "Beta_por_Argila",
        "qBeta",
    ],
    "arylsulfatase": [
        "Arilsulf",
        "Aril_por_Argila",
        "qAril",
    ],
    "organic_matter_carbon": [
        "MO_g_dm3",
        "C_org_g_d3",
        "Est_C_Mg_ha",
    ],
    "texture_physical": [
        "Argila_g_kg",
        "Areia_g_kg",
        "Silte_g_kg",
        "ADA_g_kg",
        "Floculacao_pct",
        "Dispercao_pct",
        "Ds_g_cm3",
    ],
    "exchangeable_bases": [
        "Ca_Troc_cmolc_Kg",
        "Mg_Troc_cmolc_Kg",
        "K_Troc_cmolc_Kg",
        "Na_Troc_cmolc_Kg",
        "SB_cmolc_Kg",
        "PST",
    ],
}

rows = []

for response in response_vars:
    if response not in df.columns:
        print(f"Warning: response variable not found: {response}")
        continue

    for family, indicators in indicator_families.items():
        for indicator in indicators:
            if indicator not in df.columns:
                print(f"Warning: indicator not found: {indicator}")
                continue

            temp = df[[response, indicator]].dropna()
            n = temp.shape[0]

            if n < 3:
                rho = None
                p_value = None
            else:
                rho, p_value = spearmanr(temp[indicator], temp[response])

            rows.append(
                {
                    "response": response,
                    "family": family,
                    "indicator": indicator,
                    "n": n,
                    "spearman_rho": rho,
                    "abs_spearman_rho": abs(rho) if rho is not None else None,
                    "p_value": p_value,
                }
            )

results = pd.DataFrame(rows)

results = results.sort_values(
    by=["response", "family", "abs_spearman_rho"],
    ascending=[True, True, False],
)

results.to_csv(OUTPUT_PATH, index=False)

print("\nFamily-level indicator comparison completed.")
print(f"Output file: {OUTPUT_PATH}")

for response in response_vars:
    print("\n" + "=" * 80)
    print(f"Response variable: {response}")
    print("=" * 80)

    response_results = results[results["response"] == response]

    for family in indicator_families:
        family_results = response_results[
            response_results["family"] == family
        ].copy()

        if family_results.empty:
            continue

        print("\n" + family)
        print("-" * len(family))

        print(
            family_results[
                [
                    "indicator",
                    "n",
                    "spearman_rho",
                    "p_value",
                    "abs_spearman_rho",
                ]
            ].to_string(index=False)
        )
