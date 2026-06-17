# MDS candidate sets

## Purpose

This document summarizes the Minimum Data Set (MDS) candidate structures used to build and compare Soil Quality Index (SQI) versions for irrigated Palmer mango orchards in the Brazilian semiarid region.

The MDS workflow was not based on PCA alone. Candidate sets were defined using a combination of:

* indicator screening against relative yield per plant;
* redundancy control among highly correlated indicators;
* PCA-supported interpretation of multivariate soil-quality gradients;
* agronomic interpretability;
* representation of complementary soil functions;
* internal validation performance;
* sensitivity to farm structure and Experimental group influence.

## Current principal MDS

## MDS10 without CE

Candidate name:

`MDS10_without_CE_SQI`

This is the current principal MDS/SQI candidate for manuscript-oriented interpretation.

It is derived from the previous integrated `MDS11_main_SQI`, but excludes electrical conductivity (`CE_dS_m`) because CE behaved ambiguously in the observed data range.

### Indicators

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

### Soil-quality dimensions represented

* organic matter status;
* integrated enzymatic activity;
* sulfur-related enzymatic activity;
* base fertility;
* potassium availability;
* soil physical structure;
* bulk density restriction;
* sodicity risk through PST;
* phosphorus availability;
* soil reaction.

### Interpretation

`MDS10_without_CE_SQI` is retained as the current principal SQI candidate because it provides the best balance between agronomic interpretability, multidimensional soil-quality coverage, simple validation, farm fixed-effect validation, and robustness after excluding the Experimental group.

Removing CE improved the validation balance compared with the previous CE-containing principal candidate.

## Main salinity/sodicity sensitivity MDS

## MDS11 sodicity without CE

Candidate name:

`MDS11_sodicity_without_CE_SQI`

This candidate adds exchangeable sodium to the CE-free principal MDS.

### Indicators

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
* `Na_Troc_cmolc_Kg`

### Interpretation

This candidate is retained as the main salinity/sodicity sensitivity version.

It keeps sodicity information through both PST and exchangeable sodium, but avoids the ambiguity introduced by CE. It showed strong simple validation performance and is useful for evaluating whether additional sodium-related information improves the SQI.

It is not treated as the principal SQI because it adds an extra sodium-related indicator and therefore reduces parsimony relative to `MDS10_without_CE_SQI`.

## Practical compact comparison

## MDS2 thesis compact linear

Candidate name:

`MDS2_thesis_compact_linear_SQI`

This candidate is inspired by the compact SQI structure explored in the thesis.

### Indicators

* `Beta_por_Argila`
* `SB_cmolc_Kg`

### Interpretation

This candidate is retained as a practical compact comparison.

It is useful for comparing the broader integrated SQI against a simpler operational index. However, it showed weaker farm-structured validation and greater sensitivity to Experimental group exclusion than the integrated CE-free candidates.

It is not treated as the principal SQI version in the current manuscript-oriented workflow.

## pH scoring-rule sensitivity

## MDS10 pH optimum without CE

Candidate name:

`MDS10_pH_optimum_without_CE_SQI`

This candidate uses the same CE-free indicator structure as the principal MDS, but applies an optimum-range scoring function for pH.

### Indicators

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

### Interpretation

This candidate is retained as a scoring-rule sensitivity analysis.

It evaluates whether an optimum-range pH scoring approach changes SQI validation performance. Although it performed well in simple validation, it is treated as a sensitivity candidate rather than the principal SQI because the main decision should remain parsimonious and easy to interpret unless pH scoring is explicitly emphasized.

## Previous CE-containing candidates

The following candidates remain useful as methodological sensitivity comparisons, but are no longer treated as the preferred principal SQI candidates.

## MDS11 main with CE

Candidate name:

`MDS11_main_SQI`

### Indicators

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

### Interpretation

This was the previous principal integrated SQI candidate.

CE was originally retained because salinity risk is relevant in irrigated semiarid soils and was scored as `less_is_better`. However, within the observed low-to-moderate CE range, CE showed positive association with relative yield, probably reflecting soluble fertility, fertigation intensity, or management level rather than harmful salinity.

Sensitivity analysis showed that removing CE improved the validation balance. Therefore, this candidate is now retained only as a CE-containing sensitivity comparison.

## MDS12 sodicity with CE

Candidate name:

`MDS12_sodicity_SQI`

### Indicators

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
* `Na_Troc_cmolc_Kg`

### Interpretation

This was the previous sodicity-expanded candidate.

It remains useful as a methodological sensitivity comparison because it includes PST, CE, and exchangeable sodium. However, because CE behaved ambiguously in the current data set, the CE-free sodicity candidate is preferred as the main salinity/sodicity sensitivity version.

## MDS11 pH optimum with CE

Candidate name:

`MDS11_pH_optimum_SQI`

### Indicators

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

### Interpretation

This was the previous pH optimum-range scoring sensitivity candidate with CE retained. It is now retained only as a historical/scoring sensitivity comparison.

## Electrical conductivity decision

`CE_dS_m` was evaluated carefully because it has dual interpretation in irrigated semiarid systems.

On one hand, CE can indicate salinity risk and potential osmotic stress. On the other hand, within the observed low-to-moderate CE range of this data set, higher CE was associated with higher relative yield, likely reflecting soluble fertility or fertigation intensity.

Because the data do not support treating increasing CE as universally beneficial, and because scoring CE as `less_is_better` reduced validation performance, CE was excluded from the revised principal MDS.

The current interpretation is:

* CE is agronomically relevant;
* CE is ambiguous in the observed data range;
* CE should not be retained in the principal SQI candidate;
* CE-containing versions should be treated as methodological sensitivity comparisons.

## Current manuscript-oriented decision

The current MDS/SQI decision is:

* Principal candidate: `MDS10_without_CE_SQI`;
* Main salinity/sodicity sensitivity candidate: `MDS11_sodicity_without_CE_SQI`;
* Practical compact comparison: `MDS2_thesis_compact_linear_SQI`;
* pH scoring-rule sensitivity: `MDS10_pH_optimum_without_CE_SQI`;
* CE-containing candidates: retained only as methodological sensitivity comparisons.
