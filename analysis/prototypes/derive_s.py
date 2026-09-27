"""
Derivation of s(u) from population dynamics, with numerical verification.

States:  E  observable (alive, in catchment, reachable at screening)
         O  temporarily unobservable (custody, displacement, hospitalisation)  E <-> O
         X  permanently gone (death, permanent out-migration)                  absorbing

Rates (per year):  E->O = alpha,  O->E = beta,  E->X = mu,  O->X = mu'
Subscript 1 = HIV-infected, 0 = HIV-negative.

S_1(u) = P(in E at t | in E at t-u, infected at t-u) = [exp(M u)]_EE
with M the 2x2 sub-generator on {E,O}.
"""
import numpy as np
from scipy.linalg import expm

def S_closed(u, alpha, beta, mu, mup):
    """Closed form for [exp(Mu)]_EE, M = [[-(alpha+mu), alpha],[beta, -(beta+mup)]]."""
    u = np.atleast_1d(np.asarray(u, float))
    a, b = alpha + mu, beta + mup
    disc = np.sqrt((a - b) ** 2 + 4 * alpha * beta)
    x1, x2 = (-(a + b) + disc) / 2, (-(a + b) - disc) / 2
    if abs(x1 - x2) < 1e-14:
        return np.exp(x1 * u) * (1 + (x1 + b) * u)          # degenerate case
    return (np.exp(x1 * u) * (x1 + b) - np.exp(x2 * u) * (x2 + b)) / (x1 - x2)

def S_numeric(u, alpha, beta, mu, mup):
    M = np.array([[-(alpha + mu), alpha], [beta, -(beta + mup)]])
    return np.array([expm(M * x)[0, 0] for x in np.atleast_1d(u)])

if __name__ == "__main__":
    u = np.array([0.0, 0.25, 0.5, 1.0, 2.0])
    print("1. Closed form vs matrix exponential\n")
    for lab, pr in [("absorbing only  (a=0,b=0,mu=.05)", (0.0, 0.0, 0.05, 0.05)),
                    ("transient only  (a=.5,b=12,mu=0)", (0.5, 12.0, 0.0, 0.0)),
                    ("mixed           (a=.5,b=12,mu=.03,mu'=.06)", (0.5, 12.0, 0.03, 0.06)),
                    ("long sojourn    (a=.3,b=.33,mu=.02)", (0.3, 1/3, 0.02, 0.02))]:
        c, n = S_closed(u, *pr), S_numeric(u, *pr)
        print(f"  {lab:<44} max|diff| = {np.abs(c-n).max():.2e}")

    print("\n2. Limiting forms\n")
    mu = 0.05
    print(f"  absorbing only:  S_1(u) = exp(-mu u).   check at u=2: "
          f"{S_closed(2.0,0,0,mu,mu)[0]:.6f} vs {np.exp(-mu*2):.6f}")
    a, b = 0.5, 12.0
    q = a / (a + b)
    S_t = lambda x: (b + a*np.exp(-(a+b)*x)) / (a+b)
    print(f"  transient only:  S_1(u) = (1-q) + q e^-(a+b)u,  q = a/(a+b) = {q:.4f}")
    print(f"                   check at u=2: {S_closed(2.0,a,b,0,0)[0]:.6f} vs {S_t(2.0):.6f}")
    print(f"                   floor S_1(inf) = 1-q = {1-q:.4f};  relaxation rate a+b = {a+b:.2f}/yr"
          f"  (halflife {np.log(2)/(a+b)*365:.0f} d)")


# ----------------------------------------------------------------------------
# The full observability function.
#
#   N_rec = INT lambda * n0_E(t-u) * S_1(u) * phi(u) du ,   N_neg = n0_E(t)
#   =>  lam_hat / lam = INT phi(u) s(u) du / INT phi(u) du
#   with
#         s(u) = S_1(u) * n0_E(t-u)/n0_E(t) = S_1(u) * exp(-rho*u)
#
#   rho = d log n0_E / dt, the exponential growth rate of the OBSERVABLE
#   susceptible pool. It is NOT 1/S_0(u): the O compartment feeds back into E,
#   and infection itself depletes the susceptibles.
# ----------------------------------------------------------------------------

def rho_susceptible(alpha0, beta0, mu0, lam, stationary=False, t=20.0):
    """d log n0_E/dt, propagated from n=(1,0). Handles an unreachable O state."""
    if stationary:
        return 0.0
    M = np.array([[-(alpha0 + mu0 + lam), alpha0], [beta0, -(beta0 + mu0)]])
    e0 = np.array([1.0, 0.0])
    n1, n2 = e0 @ expm(M * t), e0 @ expm(M * (t + 0.5))
    return float(np.log(n2[0] / n1[0]) / 0.5)

def s_of_u(u, infected, susceptible, lam, stationary=False):
    """infected/susceptible = dicts with keys alpha, beta, mu (per year)."""
    S1 = S_closed(u, infected["alpha"], infected["beta"], infected["mu"], infected["mu"])
    rho = rho_susceptible(susceptible["alpha"], susceptible["beta"], susceptible["mu"],
                          lam, stationary=stationary)
    return S1 * np.exp(-rho * np.asarray(u, float))
