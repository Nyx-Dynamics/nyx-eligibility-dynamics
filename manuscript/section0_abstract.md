# Paper A — Abstract (draft rev. 1)

---

## Title

**Temporary Loss of Eligibility and Bias in Cross-Sectional HIV Incidence Estimation**

## Abstract

Cross-sectional HIV incidence estimation from recency assays underpins counterfactual-placebo designs in prevention trials, where randomised placebo control is no longer ethically available. These estimators are defined on a population eligible at the time of survey, yet eligibility can change between infection and sampling — through incarceration, displacement, hospitalisation, migration or death. Existing frameworks treat survey-time eligibility as a primitive and bound the problem by assuming that few individuals move, which is not the case in the populations for which counterfactual designs are most often required.

We retain the estimand, recency function and assumptions of the established framework and refine the eligibility indicator as the observable marginal of a finite-state process comprising an observable state, temporarily unobservable states permitting return, and an absorbing state. Allowing HIV acquisition in every living state rather than only while observable, we obtain the probability limit of the adjusted estimator as an integral of the recency function against a historical observability weight.

Temporary loss of eligibility is not inherently biasing. Under stable living-state composition, a demographically stationary observable susceptible pool, state-invariant acquisition, infection-independent movement and no absorbing loss, losses and returns cancel exactly — for any admissible recency function and at any occupancy of unobservable states. Cancellation holds within stationary strata and therefore under arbitrary heterogeneity in movement propensity, so concentration of movement in a high-propensity minority does not generate bias. Bias requires a specific symmetry failure: absorbing loss, state-dependent acquisition, infection-dependent movement, or non-stationarity. At sourced mortality of 0.040 per year the attenuation is 2.1%. State-dependent acquisition can attenuate or inflate, is the governing parameter, and is not identifiable from routine surveillance; we report it as a sensitivity axis rather than a corrected estimate. Analytic results were verified against an independently written generative simulator sharing no code with the derivation.

Occupancy of temporarily unobservable states cannot by itself establish that a cross-sectional incidence estimate is biased, or in which direction. Absorbing and temporary loss are not interchangeable, and correction is warranted only where a named condition fails.

**Keywords:** cross-sectional HIV incidence; recent infection testing algorithm; eligibility; selection bias; identifiability; counterfactual placebo; people who inject drugs

---

## Structured variant

For venues requiring structured abstracts. Same content, same claims.

**Background.** Cross-sectional incidence estimation from recency assays anchors counterfactual-placebo designs in HIV prevention trials. Such estimators condition on eligibility at survey, yet eligibility often changes between infection and sampling. Whether this biases estimation, and in which direction, has not been established.

**Methods.** We refined the eligibility indicator as the observable marginal of a finite-state process with temporarily unobservable states and absorbing loss, derived the expected recent-infection count allowing acquisition in every living state, and obtained the estimator's probability limit through a historical observability weight. The process was composed with an existing model of survey attendance and prior-testing exclusion. Results were checked by matrix exponentials, adaptive quadrature and an independent generative simulator.

**Results.** Temporary eligibility loss did not itself induce bias: under five stated conditions, losses and returns cancelled exactly, for any admissible recency function and at occupancies to 15%, and within stationary frailty strata. Absorbing mortality of 0.040/year attenuated estimates by 2.1%; moving the composed zero-bias boundary above unity required 0.085/year. State-dependent acquisition changed both magnitude and direction (0.944 at η = 0; 1.007 at η = 1.8).

**Conclusions.** Temporary, bidirectional loss of eligibility is not inherently biasing. State-specific acquisition, not occupancy, determines whether and in which direction an estimate is biased.

---

## Drafting notes (not for submission)

**Length.** Unstructured version is 332 words; structured is 202 (measured, not estimated). Common limits: *Statistics in Medicine* 250 unstructured, *American Journal of Epidemiology* 250 unstructured, *Epidemiology* 250 structured, preprints.org none. **The unstructured version is over for every journal target and must be cut to ~250 before submission** — it is currently written for the preprint, where length is free. The paragraph on heterogeneity and the simulator sentence are the first two cuts; the five conditions can compress to "five stated conditions" as the structured version already does.

**Claims audit.** Every quantity appears in §3–§4 and is regenerated by `make figures`. No named trial is called biased; no point estimate of η is given; no corroboration is claimed for the recency basis.

**Not decided.** Whether to signal the superseded predecessor in the abstract. §5.8 carries it in full and the reference list cites it. Most venues would not expect it here; a preprint posting may warrant one clause, since the predecessor is publicly archived under an overlapping title.

**Title.** Set to the CROI-compliant form, which also satisfies the general rule against stating conclusions in a title. If the target venue has no such rule, *Temporary Loss of Eligibility Cancels Exactly in Cross-Sectional HIV Incidence Estimation* is the stronger and more citable form.
