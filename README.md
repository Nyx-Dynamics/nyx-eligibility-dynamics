# Eligibility dynamics in cross-sectional HIV incidence estimation

Reproducibility package for the methods paper *When eligibility dynamics bias cross-sectional HIV incidence estimation*.

---

## The result

Cross-sectional HIV incidence estimation from recency assays is often assumed to be biased whenever individuals are lost from the screening-eligible population — through death, incarceration, displacement, or disengagement. This is not generally true, and the conditions under which it is false are sharp.

**Theorem (exact cancellation).** Let living states be $\mathcal{L}=\{E,O_1,\dots,O_m\}$ with $E$ observable, plus an absorbing state $X$. If

1. the movement process is state-stationary, $\boldsymbol\pi^{\!\top}Q=\mathbf{0}^{\!\top}$;
2. the observable susceptible pool is demographically stationary;
3. acquisition is state-invariant, $\eta_k \equiv 1$;
4. movement is infection-independent, $Q_1=Q_0$;
5. there is no absorbing loss,

then the adjusted estimator is **exactly consistent**: $\hat\lambda \to \lambda_E$. Movement into and out of temporarily unobservable states does not, by itself, bias the estimator — the loss of individuals infected while observable and unobservable at survey is offset exactly by individuals infected while unobservable who have returned by survey.

The result survives arbitrary unobserved heterogeneity in movement propensity: any mixture of stationary strata inherits the cancellation, and the marginal movement process need not be Markov.

**Bias therefore requires a specific violation of flow symmetry.** Four mechanisms break it within the transition model:

| | mechanism | direction |
|---|---|---|
| **M1** | absorbing loss ($X \nrightarrow E$, no return flow) | attenuation |
| **M2** | state-dependent acquisition, $\eta_k \neq 1$ | attenuation if $\eta_k<1$; inflation if $\eta_k>1$ |
| **M3** | infection-dependent movement, $Q_1 \neq Q_0$ | sign depends on which transitions differ |
| **M4** | non-stationarity — demographic ($g_E\neq1$) or compositional ($\boldsymbol\pi$ drifting) | scalar growth signs deterministically; drift does not |

M1 is the only mechanism that cannot in principle be offset, because death admits no return flow. At empirically sourced rates its magnitude is modest: ≈2.1% attenuation at $\mu_E = 0.040$/yr, and moving the zero-bias boundary above unity would require $\mu \approx 0.085$/yr, roughly twice sourced rates.

## Composition with screening-stage selection

The transition process operates **upstream** of the selection mechanisms of Pan, Bannick & Gao (*Am J Epidemiol* 2026):

```
population at t−u  ──P₁(u)──▶  observable source at t  ──Q──▶  screened  ──C──▶  survey
        └──────── historical weight w_t(u) ────────┘
```

Substituting the full historical weight into their limiting estimation error moves the zero-bias boundary from $r^\star = e^{-\theta c}$ to $r^\star_w = e^{-\theta c}\big[1+(\Omega_{T^*}-\Omega_w)/K_w\big]$. Setting $w_t\equiv1$ recovers their expression exactly. Their boundary is independent of the recency function — exactly so under a Poisson testing
process, and only approximately under a uniform inter-test process, where $r^\star$ also
stops equalling $\Pr(S>c)$. `analysis/inter_test_process.py` computes the difference rather
than asserting it, because conflating an assay recency basis with an inter-test process is
the error that set the predecessor manuscript's sign.

## Reproduction

```bash
pip install -r requirements.txt
make verify       # theorem-level test suite
make verify-fast  # the same, skipping the Monte Carlo cells
make figures      # figures and tables into outputs/
```

`make verify` tests mathematical invariants rather than manuscript table values:

```
$ make verify
72 passed, 1 skipped in 6.7s
```

Covering: Gao–Bannick recovery; exact transient cancellation across nine occupancy ×
sojourn combinations; φ-independence of the cancellation; frailty-mixture cancellation
over four stratifications; restricted-model recovery at η = 0 against an *independent*
implementation; absorbing-only closed form; μ_crit as a root; Pan Table 1 recovery on all
nine published cells; φ-freeness of the zero-bias boundary, exact under Poisson and
approximate under a uniform inter-test process; matrix exponential against two- and
three-state analytic forms; quadrature against the trapezoid grid; recovery of a known
recency curve by the empirical fit; and regression guards for every error made during
development.

The Monte Carlo cells compare Theorem 2 and the composed limiting estimation error against
an **independently written generative simulator** — `src/simulation.py` imports no analytic
expression — over seven population scenarios and seven screening configurations. The one
skipped test needs the CEPHIA dataset, which is not redistributed.

## Layout

```
manuscript/     manuscript.tex, supplement.tex
src/            eligibility_dynamics.py, pan_composition.py, simulation.py
analysis/       reproduce_pan.py, validate_theorems.py, mortality_threshold.py,
                eta_surface.py, frailty_mixture.py, empirical_phi.py,
                wang_comparator.py, inter_test_process.py
tests/          test_theorems.py, test_simulation.py, test_empirical_phi.py
data/           README.md + fixtures/ — no bundled surveillance data
docs/           ESTIMAND.md, ASSUMPTIONS.md, REPRODUCE.md, PROVENANCE.md
outputs/        figures/, tables/
```

**Start with [`docs/ESTIMAND.md`](docs/ESTIMAND.md)** if you are arriving from the predecessor repository. What $\lambda$ denotes changed, and everything else follows from that.

## Empirical illustration

The empirical sections demonstrate that the symmetry-breaking parameters occupy plausible ranges. They do not make an independent epidemiologic claim.

- **Recency function.** $\varphi(u)$ estimated from the CEPHIA public-use dataset (Zenodo [4900634](https://doi.org/10.5281/zenodo.4900634)) by logit-GEE clustered on participant, following the `XSRecency` procedure. Subtype C, LAg-Sedia ODn ≤ 1.5 with VL > 75: MDRI 182.4 d (95% CI 161–213).
- **Absorbing loss.** $\mu_E$ from published PWID cohort mortality; $\mu_{\mathrm{crit}}$ reported against it.
- **State-dependent acquisition.** A two-dimensional $(\eta_J,\eta_P)$ sensitivity surface with the $r^\star=1$ contour. Literature-informed ranges are *overlaid, not fitted*; jail and prison are parameterised separately because sojourn length enters independently of occupancy.

Data are not redistributed. `data/README.md` gives retrieval instructions; `data/fixtures/` holds small derived files sufficient to run the test suite offline.

## Provenance

This work supersedes the analysis in [`nyx-kassanjee-letter`](https://github.com/Nyx-Dynamics/nyx-kassanjee-letter) (manuscript QAIV24714, submitted to JAIDS May 2026, declined; Zenodo [10.5281/zenodo.20344293](https://doi.org/10.5281/zenodo.20344293), tag `v9.0`). That analysis derived the recent-infection count under the implicit assumption that no acquisition occurs in temporarily unobservable states, and separately applied a jail-length return rate to prison occupancy. Its central empirical conclusions are not carried forward. See that repository's `SUPERSEDED.md`, and `docs/PROVENANCE.md` here, for the technical account.

The predecessor DOI is not superseded in place; this package receives its own, and the two are cross-linked.

## Citation

See `CITATION.cff`.

## License

MIT, for everything in this repository — see [`LICENSE`](LICENSE). A single
licence is deliberate: the theory, the implementation and the manuscript source
here are one artifact and splitting them would only create ambiguity about which
terms govern a derived figure.

The Zenodo deposition of the derived dataset carries its own CC licence, stated
in the deposition record rather than here. No third-party data are redistributed
in this repository; retrieval instructions and the upstream terms are in
[`data/README.md`](data/README.md).
