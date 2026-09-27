"""
Table 3: Corollary 3 -- cancellation under arbitrary stationary mixtures.

Carceral contact is recurrent and concentrated, so a homogeneous Markov model is
an obvious target for objection. The corollary answers it: cancellation holds
per stratum, so any mixture of stationary strata inherits it, and the marginal
movement process need not be Markov. Aggregation is over numerators and
denominators separately, as the estimator does it.
"""
from _common import (banner, phi_for, write_table, BETA_JAIL, BETA_PRISON,
                     MU_PWID, MU_CUSTODY)
import numpy as np
from src.eligibility_dynamics import generator, historical_weight, omega

Q_MEAN = {"J": 0.03, "P": 0.05}
BETAS = {"J": BETA_JAIL, "P": BETA_PRISON}


def build(weights, multipliers):
    """Strata preserving the population-mean occupancy. None = residual class."""
    out, k = [], len(weights)
    resid_idx = [i for i, m in enumerate(multipliers) if m is None]
    fixed = [(w, m) for w, m in zip(weights, multipliers) if m is not None]
    q_res = {}
    for s, qm in Q_MEAN.items():
        used = sum(w * m * qm for w, m in fixed)
        wr = sum(weights[i] for i in resid_idx)
        q_res[s] = (qm - used) / wr if wr else 0.0
        if q_res[s] < 0:
            raise ValueError("infeasible mixture: residual occupancy negative")
    for i in range(k):
        m = multipliers[i]
        q = {s: (q_res[s] if m is None else m * Q_MEAN[s]) for s in Q_MEAN}
        if sum(q.values()) >= 0.95:
            raise ValueError("infeasible mixture: occupancy too high")
        out.append((weights[i], q))
    return out


def aggregate(phi, strata, eta, mus, lam=1.0):
    num = den = 0.0
    for wz, q in strata:
        Q = generator(q=q, betas=BETAS, mus=mus)
        pi = {"E": 1.0 - sum(q.values()), **q}
        w = historical_weight(Q, pi=pi, eta=eta, grid=phi.grid)
        num += wz * pi["E"] * lam * np.trapezoid(phi.values * w, phi.grid)
        den += wz * pi["E"]
    return num / (den * omega(phi))


def main():
    banner("Frailty mixtures (Corollary 3)")
    phi = phi_for()
    cases = [("homogeneous", [1.0], [1.0]),
             ("20% at 3x mean", [0.2, 0.8], [3.0, None]),
             ("10% at 6x mean", [0.1, 0.9], [6.0, None]),
             ("5%/15%/80% at 8x/2x/resid", [0.05, 0.15, 0.80], [8.0, 2.0, None])]
    eta1 = {"E": 1.0, "J": 1.0, "P": 1.0}
    eta0 = {"E": 1.0, "J": 0.0, "P": 0.0}
    nomu = {"E": 0.0, "J": 0.0, "P": 0.0}
    withmu = {"E": MU_PWID, "J": MU_CUSTODY, "P": MU_CUSTODY}
    rows = []
    print(f"{'mixture':<30}{'cancel(eta=1,mu=0)':>21}{'eta=0,mu':>11}{'eta=1,mu':>11}")
    for label, ws, ms in cases:
        try:
            st = build(ws, ms)
        except ValueError as e:
            print(f"{label:<30}  infeasible: {e}"); continue
        a = aggregate(phi, st, eta1, nomu)
        b = aggregate(phi, st, eta0, withmu)
        c = aggregate(phi, st, eta1, withmu)
        print(f"{label:<30}{a:>21.8f}{b:>11.4f}{c:>11.4f}")
        rows.append([label, f"{a:.9f}", f"{b:.4f}", f"{c:.4f}"])
        assert abs(a - 1.0) < 1e-6, f"cancellation failed for {label}"
    print("\n  Cancellation holds per stratum, so mixtures inherit it.")
    write_table(rows, ["mixture", "cancellation", "eta0_with_mu", "eta1_with_mu"],
                "table3_frailty_mixture.csv")


if __name__ == "__main__":
    main()
