"""Create a manuscript-oriented SQI candidate validation table.

This script consolidates outputs from previous validation scripts into a
single candidate-comparison table.

Inputs
------
tables/private/sqi_validation_summary.csv
tables/private/sqi_model_validation_summary.csv
tables/private/experimental_group_correlation_sensitivity.csv

Outputs
-------
tables/private/sqi_candidate_validation_table.csv
tables/private/sqi_candidate_validation_table.md
"""

from pathlib import Path

import numpy as np
import pandas as pd


TABLES_DIR = Path("tables/private")

VALIDATION_PATH = TABLES_DIR / "sqi_validation_summary.csv"
MODEL_VALIDATION_PATH = TABLES_DIR / "sqi_model_validation_summary.csv"
EXPERIMENTAL_SENSITIVITY_PATH = (
    TABLES_DIR / "experimental_group_correlation_sensitivity.csv"
)

OUTPUT_CSV = TABLES_DIR / "sqi_candidate_validation_table.csv"
OUTPUT_MD = TABLES_DIR / "sqi_candidate_validation_table.md"

MAIN_RESPONSE = "Prod_rel_pct"

SQI_LABELS = {
    "MDS11_main_SQI": "MDS11 main",
    "MDS12_sodicity_SQI": "MDS12 sodicity",
    "MDS11_pH_optimum_SQI": "MDS11 pH optimum",
}

SQI_ORDER = {
    "MDS11_main_SQI": 1,
    "MDS12_sodicity_SQI": 2,
    "MDS11_pH_optimum_SQI": 3,
}


def check_input_files(paths: list[Path]) -> None:
    """Raise an informative error if required input files are missing."""
    missing_paths = [path for path in paths if not path.exists()]

    if missing_paths:
        missing_text = "\n".join(f"- {path}" for path in missing_paths)
        raise FileNotFoundError(
            "Missing required input files. Run scripts 14, 15, and 16 first:\n"
            f"{missing_text}"
        )


def format_float(value: float, digits: int = 3) -> str:
    """Format floats for markdown output."""
    if pd.isna(value):
        return ""
    return f"{value:.{digits}f}"


def format_p_value(value: float) -> str:
    """Format p-values for markdown output."""
    if pd.isna(value):
        return ""
    if value < 0.001:
        return "<0.001"
    return f"{value:.3f}"


def create_markdown_table(summary: pd.DataFrame) -> str:
    """Create a compact markdown table for manuscript planning."""
    columns = [
        "candidate_label",
        "spearman_rho_all",
        "spearman_p_all",
        "pearson_r_all",
        "ols_simple_r2",
        "ols_simple_rmse",
        "ols_farm_fixed_r2",
        "ols_farm_fixed_aic",
        "spearman_rho_without_experimental",
        "mixed_model_note",
    ]

    headers = [
        "SQI candidate",
        "Spearman rho",
        "Spearman p",
        "Pearson r",
        "OLS R²",
        "OLS RMSE",
        "Farm fixed R²",
        "Farm fixed AIC",
        "Spearman rho without Experimental",
        "Mixed-model note",
    ]

    rows = []

    for _, row in summary[columns].iterrows():
        rows.append(
            [
                str(row["candidate_label"]),
                format_float(row["spearman_rho_all"]),
                format_p_value(row["spearman_p_all"]),
                format_float(row["pearson_r_all"]),
                format_float(row["ols_simple_r2"]),
                format_float(row["ols_simple_rmse"]),
                format_float(row["ols_farm_fixed_r2"]),
                format_float(row["ols_farm_fixed_aic"]),
                format_float(row["spearman_rho_without_experimental"]),
                str(row["mixed_model_note"]),
            ]
        )

    table_lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]

    for row in rows:
        table_lines.append("| " + " | ".join(row) + " |")

    note = (
        "\n\nNote: all validation metrics are based on `Prod_rel_pct`. "
        "The mixed random-intercept model is treated as diagnostic when the "
        "farm-level random effect converges at the boundary or is singular."
    )

    return "\n".join(table_lines) + note + "\n"


def main() -> None:
    """Create the consolidated SQI candidate validation table."""
    check_input_files(
        [
            VALIDATION_PATH,
            MODEL_VALIDATION_PATH,
            EXPERIMENTAL_SENSITIVITY_PATH,
        ]
    )

    validation = pd.read_csv(VALIDATION_PATH)
    model_validation = pd.read_csv(MODEL_VALIDATION_PATH)
    experimental_sensitivity = pd.read_csv(EXPERIMENTAL_SENSITIVITY_PATH)

    main_validation = validation[
        validation["response_variable"] == MAIN_RESPONSE
    ].copy()

    main_validation = main_validation[
        [
            "sqi_version",
            "n",
            "spearman_rho",
            "spearman_p",
            "pearson_r",
            "pearson_p",
            "linear_r2",
            "rmse",
            "mae",
        ]
    ].rename(
        columns={
            "n": "n_all",
            "spearman_rho": "spearman_rho_all",
            "spearman_p": "spearman_p_all",
            "pearson_r": "pearson_r_all",
            "pearson_p": "pearson_p_all",
            "linear_r2": "ols_simple_r2",
            "rmse": "ols_simple_rmse",
            "mae": "ols_simple_mae",
        }
    )

    farm_fixed = model_validation[
        model_validation["model_type"] == "ols_farm_fixed_effect"
    ].copy()

    farm_fixed = farm_fixed[
        [
            "sqi_version",
            "r2",
            "adj_r2",
            "aic",
            "bic",
            "rmse",
            "mae",
            "sqi_p_value",
        ]
    ].rename(
        columns={
            "r2": "ols_farm_fixed_r2",
            "adj_r2": "ols_farm_fixed_adj_r2",
            "aic": "ols_farm_fixed_aic",
            "bic": "ols_farm_fixed_bic",
            "rmse": "ols_farm_fixed_rmse",
            "mae": "ols_farm_fixed_mae",
            "sqi_p_value": "ols_farm_fixed_sqi_p",
        }
    )

    mixed = model_validation[
        model_validation["model_type"] == "mixed_farm_random_intercept"
    ].copy()

    mixed = mixed[
        [
            "sqi_version",
            "farm_variance",
            "residual_variance",
            "model_note",
            "converged",
        ]
    ].rename(
        columns={
            "farm_variance": "mixed_farm_variance",
            "residual_variance": "mixed_residual_variance",
            "model_note": "mixed_model_note",
            "converged": "mixed_converged",
        }
    )

    without_experimental = experimental_sensitivity[
        (experimental_sensitivity["dataset"] == "without_experimental")
        & (experimental_sensitivity["response_variable"] == MAIN_RESPONSE)
    ].copy()

    without_experimental = without_experimental[
        [
            "sqi_version",
            "n",
            "n_farms",
            "spearman_rho",
            "spearman_p",
            "pearson_r",
            "pearson_p",
        ]
    ].rename(
        columns={
            "n": "n_without_experimental",
            "n_farms": "n_farms_without_experimental",
            "spearman_rho": "spearman_rho_without_experimental",
            "spearman_p": "spearman_p_without_experimental",
            "pearson_r": "pearson_r_without_experimental",
            "pearson_p": "pearson_p_without_experimental",
        }
    )

    summary = (
        main_validation.merge(farm_fixed, on="sqi_version", how="left")
        .merge(mixed, on="sqi_version", how="left")
        .merge(without_experimental, on="sqi_version", how="left")
    )

    summary["candidate_label"] = summary["sqi_version"].map(SQI_LABELS)
    summary["_order"] = summary["sqi_version"].map(SQI_ORDER)

    summary = summary.sort_values("_order").drop(columns="_order")

    numeric_columns = summary.select_dtypes(include=[np.number]).columns
    summary[numeric_columns] = summary[numeric_columns].round(6)

    summary.to_csv(OUTPUT_CSV, index=False)

    markdown_table = create_markdown_table(summary)
    OUTPUT_MD.write_text(markdown_table, encoding="utf-8")

    print("SQI candidate validation table created.")
    print(f"Input validation table: {VALIDATION_PATH}")
    print(f"Input model validation table: {MODEL_VALIDATION_PATH}")
    print(f"Input Experimental sensitivity table: {EXPERIMENTAL_SENSITIVITY_PATH}")
    print(f"Output CSV: {OUTPUT_CSV}")
    print(f"Output Markdown: {OUTPUT_MD}")
    print()
    print(markdown_table)


if __name__ == "__main__":
    main()
