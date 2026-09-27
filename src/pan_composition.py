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


# ---------------------------------------------------------------------------
# General inter-test processes
# ---------------------------------------------------------------------------
#
# Everything above assumes a POISSON inter-test process, under which the
# zero-bias boundary is exactly e^{-theta c} and exactly free of phi. Pan's
# Supplement S.6 also treats a uniform inter-test variant, where neither holds.
# Distinguishing an assay recency BASIS from an inter-test PROCESS is the error
# that set the predecessor manuscript's sign, so the uniform case is implemented
# rather than asserted.
#
# For an equilibrium renewal testing process with gap CDF F and mean m, the
# equilibrium (forward = backward) recurrence CDF is
#
#       F_e(v) = int_0^v (1 - F(x)) / m dx.
#
# Under stop-when-positive with infection u ago, write V for the forward
# recurrence time from the infection epoch. Then
#
#   aware and S_swp > c   <=>  V < u - c      probability F_e((u-c)_+)
#   not aware and S > c   <=>  no test in (t-c, t) when u <= c, probability P_0;
#                              V >= u when u > c,   probability 1 - F_e(u)
#
# so the kept mass per unit q_0 is
#
#       kept(u) = r F_e((u-c)_+) + tail(u),   P_0 = 1 - F_e(c),
#
# and LEL = log[ int phi w kept / P_0 ] - log Omega_{T*}. For u <= c the
# not-aware term is P_0 exactly, with no u dependence -- the event is simply
# "no test in the last c", which is why the Poisson case collapses to e^{-theta c}.

__all__ += ["InterTestProcess", "PoissonInterTest", "UniformInterTest",
            "lel_general", "r_star_general"]


class InterTestProcess:
    """Equilibrium renewal testing process. Subclasses supply F_e."""

    def F_e(self, v):
        raise NotImplementedError

    def P0(self, c: float) -> float:
        """Pr(S > c) for an HIV-negative attendee: the denominator inclusion."""
        return float(1.0 - self.F_e(np.atleast_1d(float(c)))[0])

    def kept_parts(self, u, c: float):
        """(coefficient on r, tail) evaluated on the duration grid u."""
        u = np.asarray(u, float)
        on_r = self.F_e(np.maximum(u - c, 0.0))
        tail = np.where(u <= c, self.P0(c), 1.0 - self.F_e(u))
        return on_r, tail


class PoissonInterTest(InterTestProcess):
    """Exponential gaps at rate theta. F_e = F: memorylessness."""

    def __init__(self, theta: float):
        self.theta = float(theta)

    def F_e(self, v):
        return 1.0 - np.exp(-self.theta * np.asarray(v, float))


class UniformInterTest(InterTestProcess):
    """
    Gaps Uniform[0, b] (Pan Supplement S.6). Mean gap b/2, so the comparable
    Poisson rate is theta = 2/b.

    1 - F_e(v) = (1 - v/b)^2, hence P_0 = (1 - c/b)^2 -- the closed form Pan
    reports. Note r* != P_0 here: the identity r* = Pr(S>c) is Poisson-specific.
    """

    def __init__(self, b: float):
        self.b = float(b)

    @property
    def theta_equivalent(self) -> float:
        return 2.0 / self.b

    def F_e(self, v):
        v = np.clip(np.asarray(v, float), 0.0, self.b)
        return 1.0 - (1.0 - v / self.b) ** 2


def lel_general(phi: RecencyFunction, w, r: float, c: float,
                process: InterTestProcess) -> float:
    """
    LEL for an arbitrary equilibrium renewal inter-test process.

    With `process=PoissonInterTest(theta)` this reproduces `lel(...)` to
    quadrature error; that equality is the internal check on the derivation.
    """
    on_r, tail = process.kept_parts(phi.grid, c)
    wv = np.asarray(w, float)
    num = float(np.trapezoid(phi.values * wv * (r * on_r + tail), phi.grid))
    inner = num / process.P0(c)
    if inner <= 0:
        raise ValueError(f"non-positive argument to log ({inner:.4g})")
    return float(np.log(inner) - np.log(omega(phi)))


def r_star_general(phi: RecencyFunction, w, c: float,
                   process: InterTestProcess, k_tol: float = 1e-12) -> float:
    """
    Zero-bias boundary for an arbitrary inter-test process. Closed form:

        r* = [ P_0 Omega_{T*} - int phi w tail ] / int phi w F_e((u-c)_+)

    since the kept mass is affine in r. No root-finding required.
    """
    on_r, tail = process.kept_parts(phi.grid, c)
    wv = np.asarray(w, float)
    denom = float(np.trapezoid(phi.values * wv * on_r, phi.grid))
    if abs(denom) <= k_tol:
        raise InertExclusion(
            f"int phi w F_e((u-c)+) = {denom:.3g}: phi has no support beyond "
            f"c = {c}, so the criterion is inert and r* is undefined")
    lhs = process.P0(c) * omega(phi)
    rhs = float(np.trapezoid(phi.values * wv * tail, phi.grid))
    return (lhs - rhs) / denom
