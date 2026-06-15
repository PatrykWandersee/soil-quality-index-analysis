"""Create a manuscript-oriented validation figure for the main SQI version.

This script creates the main candidate figure for SQI validation using the
principal preliminary SQI version and relative yield per plant.

Inputs
------
data/processed/private/soil_quality_selected_sqi_versions_private.csv

Outputs
-------
figures/private/sqi/manuscript/sqi_main_validation_figure.png
figures/private/sqi/manuscript/sqi_main_validation_figure.pdf
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import linregress, spearmanr


INPUT_PATH = Path("data/processed/private/soil_quality_selected_sqi_versions_private.csv")
OUTPUT_DIR = Path("figures/private/sqi/manuscript")

SQI_COLUMN = "MDS11_main_SQI"
RESPONSE_COLUMN = "Prod_rel_pct"

PNG_OUTPUT = OUTPUT_DIR / "sqi_main_validation_figure.png"
PDF_OUTPUT = OUTPUT_DIR / "sqi_main_validation_figure.pdf"


def validate_required_columns(df: pd.DataFrame, required_columns: list[str]) -> None:
    """Check whether all required columns are present in the dataset."""
    missing_columns = [column for column in required_columns if column not in df.columns]

    if missing_columns:
        missing_text = "\n".join(f"- {column}" for column in missing_columns)
        raise ValueError(f"Missing required columns:\n{missing_text}")


def format_p_value(p_value: float) -> str:
    """Format p-values for figure annotations."""
    if p_value < 0.001:
        return "< 0.001"
    return f"= {p_value:.3f}"


def main() -> None:
    """Create the manuscript-oriented SQI validation figure."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(INPUT_PATH)

    validate_required_columns(df, [SQI_COLUMN, RESPONSE_COLUMN])

    data = df[[SQI_COLUMN, RESPONSE_COLUMN]].dropna().copy()

    x = data[SQI_COLUMN].to_numpy()
    y = data[RESPONSE_COLUMN].to_numpy()

    spearman_rho, spearman_p = spearmanr(x, y)
    linear_model = linregress(x, y)

    x_line = np.linspace(x.min(), x.max(), 100)
    y_line = linear_model.intercept + linear_model.slope * x_line

    fig, ax = plt.subplots(figsize=(6.5, 4.8))

    ax.scatter(x, y, alpha=0.8)
    ax.plot(x_line, y_line)

    ax.set_xlabel("Soil Quality Index (MDS11 main)")
    ax.set_ylabel("Relative yield per plant (%)")

    annotation = (
        f"n = {len(data)}\n"
        f"Spearman ρ = {spearman_rho:.3f}\n"
        f"p {format_p_value(spearman_p)}\n"
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

    fig.savefig(PNG_OUTPUT, dpi=300)
    fig.savefig(PDF_OUTPUT)

    plt.close(fig)

    print("Main SQI validation figure created.")
    print(f"Input file: {INPUT_PATH}")
    print(f"PNG output: {PNG_OUTPUT}")
    print(f"PDF output: {PDF_OUTPUT}")
    print()
    print(f"n = {len(data)}")
    print(f"Spearman rho = {spearman_rho:.6f}")
    print(f"Spearman p = {spearman_p:.6g}")
    print(f"Linear R2 = {linear_model.rvalue**2:.6f}")


if __name__ == "__main__":
    main()
