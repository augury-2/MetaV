# Marketing Without Growth

A micro–macro theory of sufficiency, demarketing, and consumer sovereignty under limits — with a
formal conceptual model and executable code that tests it.

> **Data status.** The micro datasets in Studies 1–3 are **synthetic**, generated from the theory's
> own data-generating process with parameters calibrated to published effect-size ranges. They
> establish that the model is identified, estimable, powered and falsifiable, and they fix the
> analysis pipeline in advance of data collection — a *computational pre-registration*. They are not
> evidence that the propositions are true. Study 4 is a formal analytical result about the model and
> does not depend on data. See the boxed statement at the top of `paper/MANUSCRIPT.md`.

---

## The theory in one paragraph

**Chosen sufficiency** — a self-authored, identity-affirming upper bound on consumption volume — is
the *net resultant* of two competing appraisal routes: an autonomy–identity route that expands
consumer sovereignty and a deprivation–reactance route that contracts it. Because the identity gain
from a limit **saturates** in stringency while the deprivation cost **accelerates**, the net effect
is inverted-U with an interior **flip point** *S\**, derivable in closed form, which **falls as
economic precarity rises**. At the market level, demarketing propagates only where business-model
reconfiguration and social contagion are *jointly* present; otherwise it leaks to rivals (futility)
or destroys the demarketer (collapse). Because the macro tipping threshold depends on the population
distribution of micro flip points, and precarity lowers those flip points, **inequality raises the
threshold and beyond a point removes it entirely** — making distributive policy a precondition of
sufficiency policy rather than a parallel concern.

---

## Repository map

```
MetaV/
├── model/
│   └── constructs.md              Formal specification: constructs, definitions,
│                                  operationalizations, 22 propositions
├── paper/
│   ├── MANUSCRIPT.md              The full paper
│   ├── WEB_APPENDIX.md            Item wording, stimuli, complete ABM equations,
│   │                              calibration search, robustness, results index
│   └── POSITIONING_MEMO.md        Journal fit, the five reviewer objections that
│                                  can kill it, honest novelty assessment
└── analysis/
    ├── requirements.txt
    ├── src/                       11 modules + master pipeline + verification harness
    └── output/
        ├── tables/                43 results tables
        ├── figures/               12 figures
        ├── summary.json           Headline numbers
        └── run_full.log           Full run log
```

---

## Headline results

### Studies 1–3 (synthetic; a specification, not evidence)

| Result | Value |
|---|---|
| Measurement model fit | CFI = .985, TLI = .983, RMSEA = .017, χ²/df = 1.45 |
| Reliability / convergent validity | α .767–.860; AVE .525–.604 (all > .50) |
| Max HTMT across 105 pairs | .673 |
| **Chosen sufficiency vs constrained restraint** | **HTMT = .120** — same behaviour, orthogonal psychology |
| Monte Carlo recovery at *N* = 1,600 | max abs bias .085; mean CI coverage .958 |
| Hypothesised terms supported | **28 / 28** |
| Cross-national path heterogeneity | **0 / 28** paths differ (metric invariance *p* = .38) |
| Bootstrap indirect/conditional effects excluding zero | **36 / 36** |
| **Inverted-U (two-lines test)** | ascending +1.17 (*p* < .001), descending −1.35 (*p* < .001) |
| **Flip point** | *Ŝ\** = .406 [.368, .436] vs analytic .353 |
| **Flip-point shift with precarity** | Δ*S\** = −.0965 [−.178, −.019]; curvature interaction *p* = .006 |
| Limit architecture, best vs worst, at identical stringency | *d* = **.516** |
| Limit *locus* effect on deprivation | *d* = .018, ***p* = .751** — a pure Route A lever |
| **Demarketing → brand equity, no sacrifice signal** | *d* = −.096, ***p* = .389** (nothing) |
| **Demarketing → brand equity, credible sacrifice** | *d* = **+.489** (*p* < .001) |
| Stringency significantly *reduces* sufficiency above | precarity = −0.203 *z* (**54.6%** of the sample) |
| Hypotheses undetectable in a survey at any realistic *N* | 1 (identified, with the design that fixes it) |

### Study 4 (formal analysis)

| Regime | Δ throughput | Leakage | Demarketer profit vs BAU |
|---|---|---|---|
| **Futility** — "buy less" on an unchanged business model | +1.1% | .740 | 0.32 |
| **Collapse** — aggressive demarketing, volume model | 0.0% | 1.000 | 0.00 (exit) |
| **Niche** — reconfigured, committed minority | +10.0% | .418 | 1.94 |
| **Tipping** — reconfiguration + contagion + institutions | **+39.1%** | **−1.443** | **5.68** |
| **Backlash** — stringent limits on a precarious population | **−23.6%** | > 1 | 1.81 |

**Strict complementarity (H16), at zero policy** — post-growth market viability rate:

| | Low reconfiguration | High reconfiguration |
|---|---|---|
| **Low contagion** | **.00** | .50 |
| **High contagion** | .25 | **1.00** |

**Inequality raises the tipping threshold, then removes it (P20):**

| Mean precarity | 0.0 | 0.5 | 1.0 | 1.5 | 2.0 | 2.5 |
|---|---|---|---|---|---|---|
| λ\* required | .56 | .60 | .64 | .68 | **unattainable** | **unattainable** |
| Share past their flip point | .016 | .050 | .124 | .258 | .444 | .640 |

**A conjecture the model rejects (P22).** We predicted that decoupling revenue from volume would
erode sufficiency credibility enough to create an interior optimum in reconfiguration. It does not,
at any credibility-erosion rate up to complete erosion. Reported as rejected.

---

## Reproduction

```bash
python -m venv .venv && . .venv/bin/activate      # Python 3.11
pip install -r analysis/requirements.txt

cd analysis/src
python run_all.py            # full pipeline, ~13 min, deterministic (SEED = 20260801)
python run_all.py --quick    # reduced replications, ~2 min
python verify_manuscript.py  # asserts every numeric claim in the manuscript
```

`verify_manuscript.py` re-reads every results table and checks each numeric claim in
`paper/MANUSCRIPT.md`, exiting non-zero on any mismatch. It currently reports **408/408 claims
verified**. It caught eleven genuine errors during drafting, including one substantive misstatement,
and will catch any future divergence between the code and the paper.

Also available: `calibrate_micro.py` (micro effect-size calibration) and `calibrate_abm.py`
(Study 4 regime-reachability search) — both reported in the appendix so the parameterisation is
auditable rather than asserted.

---

## What this repository is and is not

**It is** a complete theory specification, a working formal model, a full analysis pipeline, a
manuscript whose every number is machine-checked against that pipeline, and a design specification
for the confirmatory study — including the required sample size for each hypothesis and the
identification of the one hypothesis that must not be attempted in a survey.

**It is not** empirical evidence about consumers or markets. The five results that would have to
replicate on human participants for the theory to stand are listed in `paper/POSITIONING_MEMO.md` §5,
together with the statement that if the first three fail the theory is wrong and should be abandoned
rather than salvaged.
