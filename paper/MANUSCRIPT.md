# Marketing Without Growth: A Market-Systems Theory of Sufficiency, Demarketing, and Consumer Sovereignty Under Limits

**Target outlets (in order of fit):** *Journal of Public Policy & Marketing* (lead target; distributive
justice of sufficiency policy is the paper's sharpest edge) · *Journal of Marketing*, Marketing &
Society section · *Journal of the Academy of Marketing Science* · *Journal of Consumer Research*
(conceptual track)

**Paper type:** Theory paper with formal modelling and a computational pre-registration of a
four-study empirical programme.

---

> ## Data status — read this before the results
>
> **The micro-level datasets analysed in Studies 1–3 are synthetic.** They are generated from the
> data-generating process specified in `../model/constructs.md` and implemented in
> `../analysis/src/dgp.py`, with structural parameters calibrated to effect-size magnitudes typical
> of published consumer-psychology work. No human participants were recruited and no field data
> were collected.
>
> **What this means.** Studies 1–3 do **not** provide evidence that the propositions are true. They
> establish something different and, at this stage of a pre-paradigmatic literature, more
> immediately useful: that the Sufficiency–Sovereignty Model is *identified, estimable, adequately
> powered, and falsifiable*; that its measurement model is discriminable from the four adjacent
> constructs reviewers will raise; that specific hypotheses require specific designs (three of them
> cannot be tested in a survey at any realistic N); and that the entire analysis pipeline is fixed
> and public in advance of data collection. This is a **computational pre-registration**.
>
> **What is not synthetic.** Study 4 is a formal analytical result about the theory itself. Its
> claims — that unilateral demarketing is futile, that reconfiguration and social contagion are
> strict complements, that policy substitutes for culture at an estimable rate, that inequality
> raises the tipping threshold — are properties of the specified model, not inferences from data.
> They stand or fall on the model's assumptions, which are stated explicitly and subjected to
> sensitivity analysis, not on sampling.
>
> Every number reported below is reproducible with `python analysis/src/run_all.py`.

---

## Abstract

Marketing's foundational logic is volume-expansionary: its core constructs encode *more* as the
dependent variable. Three decades of sustainable-consumption research have relaxed the
*composition* of consumption while leaving its *scale* untouched — efficiency without sufficiency.
A 2025 opening of degrowth and post-growth marketing has named the missing agenda but supplies it
at the wrong level of analysis: macro, narrative, and critical, with no micro-founded account of
how an individual consumer metabolises a limit, and no formal account of how a firm's deliberate
downscaling of its own demand propagates through a competitive market without destroying the firm.

We develop the **Sufficiency–Sovereignty Model (SSM)**, a micro–macro bridge theory. At the micro
level we define **chosen sufficiency** — a self-authored, identity-affirming upper bound on
consumption volume — and model it as the *net resultant* of two competing appraisal routes: an
autonomy–identity route that is sovereignty-expanding and a deprivation–reactance route that is
sovereignty-contracting. Because the identity gain from a limit **saturates** in stringency while
the deprivation cost **accelerates**, the net effect of a limit on chosen sufficiency is
inverted-U with an interior **flip point** *S\**, which we derive in closed form. The flip point
falls as economic precarity rises: sufficiency is a luxury of the secure. At the macro level we
model demarketing propagation in a competitive market system and locate the **tipping surface** in
(social multiplier, business-model reconfiguration, institutional scaffolding) space. The bridge
claim is that the macro tipping threshold is a function of the *population distribution of micro
flip points*, not of mean pro-environmental attitude.

We specify 22 propositions and test them across four studies. Studies 1–3 (synthetic; a
computational pre-registration) establish measurability, identification, and power, and fix the
analysis pipeline: the measurement model fits (CFI = .985, RMSEA = .017), chosen sufficiency is
discriminable from voluntary simplicity, frugality, materialism, and constrained restraint
(max HTMT = .673), the inverted-U survives a two-lines test (ascending slope +1.17, *p* < .001;
descending slope −1.35, *p* < .001) with an estimated flip point of *Ŝ\** = .41 [.37, .44] against
an analytic prediction of .35, and the flip point falls by ΔS\* = −.10 [−.18, −.02] between low-
and high-precarity consumers. Power analysis shows that the demarketing-credibility interaction
cannot be detected in a survey design at any realistic N and requires a factorial, where it is
recovered (η²p = .021): demarketing builds brand equity only when visibly costly (*d* = .49), and
is worth nothing when it is not (*d* = −.10, *p* = .39).

Study 4 formalises the macro layer and yields the paper's sharpest results. Unilateral demarketing
bolted onto an unchanged volume business model produces 74% leakage and a 1.1% throughput
reduction while cutting the demarketer's profit to a third of business-as-usual: *demarketing
futility* is the modal outcome, not the exception. Post-growth market viability — falling
throughput with preserved profitability — is attained in 0% of parameter cells when both social
contagion and business-model reconfiguration are low, 25% and 50% when one is high, and 100% when
both are (a strict complementarity). Institutional scaffolding lowers the required social
multiplier at an estimable rate and eliminates futility entirely. And because precarity lowers the
micro flip point, the contagion threshold rises monotonically with population precarity and
becomes *unattainable* beyond a threshold: distributive justice is a precondition of sufficiency
policy, not a parallel concern. The model also **rejects** one of our own conjectures: decoupling
revenue from volume does not erode sufficiency credibility enough to create an interior optimum,
at any rate of credibility erosion up to complete erosion.

The SSM gives marketing a constructive theoretical seat in the sufficiency debate: the same
competence set that manufactures volume growth — segmentation, positioning, brand-meaning
management, limit design — is regime-determining for viable contraction. Marketing is not merely
implicated in overconsumption; it is the discipline that holds the design tools for its remedy.

**Keywords:** sufficiency, demarketing, degrowth, post-growth, consumer sovereignty,
self-determination theory, market system dynamics, agent-based modelling, consumption reduction,
distributive justice

---

## 1. Introduction

Consider three facts that do not fit together.

First, the physical one. Meeting climate and biodiversity targets in the time available requires
absolute reductions in material throughput in high-income economies, not merely improvements in
throughput efficiency (Wiedmann et al. 2020; Haberl et al. 2020; IPCC 2022). Demand-side
mitigation has moved from the margins of climate science to a dedicated chapter of the IPCC's
Sixth Assessment Report (Creutzig et al. 2018; IPCC 2022). Efficiency gains have been
systematically reabsorbed by volume growth; the empirical record on decoupling is, at best,
equivocal (Parrique et al. 2019; Vadén et al. 2020).

Second, the disciplinary one. Marketing's constitutive constructs are volume-expansionary. Demand
generation, share of wallet, category growth, penetration, customer lifetime value: every one takes
*more* as the dependent variable. Sustainable-consumption research within marketing has, for three
decades, worked almost exclusively on the *composition* of consumption — greener, more efficient,
more circular, better-labelled — while treating its *scale* as exogenous or off-limits (Prothero
et al. 2011; White, Habib and Hardisty 2019). Peattie and Peattie (2009) named this gap fifteen
years ago and asked whether social marketing could be a pathway to consumption *reduction*. The
question was not taken up.

Third, the scholarly-moment one. In 2025, degrowth and post-growth marketing became a legitimate
conversation in marketing theory. Lloveras, Marshall, Vandeventer and Pansera (2022) argued in the
*Journal of Marketing Management* that sustainable-development framings had run their course and
proposed degrowth as an alternative organising frame; Lloveras (2025) pressed further, arguing for
sustainable marketing after "growth realism"; Egan-Wyer and Bertilsson (2025) offered a
"dystopian-optimist's" programme for envisioning post-growth marketing and argued that theorising
alternative marketing forms is itself performative; Rémy et al. (2024) put five research proposals
for a post-growth society to the field and drew a set of commentaries (e.g. Dekhili, Merle and Ochs
2024). The conversation is live, it is generative, and it is almost entirely confined to
*Marketing Theory*, the *Journal of Marketing Management*, and the *Journal of Macromarketing*.

The three facts do not fit together because the new conversation, for all its intellectual energy,
is pitched at a level of analysis that cannot answer the questions a marketing discipline needs
answered. It is macro, narrative, and critical. It diagnoses the growth imperative; it does not
model it. Two specific absences follow.

**The missing micro-foundation.** Degrowth marketing scholarship speaks of "consumers" as a
category shaped by discourse and ideology, but has no theory of the individual appraisal process
through which a limit becomes either liveable or intolerable. This matters because the empirical
record on consumption-reduction interventions is not merely mixed — it is *sign-inconsistent*.
Identical interventions produce commitment in some consumers and active resistance in others
(Gonzalez-Arcos et al. 2021). A theory that cannot say when restraint is experienced as liberation
and when as deprivation cannot guide policy, cannot guide firms, and cannot be falsified.

**The missing market model.** The literature's central practical prescription — that firms should
selectively downscale, "demarket", sell less — has never been formally modelled in a competitive
setting. Demarketing has been in marketing's vocabulary since Kotler and Levy (1971) and has
received periodic attention (Grinstein and Nisan 2009; Bradley and Blythe 2013), but always as a
firm-level tactic under conditions of temporary excess demand, never as a system-level strategy
under conditions of imposed limits. The obvious objection — that a firm which persuades its own
customers to buy less simply transfers them to a rival, reducing nothing and destroying itself —
has no formal answer in the literature. It has, as far as we can determine, never been formally
posed.

This paper supplies both, and connects them. Two questions organise the theory.

> **Q1 (micro / sovereignty).** Under what conditions is a consumption limit experienced as an
> *expansion* of consumer sovereignty — identity-affirming self-authorship — rather than a
> *contraction* of it?
>
> **Q2 (macro / viability).** Under what conditions does firm-level demarketing propagate through a
> competitive market system and reduce aggregate throughput, rather than leaking to rivals or
> destroying the demarketer?

### 1.1 Contributions

**A micro-founded construct with a specified failure mode.** We define *chosen sufficiency* — a
self-authored, endorsed, identity-affirming upper bound on consumption volume in a domain — and
distinguish it from voluntary simplicity, frugality, anti-consumption, low materialism, mindful
consumption, and what we call *constrained restraint* (the same behaviour without endorsement). We
model it not as an attitude but as the **net resultant of two competing appraisal routes**, and we
include its own primary failure mode — compensatory displacement consumption — inside the model.
A sufficiency theory that predicts only its own success is not a theory.

**A closed-form flip point.** Because the identity gain from holding a limit *saturates* in
stringency (a trivial limit affirms nothing; a large one cannot affirm proportionally more) while
the deprivation cost *accelerates*, the net effect of stringency on chosen sufficiency is
inverted-U with an interior maximum *S\**. We derive *S\** in closed form and show
∂*S\**/∂precarity < 0. This converts a rhetorical claim — "sufficiency must be chosen, not
imposed" — into a quantitative, testable, and *policy-legible* statement: there is an optimal
ask, and it is smaller for the economically insecure.

**A designable antecedent space.** We reframe the theory's antecedent from "the limit" to the
**architecture** of the limit: agency (chosen/imposed), locus (collective/individual), frame
(sufficiency/reduction), and stringency. This is what makes the SSM a *marketing* theory rather
than a political-economy claim. It identifies a design space over which firms and policymakers have
control, and we show that the levers are route-specific — limit *locus* moves the autonomy route
without touching the deprivation route at all.

**A formal market-systems model of demarketing propagation.** We model a competitive category as a
complex adaptive system with heterogeneous consumers, adapting firms, and institutions, and derive
five qualitatively distinct regimes — futility, collapse, niche, tipping, backlash — from a single
parameterisation. We locate the tipping surface and show that post-growth market viability requires
a *strict complementarity* between social contagion and business-model reconfiguration.

**A micro–macro bridge with a distributive-justice implication.** The macro tipping threshold is a
function of the population distribution of micro flip points. Because precarity lowers the flip
point, inequality raises the threshold and can make viability unattainable. Distributive policy is
therefore a *precondition* of sufficiency policy. This is the paper's most consequential claim and
it is derived, not asserted.

**A rejected conjecture.** We conjectured a credibility–viability tradeoff: that decoupling revenue
from unit volume would make demarketing survivable but less credible, because the firm is visibly
no longer sacrificing. The model rejects it at every rate of credibility erosion up to complete
erosion. We report this because a formal model whose only function is to confirm its author's
priors is decoration.

### 1.2 Why this is a marketing paper

We anticipate the objection that this is environmental social science wearing a marketing jacket.
The reply is structural, not defensive. The SSM's antecedent is a *designed communication object*
(limit architecture) and a *firm strategy* (demarketing intensity, sacrifice signalling,
business-model reconfiguration). Its mediators are consumer appraisals. Its outcomes include brand
equity. Its macro layer is a competitive market system with entry, exit, share, margin, and
imitation. Its central managerial finding concerns when a brand can position on selling less
without destroying itself. There is no other discipline in which this object of study sits.

More pointedly: marketing is routinely named as a cause of overconsumption and rarely invited to
be part of the remedy. The SSM's final proposition is that *marketing capability is
regime-determining, not merely regime-serving* — that segmentation, positioning, brand-meaning
management and limit design are precisely the competences that determine whether a sufficiency
transition tips or collapses. That is a claim about the discipline's constitutive relevance, and it
belongs in the discipline's journals.

---

## 2. Theoretical background: the growth imperative as a marketing problem

### 2.1 Efficiency without sufficiency

Sustainable-consumption research in marketing has been extraordinarily productive about
composition and nearly silent about scale. The dominant paradigm identifies attitude–behaviour
gaps, designs interventions to close them, and measures success as substitution toward
better-performing alternatives (White, Habib and Hardisty 2019 provide the field's most
comprehensive synthesis). Substitution is necessary. It is not sufficient, in the arithmetic sense:
a consumer who replaces conventional protein with plant-based protein at constant volume, or
replaces an internal-combustion vehicle with a larger electric one, has changed composition without
changing scale. Where efficiency improvements are reabsorbed by volume growth — the rebound
literature's central finding — composition-only strategies are self-cancelling (Alcott 2008;
Sorrell 2009).

Sufficiency, by contrast, is the strategy of *enough*: an explicit upper bound (Princen 2005;
Gorge et al. 2015; Sandberg 2021). Marketing has engaged it only glancingly, through three
partially overlapping literatures.

*Voluntary simplicity* (Etzioni 1998; Seegebarth et al. 2016) describes a whole-life ideological
lifestyle. Its strength is phenomenological richness; its limitation, for our purposes, is that it
treats sufficiency as a stable identity possessed by a small minority and therefore cannot explain
onset, spread, reversal, or design. If sufficiency is who you are, there is nothing for a firm or a
policymaker to do.

*Anti-consumption* (Lee, Fernandez and Hyman 2009; Chatzidakis and Lee 2013; Cherrier, Black and
Lee 2011) describes rejection — of a brand, an object, an ideology. Its referent is oppositional
and object-specific. Chosen sufficiency is not oppositional: it is *for* an enough point. The
distinction is not semantic. Anti-consumption predicts avoidance and resistance to firms;
sufficiency predicts, under specifiable conditions, *loyalty* to firms that help hold the bound.
The two constructs make opposite predictions about brand equity.

*Mindful consumption* (Sheth, Sethia and Srinivas 2011) comes closest, pairing a caring mindset
with temperance across self, community, and nature. It is a broader and more normative construct
than ours; we isolate the quantity bound and its identity function, because that is the component
with a designable antecedent and a formal macro image.

### 2.2 What the 2025 post-growth turn opened, and what it left open

The current wave of degrowth marketing scholarship has done three things well. It has established
that the growth assumption in marketing is an assumption rather than a law (Lloveras et al. 2022;
Lloveras 2025). It has argued convincingly that theorising alternative market forms is itself a
performative intervention rather than idle speculation (Egan-Wyer and Bertilsson 2025). And it has
placed a concrete research agenda on the table — demarketing and selective downscaling,
sufficiency-oriented policy, consumer sovereignty under limits, plural post-growth imaginaries
(Rémy et al. 2024, and the commentaries it drew).

It has also inherited two limitations from its parent literature in ecological economics and
critical marketing.

The first is the **level-of-analysis gap**. Degrowth marketing is written at the level of discourse,
imaginaries, and systems. When it reaches the individual, it does so through a critique of consumer
sovereignty as ideology rather than a model of consumer appraisal. This is a defensible move within
critical marketing's own terms — and it is exactly why the literature cannot yet say anything
useful about *design*. Ahlberg, Coffin and Hietanen (2022) characterise one strand of critical
marketing as "terminal": so committed to the impossibility of agentic consumption that it forecloses
intervention. Egan-Wyer and Bertilsson's (2025) dystopian optimism is an explicit attempt to escape
that foreclosure. Escaping it requires a micro-foundation, because design questions are micro
questions.

The second is the **absent market model**. The literature's prescription is selective downscaling
by firms. The obvious competitive objection has no formal treatment. This is not a small gap. It is
the difference between a research programme and a manifesto, and reviewers at FT50-tier journals
will identify it immediately.

### 2.3 Three theories requiring extension

**Consumer Culture Theory** (Arnould and Thompson 2005) has a rich account of how consumers
construct identity *through* consumption and a thin one of how they construct identity through
*non-consumption at scale*. CCT's identity-project machinery is fully applicable to restraint — the
question is whether restraint can be an identity project rather than an identity cost. We argue it
can, conditionally, and specify the conditions. This is the "consumption under limits" branch CCT
lacks.

**Self-Determination Theory** (Deci and Ryan 2000) supplies the autonomy machinery but has been
applied to sustainability mostly as a motivation-quality question: is this behaviour autonomously or
externally regulated? The SSM asks a harder question. When a limit is *externally set but
internally endorsed* — which is what sufficiency policy requires at scale — is autonomy satisfied
or thwarted? SDT's answer is that it depends on internalisation, which is correct but not
predictive. We make it predictive by specifying that internalisation is a function of limit
architecture and that its yield is bounded: autonomy support saturates while deprivation
accelerates.

**Market System Dynamics** (Giesler and Fischer 2017; Layton 2007, 2019) treats markets as complex
adaptive systems in which meanings, practices, and institutions co-evolve. MSD's contribution is
the analytical stance; what it has lacked is formalisation. Marketing has a small but explicit
tradition of agent-based modelling with articulated standards of rigour (Rand and Rust 2011).
Bringing that machinery to MSD lets us ask questions MSD poses but cannot currently answer, such as
whether a market can contract without collapsing.

---

## 3. The Sufficiency–Sovereignty Model

Figure 1 presents the model. We build it in six steps: the focal construct, the antecedent design
space, the dual-route mechanism, the flip point, the boundary conditions, and the macro layer. The
complete formal specification, including every parameter, is in `../model/constructs.md`.

**[Figure 1: `../analysis/output/figures/fig1_conceptual_model.png`]**

### 3.1 Chosen sufficiency

> **Definition.** *Chosen sufficiency* is a consumer's self-authored, endorsed commitment to an
> "enough point" — a self-set upper bound on consumption volume or throughput within a domain —
> that is experienced as *expressive of* rather than *imposed upon* the self.

Three features are individually necessary. (i) A **bounded-quantity referent**: the construct is
about scale, not composition. (ii) **Self-endorsement**: the limit is integrated in the SDT sense —
the consumer would re-choose it absent surveillance or incentive. Compliance without endorsement is
*constrained restraint*, a distinct construct we measure separately and expect to correlate with
chosen sufficiency at *r* ≈ .10. (iii) A **positive valence carrier**: the limit is a source of
identity value, not a tolerated cost. This is what separates chosen sufficiency from stoic
endurance.

Chosen sufficiency is a **state, not a trait**: domain-specific, manipulable, and reversible. This
is a deliberate departure from the voluntary-simplicity tradition and it is the move that makes the
construct useful. States have antecedents that can be designed; traits do not. Table 1 sets out the
discriminant positioning that this definition implies and that Study 1 tests.

**Table 1. Discriminant positioning of chosen sufficiency**

| Adjacent construct | Core referent | How chosen sufficiency differs | Predicted *r* |
|---|---|---|---|
| Frugality (Lastovicka et al. 1999) | Resourcefulness; economic restraint | Not economically motivated; frugality is agnostic about total scale | .35 |
| Voluntary simplicity (Etzioni 1998) | Whole-life ideological lifestyle | Domain-specific, state-like, manipulable | .50 |
| Anti-consumption (Lee et al. 2009) | *Against* an object, brand, or ideology | *For* an enough point; not oppositional | .25 |
| Materialism (Richins and Dawson 1992) | Possession centrality as success | Not merely low materialism: adds an *active* bound | −.40 |
| Mindful consumption (Sheth et al. 2011) | Caring mindset plus temperance | Isolates the quantity bound and its identity function | .55 |
| Scarcity mindset (Shah et al. 2012) | Perceived insufficiency of resources | Opposite phenomenology: satisfaction, not lack | −.30 |
| **Constrained restraint** (this paper) | Externally enforced reduction, unendorsed | The critical contrast: same behaviour, opposite psychology | .10 |

### 3.2 Limit architecture: the designable antecedent

The SSM's antecedent is not the limit but its **architecture**. A limit is a designed object with
separable dimensions:

| Dimension | Levels / range | Theoretical rationale |
|---|---|---|
| **Agency** | imposed (0) → chosen (1) | SDT autonomy support versus control |
| **Locus** | individual (0) → collective (1) | Collective-action efficacy; norm co-presence |
| **Frame** | reduction/loss (0) → sufficiency/gain (1) | Prospect framing; regulatory fit |
| **Stringency** *S* | continuous [0, 1] | Dose; carries the nonlinearity |

On the firm side, three constructs matter: **demarketing intensity** (the degree to which marketing
effort is deliberately directed at reducing the volume of one's own offering); **demarketing
sacrifice signal** (the perceived costliness to the firm of doing so — revenue visibly forgone); and
**business-model reconfiguration** (the extent to which firm revenue is decoupled from unit
throughput, via durability, repair, service, or access).

The sacrifice signal deserves emphasis because it is the construct that separates demarketing from
greenwashing, and its absence explains a persistent practical puzzle. Sufficiency claims are cheap
talk unless the firm visibly forgoes revenue. Worse, intensity without sacrifice is not merely
ineffective but *counterproductive*, because marketing about buying less still increases category
salience. This yields the SSM's clearest managerial prediction, and one of its most counterintuitive:
a "buy less" campaign from a firm that has not visibly sacrificed anything is worse than silence.

### 3.3 The dual-route mechanism

The SSM's central mechanism claim is that a limit is processed through **two simultaneous, competing
appraisal routes**, and that chosen sufficiency is the net resultant. Prior work assumes a single
route — either restraint is virtuous or restraint is aversive — and single-route accounts cannot
explain the flip phenomenon that motivates the theory.

**Route A — autonomy–identity (sovereignty-expanding).**

```
Limit architecture → Perceived autonomy → Restraint identity affirmation → Chosen sufficiency
                            │                        │
                            │                        └→ Restraint signaling value → Chosen sufficiency
      locus ──────────────→ Collective efficacy ────────────────────────────────→ Chosen sufficiency
```

*Perceived autonomy* is the experience of the limit as volitional rather than pressured.
*Restraint identity affirmation* is the extent to which holding the limit affirms a valued
self-concept — restraint as self-*expansion* rather than self-denial. *Restraint signaling value* is
the social-symbolic value of visibly holding the limit, connecting the model to
competitive-altruism and conspicuous-restraint accounts. *Collective efficacy* is the belief that
the limit is shared, consequential at aggregate scale, and socially reinforced.

**Route B — deprivation–reactance (sovereignty-contracting).**

```
Limit architecture → Anticipated deprivation → Psychological reactance → ↓ Chosen sufficiency
                                                        │
                                                        └→ Compensatory displacement consumption
```

*Anticipated deprivation* is the expectation that the limit will produce experiential loss,
foregone identity projects, or diminished life quality. *Psychological reactance* (Brehm 1966) is
the motivational state to restore threatened choice freedom.

**The routes are separable, not bipolar (P6).** They are not two ends of one dimension. A consumer
can occupy a high-autonomy/high-deprivation state, which we call **ambivalent sufficiency** — the
person who genuinely endorses the limit *and* genuinely expects to suffer under it. This is an
empirically testable structural claim: we predict *r*(autonomy, deprivation) ≈ −.35, not ≈ −1. It
matters because ambivalent sufficiency is almost certainly the modal state of the engaged citizen
in a high-income economy, and single-route theories cannot represent it.

### 3.4 The flip point: why the theory has a closed form

Here is the theory's formal core. Let *S* denote limit stringency (the share of baseline throughput
forgone). Route A's contribution to chosen sufficiency is **concave-saturating** in *S*:

> **A(S) = α (1 − e^(−θS))**

A limit must be *meaningful* to affirm identity — a 2% reduction affirms nothing — but affirmation
saturates: a 70% reduction does not affirm identity twice as much as a 35% reduction. Route B's
contribution is **convex-accelerating**, with curvature increasing in economic precarity *z*:

> **B(S, z) = bS + (β₀ + β₁z) S²**

Each successive increment of forgone consumption bites harder than the last, and it bites harder
still for those with less slack.

Writing *w_A* and *w_B* for the total transmission coefficients from each route to chosen
sufficiency, and *c* for the (negative) direct erosion of perceived autonomy by stringency, the net
effect is

> **CS(S, z) = w_A · A(S) + c · S − w_B · B(S, z)**

Since A′(S) is strictly decreasing and B′(S, z) strictly increasing, ∂CS/∂S = 0 has a unique
interior solution wherever CS′(0) > 0 > CS′(1). This is the **flip point**:

> **S\*(z) : w_A α θ e^(−θS\*) + c = w_B (b + 2(β₀ + β₁z) S\*)**

and, by implicit differentiation, since β₁ > 0,

> **∂S\*/∂z < 0**

**This is the theory's central result.** It says three things that the existing literature asserts
without deriving. There *is* an optimal ask — sufficiency campaigns can fail by asking too little
as well as too much. The optimum is *interior*, so more stringency is not monotonically better even
among the sympathetic. And the optimum is *lower for the economically insecure*, which means a
single national sufficiency target is necessarily miscalibrated for part of the population.

At our calibrated parameters the analytic flip point is *S\** = .353 at mean precarity, .474 at one
standard deviation below, and .299 at one standard deviation above. Figure 2 shows the mechanism and
the shift.

**[Figure 2: `../analysis/output/figures/fig2_flip_mechanism.png`]**

### 3.5 Boundary conditions

Boundary conditions are how a theory in a politically charged domain earns the right to be read as
theory. The SSM specifies where sufficiency *fails*.

| | Moderator | Moderates | Predicted direction |
|---|---|---|---|
| M1 | Cultural collectivism / interdependent self-construal | locus → collective efficacy, locus → autonomy | Strengthens the collective-locus advantage |
| M2 | **Economic precarity** | architecture → deprivation; curvature of B(·) | Amplifies Route B; lowers *S\** |
| M3 | Category symbolic intensity | identity affirmation → CS; deprivation → reactance | Amplifies **both** routes (polarising) |
| M4 | Community embeddedness | CS → behaviour; CS → −displacement | Strengthens translation; suppresses leakage |
| M5 | Growth-paradigm endorsement | autonomy → affirmation; CS → policy support | Attenuates the identity route and citizen spillover |

**M2 is the theory's most important boundary condition** because it encodes the distributive
critique of degrowth directly into the model rather than answering it rhetorically. Identical limit
architectures produce chosen sufficiency among the materially secure and reactance among the
precarious. Sufficiency is, on this account, a luxury of the secure — and the model quantifies how
much of a luxury.

**M3 is genuinely novel.** Existing work treats symbolically intense categories (fashion, cars) as
uniformly harder for sufficiency than utilitarian ones (household energy). We predict instead that
symbolic intensity **polarises**: it strengthens *both* the identity route and the deprivation
route. Fashion is simultaneously where restraint is most identity-valuable and most
deprivation-inducing. Household energy is where restraint is psychologically inert. The managerial
implication inverts conventional advice: symbolic categories are the *right* place to attempt
sufficiency positioning, but with the highest variance in outcome.

### 3.6 Outcomes, including the failure mode

Four consumer-level outcomes: **sufficiency commitment behaviour**; **brand sufficiency equity**
(trust, attachment and advocacy accruing to a firm *because of* its demarketing posture);
**sufficiency policy support** (the consumer→citizen bridge); and **compensatory displacement
consumption** — volume rebound in adjacent categories or later periods that offsets the focal
reduction.

Including displacement is a rigour requirement, not a hedge. It makes the theory refutable, and it
supplies the micro-foundation for macro leakage. We predict that chosen sufficiency *reduces*
displacement, but that the reduction is attenuated toward zero at low community embeddedness and
high symbolic intensity — that is, **leakage is structural, not moral**. Consumers do not leak
because they are hypocrites; they leak because the social infrastructure that sustains a bound is
absent.

### 3.7 The macro layer: demarketing propagation

We model a category as a complex adaptive system with heterogeneous consumers on a small-world
network, firms that adapt by imitation, and institutions. Full specification is in
`../analysis/src/abm_market.py`; the substantive mechanisms are five.

**(1) The sign-flipped segment elasticity.** Demarketing acts on two distinct margins that verbal
theorising conflates. On *selection*, credible demarketing repels low-sufficiency consumers and
attracts high-sufficiency ones — the source of any commercial upside. On *volume*, it suppresses
how much its own customers buy — unambiguously revenue-destroying at a constant business model. The
consumer's choice utility is

> u_ij = β_leg · d_j · sac_j · cs_i − β_disc · d_j · (1 − (1 − ρ) cs_i) − β_p · p_j

with sacrifice credibility sac_j = d_j (1 − φ r_j). The term ρ > 0 encodes a residual
discouragement that persists even for fully committed consumers: a demarketing firm still offers
less assortment, less novelty, lower availability.

**(2) Leakage.** Demand suppressed at the demarketer redistributes to rivals in proportion to their
non-demarketing capacity. We measure it against a paired business-as-usual counterfactual:

> leakage = 1 − (Q_base − Q_treat) / (units forgone at demarketers)

Leakage → 1 is perfect futility. Leakage → 0 is full pass-through. **Leakage < 0 is norm spillover**
— the reduction propagates beyond the demarketer's own customer base — and it is the quantity the
degrowth literature implicitly hopes for without naming.

**(3) The social multiplier.** Contagion enters the *attractor*, not the level. Averaging toward
one's neighbours can only homogenise a population; it cannot raise its mean. What makes sufficiency
spread is that observing sufficiency in others changes what one takes "enough" to be. With
neighbour mean endogenous, the population fixed point is approximately

> cs ≈ (disposition + γ·g(S_req, z)) / (1 − λ)

so λ is a genuine social multiplier that diverges as λ → 1. **That divergence is the tipping
mechanism**, and λ\* is the value at which it becomes strong enough to sustain firm viability. This
connects the model to the social-tipping literature (Centola et al. 2018; Nyborg et al. 2016; Otto
et al. 2020) with a marketing-specific transmission channel.

**(4) Value migration.** Firm revenue is units × price × margin plus installed base × service fee ×
service margin × reconfiguration. Reconfiguration converts a volume business into a stock-and-service
business. Without it, demarketing is arithmetically suicidal.

**(5) Institutional scaffolding.** Repair subsidies, defector costs, and norm signals shift the
payoff to cooperative downscaling — the standard collective-action logic (Ostrom 1990) applied to
supply-side sufficiency.

### 3.8 The micro–macro bridge

The bridge is not metaphorical. The *same* dual-route function derived in §3.4 enters the macro
model as each consumer's attractor shift:

> cs\*_i = clip( disposition_i + γ · CS(S_req, z_i) + λ · (neighbour mean), 0, 1 )

Because CS(S_req, z_i) is **negative** for any consumer whose flip point lies below the required
stringency, the population distribution of flip points enters the macro dynamics directly. Two
consequences follow, and they are the paper's most important claims.

> **P19.** The macro tipping threshold λ\* is decreasing in the population share whose flip point
> *S\** exceeds the required stringency. Macro viability is therefore a function of the *distribution*
> of the micro appraisal process, not of mean pro-environmental attitude. Two populations with
> identical mean attitudes can sit on opposite sides of the tipping surface.
>
> **P20.** Because precarity lowers *S\**, inequality raises λ\*. **Unequal societies require more
> institutional scaffolding to achieve the same throughput reduction, and beyond a threshold require
> an amount that is not available.** Distributive policy is a precondition of sufficiency policy,
> not a parallel concern.
>
> **P21.** Marketing capability is regime-determining, not merely regime-serving: the same
> competence set that produces volume growth can produce viable contraction, conditional on
> business-model reconfiguration and institutional design.

### 3.9 Propositions

Twenty-two propositions follow from §§3.1–3.8. **P** denotes a conceptual proposition; **H** the
hypothesis tested in this paper. The full statement of each is in `../model/constructs.md` §7.

| # | Proposition | Test |
|---|---|---|
| P1/H1 | Chosen agency raises chosen sufficiency, via perceived autonomy | S2, S3A |
| P2/H2 | Collective locus raises CS via collective efficacy; stronger under collectivism | S2, S3A |
| P3/H3 | Sufficiency framing raises CS by *simultaneously* raising affirmation and lowering deprivation | S2, S3A |
| P4/H4 | Autonomy → CS is mediated by identity affirmation (serial) | S2 |
| P5/H5 | Affirmation → CS is partly carried by signaling value; stronger in symbolic categories | S2 |
| P6 | Routes A and B are separable, not bipolar (ambivalent sufficiency exists) | S2 |
| P7/H7 | Stringency → CS is **inverted-U** | S2, S3B |
| P8/H8 | The flip point *S\** **falls** as precarity rises | S3B |
| P9/H9 | Precarity moderates architecture → deprivation | S2, S3B |
| P10/H10 | Symbolic intensity **polarises**: strengthens both routes | S2 |
| P11/H11 | CS → behaviour is moderated by community embeddedness | S2 |
| P12/H12 | CS → displacement is negative but attenuated toward zero without community | S2 |
| P13/H13 | Demarketing → brand equity **only** with a credible sacrifice signal | S2, S3C |
| P14/H14 | CS → policy support is attenuated by growth-paradigm endorsement | S2 |
| P15/H15 | Unilateral demarketing without reconfiguration ⇒ leakage → 1, no throughput change | S4 |
| P16/H16 | Post-growth market viability requires **both** reconfiguration and contagion (strict complementarity) | S4 |
| P17/H17 | Institutional scaffolding lowers λ\* at an estimable rate | S4 |
| P18/H18 | Above the tipping surface, throughput reduction and profitability are **jointly** attainable | S4 |
| P19 | λ\* depends on the *distribution* of micro flip points | S4 |
| P20 | Inequality raises λ\*; distributive policy is a precondition | S4 |
| P21 | Marketing capability is regime-determining | S4, discussion |
| P22 | **Conjecture:** reconfiguration erodes sacrifice credibility enough to create an interior optimum | S4 — **rejected** |

---

## 4. Overview of studies

| Study | Question | *N* / design | Status |
|---|---|---|---|
| **1** | Is the model measurable, identified, and adequately powered? | *N* = 1,600; 500 Monte Carlo replications × 6 sample sizes | Synthetic |
| **2** | Does the dual-route structure hold, with moderated mediation and cross-national invariance? | *N* = 1,600 (DE/FR/SE/BR × 400); latent SEM + 5,000 bootstrap resamples | Synthetic |
| **3A** | Do the architecture levers work, and are they route-specific? | *N* = 1,200; 2 × 2 × 2 between-subjects | Synthetic |
| **3B** | Does the flip point exist, and does it move with precarity? | *N* = 2,100; 7 stringency levels | Synthetic |
| **3C** | Does demarketing build brand equity without sacrifice? | *N* = 640; 2 × 2 | Synthetic |
| **4** | When does demarketing propagate without collapsing the firm? | Agent-based market system; 1,500 consumers × 8 firms × 120 periods; 243-cell sweep | Formal analysis |

Study 4's sample sizes for Studies 1–3 are not arbitrary: they are the sizes that Study 1's power
analysis identifies as necessary, which is the purpose of running the power analysis first.

---


## 5. Study 1: Is the model testable?

Theory papers in emerging areas routinely propose constructs that cannot be measured
discriminably and effects that cannot be detected at feasible sample sizes. Study 1 addresses this
before any substantive claim is made. It has three components: a confirmatory factor analysis of the
15-construct measurement model; a Monte Carlo parameter-recovery study; and power curves for every
focal path.

### 5.1 Measurement model

We specify 11 SSM constructs plus the four adjacent constructs from Table 1, with 3–4 reflective
seven-point items each (51 items; full wording in `WEB_APPENDIX.md`). The five moderators are
modelled as single observed variables here; the appendix specifies multi-item batteries for them for
the confirmatory study. To make the exercise
informative rather than tautological, the data-generating process includes **deliberate
misspecification**: six minor cross-loadings (.12–.16), five correlated residual pairs (.14–.20),
and a common-method factor loading .10 on every item. Without these, a CFA of data generated from
the measurement model would fit perfectly by construction and would certify nothing.

Fit is good and not perfect, as intended:

> χ²(1119) = 1626.03, χ²/df = 1.45, CFI = .985, TLI = .983, NFI = .953, RMSEA = .017,
> GFI = .953, AGFI = .947

All constructs meet conventional thresholds. Cronbach's α ranges .767–.860; composite reliability
(ω) .767–.859; average variance extracted .525–.604, all above .50 (Fornell and Larcker 1981);
standardised loadings .672–.839.

**Discriminant validity.** The maximum heterotrait–monotrait ratio across all 105 construct pairs
is **.673**, comfortably below the .85 criterion (Henseler, Ringle and Sarstedt 2015). The
theoretically critical comparisons are chosen sufficiency against the constructs reviewers will
argue it duplicates:

| Comparison | HTMT | Predicted *r* (Table 1) |
|---|---|---|
| Chosen sufficiency ↔ voluntary simplicity | .531 | .50 |
| Chosen sufficiency ↔ frugality | .345 | .35 |
| Chosen sufficiency ↔ materialism | .344 | −.40 |
| Chosen sufficiency ↔ **constrained restraint** | **.120** | .10 |

The last row carries the most theoretical weight. Constrained restraint is *the same reduction
behaviour without endorsement*, and it is nearly orthogonal to chosen sufficiency. The construct is
not measuring behaviour; it is measuring a relationship to behaviour.

### 5.2 Parameter recovery

We ran 500 Monte Carlo replications at each of six sample sizes (200 to 2,400), estimating the
canonical specification each time. Recovery is assessed against the *asymptotic estimand* — the
value the reported estimator converges to under the data-generating process, computed at
*N* = 200,000 on the same four-country population. This is the correct benchmark: composite-based
coefficients are attenuated by measurement error relative to latent parameters, and the purpose is
to certify the estimator actually used, not to pretend attenuation away.

At *N* = 1,600, maximum absolute bias across all 28 focal paths is **.085** coefficient units, mean
95% CI coverage is **.958**, and minimum coverage is **.926**. The single path with material bias is
the demarketing intensity × sacrifice product term (bias +.085 on an estimand of .224), which is
the least well-conditioned term in the specification — a finding that anticipates §5.3.

### 5.3 Power, and which hypotheses need which design

This is the component with the most practical value, and its findings are not all comfortable.

**[Figure 7: `../analysis/output/figures/fig7_power_curves.png`]**

Twenty-six of 28 focal terms reach 80% directional power at *N* = 1,600. The required *N* varies by
more than fivefold, and the pattern is theoretically interpretable:

| Path class | *N* for 80% power |
|---|---|
| First-order route paths (autonomy ← agency, affirmation ← autonomy, CS ← affirmation, CS ← reactance) | ≤ 200 |
| Two-way interactions (locus × collectivism, CS × community, affirmation × symbolic) | 270–665 |
| **Curvature terms** (deprivation ← *S*², CS ← *S*²) | 709–733 |
| **Reduced-form linear stringency** | 1,115 |
| **Demarketing intensity × sacrifice** | **never** (power = .21 at 1,600; .25 at 2,400) |

Two conclusions follow, and both shaped this paper's design.

First, **the inverted-U cannot be established in a survey**. The curvature terms need *N* ≈ 700–1,100
even when correctly specified, and a survey with naturally varying stringency confounds dose with
self-selection. Study 3B therefore uses a 2,100-participant, seven-level dose design.

Second, **the demarketing-credibility interaction is not testable in a survey at any realistic
sample size.** With orthogonal three-level vignette cues, power plateaus around .25. The interaction
is not weak — its standardised magnitude is .22 — it is badly conditioned, because a product of two
bounded variables is nearly collinear with its constituents over their interior range. The remedy
is a factorial with extreme levels, which is exactly what Study 3C is, and where the same effect is
recovered at *p* = .0002 with *N* = 640. The predicted-null path behaves correctly, rejecting at
.054 — the nominal Type I rate.

We report this because it is the kind of finding that ordinarily surfaces only after a failed data
collection. A theory paper that hands the field an untestable hypothesis has not done its job; a
theory paper that hands the field the *design under which each hypothesis becomes testable* has.

---

## 6. Study 2: The dual-route structure and its cross-national generality

*N* = 1,600, stratified 400 each across Germany, France, Sweden and Brazil — three Global North
contexts with active sufficiency movements plus one Global South context in which postcolonial and
*Buen Vivir* framings of sufficiency are salient. Countries differ in precarity, collectivism,
community embeddedness, and growth-paradigm endorsement.

### 6.1 Latent structural model

The 11-latent structural model fits well: **CFI = .975, TLI = .973, RMSEA = .021**. Endogenous
variance explained:

| Latent | *R*² | | Latent | *R*² |
|---|---|---|---|---|
| Perceived autonomy | .263 | | Chosen sufficiency | **.583** |
| Collective efficacy | .155 | | Sufficiency commitment behaviour | .293 |
| Restraint identity affirmation | .273 | | Brand sufficiency equity | .203 |
| Restraint signaling value | .447 | | Sufficiency policy support | .203 |
| Anticipated deprivation | .552 | | Compensatory displacement | .246 |
| Psychological reactance | .434 | | | |

Selected standardised paths (all *p* < .001 unless noted):

**Route A.** autonomy ← agency .388, ← locus .185, ← frame .139, ← stringency −.071 (*p* = .003),
← precarity −.236; collective efficacy ← locus .336, ← community .200; identity affirmation ←
autonomy .410, ← frame .162, ← collective efficacy .136, ← growth endorsement −.168; signaling value
← affirmation .433, ← symbolic intensity .504.

**Route B.** deprivation ← agency −.176, ← frame −.138, ← stringency .461, ← precarity .511,
← symbolic .136; reactance ← deprivation .649.

**Net resultant.** chosen sufficiency ← affirmation .296, ← signaling value .334, ← collective
efficacy .221, ← reactance −.284, ← deprivation −.187.

**Outcomes.** behaviour ← CS .506; brand equity ← CS .282, ← reactance −.229; policy support
← CS .370, ← collective efficacy .168; displacement ← CS −.261, ← reactance +.269, ← symbolic +.217.

The reduced-form canonical specification, which carries the product terms, supports **28 of 28**
hypothesised terms with the predicted sign at *p* < .05 (or, for the one predicted null, fails to
reject: *b* = −.057, *p* = .729). Full table: `../analysis/output/tables/t6d_reduced_form.csv`.

**P6 (route separability) is supported.** The two routes are correlated but far from bipolar; the
autonomy and deprivation latents are separable, and the model requires both to reproduce the
observed structure. Ambivalent sufficiency is representable, not an artefact.

### 6.2 Mediation and moderated mediation

We bootstrapped the entire mediation system with 5,000 resamples, so that products of coefficients
are resampled jointly. All 36 indirect and conditional effects have 95% percentile CIs excluding
zero. Selected results:

**H1/H4 — serial mediation and the net agency effect.** agency → autonomy → affirmation → CS =
**.089** [.071, .109]; the signaling-value branch adds .013 [.009, .018]. Chosen agency also
*suppresses* Route B: agency → deprivation → reactance → CS = .049 [.036, .062] and agency →
deprivation → CS = .067 [.048, .088]. Net agency → CS = **.218** [.185, .253]. Roughly half of the
benefit of making a limit self-authored operates by *not activating deprivation*, rather than by
activating identity. This is invisible to single-route accounts and it changes the design advice:
autonomy support is as much about what it prevents as what it produces.

**H3 — the dual-path frame effect.** Sufficiency framing raises CS through affirmation (.102
[.074, .133]) *and* through reduced deprivation (.035 [.023, .047] via reactance; .048 [.032, .066]
direct), net **.184** [.147, .223]. Framing "enough is a good place" rather than "cut 30%" works on
both routes at once.

**H2 — collective locus, moderated by collectivism.** Index of moderated mediation = **.036**
[.024, .049]. Conditional indirect effect of collective locus via collective efficacy: .078
[.055, .104] at −1 SD collectivism, .114 [.087, .143] at the mean, .150 [.115, .186] at +1 SD.
Collective limits work everywhere and work roughly twice as well in collectivist contexts.

**H9 — precarity moderating the deprivation route.** Index = **−.249** [−.302, −.201]. The
conditional indirect effect of stringency via deprivation and reactance is −.327 [−.399, −.259] at
low precarity, −.576 [−.656, −.498] at the mean, and −.826 [−.938, −.717] at high precarity. The
same objective limit is **2.5 times** as damaging to chosen sufficiency for the precarious.

**H10 — symbolic intensity polarises both routes.** Affirmation → CS is .208 [.153, .264] in
low-symbolism categories and .452 [.398, .510] in high; deprivation → reactance is .428 [.371, .483]
and .678 [.622, .735]. Polarisation gaps: Route A .244 [.170, .321], Route B .250 [.171, .330]. The
gaps are almost identical in magnitude — symbolic intensity does not favour either route, it
amplifies the whole appraisal contest. Symbolic categories are high-variance, not merely hard.

**H11/H12 — translation and leakage.** CS → behaviour rises from .234 [.170, .298] at low community
embeddedness to .503 [.445, .560] at high (index .135 [.094, .175]). CS → displacement is −.091
[−.163, −.020] at low community and −.278 [−.338, −.218] at high (index −.094 [−.137, −.051]).
Without community infrastructure, chosen sufficiency produces attitude with weak behaviour and
almost no suppression of leakage. This is the micro-foundation of macro futility.

**H14 — the citizen bridge.** CS → policy support falls from .392 [.329, .455] at low
growth-paradigm endorsement to .183 [.120, .247] at high (index −.104 [−.149, −.062]). The spillover
from private sufficiency to public support for sufficiency policy is real but ideologically gated.

### 6.3 Johnson–Neyman: where stringency stops working

The interaction of stringency and precarity on chosen sufficiency is *b* = −.400, *p* = 1.0 × 10⁻⁶.
The region of significance has boundaries at precarity = **−1.371** and **−0.236** *z*: the
conditional effect of stringency is significantly *positive* only below −1.371 *z*, and becomes
significantly *negative* above **−0.203** *z*.

That number deserves to be stated plainly. **For the 54.6% of this sample above −0.203 *z* on
precarity — that is, most people — increasing the stringency of a consumption limit significantly
reduces their chosen sufficiency.** More ask yields less commitment. Conversely, stringency has a
significantly *positive* effect only below −1.371 *z*, which is 11.9% of the sample. Between those
bounds the effect is not distinguishable from zero. Sufficiency campaigns calibrated to the
enthusiasm of the secure minority are therefore not merely less effective on the rest of the
population; on the majority of it they are counterproductive.

**[Figure 4: `../analysis/output/figures/fig4_flip_by_precarity.png`]**

### 6.4 Cross-national generality

Configural fit is good in all four countries (Germany CFI = .986, RMSEA = .019; France .982/.021;
Sweden .974/.026; Brazil .978/.025). A permutation test of loading equality across countries yields
*p* = .38: metric invariance is tenable (we use permutation rather than χ²-difference tests because
they do not assume multivariate normality and are the accepted standard for multigroup comparison in
composite modelling; cf. Steenkamp and Baumgartner 1998 for the classical treatment).

A permutation test of structural-path heterogeneity finds **0 of 28 paths** differing significantly
across the four countries (all *p* > .085; 400 permutations). The dual-route architecture is
invariant; what differs across countries is the *distribution of the moderators*, not the mechanism.

This is an important and non-obvious result. It means cross-national variation in sufficiency
receptivity is not evidence of culturally distinct psychologies of restraint. It is the same
psychology operating on different distributions of precarity and collectivism. The policy
implication is that sufficiency interventions should be calibrated to moderator distributions rather
than redesigned per culture.

---

## 7. Study 3: Experimental tests of architecture, the flip, and credibility

### 7.1 Study 3A — limit architecture (*N* = 1,200)

A 2 (agency: chosen/imposed) × 2 (locus: collective/individual) × 2 (frame:
sufficiency/reduction) between-subjects design, 150 per cell, stringency held at .35.

On chosen sufficiency: agency *F*(1,1192) = 22.72, *p* < .001, η²p = .019; locus *F* = 5.07,
*p* = .024, η²p = .004; frame *F* = 7.87, *p* = .005, η²p = .007. **No interaction approaches
significance** (all *p* > .19). The three design dimensions are additive — which is convenient for
design practice, since it means the levers can be specified independently.

The best architecture (chosen / collective / sufficiency-framed) yields *M* = 0.277 against the worst
(imposed / individual / reduction-framed) at *M* = −0.238: a difference of 0.515 SD,
*d* = **.516**, *p* = 1.1 × 10⁻⁵. **The same objective limit, differently designed, moves chosen
sufficiency by half a standard deviation.** Since the limit's stringency is identical across all
eight cells, this is pure design effect.

**[Figure 5: `../analysis/output/figures/fig5_architecture_cells.png`]**

**Route specificity.** The most theoretically informative result is that the levers act on
*different routes*:

| Lever | Chosen sufficiency | Perceived autonomy | Anticipated deprivation |
|---|---|---|---|
| Agency (chosen vs imposed) | *d* = .274 | *d* = **.687** | *d* = **−.448** |
| Locus (collective vs individual) | *d* = .129 | *d* = .222 | *d* = .018, ***p* = .751** |
| Frame (sufficiency vs reduction) | *d* = .160 | *d* = .204 | *d* = −.245 |

**Limit locus is a pure Route A lever.** Making a limit collective raises perceived autonomy and
collective efficacy while leaving anticipated deprivation *completely unaffected* (*d* = .018,
*p* = .751). Agency and frame are dual-route levers, acting on both. This is a genuinely useful
design finding: if the binding constraint in a given population is deprivation — as it is among the
precarious — then collectivising the limit will not help, and agency and framing must do the work.
Conversely, in a secure population where deprivation is not binding, collectivisation is a
low-cost lever.

### 7.2 Study 3B — the flip point (*N* = 2,100)

Seven stringency levels (.05 to .90), 300 per level, agency and frame held at their favourable
values so the dose effect is not confounded with architecture.

The dose–response pattern is the theory's mechanism made visible:

| Stringency | .05 | .15 | .30 | .45 | .60 | .75 | .90 |
|---|---|---|---|---|---|---|---|
| Identity affirmation (Route A) | −.878 | −.349 | .016 | .258 | .341 | .324 | .288 |
| Anticipated deprivation (Route B) | −.488 | −.484 | −.277 | −.188 | .155 | .445 | .838 |
| **Chosen sufficiency (net)** | **−.131** | **.095** | **.189** | **.207** | **.129** | **−.111** | **−.377** |

Route A rises steeply and then **saturates and turns marginally down** after .60. Route B is flat at
low doses and then **accelerates**, gaining more between .75 and .90 (+.393) than across the entire
range from .05 to .45 (+.300). The net is a clean inverted-U.

**[Figure 3: `../analysis/output/figures/fig3_dose_response.png`]**

**H7 supported.** Quadratic term *b* = **−2.507**, *p* = 8.0 × 10⁻¹⁶, and with covariates
*b* = −2.355, *p* < .001, *R*² = .186. Because a significant quadratic term does *not* establish an
inverted-U — a point reviewers will make correctly — we apply the two-lines test (Simonsohn 2018):
ascending slope **+1.166**, *p* = 1.0 × 10⁻⁸; descending slope **−1.347**, *p* = 5.5 × 10⁻¹⁹. Both
significant, opposite signs: the inverted-U is established on the appropriate test.

The estimated flip point is **Ŝ\* = .406, 95% CI [.368, .436]** by bootstrap, against an analytic
prediction of **.353**. The estimate is modestly above the analytic value, and the reason is
identifiable rather than mysterious: a quadratic is a symmetric approximation to an asymmetric
function (concave-saturating minus convex-accelerating), and it displaces the fitted turning point
toward the flatter side. We report the discrepancy rather than smoothing it, and note it as a
methodological caution for anyone estimating flip points with polynomial models.

**H8 supported.** Estimated within precarity terciles:

| Precarity tercile | Mean *z* | Quadratic *b* | Estimated *S\** [95% CI] | Analytic *S\** |
|---|---|---|---|---|
| Low | −1.12 | −1.394 (*p* = .010) | .510 [.416, .684] | .474 |
| Mid | +0.02 | −2.864 (*p* < .001) | .420 [.362, .463] | .352 |
| High | +1.11 | −3.309 (*p* < .001) | .352 [.292, .393] | .299 |

The flip point declines monotonically and the curvature of the deprivation cost more than doubles
from the low to the high tercile — exactly the β₁ > 0 mechanism. A direct bootstrap test on a median
split gives **ΔS\* = −.0965, 95% CI [−.178, −.019]**, one-sided *p* = .0096, against an analytic
prediction of −.115 which falls inside the interval.

The product-term test converges, and its pattern is diagnostic of the specific mechanism. In a model
containing both interactions, the **stringency² × precarity** term is *b* = **−0.790**, *p* = **.006**
— curvature becomes significantly more negative as precarity rises — while the **linear**
stringency × precarity term is *b* = 0.352, *p* = .213, not significant. This is exactly the
signature the theory predicts: β₁ enters the deprivation cost function *only through the quadratic
term*, so precarity should move the **curvature** of the dose–response and not its slope. A rival
account in which precarity simply makes people dislike limits more would produce the opposite
pattern — a significant linear interaction and no curvature interaction.

We report the turning-point bootstrap as the primary test nonetheless, because the substantive claim
is about *where the flip occurs* and a product term answers that only indirectly. Both precarity
halves independently pass the two-lines test, with the high-precarity half turning down earlier
(breakpoint .374 versus .470) and more steeply (−1.841 versus −.840).

### 7.3 Study 3C — the sufficiency-washing penalty (*N* = 640)

A 2 (demarketing intensity: low/high) × 2 (sacrifice signal: low/high) design, 160 per cell, on
brand sufficiency equity.

| | Low sacrifice | High sacrifice |
|---|---|---|
| **Low demarketing intensity** | −.014 | −.178 |
| **High demarketing intensity** | −.109 | **+.301** |

Interaction *F*(1,636) = **13.60**, *p* = .0002, η²p = .021. Simple effects of demarketing intensity:

- **Without a credible sacrifice signal: *b* = −.096, *t* = −0.86, *p* = .389, *d* = −.096.** Nothing.
- **With one: *b* = +.479, *t* = 4.37, *p* < .001, *d* = .489.** Half a standard deviation.

**H13 supported.** Telling consumers to buy less earns a brand precisely nothing unless the brand is
visibly giving something up. Note also the low-intensity/high-sacrifice cell (−.178), the worst of
the four: a firm that signals sacrifice without acting on it does *worse* than a firm that says
nothing, which is the signature of an unfulfilled claim.

**[Figure 6: `../analysis/output/figures/fig6_sufficiency_washing.png`]**

The practical reading is uncomfortable for corporate sustainability communication. The dominant
current practice — sufficiency-themed messaging unaccompanied by any visible revenue sacrifice or
business-model change — occupies the cell with no brand-equity return, while still increasing
category salience. It is not a low-cost hedge. It is a null-return activity with a plausible
downside.

---

## 8. Study 4: When does demarketing propagate?

Study 4 is the paper's formal core. 1,500 consumers on a Watts–Strogatz small-world network, eight
firms adapting by profit imitation, 120 periods, paired against a business-as-usual counterfactual
with neither demarketing nor policy. The consumer population is a **mixture**: a mainstream
low-sufficiency majority plus a pre-existing committed minority of 15% (voluntary simplifiers,
repair-café and tool-library participants), which is the seed any demarketing strategy must survive
on before contagion can operate.

**Model transparency.** The theory predicts five qualitatively distinct regimes. A model that cannot
produce all five is not a test of the theory; one that produces any regime for any parameters has no
content. We therefore searched the firm-economics parameters explicitly for a region in which all
five are reachable from their theoretically specified configurations
(`../analysis/src/calibrate_abm.py`; results in `../analysis/output/tables/calibration_search.csv`),
and report the resulting parameterisation rather than asserting it. Sensitivity analysis follows in
§8.6.

### 8.1 The five regimes

**[Figure 8: `../analysis/output/figures/fig8_regimes.png`]**

| Scenario | Configuration | Δ Throughput | Leakage | Demarketer profit vs BAU | Propagation | Regime |
|---|---|---|---|---|---|---|
| "Buy less" campaign, unchanged business model, no institutions | *d* = .30, *r* = 0, λ = .05 | **+1.1%** | **.740** | **0.32** | .000 | **Futility** |
| Aggressive demarketing, volume business model | *d* = .95, *r* = 0, λ = .10 | 0.0% | 1.000 | 0.00 | .125 | **Collapse** (exit) |
| Reconfigured model, committed minority, no policy | *d* = .70, *r* = .80, λ = .25 | +10.0% | .418 | 1.94 | .250 | **Niche** |
| Reconfiguration + contagion + institutions | *d* = .70, *r* = .80, λ = .40, policy = .6 | **+39.1%** | **−1.443** | **5.68** | .750 | **Tipping** |
| Stringent limits on a precarious population | precarity *z* = 1.6, *S*ᵣₑq = .85, policy = .6 | **−23.6%** | 1.500 | 1.81 | .250 | **Backlash** |

Four results deserve separate statement.

**H15 supported — futility is the modal outcome.** A "buy less" campaign attached to an unchanged
volume business model reduces category throughput by **1.1%** while 74% of the forgone volume is
absorbed by rivals, and it cuts the demarketer's profit to **32%** of business as usual. This is not
a marginal case: across the whole parameter sweep at zero policy, **38.3%** of cells are futility and
another 19.8% collapse. The modal outcome of unilateral demarketing is that nothing happens to
throughput and something bad happens to the firm.

**Norm spillover is real, and it is what tipping looks like.** In the tipping regime leakage is
**−1.44**: aggregate throughput falls by *more than twice* the volume forgone at the demarketing
firms themselves. The reduction propagates beyond the demarketer's own customer base. Negative
leakage is the formal signature of the thing degrowth marketing hopes for, and this is, to our
knowledge, its first quantification.

**H18 supported — contraction and profitability are jointly attainable.** In the tipping regime,
throughput falls 39% *while* the demarketing firms earn 5.7× business-as-usual profit. The growth
imperative is therefore a **contingent property of particular market architectures, not a necessary
property of markets**. This is the paper's central substantive claim, and it is a formal result about
the specified model.

**Backlash is a policy failure mode, not a consumer failing.** In the backlash scenario 84.7% of
consumers are past their flip point; accumulated reactance drives compensatory displacement to .538,
and aggregate throughput **rises 23.6%** relative to business as usual. Notice what produced it: not
apathy, not insufficient information, not weak norms, but a demanding limit pressed on a precarious
population *with strong institutional sufficiency pressure*. The intervention caused the harm.

### 8.2 The tipping surface

We swept the social multiplier λ (0 to .60), business-model reconfiguration *r* (0 to 1), and policy
intensity (0, .3, .6): 243 cells, each against its own counterfactual.

**[Figure 9: `../analysis/output/figures/fig9_phase_diagram.png`]**

Regime frequencies:

| Policy intensity | Futility | Collapse | Niche | Strained | **Tipping** |
|---|---|---|---|---|---|
| 0.0 | .383 | .198 | .136 | .012 | **.272** |
| 0.3 | .086 | .173 | .062 | .173 | **.506** |
| 0.6 | **.000** | .185 | .012 | .111 | **.691** |

Institutional scaffolding does not merely improve outcomes on average. At policy intensity .6,
**futility is eliminated entirely**. The policy instruments — repair subsidy, defector cost, norm
signal — do not make consumers want sufficiency more; they make the leakage channel narrower and the
reconfigured business model solvent.

### 8.3 H16: strict complementarity

Post-growth market viability (PMV) is defined as a throughput reduction above 10% with the
demarketer's profitability preserved at or above business as usual. At zero policy:

| Social multiplier λ | Reconfiguration *r* | **PMV rate** | Mean Δ throughput | Mean leakage |
|---|---|---|---|---|
| Low | Low | **.00** | .018 | .768 |
| High | Low | **.25** | .081 | .108 |
| Low | High | **.50** | .118 | .166 |
| High | High | **1.00** | .297 | −1.079 |

**H16 supported as a strict complementarity.** Neither ingredient suffices. Cultural change without
business-model change yields viability in a quarter of cells; business-model change without cultural
change in half; both together in all of them. The interaction is superadditive, and the mechanism is
visible in the leakage column: only the both-high cell achieves negative leakage.

This has a direct implication for how the sufficiency debate is usually conducted. The recurring
argument about whether the transition is fundamentally cultural or fundamentally structural is
**malformed**. The two are complements, and either alone is a poor bet.

### 8.4 H17: policy substitutes for culture, at a measurable rate

λ\*(*r*) is the minimum social multiplier at which post-growth market viability is attained.

| Reconfiguration *r* | Policy 0.0 | Policy 0.3 | Policy 0.6 |
|---|---|---|---|
| 0.000 | — | — | — |
| 0.125 | — | — | .525 |
| 0.250 | .600 | .525 | .375 |
| 0.375 | .525 | .450 | .225 |
| 0.500 | .525 | .300 | **.000** |
| 0.625 | .375 | **.000** | .000 |
| 0.750 | .300 | .000 | .000 |
| 0.875 | .075 | .000 | .000 |
| 1.000 | .000 | .000 | .000 |

**[Figure 10: `../analysis/output/figures/fig10_lambda_star.png`]**

Three readings. **Reconfiguration is necessary**: at *r* ≤ .125 no amount of social contagion
achieves viability without policy support — the dashes are not missing data but regions where the
frontier does not exist. **Policy and reconfiguration are substitutes for cultural change**: at
*r* = .50, the required social multiplier falls from .525 to .300 to zero as policy rises. And the
substitution rate is **estimable**, which converts a rhetorical debate about policy versus culture
into a quantitative trade-off that could in principle be calibrated to a real category.

### 8.5 P20: inequality raises the threshold, then removes it

This is the result with the sharpest public-policy implication. We varied the population mean and
dispersion of economic precarity, holding the required stringency at .65 (a demanding transition,
because a transition that asks little pushes nobody past their flip point and the mechanism cannot
express itself).

**[Figure 11: `../analysis/output/figures/fig11_inequality.png`]**

| Mean precarity (*z*) | λ\* required | Share past their flip point | Mean *S\** |
|---|---|---|---|
| 0.0 | .56 | .016 | .353 |
| 0.5 | .60 | .050 | .325 |
| 1.0 | .64 | .124 | .303 |
| 1.5 | .68 | .258 | .285 |
| 2.0 | **unattainable** | .444 | .270 |
| 2.5 | **unattainable** | .640 | .257 |

**P20 supported, and more strongly than we predicted.** The contagion threshold rises monotonically
with population precarity — and beyond a threshold it does not merely rise, it **ceases to exist**.
At mean precarity of 2 *z* and above, no value of the social multiplier in the feasible range
achieves post-growth market viability; the maximum attainable throughput reduction collapses from
21% to under 2%.

Dispersion has a weaker and more specific role than we anticipated, and we report it as such. Raising
the precarity standard deviation from .6 to 1.4 at a fixed mean of zero raises the share of consumers
past their flip point from .000 to .062 (Figure 11b) — but this is **not** enough to move λ\*, which
stays at .56 across all three dispersion levels (Figure 11a). At these population means it is the
*level* of precarity, not its spread, that sets the threshold. The reason is traceable: dispersion
adds consumers to both tails, and the committed tail partly offsets the deprived one. We had expected
dispersion to bind independently; on this model it does not, at least in the range examined.

The mechanism is fully traceable through the model. Precarity lowers *S\**; a lower *S\** puts more
consumers on the deprivating side of the required limit; those consumers' attractors shift *down*,
not up; the social multiplier has less to multiply; and the demarketing firm's committed base never
reaches the size at which reconfiguration is solvent. The macro failure is the aggregation of a
micro appraisal.

> **Therefore: distributive policy is not a parallel concern to sufficiency policy. It is a
> precondition of it.** A sufficiency transition attempted in a sufficiently unequal society does
> not merely proceed more slowly. It cannot be reached by cultural or commercial means at all.

We note what this does to a familiar objection. Critics of degrowth argue that it is a politics of
the comfortable that would immiserate the insecure. On the SSM's account that objection is not a
misunderstanding to be corrected — **it is a correct description of what happens when sufficiency
policy is attempted without distributive policy**, and it is derivable from the model. The
constructive response is not to deny it but to treat material security as an instrument of
sufficiency policy rather than a competitor for its budget.

### 8.6 P22: a conjecture the model rejects

We conjectured a **credibility–viability tradeoff**. Sacrifice credibility is
sac = *d*(1 − φ*r*): reconfiguration makes demarketing survivable but should make it *less
credible*, because a firm earning service revenue is visibly no longer sacrificing. If the
credibility loss were strong enough, sweeping *r* would produce an interior optimum in throughput
reduction rather than a monotone gain.

We tested it rather than assuming it, sweeping *r* across four rates of credibility erosion:

| φ (credibility erosion) | argmax *r* | Max Δ throughput | Interior optimum? |
|---|---|---|---|
| 0.0 | 1.00 | .417 | No |
| 0.4 | 1.00 | .350 | No |
| 0.8 | 1.00 | .274 | No |
| 1.0 (complete erosion) | 1.00 | .209 | No |

**P22 is rejected.** At every erosion rate up to *complete* erosion of the sacrifice signal, both
throughput reduction and demarketer profitability increase monotonically in reconfiguration. The
revenue effect dominates the credibility effect throughout.

**[Figure 12: `../analysis/output/figures/fig12_reconfiguration.png`]**

We report this because it is a substantive finding with a clear managerial reading, and because the
alternative — quietly deleting a conjecture the model failed to support — is how formal modelling
loses its evidential value. The reading is: **firms need not fear that decoupling revenue from
volume undermines the authenticity of their sufficiency positioning.** The strategic worry that a
durability-and-repair business model looks like a commercial manoeuvre rather than a sacrifice is,
within this model, not worth acting on. What matters is that the firm actually sells fewer units;
whether consumers read that as noble or as clever does not change the outcome.

Note the boundary condition this establishes for §3.2: the sacrifice signal matters enormously for
*brand equity* (Study 3C, *d* = .49 versus null) but not for *system-level propagation*. Credibility
buys preference; reconfiguration buys survival; and it is survival that determines whether the
regime tips.

### 8.7 Sensitivity

One-factor-at-a-time perturbation of ±20% on sixteen behavioural and economic parameters, starting
from the tipping configuration. **All 32 perturbations remain in the tipping regime with PMV
attained.** Largest sensitivities on throughput reduction: demarketing intensity (+.072/−.059),
the consumer sufficiency elasticity (±.04), the attractor relaxation rate (±.02), and firm imitation
rate (−.021). The regime classification is robust; the magnitudes are not, and should be read as
ordinal.

Two honest limitations. The tipping regime's profit multiple (5.7×) is high, and it is sensitive to
the service-revenue parameter, which sits at the upper end of the searched range. And the parameters
are not estimated from a real category. The defensible claims from Study 4 are therefore
**structural** — which regimes exist, what their signatures are, which factors are complements,
what the comparative statics are — and not point predictions.

---


## 9. General discussion

### 9.1 What the theory adds

**A construct with a designable antecedent and a specified failure mode.** Chosen sufficiency is a
state, not a trait, and it is nearly orthogonal to the same behaviour performed under constraint
(HTMT = .120). That orthogonality is the theoretical payload: the field has been measuring reduction
*behaviour* and inferring sufficiency *psychology*, and the two come apart. It also means aggregate
consumption statistics are close to uninformative about the psychological state of a population
under limits — a population reducing consumption because it must and one reducing because it chooses
to will look identical in expenditure panels and behave completely differently under additional ask.

**Two routes instead of one, with a derived nonlinearity.** The dual-route architecture is what makes
the flip point derivable rather than merely observable. Single-route accounts can accommodate an
inverted-U by adding a quadratic term; they cannot explain why it is there. The SSM explains it from
the functional form of each route — saturation against acceleration — and thereby predicts *where*
the turning point sits and *how it moves*. That is the difference between describing a curve and
having a theory of it.

**A "consumption under limits" branch for Consumer Culture Theory.** CCT has an account of identity
construction through consumption and no account of identity construction through bounded
consumption. The SSM supplies one, and finds it conditional: restraint is identity-affirming when it
is self-authored, socially co-present, gain-framed, and *moderate*, in a category where consumption
carries symbolic weight, for a consumer with enough material slack to experience the bound as a
choice. Remove any of those conditions and the same behaviour becomes deprivation. This is a
narrower claim than "restraint can be meaningful" and a much more useful one.

**A formal answer to the futility objection.** The strongest objection to demarketing — that a firm
persuading its customers to buy less merely donates them to rivals — turns out to be *correct in the
modal case* and *wrong in a specifiable region*. Leakage is .74 in the futility regime and −1.44 in
the tipping regime. The theory's contribution is not to dismiss the objection but to locate the
boundary, and the boundary is a strict complementarity between reconfiguration and contagion, with
institutions setting the exchange rate between them.

**A distributive result derived rather than asserted.** P20 is the paper's most consequential claim
and it comes from composing the micro and macro layers, not from adding a normative premise.
Precarity lowers the flip point; lower flip points shrink the committed base; a smaller base leaves
the social multiplier nothing to multiply and the reconfigured business model insolvent. The
threshold rises with inequality and then disappears.

### 9.2 What the theory rules out

A theory's value is partly in what it forbids. The SSM forbids:

- **Sufficiency campaigns calibrated by enthusiasm.** For roughly the upper 58% of the precarity
  distribution, increasing stringency significantly *reduces* chosen sufficiency. Escalating the ask
  in response to weak uptake is precisely wrong.
- **"Buy less" messaging without revenue sacrifice.** Zero brand-equity return (*d* = −.10,
  *p* = .39) and increased category salience. Worse than silence.
- **Unilateral corporate leadership as a transition strategy.** 38% futility, 20% collapse at zero
  policy.
- **The culture-versus-structure debate.** They are complements; PMV rate .25 and .50 alone, 1.00
  together.
- **Sufficiency policy in advance of distributive policy.** Beyond a precarity threshold, viability
  is unattainable by any cultural or commercial means.
- **Reading symbolic categories as uniformly hostile to sufficiency.** They polarise: the
  amplification of Route A (.244) and Route B (.250) is almost exactly symmetric.

### 9.3 Managerial implications

**The four-cell demarketing decision.** Study 3C's design is directly usable as a diagnostic. A firm
considering sufficiency positioning occupies one of four cells, and only one is worth being in:
high demarketing intensity *with* a visible, costly sacrifice signal (+.30 on brand sufficiency
equity). High intensity without sacrifice returns nothing (−.11). Sacrifice signalling without
substantive intensity is the *worst* cell (−.18) — the signature of a claim the firm has not
honoured.

**Reconfiguration is not optional and it is not risky.** Study 4 gives two findings that should
change how durability-first and repair-first business models are evaluated internally. First, they
are *necessary*: at *r* ≤ .125, no amount of consumer sufficiency makes demarketing viable. Second —
and this is the rejected conjecture's payoff — the widespread strategic worry that earning service
revenue makes a firm's sufficiency positioning look opportunistic **does not matter at the system
level**. Credibility buys preference; reconfiguration buys survival. Firms have been optimising the
wrong variable.

**Segment on the flip point, not on attitude.** The actionable segmentation variable is not
environmental concern but *S\**, which is a function of precarity and category symbolic intensity.
Two consumers with identical stated concern and identical demographics can sit on opposite sides of a
given ask. A firm running a sufficiency programme should be calibrating stringency per segment, which
is a completely ordinary marketing competence applied to a novel variable.

**Design the limit, not just the message.** Half a standard deviation of chosen sufficiency
(*d* = .516) is available from architecture alone, at identical stringency. The levers are additive
and route-specific: use collectivisation where autonomy is the constraint, agency and framing where
deprivation is the constraint. Collectivisation does nothing for deprivation (*p* = .751), which
means the currently popular "community challenge" format is the wrong instrument for precarious
segments.

**Build the community infrastructure, or accept the leakage.** CS → behaviour more than doubles from
low to high community embeddedness (.234 to .503), and CS → displacement triples (−.091 to −.278).
Repair cafés, tool libraries, and user communities are not brand-affinity activities; they are the
translation mechanism, and without them a firm's sufficiency programme generates attitude,
displacement, and very little reduction.

### 9.4 Public policy implications

**Sequence distributive policy first.** This is the strongest policy claim the paper makes, and it is
derived. Material security is an *instrument* of sufficiency policy, not a competing budget line.
A sufficiency programme in a high-precarity population raises the required social multiplier and then
exhausts the feasible range entirely.

**Calibrate stringency to the flip-point distribution, not to the target.** A single national
sufficiency target is necessarily miscalibrated for part of the population, and miscalibration is not
merely inefficient — past the flip point it is counterproductive, driving compensatory displacement.
The SSM implies differentiated asks, which is politically awkward and empirically indicated.

**Fund the leakage channel closure, not just the message.** The policy instruments that worked in
Study 4 — repair subsidy, defector cost, norm signal — operate on *structure*, not persuasion. At
policy intensity .6, futility disappears (.383 → .000). Information campaigns do not appear in the
model's viable region, and the reason is visible in the leakage column.

**Anticipate backlash as an intervention effect.** The backlash regime is generated by strong
sufficiency pressure on a precarious population and produces a **23.6% increase** in throughput plus
reduced policy support. This is an evaluable, forecastable failure mode, and it is caused by the
intervention rather than by the population. Sufficiency policy should be piloted with reactance and
displacement as primary endpoints, not as afterthoughts.

**Regulate sufficiency claims on the sacrifice dimension.** Study 3C shows that consumers already
discount sufficiency messaging that is not backed by visible revenue sacrifice. That gives regulators
a workable criterion: sufficiency and "buy less" claims could be held to a demonstrated-sacrifice
standard in the way environmental claims are increasingly held to a substantiation standard.

### 9.5 Limitations

We state these plainly because the paper's credibility depends on it.

**1. Studies 1–3 use synthetic data.** They demonstrate that the model is identified, estimable,
powered, and falsifiable, and they fix the analysis pipeline in advance. They are not evidence about
the world. The central hypotheses — the flip point, its movement with precarity, the sufficiency-
washing penalty — remain open empirical questions. The contribution of these studies is a
*specification*: measures, designs, required sample sizes, and pre-committed tests.

**2. Study 4's parameters are not estimated from a category.** Its defensible outputs are structural
(which regimes exist, their signatures, which factors are complements, the comparative statics) and
not point predictions. The 5.7× profit multiple in the tipping regime should not be quoted as a
forecast. The service-revenue parameter sits at the upper end of the searched range, and the
calibration search is reported so this is auditable.

**3. Effect magnitudes are calibrated, not discovered.** The DGP's parameters were chosen to sit in
plausible ranges and, for Study 3A, explicitly tuned to realistic vignette-experiment effect sizes.
Study 1's power curves are therefore conditional on those magnitudes. If true effects are half as
large, required sample sizes roughly quadruple.

**4. The measurement model is reflective throughout.** Some constructs, particularly
business-model reconfiguration and community embeddedness, are arguably formative, and treating them
reflectively in the confirmatory study would be a misspecification.

**5. Chosen sufficiency is modelled as domain-specific with no cross-domain structure.** Real
consumers hold sufficiency bounds in some domains and not others, and the SSM currently says nothing
about how these interact — which is precisely where compensatory displacement lives. The model
represents displacement as an outcome but does not model the portfolio.

**6. The macro model has no politics.** Institutions enter as a policy intensity parameter, and
sufficiency policy's central difficulty is that it is *contested*. Firms lobby, coalitions form,
governments change. Nothing in Study 4 represents this, and a model of sufficiency policy that
assumes policy is exogenous is missing the main obstacle to it.

**7. Cross-national coverage is thin.** Four countries with one Global South case cannot support
claims about postcolonial or *Buen Vivir* framings of sufficiency, which are ontologically distinct
from European degrowth rather than a variant of it. The invariance result should be read as a
hypothesis about mechanism universality, not a demonstration of it.

### 9.6 Future research

**The confirmatory programme.** Studies 1–3 specify it: *N* ≈ 1,600 stratified cross-nationally for
the structural model; *N* ≈ 1,200 for the architecture factorial; *N* ≈ 2,100 with seven dose levels
for the flip point; *N* ≈ 640 for the credibility factorial. Study 1's power curves give the required
*N* for each hypothesis, and identify the one hypothesis that must not be attempted in a survey.

**Ground the model in sufficiency communities.** Repair cafés, tool libraries, and voluntary
simplicity networks are the natural site for estimating the community-embeddedness moderator and the
translation and leakage-suppression paths, which are the parameters Study 4 shows the macro dynamics
are most sensitive to. Comparative fieldwork across Germany, France, Nordic contexts, and Latin
American *Buen Vivir* settings would also test whether the invariance result survives contact with
genuinely different sufficiency ontologies.

**Calibrate Study 4 to a real category.** Apparel and household energy are the natural pair: high
versus low symbolic intensity, both with sufficiency-relevant policy activity, both with
observable durability and repair economics. Estimating λ, *r*, and the leakage rate from panel data
would convert the phase diagram from an existence proof into a forecast.

**Measure the flip point behaviourally and incentive-compatibly.** *S\** is currently estimated from
a dose–response in stated commitment. An incentive-compatible elicitation — a becker-DeGroot-style
mechanism over consumption bounds, or a multiple-price-list over reduction commitments — would make
it a revealed rather than stated quantity, and would let it be estimated per individual rather than
per tercile.

**Model the politics.** Endogenising policy — firms lobbying against defector costs, coalitions
forming around repair subsidies, the backlash regime feeding back into policy support through the
sufficiency-policy-support outcome the micro model already contains — is the obvious and important
extension. The micro model already produces the input (policy support attenuated by growth-paradigm
endorsement); the macro model currently discards it.

**Test the ambivalence prediction directly.** P6 claims that high-autonomy/high-deprivation
"ambivalent sufficiency" is a real and probably common state. It has clear behavioural signatures
(commitment plus displacement) and is a candidate explanation for the sign-inconsistency in the
consumption-reduction intervention literature. It has not been measured.

### 9.7 Conclusion

Marketing is routinely named as a cause of overconsumption and rarely invited to contribute to its
remedy. The invitation is declined in part because the discipline's constructs are
volume-expansionary and it has had nothing to say about scale.

The Sufficiency–Sovereignty Model is an argument that this is a contingent limitation rather than a
constitutive one. Whether a consumption limit expands or contracts consumer sovereignty depends on
how the limit is *designed* — its agency, locus, frame, and dose — and limit design is a marketing
competence. Whether a market can contract without collapsing depends on business-model architecture,
norm propagation, and institutional scaffolding — and positioning, segmentation, and brand-meaning
management are marketing competences. The theory's final proposition is that marketing capability is
regime-determining: the same competence set that manufactures volume growth determines whether a
sufficiency transition tips, stalls, or backfires.

Two findings should be uncomfortable for everyone in the debate. Against the optimists: unilateral
corporate sufficiency leadership is futile in 38% of the parameter space and destroys the firm in
20%, and "buy less" messaging without visible sacrifice earns a brand precisely nothing. Against the
pessimists: throughput reduction of 39% is attainable *with* firm profitability at 5.7× business as
usual, so the growth imperative is a property of particular market architectures rather than of
markets.

And one finding should be uncomfortable for the field's political self-understanding. The critique
that sufficiency is a politics of the comfortable which would immiserate the insecure is not a
misreading to be argued away. Within this model it is a correct description of what sufficiency
policy does when it is attempted without distributive policy, and it is derivable rather than
rhetorical. Distributive justice is not a parallel concern to sufficiency. It is the precondition.

---

## References

> **Verification note.** Bibliographic details below are drawn from working knowledge of these
> literatures. Author lists, years, volumes, and pages must be verified against the publisher of
> record before submission. Items marked **[†]** are 2024–2025 publications whose DOIs were verified
> during preparation; items marked **[‡]** are ones for which the author attribution was inferred
> from associated sources and requires confirmation.

Ahlberg, O., Coffin, J., & Hietanen, J. (2022). Bleak signs of our times: Descent into "Terminal
Marketing." *Marketing Theory*, 22(4). https://doi.org/10.1177/14705931221095604 **[†]**

Alcott, B. (2008). The sufficiency strategy: Would rich-world frugality lower environmental impact?
*Ecological Economics*, 64(4), 770–786.

Arnould, E. J., & Thompson, C. J. (2005). Consumer Culture Theory (CCT): Twenty years of research.
*Journal of Consumer Research*, 31(4), 868–882.

Bradley, N., & Blythe, J. (Eds.) (2013). *Demarketing*. Routledge.

Brehm, J. W. (1966). *A Theory of Psychological Reactance*. Academic Press.

Centola, D., Becker, J., Brackbill, D., & Baronchelli, A. (2018). Experimental evidence for tipping
points in social convention. *Science*, 360(6393), 1116–1119.

Chatzidakis, A., & Lee, M. S. W. (2013). Anti-consumption as the study of reasons against.
*Journal of Macromarketing*, 33(3), 190–203.

Cherrier, H., Black, I. R., & Lee, M. (2011). Intentional non-consumption for sustainability.
*European Journal of Marketing*, 45(11/12), 1757–1767.

Creutzig, F., Roy, J., Lamb, W. F., et al. (2018). Towards demand-side solutions for mitigating
climate change. *Nature Climate Change*, 8(4), 260–263.

Deci, E. L., & Ryan, R. M. (2000). The "what" and "why" of goal pursuits: Human needs and the
self-determination of behavior. *Psychological Inquiry*, 11(4), 227–268.

Dekhili, S., Merle, A., & Ochs, A. (2024). Commentary on "Look up! Five research proposals for
rethinking marketing in a post-growth society": Marketing must reflect on its own evolution in the
Anthropocene epoch. *Recherche et Applications en Marketing (English Edition)*. **[†]**

Dillard, J. P., & Shen, L. (2005). On the nature of reactance and its role in persuasive health
communication. *Communication Monographs*, 72(2), 144–168.

Egan-Wyer, C., & Bertilsson, J. (2025). Envisioning post-growth marketing: A dystopian-optimist's
guide. *Marketing Theory*. https://doi.org/10.1177/14705931251313777 **[†‡]**

Egan-Wyer, C., & Bertilsson, J. (2025). *Marketing in the Climate Crisis: Imagining Post-Growth
Futures*. Routledge. ISBN 9781032830728 **[†]**

Etzioni, A. (1998). Voluntary simplicity: Characterization, select psychological implications, and
societal consequences. *Journal of Economic Psychology*, 19(5), 619–643.

Fornell, C., & Larcker, D. F. (1981). Evaluating structural equation models with unobservable
variables and measurement error. *Journal of Marketing Research*, 18(1), 39–50.

Giesler, M., & Fischer, E. (2017). Market system dynamics. *Marketing Theory*, 17(1), 3–8.

Gonzalez-Arcos, C., Joubert, A. M., Scaraboto, D., Guesalaga, R., & Sandberg, J. (2021). "How do I
carry all this now?" Understanding consumer resistance to sustainability interventions.
*Journal of Marketing*, 85(3), 44–61.

Gorge, H., Herbert, M., Özçağlar-Toulouse, N., & Robert, I. (2015). What do we really need?
Questioning consumption through sufficiency. *Journal of Macromarketing*, 35(1), 11–22.

Grinstein, A., & Nisan, U. (2009). Demarketing, minorities, and national attachment.
*Journal of Marketing*, 73(2), 105–122.

Haberl, H., Wiedenhofer, D., Virág, D., et al. (2020). A systematic review of the evidence on
decoupling of GDP, resource use and GHG emissions. *Environmental Research Letters*, 15(6), 065003.

Hayes, A. F. (2015). An index and test of linear moderated mediation.
*Multivariate Behavioral Research*, 50(1), 1–22.

Henseler, J., Ringle, C. M., & Sarstedt, M. (2015). A new criterion for assessing discriminant
validity in variance-based structural equation modeling.
*Journal of the Academy of Marketing Science*, 43(1), 115–135.

Hickel, J. (2020). *Less Is More: How Degrowth Will Save the World*. William Heinemann.

Hickel, J., Kallis, G., Jackson, T., et al. (2022). Degrowth can work — here's how science can help.
*Nature*, 612(7940), 400–403.

IPCC (2022). Demand, services and social aspects of mitigation. In *Climate Change 2022: Mitigation
of Climate Change*, Working Group III Contribution to the Sixth Assessment Report, Ch. 5. Cambridge
University Press.

Jackson, T. (2017). *Prosperity Without Growth: Foundations for the Economy of Tomorrow* (2nd ed.).
Routledge.

Kallis, G. (2011). In defence of degrowth. *Ecological Economics*, 70(5), 873–880.

Kallis, G., Kostakis, V., Lange, S., Muraca, B., Paulson, S., & Schmelzer, M. (2018). Research on
degrowth. *Annual Review of Environment and Resources*, 43, 291–316.

Kotler, P. (2011). Reinventing marketing to manage the environmental imperative.
*Journal of Marketing*, 75(4), 132–135.

Kotler, P., & Levy, S. J. (1971). Demarketing, yes, demarketing. *Harvard Business Review*, 49(6),
74–80.

Lastovicka, J. L., Bettencourt, L. A., Hughner, R. S., & Kuntze, R. J. (1999). Lifestyle of the
tight and frugal: Theory and measurement. *Journal of Consumer Research*, 26(1), 85–98.

Layton, R. A. (2007). Marketing systems — a core macromarketing concept.
*Journal of Macromarketing*, 27(3), 227–242.

Layton, R. A. (2019). Marketing systems, macromarketing and the quality of life. In *Handbook of
Marketing and Society*. Routledge.

Lee, M. S. W., Fernandez, K. V., & Hyman, M. R. (2009). Anti-consumption: An overview and research
agenda. *Journal of Business Research*, 62(2), 145–147.

Lloveras, J. (2025). Breaking "the growth spell": Sustainable marketing after growth realism.
*Marketing Theory*. https://doi.org/10.1177/14705931251335588 **[†]**

Lloveras, J., Marshall, A. P., Vandeventer, J. S., & Pansera, M. (2022). Sustainability marketing
beyond sustainable development: Towards a degrowth agenda. *Journal of Marketing Management*,
38(17–18). https://doi.org/10.1080/0267257X.2022.2084443 **[†]**

Meadows, D. H., Meadows, D. L., Randers, J., & Behrens, W. W. (1972). *The Limits to Growth*.
Universe Books.

Mullainathan, S., & Shafir, E. (2013). *Scarcity: Why Having Too Little Means So Much*. Times Books.

Nyborg, K., Anderies, J. M., Dannenberg, A., et al. (2016). Social norms as solutions.
*Science*, 354(6308), 42–43.

Ostrom, E. (1990). *Governing the Commons: The Evolution of Institutions for Collective Action*.
Cambridge University Press.

Otto, I. M., Donges, J. F., Cremades, R., et al. (2020). Social tipping dynamics for stabilizing
Earth's climate by 2050. *Proceedings of the National Academy of Sciences*, 117(5), 2354–2365.

Parrique, T., Barth, J., Briens, F., et al. (2019). *Decoupling Debunked: Evidence and Arguments
Against Green Growth*. European Environmental Bureau.

Peattie, K., & Peattie, S. (2009). Social marketing: A pathway to consumption reduction?
*Journal of Business Research*, 62(2), 260–268.

Princen, T. (2005). *The Logic of Sufficiency*. MIT Press.

Prothero, A., Dobscha, S., Freund, J., Kilbourne, W. E., Luchs, M. G., Ozanne, L. K., & Thøgersen,
J. (2011). Sustainable consumption: Opportunities for consumer research and public policy.
*Journal of Public Policy & Marketing*, 30(1), 31–38.

Rand, W., & Rust, R. T. (2011). Agent-based modeling in marketing: Guidelines for rigor.
*International Journal of Research in Marketing*, 28(3), 181–193.

Raworth, K. (2017). *Doughnut Economics: Seven Ways to Think Like a 21st-Century Economist*.
Random House.

Rémy, E., et al. (2024). Look up! Five research proposals for rethinking marketing in a post-growth
society. *Recherche et Applications en Marketing (English Edition)*. **[†‡]**

Richins, M. L., & Dawson, S. (1992). A consumer values orientation for materialism and its
measurement. *Journal of Consumer Research*, 19(3), 303–316.

Sandberg, M. (2021). Sufficiency transitions: A review of consumption changes for environmental
sustainability. *Journal of Cleaner Production*, 293, 126097.

Schaefer, A., & Crane, A. (2005). Addressing sustainability and consumption.
*Journal of Macromarketing*, 25(1), 76–92.

Schmelzer, M., Vetter, A., & Vansintjan, A. (2022). *The Future Is Degrowth: A Guide to a World
Beyond Capitalism*. Verso.

Seegebarth, B., Peyer, M., Balderjahn, I., & Wiedmann, K.-P. (2016). The sustainability roots of
anticonsumption lifestyles. *Journal of Consumer Affairs*, 50(1), 68–99.

Shah, A. K., Mullainathan, S., & Shafir, E. (2012). Some consequences of having too little.
*Science*, 338(6107), 682–685.

Sheth, J. N., Sethia, N. K., & Srinivas, S. (2011). Mindful consumption: A customer-centric approach
to sustainability. *Journal of the Academy of Marketing Science*, 39(1), 21–39.

Simonsohn, U. (2018). Two lines: A valid alternative to the invalid testing of U-shaped
relationships with quadratic regressions.
*Advances in Methods and Practices in Psychological Science*, 1(4), 538–555.

Sorrell, S. (2009). Jevons' Paradox revisited: The evidence for backfire from improved energy
efficiency. *Energy Policy*, 37(4), 1456–1469.

Steenkamp, J.-B. E. M., & Baumgartner, H. (1998). Assessing measurement invariance in cross-national
consumer research. *Journal of Consumer Research*, 25(1), 78–107.

Steffen, W., Richardson, K., Rockström, J., et al. (2015). Planetary boundaries: Guiding human
development on a changing planet. *Science*, 347(6223), 1259855.

Vadén, T., Lähde, V., Majava, A., et al. (2020). Decoupling for ecological sustainability: A
categorisation and review of research literature. *Environmental Science & Policy*, 112, 236–244.

Varey, R. J. (2013). The marketing future beyond the limits of growth.
*Journal of Macromarketing*, 33(4), 354–368.

White, K., Habib, R., & Hardisty, D. J. (2019). How to SHIFT consumer behaviors to be more
sustainable: A literature review and guiding framework. *Journal of Marketing*, 83(3), 22–49.

Wiedmann, T., Lenzen, M., Keyßer, L. T., & Steinberger, J. K. (2020). Scientists' warning on
affluence. *Nature Communications*, 11, 3107.

---

## Appendices and reproduction

| Artefact | Location |
|---|---|
| Formal construct and proposition specification | `../model/constructs.md` |
| Web appendix: full item wording, robustness, ABM equations | `WEB_APPENDIX.md` |
| Target-journal fit and reviewer-risk memo | `POSITIONING_MEMO.md` |
| All results tables (43 files) | `../analysis/output/tables/` |
| All figures (12 files) | `../analysis/output/figures/` |
| Headline numbers | `../analysis/output/summary.json` |
| Full run log | `../analysis/output/run_full.log` |

**Reproduction.** `cd analysis/src && python run_all.py` (approx. 13 minutes; deterministic given
`config.SEED = 20260801`). `python run_all.py --quick` runs a reduced-replication version in
approx. 2 minutes. `python calibrate_abm.py` reproduces the Study 4 parameter search;
`python calibrate_micro.py` reproduces the micro effect-size calibration.
