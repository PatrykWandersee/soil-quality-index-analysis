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
    / "sqi_candidate_set_comparison.csv"
)

df = pd.read_csv(DATA_PATH)

response_vars = [
    "Prod_rel_pct",
    "Prod_rel_ha_pct",
]

candidate_sets = {
    "MDS11_main": [
        "MO_g_dm3",
        "GMea",
        "Arilsulf",
        "Ca_Troc_cmolc_Kg",
        "K_Troc_cmolc_Kg",
        "Floculacao_pct",
        "Ds_g_cm3",
        "PST",
        "PM1_mg_dm3",
        "pH",
        "CE_dS_m",
    ],
    "MDS12_sodicity": [
        "MO_g_dm3",
        "GMea",
        "Arilsulf",
        "Ca_Troc_cmolc_Kg",
        "K_Troc_cmolc_Kg",
        "Floculacao_pct",
        "Ds_g_cm3",
        "PST",
        "Na_Troc_cmolc_Kg",
        "PM1_mg_dm3",
        "pH",
        "CE_dS_m",
    ],
    "MDS12_clay": [
        "MO_g_dm3",
        "GMea",
        "Arilsulf",
        "Ca_Troc_cmolc_Kg",
        "K_Troc_cmolc_Kg",
        "Floculacao_pct",
        "Ds_g_cm3",
        "PST",
        "Argila_g_kg",
        "PM1_mg_dm3",
        "pH",
        "CE_dS_m",
    ],
    "MDS12_sand": [
        "MO_g_dm3",
        "GMea",
        "Arilsulf",
        "Ca_Troc_cmolc_Kg",
        "K_Troc_cmolc_Kg",
        "Floculacao_pct",
        "Ds_g_cm3",
        "PST",
        "Areia_g_kg",
        "PM1_mg_dm3",
        "pH",
        "CE_dS_m",
    ],
}

# Conservative exploratory scoring.
# CE is treated as "less is better" because it represents salinity risk,
# even though in this dataset it may partly behave as a fertility proxy.
directions = {
    "MO_g_dm3": "more_is_better",
    "GMea": "more_is_better",
    "Arilsulf": "more_is_better",
    "Ca_Troc_cmolc_Kg": "more_is_better",
    "K_Troc_cmolc_Kg": "more_is_better",
    "Floculacao_pct": "more_is_better",
    "Ds_g_cm3": "less_is_better",
    "PST": "less_is_better",
    "Na_Troc_cmolc_Kg": "less_is_better",
    "PM1_mg_dm3": "more_is_better",
    "pH": "more_is_better",
    "CE_dS_m": "less_is_better",
    "Argila_g_kg": "more_is_better",
    "Areia_g_kg": "less_is_better",
}


def minmax_score(series, direction):
    minimum = series.min()
    maximum = series.max()

    if maximum == minimum:
        return pd.Series(1.0, index=series.index)

    if direction == "more_is_better":
        return (series - minimum) / (maximum - minimum)

    if direction == "less_is_better":
        return (maximum - series) / (maximum - minimum)

    raise ValueError(f"Unknown direction: {direction}")


rows = []

for set_name, indicators in candidate_sets.items():
    missing = [indicator for indicator in indicators if indicator not in df.columns]
    if missing:
        raise ValueError(f"Missing indicators in {set_name}: {missing}")

    scores = pd.DataFrame(index=df.index)

    for indicator in indicators:
        scores[f"{indicator}_score"] = minmax_score(
            df[indicator],
            directions[indicator],
        )

    sqi_col = f"{set_name}_SQI"
    scores[sqi_col] = scores.mean(axis=1)

    for response in response_vars:
        temp = pd.concat([scores[sqi_col], df[response]], axis=1).dropna()
        rho, p_value = spearmanr(temp[sqi_col], temp[response])

        rows.append(
            {
                "candidate_set": set_name,
                "n_indicators": len(indicators),
                "response": response,
                "n": temp.shape[0],
                "spearman_rho": rho,
                "p_value": p_value,
                "indicators": "; ".join(indicators),
            }
        )

results = pd.DataFrame(rows)

results = results.sort_values(
    by=["response", "spearman_rho"],
    ascending=[True, False],
)

results.to_csv(OUTPUT_PATH, index=False)

print("\nSQI candidate set comparison completed.")
print(f"Output file: {OUTPUT_PATH}")

for response in response_vars:
    print("\n" + "=" * 80)
    print(f"Response variable: {response}")
    print("=" * 80)

    subset = results[results["response"] == response]

    print(
        subset[
            [
                "candidate_set",
                "n_indicators",
                "n",
                "spearman_rho",
                "p_value",
            ]
        ].to_string(index=False, float_format="{:.5f}".format)
    )
