#!/usr/bin/env python
from __future__ import annotations

from pathlib import Path
import pandas as pd
import yaml

from cberm.network import inverse_distance_pressure
from cberm.risk import normalize_series, weighted_sum, combine_components, risk_tiers
from cberm.stochastic import monte_carlo_scores


def main() -> None:
    demo = Path("data/demo")
    out = Path("outputs/tables")
    out.mkdir(parents=True, exist_ok=True)
    facilities = pd.read_csv(demo / "synthetic_facility_features.csv")
    sources = pd.read_csv(demo / "synthetic_outbreak_sources.csv")
    weights = yaml.safe_load(Path("configs/weights_baseline.yml").read_text())

    facilities["active_case_pressure"] = inverse_distance_pressure(facilities, sources)

    # Normalize raw numeric columns used by the model.
    invert_cols = {"time_to_isolation_referral", "time_to_lab_sample_referral"}
    for col in facilities.select_dtypes("number").columns:
        if col in {"lon", "lat"}:
            continue
        facilities[col] = normalize_series(facilities[col], invert=col in invert_cols)

    facilities["spillover_suitability"] = weighted_sum(facilities, weights["spillover_suitability"])
    facilities["human_exposure"] = weighted_sum(facilities, weights["human_exposure"])
    facilities["importation_pressure"] = weighted_sum(facilities, weights["importation_pressure"])
    facilities["facility_vulnerability"] = weighted_sum(facilities, weights["facility_vulnerability"])
    facilities["risk_score"] = combine_components(facilities, weights["combined_risk"])
    facilities["risk_tier"] = risk_tiers(facilities["risk_score"])

    mc = monte_carlo_scores(facilities, weights["combined_risk"], n_iterations=250)
    result = pd.concat([facilities, mc], axis=1).sort_values("risk_score", ascending=False)
    result.to_csv(out / "synthetic_facility_risk_rankings.csv", index=False)
    print(result[["facility_id", "facility_name", "risk_score", "risk_tier", "risk_p05", "risk_p95"]].head(10).to_string(index=False))
    print(f"Wrote {out / 'synthetic_facility_risk_rankings.csv'}")


if __name__ == "__main__":
    main()
