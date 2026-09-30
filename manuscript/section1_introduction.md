# Paper A — Section 1: Introduction (draft rev. 1)

---

## 1. Introduction

Randomised placebo control is no longer ethically available for HIV pre-exposure prophylaxis efficacy trials. Where an effective agent exists, the comparator must be constructed rather than randomised, and cross-sectional incidence estimation from recency assays has become the primary means of doing so. A single survey of an at-risk population, combined with an assay that distinguishes recent from long-standing infection, yields an estimate of the background incidence a trial population would have experienced without the intervention. The estimator of Kassanjee and colleagues, placed on a formal footing by Gao and Bannick, now anchors this design.

The estimator is defined on an eligible population. Eligibility is assessed at the moment of survey: an individual contributes if they are alive, present in the catchment, and reachable for screening. Infection, however, occurred earlier — potentially up to two years earlier, the span the recency window covers. Over that interval people move. They enter and leave custody, are displaced or rehoused, are hospitalised, migrate, and die. Some who were observable when they acquired HIV are not observable when the survey is taken; others who were unobservable at acquisition have returned by then.

Existing treatments handle this by bounding it. Gao and Bannick require that restricted incidence and prevalence equal their unrestricted counterparts over the window, and note that the condition holds approximately when only a small proportion of subjects move in and out of the eligible population over the relevant span. That is a sufficient condition, and a reasonable one to assume when movement is rare. It is silent on what happens when movement is common — which is precisely the case in the populations where counterfactual-placebo designs are most needed. Among people who inject drugs in United States catchments, six to eight per cent of person-time is spent in custody alone, and the figure is higher in some cities.

The natural expectation is that this biases the estimator downward. People who disappear from an observable population cannot be counted by an estimator defined on it, and the individuals most likely to disappear are those whose circumstances also place them at highest risk. The expectation is intuitive, it motivated our own earlier work on this problem, and it is wrong in the general case.

What determines bias is not whether people leave but whether the flow is symmetric. Infections withheld from the recent count — acquired while observable, unobservable at survey — are offset by infections returned to it, acquired while unobservable and observable again by survey. Whether the two balance depends on the structure of the movement process, not on its volume. This paper identifies the conditions under which they balance exactly, and the specific ways the balance can fail.

Two features of the existing formalism make the question easy to get wrong, and both are worth stating at the outset. First, the recency function used by Gao and Bannick conditions on eligibility at survey and therefore carries no eligibility-survival component, whereas Kassanjee's original formulation embeds one. Eligibility dynamics must consequently enter *once*, explicitly, through a population process — and a treatment that both models the transitions and deflates the recency window has counted the same mechanism twice. Second, the population process operates upstream of, and composes with rather than replaces, the survey-attendance and prior-testing selection formalised by Pan and colleagues. Collapsing custody, mortality, attendance and testing-based exclusion into a single structural hazard makes double-counting nearly unavoidable; we keep the stages separate as an explicit modelling rule.

### Where this sits in the literature

The line from the Kassanjee estimator through Gao and Bannick's formalisation has been extended in three directions: prior-test information, covariate transport for population heterogeneity, and selection arising from survey attendance and prior-testing exclusion. Each of these takes eligibility at survey as a primitive — a time-indexed indicator whose value is given. We extend the same line by modelling the dynamics of that indicator.

The move is stated simply. Gao and Bannick define eligibility $A(t)$ as an indicator; we retain their estimand, their recency function and their assumptions, and refine $A(t)$ as the observable marginal of a stochastic state process $Z(t)$. That permits eligibility to evolve between infection and sampling, and yields the conditions under which such movement cancels exactly and the mechanisms by which it does not. This is an additive extension rather than an alternative framework: the existing results are recovered as the special case in which the process is inert.

We emphasise that the extension is in the formal treatment of eligibility, not in the assay calibration. The principal result holds for any admissible recency function, so no particular mean duration of recent infection is load-bearing; §3.2 records the calibration families the empirical evaluation spans and why they are not to be read as independent support for one another.

### Contributions

We refine the eligibility indicator rather than replace it, writing $A(t)=\mathbb{1}\{Z(t)=E\}$ for a process $Z$ on a finite state space comprising an observable state, temporarily unobservable living states permitting return, and an absorbing state. Within that refinement:

1. We derive the expected recent-infection count allowing HIV acquisition in **every** living state, not only while observable, and obtain the probability limit of the adjusted estimator as an integral of the recency function against a historical observability weight.

2. We show that under stable living-state composition, a demographically stationary observable susceptible pool, state-invariant acquisition, infection-independent movement and no absorbing loss, temporary losses and returns cancel **exactly**. The cancellation is independent of the recency function and of the occupancy of unobservable states, and it survives arbitrary heterogeneity in movement propensity — so concentration of carceral contact in a high-propensity minority, which is the empirical reality, does not by itself generate bias.

3. We characterise the four mechanisms that break the cancellation — absorbing loss, state-dependent acquisition, infection-dependent movement, and non-stationarity — and give the direction of bias each produces.

4. We compose the process with the screening-stage selection of Pan and colleagues, recovering their expression exactly in the appropriate limit and showing how eligibility dynamics displace the zero-bias attendance boundary.

5. We parameterise each mechanism from published sources, verify the analytic results against an independently written generative simulator sharing no code with the derivation, and report the parameter that governs the answer as a sensitivity axis rather than a point estimate.

### What this paper does not do

It does not assert that any published trial estimate is biased, or by how much. The relative acquisition hazard in unobservable states is the parameter that determines whether and in which direction bias arises, and it is not identifiable from the surveillance data ordinarily available; we therefore report the value it would have to take for cancellation to fail, rather than a correction. At empirically sourced rates the surviving effect is a few per cent, which we state plainly in §5.4 because an earlier version of this analysis claimed considerably more.

The contribution is structural. It replaces a question that cannot be answered usefully — how much of the population is temporarily unobservable — with questions that can: whether acquisition differs across states, whether the catchment is demographically stationary, and how much loss is irreversible over the recency window.

### Organisation

§2 develops the state-space refinement, the general recent-count identity, the probability limit, the cancellation theorem and its corollaries, the failure modes, and the composition with screening-stage selection. §3 parameterises each quantity from published sources and states for each whether it is sourced, derived, assumed, or unidentified. §4 reports the numerical results, including recovery of the reference framework and the independent Monte Carlo validation. §5 discusses the implications for design and reporting, the limitations, and the relation to the superseded analysis from which this work derives.

---

## Drafting notes (not for submission)

**Reusable from the predecessor:** only the opening context — counterfactual-placebo motivation, the Kassanjee/Gao framework, the PURPOSE-era trials. Everything downstream of its second paragraph argues the withdrawn thesis and is not adapted.

**One inherited error worth not repeating.** The predecessor's introduction wrote the window as $\int_0^T P_R(t)\,dt$ and then described it as assuming every individual infected within the window is observable at screening. That conflates the two formulations: Kassanjee's $P_R$ *contains* an eligibility-survival component, which is exactly what Gao and Bannick's $\varphi$ conditions away. The paragraph beginning "Two features of the existing formalism" exists to forestall that confusion, and it should not be cut for length.

**Trial citations to add.** PURPOSE 1 (NCT04994509) and PURPOSE 2 (NCT04925752) with their primary reports, if the motivating paragraph is to name them as the predecessor did. PURPOSE 4 (NCT06101342) is already cited in §3.10 and §4.7; note that it is phase 2 and is used only as a carceral-geography anchor.

**Prior-work disclosure.** §5.7 carries it. A single forward-reference in §1 is an option — "an earlier version of this analysis" in the penultimate paragraph is currently the only signal — but most journals prefer it later or in a cover letter.

**Length** ~1,050 words. If compressed, the paragraph on the two notational traps and the "what this paper does not do" section should survive; the contributions list can become prose.
