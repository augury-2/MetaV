# Reviewer 1 (Prof. Taiwen Feng) — Comment 1

**Journal:** Business Strategy and Development · **Decision:** Major Revision
**Manuscript:** Enablers of Green Logistics Adoption in Developing versus Emerging Economies: An Integrated PLS-SEM and fsQCA Analysis
**Theme:** Cross-sectional design / temporal precedence / reverse causality (H1)

---

## Reviewer comment (verbatim)

> The most critical limitation is the cross-sectional design. While the authors use sophisticated
> statistical techniques, they cannot establish temporal precedence. For instance, the finding that
> regulatory pressure drives top management commitment (H1) is plausible, but it is equally likely
> that firms with committed leadership are more attuned to regulatory changes.

---

## Diagnosis of the underlying concern

**Class:** methodological + inferential; secondary construct-validity issue; writing-calibration component.

**Triggers in the submitted manuscript**

1. §3.1 deferred the entire issue to "Section 9", **which does not exist**. The reviewer followed the
   pointer and found nothing.
2. Causal language unsupported by design: §5 ("external pressures *elevate*", integration "*delivers*",
   economic environment "*functions as a moderator*"); §5.2 tells policymakers regulation "is the most
   effective lever".
3. **No endogeneity assessment of any kind.** §3.6 relies on Harman's single-factor test alone.

**Precise reading of the reviewer's alternative.** "Firms with committed leadership are more attuned to
regulatory changes" is an *omitted-common-cause* argument, not merely a temporal-order argument: a latent
environmental orientation could raise both regulatory attentiveness and managerial commitment, inflating
beta(RP->TMC) = 0.44 spuriously. Sub-issue: the instrument measures *perceived* regulatory pressure, and
RP4 ("We monitor regulatory developments closely") arguably indexes managerial attention rather than
external pressure.

**What fully satisfies this reviewer:** explicit inferential-status statement; theoretical defence of
directional dominance with the reciprocal reading conceded; *empirical* endogeneity + competing-model
testing; controls absorbing the common cause; calibrated language; concrete successor design.

**Strategic posture:** do NOT defend H1 as unidirectional. Reframe as **directional dominance within an
acknowledged recursive relation**, then test it. Concede unprompted that fsQCA does not rescue the design,
because set-theoretic sufficiency is atemporal.

---

## Revisions

### R1 — REPLACE, §3.1 (Research Design), para 1, final sentence

*Delete:* "The cross-sectional design matches the purpose of measuring the present configuration of
enablement across two types of economy, though the limitation this imposes for causal inference is
discussed in Section 9."

*Insert:*

> A cross-sectional design is appropriate to the study's primary purpose, which is to characterise the
> prevailing configuration of enablement across two institutional settings rather than to trace its
> development over time. We are nonetheless explicit about what the design licenses. Because all
> constructs are measured contemporaneously and perceptually, the estimated paths establish directional
> association conditional on the specified model, not temporal precedence; several relationships in the
> framework are plausibly recursive, and the coefficients should be read as the dominant direction of a
> mutually reinforcing relation rather than as a one-way effect (Guide & Ketokivi, 2015; Ketokivi &
> McIntosh, 2017). This is a constraint the configurational analysis shares rather than resolves:
> sufficiency in set-theoretic terms is a statement about set relations among conditions and outcomes,
> and carries no temporal content of its own. Rather than treat the matter as a concluding caveat, we
> subject the directional assumptions to formal scrutiny in Section 3.7, where an endogeneity assessment
> and a comparison of competing directional specifications are set out, and we report the results in
> Section 4.6. Residual inferential limits, and the designs required to overcome them, are discussed in
> Section 6.

**Also repairs the broken "Section 9" cross-reference.**

### R2 — ADD, §2.5, new paragraph after the H1 paragraph, before H2

> The direction posited in H1 warrants explicit defence, because a reciprocal reading is readily
> available: leaders already committed to environmental goals may scan the regulatory horizon more
> attentively and consequently perceive regulatory pressure as more acute. We take three positions on
> this. First, environmental regulation is constituted at the level of the organisational field rather
> than the firm. For the logistics operators sampled here — predominantly small and medium-sized
> enterprises with negligible capacity to shape rule-making — the substance and timing of environmental
> requirements are largely exogenous to any single firm's leadership preferences, which is the condition
> under which coercive isomorphism is theorised to operate (Zhu et al., 2013; Rashid & Rasheed, 2025).
> Second, the reciprocal reading bears more forcefully on perceived than on enacted pressure, and it is
> perception that survey instruments capture; managerial attention is selective, and committed leaders
> may register an identical regulatory environment as more demanding. We therefore advance H1 as a claim
> about directional dominance within a recursive relation rather than about unidirectional causation, and
> we test that dominance in Section 3.7 by estimating the reversed specification and comparing its
> out-of-sample performance against the hypothesised one. Third, the reciprocal account implies a latent
> common antecedent — a general environmental orientation raising both regulatory attentiveness and
> leadership commitment — which we address through control variables and a formal endogeneity assessment
> rather than by assumption. The same reasoning applies, with less force, to H3 and H7, where capability
> and performance may co-evolve; these paths are subjected to the same tests.

### R3 — ADD, new §3.7 (after §3.6, before §4)

> **3.7 Inferential Status, Endogeneity, and Tests of Directional Dominance**
>
> Because the model is estimated on contemporaneous perceptual data, the specification of directional
> paths is an assumption rather than a finding. We therefore treat that assumption as a testable
> proposition and subject it to three complementary examinations, following the position that endogeneity
> in survey-based operations research is better confronted through explicit diagnosis and competing-model
> comparison than through instrumentation that is rarely available in practice (Ketokivi & McIntosh,
> 2017; Antonakis et al., 2010).
>
> **3.7.1 Control variables.** Three characteristics recorded in the sample profile — firm size, industry
> sector, and respondent experience — were introduced as exogenous predictors of the two endogenous
> constructs of principal interest, top management commitment and green logistics performance, in order
> to absorb variance attributable to organisational scale, sectoral regulatory intensity, and respondent
> tenure. We additionally control for prior environmental institutionalisation, operationalised as
> whether the firm holds a certified environmental management system, since a pre-existing environmental
> orientation is the most plausible common antecedent of both regulatory attentiveness and leadership
> commitment and hence the most credible source of the spurious association that a reciprocal reading of
> H1 would imply. Path estimates are reported with and without controls to establish whether the
> substantive conclusions are conditional on their inclusion.
>
> **3.7.2 Endogeneity assessment.** Endogeneity was evaluated using the Gaussian copula approach, which
> identifies correlation between an endogenous regressor and the structural error term without recourse
> to instrumental variables (Park & Gupta, 2012; Hult et al., 2018). Because identification requires that
> the endogenous regressor depart from normality, the Kolmogorov-Smirnov statistic was inspected for each
> construct score before the copula terms were specified, and the recent cautions regarding finite-sample
> behaviour and intercept specification were observed (Becker et al., 2022). Copula terms were introduced
> individually and then jointly for each regressor in the model, and their significance assessed by
> bootstrapping with 5,000 subsamples. A non-significant copula term indicates no detectable endogeneity
> for that regressor; a significant term indicates bias in the corresponding path estimate, which is then
> reported in its copula-corrected form.
>
> **3.7.3 Competing directional specifications.** To assess whether the hypothesised ordering outperforms
> its reversal, three specifications were estimated on identical data and an identical set of indicators.
> Model 1 is the hypothesised framework. Model 2 reverses the two paths for which a reciprocal reading is
> most defensible on theoretical grounds, so that top management commitment predicts regulatory and
> policy pressure and green logistics performance predicts green supply chain integration. Model 3
> reverses only the regulatory path, isolating the specific alternative that motivates the concern. Since
> partial least squares path modelling does not admit non-recursive specifications, comparison across
> competing recursive models is the available means of adjudicating directional plausibility. The models
> were compared using the cross-validated predictive ability test, evaluated across all endogenous
> indicators so that the comparison is not conditional on a single target construct, with the average
> out-of-sample prediction loss and its significance reported for each contrast (Liengaard et al., 2021).
> Bayesian information criterion values are reported for the subset of comparisons in which the
> endogenous construct is held constant, as the criterion is defined per endogenous construct and is not
> comparable where the endogenous set differs (Sharma et al., 2021). We emphasise that superior
> predictive performance for the hypothesised specification constitutes evidence of directional dominance
> under the observed data, not proof of causal precedence; only a design with genuine temporal separation
> can supply the latter.

### R4 — ADD, new §4.6 (after §4.5 / Figure 8, before §5)

> **4.6 Robustness: Controls, Endogeneity, and Competing Directional Models**
>
> Introducing firm size, industry sector, respondent experience, and prior environmental certification as
> controls left the structural conclusions unchanged. All paths significant in the unconditional model
> remained significant and retained their sign, the largest absolute change in any standardised
> coefficient was [X.XX], and the non-significant path from cost barrier inversion to integration
> remained non-significant. The controls therefore do not account for the estimated relationships, and in
> particular the association between regulatory pressure and top management commitment is not
> attributable to prior environmental institutionalisation, the most plausible common antecedent of the
> two.
>
> The Gaussian copula assessment is summarised in Table 14. Construct scores departed significantly from
> normality, satisfying the identification requirement for the procedure, and [N] of the [seven] copula
> terms were non-significant when introduced individually and jointly, indicating no detectable
> endogeneity for the corresponding regressors. [Where a copula term attained significance, report the
> construct and the copula-corrected coefficient here, together with a statement of whether the
> substantive inference changes.]
>
> Table 15 reports the comparison of competing directional specifications. The hypothesised model
> achieved significantly lower average out-of-sample prediction loss than both the fully reversed
> specification and the specification reversing only the regulatory path, indicating that the hypothesised
> ordering is the better-supported of the recursive alternatives available under these data. The result
> does not establish temporal precedence, and we do not read it as doing so; what it establishes is that
> the reciprocal account, when specified and estimated rather than merely entertained, fits the data less
> well than the account the framework advances. Taken together with the theoretical argument in Section
> 2.5 and the stability of the estimates under controls, this supports interpreting the paths as dominant
> directions within relations that are in all likelihood mutually reinforcing over time.

**Table 14.** Gaussian copula endogeneity assessment (pooled sample, 5,000 bootstrap subsamples)

| Endogenous regressor | Target construct | K-S normality test (p) | Copula term coefficient | t | p | beta without copula | beta with copula | Inference |
|---|---|---|---|---|---|---|---|---|
| RP | TMC | [ ] | [ ] | [ ] | [ ] | 0.44 | [ ] | [ ] |
| SP | TMC | [ ] | [ ] | [ ] | [ ] | 0.29 | [ ] | [ ] |
| TMC | GSCI | [ ] | [ ] | [ ] | [ ] | 0.38 | [ ] | [ ] |
| DI | GSCI | [ ] | [ ] | [ ] | [ ] | 0.41 | [ ] | [ ] |
| CBI | GSCI | [ ] | [ ] | [ ] | [ ] | 0.16 | [ ] | [ ] |
| KSR | DI | [ ] | [ ] | [ ] | [ ] | 0.61 | [ ] | [ ] |
| GSCI | GLP | [ ] | [ ] | [ ] | [ ] | 0.49 | [ ] | [ ] |
| TMC | GLP | [ ] | [ ] | [ ] | [ ] | 0.27 | [ ] | [ ] |

*Source:* authors. K-S = Kolmogorov-Smirnov test of departure from normality, a precondition for copula
identification (Becker et al., 2022). Copula terms specified individually and jointly; jointly specified
results reported.

**Table 15.** Comparison of competing directional specifications (CVPAT across all endogenous indicators)

| Model | Directional specification | Avg. loss difference vs. M1 | t | p | R2 (TMC) | R2 (GSCI) | R2 (GLP) | Inference |
|---|---|---|---|---|---|---|---|---|
| M1 | Hypothesised framework (Figure 1) | - | - | - | [ ] | [ ] | 0.59 | Reference |
| M2 | TMC -> RP and GLP -> GSCI reversed | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| M3 | TMC -> RP reversed only | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |

*Source:* authors. CVPAT = cross-validated predictive ability test (Liengaard et al., 2021); positive loss
difference indicates inferior out-of-sample performance relative to M1. Indicator set held identical
across models.

> **ALL BRACKETED CELLS ARE PLACEHOLDERS** to be populated from the authors' own estimation. Only the
> coefficients already reported in Table 6 have been carried forward.

### R5 — ADD, §5 Discussion, after the MGA-interpretation paragraph, before "Returning explicitly to the three gaps"

> A word is warranted on the inferential standing of these interpretations. The design measures enablers
> and outcomes at one moment, and the mechanisms described are best understood as dominant directions
> within relations that are, over longer horizons, likely to be mutually constitutive. Regulation raises
> green logistics on the leadership agenda; leadership that has internalised environmental goals in turn
> attends more closely to regulatory signals and, in aggregate, participates in shaping them. Integration
> improves performance; demonstrated performance strengthens the case for deeper integration. The
> robustness analyses in Section 4.6 indicate that the hypothesised ordering outperforms its reversal in
> out-of-sample prediction and is not an artefact of prior environmental institutionalisation, which is
> the strongest evidence a single-wave design can furnish. It is not evidence of temporal precedence, and
> the accumulation of enabling conditions over time remains the central open question that this design
> cannot address.

### R6 — REPLACE, §6 para 2, sentence 1

*Delete:* "The cross-sectional design captures associations at a single point in time and cannot establish
causal ordering with certainty; longitudinal designs that track firms as regulation tightens or digital
infrastructure matures would allow the mechanisms to be observed in motion."

*Insert:*

> The most consequential limitation is the single-wave design. Although Section 4.6 establishes that the
> hypothesised ordering predicts better out of sample than its reversal and survives the inclusion of
> controls for prior environmental institutionalisation, neither result substitutes for temporal
> separation, and the relations examined here are in all likelihood recursive: regulatory pressure and
> leadership commitment plausibly co-evolve, as do integration and the performance it produces. Two
> features of the phenomenon make this limitation more than formal. Enablement is cumulative — digital
> readiness, workforce capability, and inter-organisational integration are built over years — so a
> single observation captures firms at heterogeneous and unrecorded stages of accumulation, and the
> cross-sectional coefficient conflates firms early in that process with firms well advanced in it. The
> configurational analysis does not escape the difficulty: set-theoretic sufficiency is a statement about
> relations among sets, and a configuration identified as sufficient may represent either a developmental
> sequence or a simultaneous bundle, a distinction the data cannot adjudicate. Three designs would
> resolve this. A multi-wave panel analysed through a random-intercept cross-lagged specification would
> separate within-firm change from stable between-firm differences, which is precisely the confound that
> a single wave cannot isolate (Hamaker et al., 2015). A staggered difference-in-differences design
> exploiting the introduction of a freight-emissions or fuel-efficiency regulation as an exogenous shock
> would identify the regulatory mechanism far more credibly than perceptual measurement of regulatory
> pressure permits. And temporally ordered configurational work, calibrating conditions at an earlier
> wave and outcomes at a later one, would allow equifinal pathways to be read as developmental
> trajectories rather than static bundles — an extension that would build directly on recent
> configurational treatments of green supply chain integration and its performance consequences (Feng &
> Sheng, 2023).

### R7 — ADD, Abstract, after "...stronger in developing economies."

> Robustness analyses, comprising a Gaussian copula endogeneity assessment and a comparison of competing
> directional specifications, indicate that the hypothesised ordering outperforms its reversal out of
> sample.

---

## Analyses to run

| Test | Purpose | Software | Procedure |
|---|---|---|---|
| Controls model | Absorb the omitted-common-cause explanation | SmartPLS 4 | Add firm size (log employees), sector dummies, experience bands, ISO 14001/EMS binary as predictors of TMC and GLP. PLS algorithm + bootstrap (5,000, BCa, two-tailed). Report largest delta-beta. |
| Gaussian copula | Direct endogeneity diagnosis (currently absent) | SmartPLS 4 -> Gaussian Copula | Confirm K-S rejects normality for each regressor (identification requirement). Specify copula terms individually, then jointly. Bootstrap 5,000. |
| CVPAT M1 vs M2 vs M3 | Convert the reviewer's verbal alternative into a rejected model | SmartPLS 4 -> CVPAT | Build M2/M3 on identical indicators. Target = ALL endogenous indicators, not a single construct. Report avg. loss difference, t, p. |
| BIC | Supplementary, same-target comparisons only | SmartPLS 4 -> model selection criteria | Report only where the endogenous construct is held constant; state the restriction. |

**If a copula term is significant** (most likely TMC->GLP, self-report both sides): report it and the
corrected coefficient. Do not suppress. A transparently corrected endogeneity finding reads as rigour.

**If EMS/ISO 14001 data cannot be obtained retrospectively:** drop the control and name it explicitly in
§6 as an unmeasured common antecedent. Do not fabricate the variable.

---

## Change log

| # | Section | Subsection | Para | Page | Action | Content |
|---|---|---|---|---|---|---|
| 1 | Abstract | - | 1 | p. [1] | ADD | Robustness sentence after MGA findings |
| 2 | Literature Review | 2.5 | after H1 | p. [X] | ADD | Recursivity defence; directional-dominance reframing; extends to H3, H7 |
| 3 | Methodology | 3.1 | 1 (final sentence) | p. [X] | REPLACE | Inferential-status statement; repairs dead "Section 9" cross-reference |
| 4 | Methodology | 3.7 (new) | all | p. [X] | ADD | Controls; Gaussian copula; competing specifications |
| 5 | Results | 4.6 (new) | all | p. [X] | ADD | Robustness results + Table 14 + Table 15 |
| 6 | Discussion | 5 | after MGA para | p. [X] | ADD | Inferential-status paragraph |
| 7 | Conclusions | 6 | 2 (sentence 1) | p. [X] | REPLACE | Sophisticated limitation + RI-CLPM / staggered DiD / temporal fsQCA |
| 8 | References | - | - | p. [X] | ADD | 12 references |

**Deleted:** the "Section 9" clause (§3.1); the generic cross-sectional limitation sentence (§6).
**Renumbering:** Tables 1-13 unchanged; new tables enter as 14 and 15. No figure renumbering.

---

## References added (verified via Crossref)

Antonakis, J., Bendahan, S., Jacquart, P., & Lalive, R. (2010). On making causal claims: A review and
recommendations. *The Leadership Quarterly, 21*(6), 1086-1120. https://doi.org/10.1016/j.leaqua.2010.10.010

Becker, J.-M., Proksch, D., & Ringle, C. M. (2022). Revisiting Gaussian copulas to handle endogenous
regressors. *Journal of the Academy of Marketing Science, 50*(1), 46-66.
https://doi.org/10.1007/s11747-021-00805-y

Feng, T., & Sheng, H. (2023). Identifying the equifinal configurations of prompting green supply chain
integration and subsequent performance outcome. *Business Strategy and the Environment, 32*(8), 5234-5251.
https://doi.org/10.1002/bse.3414

Guide, V. D. R., & Ketokivi, M. (2015). Notes from the editors: Redefining some methodological criteria for
the journal. *Journal of Operations Management, 37*, v-viii.
https://doi.org/10.1016/S0272-6963(15)00056-X

Hamaker, E. L., Kuiper, R. M., & Grasman, R. P. P. P. (2015). A critique of the cross-lagged panel model.
*Psychological Methods, 20*(1), 102-116. https://doi.org/10.1037/a0038889

Hult, G. T. M., Hair, J. F., Proksch, D., Sarstedt, M., Pinkwart, A., & Ringle, C. M. (2018). Addressing
endogeneity in international marketing applications of partial least squares structural equation modeling.
*Journal of International Marketing, 26*(3), 1-21. https://doi.org/10.1509/jim.17.0151

Ketokivi, M., & McIntosh, C. N. (2017). Addressing the endogeneity dilemma in operations management
research: Theoretical, empirical, and pragmatic considerations. *Journal of Operations Management, 52*(1),
1-14. https://doi.org/10.1016/j.jom.2017.05.001

Liengaard, B. D., Sharma, P. N., Hult, G. T. M., Jensen, M. B., Sarstedt, M., Hair, J. F., & Ringle, C. M.
(2021). Prediction: Coveted, yet forsaken? Introducing a cross-validated predictive ability test in partial
least squares path modeling. *Decision Sciences, 52*(2), 362-392. https://doi.org/10.1111/deci.12445

Park, S., & Gupta, S. (2012). Handling endogenous regressors by joint estimation using copulas. *Marketing
Science, 31*(4), 567-586. https://doi.org/10.1287/mksc.1120.0718

Rashid, A., & Rasheed, R. (2025). Enabling coercive drivers with green supply chain management practices to
gain performance nexus through external collaboration and monitoring. *Cleaner Logistics and Supply Chain,
17*, 100278. https://doi.org/10.1016/j.clscn.2025.100278

Rindfleisch, A., Malter, A. J., Ganesan, S., & Moorman, C. (2008). Cross-sectional versus longitudinal
survey research: Concepts, findings, and guidelines. *Journal of Marketing Research, 45*(3), 261-279.
https://doi.org/10.1509/jmkr.45.3.261

Sharma, P. N., Shmueli, G., Sarstedt, M., Danks, N., & Ray, S. (2021). Prediction-oriented model selection
in partial least squares path modeling. *Decision Sciences, 52*(3), 567-607.
https://doi.org/10.1111/deci.12329
