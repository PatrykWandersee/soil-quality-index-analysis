# Manuscript outline — SQI article

## Working title

**Integrated soil quality index for diagnosing relative productivity in irrigated Palmer mango orchards in the Brazilian semiarid region**

Alternative titles:

1. **A multidimensional soil quality index for irrigated Palmer mango orchards in the Brazilian semiarid region**
2. **Soil quality indexing integrates biological, chemical, and physical indicators associated with mango productivity under semiarid irrigation**
3. **Minimum-data-set soil quality indexing for irrigated mango orchards in the Lower Middle São Francisco Valley**

## Manuscript focus

This manuscript focuses on the construction, comparison, and internal validation of soil quality index candidates for irrigated `Mangifera indica` L. cv. Palmer orchards in the Brazilian semiarid region.

Critical levels and biological reference ranges for enzymatic indicators will be treated in a separate manuscript.

## Core research question

Can a minimum-data-set soil quality index integrate biological, chemical, and physical soil indicators associated with relative yield per plant in irrigated Palmer mango orchards?

## Main hypothesis

A multidimensional SQI integrating biological activity, organic matter, fertility, soil physical condition, salinity/sodicity risk, and pH will provide a more balanced diagnostic framework than isolated indicators or a highly compact two-indicator index.

## Secondary hypotheses

1. Relative yield per plant is more appropriate than area-based relative yield for validating soil quality indicators in orchards with heterogeneous planting density.
2. A broad integrated SQI will show more stable performance across farms than a compact two-indicator SQI.
3. Sodicity-related indicators may improve simple validation performance, but their inclusion should be evaluated against parsimony and interpretability.
4. Alternative pH scoring rules may affect SQI values, but are not expected to change the main methodological decision.

## Dataset and study context

The study uses soil and productivity data from irrigated Palmer mango orchards in the Lower Middle São Francisco Valley, Brazilian semiarid region.

Sampling structure:

* 48 sampling points;
* nine commercial farms and one experimental area;
* 0–10 cm soil layer;
* physical, chemical, and biological soil indicators;
* relative yield per plant as the primary response variable;
* relative yield per hectare as a secondary response variable.

## Main response variable

The primary response variable is:

`Prod_rel_pct`

This variable represents relative yield per plant and is preferred because it reduces the confounding effect of planting density and orchard architecture.

The secondary response variable is:

`Prod_rel_ha_pct`

This variable is retained only as a sensitivity/secondary response because it is more strongly affected by plant density, orchard structure, and management heterogeneity.

## Candidate SQI versions

### Principal candidate

`MDS11_main_SQI`

This is the principal integrated SQI candidate. It includes 11 indicators representing organic matter, enzymatic activity, fertility, soil physical structure, sodicity, phosphorus, pH, and electrical conductivity.

### Main sensitivity candidate

`MDS12_sodicity_SQI`

This candidate adds exchangeable sodium to the principal MDS structure. It is retained as the main sensitivity version because it showed the strongest simple validation metrics, although its advantage over `MDS11_main_SQI` was small.

### Practical compact comparison

`MDS2_thesis_compact_linear_SQI`

This candidate is inspired by the compact two-indicator SQI used in the thesis. It combines clay-normalized beta-glucosidase and sum of exchangeable bases, using the current repository linear min-max scoring convention.

It is retained as a practical compact comparison, not as the principal candidate.

### Scoring-rule sensitivity

`MDS11_pH_optimum_SQI`

This candidate tests an optimum-range scoring function for pH. It is retained as a scoring-rule sensitivity analysis.

## Current working decision

The current workflow supports `MDS11_main_SQI` as the principal preliminary SQI candidate.

Although `MDS12_sodicity_SQI` showed the strongest simple validation metrics, `MDS11_main_SQI` showed the best balance across agronomic interpretability, multidimensional coverage, farm fixed-effect validation, and robustness after excluding the Experimental group.

The compact thesis-inspired candidate remained competitive, but did not outperform the broader integrated candidates under the current scoring workflow.

## Proposed manuscript structure

## 1. Introduction

### 1.1 Problem context

Irrigated mango orchards in the Brazilian semiarid region are highly productive but depend on intensive water, nutrient, and soil management. Under these conditions, soil functioning cannot be adequately interpreted from chemical fertility alone.

### 1.2 Scientific gap

There is limited information on integrated soil quality assessment for perennial fruit systems in the Brazilian semiarid region. Most available soil health approaches emphasize annual crops, especially in the Cerrado, and may not transfer directly to irrigated perennial orchards.

### 1.3 Why an SQI?

A soil quality index can synthesize complementary biological, chemical, and physical indicators into a single diagnostic framework. This is useful when productivity is controlled by multiple interacting soil constraints rather than by one isolated factor.

### 1.4 Why relative yield per plant?

Relative yield per plant is more appropriate than yield per area when planting density varies substantially among orchards.

### 1.5 Objective

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

Mention that enzymatic indicators were included, but detailed biological reference ranges will be addressed in a separate manuscript.

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

### 2.5 PCA and MDS construction

Describe:

* candidate indicator set;
* PCA interpretation;
* selection of indicators representing major soil quality dimensions;
* construction of MDS candidate sets.

### 2.6 Scoring strategy

Describe:

* linear min-max scoring;
* more-is-better indicators;
* less-is-better indicators;
* pH optimum-range sensitivity;
* CE treated conservatively;
* SQI calculated from scored indicators.

### 2.7 SQI candidate comparison

Describe the four SQI candidates:

* `MDS11_main_SQI`;
* `MDS12_sodicity_SQI`;
* `MDS2_thesis_compact_linear_SQI`;
* `MDS11_pH_optimum_SQI`.

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

### 3.2 PCA and MDS structure

Summarize the soil quality gradients captured by the PCA and the resulting MDS candidate structure.

### 3.3 Main SQI validation

Present the main relationship between `MDS11_main_SQI` and `Prod_rel_pct`.

Main equation:

`Relative yield per plant (%) = 6.04 + 110.18 × SQI`

Main metrics:

* Spearman rho = 0.665;
* p < 0.001;
* OLS R² = 0.518.

### 3.4 SQI candidate comparison

Compare:

* `MDS11_main_SQI`;
* `MDS12_sodicity_SQI`;
* `MDS2_thesis_compact_linear_SQI`;
* `MDS11_pH_optimum_SQI`.

Expected interpretation:

* `MDS12_sodicity_SQI` performs best in simple validation;
* `MDS11_main_SQI` performs best in farm fixed-effect validation;
* `MDS2_thesis_compact_linear_SQI` is practical but less robust;
* `MDS11_pH_optimum_SQI` does not improve the overall decision.

### 3.5 Farm structure and Experimental group sensitivity

Show that the SQI-yield relationship is not artificially driven by the Experimental group.

Mention that mixed random-intercept models were singular/boundary and therefore treated as diagnostic rather than as the main inference.

## 4. Discussion

### 4.1 Integrated soil quality interpretation

Discuss why productive performance in irrigated mango orchards is better interpreted through integrated soil quality than through isolated indicators.

### 4.2 Why the principal SQI is broader than the thesis compact SQI

The compact thesis-inspired SQI remains useful as an operational comparison. However, the broader `MDS11_main_SQI` is more defensible as a scientific SQI because it integrates more soil functions and showed better balance across validation criteria.

### 4.3 Sodicity as a sensitivity dimension

Discuss why sodicity-related indicators improved simple validation and may reflect early imbalance in irrigated semiarid systems, even when absolute values are low.

### 4.4 Productivity per plant versus productivity per area

Discuss why `Prod_rel_pct` is the more appropriate response for soil quality validation in orchards with contrasting planting densities.

### 4.5 Limitations

Mention:

* internal validation only;
* limited number of farms;
* 48 observations;
* one cultivar;
* one region;
* one soil layer;
* farm/time structure not fully separable;
* need for external validation.

## 5. Conclusion

A multidimensional minimum-data-set SQI was internally validated for irrigated Palmer mango orchards in the Brazilian semiarid region. The `MDS11_main_SQI` is retained as the principal preliminary SQI candidate because it balances agronomic interpretability, multidimensional soil quality coverage, and validation performance. A sodicity-expanded candidate showed slightly stronger simple validation, while the compact thesis-inspired candidate remained useful as a practical comparison. External validation is required before broader recommendation.

## Main figures and tables

### Main manuscript

Figure 1. Main SQI validation figure: `MDS11_main_SQI` versus relative yield per plant.

Table 1. MDS indicators, scoring direction, and soil function represented.

Table 2. SQI candidate validation table with Spearman rho, OLS equation, R², RMSE, farm fixed-effect R², and Experimental group sensitivity.

### Supplementary material

Supplementary Figure 1. SQI candidate comparison panel.

Supplementary Table 1. Full validation metrics for both response variables.

Supplementary Table 2. Experimental group influence diagnostics.

Supplementary Table 3. Redundancy/correlation diagnostics among candidate indicators.

## What stays out of this manuscript

The following topics should be treated in a separate manuscript:

* Cate–Nelson critical levels for beta-glucosidase, arylsulfatase, and GMea;
* low, moderate, and adequate biological reference classes;
* recursive partitioning of enzymatic indicators;
* biological diagnostic panels;
* BioAS-oriented comparison and interpretation.

## Working title for second manuscript

**Critical levels and interpretive classes for soil enzymatic indicators in irrigated Palmer mango orchards of the Brazilian semiarid region**
