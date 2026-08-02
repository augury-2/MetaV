"""
STUDY 3 - Experimental tests of limit architecture, the flip point, and the sufficiency-washing
penalty.

3A. 2 (limit agency: chosen / imposed) x 2 (locus: collective / individual)
    x 2 (frame: sufficiency / reduction) between-subjects factorial, stringency fixed at 0.35.
    DVs: chosen sufficiency; mediators PA and AD examined separately to show the dual route
    responds to different design levers.

3B. Continuous-dose experiment (7 stringency levels) locating the FLIP POINT S*.
    - quadratic regression with bootstrap CI on the turning point
    - two-lines test (Simonsohn 2018): a genuine inverted-U requires a significant positive
      slope below the breakpoint and a significant negative slope above it. A significant
      quadratic term alone does not establish an inverted-U, and reviewers know this.
    - flip point re-estimated within precarity terciles to test dS*/d(precarity) < 0 (H8)
    - comparison of the empirically recovered S* against the analytic S* implied by the theory

3C. 2 (demarketing intensity) x 2 (sacrifice signal) factorial on brand sufficiency equity,
    testing H13: demarketing builds brand equity only when it is costly to the firm.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats
from statsmodels.stats.anova import anova_lm

from config import BOOT_REPS, SEED, TAB_DIR
from dgp import cs_stringency_profile, flip_point


# ======================================================================================
# helpers
# ======================================================================================
def _partial_eta_sq(aov: pd.DataFrame) -> pd.DataFrame:
    aov = aov.copy()
    ss_resid = aov.loc["Residual", "sum_sq"]
    aov["partial_eta_sq"] = aov["sum_sq"] / (aov["sum_sq"] + ss_resid)
    aov.loc["Residual", "partial_eta_sq"] = np.nan
    return aov


def _cohens_d(a: np.ndarray, b: np.ndarray) -> float:
    na, nb = len(a), len(b)
    s = np.sqrt(((na - 1) * a.var(ddof=1) + (nb - 1) * b.var(ddof=1)) / (na + nb - 2))
    return float((a.mean() - b.mean()) / s)


# ======================================================================================
# 3A. Factorial limit architecture
# ======================================================================================
def study3a(df: pd.DataFrame) -> dict:
    out = {}
    for dv in ["CS_c", "PA_c", "AD_c", "RIA_c", "PR_c"]:
        m = smf.ols(f"{dv} ~ C(agency)*C(locus)*C(frame)", data=df).fit()
        aov = _partial_eta_sq(anova_lm(m, typ=2))
        aov.insert(0, "dv", dv)
        aov.index.name = "term"
        out[dv] = aov.reset_index()

    anova_all = pd.concat(out.values(), ignore_index=True)

    cells = (df.groupby(["agency", "locus", "frame"])
             .agg(n=("CS_c", "size"), CS_mean=("CS_c", "mean"), CS_sd=("CS_c", "std"),
                  PA_mean=("PA_c", "mean"), AD_mean=("AD_c", "mean"),
                  RIA_mean=("RIA_c", "mean"), PR_mean=("PR_c", "mean"))
             .reset_index())
    cells["CS_se"] = cells["CS_sd"] / np.sqrt(cells["n"])

    # planned contrast: best architecture (chosen / collective / sufficiency-framed)
    #                   vs worst (imposed / individual / reduction-framed)
    best = df.query("agency==1 and locus==1 and frame==1")["CS_c"].to_numpy()
    worst = df.query("agency==0 and locus==0 and frame==0")["CS_c"].to_numpy()
    t, p = stats.ttest_ind(best, worst, equal_var=False)
    contrast = {"contrast": "chosen/collective/sufficiency vs imposed/individual/reduction",
                "M_best": best.mean(), "M_worst": worst.mean(),
                "diff": best.mean() - worst.mean(), "t": float(t), "p": float(p),
                "cohens_d": _cohens_d(best, worst), "n_best": len(best), "n_worst": len(worst)}

    # marginal effects of each design dimension on each route
    marg = []
    for factor in ["agency", "locus", "frame"]:
        for dv in ["CS_c", "PA_c", "AD_c"]:
            hi = df[df[factor] == 1][dv].to_numpy()
            lo = df[df[factor] == 0][dv].to_numpy()
            tt, pp = stats.ttest_ind(hi, lo, equal_var=False)
            marg.append({"factor": factor, "dv": dv, "M_high": hi.mean(), "M_low": lo.mean(),
                         "diff": hi.mean() - lo.mean(), "t": float(tt), "p": float(pp),
                         "cohens_d": _cohens_d(hi, lo)})
    return {"anova": anova_all, "cells": cells, "contrast": contrast,
            "marginals": pd.DataFrame(marg)}


# ======================================================================================
# 3B. The flip point
# ======================================================================================
def _quad_peak(x: np.ndarray, y: np.ndarray,
               Z: np.ndarray | None = None) -> tuple[float, float, float, float, float]:
    """OLS y ~ 1 + x + x^2 (+ covariates Z); returns (b1, b2, p_b2, peak, r2)."""
    cols = [x, x ** 2] if Z is None else [x, x ** 2, *Z.T]
    X = sm.add_constant(np.column_stack(cols))
    res = sm.OLS(y, X).fit()
    b1, b2 = res.params[1], res.params[2]
    peak = -b1 / (2 * b2) if b2 != 0 else np.nan
    return b1, b2, res.pvalues[2], peak, res.rsquared


def bootstrap_peak(x: np.ndarray, y: np.ndarray, reps: int = 2000,
                   seed: int = SEED, Z: np.ndarray | None = None
                   ) -> tuple[float, float, float]:
    rng = np.random.default_rng(seed)
    n = len(x)
    peaks = np.empty(reps)
    for b in range(reps):
        idx = rng.integers(0, n, n)
        peaks[b] = _quad_peak(x[idx], y[idx], None if Z is None else Z[idx])[3]
    peaks = peaks[np.isfinite(peaks) & (np.abs(peaks) < 5)]
    lo, hi = np.percentile(peaks, [2.5, 97.5])
    return float(np.median(peaks)), float(lo), float(hi)


def bootstrap_peak_difference(x_lo, y_lo, x_hi, y_hi, reps: int = 3000,
                              seed: int = SEED) -> dict:
    """
    Direct, adequately powered test of H8: does the turning point S* differ between the
    low- and high-precarity subsamples? Bootstraps the DIFFERENCE in turning points.

    This is reported in place of relying on the stringency^2 x precarity product term, which is
    a triple-order term with very low power at realistic sample sizes.
    """
    rng = np.random.default_rng(seed)
    diffs = np.empty(reps)
    n_lo, n_hi = len(x_lo), len(x_hi)
    for b in range(reps):
        i = rng.integers(0, n_lo, n_lo)
        j = rng.integers(0, n_hi, n_hi)
        p_lo = _quad_peak(x_lo[i], y_lo[i])[3]
        p_hi = _quad_peak(x_hi[j], y_hi[j])[3]
        diffs[b] = p_hi - p_lo
    diffs = diffs[np.isfinite(diffs) & (np.abs(diffs) < 5)]
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    return {"peak_low_precarity": _quad_peak(x_lo, y_lo)[3],
            "peak_high_precarity": _quad_peak(x_hi, y_hi)[3],
            "difference_S_star": float(np.median(diffs)),
            "ci_lo": float(lo), "ci_hi": float(hi),
            "boot_p_one_sided_negative": float((diffs >= 0).mean()),
            "H8_supported": bool(hi < 0)}


def two_lines_test(x: np.ndarray, y: np.ndarray, breakpoint: float) -> dict:
    """
    Simonsohn's (2018) two-lines test: regress y on two linear segments joined at `breakpoint`.
    An inverted-U requires slope_low > 0 (p < .05) AND slope_high < 0 (p < .05).
    """
    lowx = np.minimum(x, breakpoint)
    highx = np.maximum(x - breakpoint, 0.0)
    X = sm.add_constant(np.column_stack([lowx, highx]))
    res = sm.OLS(y, X).fit()
    b_low, b_high = res.params[1], res.params[2]
    p_low, p_high = res.pvalues[1], res.pvalues[2]
    return {"breakpoint": breakpoint,
            "slope_low": float(b_low), "p_low": float(p_low),
            "slope_high": float(b_high), "p_high": float(p_high),
            "inverted_U_supported": bool(b_low > 0 and p_low < .05 and b_high < 0 and p_high < .05)}


def study3b(df: pd.DataFrame, reps: int = 2000) -> dict:
    x = df["stringency"].to_numpy()
    y = df["CS_c"].to_numpy()

    b1, b2, p2, peak, r2 = _quad_peak(x, y)
    peak_med, peak_lo, peak_hi = bootstrap_peak(x, y, reps=reps)
    tl = two_lines_test(x, y, breakpoint=float(np.clip(peak, x.min() + 0.01, x.max() - 0.01)))

    # covariate-adjusted replication (precision, not identification: stringency is randomized)
    Z = df[["precarity", "collectivism", "community", "growth_endorse", "symbolic"]].to_numpy()
    cb1, cb2, cp2, cpeak, cr2 = _quad_peak(x, y, Z)

    quad = {"b_linear": b1, "b_quadratic": b2, "p_quadratic": p2, "r2": r2,
            "peak_point_est": peak, "peak_boot_median": peak_med,
            "peak_ci_lo": peak_lo, "peak_ci_hi": peak_hi,
            "adj_b_linear": cb1, "adj_b_quadratic": cb2, "adj_p_quadratic": cp2,
            "adj_peak": cpeak, "adj_r2": cr2,
            "analytic_flip_point_at_mean_precarity": flip_point(0.0)}

    # dose-response means
    dose = (df.groupby("stringency")
            .agg(n=("CS_c", "size"), CS=("CS_c", "mean"), CS_se=("CS_c", lambda s: s.std() / np.sqrt(len(s))),
                 RIA=("RIA_c", "mean"), AD=("AD_c", "mean"), PA=("PA_c", "mean"), PR=("PR_c", "mean"))
            .reset_index())

    # H8: flip point by precarity tercile
    df = df.copy()
    df["prec_tercile"] = pd.qcut(df["precarity"], 3, labels=["low", "mid", "high"])
    rows = []
    for lab, g in df.groupby("prec_tercile", observed=True):
        gx, gy = g["stringency"].to_numpy(), g["CS_c"].to_numpy()
        gb1, gb2, gp2, gpeak, gr2 = _quad_peak(gx, gy)
        pm, plo, phi = bootstrap_peak(gx, gy, reps=max(600, reps // 3))
        rows.append({"precarity_tercile": lab, "n": len(g),
                     "mean_precarity": g["precarity"].mean(),
                     "b_quadratic": gb2, "p_quadratic": gp2,
                     "peak": gpeak, "peak_boot_median": pm,
                     "peak_ci_lo": plo, "peak_ci_hi": phi,
                     "analytic_flip_point": flip_point(g["precarity"].mean())})
    by_prec = pd.DataFrame(rows)

    # formal test that the peak shifts: interaction stringency^2 x precarity
    mod = smf.ols("CS_c ~ stringency + I(stringency**2) + precarity "
                  "+ stringency:precarity + I(stringency**2):precarity", data=df).fit()
    shift = {"b_str_x_prec": mod.params["stringency:precarity"],
             "p_str_x_prec": mod.pvalues["stringency:precarity"],
             "b_str2_x_prec": mod.params["I(stringency ** 2):precarity"],
             "p_str2_x_prec": mod.pvalues["I(stringency ** 2):precarity"],
             "r2": mod.rsquared}

    # direct bootstrap test of the flip-point shift (median split on precarity)
    med = df["precarity"].median()
    lo_g = df[df["precarity"] <= med]
    hi_g = df[df["precarity"] > med]
    peak_diff = bootstrap_peak_difference(
        lo_g["stringency"].to_numpy(), lo_g["CS_c"].to_numpy(),
        hi_g["stringency"].to_numpy(), hi_g["CS_c"].to_numpy(),
        reps=max(1500, reps))
    peak_diff["analytic_peak_low"] = flip_point(lo_g["precarity"].mean())
    peak_diff["analytic_peak_high"] = flip_point(hi_g["precarity"].mean())
    peak_diff["analytic_difference"] = (peak_diff["analytic_peak_high"]
                                       - peak_diff["analytic_peak_low"])

    # two-lines test within precarity halves: does the descending arm start earlier?
    tl_halves = {}
    for lab, g in (("low_precarity", lo_g), ("high_precarity", hi_g)):
        gx, gy = g["stringency"].to_numpy(), g["CS_c"].to_numpy()
        bp = float(np.clip(_quad_peak(gx, gy)[3], gx.min() + 0.01, gx.max() - 0.01))
        tl_halves[lab] = two_lines_test(gx, gy, bp)

    # theory curve for the figure
    grid = np.linspace(0.0, 1.0, 201)
    theory = pd.DataFrame({"stringency": grid})
    for pl, plab in [(-1.0, "precarity_-1SD"), (0.0, "precarity_mean"), (1.0, "precarity_+1SD")]:
        theory[plab] = cs_stringency_profile(grid, pl)
    theory_peaks = {f"S_star_at_precarity_{p:+.1f}": flip_point(p)
                    for p in (-1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5)}

    return {"quadratic": quad, "two_lines": tl, "dose": dose, "by_precarity": by_prec,
            "peak_shift": shift, "peak_difference": peak_diff, "two_lines_halves": tl_halves,
            "theory_curve": theory, "theory_peaks": theory_peaks}


# ======================================================================================
# 3C. Sufficiency-washing penalty
# ======================================================================================
def study3c(df: pd.DataFrame) -> dict:
    df = df.copy()
    df["intensity_hi"] = (df["demkt_intensity"] > 0.5).astype(int)
    df["sacrifice_hi"] = (df["demkt_sacrifice"] > 0.5).astype(int)

    m = smf.ols("BSE_c ~ C(intensity_hi)*C(sacrifice_hi)", data=df).fit()
    aov = _partial_eta_sq(anova_lm(m, typ=2)).reset_index().rename(columns={"index": "term"})

    cells = (df.groupby(["intensity_hi", "sacrifice_hi"])
             .agg(n=("BSE_c", "size"), BSE=("BSE_c", "mean"),
                  sd=("BSE_c", "std")).reset_index())
    cells["se"] = cells["sd"] / np.sqrt(cells["n"])

    simple = []
    for sac in (0, 1):
        hi = df.query("sacrifice_hi==@sac and intensity_hi==1")["BSE_c"].to_numpy()
        lo = df.query("sacrifice_hi==@sac and intensity_hi==0")["BSE_c"].to_numpy()
        t, p = stats.ttest_ind(hi, lo, equal_var=False)
        simple.append({"sacrifice": "high" if sac else "low",
                       "M_high_intensity": hi.mean(), "M_low_intensity": lo.mean(),
                       "effect_of_demarketing_intensity": hi.mean() - lo.mean(),
                       "t": float(t), "p": float(p), "cohens_d": _cohens_d(hi, lo)})
    return {"anova": aov, "cells": cells, "simple_effects": pd.DataFrame(simple)}


# ======================================================================================
# Driver
# ======================================================================================
def run(d3a: pd.DataFrame, d3b: pd.DataFrame, d3c: pd.DataFrame, reps: int = 2000) -> dict:
    print("[Study 3A] 2x2x2 limit-architecture factorial (N = %d) ..." % len(d3a))
    r3a = study3a(d3a)
    r3a["anova"].to_csv(f"{TAB_DIR}/t10a_study3a_anova.csv", index=False)
    r3a["cells"].to_csv(f"{TAB_DIR}/t10b_study3a_cells.csv", index=False)
    r3a["marginals"].to_csv(f"{TAB_DIR}/t10c_study3a_marginals.csv", index=False)
    print(r3a["anova"].query("dv=='CS_c'").round(4).to_string(index=False))
    print("\n  Cell means on chosen sufficiency:")
    print(r3a["cells"].round(3).to_string(index=False))
    print("\n  Planned contrast: " + ", ".join(
        f"{k}={v:.4f}" if isinstance(v, float) else f"{k}={v}"
        for k, v in r3a["contrast"].items()))
    print("\n  Design dimension -> route specificity:")
    print(r3a["marginals"].round(3).to_string(index=False))

    print("\n[Study 3B] Flip-point estimation (N = %d) ..." % len(d3b))
    r3b = study3b(d3b, reps=reps)
    pd.DataFrame([r3b["quadratic"]]).to_csv(f"{TAB_DIR}/t11a_flip_quadratic.csv", index=False)
    pd.DataFrame([r3b["two_lines"]]).to_csv(f"{TAB_DIR}/t11b_two_lines.csv", index=False)
    r3b["dose"].to_csv(f"{TAB_DIR}/t11c_dose_response.csv", index=False)
    r3b["by_precarity"].to_csv(f"{TAB_DIR}/t11d_flip_by_precarity.csv", index=False)
    pd.DataFrame([r3b["peak_shift"]]).to_csv(f"{TAB_DIR}/t11e_peak_shift.csv", index=False)
    r3b["theory_curve"].to_csv(f"{TAB_DIR}/t11f_theory_curve.csv", index=False)
    pd.DataFrame([r3b["peak_difference"]]).to_csv(f"{TAB_DIR}/t11g_peak_difference.csv", index=False)
    pd.DataFrame(r3b["two_lines_halves"]).T.to_csv(f"{TAB_DIR}/t11h_two_lines_halves.csv")
    print("  " + ", ".join(f"{k}={v:.4f}" for k, v in r3b["quadratic"].items()))
    print("  two-lines: " + ", ".join(f"{k}={v}" for k, v in r3b["two_lines"].items()))
    print("\n  Dose-response on chosen sufficiency:")
    print(r3b["dose"].round(3).to_string(index=False))
    print("\n  H8 - flip point by precarity tercile:")
    print(r3b["by_precarity"].round(3).to_string(index=False))
    print("\n  Peak-shift interaction: " + ", ".join(f"{k}={v:.4g}" for k, v in r3b["peak_shift"].items()))
    print("  H8 direct bootstrap test of the flip-point shift:")
    for k, v in r3b["peak_difference"].items():
        print(f"    {k} = {v if isinstance(v, bool) else round(float(v), 4)}")
    print("  Two-lines test within precarity halves:")
    for lab, tl in r3b["two_lines_halves"].items():
        print(f"    {lab}: " + ", ".join(
            f"{k}={v if isinstance(v, bool) else round(float(v), 4)}" for k, v in tl.items()))
    print("\n  Analytic flip points implied by the theory:")
    for k, v in r3b["theory_peaks"].items():
        print(f"    {k} = {v:.4f}")

    print("\n[Study 3C] Demarketing intensity x sacrifice on brand sufficiency equity (N = %d) ..."
          % len(d3c))
    r3c = study3c(d3c)
    r3c["anova"].to_csv(f"{TAB_DIR}/t12a_study3c_anova.csv", index=False)
    r3c["cells"].to_csv(f"{TAB_DIR}/t12b_study3c_cells.csv", index=False)
    r3c["simple_effects"].to_csv(f"{TAB_DIR}/t12c_study3c_simple.csv", index=False)
    print(r3c["anova"].round(4).to_string(index=False))
    print(r3c["cells"].round(3).to_string(index=False))
    print("\n  Simple effects of demarketing intensity:")
    print(r3c["simple_effects"].round(4).to_string(index=False))

    return {"s3a": r3a, "s3b": r3b, "s3c": r3c}
