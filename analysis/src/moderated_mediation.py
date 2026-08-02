"""
Bootstrapped mediation, serial mediation, and moderated mediation for the SSM.

Implements:
  * H1/H4  serial indirect effect  agency -> PA -> RIA -> CS  (and the RSV branch)
  * H2     moderated mediation     locus  -> CE  -> CS,  moderated by collectivism (stage 1)
  * H3     dual-path frame effect  frame  -> {RIA(+), AD(-)} -> CS
  * H8/H9  moderated mediation     stringency -> AD -> PR -> CS, moderated by precarity
  * H10    double moderation       symbolic amplifies BOTH RIA->CS and AD->PR
  * H11    moderated translation   CS -> SCB, moderated by community
  * H12    leakage                 CS -> CDC, moderated by community
  * H14    citizen spillover       CS -> SPS, moderated by growth-paradigm endorsement

Inference: nonparametric percentile bootstrap (5,000 resamples) on the *entire system*, so that
products of coefficients are resampled jointly. Design matrices are built once with patsy and
solved with lstsq inside the loop, which makes 5,000 x 8 equations tractable.

Also provides the index of moderated mediation (Hayes 2015) and Johnson-Neyman regions of
significance for the conditional effects.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import patsy
from scipy import stats

from config import ALPHA, BOOT_REPS, SEED, TAB_DIR

# Equations needed to assemble every effect below.
_SYS = {
    "PA":  "PA_c  ~ agency + locus + frame + stringency + precarity + locus:collectivism",
    "CE":  "CE_c  ~ locus + community + frame + locus:collectivism",
    "RIA": "RIA_c ~ PA_c + frame + CE_c + growth_endorse + stringency",
    "RSV": "RSV_c ~ RIA_c + symbolic + RIA_c:symbolic",
    "AD":  "AD_c  ~ agency + frame + stringency + I(stringency**2) + precarity + symbolic + stringency:precarity",
    "PR":  "PR_c  ~ AD_c + agency + symbolic + AD_c:symbolic",
    "CS":  "CS_c  ~ RIA_c + RSV_c + CE_c + PR_c + AD_c + RIA_c:symbolic + symbolic",
    "SCB": "SCB_c ~ CS_c + community + PR_c + CS_c:community",
    "CDC": "CDC_c ~ CS_c + community + symbolic + PR_c + CS_c:community",
    "SPS": "SPS_c ~ CS_c + growth_endorse + CE_c + CS_c:growth_endorse",
}


class System:
    """Pre-compiled linear system that can be refit fast on bootstrap resamples."""

    def __init__(self, df: pd.DataFrame):
        self.n = len(df)
        self._y, self._X, self._names = {}, {}, {}
        for key, formula in _SYS.items():
            y, X = patsy.dmatrices(formula, data=df, return_type="dataframe")
            self._y[key] = y.to_numpy().ravel()
            self._X[key] = X.to_numpy()
            self._names[key] = list(X.columns)

    def fit(self, idx: np.ndarray | None = None) -> dict[str, dict[str, float]]:
        out = {}
        for key in _SYS:
            X, y = self._X[key], self._y[key]
            if idx is not None:
                X, y = X[idx], y[idx]
            beta, *_ = np.linalg.lstsq(X, y, rcond=None)
            out[key] = dict(zip(self._names[key], beta))
        return out

    def term(self, key: str, term: str) -> str:
        canon = term.replace(" ", "")
        for nm in self._names[key]:
            if nm.replace(" ", "") == canon:
                return nm
        if ":" in canon:
            want = set(canon.split(":"))
            for nm in self._names[key]:
                if ":" in nm and set(nm.replace(" ", "").split(":")) == want:
                    return nm
        raise KeyError(f"{term!r} not in equation {key}: {self._names[key]}")


# --------------------------------------------------------------------------------------
# Effect definitions: each is a function of the fitted coefficient dict
# --------------------------------------------------------------------------------------
def _g(c, key, sysobj, term):
    return c[key][sysobj.term(key, term)]


def build_effects(sysobj: System, moderator_levels: dict[str, tuple[float, float, float]]):
    """
    Returns a dict effect_name -> callable(coef_dict) -> float.
    moderator_levels supplies (-1SD, mean, +1SD) values for each moderator (standardized: -1,0,1).
    """
    E = {}
    G = lambda c, k, t: _g(c, k, sysobj, t)

    # ---- H1/H4: agency -> PA -> RIA -> CS (serial), plus RIA -> RSV -> CS branch ----
    E["H4_serial_agency_PA_RIA_CS"] = lambda c: (
        G(c, "PA", "agency") * G(c, "RIA", "PA_c") * G(c, "CS", "RIA_c"))
    E["H4_serial_agency_PA_RIA_RSV_CS"] = lambda c: (
        G(c, "PA", "agency") * G(c, "RIA", "PA_c") * G(c, "RSV", "RIA_c") * G(c, "CS", "RSV_c"))
    E["H1_total_routeA_agency_to_CS"] = lambda c: (
        E["H4_serial_agency_PA_RIA_CS"](c) + E["H4_serial_agency_PA_RIA_RSV_CS"](c))
    # ---- H1: agency also suppresses Route B: agency -> AD -> PR -> CS ----
    E["H1_routeB_agency_AD_PR_CS"] = lambda c: (
        G(c, "AD", "agency") * G(c, "PR", "AD_c") * G(c, "CS", "PR_c"))
    E["H1_routeB_agency_AD_CS"] = lambda c: (
        G(c, "AD", "agency") * G(c, "CS", "AD_c"))
    E["H1_net_agency_to_CS"] = lambda c: (
        E["H1_total_routeA_agency_to_CS"](c)
        + E["H1_routeB_agency_AD_PR_CS"](c) + E["H1_routeB_agency_AD_CS"](c))

    # ---- H3: dual-path frame effect ----
    E["H3_frame_via_RIA"] = lambda c: G(c, "RIA", "frame") * G(c, "CS", "RIA_c")
    E["H3_frame_via_AD_PR"] = lambda c: G(c, "AD", "frame") * G(c, "PR", "AD_c") * G(c, "CS", "PR_c")
    E["H3_frame_via_AD_direct"] = lambda c: G(c, "AD", "frame") * G(c, "CS", "AD_c")
    E["H3_frame_net"] = lambda c: (E["H3_frame_via_RIA"](c) + E["H3_frame_via_AD_PR"](c)
                                   + E["H3_frame_via_AD_direct"](c))

    # ---- H2: locus -> CE -> CS moderated by collectivism ----
    for lab, w in zip(("lowColl", "meanColl", "highColl"), moderator_levels["collectivism"]):
        E[f"H2_cond_locus_CE_CS@{lab}"] = (
            lambda c, w=w: (G(c, "CE", "locus") + G(c, "CE", "locus:collectivism") * w)
            * G(c, "CS", "CE_c"))
    E["H2_index_modmed"] = lambda c: G(c, "CE", "locus:collectivism") * G(c, "CS", "CE_c")

    # ---- H8/H9: stringency -> AD -> PR -> CS moderated by precarity (evaluated at S = .50) ----
    S_EVAL = 0.50
    for lab, w in zip(("lowPrec", "meanPrec", "highPrec"), moderator_levels["precarity"]):
        E[f"H9_cond_stringency_AD_PR_CS@{lab}"] = (
            lambda c, w=w: (G(c, "AD", "stringency")
                            + 2 * G(c, "AD", "I(stringency ** 2)") * S_EVAL
                            + G(c, "AD", "stringency:precarity") * w)
            * (G(c, "PR", "AD_c") * G(c, "CS", "PR_c") + G(c, "CS", "AD_c")))
    E["H9_index_modmed"] = lambda c: (
        G(c, "AD", "stringency:precarity")
        * (G(c, "PR", "AD_c") * G(c, "CS", "PR_c") + G(c, "CS", "AD_c")))

    # ---- H10: symbolic polarizes both routes ----
    for lab, w in zip(("lowSym", "highSym"), (-1.0, 1.0)):
        E[f"H10_RIA_to_CS@{lab}"] = lambda c, w=w: (
            G(c, "CS", "RIA_c") + G(c, "CS", "RIA_c:symbolic") * w)
        E[f"H10_AD_to_PR@{lab}"] = lambda c, w=w: (
            G(c, "PR", "AD_c") + G(c, "PR", "AD_c:symbolic") * w)
    E["H10_polarization_gap_RouteA"] = lambda c: 2 * G(c, "CS", "RIA_c:symbolic")
    E["H10_polarization_gap_RouteB"] = lambda c: 2 * G(c, "PR", "AD_c:symbolic")

    # ---- H11: CS -> SCB moderated by community ----
    for lab, w in zip(("lowComm", "meanComm", "highComm"), moderator_levels["community"]):
        E[f"H11_cond_CS_to_SCB@{lab}"] = lambda c, w=w: (
            G(c, "SCB", "CS_c") + G(c, "SCB", "CS_c:community") * w)
    E["H11_index_mod"] = lambda c: G(c, "SCB", "CS_c:community")

    # ---- H12: CS -> CDC (leakage) moderated by community ----
    for lab, w in zip(("lowComm", "meanComm", "highComm"), moderator_levels["community"]):
        E[f"H12_cond_CS_to_CDC@{lab}"] = lambda c, w=w: (
            G(c, "CDC", "CS_c") + G(c, "CDC", "CS_c:community") * w)
    E["H12_index_mod"] = lambda c: G(c, "CDC", "CS_c:community")

    # ---- H14: CS -> SPS moderated by growth endorsement ----
    for lab, w in zip(("lowGrowth", "meanGrowth", "highGrowth"), moderator_levels["growth_endorse"]):
        E[f"H14_cond_CS_to_SPS@{lab}"] = lambda c, w=w: (
            G(c, "SPS", "CS_c") + G(c, "SPS", "CS_c:growth_endorse") * w)
    E["H14_index_mod"] = lambda c: G(c, "SPS", "CS_c:growth_endorse")

    return E


def bootstrap_effects(df: pd.DataFrame, reps: int = BOOT_REPS, seed: int = SEED) -> pd.DataFrame:
    sysobj = System(df)
    mods = {m: (-1.0, 0.0, 1.0) for m in ("collectivism", "precarity", "community", "growth_endorse")}
    effects = build_effects(sysobj, mods)

    point = sysobj.fit()
    est = {k: f(point) for k, f in effects.items()}

    rng = np.random.default_rng(seed)
    n = len(df)
    draws = {k: np.empty(reps) for k in effects}
    for b in range(reps):
        idx = rng.integers(0, n, n)
        c = sysobj.fit(idx)
        for k, f in effects.items():
            draws[k][b] = f(c)

    rows = []
    for k in effects:
        d = draws[k]
        lo, hi = np.percentile(d, [100 * ALPHA / 2, 100 * (1 - ALPHA / 2)])
        rows.append({"effect": k, "estimate": est[k], "boot_se": d.std(ddof=1),
                     "ci_lo": lo, "ci_hi": hi,
                     "excludes_zero": bool((lo > 0) or (hi < 0)),
                     "boot_p_two_sided": 2 * min((d <= 0).mean(), (d >= 0).mean())})
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------------------
# Johnson-Neyman
# --------------------------------------------------------------------------------------
def johnson_neyman(df: pd.DataFrame, dv: str, focal: str, mod: str,
                   covars: list[str] | None = None,
                   grid: np.ndarray | None = None) -> pd.DataFrame:
    """
    Region-of-significance analysis for the conditional effect of `focal` on `dv` across `mod`.
    Returns the conditional effect, SE, t, p and significance flag across a grid of moderator
    values, plus the JN boundary/boundaries where p crosses .05.
    """
    import statsmodels.formula.api as smf
    covars = covars or []
    rhs = " + ".join([focal, mod, f"{focal}:{mod}"] + covars)
    res = smf.ols(f"{dv} ~ {rhs}", data=df).fit()
    b1 = res.params[focal]
    names = [nm for nm in res.params.index if ":" in nm
             and set(nm.split(":")) == {focal, mod}]
    b3n = names[0]
    b3 = res.params[b3n]
    V = res.cov_params()
    v11, v33, v13 = V.loc[focal, focal], V.loc[b3n, b3n], V.loc[focal, b3n]
    dfree = res.df_resid
    tcrit = stats.t.ppf(1 - ALPHA / 2, dfree)

    grid = np.linspace(df[mod].quantile(0.01), df[mod].quantile(0.99), 121) if grid is None else grid
    eff = b1 + b3 * grid
    se = np.sqrt(np.maximum(v11 + 2 * grid * v13 + grid ** 2 * v33, 1e-18))
    t = eff / se
    p = 2 * (1 - stats.t.cdf(np.abs(t), dfree))
    out = pd.DataFrame({"mod_value": grid, "effect": eff, "se": se, "t": t, "p": p,
                        "significant": p < ALPHA})

    # analytic JN boundaries: solve (b1+b3w)^2 = tcrit^2 * var(w)
    A = b3 ** 2 - tcrit ** 2 * v33
    B = 2 * (b1 * b3 - tcrit ** 2 * v13)
    C = b1 ** 2 - tcrit ** 2 * v11
    roots = []
    if abs(A) > 1e-14:
        disc = B ** 2 - 4 * A * C
        if disc >= 0:
            roots = sorted([(-B - np.sqrt(disc)) / (2 * A), (-B + np.sqrt(disc)) / (2 * A)])
    out.attrs["jn_boundaries"] = roots
    out.attrs["b_focal"] = b1
    out.attrs["b_interaction"] = b3
    out.attrs["p_interaction"] = res.pvalues[b3n]
    return out


def run(df: pd.DataFrame, reps: int = BOOT_REPS) -> dict:
    print(f"[Study 2] Bootstrapping the mediation system ({reps} resamples) ...")
    eff = bootstrap_effects(df, reps=reps)
    eff.to_csv(f"{TAB_DIR}/t7_bootstrap_effects.csv", index=False)
    print(eff.round(4).to_string(index=False))

    print("\n[Study 2] Johnson-Neyman: conditional effect of stringency on CS across precarity")
    jn = johnson_neyman(df, "CS_c", "stringency", "precarity",
                        covars=["agency", "locus", "frame", "symbolic"])
    jn.to_csv(f"{TAB_DIR}/t8_johnson_neyman_stringency_precarity.csv", index=False)
    print(f"  interaction b = {jn.attrs['b_interaction']:.4f}, p = {jn.attrs['p_interaction']:.2e}")
    print(f"  JN boundaries (precarity, z-units): "
          f"{[round(r, 3) for r in jn.attrs['jn_boundaries']]}")
    sig_neg = jn[(jn['significant']) & (jn['effect'] < 0)]
    if len(sig_neg):
        print(f"  stringency significantly REDUCES chosen sufficiency above precarity = "
              f"{sig_neg['mod_value'].min():.3f} z")

    return {"effects": eff, "jn": jn}
