# Decision Log

This document records methodological decisions made during the development of the soil quality index workflow.

## 2026-06-08 — Clay-normalized indicators

Clay-normalized indicators were tested for Mehlich-1 P and GMea.

Initial Spearman screening showed that clay normalization did not improve the association with relative yield per plant:

- `PM1_mg_dm3` showed stronger association than `PM1_per_Clay`.
- `GMea` showed slightly stronger association than `GMea_per_Clay`.

Decision: retain `PM1_mg_dm3` and `GMea` as main candidate indicators. Keep clay-normalized versions for sensitivity analysis and later mixed-model comparison.

## 2026-06-08 — Main and sensitivity MDS sets

Two SQI candidate sets were retained:

- `MDS11_main`: main parsimonious candidate set.
- `MDS12_sodicity`: sensitivity set including `Na_Troc_cmolc_Kg`.

`PST` was retained as the primary sodicity indicator because it showed stronger association with relative yield and had high influence in SQI component diagnostics. `Na_Troc_cmolc_Kg` improved SQI validation only marginally and was therefore retained only in the sensitivity set.

## 2026-06-08 — Electrical conductivity scoring

In the original thesis interpretation, `CE_dS_m` behaved partly as a fertility proxy because observed salinity levels were low. However, for SQI scoring, `CE_dS_m` was treated conservatively as a "less is better" indicator because elevated electrical conductivity represents salinity risk in irrigated systems.

Decision: use the conservative CE scoring direction in the main preliminary SQI. Retain data-driven scoring only as sensitivity analysis.

## 2026-06-08 — Organic matter instead of calculated organic carbon

Both soil organic matter (`MO_g_dm3`) and calculated organic carbon (`C_org_g_d3`) were available in the dataset. `MO_g_dm3` was retained as the main indicator because it was directly measured, whereas `C_org_g_d3` was calculated from organic matter.

Decision: use `MO_g_dm3` in the MDS and treat `C_org_g_d3` as a derived redundant variable.

## 2026-06-10 – pH optimum-range sensitivity scoring

An additional sensitivity candidate set (`MDS11_pH_optimum`) was added to test whether pH should be scored using an optimum-range function instead of the linear scoring rule used in the main SQI version.

In this sensitivity set, pH receives the maximum score within the 6.5–7.5 range, with lower scores assigned to values below or above this interval. This approach was tested because pH has a known agronomic optimum range and does not necessarily behave as a simple "more is better" indicator.

The diagnostic results did not support replacing the main pH scoring rule. The optimum-range version did not improve the SQI relationship with relative yield, and leave-one-out diagnostics indicated that removing the pH component improved SQI performance in this sensitivity set.

Decision: keep `MDS11_main` as the principal SQI version and retain `MDS11_pH_optimum` only as a sensitivity analysis.

Implication: pH scoring remains transparent and data-driven in the main SQI version, while the optimum-range approach is documented as an alternative methodological test.

## 2026-06-10 – Project scope prioritization

The current repository will remain focused on the Soil Quality Index (SQI) workflow for irrigated mango orchards.

Although the full research context includes additional analyses related to enzyme activity thresholds and phosphorus extractor behavior, these topics will not be expanded within this repository at this stage.

Decision: keep `soil-quality-index-analysis` focused on the SQI article, including indicator screening, PCA/MDS selection, scoring rules, SQI construction, validation, and documentation of methodological decisions.

Implication: enzyme threshold analyses and phosphorus extractor analyses may be developed later as separate repositories or companion projects, instead of being merged into the current SQI workflow.

## 2026-06-10 – Preliminary SQI validation diagnostics

A new validation script (`scripts/14_validate_sqi_models.py`) was added to compare selected SQI candidate versions against yield response variables using simple association and regression diagnostics.

The validation table includes Spearman correlation, Pearson correlation, linear regression slope and intercept, R², RMSE, and MAE for each SQI-response combination.

Preliminary results confirmed that `Prod_rel_pct` remains the most useful response variable for SQI validation. Relationships with `Prod_rel_ha_pct` were weak across all candidate SQI versions.

For `Prod_rel_pct`, `MDS12_sodicity_SQI` showed the strongest numerical validation performance, followed closely by `MDS11_pH_optimum_SQI` and `MDS11_main_SQI`. However, the improvement of `MDS12_sodicity_SQI` over `MDS11_main_SQI` remains relatively small.

Decision: retain `MDS11_main` as the principal preliminary SQI version because it is more parsimonious and interpretable, while retaining `MDS12_sodicity` as the main sensitivity version.

Implication: validation results support the current project structure, with one principal SQI version and sensitivity analyses used to evaluate specific methodological alternatives.

## 2026-06-10 – Farm-structured SQI validation

A farm-structured validation script (`scripts/15_validate_sqi_mixed_models.py`) was added to compare selected SQI versions using three model structures:

- simple OLS;
- OLS with farm as a fixed effect;
- mixed linear model with farm as a random intercept.

The simple OLS results favored `MDS12_sodicity_SQI` numerically, indicating that the sodicity-expanded version had the strongest unadjusted relationship with relative yield per plant.

After accounting for farm as a fixed effect, `MDS11_main_SQI` showed the best model performance among the tested SQI versions. This supports the interpretation that the main parsimonious SQI version remains robust when farm-level differences are considered.

The mixed model with farm as a random intercept converged at the boundary, with farm-level variance estimated as zero. Therefore, the random-intercept model is treated as a diagnostic result rather than as the main validation model.

Decision: retain `MDS11_main` as the principal preliminary SQI version and retain `MDS12_sodicity` as the main sensitivity version.

Implication: farm-structured validation reinforces the current project interpretation: the sodicity-expanded SQI is useful for sensitivity analysis, but the simpler main SQI version remains preferable for the primary workflow because of parsimony, interpretability, and performance after accounting for farm-level structure.
