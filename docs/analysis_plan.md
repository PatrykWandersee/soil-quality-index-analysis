# Analysis Plan

This document outlines the current analytical workflow for developing and evaluating preliminary Soil Quality Index (SQI) versions for irrigated mango orchards in the Brazilian semiarid region.

## Current objective

The current objective is to document and refine a reproducible Python workflow for SQI development, starting from private soil and yield data and progressing through indicator screening, redundancy analysis, PCA interpretation, minimum data set (MDS) definition, scoring rule configuration, SQI construction, and preliminary validation.

The workflow is exploratory and manuscript-oriented. It is designed to support both scientific interpretation and public documentation of the analytical pipeline while keeping unpublished research data private.

## Response variables

The main response variables considered in the workflow are:

* `Prod_rel_pct`: relative yield per plant;
* `Prod_rel_ha_pct`: relative yield per hectare.

At this stage, `Prod_rel_pct` is treated as the primary response variable because it is more directly aligned with the original SQI validation approach and showed stronger relationships with soil quality indicators and candidate SQI versions.

`Prod_rel_ha_pct` is retained as a secondary response variable for comparison, but it is not currently used as the main validation target.

## Workflow stages

The current workflow is organized into sequential analytical stages:

1. check raw private data import;
2. verify derived indicator calculations;
3. prepare the processed private dataset;
4. screen candidate indicators against yield variables;
5. compare raw, normalized, and transformed indicator families;
6. create exploratory figures;
7. evaluate redundancy among candidate indicators;
8. run PCA on a reduced candidate indicator set;
9. define preliminary MDS candidate sets;
10. build preliminary SQI versions;
11. compare SQI candidate sets;
12. export selected SQI versions;
13. diagnose SQI component behavior;
14. summarize scoring ranges and indicator behavior.
15. validate selected SQI versions using association and simple regression diagnostics.

The corresponding scripts are stored in `scripts/` and numbered according to the workflow sequence.

## Indicator screening

Initial indicator screening uses Spearman correlation to evaluate relationships between candidate soil indicators and yield response variables.

This step is exploratory and is not intended to define the final MDS by itself. Its main purposes are to:

* compare measured and derived indicators within the same conceptual family;
* evaluate whether clay-normalized indicators improve interpretation;
* identify weak or redundant variables;
* support later PCA interpretation and MDS selection;
* document empirical relationships with relative yield.

## Variable family principle

Because the dataset contains measured variables, derived variables, ratios, and transformed indicators, the final analysis avoids treating all columns as independent indicators.

For each conceptual family, only one or a small number of representative indicators should be retained for PCA, MDS construction, and SQI development.

Examples include:

* phosphorus extraction: `PM1_mg_dm3`, `PM1_per_Clay`, or `log_PM1_per_Clay`;
* integrated enzyme activity: `GMea`, `GMea_per_Clay`, or `log_GMea_per_Clay`;
* beta-glucosidase activity: `Beta_glic`, `Beta_por_Argila`, or `qBeta`;
* arylsulfatase activity: `Arilsulf`, `Aril_por_Argila`, or `qAril`;
* organic matter and carbon: `MO_g_dm3` or `C_org_g_d3`;
* sodicity: `PST` or `Na_Troc_cmolc_Kg`.

Current decisions prioritize measured, interpretable, and non-redundant indicators when possible.

## PCA and MDS selection

PCA is used as a multivariate support step for understanding indicator structure and selecting candidate MDS sets.

The current PCA workflow uses a reduced candidate set rather than all available dataset columns. This avoids overrepresenting redundant indicator families and derived variables.

Candidate MDS sets are selected based on:

* PCA contributions and loadings;
* Spearman correlations with relative yield;
* redundancy analysis;
* soil process interpretation;
* parsimony;
* preliminary SQI validation behavior.

The current principal candidate set is `MDS11_main`. Sensitivity versions include `MDS12_sodicity` and `MDS11_pH_optimum`.

Further details are documented in `docs/mds_candidate_sets.md`.

## SQI construction

Preliminary SQI versions are built by transforming selected indicators into 0–1 scores and averaging the resulting scores within each candidate set.

Scoring rules are defined in `config/scoring_rules_mds.csv` and applied through utility functions in `scripts/sqi_utils.py`.

The current workflow supports:

* linear min-max scoring;
* optimum-range scoring for sensitivity analysis;
* `more_is_better` scoring direction;
* `less_is_better` scoring direction.

The main SQI version currently uses linear scoring. Alternative scoring assumptions are treated as sensitivity analyses unless they are supported by stronger validation or agronomic evidence.

Further details are documented in `docs/scoring_strategy.md`.

## Validation and diagnostics

Preliminary SQI validation is based mainly on the relationship between each candidate SQI version and relative yield per plant.

Current validation and diagnostic steps include:

* Spearman correlation between SQI versions and response variables;
* comparison among candidate SQI sets;
* leave-one-out SQI component diagnostics;
* evaluation of scoring assumptions;
* summary of indicator ranges and score behavior.

The purpose of these diagnostics is not only to maximize correlation with yield, but also to evaluate whether each SQI version is interpretable, parsimonious, and agronomically coherent.

## Documentation and reproducibility

The original research dataset is private and is not included in the public repository.

The public repository documents the workflow structure, code, configuration files, and methodological decisions while excluding unpublished data and private outputs.

Methodological documentation is maintained in:

* `docs/decision_log.md`;
* `docs/mds_candidate_sets.md`;
* `docs/scoring_strategy.md`;
* `docs/analysis_plan.md`.

## Next steps

The next analytical steps are:

1. continue refining SQI validation diagnostics;
2. evaluate whether additional scoring functions are justified;
3. prepare publication-oriented figures and tables;
4. improve public reproducibility using anonymized or simulated example data;
5. expand validation using mixed-model approaches;
6. refine the final SQI version based on validation performance, parsimony, and agronomic interpretation.
