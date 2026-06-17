# SQI candidate decision summary

## Purpose

This document summarizes the current manuscript-oriented decision regarding Soil Quality Index (SQI) candidate selection, validation, and interpretation.

The workflow compares integrated, compact, scoring-rule sensitivity, sodicity-oriented, and electrical-conductivity sensitivity SQI candidates for irrigated Palmer mango orchards in the Brazilian semiarid region.

## Current principal decision

The current principal SQI candidate is:

`MDS10_without_CE_SQI`

This candidate is derived from the previous `MDS11_main_SQI`, but excludes electrical conductivity (`CE_dS_m`).

The revised principal candidate is preferred because electrical conductivity behaved ambiguously in the observed data range. Although CE is agronomically relevant in irrigated semiarid soils because it can represent salinity risk, higher CE values in this data set were associated with higher relative yield. This probably reflects soluble fertility, fertigation intensity, or general management level rather than harmful salinity, because the observed CE range was low to moderate.

Removing CE improved the validation balance compared with the previous CE-containing principal candidate.

## Revised candidate roles

### Principal SQI candidate

`MDS10_without_CE_SQI`

This is the revised principal SQI candidate. It retains the multidimensional structure of the main integrated SQI while excluding CE because of its ambiguous interpretation within the observed range.

Main interpretation:

* strongest overall balance across simple validation, farm fixed-effect validation, and Experimental group sensitivity;
* avoids assigning an uncertain scoring direction to CE;
* preserves biological, organic matter, fertility, physical-structure, sodicity, phosphorus, and pH dimensions.

### Main salinity/sodicity sensitivity candidate

`MDS11_sodicity_without_CE_SQI`

This candidate adds exchangeable sodium to the CE-free principal structure.

Main interpretation:

* strongest simple validation among the CE-free manuscript candidates;
* useful as the main salinity/sodicity sensitivity candidate;
* retains sodicity information through PST and exchangeable sodium, without relying on CE;
* should be interpreted as a sensitivity candidate rather than as the principal SQI because it adds an extra sodium-related indicator.

### Practical compact comparison

`MDS2_thesis_compact_linear_SQI`

This candidate is inspired by the compact thesis-oriented SQI structure, using clay-normalized beta-glucosidase and sum of exchangeable bases under the current linear min–max scoring convention.

Main interpretation:

* useful as a practical compact comparison;
* competitive in simple validation;
* less robust than the integrated CE-free candidates under farm-structured validation and Experimental group sensitivity;
* should not be treated as the principal SQI candidate in the current manuscript.

### pH scoring-rule sensitivity

`MDS10_pH_optimum_without_CE_SQI`

This candidate tests an optimum-range pH scoring rule while also excluding CE.

Main interpretation:

* useful as a scoring-rule sensitivity candidate;
* shows strong simple validation;
* does not replace `MDS10_without_CE_SQI` because the main methodological decision should remain more parsimonious and easier to interpret unless the pH scoring rule is explicitly emphasized.

### Previous CE-containing candidates

The previous candidates remain useful as methodological sensitivity comparisons:

* `MDS11_main_SQI`: previous principal candidate with CE scored as `less_is_better`;
* `MDS12_sodicity_SQI`: previous sodicity-expanded candidate with CE retained;
* `MDS11_pH_optimum_SQI`: previous pH optimum-range sensitivity with CE retained.

These are no longer treated as the preferred principal candidates.

## Key validation results

All values below use `Prod_rel_pct` as the primary response variable.

| SQI candidate                     | Role                                      | Spearman rho | OLS R² | RMSE   | Farm fixed R² | Spearman rho without Experimental |
| --------------------------------- | ----------------------------------------- | ------------ | ------ | ------ | ------------- | --------------------------------- |
| `MDS10_without_CE_SQI`            | Principal revised SQI                     | 0.682        | 0.532  | 14.808 | 0.729         | 0.671                             |
| `MDS11_sodicity_without_CE_SQI`   | Main salinity/sodicity sensitivity        | 0.692        | 0.550  | 14.520 | 0.725         | 0.674                             |
| `MDS2_thesis_compact_linear_SQI`  | Practical compact comparison              | 0.659        | 0.486  | 15.512 | 0.653         | 0.600                             |
| `MDS10_pH_optimum_without_CE_SQI` | pH scoring-rule sensitivity               | 0.691        | 0.526  | 14.905 | 0.714         | 0.653                             |
| `MDS11_main_SQI`                  | Previous CE-containing main candidate     | 0.665        | 0.518  | 15.030 | 0.722         | 0.653                             |
| `MDS12_sodicity_SQI`              | Previous CE-containing sodicity candidate | 0.680        | 0.533  | 14.788 | 0.716         | 0.669                             |
| `MDS11_pH_optimum_SQI`            | Previous CE-containing pH sensitivity     | 0.679        | 0.507  | 15.205 | 0.703         | 0.643                             |

## Electrical conductivity decision

Electrical conductivity (`CE_dS_m`) was initially retained because salinity risk is relevant in irrigated semiarid soils. It was scored as `less_is_better` in the first principal SQI candidate.

However, within the observed low-to-moderate CE range, CE showed positive association with relative yield. This does not imply that increasing CE is universally beneficial. It likely reflects soluble fertility, fertigation intensity, or general management level in the sampled orchards.

A formal sensitivity analysis showed that:

* removing CE improved the principal SQI validation balance;
* scoring CE as `more_is_better` also improved validation, but this empirical direction is not agronomically transferable beyond the observed range;
* a CE-free sodicity sensitivity candidate performed well when exchangeable sodium was added.

Therefore, CE is treated as an ambiguous indicator in this data set and is not retained in the revised principal SQI candidate.

## Current manuscript-oriented decision

The current manuscript-oriented decision is:

* Principal SQI candidate: `MDS10_without_CE_SQI`;
* Main salinity/sodicity sensitivity candidate: `MDS11_sodicity_without_CE_SQI`;
* Practical compact comparison: `MDS2_thesis_compact_linear_SQI`;
* pH scoring-rule sensitivity: `MDS10_pH_optimum_without_CE_SQI`;
* CE-containing versions: retained as methodological sensitivity comparisons, not as principal candidates.

## Interpretation for the manuscript

The manuscript should present the CE-free integrated SQI as the principal candidate.

The recommended framing is:

`MDS10_without_CE_SQI` was retained as the principal SQI candidate because it provided the best overall balance between agronomic interpretability, multidimensional soil-quality coverage, internal validation performance, farm-structured validation, and robustness after excluding the Experimental group.

`MDS11_sodicity_without_CE_SQI` should be presented as the main salinity/sodicity sensitivity candidate because it slightly improved simple validation metrics while retaining sodium-related information without relying on the ambiguous CE response.

The compact two-indicator candidate should be retained as a practical comparison, not as the main scientific SQI.

## Statistical caution

All validation is internal to the current data set. The same study system was used for SQI construction, candidate comparison, and validation.

The manuscript should avoid claiming independent external validation.

Preferred terms:

* internal validation;
* preliminary validation;
* apparent validation;
* manuscript-oriented validation.

Avoid:

* externally validated;
* universal threshold;
* definitive recommendation;
* independent predictive validation.
