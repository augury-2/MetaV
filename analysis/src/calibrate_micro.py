"""
Calibration check for the micro parameterization.

Reports the implied effect sizes of the three limit-architecture levers on chosen sufficiency, the
analytic flip point, and the endogenous R-squareds, so that the values in config.P can be set to
magnitudes that are realistic for a vignette experiment rather than left wherever they happened to
land. Target magnitudes (from the consumer-psychology literature on framing and autonomy-support
manipulations): single-lever d in the .20-.40 range, best-vs-worst architecture contrast d ~ .6.

Run:  python calibrate_micro.py
"""
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
from scipy import stats

warnings.filterwarnings("ignore")

from dgp import flip_point, study3a_factorial, study3b_stringency
from experiment_analysis import study3a, study3b


def main():
    d3a = study3a_factorial(n_per_cell=400)
    r = study3a(d3a)
    print("Implied effect sizes for each limit-architecture lever (N = %d, 400/cell):" % len(d3a))
    print(r["marginals"].round(3).to_string(index=False))
    print("\nBest-vs-worst architecture contrast:")
    print("  " + ", ".join(f"{k}={v:.4f}" if isinstance(v, float) else f"{k}={v}"
                           for k, v in r["contrast"].items()))
    print("\nLatent SDs of the composites:")
    print(d3a[[c for c in d3a.columns if c.endswith("_c")]].std().round(3).to_string())

    print(f"\nAnalytic flip point: " +
          ", ".join(f"S*({p:+.1f})={flip_point(p):.3f}" for p in (-1.5, -1.0, 0.0, 1.0, 1.5)))

    d3b = study3b_stringency(n=2100)
    q = study3b(d3b, reps=400)
    print("\nStudy 3B quadratic: " + ", ".join(
        f"{k}={float(v):.4f}" for k, v in q["quadratic"].items()))
    print("Two-lines: " + str(q["two_lines"]))


if __name__ == "__main__":
    main()
