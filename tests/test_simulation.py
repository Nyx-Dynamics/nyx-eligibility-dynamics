"""
Monte Carlo agreement: the analytic results against an independently written
generative model.

`src.simulation` imports no analytic expression beyond `omega` (a quadrature of
phi, which the simulator needs to scale its own estimator), so agreement here is
between two genuinely separate routes to the same quantity rather than a
restatement of one of them.

Two development errors are guarded directly:

  * seeds were once shared across parameter cells, which makes residuals
    perfectly correlated and degenerates an agreement test into a sign test on
    one realisation. `test_cell_seeds_are_disjoint` is a deterministic check on
    the seeding scheme, so it cannot itself be flaky;
  * `phi(u)` once returned phi(T*) rather than 0 for u > T*, because np.interp
    clamps at the grid endpoints. The simulator draws durations out to
    U_max = p/(lambda(1-p)) = 3.62 y, well past T* = 2, so this inflated every
    recent count by a scenario-dependent amount. Guarded by
    `test_phi_vanishes_outside_the_window`.
"""
import numpy as np
import pytest

from src.eligibility_dynamics import (
    T_STAR, generator, historical_weight, plim_ratio, omega,
)
from src.pan_composition import lel
from src.simulation import SimConfig, simulate_ratio, simulate_lel

N_PER_REP = 1_500_000
N_REP = 6
Z_MAX = 4.0

THETA = 0.8439           # NHBS 57% tested in 12 months, Poisson
C_PURPOSE = 0.25         # PURPOSE testing-based exclusion, years
BETA_JAIL = 365.25 / 32
BETA_PRISON = 1.0 / 2.7

# (label, q, mus, eta). Chosen to exercise each failure mode separately:
# exact cancellation, absorbing loss alone, eta below one, eta above one, and a
# large occupancy where the weight departs from one substantially.
CENSUS_CELLS = [
    ("cancellation",      {"J": .03, "P": .05}, {"E": 0., "J": 0., "P": 0.},
                          {"E": 1., "J": 1., "P": 1.}),
    ("absorbing_004",     {},                   {"E": .04},
                          {"E": 1.}),
    ("absorbing_010",     {},                   {"E": .10},
                          {"E": 1.}),
    ("eta_zero",          {"J": .03, "P": .05}, {"E": .04, "J": .002, "P": .002},
                          {"E": 1., "J": 0., "P": 0.}),
    ("eta_partial",       {"J": .03, "P": .05}, {"E": .04, "J": .002, "P": .002},
                          {"E": 1., "J": .3, "P": .3}),
    ("eta_above_one",     {"J": .03, "P": .05}, {"E": .04, "J": .002, "P": .002},
                          {"E": 1., "J": 1.8, "P": 1.8}),
    ("high_occupancy",    {"J": .15},           {"E": .04, "J": .002},
                          {"E": 1., "J": 0.}),
]

LEL_CELLS = [0.3, 0.5, 0.809, 1.0, 1.6]


def cell_seeds(cell: int, n_rep: int = N_REP) -> list[int]:
    """
    Disjoint seed block per cell.

    Sharing one population across cells is tempting -- eta and r enter the
    estimator as deterministic weights, so a single realisation would suffice --
    but it makes every cell's residual the same random draw. Do not optimise
    this away; see docs/REPRODUCE.md section 2.
    """
    return [10_000 * (cell + 1) + i for i in range(n_rep)]


def build(q, mus, eta):
    betas = {k: (BETA_JAIL if k == "J" else BETA_PRISON) for k in q}
    Q = generator(q=q, betas=betas, mus=mus)
    pi = {"E": 1.0 - sum(q.values()), **q}
    return Q, pi, eta


def test_cell_seeds_are_disjoint():
    """Deterministic guard against the correlated-seed artifact."""
    blocks = [cell_seeds(i) for i in range(len(CENSUS_CELLS) + len(LEL_CELLS))]
    flat = [s for b in blocks for s in b]
    assert len(flat) == len(set(flat)), "seed blocks overlap across cells"
    for b in blocks:
        assert len(b) == len(set(b)), "seeds repeat within a cell"


def test_phi_vanishes_outside_the_window(phi_gamma):
    """
    np.interp clamps above the grid. Under beta_{T*} = 0, phi must be zero past
    T*, and the simulator evaluates phi well past it.
    """
    assert phi_gamma(T_STAR - 0.05) > 0.0
    assert float(phi_gamma(T_STAR + 1e-9)) == pytest.approx(0.0, abs=1e-12)
    for u in (2.5, 3.62, 10.0):
        assert float(phi_gamma(u)) == 0.0
    assert float(phi_gamma(-0.5)) == 0.0
    # and the clamped alternative would have been materially non-zero
    assert np.interp(3.62, phi_gamma.grid, phi_gamma.values) > 0.02


def test_simulator_targets_lambda_E_not_total_incidence(phi_gamma):
    """
    Total infection flow is N_neg * lambda_E * sum_k pi_k eta_k, so the
    simulator's generative lambda is the TOTAL hazard and must be converted.
    Without the conversion, any eta != 1 reads as disagreement with Theorem 2:
    the ratio of the two normalisations is exactly sum_k pi_k eta_k.
    """
    q = {"J": .03, "P": .05}
    Q, pi, eta = build(q, {"E": .04, "J": .002, "P": .002},
                       {"E": 1., "J": .3, "P": .3})
    pi_eta_sum = sum(pi[s] * eta[s] for s in Q.states)
    assert pi_eta_sum == pytest.approx(0.944)

    w = historical_weight(Q, pi=pi, eta=eta, grid=phi_gamma.grid)
    analytic = plim_ratio(phi_gamma, w)
    mc = np.mean([simulate_ratio(phi_gamma, Q, pi, eta, n=1_000_000, seed=s)
                  for s in cell_seeds(99, 4)])
    assert mc == pytest.approx(analytic, abs=3e-3)
    # the un-normalised quantity is off by the identified factor, not by noise
    assert mc * pi_eta_sum == pytest.approx(analytic * pi_eta_sum, abs=3e-3)
    assert abs(mc / pi_eta_sum - analytic) > 5e-3


@pytest.mark.slow
@pytest.mark.parametrize("cell", range(len(CENSUS_CELLS)),
                         ids=[c[0] for c in CENSUS_CELLS])
def test_monte_carlo_matches_analytic(cell, phi_gamma):
    """
    Census mode: the simulated plim of lambda_hat / lambda_E against Theorem 2's
    integral, one independent seed block per cell.
    """
    label, q, mus, eta = CENSUS_CELLS[cell]
    Q, pi, eta = build(q, mus, eta)
    analytic = plim_ratio(phi_gamma, historical_weight(Q, pi=pi, eta=eta,
                                                      grid=phi_gamma.grid))
    reps = np.array([simulate_ratio(phi_gamma, Q, pi, eta, n=N_PER_REP, seed=s)
                     for s in cell_seeds(cell)])
    sem = reps.std(ddof=1) / np.sqrt(len(reps))
    z = (reps.mean() - analytic) / sem
    assert abs(z) < Z_MAX, (
        f"{label}: analytic {analytic:.5f}, MC {reps.mean():.5f} "
        f"(sem {sem:.5f}), z = {z:.2f}")


@pytest.mark.slow
@pytest.mark.parametrize("i,r", list(enumerate(LEL_CELLS)),
                         ids=[f"r{r}" for r in LEL_CELLS])
def test_monte_carlo_matches_analytic_lel(i, r, phi_gamma):
    """
    Screening mode with w == 1: the simulated LEL against Pan's closed form.

    The simulator reconstructs the stop-when-positive testing history and applies
    attendance and exclusion directly; it never evaluates Pan's integral. The
    zero crossing lands at r* = e^{-theta c} without that value being supplied.
    """
    Q, pi, eta = build({}, {"E": 0.0}, {"E": 1.0})
    w = historical_weight(Q, pi=pi, eta=eta, grid=phi_gamma.grid)
    np.testing.assert_allclose(w, 1.0, atol=1e-12)

    analytic = lel(phi_gamma, w, r=r, c=C_PURPOSE, theta=THETA)
    reps = np.array([simulate_lel(phi_gamma, Q, pi, eta, r=r, c=C_PURPOSE,
                                  theta=THETA, n=N_PER_REP, seed=s)
                     for s in cell_seeds(len(CENSUS_CELLS) + i)])
    sem = reps.std(ddof=1) / np.sqrt(len(reps))
    z = (reps.mean() - analytic) / sem
    assert abs(z) < Z_MAX, (
        f"r={r}: analytic {analytic:.5f}, MC {reps.mean():.5f} "
        f"(sem {sem:.5f}), z = {z:.2f}")
    if r == pytest.approx(np.exp(-THETA * C_PURPOSE), abs=1e-3):
        assert abs(reps.mean()) < 4 * sem + 1e-3


@pytest.mark.slow
def test_monte_carlo_matches_composed_lel(phi_gamma):
    """
    Dynamics AND screening together -- the composition of section 2.7, which is
    not a special case of either module alone.
    """
    Q, pi, eta = build({"J": .03, "P": .05}, {"E": .04, "J": .002, "P": .002},
                       {"E": 1., "J": .3, "P": .3})
    w = historical_weight(Q, pi=pi, eta=eta, grid=phi_gamma.grid)
    assert not np.allclose(w, 1.0)
    for j, r in enumerate((0.5, 1.6)):
        analytic = lel(phi_gamma, w, r=r, c=C_PURPOSE, theta=THETA)
        reps = np.array([simulate_lel(phi_gamma, Q, pi, eta, r=r, c=C_PURPOSE,
                                      theta=THETA, n=N_PER_REP, seed=s)
                         for s in cell_seeds(80 + j)])
        sem = reps.std(ddof=1) / np.sqrt(len(reps))
        z = (reps.mean() - analytic) / sem
        assert abs(z) < Z_MAX, (
            f"composed r={r}: analytic {analytic:.5f}, MC {reps.mean():.5f}, "
            f"z = {z:.2f}")


def test_u_max_matches_pan_construction():
    """U_max = p / (lambda (1-p)), Pan Lemma S.1."""
    cfg = SimConfig(prevalence=0.121, incidence=0.038)
    assert cfg.u_max == pytest.approx(0.121 / (0.038 * 0.879), rel=1e-12)
    assert cfg.u_max > T_STAR, "the flat duration support must extend past T*"


def test_simulator_refuses_impossible_population(phi_gamma):
    """pi * eta identically zero means no infection can arise anywhere."""
    Q, pi, _ = build({"J": .05}, {"E": .0, "J": .0}, {})
    with pytest.raises(ValueError, match="no infections"):
        simulate_ratio(phi_gamma, Q, pi, {"E": 0.0, "J": 0.0}, n=1000, seed=0)
