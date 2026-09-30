# REPRODUCE.md

How to verify the theorems, regenerate every figure and table, and trace any number in the manuscript to the code that produced it.

> **Implementation status: complete.** `src/` and the `analysis/` entry points are
> implemented, and both remaining ports — the individual-level simulator and the
> empirical-$\varphi$ fit — are now in `src/` and under test. `make verify` runs **72 tests, 1 skipped**
> in ≈ 7 s; `make figures` regenerates every output that does not require external data.
> One test requires the CEPHIA CSV and skips cleanly without it.
>
> `analysis/prototypes/` has been **deleted**. It held five pre-freeze scripts that all
> embedded $\eta_k = 0$ outside $E$ and a single unobservable state; keeping superseded
> assumptions in the tree alongside the corrected ones invites exactly the error the paper
> is about. §7 records what each contributed. Their content is recoverable from git history
> and from `docs/audit/computation_record.md`.

---

## 1. Environment

```bash
git clone https://github.com/Nyx-Dynamics/nyx-eligibility-dynamics.git
cd nyx-eligibility-dynamics
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Python ≥ 3.10. Developed against numpy 2.x, scipy 1.14, statsmodels 0.14, scikit-learn 1.5.
No compiled extensions, no GPU, no network access required for the offline suite.

---

## 2. Verify the theorems

```bash
make verify          # or: pytest tests/ -v
```

This is the primary check and it tests **mathematical invariants, not manuscript
table values**. Tests requiring the CEPHIA dataset skip automatically when it is absent, so a
clone with no data still exercises every theorem.

| test | asserts | tolerance |
|---|---|---|
| `test_gao_bannick_recovery` | single state, no transitions ⇒ $w\equiv1$ ⇒ consistent | 1e-12 |
| `test_corollary_1_requires_demographic_stationarity` | growing pool is biased even with no transitions | — |
| `test_exact_cancellation` | (1)–(5) ⇒ $\hat\lambda/\lambda_E = 1$, across 9 occupancy × sojourn combinations | 1e-12 |
| `test_cancellation_is_phi_independent` | holds for gamma, CEPHIA and rectangular $\varphi$ | 1e-6 |
| `test_state_stationarity_alone_insufficient` | (1) without (2) is biased | — |
| `test_frailty_mixture_cancellation` | arbitrary stationary mixtures inherit cancellation | rel 1e-9 |
| `test_eta_zero_recovers_restricted_model` | general form at $\eta=0$ equals an **independently built** restricted model | 1e-12 |
| `test_absorbing_only_closed_form` | sole $E\to X$ ⇒ $w(u)=e^{-\mu u}$ | 1e-12 |
| `test_mu_crit_is_a_root` | $r^\star(\mu_{\mathrm{crit}}) = 1$ | 1e-6 |
| `test_pan_recovery` | $w\equiv1$ reproduces Pan Table 1, 9 cells | 0.05e-3 |
| `test_zero_bias_boundary_is_phi_free` | $r^\star = e^{-\theta c}$ for every $\varphi$ | 1e-8 |
| `test_matrix_exponential_matches_analytic` | 2- and 3-state closed forms vs `expm` | 1e-12 |
| `test_quadrature_matches_closed_form` | adaptive vs trapezoid | rel 1e-6 |
| `test_inert_exclusion_is_refused` | $K_w=0$ when $\varphi$ has no support beyond $c$ ⇒ no boundary exists | exact |
| `test_eta_above_one_inflates` | $\eta_k>1$ inverts the direction | — |
| `test_rho_handles_unreachable_state` | $\rho$ correct when an unobservable state is empty | 1e-6 |
| `test_dynamics_move_the_boundary_up` | absorbing loss raises $r^\star$ above $e^{-\theta c}$ | — |
| `test_gamma_params_match_xsrecency` | window 101 / shadow 194 ⇒ shape 0.352, rate 1.273 | 0.001 |
| `test_plim_rejects_mismatched_grid` | grid mismatch raises rather than broadcasting | — |
| `test_lel_general_reproduces_the_poisson_closed_form` | the general inter-test form collapses to `lel`, 12 combinations | 1e-9 |
| `test_boundary_closed_form_agrees_with_root_finding` | algebraic $r^\star$ vs `brentq` | 1e-6 |
| `test_uniform_inter_test_boundary_is_only_approximately_phi_free` | Poisson invariance exact; Uniform[0,b] spread ≤ 0.6% across 6 bases | see §5 |
| `test_uniform_boundary_is_not_the_denominator_inclusion` | $r^\star \ne P_0$ off the Poisson case | ≥ 0.04 gap |
| `test_uniform_inter_test_reduces_to_its_mean_gap_only_approximately` | mean-matched Poisson gives a different boundary | ≥ 0.05 gap |

### `tests/test_simulation.py` — analytic vs generative

`src/simulation.py` imports no analytic expression except `omega` (a quadrature of $\varphi$
that its own estimator needs), so these compare two independent routes rather than restating
one. Marked `slow`; excluded by `make verify-fast`.

| test | asserts | tolerance |
|---|---|---|
| `test_monte_carlo_matches_analytic` | simulated $\hat\lambda/\lambda_E$ vs Theorem 2, 7 cells: cancellation, absorbing at $\mu=0.04$ and $0.10$, $\eta=0$, $\eta=0.3$, $\eta=1.8$, $q_J=15\%$ | $\lvert t\rvert<4.44$, 12 reps × 1.5 M |
| `test_monte_carlo_matches_analytic_lel` | simulated LEL vs Pan closed form at $r \in \{0.3, 0.5, 0.809, 1.0, 1.6\}$; the zero crossing lands on $e^{-\theta c}$ without being told it | $\lvert t\rvert<4.44$ |
| `test_monte_carlo_matches_composed_lel` | dynamics **and** screening together — §2.7, not a special case of either module | $\lvert t\rvert<4.44$ |
| `test_cell_seeds_are_disjoint` | seed blocks are pairwise disjoint | exact |
| `test_phi_vanishes_outside_the_window` | $\varphi(u)=0$ for $u>T^*$, and the clamped alternative is materially non-zero | exact |
| `test_simulator_targets_lambda_E_not_total_incidence` | the $\sum_k\pi_k\eta_k$ conversion is present, and its omission is detectable | 3e-3 |
| `test_u_max_matches_pan_construction` | $U_{\max}=p/(\lambda(1-p))>T^*$ | 1e-12 |
| `test_simulator_refuses_impossible_population` | $\boldsymbol\pi\odot\boldsymbol\eta\equiv0$ raises | — |

### `tests/test_empirical_phi.py` — the recency fit

Three layers, so a clone with no external data still tests something real.

| test | asserts | needs data |
|---|---|---|
| `test_empirical_phi_recovers_a_known_curve` | logit-cubic GEE recovers a synthetic MDRI known in closed form, and $\varphi$ pointwise to 0.04 | no |
| `test_empirical_phi_clusters_do_not_move_the_point_estimate` | GEE-independence ≡ unclustered GLM in the point estimate | no |
| `test_unit_convention_is_years` | a days/years mix-up moves MDRI by orders of magnitude, not percent | no |
| `test_frozen_cephia_fixture_is_self_consistent` | frozen aggregates coherent; Pan's 163 d inside the subtype-C interval; raising the VL threshold shortens MDRI | fixture |
| `test_empirical_phi_tail_is_not_flat` | tail strictly declining to zero ⇒ Assumption B.1 violated | fixture |
| `test_cephia_phi_differs_materially_from_the_parametric_bases` | empirical MDRI ≥ 15 d from both gamma bases, so φ-independence is not tested on near-identical curves | fixture |
| `test_empirical_phi_matches_fixture` | full refit vs frozen values, all three algorithms | **CEPHIA CSV** |

**Expected runtime** ≈ 7 s for `make verify` (≈ 1 s for `make verify-fast`), ≈ 25 s for
`make figures`.

### The agreement gate is a *t* statistic, not a *z*

The replicate standard error is **estimated** from `N_REP` draws, so the studentised
statistic follows $t_{N_{\mathrm{rep}}-1}$, not a normal. At the original 6 replicates the
two-sided 0.999 critical value is $t_5 = 6.87$ against a normal 3.29 — so a $\lvert z\rvert<4$
gate was *tighter than the sampling distribution of its own denominator*, and would have failed
spuriously at a rate far above its nominal level.

This was found while building the CROI figure, where a 10-replicate block put the $\eta=0.3$
cell at $z = 3.27$. It is not a defect in either implementation:

| seed block | MC mean | sem | $z$ |
|---|---|---|---|
| A | 0.955392 | 0.000222 | +3.10 |
| B | 0.955149 | 0.000390 | +1.14 |
| C | 0.953704 | 0.000455 | −2.19 |
| D | 0.954633 | 0.000572 | −0.12 |
| E | 0.954873 | 0.000444 | +0.38 |
| **pooled, 50 reps** | **0.954750** | **0.000203** | **+0.23** |

Analytic value 0.954703. The estimated `sem` varies by a factor of 2.6 across blocks, which is
what drives the apparent outlier. The fix is more replicates (12 in the suite, 24 in the
figure) plus a $t$ critical value, not a looser gate. Increasing `nbin` was ruled out first:
the discrepancy was flat to three figures from 240 to 3840 bins, so it was never the
midpoint approximation in `_state_at_survey`.

### A note on the Monte Carlo test

It uses **independent seeds per parameter cell**. Sharing one simulated population across cells
is tempting — $\eta$ and $r$ enter as deterministic weights, so a single population would
suffice — but it makes residuals perfectly correlated, and an agreement test then degenerates
into a sign test on one realisation. This produced a spurious "systematic bias at $p = 2^{-27}$"
during development. Do not optimise it away; see `docs/PROVENANCE.md` §3 and the computation
record Appendix J.

---

## 3. Regenerate figures and tables

```bash
make figures         # everything not requiring external data
make figures-full    # everything, including CEPHIA-dependent outputs
```

| output | script | needs data | status |
|---|---|---|---|
| Fig. 1 — $s(u)$ by mechanism (absorbing / transient / mixed) | `analysis/validate_theorems.py` | no | ✅ |
| Fig. 2 — cancellation across occupancy and sojourn | `analysis/validate_theorems.py` | no | ✅ |
| Fig. 3 — $(\eta_J,\eta_P)$ surface with the $r^\star=1$ contour | `analysis/eta_surface.py` | no | ✅ |
| empirical vs parametric $\varphi$ — *not a manuscript figure* | `analysis/empirical_phi.py` | CEPHIA | ✅ |
| Table 1 — Pan recovery, 9 cells | `analysis/reproduce_pan.py` | no | ✅ |
| Table 2 — $\mu_{\mathrm{crit}}$ vs sourced mortality | `analysis/mortality_threshold.py` | no | ✅ |
| Table 3 — frailty mixtures | `analysis/frailty_mixture.py` | no | ✅ |
| CEPHIA MDRI by algorithm and subtype — *not a manuscript table* | `analysis/empirical_phi.py` | CEPHIA | ✅ |
| Table S2 — Wang reweighting comparison | `analysis/wang_comparator.py` | no | ✅ |
| Table S3 — site sensitivity, illustrative | `analysis/eta_surface.py --sites` | fixtures only | ✅ |
| Table S4 — inter-test process vs assay basis | `analysis/inter_test_process.py` | no | ✅ |
| `cephia_recomputed.json` — this run's MDRI vs the frozen claim | `analysis/empirical_phi.py` | CEPHIA | ✅ |

`analysis/empirical_phi.py` **compares** against `data/fixtures/cephia_expected.json` and
writes its own observation to `outputs/cephia_recomputed.json`. It does not overwrite the
fixture: the fixture is the frozen claim, and a script that rewrites its own expectation
turns the regression test into a tautology.

Everything in the manuscript runs with no external downloads. The two CEPHIA-dependent outputs
are **no longer numbered manuscript items**: they were cited in §3.2 as Figure S2 and Table S1
and were cut, because a numbered item that cannot be produced from a clean clone is worse than
no item. The script still produces them, and §3.2 still reports the MDRI they establish
(182.4 d, 95% CI 161–213); only the figure and table callouts are gone.

Manuscript numbering is fixed in `analysis/assemble_manuscript.py` and gated by
`make check-refs`, which exits non-zero if a numbered item is missing or uncited.

---

## 4. External data

None is redistributed. See `data/README.md` for retrieval; `data/fixtures/` holds small
aggregate derived files sufficient for the offline suite.

| source | needed for | identifier |
|---|---|---|
| CEPHIA public-use dataset | the empirical $\varphi$ fit and its MDRI table, neither now a numbered manuscript item | Zenodo 10.5281/zenodo.4900634 |
| Vera Incarceration Trends | illustrative site occupancy | `incarceration_trends_county.csv`, `main` |
| BJS Prisoners / Jail Inmates | custody rates and sojourn lengths | bjs.ojp.gov statistical-tables series |
| Census PEP vintage 2019 | county age denominators | `cc-est2019-alldata-<STATE>.csv` |

**Before committing anything CEPHIA-derived, check the dataset's redistribution terms.** The
intended fixture pattern is synthetic inputs with the real schema plus a frozen
`cephia_expected.json` holding only MDRI, CI bounds and reference curve points.

---

## 5. Key numbers and where they come from

Every quantitative claim in the manuscript resolves here, and every row is now ✅: reproduced
by the current implementation and recorded in `docs/audit/computation_record.md`. Two rows
changed value when they were ported, and both changes are improvements rather than
discrepancies — noted inline.

| claim | value | source | |
|---|---|---|---|
| Exact cancellation deviation | 2.22e-16 | Appendix J.3 | ✅ |
| Pan Table 1 reproduction | all 9 cells within 0.03e-3 | Appendix J / K.1 | ✅ |
| Analytic cross-check, 3 routes | agree to 5e-14 | Appendix J | ✅ |
| Monte Carlo agreement, census mode | 7 cells, all \|z\| < 4 against Theorem 2 | Appendix J | ✅ |
| Monte Carlo agreement, screening | 5 values of $r$ + 2 composed cells, all \|z\| < 4 | Appendix J | ✅ |
| Zero-bias boundary | $r^\star = e^{-\theta c}$, exact, φ-free | Appendix K.1 | ✅ |
| Boundary under uniform inter-test | ≤0.6% relative spread across bases | Appendix K / record §5 | ✅ |
| $P_0$ under Uniform[0,3] / [0,4] | 0.8403 / 0.8789 | record §5 | ✅ |
| Mortality attenuation at $\mu=0.040$ | $\Omega_\mu/\Omega = 0.9786$ | Appendix K.1 | ✅ |
| $\mu_{\mathrm{crit}}$ | 0.0852/yr, ≈2.1× sourced rate | Appendix K.1 | ✅ |
| CEPHIA MDRI, subtype C, VL>75 | 182.4 d (95% CI 161–213) | Appendix C / K.2 | ✅ |
| Frailty mixtures | 1.00000000 (record: 0.99996, coarser grid) | Appendix J.5 | ✅ |
| Wang reweighting residual | 0% removed when distributions coincide; 91–97% when they differ | Appendix H | ✅ |
| $\eta$ break-even by site | 0.04–0.55 | Appendix K.3 | ✅ |
| θ from NHBS 57% tested/12 mo | 0.844/yr (Poisson) | Appendix A.1 | ✅ |

**Two ported values changed, both for the better.**

*Boundary spread under uniform inter-test.* The record reports 0.6% (Uniform[0,3]) and 0.2%
(Uniform[0,4]); `analysis/inter_test_process.py` gives **0.37%** and **0.18%** over six gamma
bases spanning MDRI 94–251 d. The record's basis set included the two CEPHIA logit-GEE fits
and spanned a slightly wider MDRI range, so the numbers are not expected to coincide exactly.
The recorded figures are the conservative ones and the claim is stated as a ≤0.6% ceiling.

*Boundary spread under Poisson.* The record shows $r^\star$ ranging 0.7764–0.7780 at
$\theta=1$, a spread of 0.0016, while simultaneously calling the invariance exact. Both
cannot be true. The spread was `brentq` bracketing plus quadrature error in the prototype;
`r_star_general` is algebraic — the kept mass is affine in $r$ — and returns exactly
$e^{-\theta c} = 0.7788$ on every basis, spread 0.0. The theory was right and the prototype's
numerics were the weaker part.

If a number here disagrees with one in the predecessor repository, the predecessor is
superseded; `SUPERSEDED.md` there says why.

---

## 6. Provenance chain

Three layers, per `docs/PROVENANCE.md` §8:

1. **this document** — the command that regenerates each output;
2. **`docs/audit/computation_record.md`** — the 1,300-line post-review reanalysis log, appendix
   by appendix. The structural correction is Appendix J; parameter grounding A–C; site-level
   work F–I; mortality and $\eta$ in K;
3. **`tests/`** — theorem-level invariants, including regression guards for both development
   errors.

`docs/audit/repo_history_verification.txt` holds the verified git output behind the
repository-history claims in `PROVENANCE.md` — including the finding that the predecessor's
`master` branch is **not** a subset of its `main`.

---

## 7. What was ported from the prototypes

`analysis/prototypes/` has been deleted. It is recorded here because the audit record cites
those filenames, and because each port involved a substantive change rather than a move.

| prototype | what survived | what had to change |
|---|---|---|
| `derive_s.py` | 3-state $S_1(u)$ closed form; $\rho$ | generalised to arbitrary $\mathcal{L}$; $\eta_k$ added; returns $w_t = s_t \cdot g_E$ rather than $s$ → `eligibility_dynamics.historical_weight` |
| `lel_removal.py` | generalised LEL, Pan-validated | takes the weight function $w_t$ rather than a scalar $\gamma$ → `pan_composition.lel` |
| `lel_removal_cephia.py` | multi-basis $r^\star$ | `phi_uniform` renamed `rectangular_phi` — it is an assay basis, not an inter-test process; the inter-test process became a separate object → `pan_composition.UniformInterTest` |
| `mc_removal.py` | simulator to Pan §S.5 | acquisition admitted in **all** living states; normalisation corrected from total incidence to $\lambda_E$; independent seed blocks per cell → `simulation.py` |
| `xcheck_xsrecency.py` | CEPHIA logit-GEE MDRI | fixture comparison inverted so the script no longer rewrites its own expectation → `analysis/empirical_phi.py` |

All five assumed $\eta_k = 0$ outside $E$ and a single unobservable state. That assumption is
what the paper's central correction removes, so keeping them in the tree next to the corrected
code was a live hazard, not a convenience. Recover them from git history if needed.

Three bugs were found *by* the port rather than carried through it:

1. **$\varphi(u)$ clamped above the window.** `np.interp` returns the endpoint value outside
   the grid, so $\varphi(u)$ returned $\varphi(T^*) \approx 0.038$ instead of $0$ for
   $u > T^*$. The simulator draws durations to $U_{\max} = 3.62$ y, so this inflated every
   simulated recent count by 13–22% — which read as a systematic analytic/Monte Carlo
   disagreement. Guarded by `test_phi_vanishes_outside_the_window`.
2. **Simulator normalised to total incidence, not $\lambda_E$.** Total infection flow is
   $N_{\text{neg}}\lambda_E\sum_k \pi_k\eta_k$, so the generative $\lambda$ must be divided
   by $\sum_k\pi_k\eta_k$ to recover the estimand. Without it, every departure from
   $\eta \equiv 1$ appeared as disagreement with Theorem 2 — by exactly that factor.
   Guarded by `test_simulator_targets_lambda_E_not_total_incidence`.
3. **`empirical_phi.py` overwrote its own expectation.** It wrote `cephia_expected.json` on
   every run, so the regression test could never fail. It now compares and writes
   `outputs/cephia_recomputed.json` instead.

Only the first two would have changed a published number; the third would have silently
removed a check.

## 8. If a test fails

| symptom | likely cause |
|---|---|
| `test_exact_cancellation` fails at 1e-12 but passes at 1e-6 | quadrature grid too coarse, or $\boldsymbol\pi$ not exactly stationary for the constructed $Q$ |
| `test_pan_recovery` off by more than 0.05e-3 | wrong $\varphi$ basis — Pan's arXiv table uses window 101 d / shadow 194 d ⇒ shape 0.352, rate 1.273 |
| `test_monte_carlo_matches_analytic` shows one-signed residuals | seeds are being shared across cells; see §2. `test_cell_seeds_are_disjoint` should have caught it first |
| Monte Carlo runs high by 10–20% in every cell | $\varphi$ is being evaluated past $T^*$ and clamped rather than zeroed; see §7 |
| Monte Carlo agrees at $\eta=1$ but not otherwise | the $\sum_k\pi_k\eta_k$ conversion to $\lambda_E$ is missing; the ratio of MC to analytic *is* that sum |
| `test_uniform_inter_test_boundary_is_only_approximately_phi_free` fails marginally | grid too coarse — this test uses `default_grid(4001)`, not the 1201-point suite grid |
| `test_empirical_phi_matches_fixture` drifts | first confirm the fixture was not overwritten by a run of `analysis/empirical_phi.py`; it should never write there. Then check the unit convention. `XSRecency::createRitaCephia` changed its contract between tag 0.2.0 (days) and `main` (years); the shipped vignette double-converts against `main` |
| everything CEPHIA-related skips | expected without the dataset; see `data/README.md` |
