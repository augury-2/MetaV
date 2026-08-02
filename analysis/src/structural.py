"""
Structural estimation of the SSM on measured composites.

A single canonical specification is defined here and reused by:
  * Study 1 Monte Carlo recovery / power analysis  (measurement.py)
  * Study 2 structural model                        (sem_micro.py)
  * Study 3 experiments                             (experiment_analysis.py)

Using one specification everywhere means the power analysis is a power analysis *of the
estimator actually reported*, which is the only version of a power analysis that means anything.

Focal paths are named to match ../../model/constructs.md section 7 (H1-H14).
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

# Each entry: name -> (dependent variable, patsy RHS, term whose coefficient is focal, hypothesis)
EQUATIONS: dict[str, tuple[str, str, str, str]] = {
    # --- Route A ---
    "PA<-agency": ("PA_c", "agency + locus + frame + stringency + precarity + locus:collectivism", "agency", "H1"),
    "PA<-locus:collectivism": ("PA_c", "agency + locus + frame + stringency + precarity + locus:collectivism", "locus:collectivism", "H2"),
    "CE<-locus": ("CE_c", "locus + community + frame + locus:collectivism", "locus", "H2"),
    "CE<-locus:collectivism": ("CE_c", "locus + community + frame + locus:collectivism", "locus:collectivism", "H2"),
    "RIA<-PA": ("RIA_c", "PA_c + frame + CE_c + growth_endorse + stringency", "PA_c", "H4"),
    "RIA<-frame": ("RIA_c", "PA_c + frame + CE_c + growth_endorse + stringency", "frame", "H3"),
    "RSV<-RIA:symbolic": ("RSV_c", "RIA_c + symbolic + RIA_c:symbolic", "RIA_c:symbolic", "H5"),
    # --- Route B ---
    "AD<-agency": ("AD_c", "agency + frame + stringency + I(stringency**2) + precarity + symbolic + stringency:precarity", "agency", "H1/H9"),
    "AD<-frame": ("AD_c", "agency + frame + stringency + I(stringency**2) + precarity + symbolic + stringency:precarity", "frame", "H3"),
    "AD<-stringency2": ("AD_c", "agency + frame + stringency + I(stringency**2) + precarity + symbolic + stringency:precarity", "I(stringency ** 2)", "H7"),
    "AD<-stringency:precarity": ("AD_c", "agency + frame + stringency + I(stringency**2) + precarity + symbolic + stringency:precarity", "stringency:precarity", "H8/H9"),
    "PR<-AD": ("PR_c", "AD_c + agency + symbolic + AD_c:symbolic", "AD_c", "H10"),
    "PR<-AD:symbolic": ("PR_c", "AD_c + agency + symbolic + AD_c:symbolic", "AD_c:symbolic", "H10"),
    # --- Net resultant ---
    "CS<-RIA": ("CS_c", "RIA_c + RSV_c + CE_c + PR_c + AD_c + RIA_c:symbolic + symbolic", "RIA_c", "H4"),
    "CS<-RSV": ("CS_c", "RIA_c + RSV_c + CE_c + PR_c + AD_c + RIA_c:symbolic + symbolic", "RSV_c", "H5"),
    "CS<-PR": ("CS_c", "RIA_c + RSV_c + CE_c + PR_c + AD_c + RIA_c:symbolic + symbolic", "PR_c", "H6"),
    "CS<-AD": ("CS_c", "RIA_c + RSV_c + CE_c + PR_c + AD_c + RIA_c:symbolic + symbolic", "AD_c", "H6"),
    "CS<-RIA:symbolic": ("CS_c", "RIA_c + RSV_c + CE_c + PR_c + AD_c + RIA_c:symbolic + symbolic", "RIA_c:symbolic", "H10"),
    # --- Outcomes ---
    "SCB<-CS": ("SCB_c", "CS_c + community + PR_c + CS_c:community", "CS_c", "H11"),
    "SCB<-CS:community": ("SCB_c", "CS_c + community + PR_c + CS_c:community", "CS_c:community", "H11"),
    "CDC<-CS": ("CDC_c", "CS_c + community + symbolic + PR_c + CS_c:community", "CS_c", "H12"),
    "CDC<-CS:community": ("CDC_c", "CS_c + community + symbolic + PR_c + CS_c:community", "CS_c:community", "H12"),
    "BSE<-int:sac": ("BSE_c", "demkt_intensity + demkt_sacrifice + demkt_intensity:demkt_sacrifice + CS_c + PR_c", "demkt_intensity:demkt_sacrifice", "H13"),
    # conditional effect of demarketing intensity at ZERO sacrifice: H13 predicts this is
    # null-to-negative (the sufficiency-washing penalty), not positive
    "BSE<-intensity|no_sacrifice": ("BSE_c", "demkt_intensity + demkt_sacrifice + demkt_intensity:demkt_sacrifice + CS_c + PR_c", "demkt_intensity", "H13"),
    "SPS<-CS": ("SPS_c", "CS_c + growth_endorse + CE_c + CS_c:growth_endorse", "CS_c", "H14"),
    "SPS<-CS:growth_endorse": ("SPS_c", "CS_c + growth_endorse + CE_c + CS_c:growth_endorse", "CS_c:growth_endorse", "H14"),
    # --- Total stringency profile on CS (reduced form, for the inverted-U) ---
    "CS<-stringency": ("CS_c", "stringency + I(stringency**2) + precarity + stringency:precarity + agency + locus + frame + symbolic", "stringency", "H7"),
    "CS<-stringency2": ("CS_c", "stringency + I(stringency**2) + precarity + stringency:precarity + agency + locus + frame + symbolic", "I(stringency ** 2)", "H7"),
}

# Predicted sign for each focal path (used for directional power)
PREDICTED_SIGN = {
    "PA<-agency": +1, "PA<-locus:collectivism": +1, "CE<-locus": +1, "CE<-locus:collectivism": +1,
    "RIA<-PA": +1, "RIA<-frame": +1, "RSV<-RIA:symbolic": +1,
    "AD<-agency": -1, "AD<-frame": -1, "AD<-stringency2": +1, "AD<-stringency:precarity": +1,
    "PR<-AD": +1, "PR<-AD:symbolic": +1,
    "CS<-RIA": +1, "CS<-RSV": +1, "CS<-PR": -1, "CS<-AD": -1, "CS<-RIA:symbolic": +1,
    "SCB<-CS": +1, "SCB<-CS:community": +1, "CDC<-CS": -1, "CDC<-CS:community": -1,
    # 0 denotes a PREDICTED NULL: H13 holds that demarketing intensity confers no brand-equity
    # benefit in the absence of a credible sacrifice signal. A predicted null is evaluated by
    # failure to reject, not by sign, and is reported alongside an equivalence assessment.
    "BSE<-int:sac": +1, "BSE<-intensity|no_sacrifice": 0,
    "SPS<-CS": +1, "SPS<-CS:growth_endorse": -1,
    "CS<-stringency": +1, "CS<-stringency2": -1,
}


def _unique_models() -> dict[str, tuple[str, str]]:
    """Collapse EQUATIONS to the set of distinct regressions that must be run."""
    models = {}
    for _, (dv, rhs, _, _) in EQUATIONS.items():
        models[f"{dv} ~ {rhs}"] = (dv, rhs)
    return models


def fit_structural(df: pd.DataFrame) -> pd.DataFrame:
    """
    Estimate every equation in the canonical specification.

    Returns a tidy DataFrame with one row per focal path:
    path, hypothesis, dv, term, b, se, t, p, r2_of_equation, n.
    """
    fitted = {}
    for formula, (dv, rhs) in _unique_models().items():
        fitted[formula] = smf.ols(formula, data=df).fit()

    rows = []
    for path, (dv, rhs, term, hyp) in EQUATIONS.items():
        res = fitted[f"{dv} ~ {rhs}"]
        # patsy normalises interaction term names; find the matching parameter
        key = _match_term(res.params.index, term)
        rows.append({
            "path": path, "hypothesis": hyp, "dv": dv, "term": key,
            "b": res.params[key], "se": res.bse[key],
            "t": res.tvalues[key], "p": res.pvalues[key],
            "ci_lo": res.conf_int().loc[key, 0], "ci_hi": res.conf_int().loc[key, 1],
            "r2": res.rsquared, "n": int(res.nobs),
            "predicted_sign": PREDICTED_SIGN.get(path, 0),
        })
    out = pd.DataFrame(rows)
    predicted_null = out["predicted_sign"] == 0
    out["sign_ok"] = np.where(predicted_null, True,
                              np.sign(out["b"]) == out["predicted_sign"])
    out["supported"] = np.where(predicted_null,
                                out["p"] >= 0.05,                     # fail to reject the null
                                out["sign_ok"] & (out["p"] < 0.05))
    out["test_type"] = np.where(predicted_null, "predicted null", "directional")
    return out


def _match_term(index, term: str) -> str:
    """Resolve a requested term name against patsy's parameter naming."""
    if term in index:
        return term
    canon = term.replace(" ", "")
    for name in index:
        if name.replace(" ", "") == canon:
            return name
    # interaction terms may be reordered by patsy
    if ":" in canon:
        want = set(canon.split(":"))
        for name in index:
            if ":" in name and set(name.replace(" ", "").split(":")) == want:
                return name
    raise KeyError(f"Could not match term {term!r} in {list(index)}")


def equation_r2(df: pd.DataFrame) -> pd.DataFrame:
    """R^2 for each distinct structural equation (endogenous-variable explanatory power)."""
    rows = []
    for formula, (dv, rhs) in _unique_models().items():
        res = smf.ols(formula, data=df).fit()
        rows.append({"equation": formula, "dv": dv, "r2": res.rsquared,
                     "adj_r2": res.rsquared_adj, "n": int(res.nobs)})
    return pd.DataFrame(rows).sort_values("dv").reset_index(drop=True)
