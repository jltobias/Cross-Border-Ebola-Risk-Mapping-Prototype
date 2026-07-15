from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd


def plot_ranked_risk(frame: pd.DataFrame, score_col: str = "risk_score", label_col: str = "facility_name", top_n: int = 25):
    """Plot the top ranked facilities as a simple horizontal bar chart."""
    data = frame.sort_values(score_col, ascending=False).head(top_n).iloc[::-1]
    fig, ax = plt.subplots(figsize=(9, max(4, 0.25 * len(data))))
    ax.barh(data[label_col].astype(str), data[score_col])
    ax.set_xlabel(score_col)
    ax.set_ylabel(label_col)
    ax.set_title(f"Top {len(data)} facility risk scores")
    fig.tight_layout()
    return fig, ax
