"""Create a manuscript-oriented SQI candidate validation table.

This script consolidates the main validation outputs into a compact table for
manuscript interpretation. The table includes simple OLS equations relating
relative yield per plant to each SQI candidate.

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

import pandas as pd


VALIDATION_PATH = Path("tables/private/sqi_validation_summary.csv")
MODEL_VALIDATION_PATH = Path("tables/private/sqi_model_validation_summary.csv")
EXPERIMENTAL_SENSITIVITY_PATH = Path(
    "tables/private/experimental_group_correlation_sensitivity.csv"
)

OUTPUT_CSV = Path("tables/private/sqi_candidate_validation_table.csv")
OUTPUT_MD = Path("tables/private/sqi_candidate_validation_table.md")

RESPONSE_VARIABLE = "Prod_rel_pct"

CANDIDATE_LABELS = {
    "MDS11_main_SQI": "MDS11 main",
    "MDS2_thesis_compact_linear_SQI": "MDS2 thesis compact",
    "MDS12_sodicity_SQI": "MDS12 sodicity",
    "MDS11_pH_optimum_SQI": "MDS11 pH optimum",
}

CANDIDATE_ORDER = {
    "MDS11_main_SQI": 1,
    "MDS2_thesis_compact_linear_SQI": 2,
    "MDS12_sodicity_SQI": 3,
    "MDS11_pH_optimum_SQI": 4,
}


def get_single_row(df: pd.DataFrame, **filters: str) -> pd.Series:
    """Return a single row matching all filters."""
    subset = df.copy()

    for column, value in filters.items():
        subset = subset[subset[column] == value]

    if subset.empty:
        filter_text = ", ".join(f"{key}={value}" for key, value in filters.items())
        raise ValueError(f"No row found for filters: {filter_text}")

    return subset.iloc[0]


def format_number(value: float, digits: int = 3) -> str:
    """Format numeric values for manuscript tables."""
    if pd.isna(value):
        return ""
    return f"{float(value):.{digits}f}"


def format_p_value(value: float) -> str:
    """Format p-values for manuscript tables."""
    if pd.isna(value):
        return ""
    if float(value) < 0.001:
        return "<0.001"
    return f"{float(value):.3f}"


def format_ols_equation(intercept: float, slope: float) -> str:
    """Format the simple OLS equation for manuscript output."""
    sign = "+" if slope >= 0 else "-"
    return f"y = {intercept:.2f} {sign} {abs(slope):.2f} × SQI"


def dataframe_to_markdown(df: pd.DataFrame) -> str:
    """Create a simple Markdown table without external dependencies."""
    headers = list(df.columns)
    rows = df.astype(str).values.tolist()

    header_line = "| " + " | ".join(headers) + " |"
    separator_line = "| " + " | ".join(["---"] * len(headers)) + " |"
    row_lines = ["| " + " | ".join(row) + " |" for row in rows]

    return "\n".join([header_line, separator_line, *row_lines])


def main() -> None:
    """Create the manuscript-oriented validation table."""
    validation = pd.read_csv(VALIDATION_PATH)
    model_validation = pd.read_csv(MODEL_VALIDATION_PATH)
    experimental_sensitivity = pd.read_csv(EXPERIMENTAL_SENSITIVITY_PATH)

    rows = []

    for sqi_version in sorted(CANDIDATE_LABELS, key=CANDIDATE_ORDER.get):
        simple = get_single_row(
            validation,
            sqi_version=sqi_version,
            response_variable=RESPONSE_VARIABLE,
        )

        farm_fixed = get_single_row(
            model_validation,
            sqi_version=sqi_version,
            model_type="ols_farm_fixed_effect",
        )

        mixed = get_single_row(
            model_validation,
            sqi_version=sqi_version,
            model_type="mixed_farm_random_intercept",
        )

        without_experimental = get_single_row(
            experimental_sensitivity,
            dataset="without_experimental",
            response_variable=RESPONSE_VARIABLE,
            sqi_version=sqi_version,
        )

        rows.append(
            {
                "SQI candidate": CANDIDATE_LABELS[sqi_version],
                "Spearman rho": format_number(simple["spearman_rho"]),
                "Spearman p": format_p_value(simple["spearman_p"]),
                "Pearson r": format_number(simple["pearson_r"]),
                "OLS equation": format_ols_equation(
                    intercept=float(simple["linear_intercept"]),
                    slope=float(simple["linear_slope"]),
                ),
                "OLS R²": format_number(simple["linear_r2"]),
                "OLS RMSE": format_number(simple["rmse"]),
                "Farm fixed R²": format_number(farm_fixed["r2"]),
                "Farm fixed AIC": format_number(farm_fixed["aic"]),
                "Spearman rho without Experimental": format_number(
                    without_experimental["spearman_rho"]
                ),
                "Mixed-model note": mixed["model_note"],
            }
        )

    output = pd.DataFrame(rows)

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    output.to_csv(OUTPUT_CSV, index=False)

    markdown_table = dataframe_to_markdown(output)
    note = (
        "\n\nNote: all validation metrics are based on `Prod_rel_pct`. "
        "The OLS equation represents the simple linear model "
        "`Prod_rel_pct = intercept + slope × SQI`. "
        "The mixed random-intercept model is treated as diagnostic when the "
        "farm-level random effect converges at the boundary or is singular.\n"
    )

    OUTPUT_MD.write_text(markdown_table + note, encoding="utf-8")

    print("SQI candidate validation table created.")
    print(f"Input validation table: {VALIDATION_PATH}")
    print(f"Input model validation table: {MODEL_VALIDATION_PATH}")
    print(f"Input Experimental sensitivity table: {EXPERIMENTAL_SENSITIVITY_PATH}")
    print(f"Output CSV: {OUTPUT_CSV}")
    print(f"Output Markdown: {OUTPUT_MD}")
    print()
    print(markdown_table)
    print(note)


if __name__ == "__main__":
    main()
