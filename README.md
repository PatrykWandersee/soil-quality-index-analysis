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
* `sqi_utils.py`: contains shared utility functions for scoring and SQI construction.

## Candidate SQI versions

The current workflow retains one main SQI candidate set and two sensitivity versions:

* `MDS11_main`: principal preliminary SQI version with 11 indicators;
* `MDS12_sodicity`: sensitivity version adding `Na_Troc_cmolc_Kg`;
* `MDS11_pH_optimum`: sensitivity version testing optimum-range pH scoring.

The main candidate set is retained because it is parsimonious, interpretable, and maintains a strong association with relative yield. Sensitivity versions are used to evaluate specific methodological alternatives without replacing the main SQI version.

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
* `scoring_strategy.md`: current scoring rules and planned refinements.

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

Planned refinements include:

* improving public-facing documentation;
* adding anonymized or simulated example data;
* improving reproducibility for users without access to the private dataset;
* refining scoring functions with agronomic thresholds or independent validation;
* preparing publication-oriented figures and tables;
* expanding model validation, including mixed-model approaches.

## Author

Patryk Ramon Wandersee
Agronomist | PhD in Soil Science

GitHub: [PatrykWandersee](https://github.com/PatrykWandersee)
