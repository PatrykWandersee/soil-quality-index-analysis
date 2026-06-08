from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import spearmanr


PROJECT_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "private"
    / "soil_quality_processed_private.csv"
)

FIGURE_DIR = PROJECT_DIR / "figures" / "private" / "candidate_indicators"
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH)

response = "Prod_rel_pct"

figures_to_create = [
    {
        "x": "PM1_mg_dm3",
        "y": response,
        "xlabel": "Mehlich-1 P (mg dm⁻³)",
        "ylabel": "Relative yield per plant (%)",
        "filename": "pm1_vs_relative_yield.png",
    },
    {
        "x": "PM1_per_Clay",
        "y": response,
        "xlabel": "Mehlich-1 P / clay",
        "ylabel": "Relative yield per plant (%)",
        "filename": "pm1_per_clay_vs_relative_yield.png",
    },
    {
        "x": "GMea",
        "y": response,
        "xlabel": "GMea",
        "ylabel": "Relative yield per plant (%)",
        "filename": "gmea_vs_relative_yield.png",
    },
    {
        "x": "GMea_per_Clay",
        "y": response,
        "xlabel": "GMea / clay",
        "ylabel": "Relative yield per plant (%)",
        "filename": "gmea_per_clay_vs_relative_yield.png",
    },
]


def create_scatter_plot(data, x, y, xlabel, ylabel, output_path):
    plot_data = data[[x, y]].dropna()

    rho, p_value = spearmanr(plot_data[x], plot_data[y])

    fig, ax = plt.subplots(figsize=(5.5, 4.2))

    ax.scatter(
        plot_data[x],
        plot_data[y],
        s=38,
        facecolors="none",
        edgecolors="black",
        linewidths=0.8,
    )

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    annotation = f"Spearman rho = {rho:.3f}\np = {p_value:.4f}\nn = {len(plot_data)}"

    ax.text(
        0.05,
        0.95,
        annotation,
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=9,
        bbox={
            "boxstyle": "round",
            "facecolor": "white",
            "edgecolor": "black",
            "linewidth": 0.5,
        },
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)


for item in figures_to_create:
    output_path = FIGURE_DIR / item["filename"]

    create_scatter_plot(
        data=df,
        x=item["x"],
        y=item["y"],
        xlabel=item["xlabel"],
        ylabel=item["ylabel"],
        output_path=output_path,
    )

    print(f"Saved: {output_path}")

print("\nExploratory figures created.")
