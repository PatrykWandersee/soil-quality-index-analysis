"""Create manuscript-oriented comparison figures for SQI candidates.

This script uses the consolidated SQI candidate validation table to create
simple comparison figures for the main validation metrics.

Inputs
------
tables/private/sqi_candidate_validation_table.csv

Outputs
-------
figures/private/sqi/manuscript/sqi_candidate_comparison_spearman_rho.png
figures/private/sqi/manuscript/sqi_candidate_comparison_spearman_rho.pdf
figures/private/sqi/manuscript/sqi_candidate_comparison_ols_r2.png
figures/private/sqi/manuscript/sqi_candidate_comparison_ols_r2.pdf
figures/private/sqi/manuscript/sqi_candidate_comparison_farm_fixed_r2.png
figures/private/sqi/manuscript/sqi_candidate_comparison_farm_fixed_r2.pdf
figures/private/sqi/manuscript/sqi_candidate_comparison_without_experimental.png
figures/private/sqi/manuscript/sqi_candidate_comparison_without_experimental.pdf
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


INPUT_PATH = Path("tables/private/sqi_candidate_validation_table.csv")
OUTPUT_DIR = Path("figures/private/sqi/manuscript")

CANDIDATE_ORDER = [
    "MDS10 without CE",
    "MDS11 sodicity without CE",
    "MDS2 thesis compact",
    "MDS10 pH optimum without CE",
    "MDS11 main with CE",
    "MDS12 sodicity with CE",
    "MDS11 pH optimum with CE",
]

METRICS = [
    {
        "column": "Spearman rho",
        "label": "Spearman rho",
        "file_stem": "sqi_candidate_comparison_spearman_rho",
        "xlim": (0, 0.8),
    },
    {
        "column": "OLS R²",
        "label": "OLS R²",
        "file_stem": "sqi_candidate_comparison_ols_r2",
        "xlim": (0, 0.8),
    },
    {
        "column": "Farm fixed R²",
        "label": "Farm fixed-effect OLS R²",
        "file_stem": "sqi_candidate_comparison_farm_fixed_r2",
        "xlim": (0, 0.8),
    },
    {
        "column": "Spearman rho without Experimental",
        "label": "Spearman rho without Experimental",
        "file_stem": "sqi_candidate_comparison_without_experimental",
        "xlim": (0, 0.8),
    },
]


def validate_required_columns(df: pd.DataFrame, required_columns: list[str]) -> None:
    """Check whether all required columns are present."""
    missing_columns = [column for column in required_columns if column not in df.columns]

    if missing_columns:
        missing_text = "\n".join(f"- {column}" for column in missing_columns)
        raise ValueError(f"Missing required columns:\n{missing_text}")


def prepare_table(df: pd.DataFrame) -> pd.DataFrame:
    """Prepare candidate comparison table for plotting."""
    required_columns = ["SQI candidate", *[metric["column"] for metric in METRICS]]
    validate_required_columns(df, required_columns)

    output = df.copy()

    output["candidate_order"] = output["SQI candidate"].map(
        {candidate: index for index, candidate in enumerate(CANDIDATE_ORDER)}
    )

    output = output.sort_values("candidate_order").drop(columns="candidate_order")

    for metric in METRICS:
        column = metric["column"]
        output[column] = pd.to_numeric(output[column], errors="coerce")

    return output


def create_bar_figure(
    df: pd.DataFrame,
    metric_column: str,
    metric_label: str,
    output_stem: str,
    xlim: tuple[float, float],
) -> None:
    """Create one horizontal bar figure for one validation metric."""
    fig, ax = plt.subplots(figsize=(8.5, 5.8))

    candidates = df["SQI candidate"].tolist()
    values = df[metric_column].tolist()

    y_positions = range(len(candidates))

    ax.barh(y_positions, values)
    ax.set_yticks(y_positions)
    ax.set_yticklabels(candidates)
    ax.invert_yaxis()

    ax.set_xlabel(metric_label)
    ax.set_xlim(*xlim)

    for y_position, value in zip(y_positions, values):
        if pd.notna(value):
            ax.text(
                value + 0.01,
                y_position,
                f"{value:.3f}",
                va="center",
            )

    ax.set_title(f"SQI candidate comparison: {metric_label}")

    fig.tight_layout()

    png_path = OUTPUT_DIR / f"{output_stem}.png"
    pdf_path = OUTPUT_DIR / f"{output_stem}.pdf"

    fig.savefig(png_path, dpi=300)
    fig.savefig(pdf_path)

    plt.close(fig)

    print(f"Created: {png_path}")
    print(f"Created: {pdf_path}")


def create_combined_panel(df: pd.DataFrame) -> None:
    """Create a 2 x 2 panel comparing all validation metrics."""
    fig, axes = plt.subplots(2, 2, figsize=(13.0, 9.5))
    axes = axes.flatten()

    candidates = df["SQI candidate"].tolist()
    y_positions = range(len(candidates))

    for ax, metric in zip(axes, METRICS):
        column = metric["column"]
        label = metric["label"]
        values = df[column].tolist()

        ax.barh(y_positions, values)
        ax.set_yticks(y_positions)
        ax.set_yticklabels(candidates)
        ax.invert_yaxis()
        ax.set_xlim(*metric["xlim"])
        ax.set_xlabel(label)
        ax.set_title(label)

        for y_position, value in zip(y_positions, values):
            if pd.notna(value):
                ax.text(
                    value + 0.01,
                    y_position,
                    f"{value:.3f}",
                    va="center",
                )

    fig.suptitle("SQI candidate comparison", y=1.02)
    fig.tight_layout()

    png_path = OUTPUT_DIR / "sqi_candidate_comparison_panel.png"
    pdf_path = OUTPUT_DIR / "sqi_candidate_comparison_panel.pdf"

    fig.savefig(png_path, dpi=300, bbox_inches="tight")
    fig.savefig(pdf_path, bbox_inches="tight")

    plt.close(fig)

    print(f"Created: {png_path}")
    print(f"Created: {pdf_path}")


def main() -> None:
    """Create SQI candidate comparison figures."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(INPUT_PATH)
    df = prepare_table(df)

    for metric in METRICS:
        create_bar_figure(
            df=df,
            metric_column=metric["column"],
            metric_label=metric["label"],
            output_stem=metric["file_stem"],
            xlim=metric["xlim"],
        )

    create_combined_panel(df)

    print()
    print("SQI candidate comparison figures created.")
    print(f"Input table: {INPUT_PATH}")
    print(f"Output directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
