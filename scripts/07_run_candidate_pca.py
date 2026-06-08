from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


PROJECT_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "private"
    / "soil_quality_processed_private.csv"
)

TABLE_DIR = PROJECT_DIR / "tables" / "private"
FIGURE_DIR = PROJECT_DIR / "figures" / "private" / "pca"

TABLE_DIR.mkdir(parents=True, exist_ok=True)
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

candidate_vars = [
    "PM1_mg_dm3",
    "GMea",
    "Beta_glic",
    "Arilsulf",
    "MO_g_dm3",
    "Argila_g_kg",
    "Areia_g_kg",
    "Floculacao_pct",
    "Ds_g_cm3",
    "pH",
    "CE_dS_m",
    "Ca_Troc_cmolc_Kg",
    "Mg_Troc_cmolc_Kg",
    "K_Troc_cmolc_Kg",
    "Na_Troc_cmolc_Kg",
    "PST",
]

df = pd.read_csv(DATA_PATH)

missing_vars = [var for var in candidate_vars if var not in df.columns]
if missing_vars:
    raise ValueError(f"Missing variables in dataset: {missing_vars}")

pca_data = df[candidate_vars].dropna().copy()

print("\nCandidate PCA")
print("=" * 60)
print(f"Original rows: {df.shape[0]}")
print(f"Rows used in PCA after dropping missing values: {pca_data.shape[0]}")
print(f"Variables used in PCA: {len(candidate_vars)}")

# Standardize variables before PCA
scaler = StandardScaler()
x_scaled = scaler.fit_transform(pca_data)

pca = PCA()
scores = pca.fit_transform(x_scaled)

component_names = [f"PC{i + 1}" for i in range(len(candidate_vars))]

explained_variance = pd.DataFrame(
    {
        "component": component_names,
        "eigenvalue": pca.explained_variance_,
        "explained_variance_ratio": pca.explained_variance_ratio_,
        "cumulative_explained_variance": pca.explained_variance_ratio_.cumsum(),
    }
)

loadings = pd.DataFrame(
    pca.components_.T,
    index=candidate_vars,
    columns=component_names,
)

# Variable contributions to each component, expressed as percentage
contributions = loadings.pow(2)
contributions = contributions.div(contributions.sum(axis=0), axis=1) * 100

scores_df = pd.DataFrame(
    scores,
    columns=component_names,
    index=pca_data.index,
)

scores_df.insert(0, "Area", df.loc[pca_data.index, "Area"].values)
scores_df.insert(1, "Fazenda", df.loc[pca_data.index, "Fazenda"].values)
scores_df.insert(2, "Prod_rel_pct", df.loc[pca_data.index, "Prod_rel_pct"].values)

explained_variance.to_csv(
    TABLE_DIR / "pca_candidate_set_explained_variance.csv",
    index=False,
)

loadings.to_csv(
    TABLE_DIR / "pca_candidate_set_loadings.csv",
)

contributions.to_csv(
    TABLE_DIR / "pca_candidate_set_contributions.csv",
)

scores_df.to_csv(
    TABLE_DIR / "pca_candidate_set_scores.csv",
    index=False,
)

print("\nExplained variance:")
print(
    explained_variance.head(8).to_string(
        index=False,
        formatters={
            "eigenvalue": "{:.3f}".format,
            "explained_variance_ratio": "{:.3f}".format,
            "cumulative_explained_variance": "{:.3f}".format,
        },
    )
)

print("\nTop variable contributions by component:")
for component in component_names[:5]:
    print("\n" + component)
    print("-" * len(component))
    top_contrib = (
        contributions[component]
        .sort_values(ascending=False)
        .head(6)
    )
    print(top_contrib.to_string(float_format="{:.2f}".format))


# Scree plot
fig, ax = plt.subplots(figsize=(5.5, 4.2))

ax.plot(
    range(1, len(candidate_vars) + 1),
    pca.explained_variance_,
    marker="o",
    linewidth=1,
)

ax.axhline(y=1, linestyle="--", linewidth=0.8)

ax.set_xlabel("Principal component")
ax.set_ylabel("Eigenvalue")
ax.set_title("Scree plot")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

fig.tight_layout()
fig.savefig(FIGURE_DIR / "pca_candidate_set_scree.png", dpi=300)
plt.close(fig)


# Scores plot: PC1 x PC2
fig, ax = plt.subplots(figsize=(5.5, 4.5))

ax.scatter(
    scores_df["PC1"],
    scores_df["PC2"],
    s=38,
    facecolors="none",
    edgecolors="black",
    linewidths=0.8,
)

ax.axhline(y=0, linewidth=0.6)
ax.axvline(x=0, linewidth=0.6)

pc1_var = explained_variance.loc[0, "explained_variance_ratio"] * 100
pc2_var = explained_variance.loc[1, "explained_variance_ratio"] * 100

ax.set_xlabel(f"PC1 ({pc1_var:.1f}%)")
ax.set_ylabel(f"PC2 ({pc2_var:.1f}%)")
ax.set_title("PCA scores")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

fig.tight_layout()
fig.savefig(FIGURE_DIR / "pca_candidate_set_scores_pc1_pc2.png", dpi=300)
plt.close(fig)


# Loading plot: PC1 x PC2
fig, ax = plt.subplots(figsize=(6.2, 5.2))

ax.axhline(y=0, linewidth=0.6)
ax.axvline(x=0, linewidth=0.6)

for var in candidate_vars:
    x = loadings.loc[var, "PC1"]
    y = loadings.loc[var, "PC2"]

    ax.arrow(
        0,
        0,
        x,
        y,
        head_width=0.015,
        length_includes_head=True,
        linewidth=0.7,
    )

    ax.text(
        x * 1.08,
        y * 1.08,
        var,
        fontsize=8,
        ha="center",
        va="center",
    )

ax.set_xlabel(f"PC1 ({pc1_var:.1f}%)")
ax.set_ylabel(f"PC2 ({pc2_var:.1f}%)")
ax.set_title("PCA loadings")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

fig.tight_layout()
fig.savefig(FIGURE_DIR / "pca_candidate_set_loadings_pc1_pc2.png", dpi=300)
plt.close(fig)

print("\nPCA outputs saved.")
print(f"Tables: {TABLE_DIR}")
print(f"Figures: {FIGURE_DIR}")
