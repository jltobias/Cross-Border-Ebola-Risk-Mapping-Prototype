from __future__ import annotations

import pandas as pd


def prepare_presence_background(
    presences: pd.DataFrame,
    background: pd.DataFrame,
    feature_columns: list[str],
    label_column: str = "presence",
) -> pd.DataFrame:
    """Build a presence/background table for ENM/SDM modeling."""
    p = presences[feature_columns].copy()
    p[label_column] = 1
    b = background[feature_columns].copy()
    b[label_column] = 0
    return pd.concat([p, b], ignore_index=True)


def fit_elapid_maxent(training_frame: pd.DataFrame, feature_columns: list[str], label_column: str = "presence"):
    """Fit an elapid MaxentModel if elapid is installed.

    This wrapper keeps notebooks clean and allows graceful failure in environments
    where elapid is not available.
    """
    try:
        from elapid import MaxentModel  # type: ignore
    except Exception as exc:  # pragma: no cover
        raise ImportError("Install elapid to run Maxent ENM: pip install elapid") from exc
    model = MaxentModel()
    model.fit(training_frame[feature_columns], training_frame[label_column])
    return model
