"""
Composition with the screening-stage selection of Pan, Bannick & Gao
(Am J Epidemiol 2026, doi:10.1093/aje/kwag075).

Their operators -- attendance Q and testing-based eligibility C -- act on
individuals already present in the source population at t, hence DOWNSTREAM of
the transition process in src.eligibility_dynamics. Section 2.7 of the
manuscript composes the stages; this module implements the composed limiting
estimation error.

Setting w == 1 recovers their Supplement S.7.1 expression exactly.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import brentq

from .eligibility_dynamics import RecencyFunction, omega

__all__ = ["omega_w", "K_w", "lel", "r_star", "boundary_no_dynamics"]


def omega_w(phi: RecencyFunction, w) -> float:
    """Omega_w = int_0^{T*} phi(u) w(u) du."""
    return float(np.trapezoid(phi.values * np.asarray(w, float), phi.grid))


def K_w(phi: RecencyFunction, w, c: float, theta: float) -> float:
    """K_w = int_c^{T*} phi(u) w(u) [1 - e^{theta(c-u)}] du."""
    u = phi.grid
    m = u >= c
    integ = phi.values * np.asarray(w, float) * (1.0 - np.exp(theta * (c - u)))
    return float(np.trapezoid(integ[m], u[m]))


def lel(phi: RecencyFunction, w, r: float, c: float, theta: float) -> float:
    """
    Limiting estimation error on the log scale.

        LEL = log[ Omega_w - (1 - r e^{theta c}) K_w ] - log Omega_{T*}

    Parameters
    ----------
    w     : historical observability weight on phi.grid. Pass ones to recover Pan.
    r     : selective attendance ratio q_1 / q_0.
    c     : testing-based exclusion cutoff, years (PURPOSE: 0.25).
    theta : background HIV testing rate, per year, Poisson inter-test.
    """
    inner = omega_w(phi, w) - (1.0 - r * np.exp(theta * c)) * K_w(phi, w, c, theta)
    if inner <= 0:
        raise ValueError(f"non-positive argument to log ({inner:.4g}); "
                         "r is far outside the admissible range")
    return float(np.log(inner) - np.log(omega(phi)))


class InertExclusion(ValueError):
    """Raised when K_w == 0, so the testing-based criterion induces no bias."""


def r_star(phi: RecencyFunction, w, theta: float, c: float,
           hi: float = 80.0, k_tol: float = 1e-12) -> float:
    """
    Zero-bias boundary: the attendance ratio at which LEL = 0.

    With w == 1 this equals exp(-theta c) exactly and is FREE OF phi -- the
    recency function governs the magnitude of bias away from the boundary, not
    its location (manuscript Remark 5). Eligibility dynamics move it to

        r*_w = e^{-theta c} [1 + (Omega_{T*} - Omega_w) / K_w].

    Raises
    ------
    InertExclusion
        When K_w <= k_tol. This happens when phi has no support beyond c -- if
        the recency window closes before the exclusion cutoff, the criterion
        removes nobody who could have tested recent, LEL is identically zero for
        every r, and no boundary exists. Returning a root here would be
        meaningless, so it is refused rather than reported.
    """
    K = K_w(phi, w, c, theta)
    if abs(K) <= k_tol:
        raise InertExclusion(
            f"K_w = {K:.3g} at c = {c}: phi has no support beyond the exclusion "
            "cutoff, so the criterion is inert and r* is undefined")

    def f(r):
        try:
            return lel(phi, w, r=r, c=c, theta=theta)
        except ValueError:
            return -np.inf
    return float(brentq(f, 0.0, hi))


def boundary_no_dynamics(theta: float, c: float) -> float:
    """exp(-theta c): the boundary when w == 1. Closed form, no phi required."""
    return float(np.exp(-theta * c))
