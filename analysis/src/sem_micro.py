"""
STUDY 2 - Latent structural equation model of the dual-route architecture, plus cross-national
multigroup analysis.

Three components:
  2A. Full latent SEM (11 endogenous latents, observed exogenous design/moderator variables)
      estimated by ML; global fit, standardized paths, endogenous R^2.
  2B. Reduced-form canonical specification with all product terms (structural.py), which carries
      the moderation hypotheses that a latent product-indicator SEM would estimate unstably at
      this N.
  2C. Multigroup analysis across DE / FR / SE / BR:
        - configural fit (CFA per country)
        - permutation test of loading equality (metric-invariance proxy, MICOM logic)
        - permutation test of structural-path heterogeneity across countries
      Permutation tests are used rather than chi-square difference tests because they do not
      assume multivariate normality and are the accepted standard for multigroup comparison in
      the composite-modeling literature.
"""
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
import semopy

from config import COUNTRIES, MEASURES, SEED, TAB_DIR
from measurement import measurement_model_desc
from structural import EQUATIONS, equation_r2, fit_structural

warnings.filterwarnings("ignore")

LATENTS = ["PA", "CE", "RIA", "RSV", "AD", "PR", "CS", "SCB", "BSE", "SPS", "CDC"]

STRUCTURAL_DESC = """
PA  ~ agency + locus + frame + stringency + precarity
CE  ~ locus + community + frame
RIA ~ PA + frame + CE + growth_endorse
RSV ~ RIA + symbolic
AD  ~ agency + frame + stringency + precarity + symbolic
PR  ~ AD + agency
CS  ~ RIA + RSV + CE + PR + AD
SCB ~ CS + PR
BSE ~ CS + PR + demkt_intensity + demkt_sacrifice
SPS ~ CS + CE
CDC ~ CS + PR + symbolic
"""

FIT_COLS = ["chi2", "DoF", "chi2 p-value", "CFI", "TLI", "NFI", "RMSEA",
            "GFI", "AGFI", "AIC", "BIC"]


def sem_desc() -> str:
    return measurement_model_desc(LATENTS) + "\n" + STRUCTURAL_DESC


def _sem_columns(df: pd.DataFrame) -> list[str]:
    items = [f"{c}{k}" for c in LATENTS for k in range(1, MEASURES[c]["n_items"] + 1)]
    exog = ["agency", "locus", "frame", "stringency", "precarity", "collectivism",
            "community", "growth_endorse", "symbolic", "demkt_intensity", "demkt_sacrifice"]
    return [c for c in items + exog if c in df.columns]


# ======================================================================================
# 2A. Latent SEM
# ======================================================================================
def fit_latent_sem(df: pd.DataFrame):
    model = semopy.Model(sem_desc())
    model.fit(df[_sem_columns(df)])
    stats = semopy.calc_stats(model)
    ins = model.inspect(std_est=True)
    paths = ins[(ins["op"] == "~")].copy()
    paths = paths[paths["lval"].isin(LATENTS)]
    paths = paths.rename(columns={"lval": "dv", "rval": "predictor",
                                  "Est. Std": "beta_std", "Estimate": "b",
                                  "Std. Err": "se", "p-value": "p"})
    keep = ["dv", "predictor", "b", "se", "beta_std", "p"]
    return model, stats[FIT_COLS], paths[keep].reset_index(drop=True)


def latent_r2(model, df: pd.DataFrame) -> pd.DataFrame:
    """R^2 for each endogenous latent from the fitted SEM."""
    try:
        r2 = semopy.calc_stats(model)  # not used directly; fall back to inspect-based method
    except Exception:
        pass
    ins = model.inspect(std_est=True)
    rows = []
    for lv in LATENTS:
        # residual variance of the latent in standardized solution
        resid = ins[(ins["lval"] == lv) & (ins["rval"] == lv) & (ins["op"] == "~~")]
        if len(resid):
            v = float(resid["Est. Std"].iloc[0])
            rows.append({"latent": lv, "residual_var_std": v, "r2": max(0.0, 1.0 - v)})
    return pd.DataFrame(rows)


# ======================================================================================
# 2C. Multigroup
# ======================================================================================
def configural_fit(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for c in COUNTRIES:
        sub = df[df["country"] == c]
        m = semopy.Model(measurement_model_desc(LATENTS))
        m.fit(sub[[f"{k}{j}" for k in LATENTS for j in range(1, MEASURES[k]["n_items"] + 1)]])
        s = semopy.calc_stats(m)
        row = {"country": c, "n": len(sub)}
        row.update({k: float(s[k].iloc[0]) for k in ["chi2", "DoF", "CFI", "TLI", "RMSEA"]})
        rows.append(row)
    return pd.DataFrame(rows)


def _loading_vector(sub: pd.DataFrame) -> np.ndarray:
    m = semopy.Model(measurement_model_desc(LATENTS))
    m.fit(sub[[f"{k}{j}" for k in LATENTS for j in range(1, MEASURES[k]["n_items"] + 1)]])
    ins = m.inspect(std_est=True)
    lo = ins[(ins["op"] == "~") & (ins["rval"].isin(LATENTS))]
    lo = lo.sort_values(["rval", "lval"])
    return lo["Est. Std"].astype(float).to_numpy()


def metric_invariance_permutation(df: pd.DataFrame, n_perm: int = 200,
                                  seed: int = SEED) -> dict:
    """
    Permutation test of loading equality across countries.
    Statistic: mean absolute deviation of group loadings from the pooled loading vector.
    A non-significant p indicates the loadings are not distinguishable across groups
    (i.e. metric invariance is tenable).
    """
    rng = np.random.default_rng(seed)
    groups = df["country"].to_numpy()

    def stat(labels):
        vecs = [_loading_vector(df[labels == c]) for c in COUNTRIES]
        V = np.vstack(vecs)
        return float(np.mean(np.abs(V - V.mean(axis=0, keepdims=True))))

    obs = stat(groups)
    null = np.empty(n_perm)
    for b in range(n_perm):
        null[b] = stat(rng.permutation(groups))
    p = float((null >= obs).mean())
    return {"observed_MAD": obs, "perm_p": p, "null_mean": float(null.mean()),
            "null_sd": float(null.std()), "n_perm": n_perm,
            "invariance_tenable": p > 0.05}


def multigroup_paths(df: pd.DataFrame, n_perm: int = 1000, seed: int = SEED) -> pd.DataFrame:
    """
    Per-country estimates of every focal path plus an omnibus permutation test of
    cross-country heterogeneity (statistic: SD of the coefficient across the four countries).
    """
    rng = np.random.default_rng(seed)
    per_country = {c: fit_structural(df[df["country"] == c]).set_index("path")["b"]
                   for c in COUNTRIES}
    B = pd.DataFrame(per_country)
    obs = B.std(axis=1)

    labels = df["country"].to_numpy()
    null = np.empty((n_perm, len(B)))
    for b in range(n_perm):
        perm = rng.permutation(labels)
        d = df.copy()
        d["_g"] = perm
        cols = {c: fit_structural(d[d["_g"] == c]).set_index("path")["b"] for c in COUNTRIES}
        null[b] = pd.DataFrame(cols).std(axis=1).reindex(B.index).to_numpy()

    p = (null >= obs.to_numpy()[None, :]).mean(axis=0)
    out = B.copy()
    out["sd_across_countries"] = obs
    out["perm_p_heterogeneity"] = p
    out["heterogeneous"] = out["perm_p_heterogeneity"] < 0.05
    out["hypothesis"] = pd.Series({k: v[3] for k, v in EQUATIONS.items()})
    return out.reset_index()


# ======================================================================================
# Driver
# ======================================================================================
def run(df: pd.DataFrame, n_perm_metric: int = 150, n_perm_paths: int = 400) -> dict:
    print("[Study 2A] Fitting the latent structural equation model ...")
    model, fit, paths = fit_latent_sem(df)
    fit.to_csv(f"{TAB_DIR}/t6a_sem_fit.csv", index=False)
    paths.to_csv(f"{TAB_DIR}/t6b_sem_paths.csv", index=False)
    print(fit.round(4).to_string(index=False))
    print("\n[Study 2A] Standardized structural paths:")
    print(paths.round(4).to_string(index=False))

    r2 = latent_r2(model, df)
    r2.to_csv(f"{TAB_DIR}/t6c_sem_r2.csv", index=False)
    print("\n[Study 2A] Endogenous latent R^2:")
    print(r2.round(3).to_string(index=False))

    print("\n[Study 2B] Reduced-form canonical specification (all hypothesized terms):")
    red = fit_structural(df)
    red.to_csv(f"{TAB_DIR}/t6d_reduced_form.csv", index=False)
    print(red[["path", "hypothesis", "b", "se", "t", "p", "supported"]].round(4).to_string(index=False))
    print(f"\n  Hypothesized terms supported (correct sign, p < .05): "
          f"{int(red['supported'].sum())}/{len(red)}")

    eqr2 = equation_r2(df)
    eqr2.to_csv(f"{TAB_DIR}/t6e_equation_r2.csv", index=False)

    print("\n[Study 2C] Configural fit by country ...")
    cfg = configural_fit(df)
    cfg.to_csv(f"{TAB_DIR}/t9a_configural_fit.csv", index=False)
    print(cfg.round(3).to_string(index=False))

    print(f"\n[Study 2C] Metric-invariance permutation test ({n_perm_metric} permutations) ...")
    inv = metric_invariance_permutation(df, n_perm=n_perm_metric)
    pd.DataFrame([inv]).to_csv(f"{TAB_DIR}/t9b_metric_invariance.csv", index=False)
    print("  " + ", ".join(f"{k}={v}" for k, v in inv.items()))

    print(f"\n[Study 2C] Multigroup path heterogeneity ({n_perm_paths} permutations) ...")
    mg = multigroup_paths(df, n_perm=n_perm_paths)
    mg.to_csv(f"{TAB_DIR}/t9c_multigroup_paths.csv", index=False)
    print(mg.round(4).to_string(index=False))
    het = mg[mg["heterogeneous"]]["path"].tolist()
    print(f"\n  Paths differing significantly across countries: {het if het else 'none'}")

    return {"sem_fit": fit, "sem_paths": paths, "sem_r2": r2, "reduced": red,
            "equation_r2": eqr2, "configural": cfg, "invariance": inv, "multigroup": mg}
