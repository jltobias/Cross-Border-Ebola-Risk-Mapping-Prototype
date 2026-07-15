import pandas as pd

from cberm.risk import normalize_series, weighted_sum, risk_tiers
from cberm.stochastic import monte_carlo_scores


def test_normalize_series_constant_returns_zero():
    s = pd.Series([5, 5, 5])
    assert normalize_series(s).tolist() == [0.0, 0.0, 0.0]


def test_weighted_sum_bounds():
    df = pd.DataFrame({"a": [0, 0.5, 1], "b": [1, 0.5, 0]})
    score = weighted_sum(df, {"a": 0.5, "b": 0.5})
    assert ((score >= 0) & (score <= 1)).all()


def test_risk_tiers_length():
    tiers = risk_tiers(pd.Series([0.1, 0.2, 0.3, 0.4]))
    assert len(tiers) == 4


def test_monte_carlo_scores_shape():
    df = pd.DataFrame({"a": [0.1, 0.8], "b": [0.9, 0.2]})
    mc = monte_carlo_scores(df, {"a": 0.5, "b": 0.5}, n_iterations=10)
    assert set(["risk_mean", "risk_sd", "risk_p05", "risk_p50", "risk_p95"]).issubset(mc.columns)
    assert len(mc) == 2
