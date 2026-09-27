# REPRODUCE.md

How to verify the theorems, regenerate every figure and table, and trace any number in the manuscript to the code that produced it.

> **Implementation status.** This document describes the target interface. `src/` and the
> `analysis/` entry points are **not yet written** — the repository currently holds the frozen
> theory, the provenance and audit record, the test skeleton, and pre-freeze prototypes under
> `analysis/prototypes/`. Rows below are marked ⬜ pending or ✅ available. Nothing marked ⬜
> will run today.
>
> Prototypes reproduce most numbers already but **embed superseded assumptions** — all five
> assume $\eta_k = 0$ outside $E$ and a single unobservable state. Use them for reference, not
> for verification. See `analysis/prototypes/README.md`.

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

⬜ *pending.* This is the primary check and it tests **mathematical invariants, not manuscript
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
| `test_monte_carlo_matches_analytic` | individual-level simulator vs analytic LEL, 27 cells × 12 replicates | max \|z\| < 4 |
| `test_empirical_phi_matches_fixture` | CEPHIA MDRI vs frozen expected values | ±1 d |

**Expected runtime** ≈ 4 min offline; the Monte Carlo test dominates (27 cells × 12 replicates
× 6M individuals). `pytest -m "not slow"` skips it.

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
| Fig. 1 — $s(u)$ by mechanism (absorbing / transient / mixed) | `analysis/validate_theorems.py` | no | ⬜ |
| Fig. 2 — cancellation across occupancy and sojourn | `analysis/validate_theorems.py` | no | ⬜ |
| Fig. 3 — $(\eta_J,\eta_P)$ surface with the $r^\star=1$ contour | `analysis/eta_surface.py` | no | ⬜ |
| Fig. 4 — empirical vs parametric $\varphi$ | `analysis/empirical_phi.py` | CEPHIA | ⬜ |
| Table 1 — Pan recovery, 9 cells | `analysis/reproduce_pan.py` | no | ⬜ |
| Table 2 — $\mu_{\mathrm{crit}}$ vs sourced mortality | `analysis/mortality_threshold.py` | no | ⬜ |
| Table 3 — frailty mixtures | `analysis/frailty_mixture.py` | no | ⬜ |
| Table S1 — CEPHIA MDRI by algorithm and subtype | `analysis/empirical_phi.py` | CEPHIA | ⬜ |
| Table S2 — Wang reweighting comparison | `analysis/wang_comparator.py` | no | ⬜ |
| Table S3 — site sensitivity, illustrative | `analysis/eta_surface.py --sites` | fixtures only | ⬜ |

Everything except Figure 4 and Table S1 runs with no external downloads.

---

## 4. External data

None is redistributed. See `data/README.md` for retrieval; `data/fixtures/` holds small
aggregate derived files sufficient for the offline suite.

| source | needed for | identifier |
|---|---|---|
| CEPHIA public-use dataset | empirical $\varphi$, Fig. 4, Table S1 | Zenodo 10.5281/zenodo.4900634 |
| Vera Incarceration Trends | illustrative site occupancy | `incarceration_trends_county.csv`, `main` |
| BJS Prisoners / Jail Inmates | custody rates and sojourn lengths | bjs.ojp.gov statistical-tables series |
| Census PEP vintage 2019 | county age denominators | `cc-est2019-alldata-<STATE>.csv` |

**Before committing anything CEPHIA-derived, check the dataset's redistribution terms.** The
intended fixture pattern is synthetic inputs with the real schema plus a frozen
`cephia_expected.json` holding only MDRI, CI bounds and reference curve points.

---

## 5. Key numbers and where they come from

Every quantitative claim in the manuscript resolves here. ✅ marks values already computed and
recorded in `docs/audit/computation_record.md`; ⬜ marks values that will be regenerated by
`src/` once written.

| claim | value | source | |
|---|---|---|---|
| Exact cancellation deviation | 2.22e-16 | Appendix J.3 | ✅ |
| Pan Table 1 reproduction | all 9 cells within 0.03e-3 | Appendix J / K.1 | ✅ |
| Analytic cross-check, 3 routes | agree to 5e-14 | Appendix J | ✅ |
| Monte Carlo agreement | mean z = −0.16, sd 1.29, 15/27 negative | Appendix J | ✅ |
| Zero-bias boundary | $r^\star = e^{-\theta c}$, exact, φ-free | Appendix K.1 | ✅ |
| Boundary under uniform inter-test | approximate, ≤0.6% across bases | Appendix K | ✅ |
| Mortality attenuation at $\mu=0.040$ | $\Omega_\mu/\Omega = 0.9786$ | Appendix K.1 | ✅ |
| $\mu_{\mathrm{crit}}$ | 0.0852/yr, ≈2.1× sourced rate | Appendix K.1 | ✅ |
| CEPHIA MDRI, subtype C, VL>75 | 182.4 d (95% CI 161–213) | Appendix C / K.2 | ✅ |
| Frailty mixtures | 0.99996, 0.99996, 0.99997 | Appendix J.5 | ✅ |
| Wang reweighting residual | 0% removed when distributions coincide; 91–97% when they differ | Appendix H | ✅ |
| $\eta$ break-even by site | 0.04–0.55 | Appendix K.3 | ✅ |
| θ from NHBS 57% tested/12 mo | 0.844/yr (Poisson) | Appendix A.1 | ✅ |

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

## 7. Porting from the prototypes

When writing `src/`, these must be rewritten rather than copied:

| prototype | survives | must change |
|---|---|---|
| `derive_s.py` | 3-state $S_1(u)$ closed form; $\rho$ | generalise to arbitrary $\mathcal{L}$; add $\eta_k$; return $w_t$ not $s$ |
| `lel_removal.py` | generalised LEL, Pan-validated | take $w_t$ rather than a scalar $\gamma$ |
| `lel_removal_cephia.py` | multi-basis $r^\star$ | rename `phi_uniform` → `phi_rectangular` (it is an assay basis, not an inter-test process) |
| `mc_removal.py` | simulator to Pan §S.5 | admit acquisition in all living states; keep independent seeds |
| `xcheck_xsrecency.py` | CEPHIA logit-GEE MDRI | no change needed beyond packaging |

All five assume $\eta_k = 0$ outside $E$ and a single unobservable state. Delete
`analysis/prototypes/` once `src/` is complete.

---

## 8. If a test fails

| symptom | likely cause |
|---|---|
| `test_exact_cancellation` fails at 1e-12 but passes at 1e-6 | quadrature grid too coarse, or $\boldsymbol\pi$ not exactly stationary for the constructed $Q$ |
| `test_pan_recovery` off by more than 0.05e-3 | wrong $\varphi$ basis — Pan's arXiv table uses window 101 d / shadow 194 d ⇒ shape 0.352, rate 1.273 |
| `test_monte_carlo_matches_analytic` shows one-signed residuals | seeds are being shared across cells; see §2 |
| `test_empirical_phi_matches_fixture` drifts | check the unit convention. `XSRecency::createRitaCephia` changed its contract between tag 0.2.0 (days) and `main` (years); the shipped vignette double-converts against `main` |
| everything CEPHIA-related skips | expected without the dataset; see `data/README.md` |
