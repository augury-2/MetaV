"""
STUDY 4 - An agent-based market-systems model of demarketing propagation.

This is the macro half of the SSM and the formal core of the paper's contribution. It answers the
question the degrowth-marketing literature poses but never models: *when does a firm's deliberate
downscaling of its own demand reduce aggregate throughput without destroying the firm?*

------------------------------------------------------------------------------------------------
MODEL
------------------------------------------------------------------------------------------------
Populations
  Consumers i = 1..N : chosen sufficiency cs_i in [0,1], precarity z_i, baseline demand q0_i,
                       embedded in a Watts-Strogatz small-world network G.
  Firms     j = 1..J : demarketing intensity d_j in [0,1], business-model reconfiguration
                       r_j in [0,1], price p_j, installed base IB_j, profit pi_j.
  Institutions       : repair subsidy, defector cost, exogenous norm signal.

(1) Demand.  q_i,t = q0_i * (1 - eta * cs_i,t)          eta = max forgone share

(2) Choice.  Consumers allocate demand across firms by softmax over
        u_ij = beta_q*(1 - d_j) + beta_leg * d_j * sac_j * cs_i - beta_p * p_j
     The middle term is the SIGN-FLIPPED SEGMENT ELASTICITY: for high-cs consumers, demarketing
     raises preference even as it lowers volume. sac_j is the credibility-conferring costly signal

        sac_j = d_j * (1 - phi * r_j)

     Note the built-in tension the theory predicts and the literature has missed: business-model
     reconfiguration makes demarketing SURVIVABLE but makes it LESS CREDIBLE, because the firm is
     visibly no longer sacrificing. This is the credibility-viability tradeoff (P22).

(3) Firm economics.
        units_j = sum_i q_i * share_ij * (1 - delta * r_j)       (durability lengthens cycles)
        IB_j    = IB_j * (1 - decay*(1 - psi*r_j)) + units_j
        rev_j   = units_j * p_j * unit_margin
                  + r_j * IB_j * service_fee * service_margin * (1 + repair_subsidy)
        cost_j  = fixed_j + defector_cost * (1 - d_j) * units_j
        pi_j    = rev_j - cost_j

(4) Supply-side propagation.  Each period firms imitate more profitable rivals with probability
     `imitation_rate`, moving (d_j, r_j) a step toward the better performer. Demarketing therefore
     spreads (or dies) endogenously rather than by assumption.

(5) Demand-side contagion and THE MICRO-MACRO BRIDGE.
        cs_i,t+1 = clip( cs_i,t
                         + lambda * (mean cs of neighbours - cs_i,t)      social contagion
                         + kappa * exposure_i,t                          demarketing exposure
                         + mu * g(S_req, z_i)                            MICRO MODEL INPUT
                         + norm_signal
                         - decay * cs_i,t , 0, 1)

     where g(.) is `dgp.cs_stringency_profile` - the *same* dual-route function estimated in
     Studies 2 and 3. Because g is negative for consumers whose flip point S* lies below the
     required stringency S_req, the population distribution of flip points enters the macro
     dynamics directly. This is the operational form of P19/P20.

------------------------------------------------------------------------------------------------
OUTPUTS
------------------------------------------------------------------------------------------------
  * five named regime scenarios with time series (futility, collapse, niche, tipping, backlash)
  * leakage, measured against a paired counterfactual run with all d_j = 0
  * the tipping surface in (lambda, r, policy) space, and lambda*(r) frontiers
  * the inequality experiment for P20
  * one-factor-at-a-time sensitivity elasticities
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace

import networkx as nx
import numpy as np
import pandas as pd
import scipy.sparse as sp

from config import ABM, SEED, TAB_DIR
from dgp import cs_stringency_profile, flip_point


# ======================================================================================
# Parameters
# ======================================================================================
@dataclass
class Params:
    n_consumers: int = ABM["n_consumers"]
    n_firms: int = ABM["n_firms"]
    n_periods: int = ABM["n_periods"]
    burn_in: int = ABM["burn_in"]
    ws_k: int = ABM["ws_k"]
    ws_p: float = ABM["ws_p"]

    # --- choice model -------------------------------------------------------------------
    # Demarketing acts on TWO distinct margins, which prior verbal theorising conflates:
    #   (i)  SELECTION: it repels low-sufficiency consumers and attracts high-sufficiency ones.
    #        This is the sign-flipped segment elasticity, and it is the source of any
    #        commercial upside from demarketing.
    #   (ii) VOLUME: it suppresses how much its own customers buy. This is the demarketing act
    #        itself, and it is unambiguously revenue-destroying at constant business model.
    beta_leg: float = 1.20      # legitimacy premium, scaled by sacrifice x consumer sufficiency
    beta_disc: float = 0.85     # discouragement penalty among low-sufficiency consumers
    # A demarketing firm still offers less assortment, less novelty and lower availability, so a
    # residual discouragement remains even for fully committed consumers. Without this the
    # legitimacy premium is unbounded in cs and the model runs away to monopoly.
    disc_residual: float = 0.60
    beta_p: float = ABM["beta_p"]
    logit_scale: float = 2.50
    nu_demkt_volume: float = 0.55    # own-demand suppression per unit of demarketing intensity
    price_premium_demkt: float = 0.15  # willingness-to-pay uplift earned by credible demarketing

    unit_margin: float = ABM["unit_margin"]
    service_margin: float = ABM["service_margin"]
    service_fee: float = 0.190              # per-period service revenue per unit of installed base
    base_price: float = ABM["base_price"]
    fixed_cost_share: float = 0.40
    reconfig_cost_share: float = 0.14       # capability investment required to decouple revenue
    exit_threshold: float = ABM["exit_threshold"]
    exit_patience: int = 12     # consecutive loss-making periods tolerated before exit
    installed_base_decay: float = ABM["installed_base_decay"]
    durability_unit_drag: float = 0.30      # delta
    durability_decay_relief: float = 0.65   # psi
    sacrifice_discount_reconfig: float = 0.40   # phi: reconfiguration erodes the costly signal

    lambda_social: float = 0.20
    kappa_signal: float = 0.08
    # Chosen sufficiency relaxes toward a person-specific ATTRACTOR rather than toward zero:
    #     cs*_i = clip(disposition_i + gamma * g(S_req, z_i), 0, 1)
    # where g(.) is the micro dual-route function from Studies 2-3. This preserves population
    # heterogeneity (including the committed minority), gives the dynamics a well-defined
    # equilibrium, and lets the micro model shift the attractor up (identity affirmation) or down
    # (deprivation) for each consumer individually. It is the formal micro-macro bridge.
    gamma_micro: float = 0.35               # translation of micro valence into the attractor
    theta_relax: float = 0.12               # relaxation rate toward the attractor
    cs_decay: float = 0.0                   # retained for backward compatibility; unused
    # reactance / compensatory displacement (the macro image of CDC in the micro model)
    xi_reactance: float = 0.55              # rate at which a deprivating limit breeds reactance
    zeta_rebound: float = 0.60              # demand inflation per unit of accumulated rebound
    rebound_decay: float = 0.10

    pol_repair_subsidy: float = ABM["pol_repair_subsidy"]
    pol_defector_cost: float = ABM["pol_defector_cost"]
    pol_norm_signal: float = ABM["pol_norm_signal"]
    pol_pressure: float = 0.0   # visibility of institutional sufficiency demands on consumers

    precarity_mean: float = ABM["precarity_mean"]
    precarity_sd: float = 1.0
    symbolic: float = ABM["symbolic"]
    elasticity_reduction: float = ABM["elasticity_reduction"]

    # strategy configuration
    share_demarketers: float = 0.25         # initial share of firms practising demarketing
    d_demarketer: float = 0.70
    r_demarketer: float = 0.0               # business-model reconfiguration of demarketers
    imitation_rate: float = 0.08
    imitation_step: float = 0.20

    required_stringency: float = 0.45       # S_req the transition asks of consumers
    # The initial distribution of chosen sufficiency is a MIXTURE, not a single mode: alongside a
    # mainstream low-sufficiency majority there is a pre-existing committed minority (voluntary
    # simplifiers, repair-cafe and tool-library participants). That minority is the seed on which
    # any demarketing strategy has to survive before contagion can operate, which is why the
    # population's variance - not its mean - is the decisive macro parameter (P19).
    cs_init_mean: float = 0.15
    cs_init_sd: float = 0.10
    committed_share: float = 0.15
    committed_mean: float = 0.50
    committed_sd: float = 0.15

    seed: int = SEED
    policy_level: float = 0.0               # convenience scalar used by the sweeps


def apply_policy_level(p: Params, level: float) -> Params:
    """Institutional scaffolding as a single ordinal intensity (0 = laissez-faire)."""
    return replace(p,
                   policy_level=level,
                   pol_repair_subsidy=0.50 * level,
                   pol_defector_cost=0.09 * level,
                   pol_norm_signal=0.010 * level,
                   pol_pressure=0.60 * level)


# ======================================================================================
# Simulation
# ======================================================================================
def _row_normalized_adjacency(n: int, k: int, pr: float, rng: np.random.Generator) -> sp.csr_matrix:
    g = nx.watts_strogatz_graph(n, k, pr, seed=int(rng.integers(0, 2 ** 31 - 1)))
    A = nx.to_scipy_sparse_array(g, format="csr", dtype=float)
    deg = np.asarray(A.sum(axis=1)).ravel()
    deg[deg == 0] = 1.0
    return sp.diags(1.0 / deg) @ A


def simulate(p: Params, force_no_demarketing: bool = False,
             collect_series: bool = False) -> dict:
    rng = np.random.default_rng(p.seed)
    N, J, T = p.n_consumers, p.n_firms, p.n_periods

    # ---- consumers ----
    precarity = rng.normal(p.precarity_mean, p.precarity_sd, N)
    q0 = np.clip(rng.lognormal(0.0, 0.35, N), 0.15, None)
    committed = rng.random(N) < p.committed_share
    cs = np.where(committed,
                  rng.normal(p.committed_mean, p.committed_sd, N),
                  rng.normal(p.cs_init_mean, p.cs_init_sd, N))
    cs = np.clip(cs, 0.0, 1.0)
    rebound = np.zeros(N)
    W = _row_normalized_adjacency(N, p.ws_k, p.ws_p, rng)

    # micro-model input: net dual-route valence of the required limit for each consumer
    micro_g = cs_stringency_profile(p.required_stringency, precarity)
    micro_g = np.asarray(micro_g, dtype=float)
    deprivation = np.maximum(0.0, -micro_g)     # consumers whose flip point lies below S_req
    disposition = cs.copy()                     # dispositional baseline
    micro_shift = p.gamma_micro * micro_g       # shift in the attractor from the micro model

    # ---- firms ----
    n_dem = 0 if force_no_demarketing else max(1, int(round(p.share_demarketers * J)))
    d = np.zeros(J)
    r = np.zeros(J)
    if not force_no_demarketing:
        d[:n_dem] = p.d_demarketer
        r[:n_dem] = p.r_demarketer
    price0 = np.full(J, p.base_price) * rng.uniform(0.96, 1.04, J)
    price = price0.copy()
    IB = np.full(J, 1.0)
    alive = np.ones(J, dtype=bool)
    loss_streak = np.zeros(J, dtype=int)

    baseline_units_per_firm = q0.sum() / J
    baseline_margin_rev = baseline_units_per_firm * p.base_price * p.unit_margin
    fixed = p.fixed_cost_share * baseline_margin_rev
    profit_ref = baseline_margin_rev - fixed

    series = []
    for t in range(T):
        sac = d * (1.0 - p.sacrifice_discount_reconfig * r)
        # credible demarketing earns a willingness-to-pay premium, which is itself a cost in the
        # choice model - the firm trades volume for margin
        price = price0 * (1.0 + p.price_premium_demkt * sac)

        # ---- choice shares (N x J): the sign-flipped segment elasticity ----
        #   high-cs consumers are ATTRACTED by credible demarketing
        #   low-cs consumers are REPELLED by it
        U = (p.beta_leg * (d * sac)[None, :] * cs[:, None]
             - p.beta_disc * d[None, :] * (1.0 - (1.0 - p.disc_residual) * cs[:, None])
             - p.beta_p * price[None, :])
        U = p.logit_scale * U
        U = np.where(alive[None, :], U, -1e9)
        U -= U.max(axis=1, keepdims=True)
        E = np.exp(U)
        share = E / E.sum(axis=1, keepdims=True)

        # ---- demand (sufficiency suppresses, reactance-driven rebound inflates) ----
        q = q0 * (1.0 - p.elasticity_reduction * cs) * (1.0 + p.zeta_rebound * rebound)
        units = ((q[:, None] * share) * (1.0 - p.nu_demkt_volume * d)[None, :]).sum(axis=0) \
            * (1.0 - p.durability_unit_drag * r)

        # ---- firm economics ----
        IB = IB * (1.0 - p.installed_base_decay * (1.0 - p.durability_decay_relief * r)) + units
        rev = units * price * p.unit_margin \
            + r * IB * p.service_fee * p.service_margin * (1.0 + p.pol_repair_subsidy)
        cost = (fixed
                + p.reconfig_cost_share * r * baseline_margin_rev
                + p.pol_defector_cost * (1.0 - d) * units)
        profit = np.where(alive, rev - cost, 0.0)

        # Reference profit for exit decisions: the market's own profit level at the end of the
        # burn-in period, i.e. what a firm in this market earned before the transition began.
        # Normalising against an analytic no-sufficiency benchmark would make every firm look
        # unprofitable and would confound sufficiency with mismanagement.
        if t == p.burn_in and alive.any():
            m = float(np.mean(profit[alive]))
            if abs(m) > 1e-9:
                profit_ref = m
        profit_ratio = profit / (abs(profit_ref) + 1e-12)

        # ---- exit (requires sustained losses, not a single bad period) ----
        if t > p.burn_in:
            loss_streak = np.where(profit_ratio < p.exit_threshold, loss_streak + 1, 0)
            dying = alive & (loss_streak >= p.exit_patience)
            alive = alive & ~dying

        # ---- supply-side imitation (endogenous propagation) ----
        if t > p.burn_in and not force_no_demarketing:
            movers = rng.random(J) < p.imitation_rate
            targets = rng.integers(0, J, J)
            for j in np.where(movers & alive)[0]:
                k = targets[j]
                if alive[k] and profit_ratio[k] > profit_ratio[j] + 1e-9:
                    d[j] += p.imitation_step * (d[k] - d[j])
                    r[j] += p.imitation_step * (r[k] - r[j])
            d = np.clip(d, 0.0, 1.0)
            r = np.clip(r, 0.0, 1.0)

        # ---- demand-side contagion + micro bridge ----
        exposure = (share * (d * sac)[None, :]).sum(axis=1)
        neighbour_mean = W @ cs
        # An exogenous sufficiency norm only builds chosen sufficiency among consumers for whom
        # the required limit is on the affirming side of their flip point. Broadcasting a
        # sufficiency norm at consumers who experience the limit as deprivation does not
        # manufacture consent; it manufactures reactance (handled below).
        norm_effect = p.pol_norm_signal * (micro_g > 0)

        # SOCIAL MULTIPLIER. Contagion enters the ATTRACTOR, not merely the level. Averaging
        # toward one's neighbours can only homogenise a population; it cannot raise its mean. What
        # makes sufficiency spread is that observing sufficiency in others changes what one takes
        # 'enough' to be. Since neighbour_mean is itself endogenous, the population fixed point is
        # approximately cs = (disposition + gamma*g) / (1 - lambda), so lambda is a social
        # multiplier that diverges as lambda -> 1. That divergence is the tipping mechanism, and
        # lambda* is the value at which it becomes strong enough to sustain firm viability.
        cs_star = np.clip(disposition + micro_shift + p.lambda_social * neighbour_mean, 0.0, 1.0)

        cs = np.clip(cs
                     + p.kappa_signal * exposure
                     + p.theta_relax * (cs_star - cs)
                     + norm_effect,
                     0.0, 1.0)

        # Reactance accumulates where a limit is deprivating AND the consumer is subject to
        # sufficiency pressure - whether from firms (demarketing exposure) or from institutions
        # (policy pressure). Being told to consume less is what converts latent deprivation into
        # active reactance, and reactance into compensatory displacement.
        pressure = exposure + p.pol_pressure
        rebound = np.clip(rebound
                          + p.xi_reactance * deprivation * pressure
                          - p.rebound_decay * rebound,
                          0.0, 1.0)

        if collect_series:
            series.append({
                "t": t, "Q_total": units.sum(), "cs_mean": cs.mean(),
                "rebound_mean": rebound.mean(), "profit_total": profit.sum(),
                "profit_ratio_demarketers": float(np.mean(profit_ratio[:max(n_dem, 1)])) if n_dem else np.nan,
                "profit_ratio_conventional": float(np.mean(profit_ratio[n_dem:])) if n_dem < J else np.nan,
                "prop_rate": float((d > 0.20).mean()), "d_mean": float(d.mean()),
                "r_mean": float(r.mean()), "n_alive": int(alive.sum()),
            })

    out = {
        "Q_total": float(units.sum()),
        "cs_mean": float(cs.mean()),
        "cs_p90": float(np.percentile(cs, 90)),
        "rebound_mean": float(rebound.mean()),
        # diagnostics
        "share_dem": float(share[:, :max(n_dem, 1)].sum(axis=1).mean()) if n_dem else 0.0,
        "units_ratio_dem": float(units[:n_dem].mean() / baseline_units_per_firm) if n_dem else np.nan,
        "units_ratio_conv": float(units[n_dem:].mean() / baseline_units_per_firm) if n_dem < J else np.nan,
        "rev_ratio_dem": float(rev[:n_dem].mean() / baseline_margin_rev) if n_dem else np.nan,
        "cost_ratio_dem": float(cost[:n_dem].mean() / baseline_margin_rev) if n_dem else np.nan,
        "profit_ratio_conv": float(np.mean(profit_ratio[n_dem:])) if n_dem < J else np.nan,
        "profit_total": float(profit.sum()),
        "profit_ratio_mean": float(np.mean(profit_ratio[alive])) if alive.any() else 0.0,
        "profit_ratio_demarketers": float(np.mean(profit_ratio[:n_dem])) if n_dem else np.nan,
        "profit_raw_demarketers": float(np.mean(profit[:n_dem])) if n_dem else np.nan,
        "profit_raw_conventional": float(np.mean(profit[n_dem:])) if n_dem < J else np.nan,
        "profit_raw_all": float(np.mean(profit)),
        "prop_rate": float((d > 0.20).mean()),
        "d_mean": float(d.mean()), "r_mean": float(r.mean()),
        "n_alive": int(alive.sum()), "n_exits": int(J - alive.sum()),
        # Exits must be attributed. A demarketer exiting is the theory's COLLAPSE regime. A
        # conventional volume incumbent exiting during a successful transition is not collapse -
        # it is incumbent displacement, and it is what a genuine transition looks like.
        "n_exits_demarketers": int(n_dem - alive[:n_dem].sum()) if n_dem else 0,
        "n_exits_conventional": int((J - n_dem) - alive[n_dem:].sum()) if n_dem < J else 0,
        "units_by_firm": units.copy(), "n_demarketers_init": n_dem,
        "share_micro_negative": float((micro_g < 0).mean()),
        "mean_micro_g": float(micro_g.mean()),
    }
    if collect_series:
        out["series"] = pd.DataFrame(series)
    return out


# ======================================================================================
# Derived measures
# ======================================================================================
def run_pair(p: Params, collect_series: bool = False) -> dict:
    """
    Treatment run and paired counterfactual, identical seed.

    The counterfactual is BUSINESS AS USUAL: no demarketing and no sufficiency policy. This is the
    right benchmark because the object of evaluation is the whole sufficiency intervention
    (firm strategy plus institutional scaffolding), not firm strategy holding policy fixed.
    Measuring against a policy-inclusive baseline would hide policy-induced backlash, which is
    precisely one of the regimes the theory predicts.
    """
    treat = simulate(p, force_no_demarketing=False, collect_series=collect_series)
    base = simulate(apply_policy_level(p, 0.0), force_no_demarketing=True,
                    collect_series=collect_series)

    # ---- leakage -------------------------------------------------------------------------
    # Definition: the share of the volume reduction achieved at the demarketing firms that fails
    # to show up as a reduction in category throughput, because rival supply absorbs it.
    #
    #     leakage = 1 - (Q_base - Q_treat) / (units lost by demarketers)
    #
    # leakage -> 1  : perfect futility. Every unit the demarketer refuses to sell is sold by a rival
    # leakage -> 0  : the demarketer's reduction passes through fully to aggregate throughput
    # leakage <  0  : NEGATIVE leakage, i.e. norm spillover - the reduction propagates beyond the
    #                 demarketer's own customer base. This is the signature of the tipping regime
    #                 and is the quantity the degrowth-marketing literature implicitly hopes for.
    n_dem = treat["n_demarketers_init"]
    ub, ut = base["units_by_firm"], treat["units_by_firm"]
    lost_at_demarketers = (ub[:n_dem] - ut[:n_dem]).sum()
    total_reduction = base["Q_total"] - treat["Q_total"]
    if abs(lost_at_demarketers) < 1e-9:
        leakage = np.nan
    else:
        leakage = float(np.clip(1.0 - total_reduction / lost_at_demarketers, -3.0, 1.5))

    dQ = total_reduction / max(1e-9, base["Q_total"])

    # The economically meaningful benchmark for a demarketing firm is not an abstract
    # no-sufficiency ideal but what a comparable firm earns in the SAME market without
    # demarketing. `relative_profit` therefore divides the demarketer's realised profit by the
    # mean profit of firms in the paired counterfactual run.
    denom = base["profit_raw_all"]
    relative_profit = (treat["profit_raw_demarketers"] / denom) if abs(denom) > 1e-12 else np.nan
    viable = (treat["n_exits_demarketers"] == 0) and (relative_profit >= 0.95)

    res = {
        "Q_base": base["Q_total"], "Q_treat": treat["Q_total"],
        "throughput_reduction": float(dQ), "leakage": leakage,
        "relative_profit_demarketers": float(relative_profit),
        "profit_ratio_demarketers": treat["profit_ratio_demarketers"],
        "profit_ratio_mean": treat["profit_ratio_mean"],
        "profit_total_treat": treat["profit_total"], "profit_total_base": base["profit_total"],
        "cs_mean_treat": treat["cs_mean"], "cs_mean_base": base["cs_mean"],
        "rebound_mean_treat": treat["rebound_mean"],
        "units_lost_at_demarketers": float(lost_at_demarketers),
        "prop_rate": treat["prop_rate"], "d_mean": treat["d_mean"], "r_mean": treat["r_mean"],
        "n_exits": treat["n_exits"],
        "n_exits_demarketers": treat["n_exits_demarketers"],
        "n_exits_conventional": treat["n_exits_conventional"],
        "viable": bool(viable),
        "PMV": bool(viable and dQ > 0.10),
        "share_micro_negative": treat["share_micro_negative"],
        "mean_micro_g": treat["mean_micro_g"],
        "regime": classify_regime(dQ, treat["n_exits_demarketers"], relative_profit),
    }
    if collect_series:
        res["series_treat"] = treat["series"]
        res["series_base"] = base["series"]
    return res


def classify_regime(dQ: float, n_exits_demarketers: int, rel_profit: float) -> str:
    """
    Regime taxonomy (constructs.md 6.3). Ordering matters: backlash and collapse are diagnosed
    first because they are failure modes that override any throughput result.

      backlash : aggregate throughput RISES - compensatory displacement dominates
      collapse : the DEMARKETER exits or earns negative profit
      futility : throughput essentially unchanged; the reduction leaks to rivals
      niche    : modest but real reduction, demarketer commercially viable
      tipping  : large reduction AND viability - post-growth market viability attained
      strained : real reduction achieved, but only by eroding the demarketer's profitability

    Note that only DEMARKETER exit counts as collapse. Conventional volume incumbents exiting in
    the course of a successful transition is incumbent displacement, not failure, and conflating
    the two would mislabel the theory's success case as its failure case.
    """
    n_exits = n_exits_demarketers
    viable = (n_exits == 0) and (rel_profit >= 0.95)
    if dQ < -0.02:
        return "backlash"
    if n_exits > 0 or (not np.isnan(rel_profit) and rel_profit <= 0.0):
        return "collapse"
    if dQ < 0.05:
        return "futility"
    if dQ < 0.20 and viable:
        return "niche"
    if dQ >= 0.20 and viable:
        return "tipping"
    return "strained"


# ======================================================================================
# Experiments
# ======================================================================================
def named_scenarios(base: Params | None = None) -> dict[str, Params]:
    base = base or Params()
    return {
        # A 'buy less' campaign bolted onto an unchanged volume business model, no institutions,
        # negligible social contagion. The empirically common case.
        "futility": replace(base, d_demarketer=0.30, r_demarketer=0.0, lambda_social=0.05,
                            share_demarketers=0.125, imitation_rate=0.02, policy_level=0.0),
        # Aggressive demarketing with a pure volume business model: arithmetically suicidal.
        "collapse": replace(base, d_demarketer=0.95, r_demarketer=0.0, lambda_social=0.10,
                            share_demarketers=0.125, imitation_rate=0.02),
        # Reconfigured business model serving a committed minority, no institutional support.
        "niche": replace(base, d_demarketer=0.70, r_demarketer=0.80, lambda_social=0.25,
                         share_demarketers=0.25, imitation_rate=0.03),
        # Reconfiguration + contagion + institutional scaffolding.
        "tipping": apply_policy_level(
            replace(base, d_demarketer=0.70, r_demarketer=0.80, lambda_social=0.40,
                    share_demarketers=0.25, imitation_rate=0.08), 0.6),
        # Stringent limits pressed on a highly precarious population, with strong institutional
        # sufficiency pressure: reactance, compensatory displacement, rebound.
        "backlash": apply_policy_level(
            replace(base, precarity_mean=1.60, required_stringency=0.85,
                    d_demarketer=0.70, r_demarketer=0.60, lambda_social=0.35,
                    share_demarketers=0.25), 0.6),
    }


def run_named_scenarios() -> tuple[pd.DataFrame, dict[str, pd.DataFrame]]:
    rows, series = [], {}
    for name, p in named_scenarios().items():
        res = run_pair(p, collect_series=True)
        series[name] = res.pop("series_treat")
        res.pop("series_base", None)
        rows.append({"scenario": name, **{k: v for k, v in res.items()}})
    return pd.DataFrame(rows), series


def tipping_surface(lambda_grid=None, r_grid=None, policy_levels=(0.0, 0.3, 0.6),
                    n_periods: int = 80, n_consumers: int = 1200) -> pd.DataFrame:
    """Sweep the (contagion, reconfiguration, policy) space and classify the resulting regime."""
    lambda_grid = np.linspace(0.0, 0.60, 9) if lambda_grid is None else lambda_grid
    r_grid = np.linspace(0.0, 1.0, 9) if r_grid is None else r_grid
    rows = []
    for pol in policy_levels:
        for lam in lambda_grid:
            for rr in r_grid:
                p = apply_policy_level(
                    replace(Params(), lambda_social=float(lam), r_demarketer=float(rr),
                            n_periods=n_periods, n_consumers=n_consumers), pol)
                res = run_pair(p)
                rows.append({"policy": pol, "lambda_social": float(lam), "r_demarketer": float(rr),
                             **{k: v for k, v in res.items() if not isinstance(v, np.ndarray)}})
    return pd.DataFrame(rows)


def lambda_star(surface: pd.DataFrame) -> pd.DataFrame:
    """Minimum contagion rate achieving post-growth market viability, by (policy, r)."""
    rows = []
    for (pol, rr), g in surface.groupby(["policy", "r_demarketer"]):
        ok = g[g["PMV"]].sort_values("lambda_social")
        rows.append({"policy": pol, "r_demarketer": rr,
                     "lambda_star": float(ok["lambda_social"].iloc[0]) if len(ok) else np.nan,
                     "max_throughput_reduction": float(g["throughput_reduction"].max()),
                     "any_PMV": bool(len(ok) > 0)})
    return pd.DataFrame(rows)


def complementarity_test(surface: pd.DataFrame) -> pd.DataFrame:
    """
    H16 strict complementarity: PMV requires BOTH reconfiguration and contagion.
    Reports PMV rate in each quadrant of the (lambda, r) space.
    """
    s = surface.copy()
    lam_med = s["lambda_social"].median()
    r_med = s["r_demarketer"].median()
    s["lambda_hi"] = s["lambda_social"] > lam_med
    s["r_hi"] = s["r_demarketer"] > r_med
    out = (s.groupby(["policy", "lambda_hi", "r_hi"])
           .agg(n=("PMV", "size"), PMV_rate=("PMV", "mean"),
                mean_reduction=("throughput_reduction", "mean"),
                mean_relative_profit=("relative_profit_demarketers", "mean"),
                mean_leakage=("leakage", "mean"))
           .reset_index())
    return out


def inequality_experiment(precarity_means=(0.0, 0.5, 1.0, 1.5, 2.0, 2.5),
                          precarity_sds=(0.6, 1.0, 1.4),
                          required_stringency: float = 0.65,
                          n_periods: int = 80, n_consumers: int = 1200) -> pd.DataFrame:
    """
    P20: because precarity lowers the micro flip point S*, higher precarity (and higher dispersion)
    should raise the contagion threshold lambda* required for post-growth market viability.

    Configuration notes. (a) The required stringency is set to 0.65 rather than the default 0.45,
    because a transition that asks little of consumers pushes almost nobody past their flip point
    and the mechanism cannot express itself - the interesting case is a demanding transition.
    (b) Reconfiguration is set to 0.55 and policy to zero so that the run sits NEAR the viability
    frontier; inside the region where viability is attained for any lambda, lambda* is trivially
    zero and the comparison is uninformative.
    """
    lam_grid = np.linspace(0.0, 0.68, 18)
    rows = []
    for mu in precarity_means:
        for sd in precarity_sds:
            lam_needed, best_red = np.nan, -9.9
            for lam in lam_grid:
                p = replace(Params(), precarity_mean=mu, precarity_sd=sd,
                            required_stringency=required_stringency,
                            lambda_social=float(lam), r_demarketer=0.55,
                            share_demarketers=0.125,
                            n_periods=n_periods, n_consumers=n_consumers)
                res = run_pair(p)
                best_red = max(best_red, res["throughput_reduction"])
                if res["PMV"] and np.isnan(lam_needed):
                    lam_needed = float(lam)
            draws = np.random.default_rng(1).normal(mu, sd, 40000)
            share_neg = float(np.mean(
                np.asarray(cs_stringency_profile(required_stringency, draws)) < 0))
            rows.append({"precarity_mean": mu, "precarity_sd": sd,
                         "lambda_star": lam_needed,
                         "max_throughput_reduction": best_red,
                         "share_below_flip_point": share_neg,
                         "mean_flip_point_S_star": flip_point(mu),
                         "required_stringency": required_stringency})
    return pd.DataFrame(rows)


def sensitivity(base: Params | None = None, pct: float = 0.20,
                n_periods: int = 80, n_consumers: int = 1200) -> pd.DataFrame:
    """One-factor-at-a-time elasticities of the two headline outcomes."""
    base = base or apply_policy_level(
        replace(Params(), lambda_social=0.50, r_demarketer=0.80, share_demarketers=0.25,
                n_periods=n_periods, n_consumers=n_consumers), 0.6)
    ref = run_pair(base)
    knobs = ["beta_leg", "beta_disc", "beta_p", "kappa_signal", "gamma_micro", "theta_relax",
             "elasticity_reduction", "service_margin", "unit_margin", "durability_unit_drag",
             "sacrifice_discount_reconfig", "imitation_rate", "precarity_mean",
             "required_stringency", "d_demarketer", "share_demarketers"]
    rows = []
    for k in knobs:
        v0 = getattr(base, k)
        for direction in (-1, +1):
            v = v0 * (1 + direction * pct) if v0 != 0 else direction * pct
            res = run_pair(replace(base, **{k: v}))
            rows.append({
                "parameter": k, "direction": "-20%" if direction < 0 else "+20%",
                "value": v, "throughput_reduction": res["throughput_reduction"],
                "d_throughput_reduction": res["throughput_reduction"] - ref["throughput_reduction"],
                "relative_profit_demarketers": res["relative_profit_demarketers"],
                "d_relative_profit": (res["relative_profit_demarketers"]
                                      - ref["relative_profit_demarketers"]),
                "regime": res["regime"], "PMV": res["PMV"]})
    out = pd.DataFrame(rows)
    out.attrs["reference"] = ref
    return out


def credibility_viability_tradeoff(n_periods: int = 80, n_consumers: int = 1200,
                                   phi_levels=(0.0, 0.4, 0.8, 1.0)) -> pd.DataFrame:
    """
    P22: reconfiguration raises viability but erodes the costly-signal credibility that drives the
    legitimacy premium (sac = d * (1 - phi * r)). If the credibility loss were strong enough,
    sweeping r would produce an INTERIOR optimum rather than a monotone gain.

    We sweep r at several values of phi so the conjecture is tested rather than assumed: phi is
    the rate at which reconfiguration erodes perceived sacrifice, and the question is whether any
    plausible phi makes the tradeoff bind.
    """
    rows = []
    for phi in phi_levels:
        for rr in np.linspace(0.0, 1.0, 21):
            p = apply_policy_level(
                replace(Params(), lambda_social=0.40, r_demarketer=float(rr),
                        sacrifice_discount_reconfig=float(phi),
                        share_demarketers=0.25, n_periods=n_periods,
                        n_consumers=n_consumers), 0.3)
            res = run_pair(p)
            rows.append({"phi_credibility_erosion": phi, "r_demarketer": rr,
                         "throughput_reduction": res["throughput_reduction"],
                         "relative_profit_demarketers": res["relative_profit_demarketers"],
                         "cs_mean_treat": res["cs_mean_treat"],
                         "leakage": res["leakage"], "regime": res["regime"],
                         "PMV": res["PMV"]})
    return pd.DataFrame(rows)


def interior_optimum_summary(cvt: pd.DataFrame) -> pd.DataFrame:
    """For each phi, report the argmax of throughput reduction and whether it is interior."""
    rows = []
    for phi, g in cvt.groupby("phi_credibility_erosion"):
        g = g.sort_values("r_demarketer")
        i = int(g["throughput_reduction"].idxmax())
        r_opt = float(g.loc[i, "r_demarketer"])
        rows.append({"phi_credibility_erosion": phi, "r_argmax": r_opt,
                     "max_reduction": float(g.loc[i, "throughput_reduction"]),
                     "reduction_at_r1": float(g[g["r_demarketer"] == 1.0]["throughput_reduction"].iloc[0]),
                     "interior_optimum": bool(0.0 < r_opt < 1.0)})
    return pd.DataFrame(rows)


# ======================================================================================
# Driver
# ======================================================================================
def run(full: bool = True) -> dict:
    print("[Study 4A] Named regime scenarios ...")
    scen, series = run_named_scenarios()
    scen.to_csv(f"{TAB_DIR}/t13a_abm_scenarios.csv", index=False)
    for k, v in series.items():
        v.to_csv(f"{TAB_DIR}/t13b_series_{k}.csv", index=False)
    cols = ["scenario", "regime", "throughput_reduction", "leakage",
            "relative_profit_demarketers", "prop_rate", "cs_mean_treat",
            "rebound_mean_treat", "n_exits_demarketers", "n_exits_conventional", "PMV"]
    print(scen[cols].round(4).to_string(index=False))

    print("\n[Study 4B] Tipping surface sweep over (contagion x reconfiguration x policy) ...")
    surf = tipping_surface() if full else tipping_surface(
        lambda_grid=np.linspace(0, 0.60, 5), r_grid=np.linspace(0, 1, 5), policy_levels=(0.0, 0.6))
    surf.to_csv(f"{TAB_DIR}/t14a_tipping_surface.csv", index=False)
    print("  regime frequencies by policy level:")
    print(pd.crosstab(surf["policy"], surf["regime"], normalize="index").round(3).to_string())

    lstar = lambda_star(surf)
    lstar.to_csv(f"{TAB_DIR}/t14b_lambda_star.csv", index=False)
    print("\n[Study 4B] lambda* (minimum contagion for post-growth market viability):")
    print(lstar.pivot(index="r_demarketer", columns="policy", values="lambda_star")
          .round(3).to_string())
    print("\n[Study 4B] maximum attainable throughput reduction:")
    print(lstar.pivot(index="r_demarketer", columns="policy",
                      values="max_throughput_reduction").round(3).to_string())

    comp = complementarity_test(surf)
    comp.to_csv(f"{TAB_DIR}/t14c_complementarity.csv", index=False)
    print("\n[Study 4B] H16 complementarity - PMV rate by quadrant:")
    print(comp.round(3).to_string(index=False))

    print("\n[Study 4C] Credibility-viability tradeoff in reconfiguration ...")
    cvt = credibility_viability_tradeoff()
    cvt.to_csv(f"{TAB_DIR}/t15a_credibility_viability.csv", index=False)
    io = interior_optimum_summary(cvt)
    io.to_csv(f"{TAB_DIR}/t15b_interior_optimum.csv", index=False)
    print(io.round(4).to_string(index=False))
    print("  (r sweep at phi = 0.4, the default credibility-erosion rate:)")
    print(cvt[cvt["phi_credibility_erosion"] == 0.4][
        ["r_demarketer", "throughput_reduction", "relative_profit_demarketers",
         "leakage", "regime", "PMV"]].round(4).to_string(index=False))

    print("\n[Study 4D] Inequality experiment (P20) ...")
    ineq = inequality_experiment()
    ineq.to_csv(f"{TAB_DIR}/t16_inequality.csv", index=False)
    print(ineq.round(4).to_string(index=False))

    print("\n[Study 4E] One-factor-at-a-time sensitivity ...")
    sens = sensitivity()
    sens.to_csv(f"{TAB_DIR}/t17_sensitivity.csv", index=False)
    top = sens.reindex(sens["d_throughput_reduction"].abs().sort_values(ascending=False).index)
    print(top.head(16).round(4).to_string(index=False))

    return {"scenarios": scen, "series": series, "surface": surf, "lambda_star": lstar,
            "complementarity": comp, "credibility_viability": cvt,
            "inequality": ineq, "sensitivity": sens}
