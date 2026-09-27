"""
Figure 3 / Table S3: the (eta_J, eta_P) sensitivity surface.

eta_k = lambda_k / lambda_E is the symmetry-breaking parameter (mechanism M2).
Jail and prison are kept SEPARATE because sojourn length enters independently of
occupancy: at fixed occupancy a 32-day spell relaxes within the recency window
while a 2.7-year spell does not. Collapsing to a common eta would apply a
prison-derived literature bound to the parameter it does not constrain.

Any literature range is OVERLAID, never fitted. Gough et al. 2010 (BMC Public
Health 10:777) give 0.08 vs 1.14-2.78 per 100 PY for continuous incarceration
versus community IVDU -- crude ratios 0.03-0.07, informative about PRISON only.

--sites adds an illustrative site table from data/fixtures/. That is an
illustration that the parameters occupy plausible ranges, not an epidemiologic
claim about any trial.
"""
import argparse, csv
from _common import (banner, phi_for, write_table, FIGURES, THETA_NHBS,
                     C_PURPOSE, MU_PWID, MU_CUSTODY, BETA_JAIL, BETA_PRISON, ROOT)
import numpy as np
from scipy.optimize import brentq
from src.eligibility_dynamics import generator, historical_weight
from src.pan_composition import r_star

GOUGH_PRISON = (0.029, 0.070)


def rstar(phi, qJ, qP, eJ, eP, mu=MU_PWID):
    Q = generator(q={"J": max(qJ, 1e-12), "P": max(qP, 1e-12)},
                  betas={"J": BETA_JAIL, "P": BETA_PRISON},
                  mus={"E": mu, "J": MU_CUSTODY, "P": MU_CUSTODY})
    pi = {"E": 1.0 - qJ - qP, "J": qJ, "P": qP}
    w = historical_weight(Q, pi=pi, eta={"E": 1.0, "J": eJ, "P": eP},
                          grid=phi.grid)
    return r_star(phi, w, theta=THETA_NHBS, c=C_PURPOSE)


def surface(phi, qJ, qP, n=21):
    es = np.linspace(0.0, 1.0, n)
    Z = np.array([[rstar(phi, qJ, qP, eJ, eP) for eP in es] for eJ in es])
    return es, Z


def figure3(phi, qJ=0.03, qP=0.05):
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    es, Z = surface(phi, qJ, qP)
    fig, ax = plt.subplots(figsize=(5.8, 4.8))
    cf = ax.contourf(es, es, Z, levels=14, cmap="RdBu_r",
                     vmin=Z.min(), vmax=max(Z.max(), 2 - Z.min()))
    ax.contour(es, es, Z, levels=[1.0], colors="k", linewidths=2.2)
    ax.axvspan(*GOUGH_PRISON, color="k", alpha=0.10, lw=0)
    ax.text(np.mean(GOUGH_PRISON), 0.97, "Gough\nprison band", fontsize=7,
            ha="center", va="top")
    fig.colorbar(cf, ax=ax, label="$r^\\star$")
    ax.set_xlabel(r"$\eta_P$  (prison)")
    ax.set_ylabel(r"$\eta_J$  (jail)")
    ax.set_title(f"Zero-bias boundary, $q_J$={qJ:.0%}, $q_P$={qP:.0%}\n"
                 "heavy contour: $r^\\star=1$")
    fig.tight_layout()
    FIGURES.mkdir(parents=True, exist_ok=True)
    p = FIGURES / "fig3_eta_surface.png"
    fig.savefig(p, dpi=200); print(f"  wrote {p.name}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sites", action="store_true",
                    help="add illustrative site table from data/fixtures/")
    args = ap.parse_args()

    banner(f"eta surface, theta={THETA_NHBS:.3f}, c={C_PURPOSE}, mu={MU_PWID}")
    phi = phi_for()
    print(f"{'eta (both)':>11}{'r*':>9}{'crosses':>9}   q_J=3%, q_P=5%")
    rows = []
    for e in (0.0, 0.05, 0.25, 0.5, 0.75, 1.0):
        r = rstar(phi, 0.03, 0.05, e, e)
        print(f"{e:>11.2f}{r:>9.3f}{'YES' if r > 1 else 'no':>9}")
        rows.append([f"{e:.2f}", f"{r:.4f}", int(r > 1)])
    write_table(rows, ["eta", "r_star", "crosses"], "tableS3a_eta_common.csv")
    figure3(phi)

    if args.sites:
        src = ROOT / "data" / "fixtures" / "p4_split.csv"
        if not src.exists():
            print(f"  skipping --sites: {src.name} absent"); return
        banner("Illustrative site sensitivity (NOT an epidemiologic claim)")
        out = []
        with src.open() as fh:
            for row in csv.DictReader(fh):
                qJ, qP = float(row["qJ"]), float(row["qP"])
                cells = [rstar(phi, qJ, qP, e, e) for e in (0.0, 0.25, 0.5)]
                try:
                    be = brentq(lambda e: rstar(phi, qJ, qP, e, e) - 1.0, 0.0, 3.0)
                except ValueError:
                    be = float("nan")
                print(f"  {row['site']:<24}" + "".join(f"{v:>8.3f}" for v in cells)
                      + f"   break-even eta {be:.2f}" if be == be
                      else f"  {row['site']:<24}" + "".join(f"{v:>8.3f}" for v in cells)
                      + "   never crosses")
                out.append([row["site"], f"{qJ:.4f}", f"{qP:.4f}",
                            *[f"{v:.4f}" for v in cells],
                            f"{be:.3f}" if be == be else "never"])
        write_table(out, ["site", "q_J", "q_P", "r_eta0", "r_eta0.25",
                          "r_eta0.5", "breakeven_eta"], "tableS3b_eta_sites.csv")


if __name__ == "__main__":
    main()
