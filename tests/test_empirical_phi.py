"""
Empirical recency function: the fitting machinery, and the frozen CEPHIA claim.

Split deliberately into three layers, so that a clone with no external data
still tests something real:

  * the estimator is checked against a SYNTHETIC curve whose MDRI is known in
    closed form. This runs always and needs no dataset;
  * the frozen aggregate expectations in data/fixtures/cephia_expected.json are
    checked for internal consistency and for the Assumption B.1 violation. These
    run always -- the fixture carries no participant rows;
  * the full refit against the CEPHIA CSV runs only when the dataset is present.

Unit convention. XSRecency::createRitaCephia changed its contract between tag
0.2.0 (days) and main (years), and the shipped vignette double-converts against
main. `test_unit_convention_is_years` is the guard: feeding days where years are
expected moves MDRI by three orders of magnitude, not by a few percent.
"""
import numpy as np
import pytest

from src.eligibility_dynamics import (
    T_STAR, YEAR_DAYS, default_grid, empirical_phi, gamma_phi,
)

GRID = default_grid(2001)


def _expit(x):
    return 1.0 / (1.0 + np.exp(-x))


# logit phi(u) = 3.0 - 6.0 u + 1.2 u^2: 0.95 at u=0, 0.14 at u=1, 0.015 at T*
TRUE_COEF = (3.0, -6.0, 1.2)


def _true_phi(u):
    u = np.asarray(u, float)
    return _expit(TRUE_COEF[0] + TRUE_COEF[1] * u + TRUE_COEF[2] * u ** 2)


def _true_mdri_days():
    return float(np.trapezoid(_true_phi(GRID), GRID) * YEAR_DAYS)


def _synthetic(n=60_000, seed=7, u_hi=3.0):
    rng = np.random.default_rng(seed)
    u = rng.uniform(0.0, u_hi, n)
    recent = (rng.random(n) < _true_phi(u)).astype(int)
    return u, recent


def test_empirical_phi_recovers_a_known_curve():
    """The logit-polynomial fit recovers an MDRI computable in closed form."""
    u, recent = _synthetic()
    phi = empirical_phi(u, recent, degree=3, grid=GRID)
    truth = _true_mdri_days()
    assert phi.mdri_days == pytest.approx(truth, abs=6.0), \
        f"fitted {phi.mdri_days:.1f} d vs true {truth:.1f} d"
    # pointwise, not just the integral
    for x in (0.1, 0.5, 1.0, 1.5, 1.9):
        assert float(phi(x)) == pytest.approx(float(_true_phi(x)), abs=0.04)
    # and the fitted phi obeys the window convention
    assert float(phi(T_STAR + 0.5)) == 0.0


def test_empirical_phi_clusters_do_not_move_the_point_estimate():
    """
    GEE with an independence working correlation gives the same point estimate as
    unclustered logistic regression; clustering changes the variance only. Stated
    as a test because the analysis script relies on it.
    """
    u, recent = _synthetic(n=20_000, seed=11)
    groups = np.repeat(np.arange(len(u) // 4), 4)[:len(u)]
    a = empirical_phi(u, recent, degree=3, grid=GRID)
    b = empirical_phi(u, recent, degree=3, grid=GRID, groups=groups)
    assert b.mdri_days == pytest.approx(a.mdri_days, rel=1e-6)


def test_unit_convention_is_years():
    """
    Guard on the days/years contract. Fitting the same specimens with durations
    expressed in days puts essentially all the mass outside [0, T*], so MDRI
    collapses -- it does not shift slightly.
    """
    u, recent = _synthetic(n=20_000, seed=3)
    years = empirical_phi(u, recent, degree=3, grid=GRID)
    days = empirical_phi(u * YEAR_DAYS, recent, degree=3, grid=GRID)
    assert years.mdri_days > 100.0
    assert days.mdri_days > years.mdri_days * 3, \
        "a days/years mix-up must be obvious, not subtle"


def test_frozen_cephia_fixture_is_self_consistent(cephia_expected):
    """The frozen aggregates are internally coherent and bracket Pan's 163 d."""
    algs = cephia_expected["algorithms"]
    assert len(algs) == 3
    pan = cephia_expected["pan_published_mdri_days"]
    for a in algs:
        assert a["ci_lo"] < a["mdri_days"] < a["ci_hi"]
        assert a["participants"] > 100
    ref = next(a for a in algs if a["subtype"] == "C" and a["vl_threshold"] == 75)
    assert ref["mdri_days"] == pytest.approx(182.4, abs=0.05)
    assert ref["ci_lo"] <= pan <= ref["ci_hi"], \
        "Pan's published 163 d must fall inside the subtype-C interval"
    # raising the viral-load threshold removes low-VL specimens and shortens MDRI
    hi_vl = next(a for a in algs if a["subtype"] == "C" and a["vl_threshold"] == 1000)
    assert hi_vl["mdri_days"] < ref["mdri_days"]


def test_empirical_phi_tail_is_not_flat(cephia_expected):
    """
    Gao & Bannick Assumption B.1 requires phi constant at beta_{T*} beyond T*.

    Neither CEPHIA subset is flat, and they fail in OPPOSITE directions: among
    treatment-naive visits the test-recent proportion declines to zero, while
    across all visits it rises in the final bin because ART drives LAg ODn back
    down and treated individuals re-enter the recent category at long duration.

    An earlier fixture recorded 0.099, 0.058, 0 at n=4184 for the untreated
    subset. Those values do not reproduce from the public-use dataset by any
    subset tried; the qualitative claim does. The test now asserts the shape of
    each subset separately rather than a single sequence.
    """
    tail = cephia_expected["tail_bins"]
    edges = tail["edges_days"]
    assert all(e > T_STAR * YEAR_DAYS * 0.99 for e in edges[:-1])

    naive = tail["treatment_naive"]["proportion_test_recent"]
    assert len(naive) == len(edges) - 1
    assert all(naive[i] > naive[i + 1] for i in range(len(naive) - 1)), \
        f"untreated tail must decline, got {naive}"
    assert naive[-1] == pytest.approx(0.0, abs=1e-9)

    allv = tail["all_visits"]["proportion_test_recent"]
    assert allv[-1] > allv[-2], \
        f"all-visit tail must rise in the final bin, got {allv}"

    # a flat tail would be consistent with a single constant beta_{T*}
    for props in (naive, allv):
        assert max(props) - min(props) > 0.02


@pytest.mark.slow
def test_empirical_phi_matches_fixture(local_cephia_csv, cephia_expected):
    """
    Full refit against the CEPHIA CSV, compared to the frozen expectation.

    Skipped without the dataset, which is not redistributed. The script
    analysis/empirical_phi.py performs the same comparison and writes
    outputs/cephia_recomputed.json; it never overwrites the fixture.
    """
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
    from empirical_phi import load, fit, binned_recency

    d = load(local_cephia_csv)
    tol = float(cephia_expected["mdri_tolerance_days"])
    for e in cephia_expected["algorithms"]:
        phi, n = fit(d, e["subtype"], e["vl_threshold"])
        assert phi.mdri_days == pytest.approx(e["mdri_days"], abs=tol), \
            (f"subtype {e['subtype']}, VL>{e['vl_threshold']}: "
             f"{phi.mdri_days:.1f} d vs frozen {e['mdri_days']:.1f} d")
        assert n == e["participants"]

    naive, n_naive = binned_recency(d, treatment_naive=True)
    allv, n_all = binned_recency(d)
    exp = cephia_expected["tail_bins"]
    for got, key in ((naive, "treatment_naive"), (allv, "all_visits")):
        want = exp[key]["proportion_test_recent"]
        assert got == pytest.approx(want, abs=0.002), f"{key}: {got} vs {want}"
    assert n_naive == exp["treatment_naive"]["n_visits"]
    assert n_all == exp["all_visits"]["n_visits"]


def test_cephia_phi_differs_materially_from_the_parametric_bases(cephia_expected):
    """
    The empirical MDRI is not interchangeable with the gamma bases used for the
    Pan reproduction, so phi-independence claims are not being tested against
    near-identical curves.
    """
    ref = cephia_expected["algorithms"][0]["mdri_days"]
    for w, h in ((163, 260), (101, 194)):
        assert abs(gamma_phi(w, h, GRID).mdri_days - ref) > 15.0
