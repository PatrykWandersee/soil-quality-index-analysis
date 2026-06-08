# Scoring Strategy

This document describes the current exploratory scoring strategy used to build preliminary soil quality index (SQI) versions.

## Current scoring method

The current SQI workflow uses linear min-max scoring. Each indicator is transformed to a 0–1 score according to its expected direction:

- `more_is_better`: higher observed values receive higher scores;
- `less_is_better`: lower observed values receive higher scores.

This approach is exploratory and data-driven because scores are scaled using the observed minimum and maximum values in the dataset.

## Main candidate set

The current main SQI candidate is `MDS11_main`, which includes 11 indicators representing biological, chemical, physical, salinity, sodicity, and organic matter domains.

## Sensitivity candidate set

The `MDS12_sodicity` set adds `Na_Troc_cmolc_Kg` to the main set as a sodicity-expanded sensitivity analysis.

## Electrical conductivity

Electrical conductivity (`CE_dS_m`) showed behavior that may reflect fertility or ionic concentration under the low salinity range observed in the dataset. However, it is scored conservatively as `less_is_better` because elevated salinity represents a risk in irrigated semiarid systems.

## Future refinement

Future SQI versions may replace simple linear min-max scoring with agronomic scoring functions, including threshold-based, plateau, or optimum-range functions.
