from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = [
    "candidate_set",
    "indicator",
    "domain",
    "scoring_direction",
    "scoring_method",
    "main_role",
    "notes",
]


def load_scoring_rules(config_path):
    config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(f"Scoring rules file not found: {config_path}")

    rules = pd.read_csv(config_path)

    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in rules.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns in scoring rules file: {missing_columns}"
        )

    duplicated = rules.duplicated(subset=["candidate_set", "indicator"])

    if duplicated.any():
        duplicated_rows = rules.loc[
            duplicated,
            ["candidate_set", "indicator"],
        ]
        raise ValueError(
            "Duplicated candidate_set/indicator combinations found:\n"
            f"{duplicated_rows}"
        )

    return rules


def get_candidate_sets(scoring_rules):
    candidate_sets = {}

    for candidate_set, group in scoring_rules.groupby("candidate_set", sort=False):
        candidate_sets[candidate_set] = group["indicator"].tolist()

    return candidate_sets


def minmax_score(series, direction):
    minimum = series.min()
    maximum = series.max()

    if maximum == minimum:
        return pd.Series(1.0, index=series.index)

    if direction == "more_is_better":
        return (series - minimum) / (maximum - minimum)

    if direction == "less_is_better":
        return (maximum - series) / (maximum - minimum)

    raise ValueError(f"Unknown scoring direction: {direction}")


def build_sqi_scores(data, scoring_rules, candidate_set):
    set_rules = scoring_rules[
        scoring_rules["candidate_set"] == candidate_set
    ].copy()

    if set_rules.empty:
        raise ValueError(f"No scoring rules found for candidate set: {candidate_set}")

    scores = pd.DataFrame(index=data.index)
    score_columns = []

    for _, row in set_rules.iterrows():
        indicator = row["indicator"]
        scoring_direction = row["scoring_direction"]
        scoring_method = row["scoring_method"]

        if indicator not in data.columns:
            raise ValueError(f"Indicator not found in dataset: {indicator}")

        if scoring_method != "linear_minmax":
            raise ValueError(
                f"Unsupported scoring method for {indicator}: {scoring_method}"
            )

        score_col = f"{candidate_set}_{indicator}_score"

        scores[score_col] = minmax_score(
            data[indicator],
            scoring_direction,
        )

        score_columns.append(score_col)

    sqi_col = f"{candidate_set}_SQI"
    scores[sqi_col] = scores[score_columns].mean(axis=1)

    return scores, sqi_col, score_columns
