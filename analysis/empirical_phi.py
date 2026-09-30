"""
Figure 4 / Table S1: phi(u) estimated from the CEPHIA public-use dataset.

Procedure follows XSRecency: Evaluation Panel, LAg-Sedia consolidated
final_result ODn, subtypes A1/B/C/D, logit polynomial in years since EDDI, GEE
clustered on participant with an independence working correlation.

Requires the CEPHIA CSV, which is NOT redistributed. See data/README.md. Without
it this script exits cleanly and the offline suite skips the dependent tests.

Reference: subtype C, ODn <= 1.5 and VL > 75 gives MDRI 182.4 d (95% CI
161-213), consistent with the 163 d used in the literature.
"""
import json, sys
from pathlib import Path
from _common import banner, write_table, FIGURES, ROOT, phi_for
import numpy as np
from src.eligibility_dynamics import (empirical_phi, YEAR_DAYS, T_STAR,
                                      default_grid)

CANDIDATES = sorted(ROOT.glob("data/cephia_public_use_dataset_*.csv"))
EXPECTED = ROOT / "data" / "fixtures" / "cephia_expected.json"
RECOMPUTED = ROOT / "outputs" / "cephia_recomputed.json"


def have_cephia() -> bool:
    return bool(CANDIDATES)


def load(csv_path):
    import pandas as pd
    cols = ["cephia_panel", "assay", "assay_result_field", "assay_result_value",
            "hiv_subtype", "days_since_eddi", "viral_load_closest_to_visit",
            "participant_identifier", "treatment_naive_at_visit",
            "designated_as_elite_controller_at_visit"]
    d = pd.read_csv(csv_path, usecols=cols, low_memory=False)
    d = d[(d.cephia_panel == "CEPHIA 1 Evaluation Panel")
          & (d.assay == "LAg-Sedia")
          & (d.assay_result_field == "final_result")
          & (d.hiv_subtype.isin(["A1", "B", "C", "D"]))
          & d.days_since_eddi.notna()].copy()
    d["odn"] = pd.to_numeric(d.assay_result_value, errors="coerce")
    d["u"] = d.days_since_eddi / YEAR_DAYS
    return d.dropna(subset=["odn"])


def fit(d, subtype="C", vl_threshold=75, max_u=5.0, degree=3):
    s = d[(d.hiv_subtype == subtype) & (d.u.between(0, max_u))]
    recent = ((s.odn <= 1.5) & (s.viral_load_closest_to_visit > vl_threshold))
    phi = empirical_phi(s.u.values, recent.astype(int).values, degree=degree,
                        grid=default_grid(), groups=s.participant_identifier.values)
    return phi, int(s.participant_identifier.nunique())


EDGES = (730, 1095, 1825, 3650)


def binned_recency(d, edges=EDGES, vl_threshold=None,
                   treatment_naive=None):
    """
    Raw test-recent proportion by duration bin, for a STATED subset.

    The subset is not a detail. Assumption B.1 concerns the false-recency rate of
    untreated infection, and antiretroviral treatment drives LAg ODn back down,
    so treated individuals re-enter the "recent" category at long durations. The
    tail therefore has opposite shapes depending on who is included, and quoting
    one without naming the subset is how a wrong number survives.

    treatment_naive=True  restricts to treatment-naive, non-elite-controller
    visits; None uses every visit in the frame.
    """
    f = d
    if treatment_naive is True:
        f = f[(f.treatment_naive_at_visit == True)                      # noqa: E712
              & (f.designated_as_elite_controller_at_visit != True)]    # noqa: E712
    rec = (f.odn <= 1.5)
    if vl_threshold is not None:
        rec &= (f.viral_load_closest_to_visit > vl_threshold)
    out = []
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = (f.days_since_eddi > lo) & (f.days_since_eddi <= hi)
        out.append(float(rec[m].mean()) if m.any() else float("nan"))
    return out, int(len(f))


def main():
    banner("Empirical phi from CEPHIA")
    if not have_cephia():
        print("  CEPHIA CSV not found under data/ -- skipping.")
        print("  Retrieve per data/README.md (Zenodo 10.5281/zenodo.4900634).")
        return 0
    d = load(CANDIDATES[0])
    rows = []
    print(f"{'algorithm':<34}{'MDRI (d)':>10}{'shadow (d)':>12}{'n':>7}")
    ref = None
    for st, vl in (("C", 75), ("C", 1000), ("B", 75)):
        phi, n = fit(d, st, vl)
        print(f"{f'subtype {st}, ODn<=1.5 & VL>{vl}':<34}"
              f"{phi.mdri_days:>10.1f}{phi.shadow_days:>12.1f}{n:>7}")
        rows.append([st, vl, f"{phi.mdri_days:.1f}", f"{phi.shadow_days:.1f}", n])
        if (st, vl) == ("C", 75):
            ref = phi
    write_table(rows, ["subtype", "vl_threshold", "mdri_days", "shadow_days",
                       "participants"], "tableS1_cephia_mdri.csv")

    naive, n_naive = binned_recency(d, treatment_naive=True)
    allv, n_all = binned_recency(d)
    fmt = lambda t: ", ".join(f"{x:.3f}" for x in t)
    print(f"\n  raw test-recent proportion, 730-1095 / 1095-1825 / 1825-3650 d")
    print(f"    treatment-naive, non-elite-controller (n={n_naive}): {fmt(naive)}")
    print(f"    all visits in frame            (n={n_all}): {fmt(allv)}")

    def verdict(t):
        if all(t[i] > t[i + 1] for i in range(len(t) - 1)):
            return "declines monotonically"
        if t[-1] > t[-2]:
            return "RISES in the final bin"
        return "neither monotone nor flat"
    print(f"    untreated: {verdict(naive)}; all visits: {verdict(allv)}")
    print("  Either way the tail is not flat, so Gao & Bannick's Assumption B.1")
    print("  does not hold in these data. The direction of the violation depends")
    print("  on treatment status: ART drives ODn back down, so treated visits")
    print("  re-enter the recent category at long duration.")
    tail = naive

    # Compare against the frozen expectation; do NOT overwrite it. The fixture is
    # the recorded claim (computation_record.md section 3); this run is the
    # observation. Overwriting would make the regression test vacuous.
    exp = json.loads(EXPECTED.read_text())
    tol = float(exp["mdri_tolerance_days"])
    print(f"\n  against {EXPECTED.relative_to(ROOT)} (tolerance {tol} d):")
    worst = 0.0
    for e in exp["algorithms"]:
        got = next((r for r in rows
                    if r[0] == e["subtype"] and r[1] == e["vl_threshold"]), None)
        if got is None:
            print(f"    subtype {e['subtype']}, VL>{e['vl_threshold']}: not computed")
            continue
        d_mdri = float(got[2]) - e["mdri_days"]
        worst = max(worst, abs(d_mdri))
        flag = "ok " if abs(d_mdri) <= tol else "OFF"
        print(f"    {flag} subtype {e['subtype']}, VL>{e['vl_threshold']}: "
              f"{float(got[2]):.1f} d vs frozen {e['mdri_days']:.1f} "
              f"({d_mdri:+.1f}); participants {got[4]} vs {e['participants']}")
    print(f"    worst MDRI deviation {worst:.2f} d")

    RECOMPUTED.parent.mkdir(parents=True, exist_ok=True)
    RECOMPUTED.write_text(json.dumps(
        {"algorithms": [{"subtype": r[0], "vl_threshold": r[1],
                         "mdri_days": float(r[2]), "shadow_days": float(r[3]),
                         "participants": r[4]} for r in rows],
         "tail_bins_treatment_naive": [round(t, 4) for t in naive],
         "tail_bins_all_visits": [round(t, 4) for t in allv],
         "n_treatment_naive": n_naive, "n_all_visits": n_all,
         "worst_mdri_deviation_days": round(worst, 3),
         "note": "observation from this run; the frozen claim is "
                 "data/fixtures/cephia_expected.json"}, indent=2))
    print(f"  wrote {RECOMPUTED.relative_to(ROOT)}")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # Two panels of the same analysis: the fitted recency function, and the raw
    # tail that shows Assumption B.1 failing. The tail belongs here rather than
    # in prose because its two subsets fail in opposite directions, which a
    # sentence conveys poorly and a plot conveys at a glance.
    fig, (axA, axB) = plt.subplots(1, 2, figsize=(9.4, 4.0), layout="constrained")

    axA.plot(ref.grid, ref.values, lw=2,
             label="CEPHIA empirical\n(subtype C, ODn$\\leq$1.5, VL>75)")
    for nm in ("pan_aje", "pan_arxiv"):
        q = phi_for(nm)
        axA.plot(q.grid, q.values, lw=1.2, ls="--", label=q.label)
    axA.set_xlabel("infection duration $u$ (years)")
    axA.set_ylabel(r"$\varphi(u)$")
    axA.legend(fontsize=8, frameon=False)
    axA.set_title("Fitted against parametric bases", fontsize=10)
    for sp in ("top", "right"):
        axA.spines[sp].set_visible(False)

    # Categorical positions, not day-centres. The bins are 365, 730 and 1825 days
    # wide, so bars scaled to bin width make the last one dominate the panel and
    # overrun the axis. Width here carries no information; height does.
    import numpy as np
    x = np.arange(len(naive))
    axB.bar(x - 0.19, naive, width=0.36, color="#1f77b4",
            label=f"treatment-naive (n={n_naive})")
    axB.bar(x + 0.19, allv, width=0.36, color="#c1272d",
            label=f"all visits (n={n_all})")
    for xi, v in zip(x - 0.19, naive):
        axB.text(xi, v + 0.006, f"{v:.3f}", ha="center", fontsize=7.5)
    for xi, v in zip(x + 0.19, allv):
        axB.text(xi, v + 0.006, f"{v:.3f}", ha="center", fontsize=7.5)
    axB.set_xticks(x)
    axB.set_xticklabels([f"{lo}–{hi}" for lo, hi in zip(EDGES[:-1], EDGES[1:])],
                        fontsize=8.5)
    axB.set_xlabel("infection duration (days), all bins beyond $T^*$")
    axB.set_ylabel("proportion test-recent")
    axB.set_ylim(0, max(allv) * 1.18)
    axB.legend(fontsize=8, frameon=False, loc="upper left")
    axB.set_title("Raw tail: B.1 fails in both directions", fontsize=10)
    for sp in ("top", "right"):
        axB.spines[sp].set_visible(False)

    for ax, ltr in ((axA, "A"), (axB, "B")):
        ax.text(0.0, 1.06, ltr, transform=ax.transAxes, fontsize=11,
                fontweight="bold", va="bottom", ha="left")

    p = FIGURES / "fig4_empirical_phi.png"
    fig.savefig(p, dpi=200)
    fig.savefig(p.with_suffix(".pdf"))
    print(f"  wrote {p.name} and {p.with_suffix('.pdf').name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
