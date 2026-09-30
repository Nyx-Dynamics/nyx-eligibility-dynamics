"""
Corollary 2 under an explicitly non-Markov movement process.

Section 2 assumes E.1, a time-homogeneous Markov jump process, so sojourns are
exponential and the hazard of re-incarceration does not depend on how many
episodes a person has had or how recently they were released. Carceral contact
is not like that: it is recurrent, concentrated in a minority, and the hazard is
highest immediately after release.

Remark 2 argues E.1 is not needed for the cancellation, because with eta = 1 and
infection-independent movement the weight collapses by the law of total
probability to Pr{Z(t)=E}/pi_E = 1, which uses only stationarity. This tests
that argument against a process that violates E.1 in every way that matters:

  * Weibull free periods with shape < 1, so the hazard of returning to custody
    DECREASES with time since release -- textbook recidivism, strongly
    history-dependent, and not exponential;
  * lognormal heterogeneity in individual propensity, so movement is
    concentrated rather than uniform.

Population parameters are constant in calendar time, so the process is
stationary though not Markov. That is the distinction the test isolates: the
cancellation needs stationarity, not memorylessness.
"""
import math

import numpy as np
import pytest

from src.eligibility_dynamics import gamma_phi, default_grid, omega

PREV, INC = 0.121, 0.038
U_MAX = PREV / (INC * (1 - PREV))
T_OBS = 40.0                      # long burn-in so the renewal process settles
N = 40_000
REPS = 4
TOL = 0.04                        # Monte Carlo, not machine precision


def _population(rng, n, shape=0.6, mean_free=1.05, mean_jail=32 / 365.25,
                frailty_sd=0.8):
    """
    Alternating renewal per individual: free, custody, free, ...

    Returns (observable_at_t, observable_at_infection, u), where u is infection
    duration drawn on the flat density of Pan's construction.
    """
    frail = np.exp(rng.normal(0, frailty_sd, n) - frailty_sd ** 2 / 2)
    scale = mean_free * frail / math.gamma(1 + 1 / shape)
    horizon = T_OBS + U_MAX + 1.0
    u = rng.uniform(0, U_MAX, n)
    at_t = np.empty(n, bool)
    at_inf = np.empty(n, bool)
    for i in range(n):
        # start mid-free-period so the process is in equilibrium, not at a renewal
        t = rng.weibull(shape) * scale[i] * rng.random()
        seq = [t]
        while t < horizon:
            t += rng.exponential(mean_jail); seq.append(t)
            t += rng.weibull(shape) * scale[i]; seq.append(t)
        s = np.asarray(seq)
        at_t[i] = (np.searchsorted(s, T_OBS) % 2) == 0
        at_inf[i] = (np.searchsorted(s, T_OBS - u[i]) % 2) == 0
    return at_t, at_inf, u


def _ratio(rng, phi):
    at_t, at_inf, u = _population(rng, N)
    infected = rng.random(N) < PREV
    # eta = 1: infection arises at t-u regardless of state, so no reweighting
    n_rec = float((phi(u[infected]) * at_t[infected]).sum())
    n_neg = int(at_t[~infected].sum())
    lam_hat = n_rec / (n_neg * omega(phi))
    return lam_hat / INC, 1.0 - at_t.mean(), at_inf[infected].mean()


@pytest.mark.slow
def test_cancellation_survives_non_markov_recidivism():
    phi = gamma_phi(163, 260, default_grid(4001))
    out = [_ratio(np.random.default_rng(90_000 + i), phi) for i in range(REPS)]
    r = np.array([x[0] for x in out])
    q = np.mean([x[1] for x in out])
    obs_at_inf = np.mean([x[2] for x in out])

    # the test is only meaningful if the process actually exercises the mechanism
    assert q > 0.05, f"too little time unobservable to test anything: q={q:.3f}"
    assert obs_at_inf < 0.95, \
        f"almost nobody infected while unobservable: {obs_at_inf:.3f}"

    sem = r.std(ddof=1) / np.sqrt(len(r))
    assert abs(r.mean() - 1.0) < TOL, (
        f"non-Markov recidivism broke the cancellation: "
        f"{r.mean():.4f} (sem {sem:.4f}) at q={q:.3f}")


def test_weibull_free_periods_are_not_exponential():
    """
    Guard on the premise. If the free-period draw were exponential the process
    would be Markov and the test above would prove nothing.
    """
    rng = np.random.default_rng(3)
    shape = 0.6
    x = rng.weibull(shape, 200_000)
    # decreasing hazard: the conditional mean residual life grows with age
    early = x[x > np.quantile(x, 0.10)].mean() - np.quantile(x, 0.10)
    late = x[x > np.quantile(x, 0.75)].mean() - np.quantile(x, 0.75)
    assert late > early * 1.5, (
        "free periods do not show decreasing hazard; the process may be "
        f"effectively memoryless (early {early:.3f}, late {late:.3f})")
