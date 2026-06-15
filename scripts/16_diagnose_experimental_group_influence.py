"""Diagnose the influence of the Experimental group on SQI validation.

This script evaluates whether the Experimental group drives the relationship
between preliminary SQI versions and yield response variables.

The goal is not to exclude the Experimental group by default, but to document
whether SQI-yield relationships remain stable when this group is removed.

Inputs
------
data/processed/private/soil_quality_selected_sqi_versions_private.csv

Outputs
-------
tables/private/experimental_group_influence_summary.csv
tables/private/experimental_group_correlation_sensitivity.csv
"""

from pathlib import Path

import pandas as pd
from scipy.stats import pearsonr, spearmanr


INPUT_PATH = Path("data/processed/private/soil_quality_selected_sqi_versions_private.csv")
TABLES_DIR = Path("tables/private")

GROUP_COLUMN = "Fazenda"
EXPERIMENTAL_LABEL = "Experimental"

RESPONSE_COLUMNS = [
    "Prod_rel_pct",
    "Prod_rel_ha_pct",
]

SQI_COLUMNS = [
    "MDS11_main_SQI",
    "MDS12_sodicity_SQI",
    "MDS11_pH_optimum_SQI",
]


def validate_required_columns(df: pd.DataFrame, required_columns: list[str]) -> None:
    """Check whether all required columns are present in the dataset."""
    missing_columns = [column for column in required_columns if column not in df.columns]

    if missing_columns:
        missing_text = "\n".join(f"- {column}" for column in missing_columns)
        raise ValueError(f"Missing required columns:\n{missing_text}")


def summarize_group_values(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize response and SQI values by dataset group."""
    data = df.copy()

    data["dataset_group"] = data[GROUP_COLUMN].eq(EXPERIMENTAL_LABEL).map(
        {
            True: "Experimental",
            False: "Commercial_farms",
        }
    )

    summary_columns = RESPONSE_COLUMNS + SQI_COLUMNS

    summary = (
        data.groupby("dataset_group")[summary_columns]
        .agg(["count", "mean", "median", "min", "max"])
        .round(6)
    )

    summary.columns = [
        f"{variable}_{statistic}" for variable, statistic in summary.columns
    ]

    return summary.reset_index()


def calculate_correlations(
    df: pd.DataFrame,
    dataset_label: str,
) -> list[dict[str, object]]:
    """Calculate SQI-response correlations for one dataset subset."""
    results = []

    for response_column in RESPONSE_COLUMNS:
        for sqi_column in SQI_COLUMNS:
            data = df[[response_column, sqi_column]].dropna().copy()

            spearman_rho, spearman_p = spearmanr(
                data[sqi_column],
                data[response_column],
            )

            pearson_r, pearson_p = pearsonr(
                data[sqi_column],
                data[response_column],
            )

            results.append(
                {
                    "dataset": dataset_label,
                    "response_variable": response_column,
                    "sqi_version": sqi_column,
                    "n": int(len(data)),
                    "n_farms": int(df[GROUP_COLUMN].nunique()),
                    "spearman_rho": float(spearman_rho),
                    "spearman_p": float(spearman_p),
                    "pearson_r": float(pearson_r),
                    "pearson_p": float(pearson_p),
                }
            )

    return results


def main() -> None:
    """Run Experimental group influence diagnostics."""
    TABLES_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(INPUT_PATH).copy()

    required_columns = [GROUP_COLUMN] + RESPONSE_COLUMNS + SQI_COLUMNS
    validate_required_columns(df, required_columns)

    group_summary = summarize_group_values(df)

    correlation_results = []

    correlation_results.extend(
        calculate_correlations(
            df=df,
            dataset_label="all_data",
        )
    )

    df_without_experimental = df[df[GROUP_COLUMN] != EXPERIMENTAL_LABEL].copy()

    correlation_results.extend(
        calculate_correlations(
            df=df_without_experimental,
            dataset_label="without_experimental",
        )
    )

    correlation_summary = pd.DataFrame(correlation_results)

    group_summary_path = TABLES_DIR / "experimental_group_influence_summary.csv"
    correlation_summary_path = TABLES_DIR / "experimental_group_correlation_sensitivity.csv"

    group_summary.to_csv(group_summary_path, index=False)
    correlation_summary.to_csv(correlation_summary_path, index=False)

    print("Experimental group influence diagnostics completed.")
    print(f"Input file: {INPUT_PATH}")
    print(f"Group summary: {group_summary_path}")
    print(f"Correlation sensitivity: {correlation_summary_path}")
    print()
    print("Group summary:")
    print(group_summary.to_string(index=False))
    print()
    print("Correlation sensitivity:")
    print(correlation_summary.to_string(index=False))


if __name__ == "__main__":
    main()
