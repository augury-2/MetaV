"""
Data-generating process for the Sufficiency-Sovereignty Model (SSM).

This module IS the formal statement of the micro theory. Each function corresponds to one
block of the structural model in ../../model/constructs.md, section 3.

Key structural feature (P7/P8): the effect of limit stringency S on Chosen Sufficiency is the
difference between a CONCAVE-SATURATING Route A gain and a CONVEX-ACCELERATING Route B cost:

    RouteA_gain(S)  = alpha * (1 - exp(-theta * S))                     [identity affirmation]
    RouteB_cost(S)  = b_lin * S + (beta0 + beta1 * precarity) * S^2     [anticipated deprivation]

Consequently d(CS)/dS = 0 has an interior solution S* (the FLIP POINT) with dS*/d(precarity) < 0.
`flip_point()` solves this in closed/numeric form so that the simulated peak can be validated
against the analytic peak.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.optimize import brentq

from config import (ADJACENT_R, CMV_LOADING, COUNTRIES, COUNTRY_PARAMS,
                    CROSS_LOADINGS, LIKERT_MAX, LIKERT_MIN, MEASURES,
                    N_PER_COUNTRY, P, RESID_CORR, SEED)


# ======================================================================================
# Analytic properties of the theory
# ======================================================================================
def route_a_gain(S: np.ndarray | float) -> np.ndarray | float:
    """Concave-saturating identity-affirmation gain from limit stringency."""
    return P["RIA_sat_alpha"] * (1.0 - np.exp(-P["RIA_sat_theta"] * np.asarray(S, dtype=float)))


def route_b_curvature(precarity: np.ndarray | float = 0.0) -> np.ndarray | float:
    """Curvature of the deprivation cost. Floored so the cost is always convex."""
    curv = P["AD_str_quad_base"] + P["AD_str_quad_precarity"] * np.asarray(precarity, dtype=float)
    return np.maximum(curv, P["AD_str_quad_min"])


def route_b_cost(S: np.ndarray | float, precarity: np.ndarray | float = 0.0) -> np.ndarray | float:
    """Convex, precarity-amplified deprivation cost from limit stringency."""
    S = np.asarray(S, dtype=float)
    return P["AD_str_lin"] * S + route_b_curvature(precarity) * S ** 2


def _cs_transmission() -> tuple[float, float]:
    """
    Total standardized transmission coefficients from (Route A gain, Route B cost) to CS.

    Route A: RIA -> CS directly, plus RIA -> RSV -> CS.
    Route B: AD -> CS directly, plus AD -> PR -> CS.
    """
    w_a = P["CS_RIA"] + P["RSV_RIA"] * P["CS_RSV"]
    w_b = abs(P["CS_AD"]) + P["PR_AD"] * abs(P["CS_PR"])
    return w_a, w_b


def cs_stringency_profile(S: np.ndarray | float, precarity: float = 0.0) -> np.ndarray | float:
    """Net effect of stringency on latent CS, holding all else at reference values."""
    w_a, w_b = _cs_transmission()
    # PA also declines linearly in S and feeds RIA -> CS
    pa_channel = P["PA_stringency"] * P["RIA_PA"] * w_a
    return (w_a * route_a_gain(S)
            + pa_channel * np.asarray(S, dtype=float)
            - w_b * route_b_cost(S, precarity))


def flip_point(precarity: float = 0.0) -> float:
    """
    Analytic flip point S*: the stringency at which the marginal identity gain is exactly
    offset by the marginal deprivation cost. Returns the interior maximizer of
    cs_stringency_profile on (0, 1), or a boundary value if no interior optimum exists.
    """
    w_a, w_b = _cs_transmission()
    alpha, theta = P["RIA_sat_alpha"], P["RIA_sat_theta"]
    b_lin = P["AD_str_lin"]
    curv = float(route_b_curvature(precarity))
    pa_channel = P["PA_stringency"] * P["RIA_PA"] * w_a

    def deriv(S: float) -> float:
        return (w_a * alpha * theta * np.exp(-theta * S)
                + pa_channel
                - w_b * (b_lin + 2.0 * curv * S))

    lo, hi = 1e-6, 1.0
    if deriv(lo) <= 0:
        return 0.0
    if deriv(hi) >= 0:
        return 1.0
    return float(brentq(deriv, lo, hi, xtol=1e-8))


# ======================================================================================
# Latent structural simulation
# ======================================================================================
def _rand_normal(rng, n, mu=0.0, sd=1.0):
    return rng.normal(mu, sd, n)


def simulate_latents(n: int,
                     rng: np.random.Generator,
                     *,
                     country: str | None = None,
                     agency=None, locus=None, frame=None, stringency=None,
                     symbolic=None, demkt_intensity=None, demkt_sacrifice=None,
                     precarity_mu: float | None = None,
                     collectivism_mu: float | None = None,
                     growth_endorse_mu: float | None = None,
                     community_mu: float | None = None) -> pd.DataFrame:
    """
    Simulate the latent structural model for n respondents.

    Any design variable passed as an array is treated as experimentally fixed; otherwise it is
    drawn from its population distribution (survey mode).
    """
    cp = COUNTRY_PARAMS.get(country, {}) if country else {}
    precarity_mu = cp.get("precarity_mu", 0.0) if precarity_mu is None else precarity_mu
    collectivism_mu = cp.get("collectivism_mu", 0.0) if collectivism_mu is None else collectivism_mu
    growth_endorse_mu = cp.get("growth_endorse_mu", 0.0) if growth_endorse_mu is None else growth_endorse_mu
    community_mu = cp.get("community_mu", 0.0) if community_mu is None else community_mu

    d = pd.DataFrame(index=np.arange(n))

    # ---- Limit architecture (design space) ----
    d["agency"] = rng.binomial(1, 0.5, n) if agency is None else np.asarray(agency, dtype=float)
    d["locus"] = rng.binomial(1, 0.5, n) if locus is None else np.asarray(locus, dtype=float)
    d["frame"] = rng.binomial(1, 0.5, n) if frame is None else np.asarray(frame, dtype=float)
    d["stringency"] = rng.uniform(0.05, 0.95, n) if stringency is None else np.asarray(stringency, dtype=float)

    # ---- Firm-side demarketing cues ----
    # These are administered as a 3 x 3 VIGNETTE within the survey (respondents evaluate a firm
    # profile with orthogonally varied demarketing intensity and sacrifice signal) rather than as
    # continuous self-reports. Orthogonal discrete levels are what a competent survey design would
    # use, and they condition the intensity x sacrifice product term far better than continuous
    # measures, whose product is badly collinear with its constituents.
    vignette_levels = np.array([0.15, 0.50, 0.85])
    d["demkt_intensity"] = (rng.choice(vignette_levels, n) if demkt_intensity is None
                            else np.asarray(demkt_intensity, dtype=float))
    d["demkt_sacrifice"] = (rng.choice(vignette_levels, n) if demkt_sacrifice is None
                            else np.asarray(demkt_sacrifice, dtype=float))

    # ---- Moderators ----
    d["precarity"] = _rand_normal(rng, n, precarity_mu, 1.0)
    d["collectivism"] = _rand_normal(rng, n, collectivism_mu, 1.0)
    d["growth_endorse"] = _rand_normal(rng, n, growth_endorse_mu, 1.0)
    d["community"] = _rand_normal(rng, n, community_mu, 1.0)
    if symbolic is None:
        # half the sample assigned to a symbolically intense category (apparel), half to a
        # low-symbolism utility category (household energy)
        d["symbolic"] = rng.binomial(1, 0.5, n) * 2.0 - 1.0
    else:
        d["symbolic"] = np.asarray(symbolic, dtype=float)

    S = d["stringency"].to_numpy()
    prec = d["precarity"].to_numpy()
    sym = d["symbolic"].to_numpy()

    # Shared appraisal disturbance: makes routes correlated yet separable (P6)
    u = _rand_normal(rng, n, 0.0, P["route_shared_sd"])

    # ---- Route A ----
    d["PA"] = (P["PA_agency"] * d["agency"]
               + P["PA_locus"] * d["locus"]
               + P["PA_frame"] * d["frame"]
               + P["PA_stringency"] * S
               + P["PA_precarity"] * d["precarity"]
               + P["PA_locus_x_collectivism"] * d["locus"] * d["collectivism"]
               + u
               + _rand_normal(rng, n, 0, P["sd_PA"]))

    d["CE"] = (P["CE_locus"] * d["locus"]
               + P["CE_locus_x_collectivism"] * d["locus"] * d["collectivism"]
               + P["CE_community"] * d["community"]
               + P["CE_frame"] * d["frame"]
               + _rand_normal(rng, n, 0, P["sd_CE"]))

    d["RIA"] = (P["RIA_PA"] * d["PA"]
                + P["RIA_frame"] * d["frame"]
                + P["RIA_CE"] * d["CE"]
                + P["RIA_growth_endorse"] * d["growth_endorse"]
                + route_a_gain(S)                      # saturating identity gain
                + _rand_normal(rng, n, 0, P["sd_RIA"]))

    d["RSV"] = (P["RSV_RIA"] * d["RIA"]
                + P["RSV_symbolic"] * sym
                + P["RSV_RIA_x_symbolic"] * d["RIA"] * sym
                + _rand_normal(rng, n, 0, P["sd_RSV"]))

    # ---- Route B ----
    d["AD"] = (P["AD_agency"] * d["agency"]
               + P["AD_frame"] * d["frame"]
               + P["AD_precarity"] * d["precarity"]
               + P["AD_symbolic"] * sym
               + route_b_cost(S, prec)                 # convex, precarity-amplified
               - u                                     # shared disturbance, opposite sign
               + _rand_normal(rng, n, 0, P["sd_AD"]))

    d["PR"] = (P["PR_AD"] * d["AD"]
               + P["PR_agency"] * d["agency"]
               + P["PR_AD_x_symbolic"] * d["AD"] * sym
               + _rand_normal(rng, n, 0, P["sd_PR"]))

    # ---- Net resultant: Chosen Sufficiency ----
    d["CS"] = (P["CS_RIA"] * d["RIA"]
               + P["CS_RSV"] * d["RSV"]
               + P["CS_CE"] * d["CE"]
               + P["CS_RIA_x_symbolic"] * d["RIA"] * sym
               + P["CS_PR"] * d["PR"]
               + P["CS_AD"] * d["AD"]
               + _rand_normal(rng, n, 0, P["sd_CS"]))

    # ---- Outcomes ----
    d["SCB"] = (P["SCB_CS"] * d["CS"]
                + P["SCB_CS_x_community"] * d["CS"] * d["community"]
                + P["SCB_PR"] * d["PR"]
                + _rand_normal(rng, n, 0, P["sd_SCB"]))

    d["BSE"] = (P["BSE_CS"] * d["CS"]
                + P["BSE_demkt_intensity"] * d["demkt_intensity"]
                + P["BSE_demkt_sacrifice"] * d["demkt_sacrifice"]
                + P["BSE_int_x_sac"] * d["demkt_intensity"] * d["demkt_sacrifice"]
                + P["BSE_PR"] * d["PR"]
                + _rand_normal(rng, n, 0, P["sd_BSE"]))

    d["SPS"] = (P["SPS_CS"] * d["CS"]
                + P["SPS_CS_x_growth_endorse"] * d["CS"] * d["growth_endorse"]
                + P["SPS_CE"] * d["CE"]
                + _rand_normal(rng, n, 0, P["sd_SPS"]))

    d["CDC"] = (P["CDC_CS"] * d["CS"]
                + P["CDC_CS_x_community"] * d["CS"] * d["community"]
                + P["CDC_symbolic"] * sym
                + P["CDC_PR"] * d["PR"]
                + _rand_normal(rng, n, 0, P["sd_CDC"]))

    # ---- Adjacent constructs for discriminant validity ----
    cs_z = (d["CS"] - d["CS"].mean()) / d["CS"].std()
    for name, r in ADJACENT_R.items():
        d[name] = r * cs_z + np.sqrt(max(1e-9, 1 - r ** 2)) * _rand_normal(rng, n)

    if country:
        d["country"] = country
    return d


# ======================================================================================
# Measurement: latent -> observed 7-point items
# ======================================================================================
def add_items(latents: pd.DataFrame, rng: np.random.Generator,
              constructs: list[str] | None = None,
              discretize: bool = True) -> pd.DataFrame:
    """
    Generate reflective 7-point Likert indicators for each construct in MEASURES.

    IMPORTANT: must be called ONCE on the fully assembled dataset. Latent scores are
    standardized against the moments of the frame passed in, so calling this separately per
    experimental cell or per country would standardize away exactly the between-cell mean
    differences the design is meant to create.
    """
    out = latents.copy()
    constructs = constructs or list(MEASURES.keys())
    constructs = [c for c in constructs if c in latents.columns]
    n = len(latents)

    # standardized latent scores for every construct (needed for cross-loadings)
    z = {}
    for c in constructs:
        eta = latents[c].to_numpy()
        z[c] = (eta - eta.mean()) / (eta.std() + 1e-12)

    cmv = rng.normal(0, 1, n)                      # common-method nuisance factor
    raw: dict[str, np.ndarray] = {}
    for c in constructs:
        for k, lam in enumerate(MEASURES[c]["loadings"], start=1):
            resid_sd = np.sqrt(max(1e-6, 1.0 - lam ** 2))
            raw[f"{c}{k}"] = lam * z[c] + CMV_LOADING * cmv + rng.normal(0, resid_sd, n)

    # minor cross-loadings
    for c, k, src, load in CROSS_LOADINGS:
        key = f"{c}{k}"
        if key in raw and src in z:
            raw[key] = raw[key] + load * z[src]

    # correlated residuals via shared item-pair nuisance factors
    for c, ka, kb, rho in RESID_CORR:
        a, b = f"{c}{ka}", f"{c}{kb}"
        if a in raw and b in raw:
            shared = rng.normal(0, np.sqrt(abs(rho)), n)
            raw[a] = raw[a] + shared
            raw[b] = raw[b] + np.sign(rho) * shared

    for key, x in raw.items():
        x = (x - x.mean()) / (x.std() + 1e-12)     # rescale after contamination
        x = 4.0 + 1.15 * x                          # 7-point scale centred at 4
        if discretize:
            x = np.clip(np.rint(x), LIKERT_MIN, LIKERT_MAX)
        out[key] = x
    return out


def composites(df: pd.DataFrame, constructs: list[str] | None = None,
               standardize: bool = True) -> pd.DataFrame:
    """Mean-score composites from the generated items (used for moderation analyses)."""
    out = df.copy()
    constructs = constructs or list(MEASURES.keys())
    for c in constructs:
        cols = [f"{c}{k}" for k in range(1, MEASURES[c]["n_items"] + 1)]
        cols = [col for col in cols if col in df.columns]
        if not cols:
            continue
        s = df[cols].mean(axis=1)
        out[f"{c}_c"] = (s - s.mean()) / s.std() if standardize else s
    return out


# ======================================================================================
# Study-specific datasets
# ======================================================================================
def _assemble(frames: list[pd.DataFrame], rng: np.random.Generator) -> pd.DataFrame:
    """Concatenate latent blocks, then generate items ONCE so between-block variance survives."""
    df = pd.concat(frames, ignore_index=True)
    df = add_items(df, rng)
    return composites(df)


def study2_survey(seed: int = SEED) -> pd.DataFrame:
    """Cross-national survey sample (Study 2): 4 countries x N_PER_COUNTRY."""
    rng = np.random.default_rng(seed)
    frames = [simulate_latents(N_PER_COUNTRY, rng, country=c) for c in COUNTRIES]
    return _assemble(frames, rng)


def study3a_factorial(seed: int = SEED + 1, n_per_cell: int = 150) -> pd.DataFrame:
    """2 (agency) x 2 (locus) x 2 (frame) between-subjects experiment, stringency held at 0.35."""
    rng = np.random.default_rng(seed)
    frames = []
    for a in (0, 1):
        for l in (0, 1):
            for f in (0, 1):
                frames.append(simulate_latents(
                    n_per_cell, rng,
                    agency=np.full(n_per_cell, a),
                    locus=np.full(n_per_cell, l),
                    frame=np.full(n_per_cell, f),
                    stringency=np.full(n_per_cell, 0.35),
                ))
    return _assemble(frames, rng)


def study3b_stringency(seed: int = SEED + 2, n: int = 1400,
                       levels: list[float] | None = None) -> pd.DataFrame:
    """Continuous-dose stringency experiment used to locate the flip point (P7/P8)."""
    from config import EXP3B_LEVELS
    levels = levels or EXP3B_LEVELS
    rng = np.random.default_rng(seed)
    per = n // len(levels)
    frames = []
    for s in levels:
        frames.append(simulate_latents(
            per, rng,
            agency=np.ones(per),           # chosen limits throughout, to isolate dose
            locus=rng.binomial(1, 0.5, per),
            frame=np.ones(per),
            stringency=np.full(per, s),
        ))
    return _assemble(frames, rng)


def study3c_sacrifice(seed: int = SEED + 3, n_per_cell: int = 160) -> pd.DataFrame:
    """2 (demarketing intensity) x 2 (sacrifice signal) experiment on brand sufficiency equity."""
    rng = np.random.default_rng(seed)
    frames = []
    for di in (0.15, 0.85):
        for ds in (0.15, 0.85):
            frames.append(simulate_latents(
                n_per_cell, rng,
                stringency=np.full(n_per_cell, 0.35),
                demkt_intensity=np.full(n_per_cell, di),
                demkt_sacrifice=np.full(n_per_cell, ds),
            ))
    return _assemble(frames, rng)
