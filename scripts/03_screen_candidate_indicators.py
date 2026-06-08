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
    / "candidate_indicator_spearman.csv"
)

df = pd.read_csv(DATA_PATH)

response_vars = [
    "Prod_rel_pct",
    "Prod_rel_ha_pct",
]

candidate_vars = [
    # Phosphorus
    "PM1_mg_dm3",
    "PM1_per_Clay",
    "log_PM1_per_Clay",

    # Enzymatic indicators
    "Beta_glic",
    "Arilsulf",
    "Beta_por_Argila",
    "Aril_por_Argila",
    "GMea",
    "GMea_per_Clay",
    "log_GMea_per_Clay",
    "qGMea",
    "qBeta",
    "qAril",
    "Ativ_Enzimat_Total",
    "Rel_Beta_Aril",
    "Ativ_Enzim_por_MO",

    # Organic matter and texture
    "MO_g_dm3",
    "C_org_g_d3",
    "Argila_g_kg",
    "Areia_g_kg",
    "Silte_g_kg",
    "Ds_g_cm3",

    # Basic fertility / salinity
    "pH",
    "CE_dS_m",
    "Ca_Troc_cmolc_Kg",
    "Mg_Troc_cmolc_Kg",
    "K_Troc_cmolc_Kg",
    "Na_Troc_cmolc_Kg",
    "SB_cmolc_Kg",
    "PST",
]

rows = []

for response in response_vars:
    if response not in df.columns:
        print(f"Warning: response variable not found: {response}")
        continue

    for indicator in candidate_vars:
        if indicator not in df.columns:
            print(f"Warning: candidate variable not found: {indicator}")
            continue

        temp = df[[response, indicator]].dropna()

        if temp.shape[0] < 3:
            rho = None
            p_value = None
            n = temp.shape[0]
        else:
            rho, p_value = spearmanr(temp[indicator], temp[response])
            n = temp.shape[0]

        rows.append(
            {
                "response": response,
                "indicator": indicator,
                "n": n,
                "spearman_rho": rho,
                "p_value": p_value,
                "abs_spearman_rho": abs(rho) if rho is not None else None,
            }
        )

results = pd.DataFrame(rows)

results = results.sort_values(
    by=["response", "abs_spearman_rho"],
    ascending=[True, False],
)

results.to_csv(OUTPUT_PATH, index=False)

print("\nSpearman screening completed.")
print(f"Output file: {OUTPUT_PATH}")

for response in response_vars:
    print("\n" + "=" * 70)
    print(f"Response variable: {response}")
    print("=" * 70)

    subset = results[results["response"] == response].copy()

    print(
        subset[
            [
                "indicator",
                "n",
                "spearman_rho",
                "p_value",
                "abs_spearman_rho",
            ]
        ].head(15).to_string(index=False)
    )
