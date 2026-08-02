"""
Central configuration and the formal parameterization of the Sufficiency-Sovereignty Model (SSM).

Every parameter here corresponds to a named path in ../../model/constructs.md.
Values are calibrated to effect sizes typical of published consumer-psychology work
(standardized paths .15-.55; R^2 .25-.50) so that the synthetic data used in Studies 1-3
are realistic in magnitude. See MANUSCRIPT.md 'Data status' for the epistemic caveat.
"""
from __future__ import annotations

import os

SEED = 20260801

# --------------------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------------------
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
ANALYSIS_DIR = os.path.dirname(SRC_DIR)
OUT_DIR = os.path.join(ANALYSIS_DIR, "output")
TAB_DIR = os.path.join(OUT_DIR, "tables")
FIG_DIR = os.path.join(OUT_DIR, "figures")
for _d in (OUT_DIR, TAB_DIR, FIG_DIR):
    os.makedirs(_d, exist_ok=True)

# --------------------------------------------------------------------------------------
# Sample design (Study 2: cross-national survey)
# --------------------------------------------------------------------------------------
N_PER_COUNTRY = 400
COUNTRIES = ["DE", "FR", "SE", "BR"]  # Global North degrowth-active + Global South (Buen Vivir)

# Country-level distributional shifts (standardized units, applied to latent covariates).
# Rationale: Nordic/German-speaking Europe = lower precarity, higher institutional trust;
# Brazil = higher precarity, higher collectivism (postcolonial / Buen Vivir context).
COUNTRY_PARAMS = {
    "DE": {"precarity_mu": -0.35, "collectivism_mu": -0.30, "growth_endorse_mu": 0.10, "community_mu": 0.20},
    "FR": {"precarity_mu": -0.10, "collectivism_mu": -0.10, "growth_endorse_mu": -0.05, "community_mu": 0.15},
    "SE": {"precarity_mu": -0.50, "collectivism_mu": -0.20, "growth_endorse_mu": -0.15, "community_mu": 0.30},
    "BR": {"precarity_mu": 0.75, "collectivism_mu": 0.55, "growth_endorse_mu": 0.20, "community_mu": -0.05},
}

# --------------------------------------------------------------------------------------
# STRUCTURAL PARAMETERS
# --------------------------------------------------------------------------------------
# Route A: autonomy-identity (sovereignty-expanding)
P = {
    # --- Perceived Autonomy (PA) ---
    "PA_agency": 0.66,
    "PA_locus": 0.22,
    "PA_frame": 0.20,
    "PA_stringency": -0.35,
    "PA_precarity": -0.20,
    "PA_locus_x_collectivism": 0.13,       # H2 support at the autonomy stage
    # --- Collective Efficacy / norm reinforcement (CE) ---
    "CE_locus": 0.64,
    "CE_locus_x_collectivism": 0.21,       # H2 (mediated moderation)
    "CE_community": 0.24,
    "CE_frame": 0.10,
    # --- Restraint Identity Affirmation (RIA) ---
    "RIA_PA": 0.42,                        # H4 serial mediation second stage
    "RIA_frame": 0.27,
    "RIA_CE": 0.15,
    "RIA_growth_endorse": -0.17,           # M5 attenuation of the identity route
    # Route A gain in stringency is CONCAVE-SATURATING: a limit must be meaningful to
    # affirm identity, but affirmation saturates. This is the theoretical source of the
    # inverted-U (P7) together with the convex Route B cost below.
    "RIA_sat_alpha": 1.70,                 # alpha in alpha * (1 - exp(-theta * S))
    "RIA_sat_theta": 5.50,                 # theta: saturation rate
    # --- Restraint Signaling Value (RSV) ---
    "RSV_RIA": 0.47,
    "RSV_symbolic": 0.23,
    "RSV_RIA_x_symbolic": 0.17,            # H5
    # --- Anticipated Deprivation (AD) ---
    "AD_agency": -0.40,
    "AD_frame": -0.34,
    "AD_precarity": 0.29,
    "AD_symbolic": 0.16,
    # Route B cost in stringency is CONVEX (accelerating), and its curvature grows with
    # precarity -> the flip point S* falls as precarity rises (P8).
    "AD_str_lin": 0.35,
    "AD_str_quad_base": 1.90,              # beta0
    "AD_str_quad_precarity": 1.30,         # beta1 (precarity amplifies curvature)
    "AD_str_quad_min": 0.40,               # deprivation cost is always convex
    # --- Psychological Reactance (PR) ---
    "PR_AD": 0.52,
    "PR_agency": -0.19,
    "PR_AD_x_symbolic": 0.15,              # H10 polarization, Route B side
    # --- Chosen Sufficiency (CS) : the NET RESULTANT ---
    "CS_RIA": 0.34,
    "CS_RSV": 0.15,
    "CS_CE": 0.22,
    "CS_RIA_x_symbolic": 0.12,             # H10 polarization, Route A side
    "CS_PR": -0.27,
    "CS_AD": -0.15,
    # --- Outcomes ---
    "SCB_CS": 0.44,
    "SCB_CS_x_community": 0.18,            # H11 translation moderator
    "SCB_PR": -0.12,
    "BSE_CS": 0.26,
    "BSE_demkt_intensity": 0.05,           # near-zero main effect by design (H13)
    "BSE_demkt_sacrifice": 0.21,
    "BSE_int_x_sac": 0.30,                 # H13 the sufficiency-washing interaction
    "BSE_PR": -0.22,
    "SPS_CS": 0.40,
    "SPS_CS_x_growth_endorse": -0.16,      # H14
    "SPS_CE": 0.17,
    "CDC_CS": -0.28,
    "CDC_CS_x_community": -0.15,           # H12 community suppresses leakage
    "CDC_symbolic": 0.20,
    "CDC_PR": 0.24,
    # --- Residual SDs (govern R^2) ---
    "sd_PA": 0.72, "sd_CE": 0.74, "sd_RIA": 0.74, "sd_RSV": 0.76,
    "sd_AD": 0.72, "sd_PR": 0.78, "sd_CS": 0.55,
    "sd_SCB": 0.76, "sd_BSE": 0.80, "sd_SPS": 0.78, "sd_CDC": 0.84,
    # Shared appraisal-process disturbance: makes Route A and Route B correlated but
    # SEPARABLE (P6). Target r(PA, AD) ~ -.35, not ~ -1.
    "route_shared_sd": 0.30,
}

# --------------------------------------------------------------------------------------
# MEASUREMENT MODEL
# --------------------------------------------------------------------------------------
# Reflective constructs with 3-4 items, loadings in [.68, .87], 7-point Likert.
MEASURES = {
    "PA":  {"n_items": 4, "loadings": [0.84, 0.80, 0.77, 0.72]},
    "CE":  {"n_items": 3, "loadings": [0.82, 0.78, 0.74]},
    "RIA": {"n_items": 4, "loadings": [0.86, 0.83, 0.79, 0.75]},
    "RSV": {"n_items": 3, "loadings": [0.81, 0.77, 0.73]},
    "AD":  {"n_items": 4, "loadings": [0.85, 0.81, 0.78, 0.71]},
    "PR":  {"n_items": 4, "loadings": [0.87, 0.82, 0.78, 0.74]},
    "CS":  {"n_items": 4, "loadings": [0.85, 0.82, 0.80, 0.76]},
    "SCB": {"n_items": 3, "loadings": [0.83, 0.79, 0.75]},
    "BSE": {"n_items": 4, "loadings": [0.86, 0.83, 0.79, 0.74]},
    "SPS": {"n_items": 3, "loadings": [0.82, 0.78, 0.72]},
    "CDC": {"n_items": 3, "loadings": [0.79, 0.75, 0.70]},
    # Adjacent constructs, included for discriminant validity (Table 2)
    "VS":   {"n_items": 3, "loadings": [0.80, 0.76, 0.72]},   # voluntary simplicity
    "FRUG": {"n_items": 3, "loadings": [0.79, 0.75, 0.71]},   # frugality
    "MAT":  {"n_items": 3, "loadings": [0.82, 0.78, 0.74]},   # materialism
    "CR":   {"n_items": 3, "loadings": [0.81, 0.77, 0.73]},   # constrained restraint
}

# True latent correlations of CS with adjacent constructs (constructs.md Table 1.2)
ADJACENT_R = {"VS": 0.50, "FRUG": 0.35, "MAT": -0.40, "CR": 0.10}

# --------------------------------------------------------------------------------------
# Deliberate measurement misspecification
# --------------------------------------------------------------------------------------
# Real survey items are never perfectly congeneric. Without these, the CFA in Study 1 would fit
# perfectly by construction and would therefore certify nothing. These induce the kind of minor
# model-data discrepancy that real instruments exhibit, so that the reported fit indices,
# reliability estimates and HTMT ratios are informative rather than tautological.
#
# (construct, item index, contaminating construct, cross-loading)
CROSS_LOADINGS = [
    ("PA", 4, "RIA", 0.15),
    ("AD", 4, "PR", 0.16),
    ("CS", 4, "VS", 0.14),
    ("RSV", 3, "MAT", 0.13),
    ("SCB", 3, "CS", 0.13),
    ("SPS", 3, "CE", 0.12),
]
# (construct, item a, item b, residual correlation induced by a shared method factor)
RESID_CORR = [
    ("PR", 1, 2, 0.20),
    ("BSE", 1, 2, 0.17),
    ("AD", 2, 3, 0.16),
    ("CS", 2, 3, 0.15),
    ("RIA", 3, 4, 0.14),
]
# Common-method variance: a single nuisance factor loading weakly on every item.
CMV_LOADING = 0.10

LIKERT_MIN, LIKERT_MAX = 1, 7

# --------------------------------------------------------------------------------------
# Monte Carlo / bootstrap settings
# --------------------------------------------------------------------------------------
MC_REPS = 500
MC_SAMPLE_SIZES = [200, 400, 800, 1200, 1600, 2400]
BOOT_REPS = 5000
ALPHA = 0.05

# --------------------------------------------------------------------------------------
# Study 3 experiment design
# --------------------------------------------------------------------------------------
EXP3A_N_PER_CELL = 150          # 2 x 2 x 2 = 8 cells -> N = 1200
EXP3B_N = 2100                  # continuous stringency, 7 levels x 300
EXP3B_LEVELS = [0.05, 0.15, 0.30, 0.45, 0.60, 0.75, 0.90]
EXP3C_N_PER_CELL = 160          # 2 x 2 = 4 cells -> N = 640

# --------------------------------------------------------------------------------------
# Study 4: agent-based market system
# --------------------------------------------------------------------------------------
ABM = {
    "n_consumers": 1500,
    "n_firms": 8,
    "n_periods": 120,
    "burn_in": 20,
    # network
    "ws_k": 8,
    "ws_p": 0.10,
    # preference weights
    "beta_q": 1.00,        # weight on volume-availability (conventional demand)
    "beta_leg": 1.35,      # legitimacy premium weight (scaled by sacrifice x CS)
    "beta_p": 0.60,        # price sensitivity
    # firm economics
    "unit_margin": 0.22,
    "service_margin": 0.38,      # margin on durability/repair/service revenue
    "base_price": 1.00,
    "fixed_cost_share": 0.10,    # fixed cost as share of baseline revenue
    "exit_threshold": -0.05,     # profit ratio below which a firm exits
    "installed_base_decay": 0.10,
    # contagion
    "lambda_social": 0.10,       # swept
    "kappa_signal": 0.25,        # demarketing exposure -> CS
    "rho_precarity": 0.30,       # precarity suppresses CS
    "cs_decay": 0.04,
    # policy
    "pol_repair_subsidy": 0.0,
    "pol_defector_cost": 0.0,
    "pol_norm_signal": 0.0,
    # population
    "precarity_mean": 0.35,
    "precarity_gini": 0.30,
    "symbolic": 0.55,
    "elasticity_reduction": 0.55,   # max share of throughput a fully committed consumer forgoes
}
