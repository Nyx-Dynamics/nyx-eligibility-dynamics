"""
Theorem-level invariants. These test MATHEMATICS, not manuscript table values.

Three tests are regression guards for errors actually made during development;
they are marked REGRESSION and should not be removed.
"""
import numpy as np
import pytest
from scipy import integrate
from scipy.linalg import expm

from src.eligibility_dynamics import (
    generator, historical_weight, plim_ratio, omega, S1_closed, rho_susceptible,
    gamma_phi,
)
from src.pan_composition import lel, r_star, boundary_no_dynamics

TOL_EXACT = 1e-10
TOL_NUM = 1e-6
BJ, BP = 365.25 / 32.0, 1.0 / 2.7
E1 = {"E": 1.0, "J": 1.0, "P": 1.0}
E0 = {"E": 1.0, "J": 0.0, "P": 0.0}
NOMU = {"E": 0.0, "J": 0.0, "P": 0.0}


def _w(phi, q, betas, mus, eta, g_E=None):
    Q = generator(q=q, betas=betas, mus=mus)
    pi = {"E": 1.0 - sum(q.values()), **q}
    return historical_weight(Q, pi=pi, eta=eta, g_E=g_E, grid=phi.grid)


# --- 1. Gao-Bannick recovery (Corollary 1) --------------------------------

def test_gao_bannick_recovery(phi_gamma):
    w = _w(phi_gamma, {}, {}, {"E": 0.0}, {"E": 1.0})
    assert np.allclose(w, 1.0, atol=TOL_EXACT)
    assert plim_ratio(phi_gamma, w) == pytest.approx(1.0, abs=TOL_NUM)


def test_corollary_1_requires_demographic_stationarity(phi_gamma):
    """REGRESSION. No transitions gives s_t == 1, so w_t == g_E. A growing
    susceptible pool must still be biased."""
    w = _w(phi_gamma, {}, {}, {"E": 0.0}, {"E": 1.0},
           g_E=lambda u: np.exp(-0.05 * u))
    assert plim_ratio(phi_gamma, w) < 1.0 - 1e-4


# --- 2. Exact cancellation (Corollary 2) ----------------------------------

@pytest.mark.parametrize("qJ,qP", [(0.03, 0.05), (0.01, 0.01), (0.10, 0.02)])
@pytest.mark.parametrize("bJ,bP", [(BJ, BP), (5.0, 5.0), (20.0, 1.0)])
def test_exact_cancellation(phi_gamma, qJ, qP, bJ, bP):
    """The paper's central result. Must hold to algebraic tolerance and be
    insensitive to occupancy and sojourn length."""
    w = _w(phi_gamma, {"J": qJ, "P": qP}, {"J": bJ, "P": bP}, NOMU, E1)
    assert np.allclose(w, 1.0, atol=TOL_EXACT)
    assert plim_ratio(phi_gamma, w) == pytest.approx(1.0, abs=TOL_EXACT)


def test_cancellation_is_phi_independent(phi_gamma, phi_cephia, phi_rectangular):
    for phi in (phi_gamma, phi_cephia, phi_rectangular):
        w = _w(phi, {"J": 0.03, "P": 0.05}, {"J": BJ, "P": BP}, NOMU, E1)
        assert plim_ratio(phi, w) == pytest.approx(1.0, abs=TOL_NUM)


def test_state_stationarity_alone_insufficient(phi_gamma):
    """REGRESSION for the rev.2 proof error: pi'Q == 0 fixes proportions, not
    totals. Both stationarity conditions are required."""
    q, b = {"J": 0.03, "P": 0.05}, {"J": BJ, "P": BP}
    w_stat = _w(phi_gamma, q, b, NOMU, E1)
    w_grow = _w(phi_gamma, q, b, NOMU, E1, g_E=lambda u: np.exp(-0.05 * u))
    assert plim_ratio(phi_gamma, w_stat) == pytest.approx(1.0, abs=TOL_EXACT)
    assert plim_ratio(phi_gamma, w_grow) < 1.0 - 1e-4


def test_eta_above_one_inflates(phi_gamma):
    """eta_k > 1 is admitted and inverts the direction, which is why the
    boundary condition is stated via Omega_w, not pointwise w < 1."""
    w = _w(phi_gamma, {"J": 0.03, "P": 0.05}, {"J": BJ, "P": BP}, NOMU,
           {"E": 1.0, "J": 2.0, "P": 2.0})
    assert plim_ratio(phi_gamma, w) > 1.0 + 1e-4


# --- 3. Frailty mixture (Corollary 3) ------------------------------------

@pytest.mark.parametrize("weights,mult", [
    ([1.0], [1.0]),
    ([0.2, 0.8], [3.0, None]),
    ([0.1, 0.9], [6.0, None]),
    ([0.05, 0.15, 0.80], [8.0, 2.0, None]),
])
def test_frailty_mixture_cancellation(phi_gamma, weights, mult, mixture_builder):
    """Aggregate numerators and denominators separately, as the estimator does."""
    strata = mixture_builder({"J": 0.03, "P": 0.05}, weights, mult)
    num = den = 0.0
    for wz, pi, Q, lam in strata:
        w = historical_weight(Q, pi=pi, eta=E1, grid=phi_gamma.grid)
        num += wz * pi["E"] * lam * np.trapezoid(phi_gamma.values * w, phi_gamma.grid)
        den += wz * pi["E"]
    target = sum(wz * pi["E"] * lam for wz, pi, _, lam in strata) / den
    assert num / (den * omega(phi_gamma)) == pytest.approx(target, rel=1e-8)


# --- 4. Restricted-model recovery at eta = 0 -----------------------------

def test_eta_zero_recovers_restricted_model(phi_gamma):
    """REGRESSION. The restricted form is built INDEPENDENTLY from expm, not by
    calling historical_weight with eta = 0 -- otherwise this asserts that a
    function equals itself."""
    qJ, qP, mu, rho = 0.03, 0.05, 0.04, 0.02
    Q = generator(q={"J": qJ, "P": qP}, betas={"J": BJ, "P": BP},
                  mus={"E": mu, "J": 0.002, "P": 0.002})
    pi = {"E": 1 - qJ - qP, "J": qJ, "P": qP}
    w_general = historical_weight(Q, pi=pi, eta=E0, grid=phi_gamma.grid,
                                  g_E=lambda u: np.exp(-rho * u))
    M = np.asarray(Q)
    w_restricted = np.array([expm(M * u)[0, 0] * np.exp(-rho * u)
                             for u in phi_gamma.grid])
    assert np.allclose(w_general, w_restricted, atol=TOL_EXACT)


# --- 5. Absorbing-only closed form (Corollary 4) -------------------------

@pytest.mark.parametrize("mu", [0.0, 0.01, 0.04, 0.10, 0.25])
def test_absorbing_only_closed_form(phi_gamma, mu):
    w = _w(phi_gamma, {}, {}, {"E": mu}, {"E": 1.0})
    assert np.allclose(w, np.exp(-mu * phi_gamma.grid), atol=TOL_EXACT)


def test_mu_crit_is_a_root(phi_gamma):
    import sys
    sys.path.insert(0, str(__import__("pathlib").Path(__file__).parents[1] / "analysis"))
    from mortality_threshold import mu_crit, absorbing_w
    mc = mu_crit(phi_gamma, theta=0.844, c=0.25)
    assert r_star(phi_gamma, absorbing_w(phi_gamma, mc),
                  theta=0.844, c=0.25) == pytest.approx(1.0, abs=1e-6)


def test_rho_handles_unreachable_state():
    """REGRESSION. Taking a dominant eigenvalue is wrong when the unobservable
    state is unreachable and therefore empty."""
    Q = generator(q={}, betas={}, mus={"E": 0.10})
    assert rho_susceptible(Q, lam=0.05) == pytest.approx(-0.15, abs=1e-6)


# --- 6. Pan composition -------------------------------------------------

PAN_T1 = [(0.00, 1.0, 0.0, -9.95), (0.00, 1.0, 0.6, -3.98),
          (0.00, 2.0, 0.0, -15.03), (0.25, 1.0, 0.0, -5.93),
          (0.25, 1.0, 0.6, -1.36), (0.25, 1.0, 1.0, 1.68),
          (0.25, 2.0, 0.0, -8.97), (0.25, 2.0, 0.6, -0.10),
          (0.25, 2.0, 1.0, 5.82)]


@pytest.mark.parametrize("c,theta,r,published", PAN_T1)
def test_pan_recovery(phi_pan_arxiv, c, theta, r, published):
    ones = np.ones_like(phi_pan_arxiv.grid)
    got = 1e3 * 0.032 * (np.exp(lel(phi_pan_arxiv, ones, r=r, c=c,
                                    theta=theta)) - 1)
    assert got == pytest.approx(published, abs=0.05)


def test_zero_bias_boundary_is_phi_free(phi_gamma, phi_cephia, phi_rectangular):
    """
    At w == 1 the boundary is exp(-theta c) exactly, independent of the RECENCY
    FUNCTION. phi_rectangular is a rectangular recency WINDOW -- unrelated to a
    uniform INTER-TEST process, which is a property of testing behaviour. The
    boundary is exactly phi-free under Poisson inter-test; under uniform
    inter-test it is only approximately so. Conflating assay basis with testing
    process is the error that set the predecessor's sign.
    """
    for theta, c in ((0.5, 0.25), (1.0, 0.25), (2.0, 0.25), (1.0, 0.5)):
        for phi in (phi_gamma, phi_cephia, phi_rectangular):
            ones = np.ones_like(phi.grid)
            if phi.values[phi.grid > c].max(initial=0.0) == 0.0:
                continue        # exclusion inert; covered by the test below
            assert r_star(phi, ones, theta=theta, c=c) == pytest.approx(
                boundary_no_dynamics(theta, c), abs=1e-7)


def test_inert_exclusion_is_refused(phi_rectangular):
    """
    Degenerate case. A 180-day rectangular window has no support beyond
    c = 0.5 y, so K_w == 0, LEL is identically zero for every r, and no
    boundary exists. r_star must refuse rather than return the bracket endpoint.
    """
    from src.pan_composition import InertExclusion, K_w
    ones = np.ones_like(phi_rectangular.grid)
    assert K_w(phi_rectangular, ones, c=0.5, theta=1.0) == pytest.approx(0.0, abs=1e-12)
    assert lel(phi_rectangular, ones, r=0.3, c=0.5, theta=1.0) == pytest.approx(0.0)
    assert lel(phi_rectangular, ones, r=9.9, c=0.5, theta=1.0) == pytest.approx(0.0)
    with pytest.raises(InertExclusion):
        r_star(phi_rectangular, ones, theta=1.0, c=0.5)


def test_dynamics_move_the_boundary_up(phi_gamma):
    w = _w(phi_gamma, {}, {}, {"E": 0.10}, {"E": 1.0})
    assert r_star(phi_gamma, w, theta=0.844, c=0.25) > \
        boundary_no_dynamics(0.844, 0.25)


# --- 7. Numerical consistency -------------------------------------------

@pytest.mark.parametrize("nstate", [2, 3])
def test_matrix_exponential_matches_analytic(nstate, closed_form_S1):
    """Only 2 and 3 are parametrised; no independent 4-state analytic form
    exists, and testing expm against itself would be vacuous."""
    Q, analytic = closed_form_S1(nstate)
    u = np.linspace(0, 2.0, 97)
    M = np.asarray(Q)
    assert np.allclose([expm(M * x)[0, 0] for x in u], analytic(u),
                       atol=1e-12)


def test_quadrature_matches_closed_form(phi_gamma):
    Q = generator(q={"J": 0.03}, betas={"J": BJ}, mus={"E": 0.04, "J": 0.002})
    pi, eta = {"E": 0.97, "J": 0.03}, {"E": 1.0, "J": 0.3}
    w = historical_weight(Q, pi=pi, eta=eta, grid=phi_gamma.grid)
    grid_val = np.trapezoid(phi_gamma.values * w, phi_gamma.grid)
    adaptive = integrate.quad(
        lambda u: float(phi_gamma(u)) * historical_weight(Q, pi=pi, eta=eta, at=u),
        0, 2.0, limit=200)[0]
    assert grid_val == pytest.approx(adaptive, rel=1e-5)


def test_plim_rejects_mismatched_grid(phi_gamma):
    w = np.ones(7)
    with pytest.raises(ValueError, match="expected"):
        plim_ratio(phi_gamma, w)


def test_gamma_params_match_xsrecency():
    """window 101 d / shadow 194 d -> shape 0.352, rate 1.273 (published)."""
    from src.eligibility_dynamics import YEAR_DAYS
    W, H = 101 / YEAR_DAYS, 194 / YEAR_DAYS
    rate = 1.0 / (2 * H - W)
    assert rate == pytest.approx(1.273, abs=0.001)
    assert W * rate == pytest.approx(0.352, abs=0.001)


# ---------------------------------------------------------------------------
# Inter-test process vs assay basis
# ---------------------------------------------------------------------------

BASES_6 = [(97, 180), (101, 194), (130, 220), (163, 260), (182, 290), (300, 400)]


def _six_bases():
    from src.eligibility_dynamics import gamma_phi, default_grid
    g = default_grid(4001)
    return [gamma_phi(w, h, g) for w, h in BASES_6]


def test_lel_general_reproduces_the_poisson_closed_form(phi_gamma):
    """
    Internal check on the general derivation: with a Poisson process, the general
    kept-mass form must reproduce `lel` exactly. If this drifts, the general
    expression is wrong, not the Poisson one.
    """
    from src.pan_composition import lel, lel_general, PoissonInterTest
    ones = np.ones_like(phi_gamma.grid)
    for theta in (0.5, 0.8439, 1.0, 2.0):
        for r in (0.4, 1.0, 1.7):
            assert lel_general(phi_gamma, ones, r, 0.25,
                               PoissonInterTest(theta)) == pytest.approx(
                lel(phi_gamma, ones, r=r, c=0.25, theta=theta), abs=1e-9)


def test_boundary_closed_form_agrees_with_root_finding(phi_gamma):
    """r_star_general is algebraic; r_star brackets numerically. They must agree."""
    from src.pan_composition import r_star, r_star_general, PoissonInterTest
    ones = np.ones_like(phi_gamma.grid)
    for theta, c in ((0.5, 0.25), (1.0, 0.25), (2.0, 0.25), (1.0, 0.4)):
        assert r_star_general(phi_gamma, ones, c, PoissonInterTest(theta)) == \
            pytest.approx(r_star(phi_gamma, ones, theta=theta, c=c), abs=1e-6)


def test_uniform_inter_test_boundary_is_only_approximately_phi_free():
    """
    Assay basis is not inter-test process. Under Poisson the boundary is exactly
    e^{-theta c} and exactly free of phi; under Pan's Uniform[0,b] variant it is
    neither. Invariance survives only approximately -- the record's ceiling is
    0.6% relative spread across bases spanning MDRI 94-251 d.
    """
    from src.pan_composition import (r_star_general, PoissonInterTest,
                                     UniformInterTest, boundary_no_dynamics)
    bases = _six_bases()
    c = 0.25

    exact = np.array([r_star_general(p, np.ones_like(p.grid), c,
                                     PoissonInterTest(1.0)) for p in bases])
    np.testing.assert_allclose(exact, boundary_no_dynamics(1.0, c), atol=1e-9)
    assert np.ptp(exact) < 1e-9, "Poisson invariance must be exact, not approximate"

    for b, ceiling in ((3.0, 0.006), (4.0, 0.006)):
        proc = UniformInterTest(b)
        rs = np.array([r_star_general(p, np.ones_like(p.grid), c, proc)
                       for p in bases])
        rel = np.ptp(rs) / rs.mean()
        assert 0.0 < rel <= ceiling, \
            f"Uniform[0,{b}]: relative spread {rel:.4f} exceeds {ceiling}"


def test_uniform_boundary_is_not_the_denominator_inclusion():
    """
    Guard on a false generalisation. r* = Pr(S>c) is Poisson-specific. Under
    Uniform[0,3], P_0 = (1-c/b)^2 = 0.8403 but r* is about 0.90, so reading the
    boundary off the denominator would understate it by six percentage points.
    """
    from src.pan_composition import (r_star_general, UniformInterTest,
                                     PoissonInterTest)
    from src.eligibility_dynamics import gamma_phi, default_grid
    g = default_grid(4001)
    phi = gamma_phi(163, 260, g)
    ones = np.ones_like(g)
    c = 0.25

    for b, p0_ref in ((3.0, 0.8403), (4.0, 0.8789)):
        proc = UniformInterTest(b)
        assert proc.P0(c) == pytest.approx(p0_ref, abs=5e-5)
        rs = r_star_general(phi, ones, c, proc)
        assert rs > proc.P0(c) + 0.04, \
            f"Uniform[0,{b}]: r* {rs:.4f} vs P_0 {proc.P0(c):.4f}"

    # whereas under Poisson the two coincide exactly
    proc = PoissonInterTest(1.0)
    assert r_star_general(phi, ones, c, proc) == pytest.approx(proc.P0(c), abs=1e-9)


def test_uniform_inter_test_reduces_to_its_mean_gap_only_approximately(phi_gamma):
    """
    Uniform[0,b] has mean gap b/2, so theta = 2/b is the comparable Poisson rate.
    Matching the mean does NOT match the boundary -- the discrepancy is the whole
    content of the distinction.
    """
    from src.pan_composition import (r_star_general, UniformInterTest,
                                     PoissonInterTest)
    ones = np.ones_like(phi_gamma.grid)
    proc = UniformInterTest(3.0)
    matched = PoissonInterTest(proc.theta_equivalent)
    u = r_star_general(phi_gamma, ones, 0.25, proc)
    p = r_star_general(phi_gamma, ones, 0.25, matched)
    assert abs(u - p) > 0.05, (
        f"uniform {u:.4f} vs mean-matched Poisson {p:.4f}: if these agreed, the "
        "process/basis distinction would not matter")
