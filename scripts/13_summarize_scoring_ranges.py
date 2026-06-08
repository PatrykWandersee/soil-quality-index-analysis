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

CONFIG_PATH = PROJECT_DIR / "config" / "scoring_rules_mds.csv"

OUTPUT_PATH = (
    PROJECT_DIR
    / "tables"
    / "private"
    / "scoring_indicator_ranges.csv"
)

df = pd.read_csv(DATA_PATH)
rules = pd.read_csv(CONFIG_PATH)

response = "Prod_rel_pct"

# Use each indicator only once, even if it appears in multiple candidate sets
indicator_rules = (
    rules.sort_values(["main_role", "candidate_set", "indicator"])
    .drop_duplicates(subset=["indicator"])
    .copy()
)

rows = []

for _, row in indicator_rules.iterrows():
    indicator = row["indicator"]

    if indicator not in df.columns:
        raise ValueError(f"Indicator not found in dataset: {indicator}")

    values = df[indicator].dropna()

    temp = df[[indicator, response]].dropna()
    rho, p_value = spearmanr(temp[indicator], temp[response])

    rows.append(
        {
            "indicator": indicator,
            "domain": row["domain"],
            "current_scoring_direction": row["scoring_direction"],
            "current_scoring_method": row["scoring_method"],
            "n": values.shape[0],
            "min": values.min(),
            "p05": values.quantile(0.05),
            "p25": values.quantile(0.25),
            "median": values.median(),
            "p75": values.quantile(0.75),
            "p95": values.quantile(0.95),
            "max": values.max(),
            "mean": values.mean(),
            "std": values.std(),
            "spearman_rho_with_yield": rho,
            "p_value_with_yield": p_value,
            "notes": row["notes"],
        }
    )

summary = pd.DataFrame(rows)

summary = summary.sort_values(
    by=["domain", "indicator"],
    ascending=[True, True],
)

summary.to_csv(OUTPUT_PATH, index=False)

print("\nScoring indicator range summary created.")
print(f"Output file: {OUTPUT_PATH}")

print("\nObserved ranges and current scoring directions:")
print("=" * 100)

print(
    summary[
        [
            "indicator",
            "domain",
            "current_scoring_direction",
            "min",
            "p25",
            "median",
            "p75",
            "max",
            "spearman_rho_with_yield",
        ]
    ].to_string(index=False, float_format="{:.4f}".format)
)
