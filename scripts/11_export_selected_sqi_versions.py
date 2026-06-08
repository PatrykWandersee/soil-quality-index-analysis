from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import spearmanr

from sqi_utils import build_sqi_scores, get_candidate_sets, load_scoring_rules


PROJECT_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "private"
    / "soil_quality_processed_private.csv"
)

CONFIG_PATH = PROJECT_DIR / "config" / "scoring_rules_mds.csv"

OUTPUT_DATA_PATH = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "private"
    / "soil_quality_selected_sqi_versions_private.csv"
)

TABLE_DIR = PROJECT_DIR / "tables" / "private"
FIGURE_DIR = PROJECT_DIR / "figures" / "private" / "sqi"

TABLE_DIR.mkdir(parents=True, exist_ok=True)
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH)
scoring_rules = load_scoring_rules(CONFIG_PATH)
candidate_sets = get_candidate_sets(scoring_rules)

response = "Prod_rel_pct"


def format_p_value(p_value):
    if p_value < 0.0001:
        return "p < 0.0001"
    return f"p = {p_value:.4f}"


output = df.copy()
summary_rows = []

for set_name, indicators in candidate_sets.items():
    scores, sqi_col, score_cols = build_sqi_scores(
        data=output,
        scoring_rules=scoring_rules,
        candidate_set=set_name,
    )

    output = pd.concat([output, scores], axis=1)

    temp = output[[sqi_col, response]].dropna()
    rho, p_value = spearmanr(temp[sqi_col], temp[response])

    summary_rows.append(
        {
            "sqi": sqi_col,
            "candidate_set": set_name,
            "n_indicators": len(indicators),
            "n": temp.shape[0],
            "spearman_rho_with_yield": rho,
            "p_value": p_value,
            "indicators": "; ".join(indicators),
        }
    )

summary = pd.DataFrame(summary_rows)

summary.to_csv(
    TABLE_DIR / "selected_sqi_versions_validation.csv",
    index=False,
)

output.to_csv(OUTPUT_DATA_PATH, index=False)

print("\nSelected SQI versions exported.")
print(f"Scoring rules: {CONFIG_PATH}")
print(f"Output dataset: {OUTPUT_DATA_PATH}")

print("\nValidation summary:")
print(
    summary[
        [
            "sqi",
            "n_indicators",
            "n",
            "spearman_rho_with_yield",
            "p_value",
        ]
    ].to_string(index=False, float_format="{:.5f}".format)
)


for _, row in summary.iterrows():
    sqi_col = row["sqi"]
    plot_data = output[[sqi_col, response]].dropna()

    rho, p_value = spearmanr(plot_data[sqi_col], plot_data[response])

    fig, ax = plt.subplots(figsize=(5.5, 4.2))

    ax.scatter(
        plot_data[sqi_col],
        plot_data[response],
        s=38,
        facecolors="none",
        edgecolors="black",
        linewidths=0.8,
    )

    ax.set_xlabel(sqi_col)
    ax.set_ylabel("Relative yield per plant (%)")

    annotation = (
        f"Spearman rho = {rho:.3f}\n"
        f"{format_p_value(p_value)}\n"
        f"n = {len(plot_data)}"
    )

    ax.text(
        0.05,
        0.95,
        annotation,
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=9,
        bbox={
            "boxstyle": "round",
            "facecolor": "white",
            "edgecolor": "black",
            "linewidth": 0.5,
        },
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()

    file_name = sqi_col.lower() + "_vs_relative_yield.png"
    fig.savefig(FIGURE_DIR / file_name, dpi=300)
    plt.close(fig)

print("\nFigures saved.")
print(f"Figure directory: {FIGURE_DIR}")
