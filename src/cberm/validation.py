from __future__ import annotations

import pandas as pd
from sklearn.metrics import roc_auc_score, average_precision_score


def binary_metrics(y_true, y_score) -> dict[str, float]:
    """Compute common binary ranking metrics with robust fallbacks."""
    y_true = pd.Series(y_true).astype(int)
    y_score = pd.Series(y_score).astype(float)
    out: dict[str, float] = {}
    if y_true.nunique() > 1:
        out["roc_auc"] = float(roc_auc_score(y_true, y_score))
        out["average_precision"] = float(average_precision_score(y_true, y_score))
    else:
        out["roc_auc"] = float("nan")
        out["average_precision"] = float("nan")
    return out
