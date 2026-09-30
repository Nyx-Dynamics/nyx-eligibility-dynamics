"""
Figures 1-2: the observability weight by mechanism, and cancellation across
occupancy and sojourn.

Demonstrates Corollaries 2, 4 and 5. Figure 2 is the visual form of the paper's
central result: the cancellation holds regardless of how much person-time is
spent unobservable or how long each spell lasts.
"""
from _common import (banner, phi_for, FIGURES, BETA_JAIL, BETA_PRISON,
                     MU_PWID, MU_CUSTODY)
import numpy as np
from src.eligibility_dynamics import generator, historical_weight, plim_ratio

TOL = 1e-10


def _w(phi, q, betas, mus, eta, g_E=None):
    Q = generator(q=q, betas=betas, mus=mus)
    pi = {"E": 1.0 - sum(q.values()), **q}
    return historical_weight(Q, pi=pi, eta=eta, g_E=g_E, grid=phi.grid)


def figure1(phi):
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    cases = [
        ("absorbing only, mu=0.04", {}, {}, {"E": MU_PWID}, {"E": 1.0}),
        ("transient only, q=8%, eta=1",
         {"O": 0.08}, {"O": BETA_JAIL}, {"E": 0.0, "O": 0.0},
         {"E": 1.0, "O": 1.0}),
        ("transient only, q=8%, eta=0",
         {"O": 0.08}, {"O": BETA_JAIL}, {"E": 0.0, "O": 0.0},
         {"E": 1.0, "O": 0.0}),
        ("mixed: mu=0.04, q=8%, eta=0.3",
         {"O": 0.08}, {"O": BETA_JAIL}, {"E": MU_PWID, "O": MU_CUSTODY},
         {"E": 1.0, "O": 0.3}),
    ]
    for label, q, b, m, e in cases:
        ax.plot(phi.grid, _w(phi, q, b, m, e), lw=1.8, label=label)
    ax.axhline(1.0, color="k", lw=0.7, ls=":")
    ax.set_xlabel("infection duration $u$ (years)")
    ax.set_ylabel("$w_t(u)$")
    ax.set_title("Historical observability weight by mechanism")
    ax.legend(fontsize=8, frameon=False)
    fig.tight_layout()
    p = FIGURES / "fig1_weight_by_mechanism.png"
    fig.savefig(p, dpi=200)
    fig.savefig(p.with_suffix(".pdf"))
    print(f"  wrote {p.name} and {p.with_suffix('.pdf').name}")


def figure2(phi):
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    qs = np.linspace(0.005, 0.30, 24)
    sojourns = [7, 32, 180, 365 * 2.7]
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    for sd in sojourns:
        beta = 365.25 / sd
        vals = [plim_ratio(phi, _w(phi, {"O": q}, {"O": beta},
                                   {"E": 0.0, "O": 0.0}, {"E": 1.0, "O": 1.0}))
                for q in qs]
        ax.plot(qs * 100, vals, lw=1.6, label=f"mean sojourn {sd:.0f} d")
        assert max(abs(v - 1.0) for v in vals) < TOL, "cancellation violated"
    ax.axhline(1.0, color="k", lw=0.7, ls=":")
    ax.set_ylim(0.9, 1.1)
    ax.set_xlabel("person-time unobservable, $q$ (%)")
    ax.set_ylabel(r"plim $\hat\lambda/\lambda_E$")
    ax.set_title("Exact cancellation: invariant to occupancy and sojourn")
    ax.legend(fontsize=8, frameon=False)
    fig.tight_layout()
    p = FIGURES / "fig2_cancellation.png"
    fig.savefig(p, dpi=200)
    fig.savefig(p.with_suffix(".pdf"))
    print(f"  wrote {p.name} and {p.with_suffix('.pdf').name}")


def main():
    banner("Theorem validation figures")
    phi = phi_for()
    w = _w(phi, {"J": 0.03, "P": 0.05}, {"J": BETA_JAIL, "P": BETA_PRISON},
           {"E": 0.0, "J": 0.0, "P": 0.0}, {"E": 1.0, "J": 1.0, "P": 1.0})
    dev = abs(plim_ratio(phi, w) - 1.0)
    print(f"  Corollary 2, jail+prison, eta=1: deviation {dev:.2e}")
    assert dev < TOL
    figure1(phi); figure2(phi)


if __name__ == "__main__":
    main()
