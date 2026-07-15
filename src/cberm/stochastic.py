from __future__ import annotations

from typing import Mapping
import numpy as np
import pandas as pd

from .risk import weighted_sum


def sample_dirichlet_weights(base_weights: Mapping[str, float], concentration: float = 40, rng=None) -> dict[str, float]:
    """Sample uncertain weights around a baseline using a Dirichlet distribution."""
    rng = np.random.default_rng(rng)
    keys = list(base_weights)
    baseline = np.array([max(0.0, float(base_weights[k])) for k in keys], dtype=float)
    if baseline.sum() == 0:
        baseline = np.ones(len(keys), dtype=float) / len(keys)
    else:
        baseline = baseline / baseline.sum()
    alpha = np.maximum(baseline * float(concentration), 1e-6)
    draw = rng.dirichlet(alpha)
    return dict(zip(keys, draw))


def monte_carlo_scores(
    features: pd.DataFrame,
    base_weights: Mapping[str, float],
    n_iterations: int = 1000,
    concentration: float = 40,
    random_seed: int = 42,
) -> pd.DataFrame:
    """Run a Monte Carlo weighted-overlay model over tabular features."""
    rng = np.random.default_rng(random_seed)
    simulations = []
    for _ in range(int(n_iterations)):
        weights = sample_dirichlet_weights(base_weights, concentration=concentration, rng=rng)
        simulations.append(weighted_sum(features, weights).to_numpy())
    arr = np.vstack(simulations)
    return pd.DataFrame(
        {
            "risk_mean": arr.mean(axis=0),
            "risk_sd": arr.std(axis=0),
            "risk_p05": np.quantile(arr, 0.05, axis=0),
            "risk_p50": np.quantile(arr, 0.50, axis=0),
            "risk_p95": np.quantile(arr, 0.95, axis=0),
        },
        index=features.index,
    )
