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

PCA_CONTRIBUTIONS_PATH = (
    PROJECT_DIR
    / "tables"
    / "private"
    / "pca_candidate_set_contributions.csv"
)

PCA_LOADINGS_PATH = (
    PROJECT_DIR
    / "tables"
    / "private"
    / "pca_candidate_set_loadings.csv"
)

HIGH_CORRELATION_PATH = (
    PROJECT_DIR
    / "tables"
    / "private"
    / "highly_correlated_indicator_pairs.csv"
)

OUTPUT_PATH = (
    PROJECT_DIR
    / "tables"
    / "private"
    / "preliminary_mds_selection.csv"
)

df = pd.read_csv(DATA_PATH)
contributions = pd.read_csv(PCA_CONTRIBUTIONS_PATH, index_col=0)
loadings = pd.read_csv(PCA_LOADINGS_PATH, index_col=0)
high_corr = pd.read_csv(HIGH_CORRELATION_PATH)

response = "Prod_rel_pct"

retained_pcs = ["PC1", "PC2", "PC3", "PC4"]

preliminary_mds = {
    "MO_g_dm3": {
        "domain": "organic matter",
        "rationale": "Represents soil organic matter and carbon-related soil functioning.",
    },
    "GMea": {
        "domain": "biological",
        "rationale": "Represents integrated enzyme activity and showed strong association with relative yield.",
    },
    "Arilsulf": {
        "domain": "biological",
        "rationale": "Represents sulfur-related enzymatic activity and complements GMea.",
    },
    "Ca_Troc_cmolc_Kg": {
        "domain": "chemical fertility",
        "rationale": "Represents exchangeable calcium and base fertility status.",
    },
    "K_Troc_cmolc_Kg": {
        "domain": "chemical fertility",
        "rationale": "Represents exchangeable potassium, a key plant nutrient.",
    },
    "Floculacao_pct": {
        "domain": "physical structure",
        "rationale": "Represents clay flocculation and structural stability.",
    },
    "Ds_g_cm3": {
        "domain": "physical structure",
        "rationale": "Represents soil bulk density and physical restriction.",
    },
    "PST": {
        "domain": "sodicity",
        "rationale": "Represents exchangeable sodium percentage and sodicity risk.",
    },
    "Na_Troc_cmolc_Kg": {
        "domain": "sodicity",
        "rationale": "Represents exchangeable sodium and complements PST in the sodicity gradient.",
    },
    "PM1_mg_dm3": {
        "domain": "chemical fertility",
        "rationale": "Represents Mehlich-1 available phosphorus; clay normalization did not improve initial association with yield.",
    },
    "pH": {
        "domain": "chemical reaction",
        "rationale": "Represents soil acidity/alkalinity and nutrient availability conditions.",
    },
    "CE_dS_m": {
        "domain": "salinity",
        "rationale": "Represents electrical conductivity and salinity stress.",
    },
}

rows = []

for indicator, metadata in preliminary_mds.items():
    if indicator not in df.columns:
        raise ValueError(f"Indicator not found in dataset: {indicator}")

    temp = df[[indicator, response]].dropna()

    rho, p_value = spearmanr(temp[indicator], temp[response])

    pc_contrib = contributions.loc[indicator, retained_pcs]
    dominant_pc = pc_contrib.idxmax()
    max_contribution = pc_contrib.max()
    loading_on_dominant_pc = loadings.loc[indicator, dominant_pc]

    redundant_pairs = high_corr[
        (high_corr["indicator_1"] == indicator)
        | (high_corr["indicator_2"] == indicator)
    ].copy()

    redundant_with = []

    for _, pair in redundant_pairs.iterrows():
        other = (
            pair["indicator_2"]
            if pair["indicator_1"] == indicator
            else pair["indicator_1"]
        )
        redundant_with.append(f"{other} (rho={pair['spearman_rho']:.3f})")

    rows.append(
        {
            "indicator": indicator,
            "domain": metadata["domain"],
            "dominant_pc": dominant_pc,
            "loading_on_dominant_pc": loading_on_dominant_pc,
            "max_contribution_pct": max_contribution,
            "spearman_rho_with_yield": rho,
            "p_value_with_yield": p_value,
            "high_redundancy_links": len(redundant_with),
            "highly_correlated_with": "; ".join(redundant_with),
            "rationale": metadata["rationale"],
        }
    )

selection = pd.DataFrame(rows)

selection = selection.sort_values(
    by=["domain", "indicator"],
    ascending=[True, True],
)

selection.to_csv(OUTPUT_PATH, index=False)

print("\nPreliminary MDS selection table created.")
print(f"Output file: {OUTPUT_PATH}")

print("\nPreliminary MDS indicators:")
print("=" * 80)

print(
    selection[
        [
            "indicator",
            "domain",
            "dominant_pc",
            "max_contribution_pct",
            "spearman_rho_with_yield",
            "p_value_with_yield",
            "high_redundancy_links",
        ]
    ].to_string(index=False, float_format="{:.4f}".format)
)
