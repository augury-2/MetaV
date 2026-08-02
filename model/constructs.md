# The Sufficiency–Sovereignty Model (SSM): Formal Construct and Proposition Specification

**Companion document to:** *Marketing Without Growth: A Market-Systems Theory of Sufficiency,
Demarketing, and Consumer Sovereignty Under Limits*

This document is the normative specification of the theory. It is the single source of truth for
(a) construct definitions, (b) discriminant positioning against adjacent constructs,
(c) operationalizations, (d) the structural model, and (e) the propositions/hypotheses that the
code in `../analysis/` estimates. Every parameter name used here maps 1:1 to a variable name in
`../analysis/src/`.

---

## 0. The theoretical problem in one paragraph

Marketing's foundational logic is *volume-expansionary*: the discipline's core constructs (demand
generation, share of wallet, category growth, customer lifetime value) all encode "more" as the
dependent variable. Sustainable-consumption research has, for three decades, relaxed the
*composition* of consumption (greener, more efficient, more circular) while leaving the *scale*
of consumption untouched — the "efficiency without sufficiency" trap. The 2025 opening of
degrowth/post-growth marketing as a scholarly conversation names the missing piece but supplies it
at the wrong level of analysis: it is macro, narrative, and critical, with no micro-founded account
of how an individual consumer psychologically metabolizes a limit, and no formal account of how a
firm-level demarketing act propagates through a competitive market system without destroying the
firm. The SSM supplies both, and connects them.

**Two questions organize the theory:**

- **Q1 (micro / sovereignty):** Under what conditions is a consumption limit experienced as an
  *expansion* of consumer sovereignty (identity-affirming self-authorship) rather than a
  *contraction* of it (deprivation, reactance)?
- **Q2 (macro / viability):** Under what conditions does firm-level demarketing *propagate* through
  a market system and reduce aggregate throughput, rather than leaking to rivals (futility) or
  destroying the demarketer (collapse)?

**The bridge claim:** the macro tipping threshold is a function of the micro flip point. Aggregate
demarketing viability is not determined by firm strategy alone; it is determined by the *shape of
the population distribution of the micro-level appraisal process*. This is the micro–macro bridge
the literature lacks.

---

## 1. Focal construct

### 1.1 Chosen Sufficiency (CS)

> **Definition.** *Chosen sufficiency* is a consumer's self-authored, endorsed commitment to an
> "enough point" — a self-set upper bound on consumption volume or throughput within a domain —
> that is experienced as *expressive of* rather than *imposed upon* the self.

Three definitional features, all necessary:

1. **Bounded-quantity referent.** CS is about *scale* (how much), not composition (which kind).
   A consumer who replaces conventional beef with plant-based beef at constant volume is not
   exhibiting CS.
2. **Self-endorsement.** The limit is *integrated* in the Self-Determination Theory sense: the
   consumer would re-choose it absent surveillance or incentive. External compliance without
   endorsement is *constrained restraint*, not CS.
3. **Positive valence carrier.** The limit is a source of identity value ("this is who I am"),
   not merely a tolerated cost. This is what distinguishes CS from stoic endurance.

**CS is a state, not a trait.** It is domain-specific, manipulable, and reversible. This is a
deliberate departure from voluntary-simplicity research, which treats sufficiency as a stable
lifestyle identity and therefore cannot explain onset, spread, or collapse.

### 1.2 Discriminant positioning (what CS is *not*)

| Adjacent construct | Core referent | How CS differs | Expected correlation with CS |
|---|---|---|---|
| Frugality (Lastovicka et al. 1999) | Resourcefulness, price/economic restraint | CS is not motivated by economy; frugality is agnostic about total scale | r ≈ .35 |
| Voluntary simplicity (Etzioni 1998) | Whole-life ideological lifestyle | CS is domain-specific, state-like, manipulable | r ≈ .50 |
| Anti-consumption (Lee et al. 2009) | *Against* an object/brand/ideology (rejection, aversion) | CS is *for* an enough point; not oppositional | r ≈ .25 |
| Materialism (Richins & Dawson 1992) | Possession centrality as success/happiness | Theoretical opposite pole, but not merely low materialism: CS adds an *active* bound | r ≈ −.40 |
| Mindful consumption (Sheth et al. 2011) | Caring mindset + temperance across self/community/nature | CS isolates the *quantity bound* and its identity function | r ≈ .55 |
| Scarcity / deprivation mindset (Shah et al. 2012) | Perceived insufficiency of resources | Opposite phenomenology: CS is sufficiency *satisfaction*; scarcity is lack | r ≈ −.30 |
| Constrained restraint (this paper) | Externally enforced reduction without endorsement | The critical contrast case; same behavior, opposite psychology | r ≈ .10 |

> **Discriminant validity requirement.** CS must show HTMT < .85 against all of the above and
> incremental predictive validity over voluntary simplicity and low materialism on the outcome
> set. This is tested in Study 1/2.

---

## 2. Antecedents: Limit Architecture (the manipulable design space)

The SSM's marketing-actionable antecedent is not "the limit" but the **architecture** of the limit.
A limit is a designed object with separable design dimensions. This is what makes the theory a
*marketing* theory rather than a political-economy claim: it identifies a design space over which
firms and policymakers have control.

**Limit Architecture** `LA = (A, L, F, S)`

| Dim. | Name | Code | Levels / range | Theoretical rationale |
|---|---|---|---|---|
| A | **Limit agency** | `agency` | 0 = imposed (external actor sets bound) → 1 = chosen (consumer authors bound) | SDT autonomy support vs. control |
| L | **Limit locus** | `locus` | 0 = individual ("your budget") → 1 = collective ("our shared cap") | Collective-action efficacy; norm co-presence |
| F | **Limit frame** | `frame` | 0 = reduction/loss ("cut 30%") → 1 = sufficiency/gain ("enough is a good place") | Prospect framing + regulatory fit |
| S | **Limit stringency** | `stringency` | continuous ∈ [0, 1]; share of baseline throughput forgone | Dose. Carries the nonlinearity (§5, P7) |

**Firm-side antecedents (the demarketing act):**

| Construct | Code | Definition |
|---|---|---|
| **Demarketing intensity** | `demkt_intensity` | Degree to which a firm's marketing effort is deliberately directed at reducing the volume of its own category/offering (selective downscaling), ∈ [0,1] |
| **Demarketing sacrifice signal** | `demkt_sacrifice` | Perceived costliness to the firm of its demarketing act (revenue visibly forgone); a costly-signaling credibility cue, ∈ [0,1] |
| **Business-model reconfiguration** | `bm_reconfig` | Extent to which firm revenue is decoupled from unit throughput (durability, repair, service, access), ∈ [0,1] |

> **Why `demkt_sacrifice` matters theoretically.** It is the construct that separates demarketing
> from greenwashing. Sufficiency claims are cheap talk unless the firm visibly forgoes revenue;
> `demkt_sacrifice` is the credibility-conferring costly signal. Its interaction with
> `demkt_intensity` is the theory's answer to "why do 'buy less' campaigns usually fail?" —
> because intensity without sacrifice reads as marketing, and marketing about buying less
> *increases* category salience.

---

## 3. The dual-route mechanism (the theoretical engine)

The SSM's central claim is that a limit is processed through **two simultaneous, competing
appraisal routes**, and that CS is the *net* resultant. Prior work assumes a single route (either
"restraint is virtuous" or "restraint is aversive"); the flip phenomenon is only explicable with two.

### Route A — Autonomy–Identity route (sovereignty-expanding)

```
Limit Architecture ──► Perceived Autonomy (PA) ──► Restraint Identity Affirmation (RIA) ──► CS
                              │                              │
                              │                              └──► Restraint Signaling Value (RSV) ──► CS
                              │
        locus ──► Collective Efficacy & Norm Reinforcement (CE) ──► CS
```

| Mediator | Code | Definition |
|---|---|---|
| **Perceived autonomy** | `PA` | Extent to which the consumer experiences the limit as volitional and self-endorsed rather than pressured (SDT autonomy need satisfaction, limit-specific) |
| **Restraint identity affirmation** | `RIA` | Extent to which holding the limit affirms a valued self-concept — restraint as *self-expansion* rather than self-denial |
| **Restraint signaling value** | `RSV` | Perceived social-symbolic value of visibly holding the limit (competitive-altruism/conspicuous-restraint signal) |
| **Collective efficacy & norm reinforcement** | `CE` | Belief that the limit is shared, consequential at aggregate scale, and socially reinforced |

### Route B — Deprivation–Reactance route (sovereignty-contracting)

```
Limit Architecture ──► Anticipated Deprivation (AD) ──► Psychological Reactance (PR) ──► ↓CS
                                                                    │
                                                                    └──► Compensatory Displacement (CDC)
```

| Mediator | Code | Definition |
|---|---|---|
| **Anticipated deprivation** | `AD` | Expectation that the limit will produce experiential loss, foregone identity projects, or diminished life quality |
| **Psychological reactance** | `PR` | Motivational-arousal state to restore threatened choice freedom (anger + negative cognitions toward the limit-setting agent) |

### Net-resultant specification

```
CS* = ω_A · (Route A activation) − ω_B · (Route B activation)
```

Route A and Route B are **not** endpoints of one bipolar dimension. They are separable and can be
*simultaneously high* (ambivalent sufficiency) — an empirically testable and theoretically
important claim (P6). The correlation r(PA, AD) is predicted to be moderate-negative
(≈ −.35), not near −1.

---

## 4. Outcomes

| Outcome | Code | Definition | Level |
|---|---|---|---|
| **Sufficiency commitment behavior** | `SCB` | Behavioral commitment to reduced throughput (intentions + incentivized/behavioral proxy) | Consumer |
| **Brand sufficiency equity** | `BSE` | Trust, attachment, and advocacy accruing to a firm *because of* its demarketing posture | Consumer→Firm |
| **Sufficiency policy support** | `SPS` | Support for sufficiency-oriented public policy (caps, durability mandates, advertising limits) | Consumer→Citizen |
| **Compensatory displacement consumption** | `CDC` | Volume rebound in adjacent categories or later periods offsetting the focal reduction | Consumer (leakage) |

> **Why CDC is in the model.** Including the theory's own primary failure mode is a rigor move,
> not a hedge. A sufficiency theory that only predicts its own success is unfalsifiable and will
> be (correctly) rejected by FT50 reviewers as advocacy. CDC makes the theory refutable and
> supplies the micro-foundation for macro leakage (§6).

### Macro outcomes (market-system level)

| Outcome | Code | Definition |
|---|---|---|
| **Aggregate throughput** | `Q_total` | Total physical units transacted in the category per period |
| **Post-growth market viability** | `PMV` | Firm profitability sustained while category throughput declines: `PMV = 1` iff `π_t ≥ π_0` and `Q_t < Q_0` |
| **Demarketing propagation** | `prop_rate` | Share of category supply-side capacity practicing demarketing at intensity > threshold |
| **Leakage rate** | `leakage` | Share of demand forgone at the demarketing firm that is absorbed by non-demarketing rivals |

---

## 5. Moderators (boundary conditions)

Boundary conditions are the theory's defense against the "ideologically loaded" reviewer critique:
the SSM specifies precisely where sufficiency **fails**.

| # | Moderator | Code | Moderates | Predicted direction |
|---|---|---|---|---|
| M1 | Cultural collectivism / interdependent self-construal | `collectivism` | `locus → CE`, `locus → PA` | Strengthens collective-locus advantage |
| M2 | Economic precarity / material insecurity | `precarity` | `LA → AD` (all dims) | Amplifies Route B; converts sufficiency into deprivation |
| M3 | Category symbolic intensity | `symbolic` | `RIA → CS` (+), `AD → PR` (+) | Amplifies *both* routes (polarizing) |
| M4 | Community embeddedness | `community` | `CS → SCB`, `CS → −CDC` | Strengthens translation; suppresses leakage |
| M5 | Growth-paradigm endorsement / system justification | `growth_endorse` | `PA → RIA`, `CS → SPS` | Attenuates identity route and citizen spillover |

**M2 (precarity) is the theory's most important boundary condition.** It encodes the distributive
critique of degrowth directly into the model: sufficiency is a *luxury of the secure*. The SSM
predicts that identical limit architectures produce CS among the materially secure and reactance
among the precarious. This is what makes the theory politically serious rather than politically
naive, and it is why the JPP&M framing (distributive justice of sufficiency policy) is the
strongest target.

**M3 (symbolic intensity) is a genuinely novel prediction:** symbolic categories *polarize* rather
than uniformly dampen. Fashion is where restraint is most identity-valuable *and* most
deprivation-inducing. Utilities are where restraint is psychologically inert. Prior work assumes
symbolic categories are simply harder.

---

## 6. Macro layer: demarketing propagation in a market system

The market is modeled as a complex adaptive system (Market System Dynamics) with three
interacting populations.

### 6.1 Agents

**Consumers** `i = 1..N`, each with:
- `cs_i` — chosen sufficiency (from the micro model)
- `precarity_i`, `symbolic_sens_i`, `collectivism_i`
- `q_i` — throughput demand per period
- position in social network `G` (Watts–Strogatz small world)

**Firms** `j = 1..J`, each with:
- `d_j` — demarketing intensity
- `r_j` — business-model reconfiguration (revenue decoupled from units)
- `m_j` — margin, `share_j` — market share, `π_j` — profit
- survival state

**Institutions** — a policy vector:
- `pol_repair_subsidy` — lowers cost of durability/repair revenue
- `pol_defector_cost` — raises cost of non-demarketing supply (advertising restrictions, EPR fees)
- `pol_norm_signal` — exogenous sufficiency norm injection

### 6.2 Core mechanisms

1. **Sufficiency demand elasticity (sign-flipped segment).** For high-CS consumers, demarketing
   *increases* purchase-preference weight (legitimacy premium) even as it decreases volume:
   `pref_ij = β_q·(1−d_j) + β_leg·d_j·sacrifice_j·cs_i − β_p·price_j`
   This is the formal representation of the paper's key commercial insight: demarketing buys
   *preference* while selling *fewer units*. Whether that trade is profitable is the whole question.

2. **Leakage / free-riding.** Demand suppressed by firm *j* redistributes to rivals in proportion
   to their non-demarketing capacity. Leakage is the market system's homeostatic response and the
   reason unilateral demarketing is typically futile.

3. **Norm contagion.** `cs_i` updates via social influence:
   `cs_i,t+1 = cs_i,t + λ·(mean CS of neighbours − cs_i,t) + κ·(exposure to demarketing signal) − ρ·precarity_i`
   Contagion is what makes tipping possible.

4. **Value migration.** Firm revenue: `rev_j = units_j·p_j·(1−r_j) + installed_base_j·s_j·r_j`
   Reconfiguration converts a volume business into a stock/service business. Without it,
   demarketing is arithmetically suicidal.

5. **Institutional scaffolding.** Policy shifts the payoff of defection, making cooperative
   downscaling an equilibrium rather than a sacrifice.

### 6.3 Predicted regimes (P13–P17)

| Regime | Condition | Signature |
|---|---|---|
| **Futility** | low contagion, low policy, high rival capacity | `Q_total` ≈ unchanged, leakage → 1, demarketer loses share |
| **Collapse** | high `d_j`, low `r_j` | demarketer profit → 0, exit, `Q_total` unchanged |
| **Niche** | moderate contagion, high `r_j`, low policy | demarketer viable, `Q_total` reduced only marginally |
| **Contagion / tipping** | contagion > λ*, `r_j` > r*, policy > 0 | `Q_total` ↓ substantially **and** `PMV = 1` |
| **Backlash** | imposed limits × high mean precarity | CDC rebound, `SPS` ↓, policy delegitimized, `Q_total` ↑ |

The scientific product of the macro model is the **location of the tipping surface** in
(λ, r, policy) space — the first formal statement of when demarketing is commercially survivable.

---

## 7. Propositions and hypotheses

Notation: **P** = conceptual proposition (theory paper contribution). **H** = empirically tested
hypothesis in this manuscript.

### Micro: Route architecture

- **P1 / H1.** Limit agency (chosen > imposed) increases CS, mediated by PA.
- **P2 / H2.** Limit locus (collective > individual) increases CS, mediated by CE, and this
  indirect effect is stronger at higher `collectivism`.
- **P3 / H3.** Sufficiency framing (gain > reduction) increases CS by *simultaneously* raising RIA
  and lowering AD — a dual-path frame effect.
- **P4 / H4.** PA → CS is mediated by RIA (autonomy becomes sufficiency only when it is
  identity-relevant). Serial mediation: `agency → PA → RIA → CS`.
- **P5 / H5.** RIA → CS is partially carried by RSV (restraint as social signal), and RSV's
  contribution rises with `symbolic` intensity.
- **P6.** Route A and Route B are separable, not bipolar: consumers can occupy a high-PA/high-AD
  *ambivalent sufficiency* state; r(PA, AD) is moderate, not near −1.

### Micro: the flip

- **P7 / H7.** The effect of limit stringency on CS is **inverted-U**: CS rises to a
  sufficiency optimum `S*` then falls, because Route A saturates while Route B accelerates.
- **P8 / H8.** The **flip point** `S*` is moderated by precarity: `∂S*/∂precarity < 0`
  (the precarious flip into deprivation at lower stringency). Tested by Johnson–Neyman.
- **P9 / H9.** Precarity moderates `LA → AD`: identical architectures generate deprivation among
  the precarious. Chosen-vs-imposed advantages shrink or reverse under high precarity.
- **P10 / H10.** Symbolic intensity **polarizes**: it strengthens *both* `RIA → CS` and `AD → PR`.

### Micro: outcomes and leakage

- **P11 / H11.** CS → SCB is moderated by `community` embeddedness (translation moderator);
  CS without community produces attitude without behavior.
- **P12 / H12.** CS → CDC is negative but attenuated toward zero at low `community` and high
  `symbolic`, i.e. leakage is a *structural* not a moral failure.
- **P13 / H13.** Demarketing intensity → BSE is moderated by `demkt_sacrifice`:
  positive at high sacrifice, **null or negative** at low sacrifice (sufficiency-washing penalty).
- **P14 / H14.** CS → SPS (consumer→citizen spillover) is attenuated by `growth_endorse`.

### Macro: propagation and viability

- **P15 / H15.** Unilateral demarketing without business-model reconfiguration yields
  leakage → 1 and no change in `Q_total` (futility), regardless of intensity.
- **P16 / H16.** `PMV` is achievable **only** in the joint region
  `r_j > r*` **and** `λ > λ*`; neither reconfiguration nor contagion alone suffices
  (a strict complementarity claim — the model's sharpest falsifiable prediction).
- **P17 / H17.** Institutional scaffolding lowers the contagion threshold `λ*` — policy substitutes
  for cultural change, and the substitution rate is estimable.
- **P18 / H18.** Above the tipping surface, throughput reduction and firm profitability are
  **jointly** attainable: the growth imperative is a contingent, not necessary, property of markets.

### Bridge

- **P19.** The macro tipping threshold `λ*` is decreasing in the population share whose micro flip
  point `S*` exceeds the required stringency — i.e., **macro viability is a function of the micro
  distribution of the flip point**, not of mean pro-environmental attitude.
- **P20.** Because precarity lowers `S*` (P8), inequality raises `λ*`: **unequal societies require
  more institutional scaffolding to achieve the same throughput reduction.** Distributive policy is
  therefore a *precondition* of sufficiency policy, not a parallel concern.
- **P21.** Marketing capability is regime-determining, not merely regime-serving: the same
  competence set (positioning, segmentation, brand-meaning management) that produces volume growth
  can produce viable contraction, conditional on `r` and institutional design.

---

## 8. Estimation plan (maps to `../analysis/src/`)

| Study | Question | File | Method |
|---|---|---|---|
| 1 | Is the model measurable, identified, and adequately powered? | `simulate_micro.py`, `measurement.py` | DGP + CFA, reliability, AVE/HTMT, Monte Carlo parameter recovery, power curves |
| 2 | Does the dual-route structural model hold, with moderated mediation and cross-national invariance? | `sem_micro.py`, `moderated_mediation.py` | SEM (semopy), bootstrapped conditional indirect effects, index of moderated mediation, multigroup |
| 3 | Does the flip exist and move with precarity? | `experiment_analysis.py` | 2×2×2 factorial ANOVA, planned contrasts, Johnson–Neyman, quadratic + two-lines inverted-U test |
| 4 | When does demarketing propagate without collapsing the firm? | `abm_market.py` | Agent-based market system, regime classification, tipping-surface sweep, sensitivity analysis |

**Data status (stated plainly).** The micro datasets analyzed in Studies 1–3 are **synthetic**,
generated from the DGP specified above with parameters calibrated to published effect sizes in
adjacent literatures. They therefore constitute a *computational pre-registration*: they establish
that the SSM is identified, estimable, and adequately powered, and they fix the analysis pipeline
in advance of field data collection. They are **not** evidence that the propositions are true.
Study 4 is a formal analytical result about the model itself and does not depend on field data.
