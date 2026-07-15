from __future__ import annotations

import math
import pandas as pd


def haversine_km(lon1, lat1, lon2, lat2) -> float:
    """Great-circle distance in kilometers for fallback corridor metrics."""
    r = 6371.0088
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def inverse_distance_pressure(
    targets: pd.DataFrame,
    sources: pd.DataFrame,
    target_lon: str = "lon",
    target_lat: str = "lat",
    source_lon: str = "lon",
    source_lat: str = "lat",
    source_weight: str = "case_count",
    decay_km: float = 150,
) -> pd.Series:
    """Compute simple distance-decay importation pressure from source locations."""
    scores = []
    for _, target in targets.iterrows():
        score = 0.0
        for _, source in sources.iterrows():
            d = haversine_km(target[target_lon], target[target_lat], source[source_lon], source[source_lat])
            score += float(source.get(source_weight, 1.0)) * math.exp(-d / decay_km)
        scores.append(score)
    return pd.Series(scores, index=targets.index)
