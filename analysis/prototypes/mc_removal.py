"""
Analytic LEL vs individual-level Monte Carlo, with post-infection removal s(u) ON.

Simulator follows Pan et al. AJE 2026 Supp S.5:
  Source Eligible Population: constant prevalence p, constant incidence lam
    => Pr(U=u|D=1) flat on [0, Umax], Umax = p / (lam*(1-p))     (their Lemma S.1)
  Testing: equilibrium renewal (Lemma S.3), Poisson intensity theta
  SWP: stop testing after first positive => S_swp = first test AFTER infection if one exists
  Selective attendance: q1 if aware (Delta=1), q0 if not;  r = q1/q0
  Testing-based criterion: keep iff S_swp > c
NEW: infected individuals are observable with relative probability s(u) = exp(-gamma*u).
     HIV-negatives have relative observability 1 (this is the RELATIVE definition).

Estimator (beta = 0):  lam_hat = N_rec / (N_neg * Omega),  Omega = int_0^Tstar phi
Target:                lam_S (Source Eligible Population incidence)
"""
import numpy as np
from scipy import stats

YR, TSTAR = 365.25, 2.0
UG = np.linspace(0.0, TSTAR, 2001)

def gamma_phi_fn(window_d, shadow_d):
    W, H = window_d / YR, shadow_d / YR
    rate = 1.0 / (2 * H - W); shape = W * rate
    return lambda u: np.where(u <= TSTAR, 1 - stats.gamma.cdf(u, shape, scale=1 / rate), 0.0)

def analytic_LEL(phi_fn, r, c, theta, gamma):
    """Pan Supp S.7.1 generalised: log(Om_s - (1 - r e^{theta c}) K_s) - log(Om)."""
    phi = phi_fn(UG); s = np.exp(-gamma * UG)
    Om = np.trapezoid(phi, UG)
    Oms = np.trapezoid(phi * s, UG)
    m = UG >= c
    Ks = np.trapezoid((phi * s * (1 - np.exp(theta * (c - UG))))[m], UG[m])
    return np.log(Oms - (1 - r * np.exp(theta * c)) * Ks) - np.log(Om)

def simulate(phi_fn, r, c, theta, gamma, p=0.121, lam=0.038, n=6_000_000,
             seed=0, stochastic=False):
    rng = np.random.default_rng(seed)
    Umax = p / (lam * (1 - p))
    q0, q1 = 1.0, r

    D = rng.random(n) < p
    ni, nn = int(D.sum()), int((~D).sum())

    # ---- HIV-negatives: S = S_ID from equilibrium renewal; always unaware ----
    S_neg = rng.exponential(1 / theta, nn)
    if stochastic:
        Nneg = float((( S_neg > c) & (rng.random(nn) < q0)).sum())
    else:
        Nneg = q0 * float((S_neg > c).sum())

    # ---- infected: U flat on [0, Umax] (Lemma S.1) ----
    U = rng.uniform(0, Umax, ni)
    S1 = rng.exponential(1 / theta, ni)             # most recent test, regular regime
    aware = S1 < U                                   # a test occurred after infection

    # S_swp = first test AFTER infection = largest test time-since that is <= U.
    # Backward from S1 the gaps are iid Exp(theta); walk back while still <= U.
    S_swp = S1.copy()
    act = np.flatnonzero(aware)
    cur = S1[act].copy()
    while act.size:
        cur = cur + rng.exponential(1 / theta, act.size)
        ok = cur <= U[act]
        act, cur = act[ok], cur[ok]
        if act.size:
            S_swp[act] = cur

    qD = np.where(aware, q1, q0)
    sU = np.exp(-gamma * U)
    passC = S_swp > c
    phiU = phi_fn(U)

    if stochastic:
        inc = (rng.random(ni) < qD * sU) & passC
        Nrec = float((inc & (rng.random(ni) < phiU)).sum())
    else:
        Nrec = float((phiU * sU * qD * passC).sum())

    Om = np.trapezoid(phi_fn(UG), UG)
    return np.log((Nrec / (Nneg * Om)) / lam)

if __name__ == "__main__":
    phi = gamma_phi_fn(101, 194)
    c, p, lam = 0.25, 0.121, 0.038
    print(f"Umax = {p/(lam*(1-p)):.3f} y     phi: gamma window 101 d / shadow 194 d, T* = 2 y\n")
    print(f"{'theta':>6}{'gamma':>7}{'r':>5} | {'analytic LEL':>13}{'MC LEL':>10}{'diff':>9} | "
          f"{'analytic bias':>14}{'MC bias':>10}")
    print("-" * 82)
    for theta in (0.5, 1.0, 2.0):
        for gamma in (0.0, 0.10, 0.20):
            for r in (0.0, 0.6, 1.0):
                a = analytic_LEL(phi, r, c, theta, gamma)
                m = simulate(phi, r, c, theta, gamma, n=6_000_000, seed=hash((theta,gamma,r)) % 2**31)
                print(f"{theta:>6.1f}{gamma:>7.2f}{r:>5.1f} | {a:>13.4f}{m:>10.4f}{m-a:>9.4f} | "
                      f"{1e3*lam*(np.exp(a)-1):>13.2f}{1e3*lam*(np.exp(m)-1):>10.2f}")
        print()
