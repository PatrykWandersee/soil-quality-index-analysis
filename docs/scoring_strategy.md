# Scoring Strategy

This document describes the exploratory scoring strategy used to build preliminary soil quality index (SQI) versions.

## Current scoring configuration

SQI scoring rules are defined in `config/scoring_rules_mds.csv` and applied through the shared utility functions in `scripts/sqi_utils.py`.

Each indicator is transformed to a 0–1 score according to its scoring direction and scoring method. The current workflow supports the following scoring directions:

- `more_is_better`: higher observed values receive higher scores;
- `less_is_better`: lower observed values receive higher scores.

The current workflow supports the following scoring methods:

- `linear`: linear min-max scoring based on the observed minimum and maximum values;
- `optimum_range`: sensitivity scoring where values inside a defined optimum interval receive the maximum score and values below or above the interval receive lower scores.

The main SQI versions still rely on linear min-max scoring. The `optimum_range` method is currently used only for sensitivity analysis.

## Main candidate set

The main SQI candidate set is `MDS11_main`.

It includes 11 indicators representing biological, chemical, physical, salinity, sodicity, and organic matter domains. This set is treated as the principal preliminary SQI version because it is parsimonious, interpretable, and maintains a strong association with relative yield.

## Sensitivity candidate sets

Two sensitivity candidate sets are currently retained:

- `MDS12_sodicity`: adds `Na_Troc_cmolc_Kg` to the main set as a sodicity-expanded sensitivity analysis;
- `MDS11_pH_optimum`: keeps the same indicators as `MDS11_main`, but scores pH using an optimum-range function.

The `MDS12_sodicity` version is useful for evaluating whether exchangeable sodium adds information beyond `PST`. Preliminary diagnostics indicate that `Na_Troc_cmolc_Kg` improves SQI validation only marginally.

The `MDS11_pH_optimum` version is useful for evaluating whether pH should be scored as an optimum-range indicator instead of a linear indicator. Preliminary diagnostics did not support replacing the main pH scoring rule with the optimum-range version.

## Electrical conductivity

Electrical conductivity (`CE_dS_m`) showed behavior that may partly reflect fertility or ionic concentration under the low salinity range observed in the dataset. However, for SQI scoring, it is treated conservatively as a `less_is_better` indicator because elevated salinity represents a risk in irrigated semiarid systems.

Alternative data-driven scoring for electrical conductivity may be retained only as sensitivity analysis.

## pH scoring

The main SQI version uses linear scoring for pH. This choice is transparent and reflects the empirical behavior observed in the current dataset.

An additional sensitivity version, `MDS11_pH_optimum`, tests pH scoring with an optimum range of 6.5–7.5. In this version, pH values within the optimum interval receive the maximum score, while values below or above this range receive lower scores.

This optimum-range approach is documented as a methodological test, not as the principal scoring rule.

## Future refinement

Future SQI versions may replace simple linear min-max scoring with agronomic scoring functions based on external thresholds, response curves, plateau functions, or independently validated optimum ranges.

Such refinements should be introduced only when they are supported by agronomic evidence, independent validation, or clear improvement in model behavior.
