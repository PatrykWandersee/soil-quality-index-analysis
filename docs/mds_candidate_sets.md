# Candidate MDS Sets

This document records the current candidate minimum data set (MDS) configurations derived from PCA, redundancy analysis, and exploratory correlations with relative yield.

## Rationale

The candidate indicators were selected from a reduced set of soil biological, chemical, physical, salinity, and sodicity variables. The selection considered:

- PCA contribution across retained components;
- Spearman correlation with relative yield per plant;
- redundancy among candidate indicators;
- interpretability for irrigated mango orchards in semiarid conditions.

The preliminary upper limit for the MDS is 12 indicators, corresponding to approximately one quarter of the sample size (`n = 48`).

## MDS-12 exploratory set

This set retains both exchangeable sodium and exchangeable sodium percentage because they did not exceed the high-redundancy threshold in the Spearman redundancy analysis.

- `MO_g_dm3`
- `GMea`
- `Arilsulf`
- `Ca_Troc_cmolc_Kg`
- `K_Troc_cmolc_Kg`
- `Floculacao_pct`
- `Ds_g_cm3`
- `PST`
- `Na_Troc_cmolc_Kg`
- `PM1_mg_dm3`
- `pH`
- `CE_dS_m`

## MDS-11 main candidate set

This set prioritizes `PST` as the main sodicity indicator and removes `Na_Troc_cmolc_Kg`, which showed weaker direct association with relative yield.

- `MO_g_dm3`
- `GMea`
- `Arilsulf`
- `Ca_Troc_cmolc_Kg`
- `K_Troc_cmolc_Kg`
- `Floculacao_pct`
- `Ds_g_cm3`
- `PST`
- `PM1_mg_dm3`
- `pH`
- `CE_dS_m`

## MDS-12 texture alternative

This set replaces `Na_Troc_cmolc_Kg` with a texture indicator, allowing comparison between a sodicity-expanded MDS and a texture-expanded MDS.

Candidate replacement options:

- `Argila_g_kg`
- `Areia_g_kg`

The final choice should be based on SQI validation performance, interpretability, and redundancy with the remaining indicators.

## Current interpretation

At this stage, `PST` is treated as the primary sodicity indicator. `Na_Troc_cmolc_Kg` remains useful for sensitivity analysis because it contributed strongly to PC3, but it is not prioritized for the main MDS due to its weaker direct correlation with relative yield.
