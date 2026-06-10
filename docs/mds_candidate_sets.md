# Candidate MDS Sets

This document records the current candidate minimum data set (MDS) configurations derived from PCA, redundancy analysis, exploratory correlations with relative yield, and preliminary SQI validation.

## Rationale

Candidate indicators were selected from a reduced set of soil biological, chemical, physical, salinity, sodicity, and organic matter variables. The selection considered:

* PCA contribution across retained components;
* Spearman correlation with relative yield per plant;
* redundancy among candidate indicators;
* interpretability for irrigated mango orchards in semiarid conditions;
* preliminary SQI validation behavior.

The preliminary upper limit for the MDS was set at approximately 12 indicators, corresponding to one quarter of the sample size (`n = 48`). This limit was used as a practical guideline to avoid an overextended SQI while preserving the main soil quality dimensions represented in the dataset.

## Main candidate set: `MDS11_main`

`MDS11_main` is the principal preliminary SQI candidate set.

It includes 11 indicators:

* `MO_g_dm3`
* `GMea`
* `Arilsulf`
* `Ca_Troc_cmolc_Kg`
* `K_Troc_cmolc_Kg`
* `Floculacao_pct`
* `Ds_g_cm3`
* `PST`
* `PM1_mg_dm3`
* `pH`
* `CE_dS_m`

This set prioritizes parsimony and interpretability. It retains indicators representing organic matter, biological activity, fertility, soil structure, bulk density, sodicity, phosphorus extraction, pH, and electrical conductivity.

`PST` is retained as the primary sodicity indicator because it showed a stronger association with relative yield and had high influence in SQI component diagnostics. `Na_Troc_cmolc_Kg` was not included in the main set because its direct association with relative yield was weaker.

## Sensitivity set: `MDS12_sodicity`

`MDS12_sodicity` adds exchangeable sodium to the main candidate set:

* `MO_g_dm3`
* `GMea`
* `Arilsulf`
* `Ca_Troc_cmolc_Kg`
* `K_Troc_cmolc_Kg`
* `Floculacao_pct`
* `Ds_g_cm3`
* `PST`
* `Na_Troc_cmolc_Kg`
* `PM1_mg_dm3`
* `pH`
* `CE_dS_m`

This version was retained as a sodicity-expanded sensitivity analysis because `Na_Troc_cmolc_Kg` contributed to PCA structure and did not exceed the high-redundancy threshold with `PST`.

Preliminary SQI validation indicated that adding `Na_Troc_cmolc_Kg` improved the SQI relationship with relative yield only marginally. Therefore, `MDS12_sodicity` is useful as a sensitivity set, but it does not replace `MDS11_main` as the principal candidate version.

## Scoring sensitivity set: `MDS11_pH_optimum`

`MDS11_pH_optimum` uses the same 11 indicators as `MDS11_main`, but tests an alternative pH scoring method.

In this version, pH is scored using an optimum-range function instead of the linear scoring rule used in the main SQI version. The tested optimum interval is 6.5–7.5.

This candidate set does not represent a different MDS composition. It is a scoring sensitivity analysis designed to evaluate whether pH should be treated as an optimum-range indicator rather than as a linear indicator.

Preliminary diagnostics did not support replacing the main pH scoring rule. Therefore, `MDS11_pH_optimum` is retained only as a methodological sensitivity test.

## Texture-expanded alternatives

Texture-expanded alternatives using `Argila_g_kg` or `Areia_g_kg` were explored as possible MDS extensions. These alternatives were useful for comparison but are not currently retained as primary candidate sets.

The main reason is that the current SQI workflow prioritizes the more parsimonious `MDS11_main` and the sodicity-focused sensitivity version `MDS12_sodicity`. Texture variables may still be reconsidered in future analyses if they improve validation, interpretation, or mixed-model behavior.

## Current interpretation

The current SQI workflow treats:

* `MDS11_main` as the principal preliminary SQI version;
* `MDS12_sodicity` as a sodicity-expanded sensitivity version;
* `MDS11_pH_optimum` as a scoring sensitivity version.

At this stage, `PST` remains the primary sodicity indicator. `Na_Troc_cmolc_Kg` is useful for sensitivity analysis, but it is not prioritized in the main MDS because its additional contribution is limited.

The final SQI version should be selected based on validation performance, interpretability, parsimony, agronomic coherence, and later mixed-model evaluation.
