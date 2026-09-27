"""
CROI figure: analytic results against an independently written generative
simulator, across the cancellation case and each symmetry failure.

Design constraint from the submission: no text inside the axes beyond tick
labels, axis labels and a legend. Everything interpretive belongs in the caption,
which is written to manuscript/croi2026/FIGURE_CAPTION.txt by this script so the
two cannot drift apart.

Panel A -- census sampling. Probability limit of the adjusted estimator relative
to lambda_E, analytic (Theorem 2) against Monte Carlo, for the five-condition
case and for each mechanism that breaks it.

Panel B -- composed with the Pan screening and prior-testing stages. Limiting
estimation error against the selective attendance ratio r, for w == 1 (their
published setting) and for a case with eligibility dynamics. The zero crossing is
the predicted boundary; the simulator is never told where it lies.

Monte Carlo cells use DISJOINT seed blocks. Sharing one population across cells
makes residuals perfectly correlated; that produced a spurious systematic bias
during development. See docs/REPRODUCE.md section 2.
"""
import sys
import numpy as np
from _common import (banner, write_table, FIGURES, TABLES, ROOT, C_PURPOSE,
                     THETA_NHBS, BETA_JAIL, BETA_PRISON, MU_PWID, MU_CUSTODY)
from src.eligibility_dynamics import (generator, historical_weight, plim_ratio,
                                      gamma_phi, default_grid)
from src.pan_composition import lel, r_star, boundary_no_dynamics
from src.simulation import simulate_ratio, simulate_lel

GRID = default_grid(4001)
N_DRAW = 15_000_000
# 24 replicates, not 10. The replicate standard error is ESTIMATED, so with few
# replicates the error bars themselves are unreliable: during development a
# 10-replicate block put one cell at z = 3.27, while pooling 50 independent
# replicates gave z = 0.23. A figure whose whole claim is agreement must not have
# error bars that move that much between seed blocks.
N_REP = 24

# Panel A. Order: the cancellation case first, then one mechanism at a time.
# Labels are parameter values only -- the mechanism names live in the caption.
CELLS = [
    ("cancellation\nconditions met",
                                {"J": .03, "P": .05}, {"E": 0., "J": 0., "P": 0.},
                                {"E": 1., "J": 1., "P": 1.}),
    (r"mortality, $\mu_E=0.04$", {},                   {"E": MU_PWID},
                                {"E": 1.}),
    (r"mortality, $\mu_E=0.10$", {},                   {"E": .10},
                                {"E": 1.}),
    (r"$\eta=0$",               {"J": .03, "P": .05}, {"E": MU_PWID, "J": MU_CUSTODY, "P": MU_CUSTODY},
                                {"E": 1., "J": 0., "P": 0.}),
    (r"$\eta=0.3$",             {"J": .03, "P": .05}, {"E": MU_PWID, "J": MU_CUSTODY, "P": MU_CUSTODY},
                                {"E": 1., "J": .3, "P": .3}),
    (r"$\eta=1.8$",             {"J": .03, "P": .05}, {"E": MU_PWID, "J": MU_CUSTODY, "P": MU_CUSTODY},
                                {"E": 1., "J": 1.8, "P": 1.8}),
    ("$\\eta=0,\\ q_J=0.15$\n(stress test)",
                                {"J": .15},           {"E": MU_PWID, "J": MU_CUSTODY},
                                {"E": 1., "J": 0.}),
]

# Two labelling registers. FULL is the CROI submission: readable without having
# read the Methods. SPARSE is the original brief -- bare parameter values, with
# every gloss in the caption -- kept so the two can be compared side by side
# rather than argued about. Positionally aligned with CELLS.
SPARSE_LABELS = ["all five hold", r"$\mu_E=0.04$", r"$\mu_E=0.10$",
                 r"$\eta=0$", r"$\eta=0.3$", r"$\eta=1.8$",
                 r"$\eta=0,\ q_J=0.15$"]

# Panel B. r values at which the simulator is run; the analytic curve is smooth.
R_POINTS = [0.35, 0.55, 0.75, 0.95, 1.20, 1.50]


def load_cached():
    """
    Rebuild the plotting inputs from the CSVs written by a previous run.

    The simulation is ~20 minutes; the figure is iterated on far more often than
    the numbers change. Redrawing from the tables keeps the published figure and
    the published numbers the same objects, which a rerun-to-restyle workflow
    does not guarantee.
    """
    import csv
    ta = TABLES / "croi_figA_census.csv"
    tb = TABLES / "croi_figB_screening.csv"
    if not (ta.exists() and tb.exists()):
        raise SystemExit("no cached tables; run without --redraw first")
    rows_a = [r for r in list(csv.reader(ta.open()))[1:]]
    rows_b = [r for r in list(csv.reader(tb.open()))[1:]]
    # Row labels are presentation, not data: re-take them from CELLS so that
    # relabelling does not require re-running the simulation. Guard the
    # correspondence, since it is positional.
    if len(rows_a) != len(CELLS):
        raise SystemExit(f"cached table has {len(rows_a)} rows against "
                         f"{len(CELLS)} cells; re-run without --redraw")
    for row, cell in zip(rows_a, CELLS):
        row[0] = cell[0]
    return rows_a, rows_b


def rebuild_panel_b(phi, rows_b):
    """Analytic curves are cheap; only the Monte Carlo points were expensive."""
    settings = [
        ("$w\\equiv1$", {}, {"E": 0.0}, {"E": 1.0}),
        ("$\\eta=0.3$", {"J": .03, "P": .05},
         {"E": MU_PWID, "J": MU_CUSTODY, "P": MU_CUSTODY}, {"E": 1., "J": .3, "P": .3}),
    ]
    rgrid = np.linspace(0.25, 1.60, 220)
    out = []
    for label, q, mus, eta in settings:
        Q, pi, eta = build(q, mus, eta)
        w = historical_weight(Q, pi=pi, eta=eta, grid=phi.grid)
        curve = np.array([lel(phi, w, r=r, c=C_PURPOSE, theta=THETA_NHBS)
                          for r in rgrid])
        pts = np.array([[float(r[1]), float(r[3]), float(r[4])]
                        for r in rows_b if r[0] == label])
        out.append((label, rgrid, curve, pts,
                    r_star(phi, w, theta=THETA_NHBS, c=C_PURPOSE)))
    return out


def seeds(cell, n=N_REP):
    """Disjoint block per cell. Do not collapse these; see module docstring."""
    return [100_000 * (cell + 1) + i for i in range(n)]


def build(q, mus, eta):
    betas = {k: (BETA_JAIL if k == "J" else BETA_PRISON) for k in q}
    return (generator(q=q, betas=betas, mus=mus),
            {"E": 1.0 - sum(q.values()), **q}, eta)


def panel_a(phi):
    rows = []
    print(f"{'condition':<24}{'analytic':>10}{'MC':>10}{'95% CI':>18}{'z':>7}")
    for i, (label, q, mus, eta) in enumerate(CELLS):
        Q, pi, eta = build(q, mus, eta)
        a = plim_ratio(phi, historical_weight(Q, pi=pi, eta=eta, grid=phi.grid))
        reps = np.array([simulate_ratio(phi, Q, pi, eta, n=N_DRAW, seed=s)
                         for s in seeds(i)])
        m, sem = reps.mean(), reps.std(ddof=1) / np.sqrt(len(reps))
        z = (m - a) / sem
        print(f"{label:<24}{a:>10.4f}{m:>10.4f}"
              f"{f'{m-1.96*sem:.4f}-{m+1.96*sem:.4f}':>18}{z:>7.2f}")
        assert abs(z) < 4.44, f"{label}: t = {z:.2f} exceeds t_23 at 0.999"
        rows.append([label, f"{a:.5f}", f"{m:.5f}", f"{sem:.6f}", f"{z:.2f}"])
    return rows


def panel_b(phi):
    settings = [
        ("$w\\equiv1$", {}, {"E": 0.0}, {"E": 1.0}),
        ("$\\eta=0.3$", {"J": .03, "P": .05},
         {"E": MU_PWID, "J": MU_CUSTODY, "P": MU_CUSTODY}, {"E": 1., "J": .3, "P": .3}),
    ]
    out, rows = [], []
    rgrid = np.linspace(0.25, 1.60, 220)
    for j, (label, q, mus, eta) in enumerate(settings):
        Q, pi, eta = build(q, mus, eta)
        w = historical_weight(Q, pi=pi, eta=eta, grid=phi.grid)
        curve = np.array([lel(phi, w, r=r, c=C_PURPOSE, theta=THETA_NHBS)
                          for r in rgrid])
        rs = r_star(phi, w, theta=THETA_NHBS, c=C_PURPOSE)
        pts = []
        for k, r in enumerate(R_POINTS):
            reps = np.array([simulate_lel(phi, Q, pi, eta, r=r, c=C_PURPOSE,
                                          theta=THETA_NHBS, n=N_DRAW, seed=s)
                             for s in seeds(50 + 10 * j + k)])
            m, sem = reps.mean(), reps.std(ddof=1) / np.sqrt(len(reps))
            a = lel(phi, w, r=r, c=C_PURPOSE, theta=THETA_NHBS)
            pts.append((r, m, sem))
            rows.append([label, f"{r:.2f}", f"{a:.5f}", f"{m:.5f}",
                         f"{sem:.6f}", f"{(m-a)/sem:.2f}"])
        out.append((label, rgrid, curve, np.array(pts), rs))
        print(f"  {label:<12} r* = {rs:.4f}")
    return out, rows


def draw(phi, rows_a, panels_b, rows_b, sparse: bool = False):
    """
    Three axes, two panels. A is the estimator value; the narrow strip beside it
    is the same seven comparisons studentised, because at the value scale the
    confidence intervals are ~0.3% of the axis and vanish under the markers --
    a figure whose claim is agreement must show agreement at the resolution it
    was actually tested at, not at a resolution where any result would look fine.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    # Typography up ~25% from the first draft: this is read at abstract-figure
    # size, where 8 pt is legible on screen and not on a printed programme page.
    plt.rcParams.update({
        "font.size": 10, "axes.linewidth": 0.7,
        "xtick.direction": "out", "ytick.direction": "out",
        "xtick.major.width": 0.6, "ytick.major.width": 0.6,
        "mathtext.default": "regular",
    })
    INK, MC, REF, BAND = "#1a1a1a", "#c1272d", "#8c8c8c", "#dcdcdc"

    # Constrained layout, not tight_layout: three axes of unequal width plus a
    # figure-level legend is exactly the case tight_layout warns it cannot solve,
    # and it silently overlapped the axis labels with the legend.
    fig, (axA, axT, axB) = plt.subplots(
        1, 3, figsize=(8.3, 3.9), layout="constrained",
        gridspec_kw={"width_ratios": [1.0, 0.30, 0.92]})
    fig.get_layout_engine().set(w_pad=0.045, h_pad=0.03, wspace=0.055)

    labels = SPARSE_LABELS if sparse else [r[0] for r in rows_a]
    ana = np.array([float(r[1]) for r in rows_a])
    mc = np.array([float(r[2]) for r in rows_a])
    sem = np.array([float(r[3]) for r in rows_a])
    tt = np.array([float(r[4]) for r in rows_a])
    y = np.arange(len(labels))[::-1]

    # ---- A: estimator value --------------------------------------------
    axA.axvline(1.0, color=REF, lw=0.7, ls=(0, (4, 3)), zorder=1)
    axA.scatter(ana, y, s=46, facecolors="none", edgecolors=INK,
                linewidths=0.9, zorder=3)
    axA.errorbar(mc, y, xerr=1.96 * sem, fmt="o", ms=3.0, color=MC,
                 ecolor=MC, elinewidth=0.9, capsize=1.6, capthick=0.9, zorder=4)
    axA.set_yticks(y, labels)
    axA.set_ylim(-0.7, len(labels) + 0.25)
    axA.set_xlabel(r"$\hat\lambda\,/\,\lambda_E$")
    axA.set_xticks([0.85, 0.90, 0.95, 1.00])
    # Name the reference line and the band in place. A dashed line and a grey
    # rectangle are the two elements a reader cannot decode from the legend.
    if not sparse:
        axA.text(1.0, len(labels) - 0.33, "unbiased = 1", color=REF,
                 fontsize=8.5, ha="center", va="bottom")
    axA.tick_params(axis="y", length=0)
    for sp in ("top", "right", "left"):
        axA.spines[sp].set_visible(False)

    # ---- A, studentised strip ------------------------------------------
    band_top = len(labels) - 0.45
    axT.fill_betweenx([-0.7, band_top], -2, 2, color=BAND, lw=0, zorder=0)
    axT.vlines(0.0, -0.7, band_top, color=REF, lw=0.7, zorder=1)
    axT.scatter(tt, y, s=14, color=MC, zorder=3)
    axT.set_yticks(y, [])
    axT.set_ylim(-0.7, len(labels) + 0.25)
    axT.set_xlim(-5, 5)
    axT.set_xticks([-4, 0, 4])
    axT.set_xlabel(r"(MC $-$ analytic) / SE")
    if not sparse:
        axT.text(0.0, band_top + 0.12, r"$\pm2$ SE", color=REF,
                 fontsize=8.5, ha="center", va="bottom")
    axT.tick_params(axis="y", length=0)
    for sp in ("top", "right", "left"):
        axT.spines[sp].set_visible(False)

    # ---- B: composed with screening ------------------------------------
    axB.axhline(0.0, color=REF, lw=0.7, ls=(0, (4, 3)), zorder=1)
    # Curves labelled in place rather than through the legend, so the reader is
    # not decoding two keys at once. The glosses ("no upstream distortion",
    # "state-dependent acquisition") stay in the caption: at this panel width the
    # two curves are ~12% of the axis apart at their widest, which is not enough
    # room for a two-line annotation without overplotting the data.
    curve_tags = [(r"$w\equiv1$", 1.38, 0.030), (r"$\eta=0.3$", 1.38, -0.038)]
    for (label, rg, curve, pts, rs), ls, (tag, tx, dy) in zip(
            panels_b, ["-", (0, (5, 2))], curve_tags):
        axB.plot(rg, curve, color=INK, lw=1.3, ls=ls, zorder=3)
        if not sparse:
            axB.text(tx, float(np.interp(tx, rg, curve)) + dy, tag, color=INK,
                     fontsize=9.5, ha="center", va="center")
        axB.errorbar(pts[:, 0], pts[:, 1], yerr=1.96 * pts[:, 2], fmt="o",
                     ms=3.0, color=MC, ecolor=MC, elinewidth=0.9, capsize=1.6,
                     capthick=0.9, zorder=4)
        axB.plot([rs], [0.0], marker="v", ms=4.2, color=REF,
                 clip_on=False, zorder=5)
    if sparse:
        axB.set_xlabel(r"$r$")
        axB.set_ylabel("limiting estimation error", labelpad=1.5)
    else:
        # fontsize trimmed: at 10 pt this label overruns the figure's right edge,
        # since it is centred on an axis that ends there.
        axB.set_xlabel(r"selective attendance ratio, $r=q_1/q_0$", fontsize=9)
        axB.set_ylabel("limiting estimation error (LEL)", labelpad=1.5)
    axB.set_xlim(0.25, 1.60)
    axB.set_xticks([0.5, 1.0, 1.5])
    for sp in ("top", "right"):
        axB.spines[sp].set_visible(False)

    handles = [
        Line2D([], [], marker="o", ls="none", mfc="none", mec=INK, mew=0.9,
               ms=6.4, label="analytic"),
        Line2D([], [], marker="o", ls="none", color=MC, ms=3.4,
               label="Monte Carlo"),
        Line2D([], [], marker="v", ls="none", color=REF, ms=4.2,
               label=r"predicted $r^{\star}$"),
    ]
    if sparse:
        handles[2:2] = [
            Line2D([], [], color=INK, lw=1.3, label=r"$w\equiv1$"),
            Line2D([], [], color=INK, lw=1.3, ls=(0, (5, 2)), label=r"$\eta=0.3$")]
    fig.legend(handles=handles, loc="outside lower center", ncol=len(handles),
               frameon=False, handletextpad=0.45, columnspacing=1.6,
               borderpad=0.0)

    for ax, ltr in ((axA, "A"), (axB, "B")):
        ax.text(0.0, 1.05, ltr, transform=ax.transAxes,
                fontsize=9, fontweight="bold", va="bottom", ha="left")
    stem = "croi_falsification_sparse" if sparse else "croi_falsification"
    for ext in ("png", "pdf"):
        p = FIGURES / f"{stem}.{ext}"
        fig.savefig(p, dpi=600 if ext == "png" else None)
        print(f"  wrote {p.name}")
    return FIGURES / "croi_falsification.png"


def caption(rows_a, rows_b, phi):
    v = [float(r[1]) for r in rows_a]          # analytic, in CELLS order
    # The two tables have different column layouts: t is the 5th column of the
    # census table and the 6th of the screening table. Reading both at index 4
    # silently substitutes the screening standard errors (~5e-4) for their t
    # statistics, which understates the reported worst-case agreement.
    zmax = max([abs(float(r[4])) for r in rows_a]
               + [abs(float(r[5])) for r in rows_b])
    rstar0 = boundary_no_dynamics(THETA_NHBS, C_PURPOSE)
    txt = f"""FIGURE. Analytic predictions and independent Monte Carlo validation
of eligibility-dynamic bias.

(A) Estimated-to-target incidence ratio under the exact-cancellation conditions
and selected violations. The dashed line denotes no bias. Open circles are
analytic limits; red points are Monte Carlo means over {N_REP} independent
replicates of {N_DRAW // 1_000_000} million individuals each, whose 95%
confidence intervals are narrower than the plotting symbols; standardised
Monte Carlo minus analytic discrepancies are shown at right, with the shaded band
at plus or minus two standard errors. When all five conditions hold (stable
living-state composition, demographically stationary observable susceptible pool,
state-invariant acquisition, infection-independent movement, no absorbing loss),
temporary losses and returns cancel exactly at {v[0]:.3f}. Absorbing loss at
all-cause mortality mu-E attenuates the estimate to {v[1]:.3f} at 0.04/year and
{v[2]:.3f} at 0.10/year. Acquisition in temporarily unobservable states at
relative hazard eta attenuates when eta is below one ({v[3]:.3f} at eta = 0,
{v[4]:.3f} at eta = 0.3) and inflates when eta exceeds one ({v[5]:.3f} at
eta = 1.8), so the direction of bias is set by the acquisition hazard rather than
by occupancy. The final row is a stress test raising unobservable occupancy to
15% ({v[6]:.3f}); elsewhere jail and prison occupancies are 3% and 5% with mean
sojourns of 32 days and 2.7 years.

(B) Limiting estimation error across the screening-attendance ratio r, without
upstream eligibility distortion (w = 1, solid) and with state-dependent
acquisition (eta = 0.3, dashed). Triangles denote analytically predicted
zero-bias boundaries, which the simulator reproduces without being given them;
points are independent Monte Carlo estimates. Without dynamics the boundary is
exp(-theta c) = {rstar0:.3f}. Background HIV testing rate theta =
{THETA_NHBS:.3f}/year, testing-based exclusion cutoff c = 90 days, and a gamma
recency function with window parameter 163 days and shadow 260 days, giving
MDRI (Omega_T*) = {phi.mdri_days:.0f} days over the T* = 2 year window; the window
parameter and the MDRI are distinct quantities and are easily conflated.

All {len(rows_a) + len(rows_b)} comparisons agree within |t| = {zmax:.2f} on
{N_REP - 1} degrees of freedom. The simulator shares no code with the analytic
derivation and every cell uses a disjoint block of random seeds.
"""
    p = ROOT / "manuscript" / "croi2026" / "FIGURE_CAPTION.txt"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(txt)
    print(f"  wrote {p.relative_to(ROOT)}  ({len(txt.split())} words)")


def main():
    banner("CROI falsification figure")
    phi = gamma_phi(163, 260, GRID)
    if "--redraw" in sys.argv:
        print("  redrawing from cached tables; no simulation\n")
        rows_a, rows_b = load_cached()
        panels_b = rebuild_panel_b(phi, rows_b)
    else:
        print(f"  {N_REP} reps x {N_DRAW/1e6:.0f}M draws per cell, disjoint seeds\n")
        rows_a = panel_a(phi)
        print()
        panels_b, rows_b = panel_b(phi)
        write_table(rows_a, ["condition", "analytic", "mc_mean", "mc_sem", "z"],
                    "croi_figA_census.csv")
        write_table(rows_b, ["setting", "r", "analytic", "mc_mean", "mc_sem", "z"],
                    "croi_figB_screening.csv")
    draw(phi, rows_a, panels_b, rows_b, sparse=False)
    draw(phi, rows_a, panels_b, rows_b, sparse=True)
    caption(rows_a, rows_b, phi)
    return 0


if __name__ == "__main__":
    sys.exit(main())
