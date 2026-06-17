# SQI scoring strategy

## Purpose

This document summarizes the scoring strategy used to construct Soil Quality Index (SQI) candidates for irrigated Palmer mango orchards in the Brazilian semiarid region.

The current workflow uses transparent linear min–max scoring to compare SQI candidates and evaluate their internal validation against relative yield per plant.

## General scoring approach

Each selected soil indicator is transformed into a unitless score ranging from 0 to 1.

The general scoring rules are:

* `more_is_better`: higher indicator values receive higher scores;
* `less_is_better`: lower indicator values receive higher scores;
* `optimum_range`: values inside a predefined optimum interval receive higher scores, while values below or above the interval receive lower scores.

The main SQI candidates are calculated as the mean of the selected indicator scores.

## Current principal SQI scoring

The current principal SQI candidate is:

`MDS10_without_CE_SQI`

This candidate excludes electrical conductivity (`CE_dS_m`) because CE showed ambiguous interpretation within the observed data range.

The principal candidate uses linear min–max scoring for the following indicators:

| Indicator          | Scoring direction | Interpretation                                                               |
| ------------------ | ----------------- | ---------------------------------------------------------------------------- |
| `MO_g_dm3`         | `more_is_better`  | Soil organic matter is treated as beneficial within the observed range.      |
| `GMea`             | `more_is_better`  | Integrated enzymatic activity is treated as beneficial.                      |
| `Arilsulf`         | `more_is_better`  | Arylsulfatase activity is treated as beneficial.                             |
| `Ca_Troc_cmolc_Kg` | `more_is_better`  | Exchangeable calcium represents base fertility status.                       |
| `K_Troc_cmolc_Kg`  | `more_is_better`  | Exchangeable potassium represents nutrient availability.                     |
| `Floculacao_pct`   | `more_is_better`  | Clay flocculation is treated as beneficial for structural stability.         |
| `Ds_g_cm3`         | `less_is_better`  | Bulk density is treated as a physical restriction indicator.                 |
| `PST`              | `less_is_better`  | Exchangeable sodium percentage is treated as a sodicity-risk indicator.      |
| `PM1_mg_dm3`       | `more_is_better`  | Mehlich-1 phosphorus is treated as beneficial within the observed range.     |
| `pH`               | `more_is_better`  | pH is treated linearly in the principal candidate within the observed range. |

## Main salinity/sodicity sensitivity scoring

The main salinity/sodicity sensitivity candidate is:

`MDS11_sodicity_without_CE_SQI`

This candidate uses the same scoring rules as `MDS10_without_CE_SQI`, with the addition of exchangeable sodium:

| Indicator          | Scoring direction | Interpretation                                                           |
| ------------------ | ----------------- | ------------------------------------------------------------------------ |
| `Na_Troc_cmolc_Kg` | `less_is_better`  | Exchangeable sodium is treated as an additional sodicity-risk indicator. |

This candidate evaluates whether adding exchangeable sodium improves SQI performance without relying on CE.

## pH optimum-range sensitivity

The pH scoring-rule sensitivity candidate is:

`MDS10_pH_optimum_without_CE_SQI`

This candidate uses the same indicator structure as `MDS10_without_CE_SQI`, but replaces the linear pH score with an optimum-range pH score.

The tested optimum range is:

* lower optimum limit: pH 6.5;
* upper optimum limit: pH 7.5.

This candidate is retained as a scoring-rule sensitivity analysis, not as the principal SQI candidate.

## Compact thesis-inspired scoring

The compact comparison candidate is:

`MDS2_thesis_compact_linear_SQI`

It uses two indicators:

| Indicator         | Scoring direction | Interpretation                                                                  |
| ----------------- | ----------------- | ------------------------------------------------------------------------------- |
| `Beta_por_Argila` | `more_is_better`  | Clay-normalized beta-glucosidase is treated as a biological activity indicator. |
| `SB_cmolc_Kg`     | `more_is_better`  | Sum of exchangeable bases is treated as a fertility indicator.                  |

This candidate is retained as a practical compact comparison with the broader integrated SQI candidates.

## Electrical conductivity decision

Electrical conductivity (`CE_dS_m`) was originally included in the previous principal candidate, `MDS11_main_SQI`, and scored as `less_is_better` because CE can represent salinity risk in irrigated semiarid soils.

However, within the observed low-to-moderate CE range, CE was positively associated with relative yield. This pattern probably reflects soluble fertility, fertigation intensity, or general management level rather than harmful salinity.

The data do not support treating increasing CE as universally beneficial. At the same time, scoring CE as `less_is_better` reduced the validation performance of the principal SQI.

A formal sensitivity analysis showed that:

* removing CE improved the principal SQI validation balance;
* scoring CE as `more_is_better` improved validation but is not agronomically transferable beyond the observed range;
* a CE-free sodicity sensitivity candidate performed well when exchangeable sodium was added.

Therefore, CE is not retained in the current principal SQI candidate.

CE-containing candidates remain useful as methodological sensitivity comparisons:

* `MDS11_main_SQI`: previous principal candidate with CE scored as `less_is_better`;
* `MDS12_sodicity_SQI`: previous sodicity-expanded candidate with CE retained;
* `MDS11_pH_optimum_SQI`: previous pH optimum-range candidate with CE retained.

## Current interpretation

The current scoring strategy prioritizes:

* transparent scoring rules;
* agronomic interpretability;
* avoidance of ambiguous indicator direction;
* internal validation performance;
* sensitivity analysis rather than uncritical maximization of model fit.

The revised principal SQI is CE-free because this provides a better balance between data behavior and agronomic transferability.
