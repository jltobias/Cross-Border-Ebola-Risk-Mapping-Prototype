from __future__ import annotations

from typing import Iterable
import pandas as pd

from .risk import normalize_series


def normalize_feature_table(
    frame: pd.DataFrame,
    invert_columns: Iterable[str] = (),
    passthrough_columns: Iterable[str] = ("facility_id", "name", "admin", "geometry"),
) -> pd.DataFrame:
    """Normalize numeric feature columns while preserving IDs and labels."""
    invert = set(invert_columns)
    passthrough = set(passthrough_columns)
    out = pd.DataFrame(index=frame.index)
    for col in frame.columns:
        if col in passthrough or not pd.api.types.is_numeric_dtype(frame[col]):
            out[col] = frame[col]
        else:
            out[f"{col}_norm"] = normalize_series(frame[col], invert=col in invert)
    return out


def interface_overlap_score(frame: pd.DataFrame, human_cols: list[str], ecology_cols: list[str]) -> pd.Series:
    """Simple Venn-overlap proxy: mean human score times mean ecology score."""
    human = frame[human_cols].mean(axis=1).clip(0.0, 1.0) if human_cols else 0.0
    ecology = frame[ecology_cols].mean(axis=1).clip(0.0, 1.0) if ecology_cols else 0.0
    return human * ecology
