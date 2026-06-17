"""Validate SQI candidate versions using simple and farm-structured models.

This script compares selected Soil Quality Index (SQI) versions using:

1. ordinary least squares (OLS);
2. OLS with farm as a fixed effect;
3. mixed linear models with farm as a random intercept.

The goal is to evaluate whether SQI-yield relationships remain meaningful
after accounting for farm-level structure.

Inputs
------
data/processed/private/soil_quality_selected_sqi_versions_private.csv

Outputs
-------
tables/private/sqi_model_validation_summary.csv
"""

from pathlib import Path
import warnings

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


INPUT_PATH = Path("data/processed/private/soil_quality_selected_sqi_versions_private.csv")
TABLES_DIR = Path("tables/private")
OUTPUT_PATH = TABLES_DIR / "sqi_model_validation_summary.csv"

RESPONSE_COLUMN = "Prod_rel_pct"
GROUP_COLUMN = "Fazenda"

SQI_COLUMNS = [
    "MDS10_without_CE_SQI",
    "MDS11_sodicity_without_CE_SQI",
    "MDS2_thesis_compact_linear_SQI",
    "MDS10_pH_optimum_without_CE_SQI",
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


def calculate_rmse(observed: np.ndarray, predicted: np.ndarray) -> float:
    """Calculate root mean squared error."""
    return float(np.sqrt(np.mean((observed - predicted) ** 2)))


def calculate_mae(observed: np.ndarray, predicted: np.ndarray) -> float:
    """Calculate mean absolute error."""
    return float(np.mean(np.abs(observed - predicted)))


def summarize_ols_model(
    model,
    data: pd.DataFrame,
    sqi_column: str,
    model_type: str,
) -> dict[str, object]:
    """Summarize fitted OLS model diagnostics."""
    predicted = model.fittedvalues.to_numpy()
    observed = data[RESPONSE_COLUMN].to_numpy()

    return {
        "sqi_version": sqi_column,
        "model_type": model_type,
        "n": int(model.nobs),
        "n_farms": int(data[GROUP_COLUMN].nunique()),
        "sqi_slope": float(model.params.get(sqi_column, np.nan)),
        "sqi_p_value": float(model.pvalues.get(sqi_column, np.nan)),
        "r2": float(model.rsquared),
        "adj_r2": float(model.rsquared_adj),
        "aic": float(model.aic),
        "bic": float(model.bic),
        "rmse": calculate_rmse(observed, predicted),
        "mae": calculate_mae(observed, predicted),
        "farm_variance": np.nan,
        "residual_variance": float(np.var(model.resid, ddof=1)),
        "model_note": "ok",
        "converged": np.nan,
        "error_message": "",
    }


def summarize_failed_model(
    sqi_column: str,
    model_type: str,
    data: pd.DataFrame,
    note: str,
    error: Exception,
) -> dict[str, object]:
    """Return a standardized row for a model that failed to fit."""
    return {
        "sqi_version": sqi_column,
        "model_type": model_type,
        "n": int(len(data)),
        "n_farms": int(data[GROUP_COLUMN].nunique()),
        "sqi_slope": np.nan,
        "sqi_p_value": np.nan,
        "r2": np.nan,
        "adj_r2": np.nan,
        "aic": np.nan,
        "bic": np.nan,
        "rmse": np.nan,
        "mae": np.nan,
        "farm_variance": np.nan,
        "residual_variance": np.nan,
        "model_note": note,
        "converged": False,
        "error_message": str(error),
    }


def summarize_mixed_model(
    result,
    data: pd.DataFrame,
    sqi_column: str,
) -> dict[str, object]:
    """Summarize fitted mixed model diagnostics."""
    farm_variance = np.nan

    try:
        if result.cov_re is not None and result.cov_re.shape[0] > 0:
            farm_variance = float(result.cov_re.iloc[0, 0])
    except (ValueError, np.linalg.LinAlgError):
        farm_variance = np.nan

    residual_variance = float(result.scale)

    aic = float(result.aic) if result.aic is not None else np.nan
    bic = float(result.bic) if result.bic is not None else np.nan

    boundary_or_singular = (
        not np.isfinite(aic)
        or not np.isfinite(bic)
        or (np.isfinite(farm_variance) and farm_variance < 1e-8)
    )

    if boundary_or_singular:
        return {
            "sqi_version": sqi_column,
            "model_type": "mixed_farm_random_intercept",
            "n": int(result.nobs),
            "n_farms": int(data[GROUP_COLUMN].nunique()),
            "sqi_slope": float(result.params.get(sqi_column, np.nan)),
            "sqi_p_value": float(result.pvalues.get(sqi_column, np.nan)),
            "r2": np.nan,
            "adj_r2": np.nan,
            "aic": np.nan,
            "bic": np.nan,
            "rmse": np.nan,
            "mae": np.nan,
            "farm_variance": farm_variance,
            "residual_variance": residual_variance,
            "model_note": "boundary_or_singular_random_effect",
            "converged": bool(result.converged),
            "error_message": "",
        }

    predicted = result.predict(data).to_numpy()
    observed = data[RESPONSE_COLUMN].to_numpy()

    return {
        "sqi_version": sqi_column,
        "model_type": "mixed_farm_random_intercept",
        "n": int(result.nobs),
        "n_farms": int(data[GROUP_COLUMN].nunique()),
        "sqi_slope": float(result.params.get(sqi_column, np.nan)),
        "sqi_p_value": float(result.pvalues.get(sqi_column, np.nan)),
        "r2": np.nan,
        "adj_r2": np.nan,
        "aic": aic,
        "bic": bic,
        "rmse": calculate_rmse(observed, predicted),
        "mae": calculate_mae(observed, predicted),
        "farm_variance": farm_variance,
        "residual_variance": residual_variance,
        "model_note": "ok",
        "converged": bool(result.converged),
        "error_message": "",
    }


def fit_models_for_sqi(df: pd.DataFrame, sqi_column: str) -> list[dict[str, object]]:
    """Fit OLS, fixed-farm OLS, and random-intercept mixed model."""
    data = df[[RESPONSE_COLUMN, GROUP_COLUMN, sqi_column]].dropna().copy()

    results = []

    ols_formula = f"{RESPONSE_COLUMN} ~ {sqi_column}"
    ols_model = smf.ols(ols_formula, data=data).fit()

    results.append(
        summarize_ols_model(
            model=ols_model,
            data=data,
            sqi_column=sqi_column,
            model_type="ols_simple",
        )
    )

    fixed_farm_formula = f"{RESPONSE_COLUMN} ~ {sqi_column} + C({GROUP_COLUMN})"
    fixed_farm_model = smf.ols(fixed_farm_formula, data=data).fit()

    results.append(
        summarize_ols_model(
            model=fixed_farm_model,
            data=data,
            sqi_column=sqi_column,
            model_type="ols_farm_fixed_effect",
        )
    )

    mixed_formula = f"{RESPONSE_COLUMN} ~ {sqi_column}"

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            mixed_model = smf.mixedlm(
                mixed_formula,
                data=data,
                groups=data[GROUP_COLUMN],
            )
            mixed_result = mixed_model.fit(reml=False, method="lbfgs")

        results.append(
            summarize_mixed_model(
                result=mixed_result,
                data=data,
                sqi_column=sqi_column,
            )
        )

    except Exception as error:
        results.append(
            summarize_failed_model(
                sqi_column=sqi_column,
                model_type="mixed_farm_random_intercept",
                data=data,
                note="mixed_model_fit_failed",
                error=error,
            )
        )

    return results


def main() -> None:
    """Run model-based SQI validation."""
    TABLES_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(INPUT_PATH)

    required_columns = [RESPONSE_COLUMN, GROUP_COLUMN] + SQI_COLUMNS
    validate_required_columns(df, required_columns)

    all_results = []

    for sqi_column in SQI_COLUMNS:
        all_results.extend(fit_models_for_sqi(df, sqi_column))

    summary = pd.DataFrame(all_results)

    model_order = {
        "ols_simple": 1,
        "ols_farm_fixed_effect": 2,
        "mixed_farm_random_intercept": 3,
    }

    summary["_model_order"] = summary["model_type"].map(model_order)

    summary = summary.sort_values(
        by=["_model_order", "aic"],
        ascending=[True, True],
        na_position="last",
    ).drop(columns=["_model_order"])

    summary.to_csv(OUTPUT_PATH, index=False)

    print("SQI model validation completed.")
    print(f"Input file: {INPUT_PATH}")
    print(f"Output file: {OUTPUT_PATH}")
    print()
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
