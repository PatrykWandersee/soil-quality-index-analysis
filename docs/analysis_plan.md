# Analysis Plan

This document outlines the current analytical workflow for evaluating soil quality indicators in irrigated mango orchards.

## Current objective

The current objective is to reorganize the original soil quality dataset into a reproducible Python workflow and test whether selected clay-normalized indicators improve the interpretation of soil quality and crop productivity relationships.

## Response variables

The main response variables considered in the exploratory screening are:

- `Prod_rel_pct`: relative yield per plant
- `Prod_rel_ha_pct`: relative yield per hectare

At this stage, `Prod_rel_pct` is treated as the primary response variable because it is more directly aligned with the original soil quality index validation approach.

## Candidate derived indicators

The current workflow evaluates the following derived indicators:

- `PM1_per_Clay`: Mehlich-1 phosphorus divided by clay content
- `GMea_per_Clay`: geometric mean of enzyme activity divided by clay content
- `log_PM1_per_Clay`: log-transformed clay-normalized Mehlich-1 phosphorus
- `log_GMea_per_Clay`: log-transformed clay-normalized GMea

These indicators are recalculated in Python from the original measured variables to avoid spreadsheet rounding issues.

## Screening strategy

The initial screening uses Spearman correlation to compare candidate indicators against the response variables. This step is exploratory and is not intended to define the final minimum dataset by itself.

The main goals of the screening are:

- compare original and clay-normalized indicators;
- identify redundant variables within the same conceptual family;
- evaluate whether clay normalization improves the relationship with crop productivity;
- guide the selection of variables for later PCA, MDS construction, and SQI validation.

## Variable family principle

Because the dataset contains many derived variables, the final analysis should avoid treating all columns as independent indicators.

For each conceptual family, only one or a small number of representative indicators should be retained for later stages. For example:

- phosphorus availability: `PM1_mg_dm3`, `PM1_per_Clay`, or `log_PM1_per_Clay`;
- integrated enzyme activity: `GMea`, `GMea_per_Clay`, or `log_GMea_per_Clay`;
- beta-glucosidase activity: `Beta_glic`, `Beta_por_Argila`, or `qBeta`;
- arylsulfatase activity: `Arilsulf`, `Aril_por_Argila`, or `qAril`.

## Next steps

The next analytical steps are:

1. generate family-level comparison tables;
2. create exploratory figures comparing original and clay-normalized indicators;
3. evaluate redundancy among candidate indicators;
4. define candidate sets for PCA and minimum data set selection;
5. validate selected soil quality indicators against crop productivity.
