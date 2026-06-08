from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_DIR / "data" / "raw" / "private" / "soil_quality_raw_private.csv"

df = pd.read_csv(DATA_PATH, decimal=",")

# Recalculate clay-normalized indicators
df["PM1_por_argila_check"] = df["PM1_mg_dm3"] / df["Argila_g_kg"]
df["GMea_por_Argila_check"] = df["GMea"] / df["Argila_g_kg"]

# Compare spreadsheet values with recalculated values
df["PM1_por_argila_diff"] = df["PM1_por_argila"] - df["PM1_por_argila_check"]
df["GMea_por_Argila_diff"] = df["GMea_por_Argila"] - df["GMea_por_Argila_check"]

print("\nDerived indicator check")
print("=" * 40)

print("\nPM1_por_argila:")
print(f"Maximum absolute difference: {df['PM1_por_argila_diff'].abs().max()}")

print("\nGMea_por_Argila:")
print(f"Maximum absolute difference: {df['GMea_por_Argila_diff'].abs().max()}")

# Flag rows with relevant differences
tolerance = 1e-4

problem_rows = df[
    (df["PM1_por_argila_diff"].abs() > tolerance)
    | (df["GMea_por_Argila_diff"].abs() > tolerance)
]

print("\nRows with differences above tolerance:")
if problem_rows.empty:
    print("None. Spreadsheet calculations match Python recalculations.")
else:
    cols_to_show = [
        "Area",
        "Fazenda",
        "PM1_mg_dm3",
        "GMea",
        "Argila_g_kg",
        "PM1_por_argila",
        "PM1_por_argila_check",
        "PM1_por_argila_diff",
        "GMea_por_Argila",
        "GMea_por_Argila_check",
        "GMea_por_Argila_diff",
    ]
    print(problem_rows[cols_to_show])

print("\nBasic summary of checked indicators:")
summary_cols = [
    "PM1_mg_dm3",
    "PM1_por_argila",
    "PM1_por_argila_check",
    "GMea",
    "GMea_por_Argila",
    "GMea_por_Argila_check",
    "Argila_g_kg",
]

print(df[summary_cols].describe().T)
