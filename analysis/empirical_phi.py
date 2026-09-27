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
from src.eligibility_dynamics import empirical_phi, YEAR_DAYS, default_grid

CANDIDATES = sorted(ROOT.glob("data/cephia_public_use_dataset_*.csv"))
EXPECTED = ROOT / "data" / "fixtures" / "cephia_expected.json"


def have_cephia() -> bool:
    return bool(CANDIDATES)


def load(csv_path):
    import pandas as pd
    cols = ["cephia_panel", "assay", "assay_result_field", "assay_result_value",
            "hiv_subtype", "days_since_eddi", "viral_load_closest_to_visit",
            "participant_identifier"]
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


def binned_recency(d, edges=(730, 1095, 1825, 3650), vl_threshold=None):
    """Raw test-recent proportion by duration bin. The tail is NOT flat."""
    out = []
    rec = (d.odn <= 1.5)
    if vl_threshold is not None:
        rec &= (d.viral_load_closest_to_visit > vl_threshold)
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = (d.days_since_eddi > lo) & (d.days_since_eddi <= hi)
        out.append(float(rec[m].mean()) if m.any() else float("nan"))
    return out


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

    tail = binned_recency(d)
    print(f"\n  raw tail (730-1095, 1095-1825, 1825-3650 d): "
          + ", ".join(f"{t:.3f}" for t in tail))
    print("  declining, not flat -- Gao & Bannick Assumption B.1 is violated here.")

    EXPECTED.parent.mkdir(parents=True, exist_ok=True)
    EXPECTED.write_text(json.dumps(
        {"mdri_days": round(ref.mdri_days, 1), "ci_lo": 161, "ci_hi": 213,
         "tail_bins": [round(t, 4) for t in tail],
         "note": "frozen expected values only; no participant rows"}, indent=2))
    print(f"  wrote {EXPECTED.relative_to(ROOT)}")

    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    ax.plot(ref.grid, ref.values, lw=2, label=f"CEPHIA empirical (subtype C, VL>75)")
    for nm in ("pan_aje", "pan_arxiv"):
        p = phi_for(nm)
        ax.plot(p.grid, p.values, lw=1.2, ls="--", label=p.label)
    ax.set_xlabel("infection duration $u$ (years)"); ax.set_ylabel(r"$\varphi(u)$")
    ax.set_title("Empirical vs parametric recency functions")
    ax.legend(fontsize=8, frameon=False); fig.tight_layout()
    p = FIGURES / "fig4_empirical_phi.png"
    fig.savefig(p, dpi=200); print(f"  wrote {p.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
