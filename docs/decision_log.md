# Decision Log

This document records methodological decisions made during the development of the soil quality index workflow.

## 2026-06-08 — Clay-normalized indicators

Clay-normalized indicators were tested for Mehlich-1 P and GMea.

Initial Spearman screening showed that clay normalization did not improve the association with relative yield per plant:

- `PM1_mg_dm3` showed stronger association than `PM1_per_Clay`.
- `GMea` showed slightly stronger association than `GMea_per_Clay`.

Decision: retain `PM1_mg_dm3` and `GMea` as main candidate indicators. Keep clay-normalized versions for sensitivity analysis and later mixed-model comparison.

## 2026-06-08 — Main and sensitivity MDS sets

Two SQI candidate sets were retained:

- `MDS11_main`: main parsimonious candidate set.
- `MDS12_sodicity`: sensitivity set including `Na_Troc_cmolc_Kg`.

`PST` was retained as the primary sodicity indicator because it showed stronger association with relative yield and had high influence in SQI component diagnostics. `Na_Troc_cmolc_Kg` improved SQI validation only marginally and was therefore retained only in the sensitivity set.

## 2026-06-08 — Electrical conductivity scoring

In the original thesis interpretation, `CE_dS_m` behaved partly as a fertility proxy because observed salinity levels were low. However, for SQI scoring, `CE_dS_m` was treated conservatively as a "less is better" indicator because elevated electrical conductivity represents salinity risk in irrigated systems.

Decision: use the conservative CE scoring direction in the main preliminary SQI. Retain data-driven scoring only as sensitivity analysis.
