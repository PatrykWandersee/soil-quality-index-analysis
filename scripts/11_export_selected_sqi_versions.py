from pathlib import Path

import matplotlib.pyplot as plt
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

response = "Prod_rel_pct"

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
}

# Conservative exploratory scoring.
# CE is scored as "less is better" because it represents salinity risk.
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


def format_p_value(p_value):
    if p_value < 0.0001:
        return "p < 0.0001"
    return f"p = {p_value:.4f}"


output = df.copy()
summary_rows = []

for set_name, indicators in candidate_sets.items():
    score_cols = []

    for indicator in indicators:
        score_col = f"{set_name}_{indicator}_score"
        output[score_col] = minmax_score(
            output[indicator],
            directions[indicator],
        )
        score_cols.append(score_col)

    sqi_col = f"{set_name}_SQI"
    output[sqi_col] = output[score_cols].mean(axis=1)

    temp = output[[sqi_col, response]].dropna()
    rho, p_value = spearmanr(temp[sqi_col], temp[response])

    summary_rows.append(
        {
            "sqi": sqi_col,
            "n_indicators": len(indicators),
            "n": temp.shape[0],
            "spearman_rho_with_yield": rho,
            "p_value": p_value,
            "indicators": "; ".join(indicators),
        }
    )

summary = pd.DataFrame(summary_rows)
summary.to_csv(TABLE_DIR / "selected_sqi_versions_validation.csv", index=False)

output.to_csv(OUTPUT_DATA_PATH, index=False)

print("\nSelected SQI versions exported.")
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


# Create individual validation plots
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
