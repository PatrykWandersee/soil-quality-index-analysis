from pathlib import Path

import pandas as pd
import numpy as np


PROJECT_DIR = Path(__file__).resolve().parents[1]

RAW_DATA_PATH = (
    PROJECT_DIR
    / "data"
    / "raw"
    / "private"
    / "soil_quality_raw_private.csv"
)

PROCESSED_DATA_PATH = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "private"
    / "soil_quality_processed_private.csv"
)

df = pd.read_csv(RAW_DATA_PATH, decimal=",")

# Recalculate selected derived indicators to avoid spreadsheet rounding issues
df["PM1_per_Clay"] = df["PM1_mg_dm3"] / df["Argila_g_kg"]
df["GMea_per_Clay"] = df["GMea"] / df["Argila_g_kg"]

# Log-transformed versions for exploratory comparison
df["log_PM1_per_Clay"] = np.log1p(df["PM1_per_Clay"])
df["log_GMea_per_Clay"] = np.log1p(df["GMea_per_Clay"])

# Keep a simple processing report
print("\nProcessed dataset created.")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")
print(f"Output file: {PROCESSED_DATA_PATH}")

print("\nNew indicators:")
new_cols = [
    "PM1_per_Clay",
    "GMea_per_Clay",
    "log_PM1_per_Clay",
    "log_GMea_per_Clay",
]

print(df[new_cols].describe().T)

df.to_csv(PROCESSED_DATA_PATH, index=False)
