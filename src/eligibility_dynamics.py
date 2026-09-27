"""
Eligibility dynamics for cross-sectional HIV incidence estimation.

Implements the theory frozen in manuscript/section2_theory.md. Notation follows
Gao & Bannick (Stat Med 2022;41:1446-61): A(t) is eligibility, refined here as
A(t) = 1{Z(t) = E} for a process Z on living states L = {E, O_1, ..., O_m} plus
an absorbing state X.

Conventions
-----------
Time in YEARS. Rates per year. T_STAR = 2.0.
State E is always index 0, so [expm(Q u)][0, 0] is the E -> E transition.
Matrices are restricted to living states; X is implicit in row-sum deficits.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Mapping, Sequence

import numpy as np
from scipy import stats
from scipy.linalg import expm

__all__ = [
    "T_STAR", "YEAR_DAYS",
    "RecencyFunction", "gamma_phi", "rectangular_phi", "empirical_phi",
    "Generator", "generator", "transition",
    "S1_closed", "rho_susceptible",
    "historical_weight", "omega", "plim_ratio",
    "default_grid",
]

T_STAR = 2.0
YEAR_DAYS = 365.25


def default_grid(n: int = 2001, t_star: float = T_STAR) -> np.ndarray:
    """Integration grid on [0, T*]."""
    return np.linspace(0.0, t_star, n)


# ---------------------------------------------------------------------------
# Recency function phi(u)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class RecencyFunction:
    """
    Duration-specific test-recent probability phi(u) = Pr(M in R | T = t-u, A(t)=1).

    Conditions on eligibility AT SURVEY, so it carries no eligibility-survival
    component -- that enters separately through the transition process. See
    manuscript Remark 1.
    """

    grid: np.ndarray
    values: np.ndarray
    label: str = ""

    def __call__(self, u):
        """
        phi(u), with phi == 0 OUTSIDE [0, T*].

        np.interp clamps to the endpoint values, which would return phi(T*) for
        u > T* -- wrong under the beta_{T*} = 0 convention of Theorem 1, and a
        silent source of inflated recent counts for any caller evaluating
        durations beyond the recency window.
        """
        u = np.asarray(u, float)
        out = np.interp(u, self.grid, self.values)
        return np.where((u >= self.grid[0]) & (u <= self.grid[-1]), out, 0.0)

    @property
    def mdri_days(self) -> float:
        """Omega_{T*} expressed in days."""
        return float(np.trapezoid(self.values, self.grid) * YEAR_DAYS)

    @property
    def shadow_days(self) -> float:
        om = np.trapezoid(self.values, self.grid)
        return float(np.trapezoid(self.grid * self.values, self.grid) / om * YEAR_DAYS)


def gamma_phi(window_days: float, shadow_days: float,
              grid: np.ndarray | None = None) -> RecencyFunction:
    """
    Gamma-form phi with a target window and shadow period.

    Matches XSRecency::get.gamma.params:
        shape = W / (2H - W),  rate = 1 / (2H - W),   W = window, H = shadow (years)
    Verified against the published parameters for window 101 d / shadow 194 d,
    which give shape 0.3519, rate 1.2718 (published: 0.352, 1.273).
    """
    grid = default_grid() if grid is None else np.asarray(grid, float)
    W, H = window_days / YEAR_DAYS, shadow_days / YEAR_DAYS
    denom = 2.0 * H - W
    if denom <= 0:
        raise ValueError("require 2*shadow > window")
    rate = 1.0 / denom
    shape = W * rate
    vals = 1.0 - stats.gamma.cdf(grid, shape, scale=1.0 / rate)
    return RecencyFunction(grid, vals, f"gamma {window_days:g}/{shadow_days:g}")


def rectangular_phi(window_days: float,
                    grid: np.ndarray | None = None) -> RecencyFunction:
    """
    Rectangular recency WINDOW: phi(u) = 1 for u <= window, else 0.

    NOTE. This is an assay basis. It is unrelated to a uniform INTER-TEST-TIME
    process, which is a property of testing behaviour. Conflating the two is the
    error that determined the sign of the predecessor manuscript's joint bias
    factor; see docs/PROVENANCE.md.
    """
    grid = default_grid() if grid is None else np.asarray(grid, float)
    vals = (grid <= window_days / YEAR_DAYS).astype(float)
    return RecencyFunction(grid, vals, f"rectangular {window_days:g}")


def empirical_phi(u_years: Sequence[float], recent: Sequence[int], degree: int = 3,
                  grid: np.ndarray | None = None,
                  groups: Sequence | None = None) -> RecencyFunction:
    """
    phi(u) from specimen-level data by logit regression on a polynomial in u.

    With `groups`, fits GEE clustered on the group (participant) with an
    independence working correlation -- the XSRecency procedure. Without
    statsmodels or groups, falls back to unclustered logistic regression, which
    gives the same point estimate and a wrong variance.
    """
    grid = default_grid() if grid is None else np.asarray(grid, float)
    u = np.asarray(u_years, float)
    y = np.asarray(recent, int)
    X = np.column_stack([u ** k for k in range(degree + 1)])

    import statsmodels.api as sm
    if groups is not None:
        fit = sm.GEE(y, X, groups=np.asarray(groups),
                     family=sm.families.Binomial(),
                     cov_struct=sm.cov_struct.Independence()).fit()
    else:
        fit = sm.GLM(y, X, family=sm.families.Binomial()).fit()
    Xg = np.column_stack([grid ** k for k in range(degree + 1)])
    vals = 1.0 / (1.0 + np.exp(-(Xg @ np.asarray(fit.params))))
    return RecencyFunction(grid, vals, "empirical")


# ---------------------------------------------------------------------------
# Generator on living states
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Generator:
    """Sub-generator on living states L, with E first. X is implicit."""

    matrix: np.ndarray
    states: tuple[str, ...]

    def __array__(self, dtype=None, copy=None):
        a = self.matrix
        return a if dtype is None else a.astype(dtype)

    def __getitem__(self, idx):
        return self.matrix[idx]

    @property
    def stationary(self) -> np.ndarray:
        """
        Stationary distribution of the living-state process, ignoring absorption.
        Solves pi' Q_live = 0 with Q_live the generator stripped of exit rates.
        """
        Q = self.matrix.copy()
        np.fill_diagonal(Q, 0.0)
        np.fill_diagonal(Q, -Q.sum(axis=1))          # rebalance: no exit to X
        n = len(self.states)
        A = np.vstack([Q.T, np.ones(n)])
        b = np.zeros(n + 1)
        b[-1] = 1.0
        return np.linalg.lstsq(A, b, rcond=None)[0]


def generator(q: Mapping[str, float],
              betas: Mapping[str, float],
              mus: Mapping[str, float]) -> Generator:
    """
    Build the living-state generator from occupancy, return rates and exit rates.

    Parameters
    ----------
    q      : stationary share of person-time in each unobservable state, e.g.
             {"J": 0.03, "P": 0.05}. Entry rates follow from
             alpha_k = beta_k * q_k / q_E  with  q_E = 1 - sum_k q_k.
             This is the identification used throughout: occupancy and sojourn
             together determine flow, and a long sojourn at fixed occupancy
             implies a SMALL entry rate.
    betas  : return rate to E for each unobservable state (per year).
    mus    : exit rate to X per state, keyed by state name. "E" is required.

    Notes
    -----
    Empty `q` and `betas` give the single-state case L = {E}.
    """
    names = tuple(q.keys())
    states = ("E",) + names
    qE = 1.0 - sum(q.values())
    if qE <= 0:
        raise ValueError(f"occupancies must sum below 1, got {sum(q.values())}")

    n = len(states)
    Q = np.zeros((n, n))
    for i, k in enumerate(names, start=1):
        beta = float(betas[k])
        alpha = beta * float(q[k]) / qE
        Q[0, i] = alpha
        Q[i, 0] = beta
    for i, s in enumerate(states):
        mu = float(mus.get(s, 0.0))
        Q[i, i] = -(Q[i].sum() - Q[i, i] + mu)
    return Generator(Q, states)


def transition(Q, u) -> np.ndarray:
    """P_1(u) = exp(Q u). Scalar u gives a matrix; array u gives a stack."""
    M = np.asarray(Q, float)
    us = np.atleast_1d(np.asarray(u, float))
    out = np.stack([expm(M * x) for x in us])
    return out[0] if np.isscalar(u) or np.ndim(u) == 0 else out


# ---------------------------------------------------------------------------
# Closed forms, for cross-checking the matrix exponential
# ---------------------------------------------------------------------------

def S1_closed(u, alpha: float, beta: float, mu: float, mu_out: float | None = None):
    """
    Two-state closed form for [exp(Q u)]_EE with E <-> O and exits to X.

        a = alpha + mu,  b = beta + mu_out
        x = (-(a+b) +/- sqrt((a-b)^2 + 4 alpha beta)) / 2
        S1(u) = [e^{x1 u}(x1+b) - e^{x2 u}(x2+b)] / (x1 - x2)

    Limits: alpha = 0 gives exp(-mu u); mu = mu_out = 0 gives
    (1-q) + q exp(-(alpha+beta) u) with q = alpha/(alpha+beta).
    """
    mu_out = mu if mu_out is None else mu_out
    u = np.atleast_1d(np.asarray(u, float))
    a, b = alpha + mu, beta + mu_out
    disc = np.sqrt((a - b) ** 2 + 4.0 * alpha * beta)
    x1, x2 = (-(a + b) + disc) / 2.0, (-(a + b) - disc) / 2.0
    if abs(x1 - x2) < 1e-14:
        return np.exp(x1 * u) * (1.0 + (x1 + b) * u)
    return (np.exp(x1 * u) * (x1 + b) - np.exp(x2 * u) * (x2 + b)) / (x1 - x2)


def rho_susceptible(Q0, lam: float = 0.0, stationary: bool = False,
                    t: float = 20.0) -> float:
    """
    rho = d log n_0E / dt for the observable susceptible pool.

    Propagated from all-mass-in-E rather than taken as a dominant eigenvalue,
    which is wrong when an unobservable state is unreachable (alpha = 0) and
    therefore empty. `lam` adds depletion of susceptibles by infection.
    """
    if stationary:
        return 0.0
    M = np.asarray(Q0, float).copy()
    M[0, 0] -= lam
    e0 = np.zeros(M.shape[0]); e0[0] = 1.0
    n1 = e0 @ expm(M * t)
    n2 = e0 @ expm(M * (t + 0.5))
    return float(np.log(n2[0] / n1[0]) / 0.5)


# ---------------------------------------------------------------------------
# Historical observability weight  w_t(u) = s_t(u) g_E(u; t)
# ---------------------------------------------------------------------------

def historical_weight(Q, pi, eta, g_E: Callable[[float], float] | None = None,
                      grid: np.ndarray | None = None, at: float | None = None):
    """
    w_t(u) = s_t(u) * g_E(u; t), the weight entering Theorem 2.

        s_t(u) = sum_k pi_k eta_k [P_1(u)]_kE / pi_E
        g_E(u; t) = n_0E(t-u) / n_0E(t)

    Parameters
    ----------
    Q    : Generator, or array with E at index 0.
    pi   : living-state composition -- dict keyed by state, or array. A callable
           pi(u) is accepted for the general (drifting-composition) case of
           Theorem 2; a constant corresponds to Corollary 0.
    eta  : relative acquisition hazards eta_k = lambda_k / lambda_E, with
           eta_E = 1. eta_k = 0 for unobservable k reproduces the superseded
           restricted model -- see docs/PROVENANCE.md finding 10.
    g_E  : source-evolution factor; defaults to 1 (demographic stationarity).
    at   : if given, return the scalar w_t(at) instead of an array.

    Returns
    -------
    array on `grid`, or a float when `at` is given.

    Note
    ----
    w_t is a WEIGHT, not a transition probability. With eta_k > 1 it may exceed
    one, which is why the boundary condition in Remark 5 is stated as
    Omega_w < Omega_{T*} rather than as pointwise w_t < 1.
    """
    states = Q.states if isinstance(Q, Generator) else None
    M = np.asarray(Q, float)
    n = M.shape[0]

    def as_vec(d, default):
        if callable(d):
            return d
        if isinstance(d, Mapping):
            if states is None:
                raise ValueError("dict input requires a Generator with state names")
            return np.array([float(d.get(s, default)) for s in states])
        return np.asarray(d, float)

    eta_v = as_vec(eta, 0.0)
    pi_v = as_vec(pi, 0.0)
    gfun = (lambda u: 1.0) if g_E is None else g_E

    us = np.array([float(at)]) if at is not None else (
        default_grid() if grid is None else np.asarray(grid, float))

    out = np.empty(len(us))
    for i, u in enumerate(us):
        P = expm(M * u)
        p_E = P[:, 0]                                  # return vector p_E(u)
        pv = np.asarray(pi_v(u) if callable(pi_v) else pi_v, float)
        ev = np.asarray(eta_v(u) if callable(eta_v) else eta_v, float)
        out[i] = float((pv * ev) @ p_E / pv[0] * gfun(u))
    return float(out[0]) if at is not None else out


def omega(phi: RecencyFunction) -> float:
    """Omega_{T*} = int_0^{T*} phi(u) du, in years."""
    return float(np.trapezoid(phi.values, phi.grid))


def plim_ratio(phi: RecencyFunction, w) -> float:
    """
    Theorem 2: plim lambda_hat / lambda_E = int phi w du / Omega_{T*}.

    Equals 1 exactly under the five conditions of Corollary 2.
    """
    w = np.asarray(w, float)
    if w.shape != phi.grid.shape:
        raise ValueError(f"w has shape {w.shape}, expected {phi.grid.shape}; "
                         "pass grid=phi.grid to historical_weight")
    return float(np.trapezoid(phi.values * w, phi.grid) / omega(phi))
