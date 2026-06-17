# Soil Quality Index Analysis

This repository documents a reproducible analytical workflow for developing and evaluating preliminary Soil Quality Index (SQI) versions for irrigated mango orchards in the Brazilian semiarid region.

The project is based on a doctoral research workflow involving soil biological, chemical, physical, salinity, sodicity, and organic matter indicators. The current repository is under active development and is intended as a technical-scientific portfolio of the SQI analysis pipeline.

## Repository status

This project currently contains:

* a structured analytical workflow organized as numbered Python scripts;
* private data processing steps kept outside version control;
* indicator screening and redundancy analysis;
* PCA-based support for minimum data set (MDS) selection;
* preliminary SQI construction;
* configurable scoring rules for different candidate SQI versions;
* documentation of methodological decisions.

The workflow is exploratory and manuscript-oriented. Results, scoring choices, and candidate SQI versions may be refined as the analysis progresses.

## Data privacy

The original research dataset is private and is not included in this repository.

Private raw and processed files are stored locally and excluded from Git tracking. This allows the analytical workflow, documentation, and code structure to be versioned publicly without exposing unpublished research data.

The following private paths are intentionally ignored by Git:

* `data/raw/private/`
* `data/processed/private/`
* `figures/private/`
* `tables/private/`

Public example or anonymized datasets may be added later.

## Current analytical workflow

The workflow is organized as numbered scripts in `scripts/`:

* `00_check_data_import.py`: checks private raw data import;
* `01_check_derived_indicators.py`: checks derived indicator calculations;
* `02_prepare_processed_dataset.py`: prepares the processed dataset;
* `03_screen_candidate_indicators.py`: screens candidate indicators against yield variables;
* `04_compare_indicator_families.py`: compares raw and derived indicator families;
* `05_create_exploratory_figures.py`: creates exploratory figures;
* `06_analyze_indicator_redundancy.py`: evaluates redundancy among candidate indicators;
* `07_run_candidate_pca.py`: runs PCA for candidate indicator interpretation;
* `08_define_preliminary_mds.py`: defines preliminary MDS candidate sets;
* `09_build_preliminary_sqi.py`: builds preliminary SQI versions;
* `10_compare_sqi_candidate_sets.py`: compares candidate SQI versions;
* `11_export_selected_sqi_versions.py`: exports selected SQI versions;
* `12_diagnose_sqi_components.py`: evaluates SQI component behavior;
* `13_summarize_scoring_ranges.py`: summarizes scoring ranges and indicator behavior;
* `14_validate_sqi_models.py`: validates selected SQI versions against yield response variables;
* `15_validate_sqi_mixed_models.py`: compares simple OLS, farm fixed-effect OLS, and farm random-intercept mixed models for selected SQI versions;
* `16_diagnose_experimental_group_influence.py`: evaluates whether the Experimental group drives SQI-yield validation results;
* `17_create_manuscript_validation_table.py`: consolidates validation outputs into a manuscript-oriented SQI candidate comparison table;
* `18_create_manuscript_validation_figure.py`: creates a manuscript-oriented validation figure for the main SQI version;
* `19_build_thesis_compact_sqi.py`: builds and validates a compact thesis-inspired SQI candidate using clay-normalized beta-glucosidase and sum of exchangeable bases;
* `20_create_sqi_candidate_comparison_figures.py`: creates manuscript-oriented comparison figures for SQI candidates across validation metrics;
* `21_check_ce_scoring_sensitivity.py`: evaluates electrical conductivity retention and scoring-direction sensitivity in SQI candidates;
* `sqi_utils.py`: contains shared utility functions for scoring and SQI construction.

## Candidate SQI versions

The current workflow compares a revised principal SQI candidate, a salinity/sodicity sensitivity candidate, a compact thesis-inspired comparison, a pH scoring-rule sensitivity candidate, and previous CE-containing sensitivity versions.

The current principal candidate is:

* `MDS10_without_CE_SQI`: revised principal integrated SQI candidate, derived from the previous 11-indicator structure but excluding electrical conductivity (`CE_dS_m`) because CE behaved ambiguously within the observed low-to-moderate range.

The main sensitivity and comparison candidates are:

* `MDS11_sodicity_without_CE_SQI`: main salinity/sodicity sensitivity candidate, adding exchangeable sodium to the CE-free principal structure;
* `MDS2_thesis_compact_linear_SQI`: compact thesis-inspired comparison based on clay-normalized beta-glucosidase and sum of exchangeable bases;
* `MDS10_pH_optimum_without_CE_SQI`: pH scoring-rule sensitivity candidate using an optimum-range pH score without CE.

Previous CE-containing candidates are retained only as methodological sensitivity comparisons:

* `MDS11_main_SQI`: previous principal candidate with CE scored as `less_is_better`;
* `MDS12_sodicity_SQI`: previous sodicity-expanded candidate with CE retained;
* `MDS11_pH_optimum_SQI`: previous pH optimum-range candidate with CE retained.

The current manuscript-oriented decision retains `MDS10_without_CE_SQI` as the principal preliminary SQI candidate, `MDS11_sodicity_without_CE_SQI` as the main salinity/sodicity sensitivity candidate, `MDS2_thesis_compact_linear_SQI` as a practical compact comparison, and `MDS10_pH_optimum_without_CE_SQI` as a scoring-rule sensitivity analysis.

## Scoring strategy

SQI scoring rules are defined in:

* `config/scoring_rules_mds.csv`

Scoring and SQI construction functions are centralized in:

* `scripts/sqi_utils.py`

The current workflow supports:

* `linear` scoring;
* `optimum_range` scoring for sensitivity analysis;
* `more_is_better` and `less_is_better` scoring directions.

The main SQI version currently uses linear min-max scoring. The pH optimum-range approach is retained only as a methodological sensitivity test.

Further details are documented in:

* `docs/scoring_strategy.md`
* `docs/decision_log.md`

## Documentation

The `docs/` directory contains methodological notes used to track the analytical rationale behind the workflow:

* `analysis_plan.md`: overall analysis plan;
* `mds_candidate_sets.md`: candidate MDS structure and interpretation;
* `decision_log.md`: methodological decisions made during development;
* `scoring_strategy.md`: current scoring rules and planned refinements;
* `sqi_candidate_decision_summary.md`: synthesis of the current SQI candidate selection and validation rationale.

## Project structure

```text
soil-quality-index-analysis/
├── config/
│   └── scoring_rules_mds.csv
├── data/
│   ├── raw/private/          # private raw data, not tracked by Git
│   └── processed/private/    # private processed data, not tracked by Git
├── docs/
│   ├── analysis_plan.md
│   ├── decision_log.md
│   ├── mds_candidate_sets.md
│   └── scoring_strategy.md
├── figures/
│   └── private/              # private generated figures, not tracked by Git
├── notebooks/
├── scripts/
├── tables/
│   └── private/              # private generated tables, not tracked by Git
├── .gitignore
├── README.md
└── requirements.txt
```

## How to run

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Then run the scripts sequentially from the repository root:

```bash
python scripts/00_check_data_import.py
python scripts/01_check_derived_indicators.py
python scripts/02_prepare_processed_dataset.py
```

Continue through the numbered scripts according to the analysis stage.

Because the original dataset is private and not included in this repository, the workflow is not fully reproducible from public files alone at this stage. The public repository documents the code structure, analytical logic, and methodological decisions while keeping unpublished data protected.

## Main methodological notes

Current methodological decisions include:

* using relative yield per plant as the primary response variable;
* retaining raw `PM1_mg_dm3` and `GMea` instead of clay-normalized versions in the main candidate set;
* using `MO_g_dm3` instead of calculated organic carbon as the main organic matter indicator;
* retaining `PST` as the primary sodicity indicator;
* treating electrical conductivity conservatively as a `less_is_better` indicator;
* keeping pH optimum-range scoring only as a sensitivity analysis.

These decisions are documented in `docs/decision_log.md`.

## Next steps

* Refine manuscript-oriented figures and tables using the CE-free principal SQI candidate;
* Update the manuscript draft to reflect `MDS10_without_CE_SQI` as the principal candidate;
* Prepare a clear Methods narrative matching the current reproducible workflow;
* Draft the Results and Discussion sections for the SQI manuscript;
* Add simulated or anonymized example data in the future, after ensuring that no unpublished private data are exposed;
* Revisit CE-containing candidates only as sensitivity analyses, not as principal SQI versions.

## Author

- Patryk Ramon Wandersee
- Agronomist | PhD in Soil Science
- GitHub: [PatrykWandersee](https://github.com/PatrykWandersee)
