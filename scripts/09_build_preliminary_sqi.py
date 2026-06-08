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
    / "soil_quality_sqi_private.csv"
)

TABLE_DIR = PROJECT_DIR / "tables" / "private"
FIGURE_DIR = PROJECT_DIR / "figures" / "private" / "sqi"

TABLE_DIR.mkdir(parents=True, exist_ok=True)
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH)

response = "Prod_rel_pct"

mds_11 = [
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
]

# First exploratory scoring scheme.
# This is not the final agronomic scoring function.
# It uses observed min-max scaling and simple indicator direction.
score_directions_data_driven = {
    "MO_g_dm3": "more_is_better",
    "GMea": "more_is_better",
    "Arilsulf": "more_is_better",
    "Ca_Troc_cmolc_Kg": "more_is_better",
    "K_Troc_cmolc_Kg": "more_is_better",
    "Floculacao_pct": "more_is_better",
    "Ds_g_cm3": "less_is_better",
    "PST": "less_is_better",
    "PM1_mg_dm3": "more_is_better",
    "pH": "more_is_better",
    "CE_dS_m": "more_is_better",
}

# Conservative agronomic sensitivity scheme.
# CE is treated as "less is better" because it represents salinity risk,
# even though the initial Spearman association with yield was positive.
score_directions_conservative = {
    **score_directions_data_driven,
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

    raise ValueError(f"Unknown scoring direction: {direction}")


def build_sqi(data, indicators, directions, prefix):
    scored = pd.DataFrame(index=data.index)

    for indicator in indicators:
        if indicator not in data.columns:
            raise ValueError(f"Missing indicator in dataset: {indicator}")

        score_col = f"{prefix}_{indicator}_score"
        scored[score_col] = minmax_score(
            data[indicator],
            directions[indicator],
        )

    sqi_col = f"{prefix}_SQI"
    scored[sqi_col] = scored.mean(axis=1)

    return scored, sqi_col


data_driven_scores, data_driven_sqi_col = build_sqi(
    data=df,
    indicators=mds_11,
    directions=score_directions_data_driven,
    prefix="MDS11_data_driven",
)

conservative_scores, conservative_sqi_col = build_sqi(
    data=df,
    indicators=mds_11,
    directions=score_directions_conservative,
    prefix="MDS11_conservative",
)

output = pd.concat(
    [
        df,
        data_driven_scores,
        conservative_scores,
    ],
    axis=1,
)

output.to_csv(OUTPUT_DATA_PATH, index=False)

summary_rows = []

for sqi_col in [data_driven_sqi_col, conservative_sqi_col]:
    temp = output[[sqi_col, response]].dropna()
    rho, p_value = spearmanr(temp[sqi_col], temp[response])

    summary_rows.append(
        {
            "sqi": sqi_col,
            "n": temp.shape[0],
            "spearman_rho_with_yield": rho,
            "p_value": p_value,
        }
    )

summary = pd.DataFrame(summary_rows)

summary.to_csv(
    TABLE_DIR / "preliminary_sqi_validation.csv",
    index=False,
)

print("\nPreliminary SQI built.")
print(f"Output dataset: {OUTPUT_DATA_PATH}")

print("\nSQI validation against relative yield:")
print(
    summary.to_string(
        index=False,
        float_format="{:.5f}".format,
    )
)


def format_p_value(p_value):
    if p_value < 0.0001:
        return "p < 0.0001"
    return f"p = {p_value:.4f}"


def create_sqi_plot(data, sqi_col, response_col, output_path):
    plot_data = data[[sqi_col, response_col]].dropna()
    rho, p_value = spearmanr(plot_data[sqi_col], plot_data[response_col])

    fig, ax = plt.subplots(figsize=(5.5, 4.2))

    ax.scatter(
        plot_data[sqi_col],
        plot_data[response_col],
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
    fig.savefig(output_path, dpi=300)
    plt.close(fig)


create_sqi_plot(
    data=output,
    sqi_col=data_driven_sqi_col,
    response_col=response,
    output_path=FIGURE_DIR / "mds11_data_driven_sqi_vs_relative_yield.png",
)

create_sqi_plot(
    data=output,
    sqi_col=conservative_sqi_col,
    response_col=response,
    output_path=FIGURE_DIR / "mds11_conservative_sqi_vs_relative_yield.png",
)

print("\nSQI figures saved.")
print(f"Figure directory: {FIGURE_DIR}")
