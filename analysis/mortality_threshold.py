"""
Absorbing loss: attenuation, and the rate at which the zero-bias boundary
reaches unity.

Corollary 4. Mortality is the only mechanism with no compensating return flow,
so it cannot cancel -- but at sourced rates it does NOT move the boundary
either, which is the discipline the paper must keep (see K.1 of the audit
record). Do not substitute "mortality drives the crossing" for the withdrawn
"incarceration drives the crossing".
"""
from _common import banner, phi_for, write_table, THETA_NHBS, C_PURPOSE, MU_PWID
import numpy as np
from scipy.optimize import brentq
from src.eligibility_dynamics import generator, historical_weight, plim_ratio
from src.pan_composition import r_star


def absorbing_w(phi, mu):
    Q = generator(q={}, betas={}, mus={"E": float(mu)})
    return historical_weight(Q, pi={"E": 1.0}, eta={"E": 1.0}, grid=phi.grid)


def mu_crit(phi, theta=THETA_NHBS, c=C_PURPOSE, hi=1.0) -> float:
    """Mortality rate at which r*(mu) = 1."""
    f = lambda m: r_star(phi, absorbing_w(phi, m), theta=theta, c=c) - 1.0
    return float(brentq(f, 1e-4, hi))


def main():
    banner(f"Absorbing loss, theta = {THETA_NHBS:.3f}/yr, c = {C_PURPOSE}")
    phi = phi_for()
    rows = []
    print(f"{'mu (/yr)':>10}{'Omega_mu/Omega':>16}{'r*':>9}{'crosses':>9}")
    for mu in (0.0, 0.01, 0.02, MU_PWID, 0.06, 0.085, 0.10, 0.15, 0.20):
        w = absorbing_w(phi, mu)
        d, r = plim_ratio(phi, w), r_star(phi, w, theta=THETA_NHBS, c=C_PURPOSE)
        print(f"{mu:>10.3f}{d:>16.4f}{r:>9.3f}{'YES' if r > 1 else 'no':>9}")
        rows.append([f"{mu:.4f}", f"{d:.4f}", f"{r:.4f}", int(r > 1)])
    mc = mu_crit(phi)
    print(f"\n  r* = 1 at mu_crit = {mc:.4f}/yr  ({100*(1-np.exp(-mc)):.1f}% annual loss)")
    print(f"  sourced PWID mu = {MU_PWID:.3f}  ->  ratio {mc/MU_PWID:.1f}x")
    print(f"  attenuation at sourced mu: {1-plim_ratio(phi, absorbing_w(phi, MU_PWID)):.2%}")
    write_table(rows, ["mu_per_yr", "omega_ratio", "r_star", "crosses"],
                "table2_mortality_threshold.csv")


if __name__ == "__main__":
    main()
