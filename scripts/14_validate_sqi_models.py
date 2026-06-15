"""Validate preliminary SQI candidate versions against yield response variables.

This script compares selected Soil Quality Index (SQI) versions using simple
association and regression diagnostics. It is intended as a preliminary
validation step before more complex modelling approaches.

Inputs
------
data/processed/private/soil_quality_selected_sqi_versions_private.csv

Outputs
-------
tables/private/sqi_validation_summary.csv
figures/private/sqi_validation_<response>_<sqi>.png
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import linregress, pearsonr, spearmanr


INPUT_PATH = Path("data/processed/private/soil_quality_selected_sqi_versions_private.csv")
TABLES_DIR = Path("tables/private")
FIGURES_DIR = Path("figures/private/sqi/validation")

RESPONSE_COLUMNS = [
    "Prod_rel_pct",
    "Prod_rel_ha_pct",
]

SQI_COLUMNS = [
    "MDS11_main_SQI",
    "MDS12_sodicity_SQI",
    "MDS11_pH_optimum_SQI",
    "MDS2_thesis_compact_linear_SQI",
]


def validate_required_columns(df: pd.DataFrame, required_columns: list[str]) -> None:
    """Check whether all required columns are present in the dataset."""
    missing_columns = [column for column in required_columns if column not in df.columns]

    if missing_columns:
        missing_text = "\n".join(f"- {column}" for column in missing_columns)
        raise ValueError(f"Missing required columns:\n{missing_text}")


def calculate_rmse(observed: np.ndarray, predicted: np.ndarray) -> float:
    """Calculate root mean squared error."""
    return float(np.sqrt(np.mean((observed - predicted) ** 2)))


def calculate_mae(observed: np.ndarray, predicted: np.ndarray) -> float:
    """Calculate mean absolute error."""
    return float(np.mean(np.abs(observed - predicted)))


def validate_sqi_response(
    df: pd.DataFrame,
    sqi_column: str,
    response_column: str,
) -> dict[str, float | int | str]:
    """Calculate validation statistics for one SQI-response combination."""
    data = df[[sqi_column, response_column]].dropna().copy()

    x = data[sqi_column].to_numpy()
    y = data[response_column].to_numpy()

    spearman_rho, spearman_p = spearmanr(x, y)
    pearson_r, pearson_p = pearsonr(x, y)

    linear_model = linregress(x, y)
    predicted = linear_model.intercept + linear_model.slope * x

    return {
        "sqi_version": sqi_column,
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
        "rmse": calculate_rmse(y, predicted),
        "mae": calculate_mae(y, predicted),
    }


def make_validation_plot(
    df: pd.DataFrame,
    sqi_column: str,
    response_column: str,
    output_path: Path,
) -> None:
    """Create a scatter plot with a fitted linear trend line."""
    data = df[[sqi_column, response_column]].dropna().copy()

    x = data[sqi_column].to_numpy()
    y = data[response_column].to_numpy()

    linear_model = linregress(x, y)

    x_line = np.linspace(x.min(), x.max(), 100)
    y_line = linear_model.intercept + linear_model.slope * x_line

    fig, ax = plt.subplots(figsize=(6, 4))

    ax.scatter(x, y, alpha=0.8)
    ax.plot(x_line, y_line)

    ax.set_xlabel(sqi_column)
    ax.set_ylabel(response_column)
    ax.set_title(f"{sqi_column} vs {response_column}")

    annotation = (
        f"Spearman rho = {spearmanr(x, y).statistic:.3f}\n"
        f"Pearson r = {pearsonr(x, y).statistic:.3f}\n"
        f"R² = {linear_model.rvalue**2:.3f}"
    )

    ax.text(
        0.05,
        0.95,
        annotation,
        transform=ax.transAxes,
        verticalalignment="top",
        bbox={"boxstyle": "round", "alpha": 0.15},
    )

    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)


def safe_filename(text: str) -> str:
    """Create a safe lowercase filename fragment."""
    return (
        text.replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
        .replace("__", "_")
        .lower()
    )


def main() -> None:
    """Run SQI validation diagnostics."""
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(INPUT_PATH)

    required_columns = RESPONSE_COLUMNS + SQI_COLUMNS
    validate_required_columns(df, required_columns)

    results = []

    for response_column in RESPONSE_COLUMNS:
        for sqi_column in SQI_COLUMNS:
            results.append(
                validate_sqi_response(
                    df=df,
                    sqi_column=sqi_column,
                    response_column=response_column,
                )
            )

            figure_path = (
                FIGURES_DIR
                / f"sqi_validation_{safe_filename(response_column)}_{safe_filename(sqi_column)}.png"
            )

            make_validation_plot(
                df=df,
                sqi_column=sqi_column,
                response_column=response_column,
                output_path=figure_path,
            )

    summary = pd.DataFrame(results)

    summary = summary.sort_values(
        by=["response_variable", "spearman_rho"],
        ascending=[True, False],
    )

    output_path = TABLES_DIR / "sqi_validation_summary.csv"
    summary.to_csv(output_path, index=False)

    print("SQI validation completed.")
    print(f"Input file: {INPUT_PATH}")
    print(f"Validation summary: {output_path}")
    print(f"Figures directory: {FIGURES_DIR}")
    print()
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
