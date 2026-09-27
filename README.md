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

Substituting the full historical weight into their limiting estimation error moves the zero-bias boundary from $r^\star = e^{-\theta c}$ to $r^\star_w = e^{-\theta c}\big[1+(\Omega_{T^*}-\Omega_w)/K_w\big]$. Setting $w_t\equiv1$ recovers their expression exactly. Their boundary is independent of the recency function — exact under a Poisson testing process.

## Reproduction

```bash
pip install -r requirements.txt
make verify      # theorem-level test suite
make figures     # figures and tables into outputs/
```

`make verify` tests mathematical invariants rather than manuscript table values:

```
PASS  Gao–Bannick limiting case                 w(u) ≡ 1, single state
PASS  Pan LEL recovery                          w(u) ≡ 1, vs published Table 1
PASS  exact transient cancellation              η = 1, μ = 0, stationary
PASS  frailty-mixture cancellation              arbitrary stationary strata
PASS  restricted-model recovery at η = 0        vs independent implementation
PASS  absorbing-only closed form                s(u) = exp(−μu)
PASS  matrix exponential == analytic solution   two-state and three-state
PASS  quadrature == closed form                 adaptive vs trapezoid
PASS  Monte Carlo == analytic expectation       individual-level simulator
PASS  empirical φ implementation                vs CEPHIA reference fixture
```

## Layout

```
manuscript/     manuscript.tex, supplement.tex
src/            eligibility_dynamics.py, pan_composition.py
analysis/       reproduce_pan.py, validate_theorems.py, mortality_threshold.py,
                eta_surface.py, frailty_mixture.py, empirical_phi.py, wang_comparator.py
tests/          theorem-level invariants (see above)
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

Code MIT; manuscript text CC-BY-4.0.
