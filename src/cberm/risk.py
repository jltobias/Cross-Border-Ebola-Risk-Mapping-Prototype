from __future__ import annotations

from typing import Mapping, Sequence
import numpy as np
import pandas as pd


def normalize_series(values: pd.Series, invert: bool = False) -> pd.Series:
    """Min-max normalize a pandas Series to 0..1.

    Constant or all-missing inputs return zeros rather than raising.
    """
    x = pd.to_numeric(values, errors="coerce").astype(float)
    xmin = x.min(skipna=True)
    xmax = x.max(skipna=True)
    if not np.isfinite(xmin) or not np.isfinite(xmax) or xmax == xmin:
        y = pd.Series(0.0, index=values.index)
    else:
        y = (x - xmin) / (xmax - xmin)
    if invert:
        y = 1.0 - y
    return y.fillna(0.0).clip(0.0, 1.0)


def weighted_sum(frame: pd.DataFrame, weights: Mapping[str, float], missing: str = "zero") -> pd.Series:
    """Compute a normalized weighted sum from columns in *frame*.

    Parameters
    ----------
    frame:
        Feature table with normalized columns.
    weights:
        Mapping from column name to non-negative weight.
    missing:
        "zero" treats missing columns as all-zero; "raise" raises KeyError.
    """
    total_weight = float(sum(max(0.0, float(w)) for w in weights.values()))
    if total_weight == 0:
        return pd.Series(0.0, index=frame.index)
    score = pd.Series(0.0, index=frame.index, dtype=float)
    for col, weight in weights.items():
        weight = max(0.0, float(weight)) / total_weight
        if col not in frame.columns:
            if missing == "raise":
                raise KeyError(f"Missing required feature column: {col}")
            values = pd.Series(0.0, index=frame.index)
        else:
            values = pd.to_numeric(frame[col], errors="coerce").fillna(0.0)
        score = score + values.clip(0.0, 1.0) * weight
    return score.clip(0.0, 1.0)


def combine_components(frame: pd.DataFrame, component_weights: Mapping[str, float]) -> pd.Series:
    """Combine component scores into a final risk score."""
    return weighted_sum(frame, component_weights, missing="raise")


def risk_tiers(scores: pd.Series, labels: Sequence[str] = ("low", "moderate", "high", "very_high")) -> pd.Series:
    """Assign quantile-based risk tiers with robust fallback for tied values."""
    scores = pd.to_numeric(scores, errors="coerce").fillna(0.0)
    try:
        return pd.qcut(scores.rank(method="first"), q=len(labels), labels=labels).astype(str)
    except ValueError:
        bins = np.linspace(scores.min(), scores.max() if scores.max() > scores.min() else scores.min() + 1, len(labels) + 1)
        return pd.cut(scores, bins=bins, labels=labels, include_lowest=True).astype(str)


def top_drivers(row: pd.Series, weights: Mapping[str, float], n: int = 5) -> list[str]:
    """Return feature names with the largest weighted contribution for one row."""
    contributions = []
    for col, weight in weights.items():
        value = float(row.get(col, 0.0) or 0.0)
        contributions.append((col, value * float(weight)))
    return [name for name, _ in sorted(contributions, key=lambda x: x[1], reverse=True)[:n]]
