# ASSUMPTIONS.md

Every assumption the paper relies on, where it comes from, what depends on it, and what happens when it fails.

Reviewer 1 of the predecessor manuscript asked that assumptions be *stated* rather than discovered inside derivations. This document is the response. Each entry names the result that would fail, so a reader can work out which conclusions survive a given objection without re-deriving anything.

---

## 1. Inherited from Gao & Bannick (2022)

These are not ours. They are the conditions under which the snapshot and adjusted cross-sectional estimators are consistent in the absence of eligibility dynamics, and we adopt them unchanged. *Stat Med* 2022;41:1446–61.

| | Statement | Needed for |
|---|---|---|
| **A.1** | $\varphi(u) = 0$ for $u$ beyond some finite $\tau$ — the assay is perfectly specific for sufficiently old infection | snapshot estimator |
| **A.2** | Infection time uniform over $[t-\tau,\,t]$ among eligible infected individuals | snapshot estimator |
| **B.1** | $\varphi(u)$ constant at $\beta_{T^*}$ for $u \ge T^*$ — constant false-recency rate in the tail | adjusted estimator |
| **B.2** | Infection time uniform over $[t-T^*,\,t]$ among eligible infected individuals | adjusted estimator |
| **C** | Restricted incidence and prevalence equal their unrestricted values over the window: $\lambda^*_t(s) = \lambda(s)$, $p^*_t(s) = p(s)$ | both; **this is the assumption our work generalises** |
| **D** | $\lambda(s) = \lambda(t)$ and $p(s) = p(t)$ over $[t-c,\,t]$ | implies A.2 / B.2 given C |

**Assumption C is the point of contact.** Gao & Bannick state it holds approximately "when only a small proportion of the subjects move in and out of the eligible population in a time span of $c$," and hold it fixed throughout their numerical work. For the adjusted estimator $c = T^* = 2$ years. Our $Z(t)$ process is a model for what happens when C fails.

**B.1 is violated in real data.** The empirical CEPHIA recency curve does not have a flat tail: the test-recent proportion falls from 9.9% at 730–1095 days to 5.8% at 1095–1825 days to zero beyond. Gao & Bannick's own §3.6 quantifies the cost. We record this rather than assume it away; see `tests/test_empirical_phi_tail_is_not_flat`.

---

## 2. Introduced here

| | Statement | Fails when | Breaks |
|---|---|---|---|
| **E.1** | $Z(\cdot)$ is a time-homogeneous Markov jump process on $\mathcal{S}$ with $X$ absorbing | sojourn distributions are non-exponential; recidivism gives history dependence | Theorems 1–2 as stated. **But not Corollary 2** — see §5 |
| **E.2** | Given $U=u$ and $Z(t)=E$, assay response is independent of the path $\{Z(s):s<t\}$ | custody alters ART exposure, viral suppression, or biomarker trajectory | Theorem 1; $\varphi(u\mid\text{path}) \ne \varphi(u)$ |
| **E.3** | $Q_1 = Q_0$: infection does not alter the transition law | diagnosis changes movement; illness changes custody risk | Corollary 2 (mechanism **M3**) |
| **S** | Neutral cross-sectional sampling: inclusion probability $\kappa_t$ common to observable HIV-positive and HIV-negative individuals | sampling itself is status-dependent | Theorem 1. Note that *non-neutral* selection is Pan's $Q$, treated separately — it is not hidden in $\kappa_t$ |
| **L** | $\lambda_E$ locally constant over $[t-T^*,\,t]$ | epidemic trend within the recency window | Theorem 2's substitution $\lambda_k = \lambda_E\eta_k$ |

E.1 and E.3 are stated separately on purpose. E.1 concerns **memory structure**; E.3 concerns whether **infection changes the movement law**. Merging them would make mechanism M3 invisible.

---

## 3. The cancellation conditions

Corollary 2 — the paper's central result — requires five conditions. They are numbered in the manuscript because conflating the first two was an actual error during drafting.

| | Condition | Note |
|---|---|---|
| **(1)** | **State stationarity**: $\boldsymbol\pi^{\!\top}Q = \mathbf{0}^{\!\top}$ | fixes living-state *proportions* |
| **(2)** | **Demographic stationarity**: $g_E(u;t) \equiv 1$ | fixes the observable susceptible *total* |
| **(3)** | State-invariant acquisition: $\eta_k \equiv 1$ | |
| **(4)** | Infection-independent movement (E.3) | |
| **(5)** | No absorbing loss | |

**(1) and (2) are different conditions and both are required.** A composition-stable pool growing at rate $\rho$ satisfies (1) and not (2): $s_t(u) \equiv 1$ but $g_E(u;t) = e^{-\rho u}$, so $w_t \not\equiv 1$ and the estimator is biased. Guarded by `tests/test_state_stationarity_alone_insufficient`.

---

## 4. Which results need which assumptions

| Result | Requires |
|---|---|
| **Theorem 1** (recent-count identity) | E.1, E.2, S, $\beta_{T^*}=0$ |
| **Theorem 2** (probability limit) | Theorem 1's conditions + (A.1–A.2 or B.1–B.2) + L |
| **Corollary 0** (constant growth) | Theorem 2 + stable composition over the window |
| **Corollary 1** (Gao–Bannick recovery) | Theorem 2 + single living state + no transitions + **(2)** |
| **Corollary 2** (exact cancellation) | Theorem 2 + (1)–(5) |
| **Corollary 3** (frailty mixture) | (1)–(5) **within each stratum**; arbitrary mixing weights |
| **Corollary 4** (absorbing only) | Theorem 2 + sole transition $E \to X$ |
| **Corollary 5** (mixed) | Theorem 2 |
| **§2.7 Pan composition** | the above + Pan's S.1–S.3 (§6) |

Corollary 4 is the one that matters empirically, and it needs the *fewest* assumptions of the substantive results.

---

## 5. Assumptions deliberately *not* made

Stated because their absence is easy to miss and each is a place where the paper is stronger than it might appear.

**Detailed balance / reversibility.** Corollary 2 needs stationarity only. The result concerns *transient* or *bidirectional* movement, not reversible movement. Do not describe it as requiring reversibility.

**Exponential sojourns, for the cancellation result.** Corollary 3 permits arbitrary mixtures of stationary Markov strata, and **the marginal movement process of such a mixture need not be Markov**. So the cancellation survives the obvious objection that carceral contact is recurrent and concentrated in a high-propensity subgroup. A fully general semi-Markov treatment is out of scope and is not claimed.

**$\eta_k \le 1$.** Acquisition may be *higher* in an unobservable state. $w_t$ may then exceed one on part of the window, which is why Remark 5 states the boundary condition as $\Omega_w < \Omega_{T^*}$ with $K_w > 0$ rather than as pointwise $w_t < 1$.

**Differential hazard between infected and uninfected.** The predecessor manuscript's third limitation treated equal hazards as a first-order approximation and argued a differential would "modify but not eliminate" the bias. The logic is inverted: in a closed cohort the differential is what *creates* the bias, and in a demographically stationary catchment none is needed.

**A particular recency function.** The zero-bias boundary $r^\star = e^{-\theta c}$ is free of $\varphi$ — exactly, under a Poisson inter-test process. $\varphi$ governs the magnitude of bias away from the boundary, not its location.

**Zero acquisition in unobservable states.** This *was* assumed, implicitly, by the predecessor analysis. It is the special case $\eta_k = 0$, it is empirically untenable, and exposing it is the reason the conclusion changed. See `docs/PROVENANCE.md` §3, finding 10.

---

## 6. Additional assumptions when composed with Pan et al. (2026)

§2.7 places our process upstream of Pan's selection operators. Their assumptions then apply in addition. *Am J Epidemiol* 2026, doi:10.1093/aje/kwag075, Web Material §S.4.1.

| | Statement |
|---|---|
| **S.1** | Constant incidence in the source eligible population over $(t_{cs}-T^*,\,t_{cs})$; constant hypothetical placebo incidence over follow-up; constant prevalence |
| **S.2(i)** | Attendance propensity determined solely by the most recent HIV test result: $Q \perp (U,S,R,C)\mid\Delta$ |
| **S.2(ii)** | $\alpha = 1$ — a technical condition equating the testing-criterion inclusion probability for HIV-negative individuals and those acquiring at $t_{cs}$ |
| **S.2(iii)** | HIV-negative individuals in the survey population are randomly sampled for enrolment |
| **S.3(i)** | Recency result depends only on infection duration: $R \perp (S,C,Q)\mid U$ |
| **S.3(ii)** | $\varphi(u) = \beta_{T^*}$ for $u > T^*$ (their form of B.1) |

**S.2(i) is where our mechanism would enter their framework if expressed as attendance** rather than as population membership. We deliberately do not do that: the two readings differ in whether the individual remains in the source population, and conflating them is what made the predecessor's stage structure unrecoverable.

---

## 7. Known violations, with evidence

Recorded so a reader need not discover them independently.

| Assumption | Status | Evidence |
|---|---|---|
| **B.1** (flat FRR tail) | violated in CEPHIA | test-recent proportion 9.9% → 5.8% → 0 across 730–1095, 1095–1825, >1825 d |
| **C** (restricted = unrestricted) | violated by construction in populations with material eligibility movement | the reason this paper exists |
| **E.3** ($Q_1 = Q_0$) | plausibly violated | diagnosis may alter engagement and movement; untested |
| **(3)** ($\eta_k = 1$) | violated; magnitude unclear | Gough et al. 2010: 0.08 vs 1.14–2.78 per 100 PY, so $0 < \eta \ll 1$ for continuous incarceration. No contemporary PWID-specific estimate exists |
| **L** (local constancy of $\lambda_E$) | untested | would require within-window trend data |

$\eta$ is the load-bearing unmeasured parameter. It cannot be identified from state-level PWID HIV surveillance — that would require studies comparing acquisition during custody versus community person-time. The appropriate treatment is a sensitivity surface with any literature range *overlaid, not fitted*.

---

## 8. Regression tests

Two assumption errors were made during development. Both are now guarded:

| Test | Guards |
|---|---|
| `test_state_stationarity_alone_insufficient` | conflating (1) with (2) |
| `test_corollary_1_requires_demographic_stationarity` | omitting (2) from Corollary 1 |
| `test_eta_zero_recovers_restricted_model` | validating the restricted model against an *independent* implementation rather than against itself |

See `tests/` and `docs/PROVENANCE.md` §8.
