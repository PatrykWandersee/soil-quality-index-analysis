from pathlib import Path
from itertools import combinations

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

OUTPUT_DIR = PROJECT_DIR / "tables" / "private"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CORRELATION_MATRIX_PATH = OUTPUT_DIR / "candidate_indicator_spearman_matrix.csv"
HIGH_CORRELATION_PAIRS_PATH = OUTPUT_DIR / "highly_correlated_indicator_pairs.csv"

df = pd.read_csv(DATA_PATH)

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

    # Organic matter and carbon
    "MO_g_dm3",
    "C_org_g_d3",

    # Texture and physical indicators
    "Argila_g_kg",
    "Areia_g_kg",
    "Silte_g_kg",
    "ADA_g_kg",
    "Floculacao_pct",
    "Dispercao_pct",
    "Ds_g_cm3",

    # Fertility and salinity
    "pH",
    "CE_dS_m",
    "Ca_Troc_cmolc_Kg",
    "Mg_Troc_cmolc_Kg",
    "K_Troc_cmolc_Kg",
    "Na_Troc_cmolc_Kg",
    "SB_cmolc_Kg",
    "PST",
]

candidate_vars = [var for var in candidate_vars if var in df.columns]

corr_matrix = df[candidate_vars].corr(method="spearman")
corr_matrix.to_csv(CORRELATION_MATRIX_PATH)

rows = []

for var_1, var_2 in combinations(candidate_vars, 2):
    temp = df[[var_1, var_2]].dropna()

    if temp.shape[0] < 3:
        continue

    rho, p_value = spearmanr(temp[var_1], temp[var_2])

    rows.append(
        {
            "indicator_1": var_1,
            "indicator_2": var_2,
            "n": temp.shape[0],
            "spearman_rho": rho,
            "abs_spearman_rho": abs(rho),
            "p_value": p_value,
        }
    )

pairs = pd.DataFrame(rows)

high_pairs = pairs[pairs["abs_spearman_rho"] >= 0.80].copy()
high_pairs = high_pairs.sort_values(
    by="abs_spearman_rho",
    ascending=False,
)

high_pairs.to_csv(HIGH_CORRELATION_PAIRS_PATH, index=False)

print("\nIndicator redundancy analysis completed.")
print(f"Candidate indicators: {len(candidate_vars)}")
print(f"Correlation matrix: {CORRELATION_MATRIX_PATH}")
print(f"Highly correlated pairs: {HIGH_CORRELATION_PAIRS_PATH}")

print("\nHighly correlated pairs | Spearman |rho| >= 0.80")
print("=" * 70)

if high_pairs.empty:
    print("No highly correlated pairs found.")
else:
    print(
        high_pairs[
            [
                "indicator_1",
                "indicator_2",
                "n",
                "spearman_rho",
                "p_value",
            ]
        ].to_string(index=False)
    )

print("\nMost redundant indicators by number of high-correlation links")
print("=" * 70)

if high_pairs.empty:
    print("No redundancy count available.")
else:
    counts_1 = high_pairs["indicator_1"].value_counts()
    counts_2 = high_pairs["indicator_2"].value_counts()
    redundancy_counts = (
        counts_1.add(counts_2, fill_value=0)
        .sort_values(ascending=False)
        .astype(int)
    )

    print(redundancy_counts.to_string())
