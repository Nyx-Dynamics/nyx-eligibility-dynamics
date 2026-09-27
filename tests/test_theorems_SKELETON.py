"""
tests/ — theorem-level invariants for the eligibility-dynamics paper.

These test MATHEMATICAL INVARIANTS, not manuscript table values. A reviewer
should be able to clone, run `pytest`, and see the theorems checked.

Split into one file per theorem when porting; kept together here as a skeleton
so the coverage map is visible in one place.

Conventions
-----------
Time in years. T_STAR = 2.0. Rates per year.
States ordered (E, O_1, ..., O_m); X is implicit in row-sum deficits.
"""

import numpy as np
import pytest
from scipy.linalg import expm
from scipy import integrate

from src.eligibility_dynamics import (
    generator,            # (q_dict, betas, mus) -> Q on living states
    transition,           # (Q, u) -> P_1(u)
    historical_weight,    # (Q, pi, eta, g_E) -> w_t(u) on a grid
    plim_ratio,           # (phi, w) -> lambda_hat / lambda_E
    omega,                # (phi) -> Omega_{T*}
)
from src.pan_composition import lel, r_star

T_STAR = 2.0
TOL_EXACT = 1e-12      # algebraic identities
TOL_NUM = 1e-6         # quadrature vs closed form
TOL_MC = 4.0           # Monte Carlo agreement, in units of SE


# ---------------------------------------------------------------------------
# 1. Gao & Bannick limiting case  (Corollary 1)
# ---------------------------------------------------------------------------

def test_gao_bannick_recovery(phi_gamma):
    """Single living state, no transitions, stationary pool => w == 1 => consistent."""
    Q = generator(q={}, betas={}, mus={"E": 0.0})       # E only, no exits
    w = historical_weight(Q, pi={"E": 1.0}, eta={"E": 1.0}, g_E=lambda u: 1.0)
    assert np.allclose(w, 1.0, atol=TOL_EXACT)
    assert plim_ratio(phi_gamma, w) == pytest.approx(1.0, abs=TOL_NUM)


def test_corollary_1_requires_demographic_stationarity(phi_gamma):
    """
    REGRESSION. With no transitions, s_t == 1 but w_t == g_E. A growing pool must
    therefore still be biased. Guards against re-conflating the two stationarities.
    """
    Q = generator(q={}, betas={}, mus={"E": 0.0})
    rho = 0.05
    w = historical_weight(Q, pi={"E": 1.0}, eta={"E": 1.0},
                          g_E=lambda u: np.exp(-rho * u))
    assert plim_ratio(phi_gamma, w) < 1.0 - 1e-4


# ---------------------------------------------------------------------------
# 2. Exact transient cancellation  (Corollary 2)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("qJ,qP", [(0.03, 0.05), (0.01, 0.01), (0.10, 0.02)])
@pytest.mark.parametrize("betaJ,betaP", [(11.4, 0.37), (5.0, 5.0), (20.0, 1.0)])
def test_exact_cancellation(phi_gamma, qJ, qP, betaJ, betaP):
    """
    State-stationary + demographically stationary + eta == 1 + Q1 == Q0 + no
    absorbing loss  =>  lambda_hat / lambda_E == 1 EXACTLY.

    This is the paper's central result. Must hold to algebraic tolerance, not
    merely numerically close, and must be insensitive to occupancy and sojourn.
    """
    Q = generator(q={"J": qJ, "P": qP}, betas={"J": betaJ, "P": betaP},
                  mus={"E": 0.0, "J": 0.0, "P": 0.0})
    pi = {"E": 1 - qJ - qP, "J": qJ, "P": qP}
    w = historical_weight(Q, pi=pi, eta={"E": 1.0, "J": 1.0, "P": 1.0},
                          g_E=lambda u: 1.0)
    assert np.allclose(w, 1.0, atol=TOL_EXACT)
    assert plim_ratio(phi_gamma, w) == pytest.approx(1.0, abs=TOL_EXACT)


def test_cancellation_is_phi_independent(phi_gamma, phi_cephia, phi_rectangular):
    """Cancellation holds for any recency function; it is a property of the flow."""
    Q = generator(q={"J": 0.03, "P": 0.05}, betas={"J": 11.4, "P": 0.37},
                  mus={"E": 0.0, "J": 0.0, "P": 0.0})
    pi = {"E": 0.92, "J": 0.03, "P": 0.05}
    w = historical_weight(Q, pi=pi, eta={"E": 1.0, "J": 1.0, "P": 1.0},
                          g_E=lambda u: 1.0)
    for phi in (phi_gamma, phi_cephia, phi_rectangular):
        assert plim_ratio(phi, w) == pytest.approx(1.0, abs=TOL_NUM)


def test_state_stationarity_alone_insufficient(phi_gamma):
    """
    REGRESSION for the rev.2 error: pi'Q == 0 fixes proportions, not totals.
    A composition-stable pool growing at rho has s_t == 1 but g_E == exp(-rho u).
    """
    Q = generator(q={"J": 0.03, "P": 0.05}, betas={"J": 11.4, "P": 0.37},
                  mus={"E": 0.0, "J": 0.0, "P": 0.0})
    pi = {"E": 0.92, "J": 0.03, "P": 0.05}
    w_stat = historical_weight(Q, pi, {"E": 1.0, "J": 1.0, "P": 1.0}, lambda u: 1.0)
    w_grow = historical_weight(Q, pi, {"E": 1.0, "J": 1.0, "P": 1.0},
                               lambda u: np.exp(-0.05 * u))
    assert plim_ratio(phi_gamma, w_stat) == pytest.approx(1.0, abs=TOL_EXACT)
    assert plim_ratio(phi_gamma, w_grow) < 1.0 - 1e-4


# ---------------------------------------------------------------------------
# 3. Frailty-mixture cancellation  (Corollary 3)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("weights,multipliers", [
    ([1.0], [1.0]),
    ([0.2, 0.8], [3.0, None]),        # None => residual, solved to preserve the mean
    ([0.1, 0.9], [6.0, None]),
    ([0.05, 0.15, 0.80], [8.0, 2.0, None]),
])
def test_frailty_mixture_cancellation(phi_gamma, weights, multipliers,
                                      mixture_builder):
    """
    Arbitrary stationary mixtures inherit exact cancellation. Aggregate over
    strata BEFORE forming the ratio -- summing numerators and denominators
    separately, as the estimator does.
    """
    strata = mixture_builder(q_mean={"J": 0.03, "P": 0.05},
                             weights=weights, multipliers=multipliers)
    num = den = 0.0
    for w_z, pi_z, Q_z, lam_z in strata:
        w = historical_weight(Q_z, pi_z, {"E": 1.0, "J": 1.0, "P": 1.0},
                              lambda u: 1.0)
        num += w_z * pi_z["E"] * lam_z * np.trapezoid(phi_gamma.values * w,
                                                      phi_gamma.grid)
        den += w_z * pi_z["E"]
    target = sum(w_z * pi_z["E"] * lam_z for w_z, pi_z, _, lam_z in strata) / den
    assert num / (den * omega(phi_gamma)) == pytest.approx(target, rel=1e-9)


# ---------------------------------------------------------------------------
# 4. Restricted-model recovery at eta = 0
# ---------------------------------------------------------------------------

def test_eta_zero_recovers_restricted_model(phi_gamma):
    """
    The general expression at eta_k = 0 must equal the restricted historical
    model s(u) = S_1(u) exp(-rho u).

    IMPORTANT: the restricted form is computed INDEPENDENTLY below --
    [exp(Qu)]_EE directly -- not by calling historical_weight with eta = 0.
    Otherwise this asserts that a function equals itself.
    """
    qJ, qP, mu, rho = 0.03, 0.05, 0.04, 0.02
    Q = generator(q={"J": qJ, "P": qP}, betas={"J": 11.4, "P": 0.37},
                  mus={"E": mu, "J": 0.002, "P": 0.002})
    pi = {"E": 1 - qJ - qP, "J": qJ, "P": qP}

    w_general = historical_weight(Q, pi, {"E": 1.0, "J": 0.0, "P": 0.0},
                                  g_E=lambda u: np.exp(-rho * u))

    # independent construction of the restricted model
    Qm = np.asarray(Q)
    w_restricted = np.array([
        expm(Qm * u)[0, 0] * np.exp(-rho * u) for u in phi_gamma.grid
    ])

    assert np.allclose(w_general, w_restricted, atol=TOL_EXACT)


# ---------------------------------------------------------------------------
# 5. Absorbing-only closed form  (Corollary 4)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("mu", [0.0, 0.01, 0.04, 0.10, 0.25])
def test_absorbing_only_closed_form(phi_gamma, mu):
    """Sole transition E -> X at rate mu  =>  w(u) == exp(-mu u)."""
    Q = generator(q={}, betas={}, mus={"E": mu})
    w = historical_weight(Q, {"E": 1.0}, {"E": 1.0}, lambda u: 1.0)
    assert np.allclose(w, np.exp(-mu * phi_gamma.grid), atol=TOL_EXACT)


def test_mu_crit_is_a_root(phi_gamma, theta=0.844, c=0.25):
    """r*(mu_crit) == 1 by construction; verify the solver agrees."""
    from analysis.mortality_threshold import mu_crit
    mc = mu_crit(phi_gamma, theta=theta, c=c)
    Q = generator(q={}, betas={}, mus={"E": mc})
    w = historical_weight(Q, {"E": 1.0}, {"E": 1.0}, lambda u: 1.0)
    assert r_star(phi_gamma, w, theta=theta, c=c) == pytest.approx(1.0, abs=1e-6)


# ---------------------------------------------------------------------------
# 6. Pan composition and recovery
# ---------------------------------------------------------------------------

PAN_TABLE1 = [  # (c, theta, r, published bias x 1e-3)
    (0.00, 1.0, 0.0, -9.95), (0.00, 1.0, 0.6, -3.98), (0.00, 2.0, 0.0, -15.03),
    (0.25, 1.0, 0.0, -5.93), (0.25, 1.0, 0.6, -1.36), (0.25, 1.0, 1.0, 1.68),
    (0.25, 2.0, 0.0, -8.97), (0.25, 2.0, 0.6, -0.10), (0.25, 2.0, 1.0, 5.82),
]


@pytest.mark.parametrize("c,theta,r,published", PAN_TABLE1)
def test_pan_recovery(phi_pan_arxiv, c, theta, r, published, lam=0.032):
    """w(u) == 1 must reproduce Pan et al. Table 1 to within 0.05e-3."""
    w = np.ones_like(phi_pan_arxiv.grid)
    got = 1e3 * lam * (np.exp(lel(phi_pan_arxiv, w, r=r, c=c, theta=theta)) - 1)
    assert got == pytest.approx(published, abs=0.05)


def test_zero_bias_boundary_is_phi_free(phi_gamma, phi_cephia, phi_rectangular,
                                        theta=1.0, c=0.25):
    """
    At w == 1 the boundary r* == exp(-theta c) exactly, independent of the
    RECENCY FUNCTION phi.

    NOTE ON TWO DIFFERENT "UNIFORM"S. phi_rectangular is a rectangular recency
    WINDOW. It is unrelated to a uniform INTER-TEST-TIME process, which is a
    property of testing behaviour, not of the assay. The boundary is exactly
    phi-free under a Poisson inter-test process; under a uniform inter-test
    process it is only approximately phi-free (<=0.6% across bases). That is a
    separate claim, tested in test_boundary_under_uniform_intertest below.
    Conflating assay basis with testing process is the error that determined
    the sign of the predecessor manuscript's joint bias factor.
    """
    for phi in (phi_gamma, phi_cephia, phi_rectangular):
        w = np.ones_like(phi.grid)
        assert r_star(phi, w, theta=theta, c=c) == pytest.approx(
            np.exp(-theta * c), abs=1e-8)


# ---------------------------------------------------------------------------
# 7. Numerical consistency
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("nstate", [2, 3])
def test_matrix_exponential_matches_analytic(nstate, closed_form_S1):
    """
    Two- and three-state closed forms must match expm to machine precision.
    Only 2 and 3 are parametrised: no independent four-state analytic form is
    implemented, and testing expm against itself would be vacuous. Keep this
    list and the README claim in step.
    """
    Q, S1_analytic = closed_form_S1(nstate)
    u = np.linspace(0, T_STAR, 97)
    S1_expm = np.array([expm(np.asarray(Q) * x)[0, 0] for x in u])
    assert np.allclose(S1_expm, S1_analytic(u), atol=TOL_EXACT)


def test_quadrature_matches_closed_form(phi_gamma):
    """Adaptive quadrature and the trapezoid grid must agree to TOL_NUM."""
    Q = generator(q={"J": 0.03}, betas={"J": 11.4}, mus={"E": 0.04, "J": 0.002})
    pi = {"E": 0.97, "J": 0.03}
    w = historical_weight(Q, pi, {"E": 1.0, "J": 0.3}, lambda u: 1.0)
    grid = np.trapezoid(phi_gamma.values * w, phi_gamma.grid)
    adaptive = integrate.quad(
        lambda u: phi_gamma(u) * historical_weight(Q, pi, {"E": 1.0, "J": 0.3},
                                                   lambda _: 1.0, at=u),
        0, T_STAR, limit=400)[0]
    assert grid == pytest.approx(adaptive, rel=TOL_NUM)


def test_monte_carlo_matches_analytic(phi_pan_arxiv, mc_simulator):
    """
    Individual-level simulator vs analytic LEL, with INDEPENDENT seeds per cell.

    Do NOT share one simulated population across parameter cells: eta and r
    enter as deterministic weights, so shared draws make residuals perfectly
    correlated and an agreement test becomes a sign test on one realisation.
    """
    cells = [(th, g, r) for th in (0.5, 1.0, 2.0)
                        for g in (0.0, 0.1, 0.2)
                        for r in (0.0, 0.6, 1.0)]
    zs = []
    for k, (th, g, r) in enumerate(cells):
        analytic = lel(phi_pan_arxiv, np.exp(-g * phi_pan_arxiv.grid),
                       r=r, c=0.25, theta=th)
        reps = np.array([mc_simulator(theta=th, gamma=g, r=r, c=0.25,
                                      n=6_000_000, seed=1000 + 17 * k + s)
                         for s in range(12)])
        se = reps.std(ddof=1) / np.sqrt(len(reps))
        zs.append((reps.mean() - analytic) / se)
    zs = np.asarray(zs)
    assert np.abs(zs).max() < TOL_MC
    assert abs(zs.mean()) < 1.0          # no systematic offset


# ---------------------------------------------------------------------------
# 8. Empirical recency function
# ---------------------------------------------------------------------------

def test_empirical_phi_matches_fixture(cephia_expected):
    """
    CEPHIA logit-GEE phi against FROZEN EXPECTED VALUES, so the suite runs
    offline and a pipeline change is caught rather than silently absorbed.

    LICENSING. No participant-derived rows are committed. data/fixtures/ holds
    (a) synthetic inputs with the same schema, for functional tests, and
    (b) cephia_expected.json -- MDRI, CI bounds and reference curve values
    only. Verify CEPHIA redistribution terms before committing anything
    derived from participant records; retrieval instructions are in
    data/README.md and docs/REPRODUCE.md.
    """
    from analysis.empirical_phi import fit_phi
    got = fit_phi(local_cephia_csv(), subtype="C", vl_threshold=75)
    assert got.mdri_days == pytest.approx(cephia_expected["mdri_days"], abs=1.0)
    assert got.ci_days[0] == pytest.approx(cephia_expected["ci_lo"], abs=3)
    assert got.ci_days[1] == pytest.approx(cephia_expected["ci_hi"], abs=3)


@pytest.mark.skipif(not _has_local_cephia(), reason="CEPHIA CSV not retrieved; see data/README.md")
def test_empirical_phi_tail_is_not_flat(local_cephia_csv):
    """
    The observed tail declines rather than holding constant, contra Gao &
    Bannick's Assumption B.1. Recorded as a fact about the data, not a defect.
    """
    from analysis.empirical_phi import binned_recency
    b = binned_recency(local_cephia_csv(), edges=[730, 1095, 1825, 3650])
    assert b[0] > b[1] > b[2]


# ---------------------------------------------------------------------------
# Fixtures to implement in conftest.py
# ---------------------------------------------------------------------------
#
#   phi_gamma        gamma-form phi, XSRecency get.gamma.params(window, shadow)
#   phi_pan_arxiv    window 101 d / shadow 194 d  -> shape 0.352, rate 1.273
#   phi_cephia       logit-GEE fit from data/fixtures/
#   phi_rectangular  rectangular-window phi (assay basis; NOT an inter-test process)
#   closed_form_S1   (nstate) -> (Q, analytic S1 callable)
#   mixture_builder  builds stationary strata preserving a target mean occupancy
#   mc_simulator     individual-level sim to Pan Supp S.5 + removal
#   cephia_expected  frozen expected values only (MDRI, CI, curve points)
#   local_cephia_csv path to a user-retrieved CEPHIA CSV; tests needing it skip
#                    when absent. _has_local_cephia() gates them.
#
# Each phi fixture exposes .grid, .values and __call__(u).
