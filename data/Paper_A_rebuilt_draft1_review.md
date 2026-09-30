# Draft 1 Review --- Rebuilt Paper A

## Overall assessment

**The rebuild is materially stronger, but I would not submit this draft
yet.**

The paper now contains a genuinely interesting methods result at its
center:

\[ `\Omega`{=tex}\^\*(`\gamma`{=tex})=`\int`{=tex}\_0\^T P_R(t)S_c(t),dt
\< `\Omega`{=tex} \]

whenever there is nonzero loss from the screening-observable state. That
result is clean, general, and does **not** depend on the later
ecological parameterization.

The rebuild has also done something important conceptually: it no longer
rests entirely on **late diagnosis → γ**. The supplement now contains a
multivariate structural-hazard parameterization based on
criminalization, housing, SSP access, viral suppression, and IDU
prevalence, and explicitly distinguishes it from the original
single-variable late-diagnosis model.

That is a substantial improvement.

But the paper currently has a **model-generation problem**: the rebuilt
analyses have become stronger than the manuscript's original inferential
architecture, while the manuscript still sometimes speaks as though its
numerical γ values are empirically estimated hazards. They are not. They
are **structurally informed scenario parameterizations**.

That distinction needs to become absolutely explicit.

------------------------------------------------------------------------

## 1. The mathematical core is now the strongest part of Paper A

The strongest claim is no longer:

> structurally marginalized cities have *this particular* γ.

It is:

> **If members of a recently infected population have a nonzero hazard
> of becoming unavailable to the cross-sectional sampling frame during
> the assay's recency interval, the effective MDRI in that population is
> not necessarily the calibration MDRI.**

That is the paper.

Everything after that should answer:

**How large could the resulting mismatch plausibly be under
deployment-relevant hazard structures?**

That formulation makes the paper much harder to attack.

The current derivation establishes that (S_c(t)`\le1`{=tex}) implies
(`\Omega`{=tex}\^\*\<`\Omega`{=tex}) under structural censoring. Then
the exponential approximation gives the interpretable closed form

\[
`\frac{\Omega}{\Omega^*}`{=tex}`\approx1`{=tex}+`\gamma`{=tex}`\tau`{=tex}.
\]

The supplement appropriately documents the approximation and its
finite-(T) qualification.

**I would elevate this hierarchy explicitly:**

1.  **Theorem/identity:** observability-weighted MDRI.
2.  **Approximation:** constant γ + exponential (P_R(t)).
3.  **Scenario calibration:** plausible γ values.
4.  **Empirical illustration:** AIDSVu geographies.
5.  **Sensitivity/robustness:** alternative parameterizations.

Right now those epistemic levels blur together.

------------------------------------------------------------------------

## 2. The largest remaining vulnerability is γ

This is the issue I would expect a sophisticated statistical reviewer to
attack first.

The original main analysis says:

\[ `\gamma`{=tex}*{`\rm city`{=tex}} = `\gamma`{=tex}*{`\rm base`{=tex}}
`\left`{=tex}( `\frac{\text{late-dx}_{city}}`{=tex}
{`\text{late-dx}`{=tex}\_{national}} `\right`{=tex})\^`\alpha`{=tex} \]

and describes this as a structural-function relationship rather than a
measurement-error proxy.

That is conceptually more sophisticated than saying late diagnosis
*measures* γ, but it does **not empirically identify
(f\_`\gamma`{=tex})**.

Likewise, the rebuilt multivariate formulation defines

\[
`\gamma`{=tex}*{`\rm site`{=tex}}=`\gamma`{=tex}*{`\rm base`{=tex}}M(X),
\]

where (M(X)) is an additive weighted severity index.

Again: useful model, but not an empirically estimated competing-risk
hazard.

### Therefore I would change the vocabulary globally

Avoid:

> "AIDSVu-derived structural hazard"

Prefer:

> **"AIDSVu-informed structural-hazard scenario"**

or

> **"structural-hazard parameterization informed by AIDSVu
> indicators."**

That one change would remove a surprisingly large amount of reviewer
ammunition.

------------------------------------------------------------------------

## 3. The multivariate rebuild actually exposes an important result

The single-variable and multivariate models are **not numerically
interchangeable**.

The supplement acknowledges this directly: the models use different γ
bases and different treatment of selection amplification, are correlated
at (r=0.89), and produce directionally concordant but quantitatively
different correction factors.

Under the original single-variable parameterization, Hartford is
approximately:

\[ `\Omega`{=tex}/`\Omega`{=tex}\^\*=1.273 \]

or **27.3% denominator inflation**.

Under the multivariate parameterization, Hartford becomes:

\[ `\gamma=21.81`{=tex}`\times10`{=tex}\^{-4}/d,`\qquad`{=tex}
`\Omega`{=tex}/`\Omega`{=tex}\^\*=1.377 \]

or **37.7% deflation/correction**. New Haven becomes 32.3%; San Juan
31.2%.

That's not a nuisance.

**That's a finding.**

It says:

> The existence and direction of the survival correction are
> mathematically determined, but its magnitude is
> parameterization-dependent.

That is exactly the epistemic distinction the manuscript needs.

I'd make that a major sensitivity result rather than hiding it in S4.

------------------------------------------------------------------------

## 4. I would demote the IRR-bias claim

This is probably my strongest substantive recommendation.

The (`\Omega`{=tex}\^\*) correction is much stronger than the **joint
IRR bias** result.

The supplement itself demonstrates why.

Under alternative assumptions, (B\_{`\rm IRR`{=tex}}) can cross 1. In
particular, fixed high retention and some γ parameterizations reverse
the sign.

Even more importantly, the screening-side basis matters. The supplement
says explicitly that using the exponential-basis-consistent form for
(`\rho`{=tex}\_{`\rm screen`{=tex}}) **inverts the sign across the
AIDSVu range**.

That is not a small technical qualification.

It means there are really two inferential tiers:

### Robust result

\[ `\Omega`{=tex}\^\*(`\gamma`{=tex})\<`\Omega`{=tex} \]

under nonzero structural censoring.

### Model-contingent result

\[ B\_{`\rm IRR`{=tex}}\<1 \]

under particular combinations of screening-basis approximation, γ, and
retention structure.

The manuscript currently gives those results too similar an epistemic
status.

I would rebuild the central claim around **background-incidence
calibration bias**, not around the claim that the drug systematically
appears more efficacious.

The latter can remain as an important conditional consequence:

> Depending on the relative observation processes in the counterfactual
> and intervention cohorts, this calibration mismatch can propagate into
> the efficacy contrast; its magnitude and direction depend on retention
> and the screening-observation model.

That is mathematically defensible and actually more interesting.

------------------------------------------------------------------------

## 5. The longitudinal AIDSVu work is useful---but don't call it validation of γ

The 2014--2023 panel is valuable because it demonstrates that aggregate
surveillance can conceal strong geographic redistribution.

The COVID counterfactual makes this especially clear. Stratum B has a
modeled cumulative 2020--2022 deficit of **+185 \[74, 294\]** diagnoses
and Stratum C **+361 \[18, 528\]**, while Stratum A's interval crosses
zero.

Visually, the three-stratum figure also communicates the discontinuity
effectively: the COVID-era disturbance is not simply a uniform national
perturbation.

But those analyses do **not validate the mapping
(X`\rightarrow`{=tex}`\gamma`{=tex})**.

They validate a weaker---and defensible---premise:

> surveillance environments are longitudinally and geographically
> heterogeneous enough that transport of a single calibration quantity
> across them deserves explicit scrutiny.

That's plenty.

I would change section titles such as:

> **Longitudinal empirical validation of the structural-functions
> reframing**

to something closer to:

> **Longitudinal empirical support for structural heterogeneity in the
> deployment environment**

That is considerably harder to attack.

------------------------------------------------------------------------

## 6. The invariance analysis needs careful interpretation

The manuscript reports essentially unchanged optimal cascade-policy
rankings after Kassanjee correction---Spearman (ρ=0.9979), with
identical optimal policies across all 34 cities.

That could superficially sound like:

> "So the correction doesn't matter."

I would explicitly say the opposite:

**rank invariance is not magnitude invariance.**

A multiplicative or approximately monotonic correction can materially
alter incidence levels while preserving ordering.

That becomes a useful methodological result:

> Structural calibration bias can alter absolute counterfactual
> incidence estimates without materially changing within-model policy
> rankings.

That distinction is much sharper than simply presenting the invariance
test as another validation exercise.

------------------------------------------------------------------------

## 7. The paper is currently trying to prove too many things

This is the major structural/editorial problem.

At present Paper A contains:

-   Kassanjee/MDRI theory;
-   structural competing risks;
-   trial eligibility selection;
-   intervention-arm retention;
-   city-level γ estimation;
-   multivariate barrier modeling;
-   PURPOSE-site overlays;
-   longitudinal surveillance;
-   EHE breakpoint analysis;
-   geographic redistribution;
-   Van Handel vulnerable counties;
-   COVID counterfactuals;
-   cascade-policy invariance;
-   regulatory recommendations;
-   transportability theory.

That is almost **three papers' worth of inferential machinery**.

The rebuild has made the science richer but the narrative less
disciplined.

The paper needs one spine:

> **Calibration parameters estimated in one observation regime need not
> transport unchanged into populations governed by a different
> observation process. In RITA incidence estimation, competing loss from
> observability modifies the effective MDRI.**

Everything else should either demonstrate, parameterize, or stress-test
that statement.

------------------------------------------------------------------------

## 8. I would substantially rewrite the abstract

The present abstract still says the estimator "assumes closed-system
observability" and concludes that correction "requires explicit modeling
of population-specific hazard."

The Results then contains an enormous amount of longitudinal material,
making the paper sound observational rather than methodological.

I would make the abstract roughly:

**Background:** MDRI calibration is transported from validation
populations into deployment populations.

**Methods:** Derive an observability-weighted effective MDRI under
competing loss from the screening frame.

**Results:** Prove (`\Omega`{=tex}\^\*\<`\Omega`{=tex}) under nonzero
censoring; quantify the correction over plausible hazard regimes; show
sensitivity to alternative AIDSVu-informed hazard parameterizations;
evaluate downstream effects on counterfactual incidence/IRR.

**Conclusion:** The standard MDRI is not automatically transportable
across populations with different observation processes;
deployment-specific observability should be incorporated or
sensitivity-tested.

Then one sentence about the surveillance panel as empirical
motivation/support.

Much cleaner.

------------------------------------------------------------------------

## 9. One wording problem I would remove everywhere

The manuscript repeatedly uses phrases like:

> "structurally guaranteed"

and:

> "the true bias magnitudes ... are larger than the values reported
> here."

The first is appropriate \*\*only for
(`\Omega`{=tex}\^\*\<`\Omega`{=tex}) conditional on the censoring
model\*\*.

The second goes beyond what the model establishes.

I'd replace statements of that form with:

> "Under the specified selection model, the reported scenario estimates
> are conservative relative to stronger positive coupling between
> testing interval and structural-removal hazard."

That says exactly what the mathematics establishes without pretending
the unobserved true γ is known.

------------------------------------------------------------------------

## 10. Figure architecture

The rebuilt Phase 1c figure is scientifically useful but still too busy
for a main-text figure.

It combines:

-   34-city γ distribution,
-   trial-site overlays,
-   correction curve,
-   four abstract severity scenarios.

That belongs beautifully in the supplement.

For the **main paper**, I would make Figure 1 conceptual/mathematical:

\[ P_R(t) `\quad`{=tex}`\longrightarrow`{=tex}`\quad`{=tex} P_R(t)S_c(t)
\]

with shaded areas showing (`\Omega`{=tex}) versus (`\Omega`{=tex}\^\*).

Then Figure 2 can show correction magnitude versus γ with
empirical/scenario ranges.

Then Figure 3 can be the strongest empirical heterogeneity result.

That sequence visually reproduces the paper's inferential hierarchy:

**mechanism → magnitude → empirical context.**

------------------------------------------------------------------------

## 11. Referee-style assessment

  Domain                                Draft-1 assessment
  ------------------------------------- ----------------------------------------------
  Novelty                               **High**
  Mathematical core                     **Strong**
  Conceptual importance                 **High**
  Empirical support for heterogeneity   **Strong**
  Identification of γ                   **Still weak / scenario-based**
  Sensitivity analysis                  **Strong and unusually transparent**
  IRR directional claim                 **Overstated relative to robustness**
  Longitudinal analyses                 **Useful but overinterpreted as validation**
  Reproducibility                       **Strong**
  Narrative discipline                  **Needs substantial tightening**
  Submission readiness                  **Major revision before submission**

------------------------------------------------------------------------

## Central recommendation

**Do not try to make the ecological data prove the theorem.**

The theorem doesn't need them.

The mathematical result is stronger than the empirical identification:

\[ `\boxed{
\text{nonzero loss from observability}
\Rightarrow
\Omega^*<\Omega
}`{=tex} \]

The empirical analyses should then establish that **deployment
populations plausibly occupy meaningfully different structural-hazard
regimes and show what the correction looks like across those regimes**.

That change would turn the paper's biggest current weakness---γ is not
directly observed---into a transparent modeling feature.

The rebuilt analysis contains an especially strong formulation for the
manuscript's central spine:

> **The existence and direction of the MDRI correction follow from the
> observation process; surveillance data inform its magnitude, not its
> existence.**

That should become the organizing principle of rebuilt Paper A.
