from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
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


def score_less_is_better(series):
    minimum = series.min()
    maximum = series.max()

    if np.isclose(maximum, minimum):
        return pd.Series(np.nan, index=series.index)

    return (maximum - series) / (maximum - minimum)


def validate_required_columns(data, columns, context):
    missing = [column for column in columns if column not in data.columns]

    if missing:
        missing_text = "\n".join(f"- {column}" for column in missing)
        raise ValueError(f"Missing columns for {context}:\n{missing_text}")


def add_summary_row(output, summary_rows, sqi_col, candidate_set, indicators):
    temp = output[[sqi_col, response]].dropna()
    rho, p_value = spearmanr(temp[sqi_col], temp[response])

    summary_rows.append(
        {
            "sqi": sqi_col,
            "candidate_set": candidate_set,
            "n_indicators": len(indicators),
            "n": temp.shape[0],
            "spearman_rho_with_yield": rho,
            "p_value": p_value,
            "indicators": "; ".join(indicators),
        }
    )


def get_score_columns(candidate_set, indicators):
    return [f"{candidate_set}_{indicator}_score" for indicator in indicators]


output = df.copy()
summary_rows = []

for set_name, indicators in candidate_sets.items():
    scores, sqi_col, score_cols = build_sqi_scores(
        data=output,
        scoring_rules=scoring_rules,
        candidate_set=set_name,
    )

    output = pd.concat([output, scores], axis=1)

    add_summary_row(
        output=output,
        summary_rows=summary_rows,
        sqi_col=sqi_col,
        candidate_set=set_name,
        indicators=indicators,
    )


# Derived CE-free SQI candidates.
#
# CE_dS_m was initially retained because salinity risk is relevant in irrigated
# semiarid soils. However, within the observed low-to-moderate CE range, higher
# CE was positively associated with relative yield, probably reflecting soluble
# fertility or fertigation intensity rather than harmful salinity. Therefore,
# CE-free candidates are exported for the revised manuscript-oriented workflow.

if "MDS11_main" in candidate_sets:
    main_indicators = list(candidate_sets["MDS11_main"])
    main_indicators_without_ce = [
        indicator for indicator in main_indicators if indicator != "CE_dS_m"
    ]

    main_score_columns_without_ce = get_score_columns(
        candidate_set="MDS11_main",
        indicators=main_indicators_without_ce,
    )

    validate_required_columns(
        data=output,
        columns=main_score_columns_without_ce,
        context="MDS10_without_CE_SQI",
    )

    output["MDS10_without_CE_SQI"] = output[main_score_columns_without_ce].mean(
        axis=1
    )

    add_summary_row(
        output=output,
        summary_rows=summary_rows,
        sqi_col="MDS10_without_CE_SQI",
        candidate_set="MDS10_without_CE",
        indicators=main_indicators_without_ce,
    )

    validate_required_columns(
        data=output,
        columns=["Na_Troc_cmolc_Kg"],
        context="MDS11_sodicity_without_CE_SQI",
    )

    output["MDS11_sodicity_without_CE_Na_Troc_cmolc_Kg_score"] = (
        score_less_is_better(output["Na_Troc_cmolc_Kg"])
    )

    sodicity_without_ce_score_columns = [
        *main_score_columns_without_ce,
        "MDS11_sodicity_without_CE_Na_Troc_cmolc_Kg_score",
    ]

    output["MDS11_sodicity_without_CE_SQI"] = output[
        sodicity_without_ce_score_columns
    ].mean(axis=1)

    add_summary_row(
        output=output,
        summary_rows=summary_rows,
        sqi_col="MDS11_sodicity_without_CE_SQI",
        candidate_set="MDS11_sodicity_without_CE",
        indicators=[*main_indicators_without_ce, "Na_Troc_cmolc_Kg"],
    )


if "MDS11_pH_optimum" in candidate_sets:
    ph_optimum_indicators = list(candidate_sets["MDS11_pH_optimum"])
    ph_optimum_indicators_without_ce = [
        indicator for indicator in ph_optimum_indicators if indicator != "CE_dS_m"
    ]

    ph_optimum_score_columns_without_ce = get_score_columns(
        candidate_set="MDS11_pH_optimum",
        indicators=ph_optimum_indicators_without_ce,
    )

    validate_required_columns(
        data=output,
        columns=ph_optimum_score_columns_without_ce,
        context="MDS10_pH_optimum_without_CE_SQI",
    )

    output["MDS10_pH_optimum_without_CE_SQI"] = output[
        ph_optimum_score_columns_without_ce
    ].mean(axis=1)

    add_summary_row(
        output=output,
        summary_rows=summary_rows,
        sqi_col="MDS10_pH_optimum_without_CE_SQI",
        candidate_set="MDS10_pH_optimum_without_CE",
        indicators=ph_optimum_indicators_without_ce,
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
