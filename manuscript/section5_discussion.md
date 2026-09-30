# Paper A — Section 5: Discussion — Version 2

---

## 5. Discussion

### 5.1 Principal results

Temporary loss of eligibility does not, by itself, bias cross-sectional HIV incidence estimation. Under stable living-state composition, a demographically stationary observable susceptible pool, state-invariant acquisition, infection-independent movement and no absorbing loss, the infections withheld from the recent count — acquired while observable, unobservable at survey — are offset exactly by the infections returned to it, acquired while unobservable and observable again by survey. The offset is an identity, not an approximation, and it holds independently of the recency function, of the occupancy of unobservable states, and of arbitrary heterogeneity in movement propensity.

This reverses the natural intuition, which is that people disappearing from an observable population must distort an estimator defined on it. What matters is not that they leave but whether the flow is symmetric. Bias requires a specific, nameable violation: absorbing loss, state-dependent acquisition, infection-dependent movement, or non-stationarity.

The practical consequence is a change in the question to ask of a study population. "How much of the population is temporarily unobservable?" is close to uninformative; the cancellation holds at 15% occupancy as exactly as at 1%. The informative questions are whether acquisition differs between observable and unobservable states, whether the pool is demographically stationary, and how much irreversible loss occurs over the recency window.

### 5.2 Relation to existing estimation frameworks

The result refines rather than displaces the framework of Gao and Bannick, and the extension is in the formal treatment of eligibility rather than in assay calibration: the principal result holds for any admissible recency function, so no particular mean duration of recent infection is load-bearing. Their eligibility indicator is retained and given internal structure: $A(t)=\mathbb{1}\{Z(t)=E\}$ for a process on a finite state space. Their Assumption C — that restricted incidence and prevalence equal their unrestricted values over the window — is the point of contact. They state that it holds approximately when only a small proportion of subjects move in and out of the eligible population over a span of $c$, and hold it fixed throughout. Our results say something more specific: the small-proportion condition is sufficient but far from necessary, because at $\eta_k\equiv1$ and stationarity the proportion may be large and the estimator remains exact.

Composition with Pan and colleagues is a nesting rather than a competition, and the nesting condition is worth stating precisely. Their framework is recovered when $w_t\equiv1$, which requires *both* that the living-state process contributes nothing, $s_t\equiv1$, and that the pool is demographically stationary, $g_E\equiv1$. Eligibility stability alone is insufficient: a stationary catchment with non-zero mortality still has $s_t<1$. Of the two halves, $\rho=0$ is empirically defensible and $s_t\equiv1$ is the half that fails, which is why the composed boundary differs from theirs at realistic mortality. The two frameworks also differ in what they can be asked. Theirs begins with individuals present in the source population at $t$ and characterises whether those individuals attend and whether prior testing excludes them; individuals absent from that population for part of the recency window do not enter its sample space at all. That is a property of where the framework starts, not an oversight, and it is why the population process has to be modelled upstream rather than absorbed into the selection stage. Our contribution is to supply that stage and to identify when it contributes nothing, which is the case in which their expression is not merely nested but complete.

Covariate transport by reweighting addresses a different failure and the two are complementary rather than alternative. Reweighting corrects the composition of the sampled population with respect to measured covariates. It cannot correct a within-stratum duration effect, which is below unity in every stratum, so no weighted average of such factors escapes it. In the counterfactual-placebo setting the target population *is* the trial population, drawn from the same screened pool, so the covariate distributions coincide and reweighting removes exactly none of this bias — as §S3 shows. That is not a deficiency of the method but a statement that the two problems are orthogonal, and the composed expression carries both mechanisms simultaneously.

Prior-test-informed estimation likewise addresses an adjacent problem. It repairs misclassification of recency using prior test results rather than selection into the sample, and its own assumption that attendance and infection time are independent of duration is flagged there as violated by stop-when-positive testing. The awareness-driven non-entry it defers to future work is not the same as removal from observability after acquisition, which is the mechanism here.

A methodological point falls out of holding these apart. It is tempting to merge custody, mortality, attendance, known-HIV avoidance and recent-testing exclusion into a single structural hazard. Resisting that, and keeping the staged notation — population availability, then attendance, then testing-based eligibility — caught two double-counting errors during this work: adding a prevalence to a rate, and age-standardising an exposure before applying an enrichment ratio that already contained the age effect. We state stage separation as an explicit modelling rule rather than a stylistic preference.

### 5.3 Prior-testing selection in trial protocols

One consequence of the composition in §2.7 is not novel to this paper, and it is worth saying so. The PURPOSE 2 statistical analysis plan states that although its eligibility criteria require no HIV testing in the three months before screening, testing in the preceding three to twelve months may still affect the counterfactual incidence estimate: people tested shortly before screening skew the screened set toward known HIV-negative status, because those recently diagnosed are excluded from screening, and the plan concludes that both a two-year and a one-year recency cutoff would *underestimate* the background rate.

That is the prior-testing selection formalised by Pan and colleagues, identified in the protocol of a live trial and signed as to direction. What the protocol does not do is quantify it jointly with the population process that precedes it, which is what §2.7 supplies. The contribution here is therefore not the observation that the exclusion criterion matters — the trialists say so themselves — but a composed expression in which the eligibility process and the screening-stage selection can be evaluated together, and a statement of when the former contributes nothing.

### 5.4 Implications for study design and reporting

Three consequences follow, and they differ from what would follow from treating all eligibility loss as biasing.

**Transient unobservability requires no correction** under the stated conditions. Establishing that those conditions hold may still require the movement process to be examined; what the theorem removes is the need to correct for it, not the need to check it.

**Absorbing loss should be modelled**, with its magnitude assessed against the rate at which the zero-bias boundary reaches unity for the study's own testing rate and exclusion cutoff. That threshold is a property of the design, not a universal constant.

**State-dependent acquisition is the parameter to elicit.** Occupancy and sojourn determine the magnitude of its effect once $\eta_k\ne1$, but they do not determine its direction or its existence. Because sojourn enters separately from occupancy, states with comparable occupancy but different sojourn distributions — a 32-day jail episode and a 2.7-year prison term — must be parameterised separately rather than pooled. Where $\eta_k$ cannot be estimated, the appropriate reporting form is a sensitivity surface with any literature-informed range overlaid rather than fitted.

### 5.5 Magnitude of bias under sourced parameters

At empirically sourced rates the surviving effect is small. Absorbing loss at PWID all-cause mortality of 0.040 y$^{-1}$ attenuates the estimator by 2.1%, and moving the composed zero-bias boundary above unity requires roughly twice that rate. Against the sampling variability of any realistic cross-sectional survey, a 2% attenuation is not the dominant source of error.

We state this plainly because it is the honest reading and because the alternative was tried. The analysis this work supersedes claimed a deflation of 8.9–27.3% from the same structural mechanism. That range does not survive: it was obtained under an implicit assumption of zero acquisition in unobservable states, and correcting that assumption cancels most of the effect. The scale of the direct effect is percent, not tens of percent.

The result that survives is structural rather than numerical. It states when a correction is needed and when it is not, and identifies which parameter governs the answer. A method that tells you a correction is unnecessary is worth having even when the correction it dispenses with would have been small, because the same reasoning identifies the conditions under which it would not be.

### 5.6 Identifiability of the relative acquisition hazard

The relative acquisition hazard in temporarily unobservable states is the load-bearing unknown, and it is not identifiable from the data ordinarily available. State-level HIV surveillance cannot supply it: identification requires acquisition compared during custody and during community person-time within the same population, which is a narrow and separate literature.

The best available evidence — a meta-analysis of 36 predominantly prospective cohorts reporting 0.08 HIV infections per 100 person-years among the continuously incarcerated against 1.14 to 2.78 in comparable community populations — establishes that a non-zero hazard substantially below community incidence is plausible, and a documented prison outbreak establishes that it is not zero. It does not identify a contemporary value, it concerns continuous incarceration rather than short jail episodes, and "continuously incarcerated" is not synonymous with people who inject drugs. Using it as a point estimate would manufacture precision that does not exist.

The site-level analysis of §S2 is therefore presented as a break-even calculation rather than a correction: it reports the value $\eta$ would have to take for the two selection mechanisms to stop cancelling in a given catchment, given that catchment's carceral occupancy. Across nine counties that value ranges from 0.04 to 0.55, and in two it is never reached. What makes this worth reporting is not the individual numbers but that the range overlaps the interval the available incidence comparison suggests — so the question is empirical rather than hypothetical, and a study designed to answer it would resolve the matter.

### 5.7 Limitations

**Assumptions we do not make** are worth naming because their absence is easy to miss. The cancellation requires stationarity, not reversibility or detailed balance, and describing it as requiring reversible movement understates it. It does not require exponential sojourns, or the Markov property at all: with state-invariant acquisition the weight reduces by the law of total probability to a statement about the stationary law of the movement process, so any stationary process inherits it — semi-Markov, history-dependent, or a mixture. It does not require $\eta_k\le1$; acquisition may be higher in an unobservable state, which inflates rather than attenuates. And it requires no differential hazard between infected and uninfected individuals — in a demographically stationary catchment none is needed, which inverts an argument made in the superseded analysis.

**Assumptions we do make, and which may fail.** The transition process is taken to be time-homogeneous and Markov; recidivism gives real history dependence, and a fully general semi-Markov treatment is out of scope. Infection is taken not to alter the movement law, which diagnosis may well do. Most consequentially, assay response is taken to be independent of the path through the state space: if time in custody alters ART exposure, viral suppression or the biomarker trajectory, then the recency function is path-dependent and the estimator departs from our expression by a route none of our failure modes covers. That mechanism is plausible and untested.

**Inherited assumptions that are violated in real data.** A constant false-recency rate beyond the recency window does not hold in the CEPHIA data, where the test-recent proportion declines to zero rather than plateauing. We record this rather than assume it away, and evaluate the cancellation across recency functions of different shape for that reason, but the adjusted estimator's own requirement remains.

**Unsourced inputs.** Permanent out-migration enters the absorbing state identically to death and is not sourced here, so the absorbing-loss figures are a lower bound. The exclusion-cutoff convention, the reliance on a national jail-to-prison ratio in the absence of published state jail rates, and the "ever injected" numerator in one of the occupancy routes are each stated in §3 and each would move the numbers modestly rather than the conclusions.

**Scope.** The empirical illustration is US catchments of people who inject drugs with custody as the dominant unobservability mechanism, chosen because that is where occupancy and sojourn are published. Displacement, prolonged hospitalisation and institutional care fit the same state space but are not parameterised here, and nothing in this work establishes that custody dominates in any specific setting.

### 5.8 Relation to previous analysis

This work derives from an analysis submitted elsewhere and declined after review, whose central empirical conclusion it withdraws. Two errors were found in post-review reanalysis. A jail-length return rate had been applied to combined jail-and-prison occupancy, conflating sojourn scales that differ by a factor of thirty. More consequentially, the expected recent-infection count had been derived under an implicit assumption that no acquisition occurs while an individual is temporarily unobservable — the special case $\eta_k=0$, which is empirically untenable. Generalising the numerator to admit acquisition in every living state is what produces the cancellation result, and what removes the empirical claim.

We describe this because the superseded analysis is publicly archived and because the reasoning is instructive: the error was not in any calculation but in an assumption that was never stated, and it was invisible until the numerator was written in a form general enough for the assumption to appear as a parameter value. That is an argument for stating the acquisition hazard explicitly in this class of model, which is what $\eta_k$ does.

### 5.9 Conclusion

Eligibility loss should not be treated as inherently biasing in cross-sectional HIV incidence estimation. Temporary, bidirectional movement cancels exactly under identifiable symmetry conditions, and correction is warranted only where a named condition fails. Absorbing and temporary loss are therefore not interchangeable, and state-specific acquisition — not the occupancy of unobservable states — is the parameter that determines whether and in which direction an estimate is biased. Occupancy alone cannot establish that an estimate is wrong.

---

## Drafting notes (not for submission)

**Deliberately absent**, per the constraints set during the reanalysis: no claim that any named trial's estimate is biased or by how much; no point estimate of $\eta$; no replacement empirical assertion of comparable ambition to the withdrawn one; no claim of boundary exactness beyond the Poisson inter-test case.

**§5.8 placement.** Some journals prefer a prior-work disclosure in Methods or a cover letter rather than in Discussion. The material is written to move intact if so. It should not be cut: the predecessor is publicly archived and cited in the reference list, and a reader who finds it independently should find it already addressed.

**Reviewer 1 of the predecessor** objected that eligibility dynamics act on numerator and denominator alike and would largely cancel. That objection was correct, and §5.1 concedes it by proving it. Consider whether to say so explicitly — it is a strong move in a cover letter and a weak one in a Discussion.

**Length.** ~2,100 words. If the target journal wants 1,200, §5.2 compresses to a paragraph per framework and §5.6 to a single paragraph, with the detail moving to the supplement; §5.1, §5.4, §5.5 and §5.8 should survive intact.
