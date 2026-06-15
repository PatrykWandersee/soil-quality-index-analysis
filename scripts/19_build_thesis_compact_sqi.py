"""Build and validate a compact thesis-inspired SQI candidate.

This script adds a compact SQI candidate based on the two-indicator MDS used
in the thesis: clay-normalized beta-glucosidase and sum of exchangeable bases.

The implementation here uses the current repository scoring convention:
linear min-max scoring with a "more is better" direction for both indicators.

This is therefore a thesis-inspired compact candidate within the current
pipeline, not an exact reconstruction of the original thesis sigmoid-weighted
SQI.

Inputs
------
data/processed/private/soil_quality_selected_sqi_versions_private.csv

Outputs
-------
data/processed/private/soil_quality_selected_sqi_versions_private.csv
tables/private/thesis_compact_sqi_validation.csv
"""

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import linregress, pearsonr, spearmanr


INPUT_PATH = Path("data/processed/private/soil_quality_selected_sqi_versions_private.csv")
OUTPUT_PATH = INPUT_PATH

TABLES_DIR = Path("tables/private")
VALIDATION_OUTPUT = TABLES_DIR / "thesis_compact_sqi_validation.csv"

BETA_CLAY_COLUMN = "Beta_por_Argila"
SB_COLUMN = "SB_cmolc_Kg"

BETA_SCORE_COLUMN = "MDS2_thesis_compact_linear_Beta_por_Argila_score"
SB_SCORE_COLUMN = "MDS2_thesis_compact_linear_SB_cmolc_Kg_score"
SQI_COLUMN = "MDS2_thesis_compact_linear_SQI"

RESPONSE_COLUMNS = [
    "Prod_rel_pct",
    "Prod_rel_ha_pct",
]

VALIDATION_COLUMNS = [
    SQI_COLUMN,
    BETA_CLAY_COLUMN,
    SB_COLUMN,
]


def validate_required_columns(df: pd.DataFrame, required_columns: list[str]) -> None:
    """Check whether all required columns are present in the dataset."""
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


def calculate_validation_metrics(
    df: pd.DataFrame,
    indicator_column: str,
    response_column: str,
) -> dict[str, float | int | str]:
    """Calculate correlation and linear-regression validation metrics."""
    data = df[[indicator_column, response_column]].dropna().copy()

    x = data[indicator_column].to_numpy()
    y = data[response_column].to_numpy()

    spearman_rho, spearman_p = spearmanr(x, y)
    pearson_r, pearson_p = pearsonr(x, y)
    linear_model = linregress(x, y)

    predicted = linear_model.intercept + linear_model.slope * x
    residuals = y - predicted

    rmse = float(np.sqrt(np.mean(residuals**2)))
    mae = float(np.mean(np.abs(residuals)))

    return {
        "indicator": indicator_column,
        "response_variable": response_column,
        "n": int(len(data)),
        "spearman_rho": float(spearman_rho),
        "spearman_p": float(spearman_p),
        "pearson_r": float(pearson_r),
        "pearson_p": float(pearson_p),
        "linear_slope": float(linear_model.slope),
        "linear_intercept": float(linear_model.intercept),
        "linear_r2": float(linear_model.rvalue**2),
        "linear_p": float(linear_model.pvalue),
        "rmse": rmse,
        "mae": mae,
    }


def main() -> None:
    """Build and validate the compact thesis-inspired SQI."""
    TABLES_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(INPUT_PATH).copy()

    required_columns = [
        BETA_CLAY_COLUMN,
        SB_COLUMN,
        *RESPONSE_COLUMNS,
    ]

    validate_required_columns(df, required_columns)

    df[BETA_SCORE_COLUMN] = score_more_is_better(df[BETA_CLAY_COLUMN])
    df[SB_SCORE_COLUMN] = score_more_is_better(df[SB_COLUMN])

    df[SQI_COLUMN] = df[[BETA_SCORE_COLUMN, SB_SCORE_COLUMN]].mean(axis=1)

    validation_results = []

    for response_column in RESPONSE_COLUMNS:
        for indicator_column in VALIDATION_COLUMNS:
            validation_results.append(
                calculate_validation_metrics(
                    df=df,
                    indicator_column=indicator_column,
                    response_column=response_column,
                )
            )

    validation = pd.DataFrame(validation_results)
    validation = validation.round(6)

    df.to_csv(OUTPUT_PATH, index=False)
    validation.to_csv(VALIDATION_OUTPUT, index=False)

    print("Compact thesis-inspired SQI created.")
    print(f"Input/output file: {OUTPUT_PATH}")
    print(f"Validation table: {VALIDATION_OUTPUT}")
    print()
    print("New columns:")
    print(f"- {BETA_SCORE_COLUMN}")
    print(f"- {SB_SCORE_COLUMN}")
    print(f"- {SQI_COLUMN}")
    print()
    print("Validation summary:")
    print(validation.to_string(index=False))


if __name__ == "__main__":
    main()
