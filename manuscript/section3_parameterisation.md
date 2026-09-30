# Paper A — Section 3: Empirical parameterisation (draft rev. 1)

> Supplies every quantity §4 evaluates. Provenance for each is in
> `docs/audit/computation_record.md`, appendices noted inline.

---

## 3. Empirical parameterisation

### 3.1 Scope, and what the parameterisation is for

§2 is a structural result: it states when transient eligibility loss cancels and which asymmetries break the cancellation. Deciding whether those asymmetries are large enough to matter in a real deployment requires values. This section supplies them, and states for each whether it is **sourced** from published data, **derived** from sourced quantities, **assumed**, or **unidentified**.

The purpose is a sensitivity analysis, not a fitted model. No parameter is estimated from the trial data the method would be applied to, and none is tuned to produce a conclusion. Where a quantity cannot be identified from available evidence — which is the case for the single most consequential one — it is carried as a free axis and reported across its plausible range rather than fixed at a point.

The illustrative setting throughout is cross-sectional incidence estimation among people who inject drugs (PWID) in United States catchments, with temporary unobservability arising predominantly from custody. That choice is driven by data availability: carceral occupancy and sojourn are published at national, state and county level, whereas displacement and prolonged hospitalisation are not. It is not a claim that custody is the only or the dominant mechanism.

### 3.2 The recency function

Two recency bases are used. For reproducing published quantities we adopt the gamma form of Pan et al., with window parameter 163 d and shadow 260 d; integrated over $T^*=2$ y this gives $\Omega_{T^*}=151$ d. The window parameter and $\Omega_{T^*}$ are distinct quantities and are easily conflated, so both are reported wherever the basis is named.

Independently, we re-estimated $\varphi$ from the CEPHIA public-use dataset (Zenodo 10.5281/zenodo.4900634) following the `XSRecency` procedure: Evaluation Panel, LAg-Sedia consolidated final result, subtypes A1/B/C/D, logit polynomial in years since estimated date of detectable infection, fitted by GEE clustered on participant with an independence working correlation. For subtype C with ODn $\le1.5$ and viral load $>75$ copies/mL, MDRI is 182.4 d (95% CI 161–213, 194 participants). Pan's published 163 d falls inside that interval, and the estimate is stable across polynomial degree and fit horizon.

**Provenance matters here, and the three values are not three independent measurements.** Pan's 163 d is stated as relevant for subtype C using the LAg-EIA assay *and viral load*, and traces to Kassanjee et al. (2016), in which the CEPHIA consortium optimised viral-load criteria and thresholds across more than 2,000 candidate algorithms. Our re-estimate uses the CEPHIA public-use data and the same assay-plus-viral-load construction. It is therefore a **replication within the CEPHIA lineage**, not an external check: it establishes that the published basis is reproducible from the source data, and Pan's 163 d falls inside our interval, but both derive from the same consortium panel.

The genuinely external anchor is Duong et al. (2015), who recalibrated the LAg-Avidity assay against more than 250 seroconversion panels assembled independently of CEPHIA and report, by binomial regression over all data points, MDRI of 130 d (95% CI 118–142) at ODn $\le1.5$ with proportion false-recent 1.6%; by subtype, 129 d for B, 122 d for AE, 109 d for A&D and 152 d for C.

Duong's values are systematically shorter, and the reason is the criterion rather than the panel. Duong classifies on the assay alone; Pan's basis and our re-estimate additionally require detectable viral load. Adding a viral-load criterion is precisely the optimisation Kassanjee et al. (2016) introduced, and it lengthens MDRI while lowering the false-recent rate by removing virally suppressed long-term infections from the recent category. The ordering 152 d without viral load against 163–182 d with it is what that construction predicts, so the two lineages are consistent rather than discrepant — but they are measuring different algorithms and should not be averaged or presented as agreement.

We therefore report the spread — roughly 130 to 180 d across subtype, cutoff and viral-load criterion — as the relevant quantity, and this is why §4.2 evaluates the cancellation across recency functions spanning $\Omega_{T^*}$ from 94 d to 251 d rather than at a single basis. The cancellation result does not depend on which value is correct.

One provenance note bears on the framework itself: the simulation studies underpinning Gao and Bannick's own treatment are built on the Duong data, their supplementary §S.1.1 being titled a data simulation to mimic that source. The recency characteristics in the methodological literature descend from a small number of calibration panels, which is an argument for reporting results across bases rather than for any single one.

Duong's proportion false-recent of 1.6% at the working cutoff is the empirical scale of the parameter that Theorem 1 sets to zero. $\beta_{T^*}=0$ is a simplification adopted for analytic clarity, not a claim about the assay, and a non-zero false-recency rate enters the adjusted estimator by the route Gao & Bannick already specify.

The same fit shows that Gao & Bannick's Assumption B.1 — a constant false-recency rate beyond $T^*$ — does not hold in these data. The raw test-recent proportion declines from 9.9% at 730–1095 d to 5.8% at 1095–1825 d to zero beyond. We record this rather than assume it away; §4 evaluates the cancellation across recency functions of materially different shape for the same reason.

### 3.3 Background testing rate

$\theta$ enters only through the screening-stage composition of §2.7. NHBS 2018 across 23 metropolitan statistical areas reports that 57% of PWID tested for HIV in the preceding 12 months. Under a Poisson inter-test process this implies $\theta=-\ln(0.43)=0.844\ \mathrm{y}^{-1}$, a mean inter-test interval of 1.18 y.

The Poisson assumption is not innocuous and is retained deliberately. Calibrating a uniform inter-test distribution to the same observation gives gaps $\mathrm{Unif}[0,2.905]$, a mean interval of 1.45 y, and a systematically more favourable zero-bias boundary. Poisson is therefore the conservative choice as well as the one Pan's main analysis uses. §4.6 reports what changes under the uniform variant.

### 3.4 Absorbing loss

$\mu_E$ is all-cause mortality in the observable susceptible pool. The ALIVE cohort of PWID in Baltimore reports 37.2 deaths per 1,000 person-years for 2015 to February 2020 and 39.6 per 1,000 in 2020; age-standardised rates rose from 23 to 45 per 1,000 person-years between 1988 and 2018. We adopt $\mu_E=0.040\ \mathrm{y}^{-1}$ as the central value with 0.037–0.045 as the sourced range, and evaluate to 0.10 to bracket a more severe fentanyl-era cohort than ALIVE observed.

Permanent out-migration from the catchment enters $X$ identically to death and is **not sourced**. Different-county mover rates from the American Community Survey are the obvious anchor and were not retrieved. Any non-zero migration adds to $\mu_E$, so the values used are a lower bound on absorbing loss, and §4.4 should be read accordingly.

### 3.5 Occupancy of unobservable states

$q$ is the stationary share of person-time spent temporarily unobservable. It was derived by three routes that do not share inputs.

**Route A — prevalence × duration.** NHBS 2018 gives past-12-month incarceration among PWID of 21.0% (not homeless) and 43.3% (homeless) across 23 cities. Combined with a BJS mean jail stay of 32 d and assumptions about episode count, this yields $q$ from 1.84% (21%, one episode) to 7.59% (43.3%, two episodes).

**Route B — point-prevalence ratio.** In steady state a cross-sectional share equals a person-time share. Degenhardt et al. (2026) report injection-drug-use prevalence among incarcerated people in North America of 13.4% (95% CI 10.3–16.8), corresponding to 246,500 (190,500–308,500) incarcerated people who have injected. Against an estimated 3.70 M US PWID in 2018 (Bradley et al. 2023), $q=6.66\%$ (5.15–8.34%). This route uses no BJS input.

**Route C — BJS rates with enrichment.** US adult imprisonment of 453 per 100,000 scaled by the national jail:prison ratio and by the injection enrichment implied by Degenhardt gives $q=6.70\%$.

Routes B and C agree to 0.04 percentage points despite sharing no data source, and the jail multiplier is independently validated: BJS jail (253 per 100,000 adults) plus prison (453) is 706, against 698 from the multiplier construction, accurate to 1%. We adopt $q\approx6\text{–}8\%$ nationally, and where the two custody types are separated, $q_J=0.03$ and $q_P=0.05$.

One construction was rejected. Jail incarceration peaks at ages 25–34 (480 per 100,000) and 35–44 (426), the bands PWID predominantly occupy, and age-standardising to a PWID structure gives a 1.40× uplift. Applying that uplift *and* the injection enrichment double-counts, because part of the enrichment ratio exists precisely because PWID occupy high-incarceration age bands. The age correction is therefore applied to denominators only (§3.10), never layered on the enrichment.

### 3.6 Return rates

$\beta_k$ is the rate of return from unobservable state $k$ to $E$, the reciprocal of mean sojourn. BJS *Jail Inmates in 2023* gives a mean 32 d in custody for July 2022–June 2023 (36 d male, 19 d female; 43 d in jails with average daily population $\ge$2,500), so $\beta_J=365.25/32=11.4\ \mathrm{y}^{-1}$. The BJS *Prisoners* series gives mean time served of approximately 2.7 y, so $\beta_P=0.37\ \mathrm{y}^{-1}$.

The two differ by a factor of 31 and cannot be collapsed. A 32-day sojourn is short relative to $T^*=2$ y and approaches its within-living-state equilibrium quickly; a 2.7-year sojourn is comparable with $T^*$ and behaves as quasi-absorbing over the recency window. Applying a jail-length return rate to combined jail-and-prison occupancy conflates them, and is an error we made in earlier work on this problem.

Entry rates are not specified independently. Given occupancy and sojourn, $\alpha_k=\beta_kq_k/q_E$ follows, which is the identification used throughout: a long sojourn at fixed occupancy implies a *small* entry rate.

### 3.7 In-custody mortality

$\mu'$ is mortality in unobservable states. BJS gives 167 per 100,000 in local jails, 330 in state prisons and 259 in federal prisons for 2019 — 0.0017 to 0.0033 y$^{-1}$, an order of magnitude below community PWID mortality. Custody is a mortality refuge during the stay.

More useful is that $\mu'$ does not matter. Sweeping it from 0.002 to 0.100 — a fiftyfold change — moves the composed zero-bias boundary by 0.007, because at 4–8% of person-time the death rate in that state has almost no leverage. $\mu'$ can be fixed anywhere reasonable without affecting any conclusion and needs no further sourcing. This is a negative result that reduces the sourcing burden rather than shifting the answer, and it confirms that death in custody is not a material removal channel: removal during custody is the transient mechanism, not mortality.

### 3.8 Demographic stability of the catchment

Condition (2) of Corollary 2 requires a demographically stationary observable susceptible pool, $g_E\equiv1$. Tempalski et al. (2013) report median PWID prevalence across US MSAs falling from 104.4 to 91.5 per 10,000 aged 15–64 between 1992 and 2007, and describe the period 2002–2007 as relatively stable. We take $\rho\approx0$ over a two-year recency window. A catchment with material growth or decline violates condition (2), and §4.1 shows that condition is not optional.

### 3.9 Relative acquisition hazard — unidentified

$\eta_k=\lambda_k/\lambda_E$ is **not sourced and cannot be identified** from available data, and it is the parameter to which the results are most sensitive. Identification would require acquisition compared during custody and during community person-time within the same population; state-level HIV surveillance cannot supply it.

The only directly relevant evidence is a meta-analysis of 36 predominantly prospective cohort studies (Gough et al. 2010) giving pooled HIV incidence of 0.08 per 100 person-years among the continuously incarcerated against 1.14 per 100 among PWID recruited from treatment and 2.78 among street-recruited PWID — crude cross-study ratios of 0.03 to 0.07. Separately, a Georgia prison investigation documented 88 known seroconversions during incarceration with genetic evidence of within-prison transmission, establishing $\eta_P>0$.

These establish that a non-zero custodial acquisition hazard substantially below community PWID incidence is empirically plausible. They do not identify a contemporary value. They are heterogeneous historical studies rather than matched PWID followed inside and outside custody; "continuously incarcerated" is not synonymous with PWID; and the literature speaks to prison rather than to short jail episodes. We therefore use them as an **overlay band, never as a fitted value**, and do not collapse $\eta_J$ and $\eta_P$ to a common $\eta$ except where a common value is reported explicitly as such.

### 3.10 Site-level geography

For the site-level sensitivity of §4.7 we use the nine United States counties hosting PURPOSE 4, a phase 2 pharmacokinetics and safety trial of lenacapavir among PWID, chosen because it is the cleanest available anchor for carceral geography in an HIV prevention trial. **No efficacy estimate from that trial is corrected or commented on.**

Jail and prison counts are taken at county level for 2019, the last year with harmonized county-level estimates across all nine counties. **2019 is a fixed pre-pandemic structural anchor and is not assumed to be conservative** — the data disprove that reading. Post-2019 jail trajectories are heterogeneous in both magnitude and direction: relative to 2019, jail populations stand at 0.46 in the Bronx and 0.70 in San Diego, but 1.02 in Miami-Dade, 1.05 in Monongalia and 1.09 in Essex. Four of nine counties are at or above their 2019 level, so a single national multiplier would have been wrong in direction for them. A secondary analysis updates the jail component with the most recent local data while retaining the 2019 prison component, county-level post-2019 prison counts being unavailable.

Incarceration rates are published against total or 15–64 populations while trial eligibility is 18+, so a denominator conversion is required. A national 15–64 to 18+ ratio of 0.8333 was replaced with county-specific ratios from Census Population Estimates 2019, which range from 0.834 (Miami-Dade) to 0.908 (Harris). The national factor systematically understated exposure in counties with younger adult age structures, by up to 12.4%. Consistent with §3.5, the correction is applied to the denominator only.

### 3.11 Summary, and what this parameterisation licenses

| symbol | meaning | status | value used |
|---|---|---|---|
| $\Omega_{T^*}$ | mean duration of recent infection | sourced | 151 d (gamma 163/260); CEPHIA re-estimate 182.4 d (161–213) |
| $\theta$ | background HIV testing rate | sourced | 0.844 y$^{-1}$ (Poisson) |
| $c$ | testing-based exclusion cutoff | design | 0.25 y |
| $\mu_E$ | absorbing loss from $E$ | sourced (mortality only) | 0.040 y$^{-1}$; range 0.037–0.045; evaluated to 0.10 |
| migration | permanent exit | **not sourced** | omitted; $\mu_E$ is therefore a lower bound |
| $q$ | unobservable occupancy | derived, three routes | 6–8%; $q_J=0.03$, $q_P=0.05$ |
| $\beta_J$ | return from jail | sourced | 11.4 y$^{-1}$ (32 d) |
| $\beta_P$ | return from prison | sourced | 0.37 y$^{-1}$ (2.7 y) |
| $\mu'$ | in-custody mortality | sourced, non-influential | 0.002 y$^{-1}$ |
| $\rho$ | catchment growth | sourced | $\approx0$ |
| $\eta_k$ | relative acquisition hazard | **unidentified** | free axis, 0 to 1.8; literature overlay 0.03–0.07 for prison |

**Licensed.** Evaluating the magnitude of each failure mechanism of §2.6 at values a reader can recompute from published sources, and locating the break-even $\eta$ at which the composed boundary crosses unity.

**Not licensed.** Any statement that a named trial's incidence estimate is biased, or by how much. Any point estimate of $\eta$. Any claim that the values above characterise a population other than US PWID catchments, or that custody is the dominant unobservability mechanism in any specific setting.

**Stated limitations.** State-level jail rates are unpublished, so the jail component applies a national jail:prison ratio and the *ordering* of occupancy across sites is more reliable than its level. The injection enrichment is North-America-wide applied per state, understating between-state spread if enrichment correlates with incarceration. BJS imprisonment counts sentenced prisoners, so pretrial detention enters only through the jail component. Degenhardt's numerator is "ever injected" against Bradley's current-injection denominator, which biases Route B upward.

**Falsifiability.** Every occupancy is a published rate times two stated constants, so any reader can recompute it, and the construction makes a testable prediction: if PURPOSE 4 reports screening-to-enrolment attrition by site, Newark and the Bronx should show the least observability loss and Houston the most.

---

## Drafting notes (not for submission)

**References to complete.** NHBS MMWR 2021;70(42); Feder 2022 doi:10.1016/j.drugpo.2022.103842; Sun 2022 doi:10.1111/add.15659; Degenhardt 2026 doi:10.1016/j.drugpo.2025.105062; Bradley 2023 doi:10.1093/cid/ciac543; Tempalski 2013 PMID 23755143; Gough 2010 doi:10.1186/1471-2458-10-777; BJS *Jail Inmates in 2023* and *Prisoners* series; Census PEP 2019 `cc-est2019-alldata`. The bibliography lives on the predecessor repository's `master` branch, not `main`.

**Do not import the audit record's scenario conclusions.** Appendices A.3, G.1 and I.3 report zero-bias boundaries and "crosses" verdicts computed under the restricted model with $\eta_k=0$, before the cancellation theorem. Those are now the $\eta=0$ corner of the sensitivity surface, not conclusions. §4 reports the surface; §3 must not smuggle the corner back in as a headline.

**Unresolved.** $c$ is coded as 0.25 y (91.3 d) while PURPOSE specifies 90 d; the table above states the coded value. Out-migration is unsourced and should either be retrieved from ACS or explicitly scoped out in the limitations.

**Possible relocation.** §3.2's CEPHIA re-estimate is arguably a result rather than an input. It is placed here because §4 treats $\varphi$ as given; move it if the empirical fit is to carry weight of its own.
