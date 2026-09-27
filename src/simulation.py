"""
Individual-level simulator, for validating the analytic results against a
generative model built independently of them.

Population construction follows Pan, Bannick & Gao (AJE 2026) Supplement S.5:
constant prevalence and incidence give a flat infection-duration density on
[0, U_max] with U_max = p / (lambda (1-p)); testing histories come from an
equilibrium renewal process (their Lemma S.3); the stop-when-positive regime
determines the observed most-recent test; attendance follows the selective
attendance ratio r; and the testing-based criterion excludes S <= c.

This implementation differs from the prototype in one essential respect: it
admits acquisition in EVERY living state. The state at infection is drawn with
probability proportional to pi_k eta_k, which is exactly the numerator structure
of Theorem 1. Setting eta_k = 0 for unobservable k recovers the superseded
restricted model.

Everything here is generative. Nothing imports the analytic expressions, so the
comparison in tests/ is genuinely between two independent routes.
"""

from __future__ import annotations

import numpy as np
from scipy.linalg import expm

from .eligibility_dynamics import RecencyFunction, T_STAR, omega

__all__ = ["simulate_ratio", "simulate_lel", "SimConfig"]


class SimConfig:
    """Population and design parameters. Defaults follow Pan Supplement S.5."""

    def __init__(self, prevalence: float = 0.121, incidence: float = 0.038,
                 theta: float = 1.0, c: float = 0.25, r: float = 0.0,
                 q0: float = 1.0):
        self.p = float(prevalence)
        self.lam = float(incidence)
        self.theta = float(theta)
        self.c = float(c)
        self.r = float(r)
        self.q0 = float(q0)

    @property
    def u_max(self) -> float:
        """Support of the flat infection-duration density (Pan Lemma S.1)."""
        return self.p / (self.lam * (1.0 - self.p))


def _swp_time_since_test(rng, theta: float, u: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Time since the most recent observed HIV test under stop-when-positive.

    Draws S from the equilibrium backward-recurrence distribution -- Exp(theta)
    for a Poisson process -- then, if a test fell after infection, walks back
    through iid gaps to the FIRST post-infection test, since testing ceases at
    the initial positive.

    Returns (S_swp, aware) where aware indicates a post-infection test occurred.
    """
    n = len(u)
    s1 = rng.exponential(1.0 / theta, n)
    aware = s1 < u
    s = s1.copy()
    idx = np.flatnonzero(aware)
    cur = s1[idx].copy()
    while idx.size:
        cur = cur + rng.exponential(1.0 / theta, idx.size)
        keep = cur <= u[idx]
        idx, cur = idx[keep], cur[keep]
        if idx.size:
            s[idx] = cur
    return s, aware


def _state_at_survey(rng, Q, pi_eta: np.ndarray, u: np.ndarray) -> np.ndarray:
    """
    Sample the living state at survey for individuals infected u ago.

    The state AT INFECTION is drawn with probability proportional to pi_k eta_k
    -- the rate at which infections arise in state k. Evolution to survey uses
    P_1(u) = exp(Q u). Returns True where the individual is observable at t.

    Individuals absorbed into X are not observable; the row-sum deficit of Q
    carries that probability, so it appears as neither E nor any O.
    """
    M = np.asarray(Q, float)
    nstate = M.shape[0]
    w = pi_eta / pi_eta.sum()
    start = rng.choice(nstate, size=len(u), p=w)

    # Bucket by (start state, duration bin) so expm is called O(bins) times, not O(n).
    nbin = 240
    edges = np.linspace(0.0, u.max() + 1e-12, nbin + 1)
    which = np.clip(np.digitize(u, edges) - 1, 0, nbin - 1)
    mid = 0.5 * (edges[:-1] + edges[1:])

    out = np.zeros(len(u), bool)
    draws = rng.random(len(u))
    for b in range(nbin):
        m = which == b
        if not m.any():
            continue
        P = expm(M * mid[b])
        p_obs = np.clip(P[:, 0], 0.0, 1.0)      # probability of being in E
        out[m] = draws[m] < p_obs[start[m]]
    return out


def simulate_ratio(phi: RecencyFunction, Q, pi, eta, n: int = 2_000_000,
                   seed: int = 0, cfg: SimConfig | None = None,
                   screening: bool = False) -> float:
    """
    Monte Carlo estimate of plim lambda_hat / lambda_E.

    With screening=False the sampling is a census of observable individuals and
    the result should converge to Theorem 2's integral. With screening=True the
    attendance and exclusion operators of Pan are applied, and the result
    corresponds to exp(LEL).

    Parameters
    ----------
    Q   : Generator on living states, E first.
    pi  : living-state composition of susceptibles, array or dict.
    eta : relative acquisition hazards, array or dict, eta_E = 1.
    """
    cfg = cfg or SimConfig()
    rng = np.random.default_rng(seed)
    states = getattr(Q, "states", None)

    def vec(d):
        if isinstance(d, dict):
            if states is None:
                raise ValueError("dict input needs a Generator with state names")
            return np.array([float(d.get(s, 0.0)) for s in states])
        return np.asarray(d, float)

    pi_v, eta_v = vec(pi), vec(eta)
    pi_eta = pi_v * eta_v
    if pi_eta.sum() <= 0:
        raise ValueError("pi * eta is identically zero: no infections can arise")

    n_inf = rng.binomial(n, cfg.p)
    n_neg = n - n_inf

    # --- infected -------------------------------------------------------
    u = rng.uniform(0.0, cfg.u_max, n_inf)
    obs = _state_at_survey(rng, Q, pi_eta, u)
    s_swp, aware = _swp_time_since_test(rng, cfg.theta, u)
    keep = obs & (s_swp > cfg.c) if screening else obs
    weight = np.where(aware, cfg.r, 1.0) * cfg.q0 if screening else 1.0
    n_rec = float(np.sum(phi(u[keep]) * (weight[keep] if screening else 1.0)))

    # --- susceptibles ---------------------------------------------------
    obs_neg = rng.random(n_neg) < pi_v[0] / pi_v.sum()
    if screening:
        s_neg = rng.exponential(1.0 / cfg.theta, n_neg)
        obs_neg &= (s_neg > cfg.c)
        denom = obs_neg.sum() * cfg.q0
    else:
        denom = obs_neg.sum()

    lam_hat = n_rec / (denom * omega(phi))

    # cfg.lam is the TOTAL incidence across all susceptibles, which is what the
    # flat-duration construction generates. The estimand is lambda_E, the hazard
    # in state E. Total infection flow is N_neg * lambda_E * sum_k pi_k eta_k, so
    #
    #       lambda_E = lambda / (sum_k pi_k eta_k / sum_k pi_k).
    #
    # Omitting this converts every state-invariance departure into an apparent
    # disagreement with Theorem 2, because sum_k pi_k eta_k differs from one
    # exactly when eta is not identically one.
    lam_E = cfg.lam / (pi_eta.sum() / pi_v.sum())
    return float(lam_hat / lam_E)


def simulate_lel(phi: RecencyFunction, Q, pi, eta, r: float, c: float,
                 theta: float, n: int = 2_000_000, seed: int = 0,
                 cfg: SimConfig | None = None) -> float:
    """log of the simulated bias ratio, comparable to pan_composition.lel."""
    cfg = cfg or SimConfig()
    cfg.r, cfg.c, cfg.theta = float(r), float(c), float(theta)
    return float(np.log(simulate_ratio(phi, Q, pi, eta, n=n, seed=seed,
                                       cfg=cfg, screening=True)))
