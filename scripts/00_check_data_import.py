from pathlib import Path

import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_DIR / "data" / "raw" / "private" / "soil_quality_raw_private.csv"

df = pd.read_csv(DATA_PATH, decimal=",")

print("\nData imported successfully.")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

print("\nColumn names:")
for col in df.columns:
    print(col)

print("\nFirst five rows:")
print(df.head())

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
missing = df.isna().sum()
print(missing[missing > 0].sort_values(ascending=False))

print("\nData type counts:")
print(df.dtypes.value_counts())

print("\nObject columns:")
object_cols = df.select_dtypes(include=["object", "string"]).columns
for col in object_cols:
    print(col)

print("\nNumeric columns:")
numeric_cols = df.select_dtypes(include="number").columns
print(f"{len(numeric_cols)} numeric columns")

print("\nPotential problem columns:")
for col in object_cols:
    unique_sample = df[col].dropna().astype(str).head(5).tolist()
    print(f"{col}: {unique_sample}")
