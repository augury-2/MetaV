"""
Calibration search for the Study 4 market-systems model.

The theory predicts five qualitatively distinct regimes (constructs.md section 6.3). A model that
cannot produce all five is not a test of the theory - it has smuggled the answer into the
parameters. Conversely, a model that produces whichever regime you like for any parameter values
has no content. This script searches the firm-economics parameters for a region in which every
predicted regime is reachable from its theoretically specified configuration, and reports the
result so the final parameterization is auditable rather than asserted.

Run:  python calibrate_abm.py
"""
from __future__ import annotations

import itertools
import warnings
from dataclasses import replace

import pandas as pd

import abm_market as A

warnings.filterwarnings("ignore")

TARGET = ["futility", "collapse", "niche", "tipping", "backlash"]


def evaluate(service_fee: float, reconfig_cost: float, subsidy_coef: float,
             n_periods: int = 80, n_consumers: int = 1200) -> dict:
    base = replace(A.Params(), service_fee=service_fee, reconfig_cost_share=reconfig_cost,
                   n_periods=n_periods, n_consumers=n_consumers)
    orig = A.apply_policy_level

    def patched(p, level):
        q = orig(p, level)
        return replace(q, pol_repair_subsidy=subsidy_coef * level)

    A.apply_policy_level = patched
    try:
        rows = {}
        for name, p in A.named_scenarios(base).items():
            rows[name] = A.run_pair(replace(p, n_periods=n_periods, n_consumers=n_consumers))
    finally:
        A.apply_policy_level = orig

    hits = sum(1 for k in TARGET if rows[k]["regime"] == k)
    out = {"service_fee": service_fee, "reconfig_cost_share": reconfig_cost,
           "subsidy_coef": subsidy_coef, "hits": hits}
    for k in TARGET:
        out[f"{k}_regime"] = rows[k]["regime"]
        out[f"{k}_dQ"] = round(rows[k]["throughput_reduction"], 3)
        out[f"{k}_relpi"] = round(float(rows[k]["relative_profit_demarketers"]), 3)
    return out


def main():
    grid = itertools.product(
        [0.115, 0.140, 0.165, 0.190],   # service_fee
        [0.10, 0.14, 0.18],             # reconfig_cost_share
        [0.35, 0.50, 0.80],             # repair-subsidy coefficient on policy level
    )
    out = []
    for sf, rc, sc in grid:
        r = evaluate(sf, rc, sc)
        out.append(r)
        print(f"fee={sf} reconfig={rc} subsidy={sc} -> hits={r['hits']} "
              + " ".join(f"{k}:{r[k + '_regime']}({r[k + '_dQ']:+.2f},{r[k + '_relpi']:.2f})"
                         for k in TARGET))
    df = pd.DataFrame(out).sort_values("hits", ascending=False)
    df.to_csv("../output/tables/calibration_search.csv", index=False)
    print("\nBest:")
    print(df.head(6).to_string(index=False))


if __name__ == "__main__":
    main()
