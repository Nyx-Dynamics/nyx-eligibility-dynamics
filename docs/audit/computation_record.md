# Kassanjee / Paper A — computations and results

**Compiled:** 26 September 2026
**Subject:** QAIV24714 (*Calibration-to-Deployment Mismatch in HIV Prevention Trials*), JAIDS — declined after review
**Purpose:** Record of every computation run during the audit and the Paper A derivation, with the numbers, the scripts that produced them, and what each one establishes.

All figures below were computed independently rather than taken from the manuscript, the reviewer reports, or the planning memos. Where a computation contradicted something I had said earlier in the session, that is stated explicitly.

---

## 0. Provenance

| Input | Version / identifier |
|---|---|
| Manuscript | QAIV24714-2 (main text v2), supplement v10.2 |
| Decision letter | Reviewer comments + Lippincott transfer offer; no editorial decision paragraph present |
| Pan et al. | *Am J Epidemiol* 2026, doi:10.1093/aje/kwag075; preprint arXiv:2412.12316 v1, 16 Dec 2024; Web Material (supplement) |
| Gao & Bannick | *Stat Med* 2022;41:1446–1461, doi:10.1002/sim.9296 |
| Bannick et al. | *Stat Med* 2024;43:3125–3139, doi:10.1002/sim.10112 |
| Wang, Duerr & Gao | *Stat Med* 2025;44:e70216, doi:10.1002/sim.70216 |
| CEPHIA public-use dataset | 2021-06-04 release, Zenodo record 4900634 |
| XSRecency | tag 0.1.0 (2021-11-17), tag 0.2.0 (2023-08-22), `main` as of 2025-07-07 |
| Wang simulation code | github.com/qii-wang/HIV-incidence-recency-heterogeneity |
| Bannick simulation code | github.com/mbannick/RITA-plus-sims |

Constants used throughout unless stated: `T* = 2 y`, `c = 0.25 y` (PURPOSE 90-day exclusion), `τ = 173 d`, `d_visit/2 = 22.5 d`, 365.25 d/yr for CEPHIA and XSRecency work, 365 d/yr where reproducing manuscript figures.

---

## 1. Audit of the submitted manuscript

### 1.1 B_IRR: γ moves the bias the wrong way

`B_IRR = ρ_int / ρ_screen`, with `ρ_int = (1+r)/2 · exp(−γ·d_visit/2)` and `ρ_screen = exp(−γτ/2)`.

Because `τ/2 = 86.5 d` greatly exceeds `d_visit/2 = 22.5 d`, raising γ drives `ρ_screen` down faster than `ρ_int`. **B_IRR is increasing in γ.** Published Table S3 values reproduce to four decimals, so the decomposition is against the manuscript's own numbers:

| configuration | γ (10⁻⁴/d) | r | B_IRR |
|---|---|---|---|
| Jackson baseline | 5.01 | 0.936 | 0.9995 |
| γ → Hartford, r held | 15.79 | 0.936 | **1.0709** |
| r → Hartford, γ held | 5.01 | 0.752 | 0.9045 |
| both → Hartford (published) | 15.79 | 0.752 | 0.9692 |

Structural censoring acting alone puts B_IRR **above** unity. As γ → 0 the factor collapses to `(1+r)/2` = 0.968 at Jackson's retention — a plain dropout artifact with no censoring in it.

**Conclusion.** The entire monotone decline across the 34 MSAs is carried by the retention function `r = max(0.93 − 0.008(L−15), 0.70)` (Eq. 13), which is asserted with two anchors and no fit. The named mechanism works against the headline.

### 1.2 Mixed basis determines the sign

Eq. 3 derives `Ω*/Ω = 1/(1+γτ)` from an exponential `P_R(t)`. Eq. 7 models the same screening-side quantity as `exp(−γτ/2)` from a uniform-window `P_R(t)`. Using the exponential-consistent form for both:

| city | B_IRR, uniform basis (published) | B_IRR, exponential-consistent |
|---|---|---|
| Jackson | 0.9995 | **1.0401** |
| Milwaukee | 0.9989 | **1.0403** |
| New York | 0.9899 | **1.0516** |
| Hartford | 0.9694 | **1.0764** |

Supplement §S2.3 already states this: *"Under the alternative exponential-basis-consistent form ρ_screen = 1/(1+γτ), the joint bias factor B_IRR inverts sign across the AIDSVu range."* Main-text §5.6 says the direction only "reverts" **outside** the empirical range — a discrepancy between main text and supplement.

### 1.3 §S1.4's own confidence interval contains 1

`Var(log B_IRR) = [(d_visit/2) − (τ/2)]²σ_γ² + [1/(1+r)]²σ_r²`

At the stated midpoint (γ = 8×10⁻⁴/d, r = 0.88, σ_γ/γ = 0.3, σ_r = 0.05):

- `(22.5 − 86.5)² = 4096`; `σ_γ² = 5.76×10⁻⁸` → 2.359×10⁻⁴
- `(1/1.88)² = 0.2830`; `σ_r² = 0.0025` → 7.08×10⁻⁴
- Sum 9.44×10⁻⁴, **SD = 0.0307** (supplement says 0.030 ✓)
- 95% CI on B_IRR = 0.992 × exp(±1.96×0.0307) = **[0.932, 1.051]**

The interval contains 1 and is wider than the entire 34-city spread of B_IRR (0.969–0.999). The supplement's claim that 0.992 is "robustly distinguishable from unity" is contradicted by the number in the preceding clause.

### 1.4 Assumption C exit fractions

Gao & Bannick's Assumption C holds when "only a small proportion of the subjects move in and out of the eligible population in a time span of c." For the adjusted estimator `c = T* = 730 d`. At the manuscript's own γ:

| population | γ (10⁻⁴/d) | exit over T* = 730 d | exit over τ = 173 d |
|---|---|---|---|
| general population | 1.00 | 7.0% | 1.7% |
| Jackson MS (lowest AIDSVu) | 5.01 | 30.6% | 8.3% |
| Milwaukee WI | 5.14 | 31.3% | 8.5% |
| New York NY | 8.04 | 44.4% | 13.0% |
| Hartford CT (highest) | 15.79 | **68.4%** | 23.9% |
| PWID severe (Table S5) | 20.00 | **76.8%** | 29.2% |

Gao & Bannick never test this: *"Throughout the simulations, we assume that Assumption C on approximation of the eligible population always hold."* (§3, Numerical Studies, verbatim.)

### 1.5 The same γ values read as annual rates

| γ (10⁻⁴/d) | annual removal (absorbing reading) |
|---|---|
| 5.0 (manuscript anchor) | 16.7% |
| 8.04 (New York) | 25.4% |
| 15.79 (Hartford) | **43.8%** |
| 20.0 (PWID severe) | 51.8% |

Whatever makes the Assumption C violation dramatic makes the hazard implausible. This is the magnitude problem; §5 below retires it.

### 1.6 Eq. 5 drops the FRR term

The manuscript uses the adjusted estimator, whose denominator is `(Ω − βT*)`, but reports the bias as `Ω*/Ω`. The correct ratio is `(Ω* − βT*)/(Ω − βT*)`:

| β | city | published Ω*/Ω | correct | difference |
|---|---|---|---|---|
| 0.005 | Hartford | 0.7855 | 0.7809 | 0.0046 |
| 0.010 | Hartford | 0.7855 | 0.7761 | 0.0094 |
| 0.020 | Hartford | 0.7855 | 0.7658 | 0.0198 |

Small in magnitude; reads as carelessness about which estimator is being corrected.

### 1.7 Numerator/denominator cancellation (Reviewer 1's first objection)

Microsimulation of the snapshot estimator. γ₁ = infected removal hazard, γ₀ = HIV-negative:

| population structure | γ₁, γ₀ (10⁻⁴/d) | λ̂ / λ_true |
|---|---|---|
| replenished pool — no removal | 0, 0 | 1.013 |
| replenished pool — non-differential | 5.0, 5.0 | **0.929** |
| replenished pool — differential | 15.8, 0 | **0.793** |
| closed cohort — non-differential | 5.0, 5.0 | 1.053 |
| closed cohort — non-differential | 15.8, 15.8 | 0.977 |

Replenished matches the closed form (0.929 vs analytic 0.925; 0.793 vs 0.794). Closed cohort with non-differential removal largely cancels. **Which regime applies is a demographic assumption the manuscript never states.** Resolved in §7 below.

Note: §5.6's third limitation has this backwards — it claims differential hazard "would modify but not eliminate" the deflation, when in a closed cohort the differential is what *creates* it.

---

## 2. Literature verification

### 2.1 Reviewer 2's three PMIDs

| PMID | DOI | Citation |
|---|---|---|
| 34984710 | 10.1002/sim.9296 | Gao F, Bannick M. Statistical considerations for cross-sectional HIV incidence estimation based on recency test. *Stat Med* 2022;41:1446–1461 |
| 40779330 | 10.1002/sim.70216 | Wang Q, Duerr A, Gao F. Addressing population heterogeneity for HIV incidence estimation based on recency test. *Stat Med* 2025;44:e70216 |
| 38803064 | 10.1002/sim.10112 | Bannick M, Donnell D, Hayes R, Laeyendecker O, Gao F. An enhanced cross-sectional HIV incidence estimator that incorporates prior HIV test results. *Stat Med* 2024;43:3125–3139 |

Reviewer 1 cited no literature. Reviewer 2's fourth request (comparison to prospective incidence) is answered by `10.1002/jia2.25830` (Klock, HPTN 071 PopART, *JIAS* 2021) and `10.1002/jia2.70204` (Gao et al., Lima three-method comparison, *JIAS* 2026).

### 2.2 Prior art on §3

**Pan J, Bannick M, Gao F.** *Am J Epidemiol* 2026, doi:10.1093/aje/kwag075. arXiv v1 **16 Dec 2024**; received 8 Aug 2025; accepted 26 Mar 2026; **published 6 Apr 2026**. QAIV24714 submitted **22 May 2026** — 46 days later, uncited.

Formalises the PURPOSE testing-based exclusion, derives its limiting estimation error, and concludes the criterion *mitigates* rather than guarantees bias. Their Table 1 signs the error: `c = 0`, `r < 1` → underestimation; `c ≥ T*` → zero; `c ∈ (0,T*)`, `r < 1` → **indeterminate**. PURPOSE sits in the last cell (`c = 0.25 y`, `T* = 2 y`, `r = 0` by design).

They also supply a mechanism §3 omits: people stop testing after diagnosis, so excluding recent testers disproportionately *retains* HIV-positives and pushes the estimate up.

### 2.3 Structural findings in the other three

- **Gao & Bannick 2022 §2.1**: eligibility `A(t)` explicitly includes being alive; `λ(t) = Pr(T=t | T≥t, A(t)=1)`; `φ(u,t) = Pr(M∈ℛ | T=t−u, A(t)=1)` — conditional on observability. **Remark 1**: Kassanjee's original `P_R(u) = Pr(A(t)=1, M∈ℛ | T=t−u, A(t−u)=1)` contains an eligibility-survival component; Gao–Bannick condition it away. **Remark 2 / §3.6**: calibration-vs-deployment mismatch already established for β (FRR).
- **Wang 2025**: motivating paragraph is the manuscript's thesis; weighting estimators for internal and external target populations; footnote assumes X captures all effect modifiers and is time-independent; discussion names time-dependent factors as the open problem. Funding verified at source 30 Sep 2026: NIH R01AI177078, R01DA032106, R37AI029168 **and** Gilead ISR-US-20-10990 — NIH-plus-industry, not industry alone, which the earlier note implied by omission. Wang, not Pan; Pan's paper is separately funded.
- **Bannick 2024**: PT-RITA repairs *misclassification*, not selection. Assumption 4 `(Q,T) ⊥ U` is flagged as violated by stop-when-positive testing and studied in simulation. Discussion defers *awareness-based* sample non-entry to future work — not removal after infection.

---

## 3. CEPHIA MDRI estimation

Evaluation Panel, LAg-Sedia consolidated `final_result` ODn, subtypes A1/B/C/D, logit polynomial in years, GEE clustered by participant, no EDDI-interval filter (XSRecency's approach):

| algorithm | MDRI (d) | 95% CI | participants |
|---|---|---|---|
| subtype C, ODn ≤ 1.5 & VL > 75 | **182.4** | 161–213 | 194 |
| subtype C, ODn ≤ 1.5 & VL > 1000 | 154.3 | 135–182 | 194 |
| subtype B, ODn ≤ 1.5 & VL > 75 | 171.3 | 142–219 | 229 |

Pan's published 163 d for subtype C falls inside both intervals. Stable across polynomial degree (3 vs 4) and fit horizon (2.2 y vs 5 y). **No discrepancy to report.** The usable finding is that MDRI carries roughly ±25 d, which belongs in the delta-method variance.

An earlier unrestricted isotonic fit across all subtypes gave 324 d — an artifact of the wrong estimation procedure, not a real disagreement.

Raw empirical recency curve (LAg ODn<1.5, treatment-naive, non-elite-controller, n=4,184): the tail is **not flat** — 9.9% at 730–1095 d, 5.8% at 1095–1825 d, 0 beyond. A directly observable violation of Gao–Bannick Assumption B.1.

Gamma construction verified against `XSRecency::get.gamma.params`: `shape = W/(2H−W)`, `rate = 1/(2H−W)`, 365.25 d/yr. Window 101 d / shadow 194 d → shape 0.3519, rate 1.2718 (published 0.352, 1.273 ✓).

---

## 4. LEL with removal: validation and the threshold

### 4.1 Reproduction of Pan's published values

Generalised LEL with observability `s(u)`:

```
LEL = log( Ω_s − (1 − r·e^{θc})·K_s ) − log Ω
  Ω   = ∫₀^{T*} φ(u) du
  Ω_s = ∫₀^{T*} φ(u) s(u) du
  K_s = ∫_c^{T*} φ(u) s(u) [1 − e^{θ(c−u)}] du
```

With `s ≡ 1` this reduces to Pan's §S.7.1 exactly. Against their arXiv Table 1 (bias ×10⁻³), 98-day gamma basis:

| c | θ | r | formula | published |
|---|---|---|---|---|
| 0 | 1 | 0 | −9.97 | −9.95 |
| 0 | 1 | 0.6 | −3.99 | −3.98 |
| 0 | 2 | 0 | −15.06 | −15.03 |
| 0.25 | 1 | 0 | −5.94 | −5.93 |
| 0.25 | 1 | 0.6 | −1.36 | −1.36 |
| 0.25 | 1 | 1 | 1.69 | 1.68 |
| 0.25 | 2 | 0 | −8.98 | −8.97 |
| 0.25 | 2 | 0.6 | −0.10 | −0.10 |
| 0.25 | 2 | 1 | 5.83 | 5.82 |

All nine cells within 0.03×10⁻³.

### 4.2 Pan's own formula signs their indeterminate cell

Setting §S.7.1 to zero requires `1 − r·e^{θc} = 0`, so **r\* = e^{−θc}**. Numerical roots at c = 0.25 y: 0.882, 0.779, 0.607 for θ = 0.5, 1, 2 — matching `e^{−θc}` exactly. Pan derive the expression and never solve it; their Table 1 records "?".

### 4.3 Removal widens the underestimation region

`r*_γ = e^{−θc}·[1 + (Ω − Ω_s)/K_s]`, strictly greater than `e^{−θc}`. Closed form reproduces the numerical root to three decimals.

**r\* across four recency bases, c = 0.25 y.** `r* > 1` means underestimation for *every* r ≤ 1:

| basis | MDRI (d) | θ | γ=0 | γ=.05 | γ=.10 | γ=.20 |
|---|---|---|---|---|---|---|
| gamma 101/194 (Pan arXiv) | 97.5 | 0.5 | 0.882 | **1.070** | **1.269** | **1.704** |
| gamma 163/260 (Pan AJE) | 151.4 | 0.5 | 0.882 | **1.060** | **1.248** | **1.660** |
| gamma 173/306 (Sedia-like) | 155.1 | 0.5 | 0.882 | **1.056** | **1.241** | **1.646** |
| CEPHIA empirical (isotonic) | 323.6 | 0.5 | 0.882 | **1.051** | **1.230** | **1.623** |
| gamma 101/194 | 97.5 | 1.0 | 0.779 | 0.877 | 0.980 | **1.205** |
| CEPHIA empirical | 323.6 | 1.0 | 0.779 | 0.869 | 0.965 | **1.174** |

On the properly estimated logit-GEE CEPHIA φ the thresholds are slightly **larger** than parametric: at θ=1, γ=0.2, subtype C VL>75 gives **1.258** vs 1.187 for gamma 163/260. (LEL *magnitudes* are 25–35% smaller on the empirical basis — a different quantity.)

**This retires the magnitude objection.** γ = 0.05–0.20/yr is 1.4–5.5×10⁻⁴/d, at or below the range §1.5 called hard to defend. The contribution is not the size of the Ω\* deflation (0.4–4.7% at defensible mortality) but the movement of a sign threshold.

### 4.4 Denominator inflation at defensible absorbing rates

| annual rate | γ (10⁻⁴/d) | Ω*/Ω | denominator inflation |
|---|---|---|---|
| 1% | 0.28 | 0.9956 | 0.4% |
| 2% | 0.55 | 0.9911 | 0.9% |
| 5% | 1.41 | 0.9777 | 2.3% |
| 10% | 2.89 | 0.9551 | 4.7% |
| 20% | 5.75 | 0.9092 | 10.0% |

Manuscript's range for comparison: 8.9% (Milwaukee) to 27.3% (Hartford). Those require 18.0% and 45.3% annual permanent exit respectively, or 12.0% and 29.5% of person-time unobservable under a 90-day transient sojourn.

---

## 5. Scope of the assay-invariance result

Writing A(u) for the aware branch, B(u) for the unaware branch, `P₀ = Pr(S>c | D=0)`, `δ(u) = A+B−P₀`:

```
r* = 1 − ∫φ(u)δ(u)du / ∫φ(u)A(u)du
```

φ-free **iff δ(u) = k·A(u) pointwise**. Under exponential inter-test this holds exactly:

```
δ(u) = (1 − e^{−θc})·A(u)      ⇒   r* = e^{−θc}
```

A memorylessness identity, not a property of the estimator.

**Under Pan's uniform variant** (§S.6, `X ~ Unif[0,b]`, equilibrium backward-recurrence density from Lemma S.3, `P₀ = (1−c/b)²`), proportionality fails pointwise — `δ/A` spreads 0.031 (b=3) and 0.016 (b=4) against a 0.002 Monte Carlo noise floor. But the φ-weighted integral averages most of it away:

| inter-test model | P₀ | r* range over 6 bases | spread | invariance |
|---|---|---|---|---|
| Exponential, θ=1 | 0.7788 | 0.7764–0.7780 | 0.0016 | **exact (provable)** |
| Uniform[0,3] | 0.8403 | 0.9004–0.9054 | 0.0050 | approximate, 0.6% |
| Uniform[0,4] | 0.8789 | 0.9287–0.9309 | 0.0022 | approximate, 0.2% |

Bases spanned MDRI 97–300 d including both CEPHIA logit-GEE fits.

**Claim exactness only for the Poisson case.** And note one false generalisation: **r\* ≠ P₀ in general** — Uniform[0,3] gives P₀ = 0.840 but r\* ≈ 0.904. The identity `r* = Pr(S>c|D=0)` is exponential-specific.

---

## 6. Test 4 — analytic vs Monte Carlo, removal on

Individual-level simulator built to Pan §S.5: constant prevalence p = 0.121 and incidence λ = 0.038/py; flat `Pr(U|D=1)` on `[0, U_max]`, `U_max = p/(λ(1−p)) = 3.623 y` (Lemma S.1); equilibrium renewal testing (Lemma S.3); stop-when-positive construction; selective attendance `q1/q0 = r`; exclusion `S_swp > c`; relative observability `s(u) = e^{−γu}` on the infected only.

### 6.1 Analytic side cross-checked three ways

Pan's closed form on a grid; the same by adaptive quadrature; and an independent route integrating exact A(u), B(u). **Agreement to 5×10⁻¹⁴** — the algebra is exact, so the MC comparison is against a genuinely separate implementation.

### 6.2 LEL agreement, 27 cells

12 replicates × 6M individuals, **independent seeds per cell**, analytic by adaptive quadrature:

- z: mean **−0.16**, sd **1.29**, 15/27 negative, max |z| = 3.24
- Discrepancies ~0.002 log units against LEL spanning −0.38 to +0.17

### 6.3 The threshold reproduces

`LEL(r)` is linear in r given a population, so r\* solves exactly per replicate. 8 replicates × 8M:

| θ | γ | analytic r\* | MC r\* | SE | z | crosses 1 |
|---|---|---|---|---|---|---|
| 0.5 | 0.00 | 0.8825 | 0.8818 | 0.0067 | −0.10 | no |
| 0.5 | 0.05 | 1.0702 | 1.0686 | 0.0063 | −0.26 | **yes** |
| 0.5 | 0.10 | 1.2693 | 1.2691 | 0.0071 | −0.02 | **yes** |
| 0.5 | 0.20 | 1.7036 | 1.7116 | 0.0057 | 1.39 | **yes** |
| 1.0 | 0.00 | 0.7788 | 0.7785 | 0.0029 | −0.12 | no |
| 1.0 | 0.05 | 0.8767 | 0.8742 | 0.0042 | −0.60 | no |
| 1.0 | 0.10 | 0.9803 | 0.9767 | 0.0038 | −0.93 | no |
| 1.0 | 0.20 | 1.2049 | 1.2022 | 0.0043 | −0.62 | **yes** |
| 2.0 | 0.00 | 0.6065 | 0.6049 | 0.0020 | −0.83 | no |
| 2.0 | 0.05 | 0.6568 | 0.6568 | 0.0023 | 0.01 | no |
| 2.0 | 0.10 | 0.7097 | 0.7094 | 0.0028 | −0.09 | no |
| 2.0 | 0.20 | 0.8235 | 0.8287 | 0.0023 | 2.29 | no |

At γ = 0 the simulation recovers `e^{−θc}` (0.8818 / 0.7785 / 0.6049 vs 0.8825 / 0.7788 / 0.6065), so **Pan recovery holds inside the simulator**, not only in the formula.

### 6.4 A methodological correction worth keeping

A first pass showed a −0.0013 offset negative in all 27 cells, which looked like a sign test at p = 2⁻²⁷. **It was an artifact.** Every cell reused seeds 0–9, and since γ and r enter only as deterministic weights, all 27 cells shared one simulated population — the residuals were perfectly correlated, not independent. Independent seeds removed the pattern; a 40M-sample decomposition confirmed both P₀ and the infected-side integral unbiased to ~10⁻⁴ relative.

Reusing a population across parameter cells is good variance reduction for *comparisons between* cells and actively misleading for *agreement tests within* them.

---

## 7. Derivation of s(u)

### 7.1 Model

States: **E** observable (alive, in catchment, reachable at screening); **O** temporarily unobservable (custody, displacement, hospitalisation), returns to E; **X** permanently gone (death, permanent out-migration), absorbing.

Rates per year: `E→O = α`, `O→E = β`, `E→X = μ`, `O→X = μ′`. Subscript 1 = infected, 0 = susceptible.

Counting infections acquired at `t−u` still observable and test-recent at `t`:

```
N_rec = ∫ λ · n₀ᴱ(t−u) · S₁(u) · φ(u) du ,      N₋ = n₀ᴱ(t)

⇒  λ̂/λ = ∫ φ(u) s(u) du / ∫ φ(u) du

with   s(u) = S₁(u) · n₀ᴱ(t−u)/n₀ᴱ(t) = S₁(u) · e^{−ρu}
```

`S₁(u) = Pr(in E at t | in E and infected at t−u)`; `ρ = d log n₀ᴱ/dt`.

### 7.2 Closed form

With `a = α+μ`, `b = β+μ′`, `x₁,₂ = [−(a+b) ± √((a−b)² + 4αβ)]/2`:

```
S₁(u) = [ e^{x₁u}(x₁+b) − e^{x₂u}(x₂+b) ] / (x₁ − x₂)
```

Verified against matrix exponentiation to **10⁻¹⁵** across absorbing-only, transient-only, mixed, and long-sojourn parameterisations.

**Limits:**

- **Absorbing only** (α = 0): `S₁(u) = e^{−μu}` — decays without a floor.
- **Transient only** (μ = 0): `S₁(u) = (1−q) + q·e^{−(α+β)u)}`, `q = α/(α+β)` = share of person-time unobservable. Floor at `1−q`, relaxation rate `α+β`. For jail-length sojourns (30–60 d) that is 6–12/yr, so S₁ sits at its floor across most of the recency window.

### 7.3 ρ is the answer to Reviewer 1

ρ is **not** `1/S₀(u)` — the natural first guess, and wrong. The O compartment feeds back into E, and infection itself depletes the susceptibles. It must be propagated from the susceptible generator `M = [[−(α₀+μ₀+λ), α₀], [β₀, −(β₀+μ₀)]]` starting from `n = (1,0)`, which also handles the case where O is unreachable.

λ̂/λ under exponential φ (τ = 173 d, T* = 2 y), μ₁ = 0.10/yr:

| catchment | ρ | s(u) | μ₀=0 | μ₀=0.05 | μ₀=0.10 |
|---|---|---|---|---|---|
| **Stationary** | 0 | `e^{−μ₁u}` | **0.957** | **0.957** | **0.957** |
| Closed, no λ-depletion | −μ₀ | `e^{−(μ₁−μ₀)u}` | 0.957 | 0.978 | 1.000 |
| Closed, with λ-depletion | −(μ₀+λ) | `e^{−(μ₁−μ₀−λ)u}` | 0.978 | — | 1.023 |

**In a demographically stationary catchment ρ = 0 and there is no cancellation at all, regardless of how large μ₀ is.** The susceptibles' losses are replaced by in-migration and new entrants, so `n₀ᴱ(t−u) = n₀ᴱ(t)` and only the infected cohort's own attrition survives into the ratio. Cancellation requires a *closed cohort*, and trial screening is not one — a metropolitan PrEP-eligible population, PWID subpopulations included, is stable over a two-year window.

This answers Reviewer 1 through the demography rather than by assuming μ₁ ≠ μ₀. The differential-hazard assumption old §5.6 leaned on is not needed.

### 7.4 Simulation verification

Agent simulation, refined timestep (dt = 1/1461 y), 600k initial susceptibles, 2200 days:

| scenario | regime | ρ | predicted | simulated | diff |
|---|---|---|---|---|---|
| absorbing, differential μ₁=.10 μ₀=0 | stationary | 0.0000 | 0.9573 | 0.9622 | +0.0048 |
| absorbing, differential | closed | −0.0500 | 0.9782 | 0.9763 | −0.0020 |
| absorbing, NON-diff μ₁=μ₀=.10 | stationary | 0.0000 | 0.9573 | 0.9511 | −0.0062 |
| absorbing, NON-diff | closed | −0.1500 | 1.0227 | 1.0197 | −0.0030 |
| transient q=10%, 60 d sojourn | stationary | 0.0000 | 0.9241 | 0.9242 | +0.0000 |
| transient q=10%, 60 d sojourn | closed | −0.0450 | 0.9426 | 0.9441 | +0.0016 |
| mixed μ=.05 + transient q=10% | stationary | 0.0000 | 0.9044 | 0.9012 | −0.0033 |
| mixed μ=.05 + transient q=10% | closed | −0.0950 | 0.9426 | 0.9271 | **−0.0155** |

Seven of eight within ±0.007, residuals scattering around zero. The mixed-closed cell moved 0.024 between runs at different timestep and seed — Monte Carlo noise in the most depleted configuration, not a systematic failure; re-run with more replicates before it appears in a paper. **All four stationary rows — which carry the substantive conclusion — land within ±0.007.**

An earlier coarse-timestep run showed a uniform +0.008 offset; refining dt 4× removed it, confirming discretisation as the cause.

---

## 8. Scripts

| file | what it does |
|---|---|
| `lel_removal.py` | Pan §S.7.1 LEL generalised with `s(u)`; validation against arXiv Table 1; r\* sweep |
| `lel_removal_cephia.py` | Same, across four recency bases including empirical CEPHIA; takes the CEPHIA CSV path as argument |
| `xcheck_xsrecency.py` | CEPHIA MDRI by logit-GEE, XSRecency's procedure |
| `mc_removal.py` | Individual-level simulator to Pan §S.5 + removal; analytic vs Monte Carlo |
| `derive_s.py` | `S_closed`, `rho_susceptible`, `s_of_u` — the s(u) derivation with closed forms |

---

## 9. Toolchain note

`createRitaCephia()` changed its unit contract between tag 0.2.0 and `main`:

| version | roxygen doc (line 97) | conversion in code | vignette's extra ÷365.25 |
|---|---|---|---|
| tag 0.2.0 (2023-08-22) | ui in **days** — "may have to convert to years" | none | correct and necessary |
| `main` (current) | ui in **years** | line 207, ÷365.25 | **a second conversion** |

`enhanced.Rmd` was right at 0.2.0 and is wrong against `main`. **Pin to tag 0.2.0** and the vignette is executable ground truth, or use `main` and delete the vignette's conversion line — never mix.

Two corrections to how this has been described: the July 2025 commits to `get-rita-data.R` were a `data.table::as.data.table` fix cycle, not the conversion, so they are not the cause. And because the vignette fits `ri ~ poly(log(ui), 2)`, a constant rescaling of `ui` is absorbable by the polynomial coefficients — the fitted *shape* may survive while the integration domain does not, so its φ curve is more trustworthy than its Ω.

None of this affects the MDRI estimates in §3, which read the raw CSV and divide `days_since_eddi` by 365.25 exactly once.

`XSRecency` v0.2.0 exports `downloadCephia`, `createRitaCephia`, `getRitaOptions`, `estRitaProperties`, `estSnapshot`, `estAdjusted`, `estEnhanced`, `simCrossSect`, `simExternal`, `simPriorTests`, `integratePhi`, `getTestRecentFunc`, `getTestRecentFuncAdj`; imports `geepack::geese`. The simulation study can be built on the exported API rather than forked internals.

---

## 10. Status

**Established:**

- Pan's §S.7.1 signs their own indeterminate cell at `r* = e^{−θc}` — an immediate consequence they did not state
- Removal strictly widens the underestimation region; at θ = 0.5 and γ ≥ 0.05/yr the threshold exceeds 1 on every basis tested
- Exact assay-invariance under Poisson inter-test, approximate (≤0.6%) under uniform
- Analytic LEL and individual-level Monte Carlo agree, including at the threshold
- `s(u) = S₁(u)·e^{−ρu}` derived from population dynamics and simulation-verified
- Reviewer 1's cancellation objection answered by the demography (ρ = 0 in a stationary catchment)

**Does not survive from the submitted manuscript:**

- "The reported IRR understates the true IRR" — sign reverses on the consistent basis, is carried by an assumed retention curve, CI contains unity, and flips in 3 of 10 sensitivity scenarios
- "Structurally guaranteed" bias — the supplement says "conditional on the joint (γ, r) structure"
- Priority on the 90-day eligibility argument

**Open:**

- Re-run the mixed-closed verification cell with more replicates
- Empirical sourcing for μ₁ (mortality + permanent out-migration), q (custody person-time share), β (mean sojourn), and catchment stability for ρ
- The efficacy-ratio question is deliberately out of scope: Pan's LEL targets counterfactual placebo incidence, not observed trial-arm incidence, and removal attenuates both arms

---

# Appendix A — Empirical parameter grounding

Added 26 September 2026. Purpose: separate **sourced** from **derived** from **assumed**, so that illustrative parameter sweeps can be told apart from empirically plausible scenarios.

## A.1 Status of each parameter

| parameter | meaning | status | value / range | source |
|---|---|---|---|---|
| `θ` | background HIV testing rate | **sourced** | 0.844/yr | NHBS 2018, 23 MSAs: 57% of PWID tested in past 12 mo → θ = −ln(0.43). MMWR 2021;70(42) |
| `μ₁` mortality | all-cause death, PWID | **sourced** | 0.037–0.045/yr | ALIVE: 37.2/1000 py (2015–Feb 2020), 39.6/1000 py (2020) — Feder 2022, doi:10.1016/j.drugpo.2022.103842. Age-standardised 23→45/1000 py 1988–2018 — Sun 2022, doi:10.1111/add.15659 |
| `μ₁` migration | permanent exit from catchment | **assumed** | 0.02–0.05/yr | not yet sourced; ACS different-county mover rates are the obvious anchor |
| `q` | share of person-time unobservable | **derived, two routes** | 6–8% (overlap) | see A.2 |
| `β` | return rate from custody | **sourced** | 11.4/yr (32 d) | BJS *Jail Inmates in 2023*: mean 32 d in custody Jul 2022–Jun 2023; males 36 d, females 19 d; jails with ADP ≥2,500 43 d |
| `β` prison | long-sojourn variant | **partly sourced** | ≈0.37/yr | BJS *Prisoners* series, mean time served ≈2.7 y — sojourn comparable to T*, behaves quasi-absorbing within the window |
| `ρ` | catchment demographic stability | **sourced** | ≈0 | Tempalski 2013, PMID 23755143: median PWID prevalence 104.4 → 91.5 per 10,000 aged 15–64 across US MSAs 1992–2007, "relatively stable 2002–2007" |

**Not yet sourced:** permanent out-migration; a fentanyl-era *younger*-cohort mortality estimate (see A.5).

## A.2 q by two independent routes

**Route A — prevalence × duration.** NHBS 2018 past-12-month incarceration among PWID: 21.0% (not homeless), 43.3% (homeless), 23 cities; Boston 43.5%; Texas cycle 29%. BJS mean jail stay 32 d.

| assumption | q |
|---|---|
| 21%, one episode of 32 d | 1.84% |
| 30%, 1.4 episodes (45 d total) | 3.70% |
| 43.3%, two episodes (64 d total) | 7.59% |

**Route B — point-prevalence ratio.** A cross-sectional share equals a person-time share in steady state. US incarcerated ≈1.9 M (BJS: ~1.23 M prison 2022 + ~0.66 M jail ADP); US PWID ≈3.7 M in 2018 (Bradley 2023, *Clin Infect Dis* 76:96, doi:10.1093/cid/ciac543).

| injection prevalence among incarcerated | q |
|---|---|
| 11.9% "ever injected" (global) — Degenhardt 2026, doi:10.1016/j.drugpo.2025.105062 | 6.11% |
| 15% (North America plausible) | 7.70% |
| 20% (North America plausible) | 10.27% |

**Convergence: Route A 1.8–7.6%, Route B 6.1–10.3%, overlap ≈6–8%.** Route B leans high because "ever injected" over-counts against Bradley's current-injection denominator. Route A leans low because it assumes episodes are independent of each other and uses an all-jail mean stay.

Degenhardt 2026 is open access and its country/region-stratified tables would give the North America injection-prevalence-among-incarcerated figure directly, replacing the 15–20% assumption in Route B. That is the single highest-value remaining lookup.

## A.3 Scenarios against the threshold

φ = gamma 163/260 (Pan AJE basis), T* = 2 y, c = 0.25 y, ρ = 0.

| scenario | μ₁ | q | sojourn | Ω*/Ω | S₁(2y) | r* at θ=0.844 | crosses 1 |
|---|---|---|---|---|---|---|---|
| LOW (mort .02 + migr .02, q=2%) | 0.040 | 2.0% | 32 d | 0.9618 | 0.9047 | 0.968 | no |
| **MID** (mort .03 + migr .03, q=4%) | 0.060 | 4.0% | 40 d | 0.9361 | 0.8514 | **1.086** | **yes** |
| HIGH (mort .045 + migr .05, q=7.5%) | 0.095 | 7.5% | 60 d | 0.8955 | 0.7649 | **1.296** | **yes** |
| EXTREME (stress test) | 0.150 | 12.0% | 90 d | 0.8461 | 0.6519 | **1.604** | **yes** |

Holding q = 4% and a 40 d sojourn, **crossing requires μ₁ ≥ 0.024/yr** at θ = 0.844. ALIVE all-cause mortality alone is 0.037–0.045/yr, so **sourced mortality clears the threshold before any out-migration is added.** At μ₁ = 0.06 the threshold is crossed across the entire plausible q range:

| q | Ω*/Ω | r* |
|---|---|---|
| 2% | 0.9522 | 1.012 |
| 4% | 0.9361 | 1.086 |
| 6% | 0.9198 | 1.163 |
| 8% | 0.9035 | 1.244 |
| 10% | 0.8871 | 1.330 |

## A.4 θ depends on the inter-test assumption

§5 established that r\* is only approximately assay-invariant under non-exponential inter-test. The same caution applies to recovering θ from "57% tested in the past year" — calibrating **both** distributions to that same observation:

| inter-test model | implied parameter | mean inter-test |
|---|---|---|
| Poisson | θ = 0.844/yr | 1.18 y |
| Uniform[0,b] | b = 2.905 y | 1.45 y |

| scenario | Poisson r* | Uniform r* |
|---|---|---|
| LOW | 0.967 — no | **1.067 — yes** |
| MID | **1.085 — yes** | **1.193 — yes** |
| HIGH | **1.295 — yes** | **1.418 — yes** |

Uniform is more favourable at every level, so **Poisson is the conservative choice** — and it is what Pan's main analysis uses. But the LOW scenario flips on the assumption alone, so near the threshold the inter-test distribution is not a detail.

## A.5 What this does and does not license

**Licensed as an empirically plausible scenario.** The MID and HIGH rows rest on sourced θ, sourced mortality, sourced sojourn length, sourced ρ, and a q with two converging derivations. The threshold conclusion — removal moves r\* above 1 at realistic parameters — survives sourcing.

**Still illustrative, not plausible.** The EXTREME row, and anything requiring μ₁ > 0.10/yr or q > 12%.

**Does not survive sourcing.** The manuscript's denominator-inflation range. Empirically grounded Ω\*/Ω is **0.90–0.96, i.e. 4–10% inflation**, against the submitted 8.9–27.3%. Hartford's 27.3% would need 45.3%/yr permanent exit or 29.5% of person-time unobservable; neither is defensible for an MSA-wide PrEP-eligible population. **Report the threshold result; drop the magnitude claims.**

**Two caveats to state in the paper.** ALIVE is an ageing cohort — median age 37 at baseline, so 2015–2020 rates describe people in their 50s–60s and likely overstate mortality for a younger PrEP-eligible population; a fentanyl-era younger-cohort estimate is needed and would plausibly *lower* μ₁ toward the LOW row, which is the row that does not cross under Poisson. And the unit of analysis has to be the PWID subpopulation, not the MSA: q of 6–8% is arguable for PWID with heavy carceral contact and not for a general metropolitan PrEP-eligible population.

---

# Appendix B — BJS custody sources (added 26 Sep 2026)

Four BJS statistical-table series were supplied: `mlj0019st` (Mortality in Local Jails 2000–2019), `msfp0119st` (Mortality in State and Federal Prisons 2001–2019), `hivp15st` and `hivp20st` (HIV in Prisons, 2015 and 2020). The PDFs could not be opened locally (macOS quarantine on newly downloaded files), so figures below are from the BJS publication pages and should be confirmed against the tables.

## B.1 In-custody mortality sources μ′

| series | population | all-cause rate, 2019 | per year |
|---|---|---|---|
| `mlj0019st` | local jails | 167 per 100,000 inmates | 0.00167 |
| `msfp0119st` | state prisons | 330 per 100,000 prisoners | 0.00330 |
| `msfp0119st` | federal prisons | 259 per 100,000 prisoners | 0.00259 |

Jail suicide was 49 per 100,000 in 2019, the leading single cause. A drug/alcohol-intoxication figure of 184 appeared in the page summary; since that exceeds the all-cause rate it is almost certainly a **count of deaths, not a rate** — do not cite it without checking the table.

**Model consequence.** All three in-custody rates (0.0017–0.0033/yr) are an order of magnitude *below* community PWID mortality (0.037–0.045/yr, ALIVE). Custody is a mortality refuge during the stay. The three-state model had been carrying μ′ = μ, which is wrong on the evidence.

## B.2 …but μ′ turns out not to matter

Sweeping μ′ with MID parameters held (μ = 0.060, q = 4%, 40 d sojourn, θ = 0.844):

| μ′ | Ω*/Ω | r* |
|---|---|---|
| 0.002 (BJS jail) | 0.9369 | 1.082 |
| 0.010 | 0.9367 | 1.082 |
| 0.020 | 0.9366 | 1.083 |
| 0.040 | 0.9363 | 1.084 |
| 0.060 (= μ) | 0.9361 | 1.086 |
| 0.100 | 0.9355 | 1.089 |

A fifty-fold change in μ′ moves r\* by 0.007. Applied across scenarios:

| scenario | μ′ = μ | μ′ = 0.002 |
|---|---|---|
| LOW | r* = 0.968 (no) | r* = 0.967 (no) |
| MID | r* = 1.086 (yes) | r* = 1.082 (yes) |
| HIGH | r* = 1.296 (yes) | r* = 1.284 (yes) |

**μ′ is non-influential because q is small** — at 4–8% of person-time in state O, the death rate there has almost no leverage on S₁(u). This is a useful negative result: **μ′ can be fixed at μ, or at the BJS rate, without affecting any conclusion, and does not need sourcing.** No scenario changes its threshold verdict.

The BJS mortality series therefore *reduce* the sourcing burden rather than shifting the answer. They also confirm that death in custody is not a material removal channel — removal from observability during custody is the transient `q` mechanism, not mortality.

## B.3 HIV in prisons — what it does and does not establish

`hivp20st`: 11,940 people with diagnosed HIV in state and federal prisons at yearend 2020 (10,790 state, 1,144 federal; 11,280 male, 660 female). Down 15% from 14,180 in 2019. Against a yearend-2020 prison population of roughly 1.22 M, that is **≈1.0% prevalence** — about 2–2.5× the US adult general population (~0.4%), but far below PWID (7%, NHBS 2018, 23 MSAs).

Two things follow, neither of them a parameter:

1. **The incarcerated population is not predominantly PWID.** So Route B for `q` (Appendix A.2) genuinely needs an *injection*-prevalence figure among incarcerated people; HIV prevalence is not a usable substitute. The Degenhardt 2026 regional tables remain the right lookup.
2. **HIV status is not the driver of removal within the recency window.** Untreated HIV causes no excess mortality over two years post-acquisition, so for the recent infections the estimator counts, μ₁ ≈ μ₀ on HIV-specific causes. Removal is driven by the shared structural substrate. This is consistent with §7: in a stationary catchment the bias needs no differential hazard at all, so the mechanism does not depend on HIV causing the removal.

---

# Appendix C — q is now sourced (added 26 Sep 2026)

## C.1 The number

The four BJS folders could not be opened (quarantine block on downloaded directories; direct file paths inside them are blocked too). The BJS *HIV in Prisons* series carries HIV prevalence and testing policy, not injection history, and neither the *Survey of Prison Inmates 2016* drug-use tables (NCJ 252641) nor *Drug Use, Dependence, and Abuse Among State Prisoners and Jail Inmates 2007–2009* contains an injection-route variable — both report drug **type**, not route.

The figure came instead from the source flagged in Appendix A.2 as the right lookup. **Degenhardt et al. 2026, Table 1, North America row** (*Int J Drug Policy*, doi:10.1016/j.drugpo.2025.105062, PMC13058553, open access):

| quantity | value |
|---|---|
| IDU prevalence among incarcerated, North America | **13.4% (95% CI 10.3–16.8)** |
| incarcerated people who have injected drugs | **246,500 (190,500–308,500)** |
| ratio vs general population | 9.6× |
| female / male | 20.6% (15.9–25.8) / 12.7% (9.8–15.9) |

Against Bradley 2023's 3.70 M US PWID:

| | q |
|---|---|
| point estimate | **6.66%** |
| lower CI | 5.15% |
| upper CI | 8.34% |

This replaces the 15–20% assumption in Route B and lands inside the 6–8% convergence band predicted from Route A.

## C.2 Consequence: every scenario now crosses

θ = 0.844, μ′ = 0.002, q = 6.66%:

| scenario | μ₁ | sojourn | Ω*/Ω | r* | crosses 1 |
|---|---|---|---|---|---|
| LOW (mort .02 + migr .02) | 0.040 | 32 d | 0.9234 | **1.142** | **yes** |
| MID (mort .03 + migr .03) | 0.060 | 40 d | 0.9158 | **1.183** | **yes** |
| HIGH (mort .045 + migr .05) | 0.095 | 60 d | 0.9034 | **1.252** | **yes** |

The LOW row previously failed at r\* = 0.968 on an assumed q = 2%. It now crosses, and it crosses at the **lower** CI bound of q:

| q | Ω*/Ω | r* | |
|---|---|---|---|
| 2.0% (old assumption) | 0.9621 | 0.967 | no |
| 5.15% (Degenhardt lower CI) | 0.9360 | 1.083 | **yes** |
| 6.66% (point) | 0.9234 | 1.142 | **yes** |
| 8.34% (upper CI) | 0.9093 | 1.210 | **yes** |

## C.3 The remaining mismatch, quantified

The numerator is *ever* injected; the denominator is *past-year* injection. If only a fraction `f` of ever-injectors among the incarcerated are current injectors, q deflates proportionally:

| f | q | LOW r* | MID r* | HIGH r* |
|---|---|---|---|---|
| 1.0 | 6.66% | 1.142 ✓ | 1.182 ✓ | 1.252 ✓ |
| 0.8 | 5.33% | 1.090 ✓ | 1.131 ✓ | 1.204 ✓ |
| 0.6 | 4.00% | 1.039 ✓ | 1.082 ✓ | 1.156 ✓ |
| 0.5 | 3.33% | 1.015 ✓ | 1.057 ✓ | 1.133 ✓ |
| 0.4 | 2.66% | 0.990 ✗ | 1.034 ✓ | 1.110 ✓ |
| 0.3 | 2.00% | 0.966 ✗ | 1.010 ✓ | 1.088 ✓ |

Break-even points:

- **LOW** fails only if fewer than **44%** of incarcerated ever-injectors are current injectors
- **MID** fails only below **26%**
- **HIGH** crosses on mortality alone, at any f

Also note North America in Degenhardt includes Canada; the US share of that 246,500 is roughly 90% given relative prison populations, which moves q down about 0.7 points — well inside the CI and inside the f-sensitivity above.

## C.4 Revised parameter status

| parameter | status | value |
|---|---|---|
| `θ` | sourced | 0.844/yr (NHBS 2018, 57% tested past 12 mo) |
| `μ₁` mortality | sourced | 0.037–0.045/yr (ALIVE) |
| `μ₁` migration | **still assumed** | 0.02–0.05/yr |
| `μ′` | sourced **and shown non-influential** | 0.0017–0.0033/yr (BJS) |
| `q` | **sourced** | 6.66% (5.15–8.34) |
| `β` | sourced | 11.4/yr (BJS 32 d) |
| `ρ` | sourced | ≈0 (Tempalski 2013) |

**One gap remains: permanent out-migration.** It is the smaller component of μ₁, and since HIGH crosses on mortality alone and LOW crosses at f ≥ 0.44, no conclusion currently rests on it.

## C.5 What this licenses

All three scenarios are now **empirically plausible**, not illustrative — every input except out-migration carries a citation, and the threshold conclusion is robust to the one genuine measurement mismatch (ever- vs current-injection) down to f = 0.44 in the weakest scenario.

Unchanged: the **magnitudes** still do not support the submitted manuscript. Grounded Ω\*/Ω is 0.90–0.92, i.e. **9–11% denominator inflation**, against the submitted 8.9–27.3%. Only the bottom of the manuscript's range survives. Report the threshold; drop the magnitude claims.

---

# Appendix D — Source population: the q₁ formulation

## D.1 The correct quantity

The model needs the *infected* population's unobservability, because under ρ = 0 (§7) s(u) = S₁(u). So:

```
q1 = (PWH in custody) / (total PWH in the source population)
```

not (all incarcerated)/(all population). HIV prevalence *in custody* — PWH/total incarcerated — is a different quantity and is not what enters the model.

**Custody and mortality both remove people from the screening pool, and they do compound — but inside the transition generator, not by addition.** q₁ is a proportion and μ₁ is a rate; they cannot be summed. Numerically, at μ = 0.060/yr and q = 6.66%:

| channel | Ω*/Ω | deflation |
|---|---|---|
| mortality only | 0.9682 | 3.18% |
| custody only | 0.9442 | 5.58% |
| **both, via S₁(u)** | **0.9158** | **8.42%** |

Sum of deflations would be 8.77%, the product 8.59%. The model gives 8.42% — slightly below the product, because someone already in state O is not simultaneously exiting from state E. Neither addition nor multiplication captures that; the matrix exponential does.

## D.2 Custodial PWH

| component | value | source |
|---|---|---|
| PWH, state + federal prison, 2019 | 14,180 | BJS *HIV in Prisons* |
| check: 14,180 / 1,229,855 | 1.153% | matches BJS's reported 1,153 per 100,000 |
| PWH, jail (660k ADP × ~1.3% prevalence) | ≈8,580 | jail PWH is not in the BJS HIV series; estimated |
| **PWH in custody, total** | **≈22,760** | |

## D.3 The source population choice decides the result

θ = 0.844, μ′ = 0.002, all-cause mortality (not AIDS-related — the X state is *dead*, regardless of cause):

| source population | N_PWH | q₁ | μ₁ | Ω*/Ω | r* | crosses |
|---|---|---|---|---|---|---|
| All US PWH | 1,200,000 | 1.90% | 0.019 | 0.9745 | 0.913 | **no** |
| All US PWH, diagnosed only | 1,040,000 | 2.19% | 0.019 | 0.9721 | 0.923 | **no** |
| PWID with HIV | 259,000 | 6.66% | 0.040 | 0.9251 | **1.135** | **yes** |

The all-PWH denominator is dominated by diagnosed, in-care, virally suppressed, older people — low custody, low mortality. It is the wrong reference class for an estimator that counts **recent, undiagnosed** infection, and it depresses both parameters roughly threefold.

Even the all-PWH row is a **floor, not an estimate**: within any source population the recently-infected subset is younger, undiagnosed and not yet in care, so its q₁ and μ₁ exceed the prevalent-pool average. Surveillance does not report either quantity restricted to within-two-years-of-acquisition.

**Structural note.** For a PWID catchment, q₁ = q_PWID exactly — HIV prevalence cancels top and bottom (246,500 × 0.07 ÷ 3.70M × 0.07 = 246,500/3.70M). The refined q₁ and the population-average q are the same number there.

---

# Appendix E — Age restriction

## E.1 Trial-specific age frames

| trial | population | age criterion | source |
|---|---|---|---|
| PURPOSE 1 | AGYW, South Africa / Uganda | **16–25** | Pan 2026 p.2 |
| PURPOSE 2 | cis men, trans women/men, gender-nonbinary with male partners | **≥16** | NCT04925752 |
| PURPOSE 4 | US PWID | **≥18**, no upper bound | NCT06101342 |

There is no single "PURPOSE" age frame, and no single national q should be computed and labelled as such.

## E.2 Age-appropriate mortality

| source | rate | note |
|---|---|---|
| ALIVE (Baltimore) | 0.037–0.045/yr | ageing cohort, median age 37 at baseline |
| **VIDUS, PWID ≤29** | **1,368 per 100,000 py = 0.0137/yr** | age-appropriate for a young frame |
| new-onset PWID | 3.3 per 100 py | |
| PWID range, general | 0.8–3.26 per 100 py | |

Applying a young-age frame cuts μ₁ roughly threefold. But **PURPOSE 4 is ≥18 with no upper bound**, so the full adult PWID age range is in scope and ALIVE is the appropriate source. The VIDUS substitution over-corrects for PURPOSE 4.

## E.3 With q sourced, mortality is no longer load-bearing

At q = 6.66%:

| μ₁ | Ω*/Ω | r* | |
|---|---|---|---|
| 0.0000 | 0.9442 | 1.042 | yes |
| 0.0137 (VIDUS ≤29) | 0.9376 | 1.073 | yes |
| 0.0400 (ALIVE) | 0.9251 | 1.135 | yes |

No break-even μ₁ exists — the custody channel alone carries the threshold. The weight has shifted onto q:

| μ₁ | break-even q |
|---|---|
| 0.0137 | 4.69% |
| 0.0337 | 3.42% |
| 0.0400 | 3.02% |

## E.4 PURPOSE 1 is excluded on geography

AGYW 16–25 in South Africa and Uganda: the custody channel is essentially absent and no plausible mortality crosses.

| scenario | Ω*/Ω | r* | |
|---|---|---|---|
| μ = 0.005, q = 0 | 0.9973 | 0.820 | no |
| μ = 0.020, q = 0.5% | 0.9851 | 0.869 | no |
| μ = 0.040, q = 0 | 0.9786 | 0.897 | no |

US correctional and PWID-mortality data do not describe this population. **PURPOSE 1 must be excluded from the empirical section entirely.**

---

# Appendix F — PURPOSE 4: scoping and site-state matching

## F.1 What PURPOSE 4 actually is

**NCT06101342 = GS-US-528-6363**, registry acronym literally "PURPOSE 4":

| | |
|---|---|
| design | Phase 2, open-label, randomized, no masking |
| enrollment | **181 actual** |
| age | **≥18**, no upper bound |
| primary outcomes | **LEN C_trough wk 26 / wk 52; TEAEs; lab abnormalities** |
| secondary | acceptability, satisfaction, willingness, adherence |
| dates | start 2023-12-13; primary completion **2026-07-27**; completion 2028-01 |
| status | ACTIVE_NOT_RECRUITING; results not presented |
| sponsor | Gilead Sciences |

**Two scoping facts that must be stated in the paper:**

1. **No counterfactual-incidence endpoint.** Every primary outcome is pharmacokinetic or safety. With n = 181 there is no background-incidence estimation — Kassanjee requires thousands screened. Paper A therefore **cannot claim PURPOSE 4's efficacy estimate is biased; there is no efficacy estimate.** The submitted manuscript's Table S5 row "PWID US (PURPOSE 4 projected)" projected an analysis the trial was never designed to perform.
2. **No 90-day prior-testing exclusion** appears in the registered eligibility criteria. Inclusion is a negative rapid Ab/Ag, central Ab/Ag and HIV-1 RNA NAAT; exclusion is self-reported prior positive. The selection operator `c` that Pan's framework turns on is **not present in PURPOSE 4**.

**The defensible framing:**

> PURPOSE 1/2 supply the estimator architecture — they are the trials that use counterfactual incidence with a testing-based exclusion. PURPOSE 4 supplies the contemporary US PWID population for whom incarceration-driven observability loss is operationally relevant. Neither trial is both.

Paper A is then a **prospective design argument**, not a retrospective correction: *if a PWID efficacy trial is run with a counterfactual-incidence anchor and a testing-based exclusion, here are the parameters under which its zero-bias threshold sits above 1, and here is what its SAP should specify.*

## F.2 Site–state mapping

Nine US sites, eight states (verified from the registry):

| site | state |
|---|---|
| UCLA Vine Street Clinic, Los Angeles | California |
| UCSD AntiViral Research Center, San Diego | California |
| University of Miami | Florida |
| Johns Hopkins, Baltimore | Maryland |
| Rutgers NJ Medical School, Newark | New Jersey |
| ICAP Columbia, Bronx Prevention Center | New York |
| University of Pennsylvania, Philadelphia | Pennsylvania |
| Houston AIDS Research Team CRS | Texas |
| West Virginia University, Morgantown | West Virginia |

## F.3 Eight-state distribution (California counted once)

q_s = [state adult (18+) imprisonment rate × (1 + national jail:prison ratio 0.558)] × 9.6 enrichment. μ₁ = 0.040, θ = 0.844.

| state | sites | prison 18+ | +jail | q_s | Ω*/Ω | r* | crosses |
|---|---|---|---|---|---|---|---|
| New Jersey | Newark | 174 | 271 | 2.60% | 0.9578 | **0.985** | **no** |
| New York | Bronx | 199 | 310 | 2.98% | 0.9548 | **0.999** | **no** |
| California | Los Angeles, San Diego | 319 | 497 | 4.77% | 0.9404 | 1.063 | yes |
| Maryland | Baltimore | 322 | 502 | 4.82% | 0.9400 | 1.065 | yes |
| Pennsylvania | Philadelphia | 366 | 570 | 5.48% | 0.9347 | 1.090 | yes |
| West Virginia | Morgantown | 413 | 644 | 6.18% | 0.9290 | 1.116 | yes |
| Florida | Miami | 466 | 726 | 6.97% | 0.9225 | 1.147 | yes |
| Texas | Houston | 601 | 937 | 8.99% | 0.9060 | 1.227 | yes |

| summary | q_s | r* |
|---|---|---|
| median | 5.15% | 1.077 |
| IQR | 4.32 – 6.38% | 1.047 – 1.124 |
| range | 2.60 – 8.99% | 0.985 – 1.227 |
| crosses | **6 of 8 states** | |

**California decision.** CA has two sites but sits *below* the median, so site-weighting pulls the aggregate down (mean q 5.28% vs state-mean 5.35%; mean r\* 1.084 vs 1.087). Report the **8-state distribution**; adopt site-weighting only if site-level enrollment n_j becomes available, in which case q̄ = Σ n_j q_s(j) / Σ n_j.

**This is the reportable claim**: *across the eight states represented in PURPOSE 4, age-compatible correctional observability parameters ranged from 2.60% to 8.99%, and the zero-bias threshold was exceeded in six.* It preserves geographic heterogeneity instead of asserting that Texas, California, West Virginia and New York share one carceral process — and it forecloses the obvious objection by conceding it.

## F.4 PURPOSE 2 US — a separate calculation

60 US sites of 93 total, across 25 states; site-weighted adult imprisonment 406 per 100,000. The discriminator is **enrichment**: Degenhardt's 9.6× is an injection-drug-use ratio and does not transfer to MSM. Granting 2–3× for transgender women:

| scenario | enrichment | q | μ₁ | Ω*/Ω | r* | crosses |
|---|---|---|---|---|---|---|
| PURPOSE 2 US, 1.0× | 1.0 | 0.63% | 0.010 | 0.9894 | 0.852 | **no** |
| PURPOSE 2 US, 2.0× | 2.0 | 1.25% | 0.010 | 0.9843 | 0.872 | **no** |
| PURPOSE 2 US, 3.0× | 3.0 | 1.88% | 0.015 | 0.9765 | 0.904 | **no** |
| PURPOSE 4 (comparison) | 9.6 | 5.22% | 0.040 | 0.9367 | 1.080 | yes |

---

# Appendix G — Anchor comparison and robustness

## G.1 Three independent routes to q

PWID, age 18+, μ₁ = 0.040:

| anchor | q | Ω*/Ω | r* | crosses |
|---|---|---|---|---|
| A. NHBS prevalence × BJS duration — low | 1.84% | 0.9639 | 0.959 | **no** |
| A. — mid | 3.70% | 0.9490 | 1.024 | yes |
| A. — high | 7.59% | 0.9175 | 1.171 | yes |
| B. Degenhardt/Bradley direct, national | 6.66% | 0.9251 | 1.135 | yes |
| B. lower CI | 5.15% | 0.9373 | 1.077 | yes |
| B. upper CI | 8.34% | 0.9114 | 1.201 | yes |
| C. BJS state × jail × enrichment, P4 sites | 5.22% | 0.9367 | 1.080 | yes |
| C. same, US-average states | 6.70% | 0.9247 | 1.136 | yes |

**7 of 8 variants cross. Break-even q = 3.02%.** Only the bottom of anchor A fails. Anchor B is entirely BJS-free, so the conclusion does not depend on the BJS anchor.

## G.2 Cross-validation

Two unrelated constructions agree to 0.04 percentage points:

- BJS route: 453/100k adult imprisonment × 1.54 jail multiplier × 9.6 enrichment = **6.70%**
- Degenhardt/Bradley: 246,500 incarcerated PWID ÷ 3.70M US PWID = **6.66%**

The jail multiplier is also directly validated: BJS jail (all adults) 253 + prison (18+) 453 = **706 per 100,000**, against 453 × 1.54 = 698 — accurate to 1%. The multiplier caveat is resolved.

## G.3 Age gradient in jail rates, and a double-counting trap

BJS *Jail Inmates in 2023*, Display 7 — adult jail incarceration rate per 100,000 US residents:

| age | rate |
|---|---|
| 18–24 | 332 |
| **25–34** | **480** |
| **35–44** | **426** |
| 45–54 | 235 |
| 55–64 | 107 |
| 65+ | 22 |
| all adults | 253 |

PWID sit at the peak. Age-standardising to a PWID structure (10/30/28/20/10/2%) gives **355 per 100,000, a 1.40× uplift** over the all-adult rate.

**Do not then multiply by the 9.6× enrichment.** Degenhardt's ratio is IDU prevalence among incarcerated versus general population, and part of that ratio exists *because* PWID occupy high-incarceration age bands. Age-standardising and then applying 9.6× double-counts:

| construction | q | r* | status |
|---|---|---|---|
| direct jail+prison × 9.6 (all-adult rates) | 6.78% | 1.139 | clean |
| Degenhardt/Bradley direct | 6.66% | 1.135 | clean, BJS-free |
| age-standardised × 9.6 | 7.75% | 1.177 | **double-counts age** |

**What the age data does license for PURPOSE 4:** the ≥18 frame captures every high-incarceration band — 18–24 (332) sits below 25–34 (480) and 35–44 (426), so the floor does not truncate the peak. A 16–25 frame would, which is a further reason PURPOSE 1's age criterion cannot be served by these data.

## G.4 μ′ remains non-influential

Sweeping in-custody mortality μ′ from 0.002 (BJS jail) to 0.100 moves r\* by 0.007. At q = 4–8% of person-time in state O, the death rate there has almost no leverage. μ′ can be fixed anywhere reasonable and needs no further sourcing.

## G.5 Limitations to state in the text

1. **State jail rates are not published** in the BJS national jail series, so the jail component applies the national jail:prison ratio (0.558) per state. States differ in jail-versus-prison mix, so **the ordering of q_s is more reliable than its level.** Vera's county-level data would resolve this and would also permit matching at county level (LA, San Diego, Miami-Dade, Baltimore City, Essex, Bronx, Philadelphia, Harris, Monongalia), which is the granularity the sites actually occupy.
2. **The 9.6× enrichment is North-America-wide, applied per state.** If enrichment correlates with incarceration rate, the between-state spread is understated.
3. **BJS imprisonment counts sentenced prisoners**, so pretrial detention enters only through the jail component.
4. **Degenhardt's numerator is "ever injected"** against Bradley's past-year denominator. Break-even fractions: LOW scenario fails below f = 0.44, MID below f = 0.26, HIGH crosses at any f.

## G.6 Why this construction is falsifiable

Every q_s is a published BJS rate times two stated constants, so any reader can recompute it. And it makes a **testable prediction**: if PURPOSE 4 reports screening-to-enrolment attrition by site, Newark and the Bronx should show the least observability loss and Houston the most. That is checkable against data the trial will generate.

It also survives the obvious attack. "You chose convenient parameters" does not hold when two of the trial's own eight states fall below the threshold and that is reported. The threefold spread in q across one trial's geography is a stronger claim than any single national figure.

---

# Appendix H — Can Wang-style reweighting absorb s(u)?

Tested rather than asserted. Earlier drafts of this record claimed baseline-covariate reweighting "cannot" recover removal-induced bias. That is too strong; the truth is sharper and more useful.

## H.1 Setup

Binary covariate X (e.g. housing instability) with stratum-specific removal hazard μ_x. Within stratum x the estimator carries `D_x = Ω*_x/Ω = ∫φ(u)e^{−μ_x u}du / ∫φ(u)du`, a duration integral.

| stratum | μ_x | λ_x | D_x |
|---|---|---|---|
| 0 | 0.010 | 0.020 | 0.9946 |
| 1 | 0.080 | 0.060 | 0.9580 |

## H.2 Result

| case | source g | target h | truth | naive | Wang-reweighted | bias removed |
|---|---|---|---|---|---|---|
| 1 — same X distribution | 50/50 | 50/50 | 0.04000 | 0.03868 (−3.29%) | **0.03868 (−3.29%)** | **0.0%** |
| 2 — target enriched, high-removal | 80/20 | 30/70 | 0.04800 | 0.02741 (−42.90%) | 0.04620 (−3.75%) | 91.3% |
| 3 — target enriched, low-removal | 30/70 | 80/20 | 0.02800 | 0.04620 (+65.01%) | 0.02741 (−2.11%) | 96.8% |

**Reweighting is highly effective at the composition component — 91–97% of the bias when the X distributions differ.** The residual 2–4% is the within-stratum duration bias and is irreducible:

```
lambda_hat_transported = SUM_x h(x) lambda_x D_x      vs      truth = SUM_x h(x) lambda_x
```

Since `D_x < 1` in every stratum with `μ_x > 0`, any weighted average of `D_x` is below 1. Reweighting helps only insofar as the target places weight on strata with less removal; it never repairs removal *within* a stratum.

## H.3 The corollary that matters for trials

In a counterfactual-placebo design the target **is** the trial population, drawn from the same screened pool. So `h = g` on the removal-relevant axis — Case 1 — and reweighting removes **exactly zero** of the bias.

**Correct framing for the paper:** not "Wang's method cannot do this," but *Wang's method solves a different problem well, and in the trial setting the two problems are orthogonal.* The mechanisms are **composable, not competing** — the generalised LEL carries `s(u)` and `r` simultaneously.

## H.4 Two precision notes on the three-way positioning

1. **Nesting condition.** Pan ⊂ Paper A requires `s(u) ≡ 1`, which given `s(u) = S₁(u)·e^{−ρu}` needs *both* `S₁ ≡ 1` and `ρ = 0`. Eligibility stability alone is insufficient: a stationary catchment with non-zero mortality still has `S₁ < 1`. State it as the pair — `ρ = 0` is the empirically defensible half, `S₁ ≡ 1` is the half that fails.
2. **Anti-collapse principle.** Do not merge incarceration, mortality, screening attendance, known-HIV avoidance and recent-testing exclusion into one "structural hazard." Keep Pan's staged notation: `s(u)` (population availability) → `Q` (attendance) → `C` (testing eligibility). This caught two double-counting errors in the course of this work — adding a prevalence to a rate (Appendix D.1), and age-standardising before applying an enrichment ratio that already contained the age effect (Appendix G.3). Make it an explicit design rule in the Methods.

---

# Appendix I — PURPOSE 4 county-level parameterization

Site-matched empirical inputs for the nine PURPOSE 4 US site counties. Sources: Vera Institute *Incarceration Trends* (county jail and prison populations), US Census Bureau Population Estimates Program vintage 2019 (county age structure), Degenhardt 2026 (IDU enrichment), ALIVE (mortality), NHBS (θ).

## I.1 Why 2019, and why it is not "conservative"

2019 is the last year with **harmonized county-level jail and prison estimates across all nine site counties**. It is treated as a **fixed pre-pandemic structural anchor**, not as an estimate of contemporaneous custody prevalence.

It must not be described as conservative — the data disprove that. Post-2019 jail trajectories are heterogeneous **in both magnitude and direction**:

| site county | jail 2019 | jail 2023 | k_jail |
|---|---|---|---|
| Bronx, NY | 2,090 | 968 | **0.463** |
| San Diego, CA | 6,285 | 4,372 | 0.696 |
| Los Angeles, CA | 16,892 | 12,952 | 0.767 |
| Harris (Houston), TX | 8,985 | 8,224 | 0.915 |
| Philadelphia, PA | 4,670 | 4,604 | 0.986 |
| Baltimore City, MD | 1,891 | 1,901 | 1.005 |
| Miami-Dade, FL | 4,184 | 4,278 | 1.022 |
| Monongalia, WV | 263 | 277 | 1.052 |
| Essex (Newark), NJ | 2,021 | 2,193 | 1.085 |

Four counties sit **at or above** 2019. Applying a single national multiplier would have been wrong in direction for those.

**Wording for the manuscript:** *We treated 2019 as a fixed pre-pandemic structural anchor because it was the last year with harmonized county-level jail and prison estimates across all study sites. Post-2019 jail trajectories were heterogeneous in both magnitude and direction; 2019 was therefore not assumed to be uniformly conservative. A secondary analysis updated the jail component using the most recent available local data while retaining the 2019 prison component, county-level post-2019 prison counts being unavailable.*

## I.2 County-specific age denominators

The national 15–64 → 18+ conversion (0.8333) was replaced with county-specific ratios from Census PEP 2019:

| site county | total | 15–64 | 18+ | 15–64 / 18+ |
|---|---|---|---|---|
| Miami-Dade, FL | 2,716,940 | 1,806,008 | 2,166,213 | 0.8337 |
| Baltimore City, MD | 593,490 | 405,255 | 471,012 | 0.8604 |
| San Diego, CA | 3,338,330 | 2,254,380 | 2,615,240 | 0.8620 |
| Philadelphia, PA | 1,584,064 | 1,071,468 | 1,236,037 | 0.8669 |
| Essex (Newark), NJ | 798,975 | 529,422 | 610,462 | 0.8672 |
| Los Angeles, CA | 10,039,107 | 6,843,765 | 7,887,008 | 0.8677 |
| Bronx, NY | 1,418,207 | 936,860 | 1,069,372 | 0.8761 |
| Monongalia, WV | 105,612 | 77,006 | 85,960 | 0.8958 |
| Harris (Houston), TX | 4,713,325 | 3,156,092 | 3,475,483 | 0.9081 |

Range 0.834–0.908 against the national 0.833. The national factor **systematically understated exposure** in counties with younger adult age structures, by up to 12.4% (Harris).

Age matching is now performed at the same geographic level as the incarceration exposure. The correction is applied to the **denominator**, not layered on top of the 9.6× enrichment — which would re-introduce the double-counting trap identified in Appendix G.3.

## I.3 Results, three layers

μ₁ = 0.040 (ALIVE, adult PWID), θ = 0.844 (NHBS), enrichment 9.6× (Degenhardt), sojourn 40 d, μ′ = 0.002.

| site county | q 2019 | r* 2019 | k_total | q 2023 | r* 2023 | break-even k | decline required |
|---|---|---|---|---|---|---|---|
| Bronx, NY | 4.49% | 1.053 | 0.776 | 3.48% | **1.017** | **0.67** | **33%** |
| Miami-Dade, FL | 4.85% | 1.066 | 1.008 | 4.89% | 1.068 | 0.62 | 38% |
| San Diego, CA | 5.49% | 1.090 | 0.872 | 4.79% | 1.064 | 0.55 | 45% |
| Monongalia, WV | 5.54% | 1.092 | 1.028 | 5.69% | 1.098 | 0.54 | 46% |
| Los Angeles, CA | 6.96% | 1.146 | 0.931 | 6.48% | 1.128 | 0.43 | 57% |
| Harris (Houston), TX | 8.35% | 1.201 | 0.975 | 8.13% | 1.193 | 0.36 | 64% |
| Essex (Newark), NJ | 8.44% | 1.205 | 1.032 | 8.71% | 1.216 | 0.36 | 64% |
| Philadelphia, PA | 12.49% | 1.377 | 0.996 | 12.44% | 1.374 | 0.24 | 76% |
| Baltimore City, MD | 14.52% | 1.470 | 1.001 | 14.54% | 1.471 | 0.21 | 79% |

- **Layer 1 — fixed 2019 anchor.** q_j from 4.49% to 14.52%; all nine above the boundary; median 6.96%.
- **Layer 2 — 2023 jail-updated.** Median 6.48%; crossing preserved at all nine **when prison is held at 2019**.
- **Layer 3 — prison-vintage sensitivity.** The Bronx alone is materially sensitive (§I.4).

Note that the refinement moved sites **in both directions** — k_total > 1 for Essex, Monongalia, Miami-Dade and Baltimore; < 1 for Bronx, San Diego, Los Angeles and Harris. Same formula, better local inputs, site-specific changes of either sign. This was not a one-directional tuning exercise.

## I.4 The Bronx: boundary-sensitive, and probably below

The Bronx jail population fell from 2,090 (2019) to 734 (2020), 968 (2023) and 1,031 (2024) — **k_jail ≈ 0.463**, far below the national trough of ≈0.74. Because jail was only **41.8%** of the county's 2019 custody population, holding prison fixed gives k_total = 0.776, above its break-even of 0.672, and r* = 1.017.

Vera's county prison series ends at 2019, so the prison component cannot be updated. Sensitivity:

| prison scenario | k_total | q | r* | crosses |
|---|---|---|---|---|
| held at 2019 | 0.776 | 3.48% | 1.017 | yes |
| −10% | 0.717 | 3.22% | 1.007 | yes |
| −15% | 0.688 | 3.09% | 1.003 | yes |
| **−25% (NY State decline)** | **0.630** | **2.83%** | **0.993** | **no** |
| −30% | 0.601 | 2.70% | 0.989 | no |

**The Bronx crosses iff its prison component retains ≥ 82.3% of its 2019 level — i.e. it is falsified by a prison decline exceeding 18%.** New York State's prison population fell approximately 25% over the same period, so the point estimate places the Bronx **below** the boundary, not merely near it.

Classification: **unresolved**, with the balance of evidence against crossing.

## I.5 The substantive claim

> Across the nine US PURPOSE 4 site counties, site-matched 2019 correctional exposure produced q_j from 4.49% to 14.52% and placed all nine above the zero-bias boundary. Updating the jail component through 2023 gave a median q_j of 6.48% and preserved the crossing at all nine sites when county prison populations were held at their last harmonized 2019 values. Eight sites were robust, requiring correctional-exposure declines of 38–79% to fall back below the boundary. The Bronx was the sole boundary-sensitive site: its 33% break-even decline is exceeded under a prison contraction of more than 18%, and New York State's prison population declined approximately 25% over the period. We therefore classify eight sites as robust and the Bronx as unresolved.

## I.6 Distance to falsification

The more informative statistic is not the binary crossing but the **fractional custody decline required to overturn it**, R_j = 1 − k_BE,j: Bronx 33%, Miami-Dade 38%, San Diego 45%, Monongalia 46%, Los Angeles 57%, Harris 64%, Essex 64%, Philadelphia 76%, Baltimore 79%.

The model therefore makes **both fragile and robust site-specific predictions**, which is methodologically stronger than universal invariance. The falsification statement is exact: *the site-specific prediction fails whenever true post-2019 correctional exposure falls below the derived break-even level.* For the Bronx that level is reachable on current evidence; for Baltimore it is not.

## I.7 Outstanding item

County-level prison populations after 2019 are the single missing input. Obtaining them for Bronx County — from NY DOCCS county-of-commitment data — would resolve the one unresolved site. Nothing else in the parameterization depends on data that are unavailable.

## I.8 Files

`p4_county.csv` (Vera extraction), `county_agedenom.csv` (Census PEP denominators), `p4_final.csv` (merged parameterization with break-even k).

---

# Appendix J — The exact cancellation theorem, and what it retracts

This appendix **supersedes the incarceration conclusions in Appendices A–I.** Two compounding errors were found, and correcting them reverses the empirical headline.

## J.1 Error 1 — jail's return rate applied to prison occupancy

For a transient state at fixed occupancy `q`, `α = β·q/(1−q)`. A long sojourn implies a *small* return rate and therefore a *small entry rate*: prison can hold substantial point prevalence because people stay years, not because many people enter during a two-year recency window. `S₁(u)` depends on the relaxation rate `α+β`, not on `q` alone — ≈12/yr for jail (32 d) but ≈0.39/yr for prison (2.7 y).

Appendices F–I applied a single 40-day sojourn to **combined** jail+prison occupancy, over-stating flow into custody roughly thirty-fold for the prison component.

At `q_total = 6%`:

| mix | S₁(2y) | Ω*/Ω | r* |
|---|---|---|---|
| all jail | 0.8714 | 0.9289 | 1.116 |
| 50/50 | 0.8822 | 0.9481 | 1.029 |
| all prison | 0.8932 | 0.9682 | 0.941 |
| **single-O, 40 d (as used in F–I)** | 0.8713 | 0.9304 | **1.109** |

The single-state model reproduced essentially the all-jail answer. Actual jail share at the PURPOSE 4 sites is 27–53% (median 38%).

Splitting into E, J, P, X states: **2019 crossing falls 9/9 → 7/9; jail-updated 2023 falls 9/9 → 5/9**; mean shift in r* is −0.150, largest at the most prison-dominant sites (Baltimore −0.327).

## J.2 Error 2 — the numerator assumed no acquisition in custody

The Appendix A–I numerator was

```
N_rec = INT lambda * n0_E(t-u) * S1(u) * phi(u) du
```

which starts **every** incident infection in state E. It therefore silently assumed `λ_J = λ_P = 0`. The general expression is

```
E[N_rec] = INT_0^T* phi(u) * n0(t-u)' * diag(lambda) * P1(u) * e_E du
         = INT phi(u) [ lam_E n_E P_EE(u) + lam_J n_J P_JE(u) + lam_P n_P P_PE(u) ] du
```

with `P₁(u) = exp(Q₁u)`. Defining `η_k = λ_k/λ_E`, the old `s(u) = S₁(u)e^{−ρu}` is the special case `η_J = η_P = 0`.

## J.3 The cancellation theorem

**Theorem.** Let living states E, J, P have stationary distribution **π** and transition matrix `P(u) = e^{Qu}`. If `λ_E = λ_J = λ_P = λ` and infection does not alter the movement process, then `π'P(u) = π'` for all u, so

```
E[N_rec] = lambda * pi' P(u) e_E integrated against phi = lambda * pi_E * Omega
```

and since the HIV-negative denominator at survey is proportional to `π_E`, **λ̂/λ = 1 exactly.**

Verified numerically: deviation **2.22 × 10⁻¹⁶**.

Stationarity suffices — detailed balance is *not* required. Use "transient/bidirectional movement," not "reversible."

| scenario | λ̂/λ_E |
|---|---|
| η = 1, no mortality, stationary | **1.000000** |
| mortality only (μ_E = 0.040), η = 1 | 0.9793 |
| η_J = η_P = 0 + mortality — **the old model** | 0.9442 |
| η_J = η_P = 2 | 1.0358 |

The loss from people infected in E and in custody at survey is **exactly offset** by people infected in custody who have returned to E.

## J.4 Consequence for PURPOSE 4

r* by site across the acquisition-hazard ratio (2019 custody mix, μ_E = 0.040, θ = 0.844):

| site county | q_J | q_P | η=0 | η=0.25 | η=0.50 | η=0.75 | η=1.0 | break-even η |
|---|---|---|---|---|---|---|---|---|
| Bronx, NY | 1.88% | 2.62% | 0.983 | 0.961 | 0.938 | 0.917 | 0.895 | never |
| Miami-Dade, FL | 1.85% | 3.00% | 0.986 | 0.962 | 0.940 | 0.917 | 0.895 | never |
| San Diego, CA | 2.31% | 3.18% | 1.004 | 0.976 | 0.948 | 0.921 | 0.895 | 0.04 |
| Los Angeles, CA | 2.06% | 4.90% | 1.010 | 0.980 | 0.951 | 0.922 | 0.894 | 0.08 |
| Monongalia, WV | 2.94% | 2.60% | 1.023 | 0.990 | 0.957 | 0.925 | 0.894 | 0.17 |
| Harris (Houston), TX | 2.48% | 5.86% | 1.035 | 0.999 | 0.963 | 0.928 | 0.894 | 0.24 |
| Essex (Newark), NJ | 3.18% | 5.26% | 1.057 | 1.014 | 0.973 | 0.933 | 0.894 | 0.34 |
| Philadelphia, PA | 3.63% | 8.86% | 1.112 | 1.054 | 0.998 | 0.945 | 0.893 | 0.49 |
| Baltimore City, MD | 3.85% | 10.67% | 1.143 | 1.076 | 1.012 | 0.951 | 0.892 | 0.55 |

**Sites crossing: 7/9 at η=0, 3/9 at η=0.25, 1/9 at η=0.50, 0/9 at η≥0.75.**

η = 0 is not defensible. Injection continues in custody at reduced intensity, sexual transmission occurs, and in-custody HIV transmission is documented. A plausible PWID range is roughly 0.1–0.5, which places most sites **below** the boundary.

**Retraction:** the claim that incarceration drives a threshold crossing at PURPOSE 4 sites does not survive. It was an artifact of the two errors above compounding.

## J.5 Frailty and recurrence sensitivity

Carceral contact is strongly recurrent, so constant-α Markov cycling treats non-exchangeable people as exchangeable. Two-class mixtures holding population-mean custody shares fixed at q_J = 3.0%, q_P = 5.0%:

| mixture | cancellation (η=1, μ=0) | η=0, μ=0.04 | η=1, μ=0.04 |
|---|---|---|---|
| homogeneous | 0.99996 | 0.9442 | 0.9793 |
| 20% class at 3× mean | 0.99996 | 0.9457 | 0.9792 |
| 10% class at 6× mean | 0.99997 | 0.9491 | 0.9792 |

1. **The cancellation is robust to frailty** — it holds per stratum, so any mixture of stationary strata inherits it.
2. Under η = 0 the magnitude depends mildly on the mixture, and concentrating custody person-time in a small class makes the apparent bias *smaller*.
3. Under mortality with η = 1, custody frailty is essentially irrelevant (0.9793 → 0.9792).

Markov cycling is therefore an empirical approximation whose relaxation does not manufacture or destroy the result.

## J.6 What survives, and the reframed paper

**Survives.** Mortality. `E → X` is absorbing with no return flow, so it cannot cancel: at μ_E = 0.040 the deflation is **2.1%**. The LEL threshold structure, the three-way analytic cross-check, the analytic-vs-Monte-Carlo agreement, the empirical φ work and the Wang comparison all stand — the generalized numerator was absorbed without modifying the framework.

**Does not survive.** Incarceration as a driver of threshold crossing.

**The central result is now a cancellation theorem, not an empirical correction:**

> Movement into and out of temporary unobservable states does not itself bias cross-sectional HIV incidence estimation in a stationary population when acquisition hazard and post-acquisition movement are state-invariant. Bias arises from violations of that symmetry: absorbing loss such as mortality, state-dependent acquisition (η ≠ 1), infection-dependent movement, and non-stationary composition.

This answers Reviewer 1 better than the original thesis did. Their concern — that eligibility dynamics act on positives and negatives alike — is now answered with an exact theorem rather than an argument that they overlooked a bias. And their question about what advance goes beyond what follows from the assumptions has a clean answer: **the paper identifies the exact conditions under which eligibility movement cancels, and the exact mechanisms that break it.**

Their magnitude scepticism was also correct, and should be conceded: under defensible rates the direct effect is ~2%, not the 8.9–27.3% originally claimed.

**Suggested restructure.** Main text: (1) general finite-state theorem; (2) exact cancellation corollary; (3) failure modes; (4) Pan composition, with Q and C applied *after* the population-state process; (5) empirical mortality illustration; (6) one incarceration sensitivity table showing the effect vanishing as η → 1. Everything else — jail/prison split, nine sites, county/state comparison, Bronx vintage, η sweep, empirical φ, Wang comparison, analytic/MC validation, BJS/Vera construction — goes to the supplement.

**Title.** The original "structural censoring biases…" thesis is no longer what the paper shows. Something closer to *When Eligibility Dynamics Bias Cross-Sectional HIV Incidence Estimation* keeps the finding slightly surprising: not all eligibility loss creates bias.

**Do not add more state-level PWID surveillance.** State IDU-attributed diagnoses and prevalence cannot identify `η_J` or `η_P`; that requires studies comparing acquisition rates during custody versus community person-time, which is a narrow and separate literature.

---

# Appendix K — Mortality threshold, η bounds, separated surface, frailty proof

## K.1 Mortality alone does not move the boundary

Pure absorbing mortality, `s(u) = e^{−μu}`, Pan AJE basis, θ = 0.844, c = 0.25 y:

| μ (/yr) | Ω_μ/Ω | r*_μ | crosses |
|---|---|---|---|
| 0.000 | 1.0000 | 0.810 | no |
| 0.020 | 0.9892 | 0.853 | no |
| **0.040 (sourced PWID)** | **0.9786** | **0.897** | **no** |
| 0.060 | 0.9682 | 0.942 | no |
| 0.085 | 0.9554 | 1.000 | — |
| 0.100 | 0.9479 | 1.035 | yes |

`r* = 1` at **μ_crit = 0.0852/yr** (8.2% annual loss). The sourced ALIVE range 0.037–0.045 gives r* = 0.890–0.908. **Mortality would have to be 2.1× the sourced rate to move the boundary.**

This distinction must be explicit in the paper:

> Mortality creates real, non-cancelling attenuation (≈2.1% at μ = 0.040). It does **not** follow that mortality alone forces the zero-bias boundary above 1 for every r ≤ 1. It does not.

Do not substitute "mortality drives the crossing" for the discarded "incarceration drives the crossing."

## K.2 η = 0 is empirically untenable, and prison η is plausibly very low

**Gough E, Kempf MC, Graham L, Manzanero M, Hook EW, Bartolucci A, Chamot E. HIV and hepatitis B and C incidence rates in US correctional populations and high risk groups: a systematic review and meta-analysis. *BMC Public Health* 2010;10:777.** doi:10.1186/1471-2458-10-777, PMID 21176146, PMC3016391. Thirty-six predominantly prospective cohort studies.

Pooled HIV incidence:

| population | per 100 PY |
|---|---|
| continuously incarcerated | 0.08 |
| IVDU recruited from treatment | 1.14 |
| street-recruited IVDU | 2.78 |
| released / re-incarcerated | 2.92 |

Crude cross-study ratios: **0.08/2.78 ≈ 0.029** and **0.08/1.14 ≈ 0.070**.

Also relevant: the Georgia prison investigation documented **88 known seroconversions during incarceration** (1988–2005), with 33 of 67 sequenced cases in 10 genetically related clusters and evidence of within-prison sexual transmission. So `η_P > 0` is established.

**What this licenses and what it does not.** These are heterogeneous historical studies, not matched PWID followed inside and outside custody, and "continuously incarcerated" is not synonymous with PWID. They establish that **a non-zero custodial acquisition hazard substantially below community PWID incidence is empirically plausible** — they do **not** identify a contemporary PURPOSE-4-specific η. Use as an overlay band, never as a fitted value.

The literature is informative about **prison** (continuous incarceration) and largely silent on **short jail episodes**. Do not collapse to a common η.

## K.3 Separated (η_J, η_P) surface

Full 5×5 surfaces per site are in the computation log. The decisive summary, at η_P = 0.05 (Gough-informed):

| site county | q_J | q_P | jail share | crosses iff |
|---|---|---|---|---|
| Baltimore City, MD | 3.85% | 10.67% | 27% | η_J < **0.83** |
| Philadelphia, PA | 3.63% | 8.86% | 29% | η_J < 0.72 |
| Essex (Newark), NJ | 3.18% | 5.26% | 38% | η_J < 0.43 |
| Harris (Houston), TX | 2.48% | 5.86% | 30% | η_J < 0.33 |
| Monongalia, WV | 2.94% | 2.60% | 53% | η_J < 0.19 |
| Los Angeles, CA | 2.06% | 4.90% | 30% | η_J < 0.10 |
| San Diego, CA | 2.31% | 3.18% | 42% | η_J < 0.03 |
| Bronx, NY | 1.88% | 2.62% | 42% | never |
| Miami-Dade, FL | 1.85% | 3.00% | 38% | never |

**η_J, not η_P, is the load-bearing parameter.** Because prison is quasi-absorbing over T* = 2 y (relaxation ≈0.39/yr), a low η_P leaves the prison channel largely intact as a bias source. Jail cycles fast (≈12/yr), so η_J governs whether the jail channel cancels. The literature constrains the parameter that matters *less*.

This is the correct final form of the empirical sensitivity: a two-dimensional surface with the `r* = 1` contour, one literature-informed band overlaid on the η_P axis, and no fitted point estimate.

## K.4 Frailty-mixture cancellation corollary — algebraic proof

**Corollary.** Let the population comprise latent strata z with weights w_z. Suppose within each stratum the movement process is stationary with distribution **π**_z and generator Q_z, and acquisition is state-invariant: λ_{E,z} = λ_{J,z} = λ_{P,z} = λ_z. Then the estimator is exactly unbiased for the observable-susceptible-weighted population incidence, for arbitrary mixing weights.

*Proof.* Stationarity within stratum z gives **π**_z′P_z(u) = **π**_z′ for all u. Hence

```
N_rec,z = INT phi(u) lambda_z pi_z' P_z(u) e_E du = lambda_z pi_{E,z} Omega
N_neg,z proportional to pi_{E,z}
```

Aggregating over strata,

```
lambda_hat = SUM_z w_z lambda_z pi_{E,z} Omega / ( SUM_z w_z pi_{E,z} * Omega )
           = SUM_z w_z pi_{E,z} lambda_z / SUM_z w_z pi_{E,z}
```

which is the **π_E-weighted mean of λ_z** — precisely incidence among observable susceptibles, since stratum z contributes observable susceptible person-time proportional to w_z π_{E,z}. Therefore λ̂ = λ_true. ∎

Numerical confirmation (Appendix J.5): 0.99996, 0.99996, 0.99997 across homogeneous, 20%-at-3×, and 10%-at-6× mixtures.

This forecloses the predictable objection that incarceration is concentrated in a high-recidivism subgroup and so a homogeneous Markov model is unrealistic. The answer: correct, and **arbitrary stationary mixtures preserve the cancellation.**

## K.5 What the paper should not try to prove

1. That incarceration produces a universal downward correction in PURPOSE 4 — it does not (Appendix J).
2. That empirically plausible mortality makes the estimator necessarily downward biased — it does not (K.1).
3. Any replacement empirical assertion of comparable ambition.

The defensible result is the symmetry statement:

> Eligibility movement is not inherently biasing. Bias is generated by specific violations of flow symmetry: absorbing exits, state-dependent acquisition (η ≠ 1), infection-dependent transitions, non-stationarity, and subsequent Pan-type screening and eligibility selection.

## K.6 Stopping point

Modelling is complete. Do not pursue state-level PWID HIV surveillance: state IDU-attributed diagnoses and prevalence cannot identify η_J or η_P, which would require studies comparing acquisition during custody versus community person-time — a narrow separate literature, of which Gough 2010 is the best available and is insufficient for a point estimate.

The main text can be almost purely mathematical. The empirical material serves only to show that the symmetry-breaking parameters occupy plausible ranges, not to make a new epidemiologic claim.
