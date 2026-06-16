# SQI Candidate Decision Summary

This document summarizes the current methodological decision regarding the preliminary Soil Quality Index (SQI) candidate versions.

It is intended as a synthesis document connecting the analytical scripts, validation outputs, and methodological decision log.

## Current SQI candidate versions

The current workflow retains one principal SQI candidate version and two sensitivity versions:

* `MDS11_main_SQI`: principal preliminary SQI version;
* `MDS12_sodicity_SQI`: sodicity-expanded sensitivity version;
* `MDS11_pH_optimum_SQI`: pH scoring sensitivity version.

## Principal version: `MDS11_main_SQI`

`MDS11_main_SQI` is retained as the principal preliminary SQI version.

This version includes 11 indicators representing organic matter, biological activity, fertility, soil structure, bulk density, sodicity, phosphorus extraction, pH, and electrical conductivity.

The main rationale for retaining `MDS11_main_SQI` is that it provides a strong balance between:

* parsimony;
* interpretability;
* agronomic coherence;
* validation performance;
* robustness after accounting for farm-level structure.

Although it is not always the numerically strongest version in every validation comparison, it remains the most defensible principal SQI version because it avoids adding an extra sodicity indicator with only limited additional contribution.

## Main sensitivity version: `MDS12_sodicity_SQI`

`MDS12_sodicity_SQI` is retained as the main sensitivity version.

This version adds `Na_Troc_cmolc_Kg` to the main candidate set. It was retained because exchangeable sodium contributed to PCA structure and did not exceed the high-redundancy threshold with `PST`.

In simple validation against relative yield per plant, `MDS12_sodicity_SQI` showed the strongest numerical performance among the tested SQI versions.

However, after accounting for farm as a fixed effect, `MDS11_main_SQI` showed better model performance. Therefore, the additional contribution of `Na_Troc_cmolc_Kg` is interpreted as useful for sensitivity analysis, but not sufficient to replace the more parsimonious main SQI version.

## Scoring sensitivity version: `MDS11_pH_optimum_SQI`

`MDS11_pH_optimum_SQI` is retained as a methodological sensitivity analysis.

This version uses the same indicator composition as `MDS11_main_SQI`, but scores pH using an optimum-range function instead of the linear scoring rule used in the main SQI version.

The tested optimum interval was 6.5–7.5.

Preliminary diagnostics did not support replacing the main pH scoring rule. The optimum-range version did not clearly improve validation behavior and remains a sensitivity test rather than a candidate for the principal SQI version.

## Response variable decision

`Prod_rel_pct` is retained as the primary response variable for SQI validation.

This response variable showed clearer relationships with soil indicators and candidate SQI versions than `Prod_rel_ha_pct`.

`Prod_rel_ha_pct` is retained as a secondary response variable, but validation results were weak across all SQI candidate versions. This suggests that yield per hectare may be more strongly affected by planting density, orchard structure, or management factors not directly represented in the current SQI.

## Farm-structured validation

Farm-structured validation was evaluated using:

* simple OLS;
* OLS with farm as a fixed effect;
* mixed linear models with farm as a random intercept.

The simple OLS comparison favored `MDS12_sodicity_SQI` numerically.

The OLS model with farm as a fixed effect favored `MDS11_main_SQI`, supporting the interpretation that the main SQI version remains robust when farm-level differences are considered.

The mixed model with farm as a random intercept converged at the boundary, with farm-level variance estimated as zero. Therefore, the random-intercept mixed model is treated as a diagnostic result rather than as the main validation model.

## Current decision

The current decision is:

* retain `MDS11_main_SQI` as the principal preliminary SQI version;
* retain `MDS12_sodicity_SQI` as the main sensitivity version;
* retain `MDS11_pH_optimum_SQI` as a scoring sensitivity version;
* use `Prod_rel_pct` as the main validation response;
* treat `Prod_rel_ha_pct` as secondary and weakly associated with the current SQI versions;
* treat the random-intercept mixed model as diagnostic because of boundary or singular behavior.

## Implication for the manuscript

For the manuscript, the main results should prioritize `MDS11_main_SQI`.

`MDS12_sodicity_SQI` should be presented as a sensitivity analysis showing that adding exchangeable sodium produces only limited improvement and does not clearly justify replacing the main parsimonious SQI.

`MDS11_pH_optimum_SQI` should be presented as a methodological sensitivity test related to scoring assumptions.

The main validation figure should likely focus on `MDS11_main_SQI` versus `Prod_rel_pct`, supported by a comparison table including all candidate SQI versions.

Additional validation results involving `Prod_rel_ha_pct` and farm-structured models may be presented as supplementary or supporting diagnostics.

## Current SQI candidate decision

The current manuscript-oriented workflow supports `MDS11_main_SQI` as the principal preliminary SQI candidate.

Although `MDS12_sodicity_SQI` showed the strongest simple validation metrics against relative yield per plant, including the highest Spearman correlation and OLS R², its advantage over `MDS11_main_SQI` was small. In contrast, `MDS11_main_SQI` showed the strongest farm fixed-effect model performance and retained high correlation after excluding the Experimental group.

The thesis-inspired compact candidate, `MDS2_thesis_compact_linear_SQI`, was competitive but did not outperform the broader integrated candidates under the current linear scoring workflow. It is therefore retained as a practical compact comparison, not as the principal SQI version.

The pH optimum-range candidate, `MDS11_pH_optimum_SQI`, showed similar simple correlation performance but did not improve the overall validation balance. It is retained as a scoring-rule sensitivity analysis.

Final working decision:

* Principal SQI candidate: `MDS11_main_SQI`
* Main sensitivity candidate: `MDS12_sodicity_SQI`
* Practical compact comparison: `MDS2_thesis_compact_linear_SQI`
* Scoring-rule sensitivity: `MDS11_pH_optimum_SQI`

This decision is based on internal validation using `Prod_rel_pct` as the primary response variable. The area-based response, `Prod_rel_ha_pct`, remains secondary because it is more strongly affected by planting density, orchard structure, and management heterogeneity.
