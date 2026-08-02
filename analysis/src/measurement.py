"""
STUDY 1 - Measurement adequacy, identification, parameter recovery, and statistical power.

Purpose: establish that the SSM is *measurable and testable* before any substantive claim is
made. Three components:

  1A. Confirmatory factor analysis of the 15-construct measurement model (fit, loadings,
      composite reliability, AVE) plus HTMT discriminant validity against the four adjacent
      constructs that reviewers will raise (voluntary simplicity, frugality, materialism,
      constrained restraint).
  1B. Monte Carlo parameter recovery: are the focal structural parameters recovered without
      finite-sample bias, and are nominal 95% CIs actually covering?
  1C. Power curves for every focal path, giving the minimum N needed to detect each
      hypothesized effect at 80% power - i.e. a design specification for the field study.

Recovery is assessed against the *asymptotic estimand*: the value the canonical estimator
converges to under the DGP (computed once at N = 200,000). This is the correct benchmark,
because measurement error attenuates composite-based coefficients relative to the latent
parameters, and we want to certify the estimator, not pretend attenuation away.
"""
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd

import semopy

from config import (ALPHA, MC_REPS, MC_SAMPLE_SIZES, MEASURES, SEED, TAB_DIR)
from dgp import add_items, composites, simulate_latents
from structural import EQUATIONS, PREDICTED_SIGN, fit_structural

warnings.filterwarnings("ignore")

CONSTRUCT_LABELS = {
    "PA": "Perceived autonomy", "CE": "Collective efficacy", "RIA": "Restraint identity affirmation",
    "RSV": "Restraint signaling value", "AD": "Anticipated deprivation", "PR": "Psychological reactance",
    "CS": "Chosen sufficiency", "SCB": "Sufficiency commitment behavior",
    "BSE": "Brand sufficiency equity", "SPS": "Sufficiency policy support",
    "CDC": "Compensatory displacement consumption", "VS": "Voluntary simplicity",
    "FRUG": "Frugality", "MAT": "Materialism", "CR": "Constrained restraint",
}


# ======================================================================================
# 1A. CFA
# ======================================================================================
def measurement_model_desc(constructs: list[str]) -> str:
    lines = []
    for c in constructs:
        items = " + ".join(f"{c}{k}" for k in range(1, MEASURES[c]["n_items"] + 1))
        lines.append(f"{c} =~ {items}")
    return "\n".join(lines)


def run_cfa(df: pd.DataFrame, constructs: list[str] | None = None):
    constructs = constructs or list(MEASURES.keys())
    desc = measurement_model_desc(constructs)
    model = semopy.Model(desc)
    model.fit(df[[f"{c}{k}" for c in constructs for k in range(1, MEASURES[c]["n_items"] + 1)]])
    stats = semopy.calc_stats(model)
    stats = stats.assign(**{"chi2/df": stats["chi2"] / stats["DoF"]})
    ins = model.inspect(std_est=True)
    loadings = ins[(ins["op"] == "~") & (ins["rval"].isin(constructs))].copy()
    return model, stats, loadings, ins


def reliability_table(df: pd.DataFrame, loadings: pd.DataFrame,
                      constructs: list[str] | None = None) -> pd.DataFrame:
    """Cronbach's alpha, composite reliability (omega), AVE from standardized CFA loadings."""
    constructs = constructs or list(MEASURES.keys())
    rows = []
    for c in constructs:
        cols = [f"{c}{k}" for k in range(1, MEASURES[c]["n_items"] + 1)]
        sub = df[cols]
        k = len(cols)
        cm = sub.cov().to_numpy()
        alpha = (k / (k - 1)) * (1 - np.trace(cm) / cm.sum())
        lam = loadings.loc[loadings["rval"] == c, "Est. Std"].astype(float).to_numpy()
        lam = np.abs(lam)
        cr = lam.sum() ** 2 / (lam.sum() ** 2 + np.sum(1 - lam ** 2))
        ave = np.mean(lam ** 2)
        rows.append({"construct": c, "label": CONSTRUCT_LABELS.get(c, c), "n_items": k,
                     "alpha": alpha, "CR_omega": cr, "AVE": ave,
                     "min_loading": lam.min(), "max_loading": lam.max()})
    out = pd.DataFrame(rows)
    out["AVE_ok"] = out["AVE"] > 0.50
    out["CR_ok"] = out["CR_omega"] > 0.70
    return out


def htmt_matrix(df: pd.DataFrame, constructs: list[str] | None = None) -> pd.DataFrame:
    """Heterotrait-monotrait ratio of correlations (Henseler et al. 2015)."""
    constructs = constructs or list(MEASURES.keys())
    items = {c: [f"{c}{k}" for k in range(1, MEASURES[c]["n_items"] + 1)] for c in constructs}
    corr = df[[i for c in constructs for i in items[c]]].corr()

    def mono(c):
        cols = items[c]
        vals = [abs(corr.loc[a, b]) for i, a in enumerate(cols) for b in cols[i + 1:]]
        return float(np.mean(vals))

    def hetero(c1, c2):
        vals = [abs(corr.loc[a, b]) for a in items[c1] for b in items[c2]]
        return float(np.mean(vals))

    M = pd.DataFrame(np.nan, index=constructs, columns=constructs, dtype=float)
    for i, c1 in enumerate(constructs):
        for c2 in constructs[i + 1:]:
            denom = np.sqrt(mono(c1) * mono(c2))
            M.loc[c2, c1] = hetero(c1, c2) / denom if denom > 0 else np.nan
    return M


# ======================================================================================
# 1B / 1C. Monte Carlo recovery and power
# ======================================================================================
def _one_sample(n: int, rng: np.random.Generator) -> pd.DataFrame:
    """
    One replication drawn from the SAME population as the Study 2 survey: a pooled four-country
    sample. Drawing the Monte Carlo replications from an undifferentiated population while
    estimating the substantive model on a stratified cross-national sample would make the
    asymptotic estimands the wrong benchmark.
    """
    from config import COUNTRIES
    per = max(25, n // len(COUNTRIES))
    frames = [simulate_latents(per, rng, country=c) for c in COUNTRIES]
    df = pd.concat(frames, ignore_index=True)
    return composites(add_items(df, rng))


def asymptotic_estimands(n_big: int = 200_000, seed: int = 987) -> pd.Series:
    """Population values of the canonical estimator under the DGP."""
    rng = np.random.default_rng(seed)
    df = _one_sample(n_big, rng)
    res = fit_structural(df)
    return res.set_index("path")["b"]


def monte_carlo(sample_sizes=None, reps: int = MC_REPS, seed: int = SEED,
                truth: pd.Series | None = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Returns (recovery_table, power_table).

    recovery: per path x N -> mean estimate, bias, %bias, RMSE, empirical SE, mean analytic SE,
              95% CI coverage.
    power:    per path x N -> directional power (share of reps with p < .05 and correct sign).
    """
    sample_sizes = sample_sizes or MC_SAMPLE_SIZES
    truth = asymptotic_estimands() if truth is None else truth
    rng = np.random.default_rng(seed)

    records = []
    for n in sample_sizes:
        for r in range(reps):
            df = _one_sample(n, rng)
            res = fit_structural(df)
            for _, row in res.iterrows():
                records.append({"N": n, "rep": r, "path": row["path"], "b": row["b"],
                                "se": row["se"], "p": row["p"],
                                "ci_lo": row["ci_lo"], "ci_hi": row["ci_hi"],
                                "sign_ok": row["sign_ok"]})
    mc = pd.DataFrame(records)
    mc["true"] = mc["path"].map(truth)
    mc["covered"] = (mc["ci_lo"] <= mc["true"]) & (mc["true"] <= mc["ci_hi"])
    mc["detected"] = (mc["p"] < ALPHA) & mc["sign_ok"]

    recovery = (mc.groupby(["path", "N"])
                .apply(lambda g: pd.Series({
                    "true": g["true"].iloc[0],
                    "mean_est": g["b"].mean(),
                    "bias": g["b"].mean() - g["true"].iloc[0],
                    "pct_bias": 100 * (g["b"].mean() - g["true"].iloc[0]) / (abs(g["true"].iloc[0]) + 1e-12),
                    "rmse": np.sqrt(np.mean((g["b"] - g["true"]) ** 2)),
                    "emp_se": g["b"].std(),
                    "mean_analytic_se": g["se"].mean(),
                    "coverage_95": g["covered"].mean(),
                    "power": g["detected"].mean(),
                }), include_groups=False)
                .reset_index())

    power = recovery.pivot(index="path", columns="N", values="power")
    power["hypothesis"] = pd.Series({k: v[3] for k, v in EQUATIONS.items()})
    power["true_b"] = truth
    power["N_for_80pct"] = [
        _min_n_for_power(recovery[recovery["path"] == p], 0.80) for p in power.index
    ]
    cols = ["hypothesis", "true_b"] + [c for c in power.columns if isinstance(c, (int, np.integer))] + ["N_for_80pct"]
    return recovery, power[cols].reset_index()


def _min_n_for_power(sub: pd.DataFrame, target: float) -> float:
    """Linear interpolation on the power curve; NaN if never reached in the swept range."""
    sub = sub.sort_values("N")
    ns, pw = sub["N"].to_numpy(float), sub["power"].to_numpy(float)
    if pw.max() < target:
        return np.nan
    if pw[0] >= target:
        return float(ns[0])
    for i in range(1, len(ns)):
        if pw[i] >= target:
            x0, x1, y0, y1 = ns[i - 1], ns[i], pw[i - 1], pw[i]
            return float(x0 + (target - y0) * (x1 - x0) / (y1 - y0))
    return np.nan


# ======================================================================================
# Driver
# ======================================================================================
def run(df_survey: pd.DataFrame, reps: int = MC_REPS) -> dict:
    print("[Study 1A] Confirmatory factor analysis of the 15-construct measurement model ...")
    model, stats, loadings, ins = run_cfa(df_survey)
    fit = stats[["chi2", "DoF", "chi2/df", "chi2 p-value", "CFI", "TLI", "NFI",
                 "RMSEA", "GFI", "AGFI", "AIC", "BIC"]]
    fit.to_csv(f"{TAB_DIR}/t1_cfa_fit.csv", index=False)
    print(fit.to_string(index=False))

    rel = reliability_table(df_survey, loadings)
    rel.to_csv(f"{TAB_DIR}/t2_reliability_ave.csv", index=False)
    print("\n[Study 1A] Reliability and convergent validity:")
    print(rel.round(3).to_string(index=False))

    htmt = htmt_matrix(df_survey)
    htmt.round(3).to_csv(f"{TAB_DIR}/t3_htmt.csv")
    max_htmt = np.nanmax(htmt.to_numpy())
    print(f"\n[Study 1A] Max HTMT = {max_htmt:.3f} (criterion < .85)")
    cs_htmt = pd.concat([htmt.loc["CS"].dropna(), htmt["CS"].dropna()])
    print("[Study 1A] HTMT of Chosen Sufficiency vs adjacent constructs:")
    print(cs_htmt[cs_htmt.index.isin(["VS", "FRUG", "MAT", "CR"])].round(3).to_string())

    print(f"\n[Study 1B/1C] Monte Carlo: {reps} reps x {len(MC_SAMPLE_SIZES)} sample sizes ...")
    truth = asymptotic_estimands()
    recovery, power = monte_carlo(reps=reps, truth=truth)
    recovery.to_csv(f"{TAB_DIR}/t4_mc_recovery.csv", index=False)
    power.to_csv(f"{TAB_DIR}/t5_power_curves.csv", index=False)

    at_1600 = recovery[recovery["N"] == 1600]
    print(f"\n[Study 1B] Recovery at N=1600: max |%bias| = {at_1600['pct_bias'].abs().max():.2f}%, "
          f"mean coverage = {at_1600['coverage_95'].mean():.3f}")
    print("\n[Study 1C] Power at N=1600 and required N for 80% power:")
    print(power[["path", "hypothesis", "true_b", 1600, "N_for_80pct"]].round(3).to_string(index=False))

    return {"cfa_fit": fit, "reliability": rel, "htmt": htmt,
            "recovery": recovery, "power": power, "truth": truth,
            "max_htmt": max_htmt}
