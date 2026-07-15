#!/usr/bin/env python
from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd


def main() -> None:
    rng = np.random.default_rng(42)
    out = Path("data/demo")
    out.mkdir(parents=True, exist_ok=True)
    n = 40
    facilities = pd.DataFrame(
        {
            "facility_id": [f"HF{i:03d}" for i in range(n)],
            "facility_name": [f"Synthetic Facility {i:03d}" for i in range(n)],
            "lon": rng.uniform(28.0, 32.5, n),
            "lat": rng.uniform(3.0, 7.5, n),
            "population_density": rng.gamma(2.0, 80.0, n),
            "settlement_building_density": rng.gamma(2.0, 25.0, n),
            "road_accessibility": rng.uniform(0, 1, n),
            "conflict_displacement_pressure": rng.beta(1.5, 3.0, n),
            "bat_roost_proximity": rng.beta(2.0, 3.0, n),
            "forest_edge_density": rng.beta(2.5, 2.5, n),
            "recent_deforestation": rng.beta(1.2, 4.0, n),
            "mine_cave_karst_proximity": rng.beta(1.5, 5.0, n),
            "orchard_fruit_tree_interface": rng.beta(2.0, 4.0, n),
            "time_to_isolation_referral": rng.gamma(2.0, 2.0, n),
            "time_to_lab_sample_referral": rng.gamma(2.0, 3.0, n),
            "facility_level_readiness": rng.uniform(0.2, 1.0, n),
        }
    )
    facilities.to_csv(out / "synthetic_facility_features.csv", index=False)

    sources = pd.DataFrame(
        {
            "source_id": ["DRC_A", "DRC_B", "UGA_A"],
            "lon": [29.2, 30.1, 30.7],
            "lat": [1.3, 2.1, 1.1],
            "case_count": [50, 25, 8],
        }
    )
    sources.to_csv(out / "synthetic_outbreak_sources.csv", index=False)
    print(f"Wrote synthetic demo data to {out}")


if __name__ == "__main__":
    main()
