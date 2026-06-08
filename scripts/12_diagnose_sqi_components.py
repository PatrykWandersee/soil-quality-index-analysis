from pathlib import Path

import pandas as pd
from scipy.stats import spearmanr

from sqi_utils import get_candidate_sets, load_scoring_rules


PROJECT_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "private"
    / "soil_quality_selected_sqi_versions_private.csv"
)

CONFIG_PATH = PROJECT_DIR / "config" / "scoring_rules_mds.csv"

OUTPUT_PATH = (
    PROJECT_DIR
    / "tables"
    / "private"
    / "sqi_component_diagnostics.csv"
)

df = pd.read_csv(DATA_PATH)
scoring_rules = load_scoring_rules(CONFIG_PATH)
candidate_sets = get_candidate_sets(scoring_rules)

response = "Prod_rel_pct"


def spearman_summary(x, y):
    temp = pd.concat([x, y], axis=1).dropna()

    if temp.shape[0] < 3:
        return None, None, temp.shape[0]

    rho, p_value = spearmanr(temp.iloc[:, 0], temp.iloc[:, 1])
    return rho, p_value, temp.shape[0]


rows = []

for set_name, indicators in candidate_sets.items():
    sqi_col = f"{set_name}_SQI"

    if sqi_col not in df.columns:
        raise ValueError(
            f"SQI column not found: {sqi_col}. "
            "Run scripts/11_export_selected_sqi_versions.py first."
        )

    score_cols = {
        indicator: f"{set_name}_{indicator}_score"
        for indicator in indicators
    }

    missing_score_cols = [
        col for col in score_cols.values()
        if col not in df.columns
    ]

    if missing_score_cols:
        raise ValueError(f"Missing score columns: {missing_score_cols}")

    full_rho, full_p, full_n = spearman_summary(
        df[sqi_col],
        df[response],
    )

    for indicator, score_col in score_cols.items():
        component_rho_yield, component_p_yield, component_n = spearman_summary(
            df[score_col],
            df[response],
        )

        component_rho_sqi, component_p_sqi, _ = spearman_summary(
            df[score_col],
            df[sqi_col],
        )

        remaining_score_cols = [
            col for ind, col in score_cols.items()
            if ind != indicator
        ]

        leave_one_out_sqi = df[remaining_score_cols].mean(axis=1)

        loo_rho, loo_p, loo_n = spearman_summary(
            leave_one_out_sqi,
            df[response],
        )

        rows.append(
            {
                "candidate_set": set_name,
                "indicator": indicator,
                "n_indicators_full": len(indicators),
                "full_sqi_rho_with_yield": full_rho,
                "full_sqi_p_value": full_p,
                "component_rho_with_yield": component_rho_yield,
                "component_p_value_with_yield": component_p_yield,
                "component_rho_with_sqi": component_rho_sqi,
                "leave_one_out_rho_with_yield": loo_rho,
                "leave_one_out_p_value": loo_p,
                "leave_one_out_delta": loo_rho - full_rho,
                "interpretation": (
                    "removal_improves_sqi"
                    if loo_rho > full_rho
                    else "removal_reduces_sqi"
                ),
            }
        )

diagnostics = pd.DataFrame(rows)

diagnostics = diagnostics.sort_values(
    by=["candidate_set", "leave_one_out_delta"],
    ascending=[True, False],
)

diagnostics.to_csv(OUTPUT_PATH, index=False)

print("\nSQI component diagnostics completed.")
print(f"Scoring rules: {CONFIG_PATH}")
print(f"Output file: {OUTPUT_PATH}")

for set_name in candidate_sets:
    print("\n" + "=" * 80)
    print(f"Candidate set: {set_name}")
    print("=" * 80)

    subset = diagnostics[diagnostics["candidate_set"] == set_name].copy()

    print(
        subset[
            [
                "indicator",
                "component_rho_with_yield",
                "component_rho_with_sqi",
                "leave_one_out_rho_with_yield",
                "leave_one_out_delta",
                "interpretation",
            ]
        ].to_string(index=False, float_format="{:.5f}".format)
    )
