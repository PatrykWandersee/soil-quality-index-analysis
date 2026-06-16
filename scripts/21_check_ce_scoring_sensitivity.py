"""Check electrical conductivity scoring sensitivity in SQI candidates.

This script evaluates whether electrical conductivity (CE_dS_m) should be
retained, removed, or scored in the empirical positive direction within the
current SQI workflow.

The motivation is that CE showed positive association with yield within the
observed low-to-moderate CE range, probably reflecting soluble fertility or
fertigation intensity rather than harmful salinity. However, CE is also a
potential salinity-risk indicator in irrigated semiarid soils.

Inputs
------
data/processed/private/soil_quality_selected_sqi_versions_private.csv

Outputs
-------
tables/private/ce_scoring_sensitivity_summary.csv
tables/private/ce_scoring_sensitivity_summary.md
"""

from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import linregress, pearsonr, spearmanr


INPUT_PATH = Path("data/processed/private/soil_quality_selected_sqi_versions_private.csv")
OUTPUT_CSV = Path("tables/private/ce_scoring_sensitivity_summary.csv")
OUTPUT_MD = Path("tables/private/ce_scoring_sensitivity_summary.md")

FARM_COLUMN = "Fazenda"
CE_COLUMN = "CE_dS_m"
NA_COLUMN = "Na_Troc_cmolc_Kg"

PRIMARY_RESPONSE = "Prod_rel_pct"
SECONDARY_RESPONSE = "Prod_rel_ha_pct"

CURRENT_MAIN_SQI = "MDS11_main_SQI"
CURRENT_SODICITY_SQI = "MDS12_sodicity_SQI"

MDS10_WITHOUT_CE = "MDS10_without_CE_SQI"
MDS11_CE_MORE = "MDS11_CE_more_is_better_SQI"
MDS11_SODICITY_WITHOUT_CE = "MDS11_sodicity_without_CE_SQI"
MDS12_CE_MORE = "MDS12_CE_more_is_better_SQI"


def validate_required_columns(df: pd.DataFrame, required_columns: list[str]) -> None:
    """Check whether all required columns are present."""
    missing_columns = [column for column in required_columns if column not in df.columns]

    if missing_columns:
        missing_text = "\n".join(f"- {column}" for column in missing_columns)
        raise ValueError(f"Missing required columns:\n{missing_text}")


def score_more_is_better(series: pd.Series) -> pd.Series:
    """Apply linear min-max scoring where higher values receive higher scores."""
    minimum = series.min()
    maximum = series.max()

    if np.isclose(maximum, minimum):
        return pd.Series(np.nan, index=series.index)

    return (series - minimum) / (maximum - minimum)


def score_less_is_better(series: pd.Series) -> pd.Series:
    """Apply linear min-max scoring where lower values receive higher scores."""
    minimum = series.min()
    maximum = series.max()

    if np.isclose(maximum, minimum):
        return pd.Series(np.nan, index=series.index)

    return (maximum - series) / (maximum - minimum)


def get_score_columns(df: pd.DataFrame, candidate_prefix: str) -> list[str]:
    """Return component score columns for a given SQI candidate prefix."""
    score_columns = [
        column
        for column in df.columns
        if column.startswith(candidate_prefix) and column.endswith("_score")
    ]

    if not score_columns:
        raise ValueError(f"No score columns found for prefix: {candidate_prefix}")

    return score_columns


def format_p_value(value: float) -> str:
    """Format p-values for Markdown output."""
    if pd.isna(value):
        return ""
    if value < 0.001:
        return "<0.001"
    return f"{value:.3f}"


def calculate_simple_metrics(
    df: pd.DataFrame,
    sqi_column: str,
    response_column: str,
    subset_label: str,
) -> dict[str, float | int | str]:
    """Calculate simple validation metrics for one SQI candidate."""
    data = df[[sqi_column, response_column]].dropna().copy()

    x = data[sqi_column].to_numpy()
    y = data[response_column].to_numpy()

    spearman_rho, spearman_p = spearmanr(x, y)
    pearson_r, pearson_p = pearsonr(x, y)
    linear_model = linregress(x, y)

    predicted = linear_model.intercept + linear_model.slope * x
    residuals = y - predicted

    return {
        "sqi_version": sqi_column,
        "response_variable": response_column,
        "subset": subset_label,
        "n": int(len(data)),
        "spearman_rho": float(spearman_rho),
        "spearman_p": float(spearman_p),
        "pearson_r": float(pearson_r),
        "pearson_p": float(pearson_p),
        "linear_intercept": float(linear_model.intercept),
        "linear_slope": float(linear_model.slope),
        "linear_r2": float(linear_model.rvalue**2),
        "linear_p": float(linear_model.pvalue),
        "rmse": float(np.sqrt(np.mean(residuals**2))),
        "mae": float(np.mean(np.abs(residuals))),
    }


def calculate_farm_fixed_metrics(
    df: pd.DataFrame,
    sqi_column: str,
    response_column: str,
) -> dict[str, float | int | str]:
    """Calculate farm fixed-effect OLS metrics for one SQI candidate."""
    data = df[[sqi_column, response_column, FARM_COLUMN]].dropna().copy()
    data = pd.get_dummies(data, columns=[FARM_COLUMN], drop_first=True)

    y = data[response_column].astype(float)

    farm_columns = [
        column for column in data.columns if column.startswith(f"{FARM_COLUMN}_")
    ]
    x_columns = [sqi_column, *farm_columns]

    x = data[x_columns].astype(float)
    x = sm.add_constant(x)

    model = sm.OLS(y, x).fit()

    return {
        "sqi_version": sqi_column,
        "response_variable": response_column,
        "subset": "all_data",
        "farm_fixed_r2": float(model.rsquared),
        "farm_fixed_adj_r2": float(model.rsquared_adj),
        "farm_fixed_aic": float(model.aic),
        "farm_fixed_bic": float(model.bic),
        "farm_fixed_sqi_p": float(model.pvalues[sqi_column]),
    }


def dataframe_to_markdown(df: pd.DataFrame) -> str:
    """Create a simple Markdown table without external dependencies."""
    headers = list(df.columns)
    rows = df.astype(str).values.tolist()

    header_line = "| " + " | ".join(headers) + " |"
    separator_line = "| " + " | ".join(["---"] * len(headers)) + " |"
    row_lines = ["| " + " | ".join(row) + " |" for row in rows]

    return "\n".join([header_line, separator_line, *row_lines])


def main() -> None:
    """Run CE scoring sensitivity analysis."""
    df = pd.read_csv(INPUT_PATH).copy()

    validate_required_columns(
        df,
        [
            FARM_COLUMN,
            CE_COLUMN,
            NA_COLUMN,
            PRIMARY_RESPONSE,
            SECONDARY_RESPONSE,
            CURRENT_MAIN_SQI,
            CURRENT_SODICITY_SQI,
        ],
    )

    main_score_columns = get_score_columns(df, "MDS11_main_")

    ce_score_columns = [column for column in main_score_columns if CE_COLUMN in column]
    non_ce_score_columns = [
        column for column in main_score_columns if CE_COLUMN not in column
    ]

    if len(ce_score_columns) != 1:
        raise ValueError(
            "Expected exactly one CE score column in MDS11_main. "
            f"Found: {ce_score_columns}"
        )

    ce_score_column = ce_score_columns[0]

    ce_more_score = score_more_is_better(df[CE_COLUMN])
    na_less_score = score_less_is_better(df[NA_COLUMN])

    # Main candidate without CE.
    df[MDS10_WITHOUT_CE] = df[non_ce_score_columns].mean(axis=1)

    # Main candidate with empirical positive CE scoring.
    df[MDS11_CE_MORE] = pd.concat(
        [
            df[non_ce_score_columns],
            ce_more_score.rename("CE_more_is_better_score"),
        ],
        axis=1,
    ).mean(axis=1)

    # Sodicity sensitivity without CE: MDS10 + exchangeable Na.
    df[MDS11_SODICITY_WITHOUT_CE] = pd.concat(
        [
            df[non_ce_score_columns],
            na_less_score.rename("Na_Troc_less_is_better_score"),
        ],
        axis=1,
    ).mean(axis=1)

    # Sodicity sensitivity with empirical positive CE scoring: MDS10 + CE more + Na.
    df[MDS12_CE_MORE] = pd.concat(
        [
            df[non_ce_score_columns],
            ce_more_score.rename("CE_more_is_better_score"),
            na_less_score.rename("Na_Troc_less_is_better_score"),
        ],
        axis=1,
    ).mean(axis=1)

    sqi_versions = [
        CURRENT_MAIN_SQI,
        MDS10_WITHOUT_CE,
        MDS11_CE_MORE,
        CURRENT_SODICITY_SQI,
        MDS11_SODICITY_WITHOUT_CE,
        MDS12_CE_MORE,
    ]

    results = []

    for response_column in [PRIMARY_RESPONSE, SECONDARY_RESPONSE]:
        for sqi_version in sqi_versions:
            results.append(
                calculate_simple_metrics(
                    df=df,
                    sqi_column=sqi_version,
                    response_column=response_column,
                    subset_label="all_data",
                )
            )

        without_experimental = df[df[FARM_COLUMN] != "Experimental"].copy()

        for sqi_version in sqi_versions:
            results.append(
                calculate_simple_metrics(
                    df=without_experimental,
                    sqi_column=sqi_version,
                    response_column=response_column,
                    subset_label="without_experimental",
                )
            )

    simple_summary = pd.DataFrame(results)

    farm_results = [
        calculate_farm_fixed_metrics(
            df=df,
            sqi_column=sqi_version,
            response_column=PRIMARY_RESPONSE,
        )
        for sqi_version in sqi_versions
    ]

    farm_summary = pd.DataFrame(farm_results)

    summary = simple_summary.merge(
        farm_summary,
        on=["sqi_version", "response_variable", "subset"],
        how="left",
    )

    summary = summary.round(6)

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(OUTPUT_CSV, index=False)

    manuscript_summary = summary[
        (summary["response_variable"] == PRIMARY_RESPONSE)
        & (summary["subset"] == "all_data")
    ].copy()

    manuscript_summary = manuscript_summary[
        [
            "sqi_version",
            "spearman_rho",
            "spearman_p",
            "pearson_r",
            "linear_r2",
            "rmse",
            "farm_fixed_r2",
            "farm_fixed_aic",
            "farm_fixed_sqi_p",
        ]
    ]

    manuscript_summary["spearman_p"] = manuscript_summary["spearman_p"].map(
        format_p_value
    )
    manuscript_summary["farm_fixed_sqi_p"] = manuscript_summary[
        "farm_fixed_sqi_p"
    ].map(format_p_value)

    for column in [
        "spearman_rho",
        "pearson_r",
        "linear_r2",
        "rmse",
        "farm_fixed_r2",
        "farm_fixed_aic",
    ]:
        manuscript_summary[column] = manuscript_summary[column].map(
            lambda value: f"{float(value):.3f}"
        )

    markdown_table = dataframe_to_markdown(manuscript_summary)

    note = (
        "\n\nNote: this table evaluates sensitivity to electrical conductivity "
        "retention and scoring direction. CE was originally scored as "
        "less-is-better because it can represent salinity risk in irrigated "
        "semiarid soils. However, within the observed CE range, higher CE may "
        "also reflect soluble fertility or fertigation intensity.\n"
    )

    OUTPUT_MD.write_text(markdown_table + note, encoding="utf-8")

    print("CE scoring sensitivity analysis completed.")
    print(f"Input file: {INPUT_PATH}")
    print(f"Output CSV: {OUTPUT_CSV}")
    print(f"Output Markdown: {OUTPUT_MD}")
    print()
    print("MDS11 score columns used:")
    for column in main_score_columns:
        print(f"- {column}")
    print()
    print("CE score column detected:")
    print(f"- {ce_score_column}")
    print()
    print("Primary response summary:")
    print(markdown_table)
    print(note)


if __name__ == "__main__":
    main()
