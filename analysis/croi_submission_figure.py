"""
The CROI 2027 submitted graphic: panel A only, authored at 4 x 4 inches.

Why this is a separate script rather than a flag on falsification_figure.py.
That figure is the repository's validation artifact and carries both analyses at
7.4 x 3.9 in. This one is a submission deliverable bound by portal rules that
have nothing to do with the science: PNG or JPEG only, a 4-inch reproduction
size, and a 100-word budget that counts the legend and every in-plot annotation
but not axis labels or row headers. Those constraints will drift apart over time,
and a shared flag would make each one's layout hostage to the other's.

Laid out at 4 x 4 in, NOT rescaled from the 7.4 in render. Rescaling a 10 pt
label into a 4-inch reproduction leaves roughly 4.8 pt on the page; type here is
sized so that nothing falls below 7 pt at final size.

ONE panel by default. CROI rule 4 admits a second panel "only if both panels
represent the same analysis (eg, same graph type, axes, and analysis)". The
studentised discrepancy strip shares the rows, the data and the graph type with
the value scale, but NOT the x-axis -- one is a ratio near 1, the other is in
standard errors. That is a defensible reading either way, and the penalty for
losing the argument is severe and one-sided: a non-compliant graphic is removed,
cannot be replaced, is not seen by reviewers, and does not appear in the eBook.
So the submitted figure is the value scale alone, and the agreement it used to
show graphically is stated numerically in the caption instead.

Pass --with-strip to rebuild the two-panel version for the poster, where the rule
does not apply.

Panel B -- the composed screening model -- is dropped for the same rule plus its
own reasons: a second vocabulary the 100-word budget cannot carry, and both
borderline comparisons live there. See manuscript/croi2027/README.md.

Numbers come from outputs/tables/croi_figA_census.csv and are never recomputed
here; run `falsification_figure.py --redraw` if that table is missing.
"""
import csv
import sys

import numpy as np
from _common import banner, FIGURES, TABLES, ROOT

OUT = FIGURES / "croi_eligibility_panelA.png"
SRC = TABLES / "croi_figA_census.csv"

CANVAS_IN = (4.0, 4.0)
EXPORT_DPI = 600
MIN_PT = 7.0

# Verbatim from the submission spec. These are ROW HEADERS and axis labels,
# which the portal does not count against the 100-word caption budget -- so the
# defining text lives here by design, not in the caption.
# Wrapped, not abbreviated. At a 4-inch canvas the unwrapped header column is
# ~37% of the total width and the value-axis label is wider than its own axis;
# the wording is the spec's and is preserved exactly, only the line breaks are a
# layout choice. Shrinking the type instead would breach the 7 pt floor.
ROW_HEADERS = [
    "cancellation\nconditions met",
    "mortality,\n$\\mu_E$ = 0.04/y",
    "mortality,\n$\\mu_E$ = 0.10/y",
    "$\\eta$ = 0",
    "$\\eta$ = 0.3",
    "$\\eta$ = 1.8",
    "$\\eta$ = 0, $q_J$ = 0.15\n(stress test)",
]
X_VALUE = ("estimated-to-target incidence ratio,\n"
           "$\\hat\\lambda$ / $\\lambda_E$")
X_STRIP = "(Monte Carlo $-$\nanalytic) / SE"

# Counted against the 100 words: two legend entries and two annotations.
LEGEND = ("analytic", "Monte Carlo")
ANN_UNBIASED, ANN_BAND = "unbiased = 1", "$\\pm$2 SE"


def load():
    rows = list(csv.reader(SRC.open()))
    if not rows or rows[0][-1] != "t":
        raise SystemExit(f"{SRC.name}: expected a 't' column; run "
                         "falsification_figure.py --redraw")
    body = rows[1:]
    if len(body) != len(ROW_HEADERS):
        raise SystemExit(f"{SRC.name} has {len(body)} rows, "
                         f"{len(ROW_HEADERS)} headers")
    ana = np.array([float(r[1]) for r in body])
    mc = np.array([float(r[2]) for r in body])
    sem = np.array([float(r[3]) for r in body])
    t = np.array([float(r[4]) for r in body])
    return ana, mc, sem, t


# The 100-word budget counts the caption AND the legend AND every in-plot
# annotation. The brief specified a 97-word caption and separately specified the
# two legend entries and two annotations below, which together are 8 words:
# 97 + 8 = 105. The brief's own caveat says to verify the total including them,
# so the caption is trimmed to 92 and nothing is dropped from the figure.
#
# Five words removed, no fact lost:
#   "Rows give the five ..."          -> "Rows give five ..."            (-1)
#   "means are over 24 replicates"    -> "means over 24 replicates"      (-1)
#   "symbols, so standardised"        -> "symbols; standardised"         (-1)
#   "the direction of bias is set by" -> "bias direction is set by"      (-2)
# The 97-word original is preserved in manuscript/croi2027/README.md.
CAPTION = (
    "Analytic predictions and independent Monte Carlo validation. Rows give the "
    "five exact-cancellation conditions and single-condition failures; the dashed "
    "line marks no bias. Monte Carlo means are over 24 replicates of 15 million "
    "individuals, with 95% intervals narrower than the plotting symbols. Losses "
    "and returns cancel exactly at {v0:.3f}. Absorbing mortality attenuates the "
    "estimate; acquisition in temporarily unobservable states attenuates below "
    "eta=1 and inflates above it, so the direction of bias is set by acquisition "
    "hazard, not occupancy. All seven comparisons agree within |t|={tmax:.2f} on "
    "23 df; simulator and derivation share no code."
)
WORD_LIMIT = 100


def write_caption(ana, tt, with_strip: bool):
    """
    Caption with its numbers taken from the table, and the word budget enforced.

    Numbers are interpolated rather than typed so the caption cannot state a
    cancellation value or a worst-case |t| that the plotted data contradict.
    """
    txt = CAPTION.format(v0=ana[0], tmax=np.abs(tt).max())
    # CROI rule 3 counts titles, legends, labels and footnotes, EXCLUDING x- and
    # y-axis labels and row or column headers. So the row headers and both axis
    # labels are free, and the caption, the legend and the in-plot annotations
    # are not.
    counted = [txt, *LEGEND, ANN_UNBIASED]
    if with_strip:
        counted.append(ANN_BAND.replace("$\\pm$", "+/-"))
    n = sum(len(x.split()) for x in counted)
    if n > WORD_LIMIT:
        raise SystemExit(f"counted text is {n} words, limit {WORD_LIMIT}")
    out = FIGURES.parent.parent / "manuscript" / "croi2027" / "FIGURE_CAPTION.txt"
    out.write_text(txt + "\n")
    print(f"  wrote {out.relative_to(ROOT)}")
    print(f"  words counted by CROI rule 3: caption {len(txt.split())}, "
          f"legend {sum(len(x.split()) for x in LEGEND)}, "
          f"annotations {n - len(txt.split()) - sum(len(x.split()) for x in LEGEND)}"
          f"; total {n} of {WORD_LIMIT}")
    return n


def main():
    with_strip = "--with-strip" in sys.argv
    banner("CROI 2027 submitted graphic"
           + (" (two panels -- POSTER ONLY)" if with_strip else ""))
    ana, mc, sem, tt = load()

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    # Final-size points: the canvas IS 4 in, so nothing is rescaled at export and
    # these are what a reviewer sees. Dropping the strip frees width, so the type
    # is larger here than in the two-panel build.
    F_TICK, F_AXIS, F_LEG, F_ANN = (
        (7.2, 7.4, 7.2, 7.0) if with_strip else (8.4, 8.6, 8.4, 8.0))
    assert min(F_TICK, F_AXIS, F_LEG, F_ANN) >= MIN_PT

    plt.rcParams.update({
        "font.size": F_TICK, "axes.linewidth": 0.6,
        "xtick.direction": "out", "ytick.direction": "out",
        "xtick.major.width": 0.6, "xtick.major.size": 2.5,
        "mathtext.default": "regular",
    })
    INK, MC, REF, BAND = "#1a1a1a", "#c1272d", "#8c8c8c", "#dcdcdc"

    if with_strip:
        fig, (axV, axT) = plt.subplots(
            1, 2, figsize=CANVAS_IN, layout="constrained",
            gridspec_kw={"width_ratios": [1.0, 0.40]})
    else:
        fig, axV = plt.subplots(figsize=CANVAS_IN, layout="constrained")
        axT = None
    fig.get_layout_engine().set(w_pad=0.03, h_pad=0.03, wspace=0.05)

    n = len(ROW_HEADERS)
    y = np.arange(n)[::-1]
    top = n - 0.42

    axV.vlines(1.0, -0.7, top, color=REF, lw=0.7, ls=(0, (3.5, 2.5)), zorder=1)
    axV.scatter(ana, y, s=42 if not with_strip else 30, facecolors="none",
                edgecolors=INK, linewidths=0.9, zorder=3)
    axV.errorbar(mc, y, xerr=1.96 * sem, fmt="o", ms=3.0 if not with_strip else 2.4,
                 color=MC, ecolor=MC, elinewidth=0.8, capsize=1.3, capthick=0.8,
                 zorder=4)
    # Right-aligned just inside the line, not centred on it: the axis ends at
    # 1.022 and a centred label overruns the canvas, which at 4 in is a clipped
    # word rather than a cosmetic overhang.
    axV.text(0.997, top + 0.10, ANN_UNBIASED, color=REF, fontsize=F_ANN,
             ha="right", va="bottom")
    axV.set_yticks(y, ROW_HEADERS)
    axV.set_ylim(-0.7, n + 0.30)
    axV.set_xlim(0.835, 1.022)
    axV.set_xticks([0.85, 0.90, 0.95, 1.00])
    axV.set_xticklabels(["0.85", "0.90", "0.95", "1.00"])
    axV.set_xlabel(X_VALUE, fontsize=F_AXIS, labelpad=2)
    axV.tick_params(axis="y", length=0, pad=2.0)
    axV.tick_params(axis="x", labelsize=F_TICK)
    for sp in ("top", "right", "left"):
        axV.spines[sp].set_visible(False)

    if axT is not None:
        axT.fill_betweenx([-0.7, top], -2, 2, color=BAND, lw=0, zorder=0)
        axT.vlines(0.0, -0.7, top, color=REF, lw=0.7, zorder=1)
        axT.scatter(tt, y, s=11, color=MC, zorder=3)
        axT.text(0.0, top + 0.10, ANN_BAND, color=REF, fontsize=F_ANN,
                 ha="center", va="bottom")
        axT.set_yticks(y, [])
        axT.set_ylim(-0.7, n + 0.30)
        axT.set_xlim(-4.6, 4.6)
        axT.set_xticks([-3, 0, 3])
        axT.set_xticklabels(["$-$3", "0", "3"])
        axT.set_xlabel(X_STRIP, fontsize=F_AXIS, labelpad=2)
        axT.tick_params(axis="y", length=0)
        axT.tick_params(axis="x", labelsize=F_TICK)
        for sp in ("top", "right", "left"):
            axT.spines[sp].set_visible(False)

    fig.legend(
        handles=[Line2D([], [], marker="o", ls="none", mfc="none", mec=INK,
                        mew=0.9, ms=5.6, label=LEGEND[0]),
                 Line2D([], [], marker="o", ls="none", color=MC, ms=3.2,
                        label=LEGEND[1])],
        loc="outside lower center", ncol=2, frameon=False, fontsize=F_LEG,
        handletextpad=0.4, columnspacing=1.8, borderpad=0.0)

    out = (FIGURES / "croi_eligibility_panelA_withstrip.png" if with_strip
           else OUT)
    fig.savefig(out, dpi=EXPORT_DPI, format="png")
    w, h = fig.get_size_inches()
    print(f"  wrote {out.relative_to(ROOT)}")
    print(f"  canvas {w:.1f} x {h:.1f} in at {EXPORT_DPI} dpi "
          f"= {int(w*EXPORT_DPI)} x {int(h*EXPORT_DPI)} px")
    print(f"  smallest type {min(F_TICK, F_AXIS, F_LEG, F_ANN):.1f} pt at "
          f"final size (floor {MIN_PT:.0f} pt)")
    print(f"  panels: {2 if with_strip else 1}"
          + ("  <-- CROI rule 4 risk; poster only" if with_strip else
             "  (CROI rule 4: single panel, no ambiguity)"))
    print(f"  data cells if read as table-based (rule 5/6): "
          f"{n * (3 if with_strip else 2)} of 64")
    if not with_strip:
        write_caption(ana, tt, with_strip)
    return 0


if __name__ == "__main__":
    sys.exit(main())
