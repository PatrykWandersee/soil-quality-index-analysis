# Manuscript outline — SQI article

## Working title

**Integrated soil quality index for diagnosing relative productivity in irrigated Palmer mango orchards in the Brazilian semiarid region**

Alternative titles:

1. **A CE-free multidimensional soil quality index for irrigated Palmer mango orchards in the Brazilian semiarid region**
2. **Soil quality indexing integrates biological, chemical, and physical indicators associated with mango productivity under semiarid irrigation**
3. **Minimum-data-set soil quality indexing for irrigated mango orchards in the Lower Middle São Francisco Valley**

## Manuscript focus

This manuscript focuses on the construction, comparison, and internal validation of Soil Quality Index (SQI) candidates for irrigated `Mangifera indica` L. cv. Palmer orchards in the Brazilian semiarid region.

The manuscript is centered on SQI construction and validation. It does not focus on enzymatic critical levels, biological reference ranges, or Cate–Nelson diagnostic thresholds.

## Core research question

Can a minimum-data-set SQI integrate biological, chemical, and physical soil indicators associated with relative yield per plant in irrigated Palmer mango orchards?

## Main hypothesis

A multidimensional SQI integrating biological activity, organic matter, fertility, soil physical condition, sodicity risk, phosphorus availability, and pH will provide a more balanced diagnostic framework than isolated indicators or a highly compact two-indicator index.

## Secondary hypotheses

1. Relative yield per plant is more appropriate than area-based relative yield for validating soil quality indicators in orchards with heterogeneous planting density.
2. A broad integrated SQI will show more stable performance across farms than a compact two-indicator SQI.
3. Sodicity-related indicators may improve simple validation performance, but their inclusion should be evaluated against parsimony and interpretability.
4. Electrical conductivity requires careful treatment because it can represent salinity risk, but may also reflect soluble fertility or fertigation intensity within low-to-moderate observed ranges.
5. Alternative pH scoring rules may affect SQI values, but are not expected to change the main methodological decision.

## Dataset and study context

The study uses soil and productivity data from irrigated Palmer mango orchards in the Lower Middle São Francisco Valley, Brazilian semiarid region.

Sampling structure:

* 48 sampling points;
* nine commercial farms and one experimental area;
* 0–10 cm soil layer;
* physical, chemical, and biological soil indicators;
* relative yield per plant as the primary response variable;
* relative yield per hectare as a secondary response variable.

## Primary response variable

The primary response variable is:

`Prod_rel_pct`

This variable represents relative yield per plant and is preferred because it reduces the confounding effect of planting density and orchard architecture.

## Secondary response variable

The secondary response variable is:

`Prod_rel_ha_pct`

This variable is retained only as a sensitivity/secondary response because it is more strongly affected by plant density, orchard structure, and management heterogeneity.

## Candidate SQI versions

### Principal candidate

`MDS10_without_CE_SQI`

This is the revised principal integrated SQI candidate.

It is derived from the previous 11-indicator structure, but excludes electrical conductivity (`CE_dS_m`) because CE behaved ambiguously within the observed low-to-moderate range.

This candidate integrates:

* organic matter status;
* enzymatic activity;
* fertility;
* soil physical structure;
* sodicity risk through PST;
* phosphorus availability;
* soil reaction.

### Main salinity/sodicity sensitivity candidate

`MDS11_sodicity_without_CE_SQI`

This candidate adds exchangeable sodium to the CE-free principal SQI structure.

It is retained as the main salinity/sodicity sensitivity candidate because it evaluates whether additional sodium-related information improves SQI performance without relying on CE.

### Practical compact comparison

`MDS2_thesis_compact_linear_SQI`

This candidate is inspired by the compact two-indicator SQI used in the thesis. It combines clay-normalized beta-glucosidase and sum of exchangeable bases using the current repository linear min–max scoring convention.

It is retained as a practical compact comparison, not as the principal candidate.

### pH scoring-rule sensitivity

`MDS10_pH_optimum_without_CE_SQI`

This candidate tests an optimum-range scoring function for pH while excluding CE.

It is retained as a scoring-rule sensitivity analysis.

### Previous CE-containing candidates

The following candidates are retained only as methodological sensitivity comparisons:

* `MDS11_main_SQI`: previous principal candidate with CE scored as `less_is_better`;
* `MDS12_sodicity_SQI`: previous sodicity-expanded candidate with CE retained;
* `MDS11_pH_optimum_SQI`: previous pH optimum-range candidate with CE retained.

## Current working decision

The current workflow supports `MDS10_without_CE_SQI` as the principal preliminary SQI candidate.

Although `MDS11_sodicity_without_CE_SQI` showed the strongest simple validation among the CE-free candidates, `MDS10_without_CE_SQI` is preferred as the principal candidate because it provides a better balance between performance, parsimony, interpretability, and multidimensional soil-quality coverage.

CE-containing candidates remain useful as methodological sensitivity comparisons, but are not treated as principal SQI candidates because CE behaved ambiguously in the observed data range.

## Proposed manuscript structure

## 1. Introduction

### 1.1 Problem context

Irrigated mango orchards in the Brazilian semiarid region are highly productive but depend on intensive water, nutrient, and soil management. Under these conditions, soil functioning cannot be adequately interpreted from chemical fertility alone.

### 1.2 Scientific gap

There is limited information on integrated soil quality assessment for perennial fruit systems in the Brazilian semiarid region. Most available soil health approaches emphasize annual crops or different production systems and may not transfer directly to irrigated perennial orchards.

### 1.3 Why an SQI?

A Soil Quality Index can synthesize complementary biological, chemical, and physical indicators into a single diagnostic framework. This is useful when productivity is controlled by multiple interacting soil constraints rather than by one isolated factor.

### 1.4 Why relative yield per plant?

Relative yield per plant is more appropriate than yield per area when planting density and orchard architecture vary substantially among orchards.

### 1.5 Why CE required sensitivity analysis

Electrical conductivity is relevant in irrigated semiarid soils because it can indicate salinity risk. However, within the observed low-to-moderate CE range, higher CE was associated with higher relative yield, probably reflecting soluble fertility, fertigation intensity, or management level rather than harmful salinity.

Therefore, CE was treated through sensitivity analysis rather than retained in the principal SQI.

### 1.6 Objective

To construct, compare, and internally validate minimum-data-set SQI candidates for irrigated Palmer mango orchards in the Brazilian semiarid region.

## 2. Materials and Methods

### 2.1 Study area and sampling design

Describe:

* Lower Middle São Francisco Valley;
* irrigated mango orchards;
* Palmer cultivar;
* commercial farms and experimental area;
* 48 sampling points;
* 0–10 cm layer;
* sampling campaigns from 2023 to 2024.

### 2.2 Soil and productivity variables

Describe physical, chemical, and biological indicators.

Mention that enzymatic indicators were included as part of the SQI workflow, but detailed biological reference ranges are outside the scope of this manuscript.

### 2.3 Response variables

Primary response:

`Prod_rel_pct`

Secondary response:

`Prod_rel_ha_pct`

Justify why `Prod_rel_pct` is the main validation target.

### 2.4 Indicator screening and redundancy analysis

Describe:

* Spearman correlation screening;
* biological, chemical, physical, salinity/sodicity, and texture-related variables;
* redundancy analysis among strongly correlated indicators;
* decision to avoid redundant variants of the same information.

### 2.5 PCA-supported MDS definition

Describe:

* candidate indicator set;
* PCA interpretation as exploratory support;
* selection of indicators representing major soil-quality dimensions;
* final MDS candidate structures defined by multivariate structure, agronomic interpretability, redundancy control, and validation performance.

Avoid presenting PCA as the sole mechanical basis for selecting the final SQI.

### 2.6 Scoring strategy

Describe:

* linear min–max scoring;
* more-is-better indicators;
* less-is-better indicators;
* pH optimum-range sensitivity;
* CE sensitivity analysis;
* SQI calculated from scored indicators.

### 2.7 SQI candidate comparison

Describe the main candidates:

* `MDS10_without_CE_SQI`;
* `MDS11_sodicity_without_CE_SQI`;
* `MDS2_thesis_compact_linear_SQI`;
* `MDS10_pH_optimum_without_CE_SQI`.

Mention CE-containing candidates as methodological sensitivity comparisons.

### 2.8 Validation approach

Describe:

* Spearman correlation;
* Pearson correlation;
* simple OLS regression;
* OLS equation;
* RMSE and MAE;
* farm fixed-effect OLS;
* mixed random-intercept model as diagnostic;
* Experimental group sensitivity.

Important caution: this is internal validation, not independent external validation.

## 3. Results

### 3.1 Soil indicators and productivity response

Present why `Prod_rel_pct` is the main response and why `Prod_rel_ha_pct` behaves differently.

### 3.2 PCA-supported soil-quality gradients and MDS structure

Summarize the soil-quality gradients captured by the exploratory PCA and the resulting MDS candidate structure.

### 3.3 CE sensitivity and revised principal SQI

Show that CE behaved ambiguously within the observed data range.

Key interpretation:

* CE can represent salinity risk in irrigated semiarid soils;
* within the observed range, higher CE was associated with higher yield;
* CE likely reflected soluble fertility, fertigation intensity, or management level;
* removing CE improved the validation balance;
* therefore, the principal SQI was revised to exclude CE.

### 3.4 Main SQI validation

Present the relationship between `MDS10_without_CE_SQI` and `Prod_rel_pct`.

Main metrics:

* Spearman rho = 0.682;
* p < 0.001;
* OLS R² = 0.532;
* RMSE = 14.808.

### 3.5 SQI candidate comparison

Compare:

* `MDS10_without_CE_SQI`;
* `MDS11_sodicity_without_CE_SQI`;
* `MDS2_thesis_compact_linear_SQI`;
* `MDS10_pH_optimum_without_CE_SQI`;
* CE-containing candidates as sensitivity comparisons.

Expected interpretation:

* `MDS11_sodicity_without_CE_SQI` performs best in simple validation among CE-free candidates;
* `MDS10_without_CE_SQI` offers the most balanced principal structure;
* `MDS2_thesis_compact_linear_SQI` is practical but less robust;
* `MDS10_pH_optimum_without_CE_SQI` is useful as a pH scoring sensitivity;
* CE-containing candidates are retained as methodological sensitivity comparisons.

### 3.6 Farm structure and Experimental group sensitivity

Show that the SQI-yield relationship is not artificially driven by the Experimental group.

Mention that mixed random-intercept models were singular/boundary and therefore treated as diagnostic rather than as the main inference.

## 4. Discussion

### 4.1 Integrated soil quality interpretation

Discuss why productive performance in irrigated mango orchards is better interpreted through integrated soil quality than through isolated indicators.

### 4.2 Why the principal SQI excludes CE

Discuss the dual interpretation of CE:

* salinity risk under irrigated semiarid conditions;
* soluble fertility or fertigation proxy within the observed range.

Explain that CE was excluded from the principal SQI because its scoring direction was not agronomically transferable.

### 4.3 Why the principal SQI is broader than the compact SQI

The compact thesis-inspired SQI remains useful as an operational comparison. However, the broader CE-free SQI is more defensible as a scientific SQI because it integrates more soil functions and showed better balance across validation criteria.

### 4.4 Sodicity as a sensitivity dimension

Discuss why sodium-related indicators improved simple validation and may reflect early imbalance in irrigated semiarid systems.

### 4.5 Productivity per plant versus productivity per area

Discuss why `Prod_rel_pct` is the more appropriate response for soil quality validation in orchards with contrasting planting densities.

### 4.6 Limitations

Mention:

* internal validation only;
* limited number of farms;
* 48 observations;
* one cultivar;
* one region;
* one soil layer;
* farm/time structure not fully separable;
* CE range limited to low-to-moderate values;
* need for external validation.

## 5. Conclusion

A CE-free multidimensional minimum-data-set SQI was internally validated for irrigated Palmer mango orchards in the Brazilian semiarid region. The `MDS10_without_CE_SQI` is retained as the principal preliminary SQI candidate because it balances agronomic interpretability, multidimensional soil-quality coverage, and validation performance while avoiding the ambiguous scoring direction of CE. A CE-free sodicity-expanded candidate showed slightly stronger simple validation, while the compact thesis-inspired candidate remained useful as a practical comparison. External validation is required before broader recommendation.

## Main figures and tables

### Main manuscript

Figure 1. Main SQI validation figure: `MDS10_without_CE_SQI` versus relative yield per plant.

Table 1. MDS indicators, scoring direction, and soil function represented.

Table 2. SQI candidate validation table with Spearman rho, OLS equation, R², RMSE, farm fixed-effect R², and Experimental group sensitivity.

### Supplementary material

Supplementary Figure 1. SQI candidate comparison panel.

Supplementary Table 1. CE scoring sensitivity analysis.

Supplementary Table 2. Full validation metrics for both response variables.

Supplementary Table 3. Experimental group influence diagnostics.

Supplementary Table 4. Redundancy/correlation diagnostics among candidate indicators.

## What stays out of this manuscript

The following topics should be treated in a separate manuscript:

* Cate–Nelson critical levels for beta-glucosidase, arylsulfatase, and GMea;
* low, moderate, and adequate biological reference classes;
* recursive partitioning of enzymatic indicators;
* biological diagnostic panels;
* BioAS-oriented comparison and interpretation.
