# PROVENANCE.md

How this paper came to exist, why there is more than one repository, and how to trace any claim back to the computation that produced it.

This is the **chronological** record. For the mathematics of what was wrong with the predecessor analysis, see [`SUPERSEDED.md`](https://github.com/Nyx-Dynamics/nyx-kassanjee-letter/blob/main/SUPERSEDED.md) in the archive repository. This document records the sequence, the decision points, and what triggered each change.

---

## 1. Lineage

```
manuscript QAIV24714
"Calibration-to-Deployment Mismatch in HIV Prevention Trials:
 How Structural Censoring Biases Counterfactual Incidence Estimates"
        |
        |  submitted JAIDS 2026-05-22        repo: nyx-kassanjee-letter
        |  declined after external review    tags: v9.0 (Zenodo), v10.0 (submission)
        |                                    DOI:  10.5281/zenodo.20344293
        v
post-review audit, Sept 2026
        |
        |  two errors found, one structural
        |  central claim withdrawn
        |  reviewers' requested split becomes necessary rather than optional
        |
        +-----------------------------+
        |                             |
        v                             v
PAPER A (this repository)      PAPER B (not yet created)
eligibility dynamics,          AIDSVu longitudinal surveillance,
theory + proofs + validation   geographic redistribution of PWID burden
new DOI on submission          decision pending — see §6
```

## 2. The original paper, and what the reviewers said

QAIV24714 argued that competing-risk removal from the screening pool — mortality, incarceration, displacement — deflates the effective mean duration of recent infection, producing 8.9–27.3% denominator inflation across 34 US metropolitan areas, and that the 90-day no-prior-testing eligibility criterion *structurally guaranteed* this bias.

Two reviewers. Their objections, in the order they turned out to matter:

**Reviewer 1** — "the testing behavior bias applies to both the recently infected and the negative participants, not just those with infection." This was the deepest objection in either report and it was correct. It is answered in this paper by Theorem 1, which carries the transition process through both the numerator and the HIV-negative denominator, and by Corollary 2, which shows the two can cancel exactly.

Reviewer 1 also challenged the practical magnitude, asked for assumptions to be stated rather than derived, disputed the claim that Phase 3 PrEP trials "routinely" apply a testing exclusion, and questioned using US late-diagnosis data for largely non-US trial populations. All four were sustained.

**Reviewer 2** — asked for the manuscript to be split into a methods paper and a surveillance paper; for precise notation, estimands, populations and proofs; for internal and external validity to be separated; and for engagement with three named papers (PMIDs 34984710, 40779330, 38803064).

Those three citations turned out to matter more than a reading list. They are Gao & Bannick 2022, Wang/Duerr/Gao 2025, and Bannick et al. 2024 — and following them led to a fourth, Pan/Bannick/Gao 2026, which is prior art on the submitted manuscript's §3.

## 3. What the audit found, in order

Each finding is recorded with what triggered it, because the triggers are part of the evidence.

| # | Finding | Triggered by |
|---|---|---|
| 1 | The joint bias factor's direction was carried by an **unfitted retention curve**, not by censoring. Structural censoring alone moves it the *opposite* way: at fixed retention, raising the hazard from Jackson's to Hartford's value takes it from 0.9995 to **1.0709**. | Decomposing the published table by substituting one input at a time |
| 2 | The screening-side factor used a **uniform-window basis** while the mean-duration correction used an **exponential basis**. The internally consistent choice inverts the sign across the entire empirical range. The submitted supplement §S2.3 already said so. | Reading the supplement against the main text |
| 3 | The submitted variance propagation gives a **95% interval containing unity** ([0.932, 1.051]) one sentence before asserting the point estimate is "robustly distinguishable from unity." | Recomputing §S1.4 |
| 4 | Gao & Bannick's **Assumption C** is the formal slot the mechanism belongs in — and they state it as approximate and hold it fixed throughout their own simulations. | Reading Reviewer 2's first citation |
| 5 | **Pan, Bannick & Gao (*AJE* 2026)** formalise the testing-based exclusion, derive its limiting estimation error, and find the sign *indeterminate* in exactly the submitted manuscript's regime. Published 6 April 2026; arXiv 16 December 2024; submission 22 May 2026. | Following the Gao-group citations |
| 6 | Whether removal biases the estimator **depends on how the susceptible pool is replenished** — a demographic assumption the submitted manuscript never stated. | Reviewer 1's first objection, taken seriously |
| 7 | Deriving the observability function from population dynamics rather than positing it gives $s(u) = S_1(u)e^{-\rho u}$, with $\rho$ the growth rate of the observable susceptible pool. In a stationary catchment $\rho = 0$ and susceptible mortality does **not** offset infected mortality. | Working #6 through a three-state model |
| 8 | Analytic and individual-level Monte Carlo agree across 27 parameter cells; the analytic side cross-checks three independent ways to $5\times10^{-14}$. | Falsification test, run before further empirical work |
| 9 | A **jail-length return rate had been applied to combined jail-and-prison occupancy**, overstating flow into custody roughly thirtyfold for the prison component. Splitting the states reduced threshold crossing from 9/9 to 5/9 of trial site counties. | External critique of the empirical mapping |
| 10 | The recent-infection count **assumed no acquisition occurs while unobservable** ($\eta_k = 0$) — the most extreme assumption available, in the direction that inflates the bias, and invisible because the single-state formulation had no parameter to express it. | External critique of the in-out flow |
| 11 | **Exact cancellation.** Generalising the numerator to admit acquisition in all living states gives $\hat\lambda/\lambda_E = 1$ to $2.2\times10^{-16}$ under stationarity, state-invariant acquisition and infection-independent movement. **This withdraws the central empirical claim and becomes the paper's principal result.** | #10 |
| 12 | Cancellation is **robust to unobserved heterogeneity**: it holds per stratum, so arbitrary stationary mixtures inherit it, and the marginal movement process need not be Markov. | Anticipating the recidivism objection |
| 13 | **Mortality alone does not move the boundary either.** It gives real attenuation (≈2.1% at $\mu = 0.040$/yr) but $\mu_{\mathrm{crit}} \approx 0.085$/yr — about twice sourced PWID rates. | Refusing to substitute a new headline for the withdrawn one |
| 14 | $\eta = 0$ is **empirically untenable**: Gough et al. 2010 report 0.08 vs 1.14–2.78 per 100 person-years, non-zero and well below community rates. Threshold crossing falls from 7/9 sites at $\eta = 0$ to 0/9 at $\eta \ge 0.75$. | Targeted search for bounds on the one load-bearing unmeasured parameter |

Findings 9 and 10 arrived as external critique of work already believed complete. Both were correct. Finding 10 in particular reversed the paper's conclusion, and finding 11 replaced it with a stronger one.

## 4. Why the split happened

Reviewer 2 asked for it. The claim reversal made it necessary.

The submitted manuscript contained a derivation, a 34-MSA empirical application, a decade-long surveillance panel, a COVID counterfactual, a Markov decision process invariance test, and a lenacapavir resistance argument — in 7,400 words. That is why the plain-language summary could not be aligned with the manuscript, which was Reviewer 2's stated complaint.

After finding 11, a single paper became incoherent rather than merely overloaded. The surveillance material had been framed as *empirical validation of the structural-functions claim* that the cancellation result overturns. Carrying it forward in the same paper would mean presenting evidence for a claim no longer made.

The split therefore falls along a line the mathematics draws rather than one chosen for length:

- **Paper A** — what the theory now proves: eligibility movement is not inherently biasing, and bias requires a specific violation of flow symmetry. All-new code.
- **Paper B** — what the surveillance data actually show, stripped of the superseded framing: where US PWID HIV burden moved over 2014–2023 and why aggregate metrics miss it. Existing code, requiring reframing rather than inheritance.

## 5. Why three repositories rather than one renovated in place

The predecessor repository carries **Zenodo DOI 10.5281/zenodo.20344293** at tag `v9.0`, cited in the submitted manuscript. It must stay resolvable and byte-identical. It cannot be repurposed, rewritten, or force-pushed.

Renovating it into Paper A was considered and rejected. Its `README` advertises the old thesis as current, `reproduce_v9.py` exists to reproduce the declined manuscript, and its commit history argues for a conclusion the successor reverses. A repository whose own log contradicts its contents is worse than two repositories with an explicit pointer between them.

So:

| repository | role |
|---|---|
| `nyx-kassanjee-letter` | historical archive. Untouched except a supersession banner and `SUPERSEDED.md`. `v10.0` is the frozen submission state; `v9.0` carries the DOI. |
| this repository | Paper A. Starts from the corrected theory, ports only surviving code, tests theorems rather than table values. New DOI on submission. |
| Paper B repository | not yet created. See §6. |

Obsolete material was deliberately **not** copied into a `legacy/` directory here. Git preserves the predecessor's history and the DOI preserves its archived state; importing 24 MB of superseded surveillance work would make this repository look like a cleaned-up omnibus paper rather than the focused methods paper it is.

**A note on the predecessor's branch structure**, which is confusing on arrival and contains a trap. It holds two unrelated commit histories: `main` (125 files, root `a1e8921`) is authoritative and carries the releases; `master` and `repo-cleanup-v5` (40 files, root `0ed361a`, last touched April 2026) are an abandoned v5-era line with **no common ancestor** with `main`. The DOI attaches to `v9.0` on `main` and to no other branch, so port analysis code from `main` at `v10.0`.

The trap: `master` is **not** a subset of `main`. Twenty-five files exist on `master` and nowhere on `main`, because `main` was begun from a fresh root rather than branched. Among them are `.zenodo.json`, the manuscript bibliography `Demidont_KassanjeeBias_references.bib`, both dual-licence files, and several data artifacts including `data/purpose_4.json`, `data/purpose_2_full.json`, `LEN_implementation.json` and `PrEP4U_sameday_start.json`. Anyone reconstructing the full historical record, or looking for the bibliography, must consult both lines. Verified output is recorded in the computation record.

## 6. Paper B is not yet committed to

Its empirical content was largely framed as supporting the structural-functions claim. Stripped of that, it is a descriptive account of geographic redistribution in US PWID HIV burden — publishable, but a thinner and different paper than the one the AIDSVu work was built for. That judgement should be made before a repository exists for it, not after.

Until then the material remains reachable at `nyx-kassanjee-letter` tag `v10.0`.

## 7. What moved here, and what did not

**Ported** — the general transition implementation; the generalised recent-count identity; the historical weight $w_t(u)$; Gao–Bannick recovery; the cancellation and frailty tests; the absorbing-mortality calculation and $\mu_{\mathrm{crit}}$; the separated $(\eta_J,\eta_P)$ surface; Pan recovery and the generalised limiting error; the CEPHIA empirical recency function; analytic, quadrature and Monte Carlo cross-checks; the Wang comparator.

**Not ported** — the AIDSVu 2013–2023 workbooks; the late-diagnosis parameterisation of the hazard; the 34-MSA correction table; the COVID deficit analysis; the EHE break-point test; the Van Handel county overlay; the MDP invariance test; the joint bias factor; the original manuscript and supplement; and every figure supporting a claim no longer made.

Where code was ported it was **rewritten against the corrected theory** rather than copied. The predecessor's scripts were built around a single-state observability function and a hazard parameterisation that no longer appear.

## 8. Tracing a claim

Every quantitative statement in the manuscript resolves through three layers:

1. **`docs/REPRODUCE.md`** — the command that regenerates each figure and table.
2. **The computation record** — a 1,300-line audit log covering the full post-review reanalysis, appendix by appendix: the structural correction is Appendix J, the parameter grounding A–C, the site-level work F–I, the mortality and $\eta$ analysis K. Each numbered finding in §3 above maps to an appendix.
3. **`tests/`** — theorem-level invariants, including regression tests that specifically guard the two errors made during development (conflating state with demographic stationarity; and validating the restricted model against an independent implementation rather than against itself).

If a number in the manuscript disagrees with one in the predecessor repository, the predecessor is superseded and `SUPERSEDED.md` says why.

## 9. On keeping this record

The original thesis was tested thoroughly enough to be shown wrong, and the error was interesting: it turned on whether a numerator admits acquisition in states from which people later return. Two of the three most consequential findings arrived as external critique of work believed finished, and both were correct.

That sequence is worth preserving rather than tidying. A reader who wants to know whether the current result is trustworthy is better served by seeing what was wrong and how it surfaced than by a repository that appears to have contained only claims that held up.
