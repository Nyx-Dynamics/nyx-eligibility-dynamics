"""
Assemble Paper A's figures and tables under their FINAL numbers.

The generating scripts name their outputs after what they compute, which is right
for them and wrong for a manuscript: `fig3_eta_surface` is Figure S1, and the
two-panel validation figure has no number of its own at all. This script is the
one place the mapping lives, so a renumbering is a single edit here rather than a
search across five prose files and three plotting scripts.

It copies rather than regenerates. Run `make figures` first; nothing is computed
here, and no number can change as a side effect of assembly.

    python3 analysis/assemble_manuscript.py            # -> outputs/manuscript/
    python3 analysis/assemble_manuscript.py --check    # verify only, write nothing

Numbering follows the order of first citation in the text. Main-text items carry
the theorem and its validation; the supplement carries sensitivity surfaces,
comparisons with other methods, and anything requiring data we do not
redistribute.
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIG, TAB = ROOT / "outputs" / "figures", ROOT / "outputs" / "tables"
OUT = ROOT / "outputs" / "manuscript"
MANUSCRIPT = ROOT / "manuscript"

# label -> (source stem, section of first citation, caption)
FIGURES = {
    "Figure 1": ("fig1_weight_by_mechanism", "4.2",
                 "Historical observability weight $w_t(u)$ by mechanism: absorbing "
                 "loss, transient movement, and the two combined. Transient movement "
                 "alone leaves $w_t\\equiv1$."),
    "Figure 2": ("fig2_cancellation", "4.2",
                 "Exact cancellation is invariant to occupancy and sojourn. "
                 "$\\hat\\lambda/\\lambda_E$ against the share of person-time spent "
                 "unobservable, across sojourn lengths, under the five conditions "
                 "of Corollary 2."),
    "Figure 3": ("croi_falsification", "4.3",
                 "Analytic predictions against an independently written generative "
                 "simulator. (A) Census sampling, seven population scenarios. (B) "
                 "Composed with the screening and prior-testing stages. All 19 "
                 "comparisons agree within $|t|=2.20$ on 23 degrees of freedom."),
    "Figure S1": ("fig3_eta_surface", "4.5",
                  "Zero-bias boundary over the $(\\eta_J,\\eta_P)$ surface at "
                  "$q_J=3\\%$, $q_P=5\\%$, with the $r^\\star=1$ contour."),
    "Figure S2": ("fig4_empirical_phi", "3.2*",
                  "Empirical recency function from the CEPHIA public-use dataset "
                  "against the parametric bases. Requires data not redistributed "
                  "here; see data/README.md."),
}

TABLES = {
    "Table 1":   ("table1_pan_recovery", "4.1",
                  "Recovery of the published limiting estimation error at "
                  "$w_t\\equiv1$, all nine cells."),
    "Table 2":   ("table2_mortality_threshold", "4.4",
                  "Attenuation and the composed zero-bias boundary against "
                  "absorbing loss $\\mu$."),
    "Table 3":   ("table3_frailty_mixture", "4.2",
                  "Cancellation under stationary frailty mixtures of increasing "
                  "skew in movement propensity."),
    "Table S1":  ("cephia_mdri", "3.2*",
                  "CEPHIA MDRI by algorithm and subtype. Requires data not "
                  "redistributed here."),
    "Table S2":  ("tableS2_wang_comparator", "4.8",
                  "Covariate reweighting against the duration mechanism, three "
                  "target-population cases."),
    "Table S3a": ("tableS3a_eta_common", "4.5",
                  "Zero-bias boundary against a common relative acquisition "
                  "hazard $\\eta$."),
    "Table S3b": ("tableS3b_eta_sites", "4.7",
                  "Break-even $\\eta$ by site county. Illustrative; not an "
                  "epidemiologic claim about any county."),
    "Table S4":  ("tableS4_inter_test_process", "4.6",
                  "Boundary invariance across recency bases, by inter-test "
                  "process."),
}

# Items whose source data is not redistributed. Absent on a clean clone is the
# EXPECTED state for these, not a failure: a gate that always fires is a gate
# people learn to ignore. Marked by a trailing "*" on the section above.
SLUG = re.compile(r"[^a-z0-9]+")


def needs_data(sec: str) -> bool:
    return sec.endswith("*")


def final_name(label: str) -> str:
    return SLUG.sub("_", label.lower()).strip("_")


def collect():
    """(label, kind, sources, caption, section, present) for everything."""
    out = []
    for label, (stem, sec, cap) in FIGURES.items():
        srcs = [p for ext in ("pdf", "png") if (p := FIG / f"{stem}.{ext}").exists()]
        out.append((label, "figure", srcs, cap, sec, bool(srcs)))
    for label, (stem, sec, cap) in TABLES.items():
        p = TAB / f"{stem}.csv"
        out.append((label, "table", [p] if p.exists() else [], cap, sec,
                    p.exists()))
    return out


def cited_in_text():
    """Labels actually cited in the manuscript body, excluding drafting notes."""
    found = set()
    for f in sorted(MANUSCRIPT.glob("section*.md")):
        body = f.read_text().split("## Drafting notes")[0]
        found |= set(re.findall(r"\b(?:Figure|Table)\s+S?\d+[a-z]?", body))
    return {s.replace("  ", " ") for s in found}


def main():
    check = "--check" in sys.argv
    items = collect()
    cited = cited_in_text()

    print(f"{'label':<11}{'kind':<8}{'§':<6}{'status':<10}source")
    missing, uncited = [], []
    for label, kind, srcs, _cap, sec, present in items:
        optional = needs_data(sec)
        if present:
            status = "ok"
        elif optional:
            status = "needs data"
        else:
            status = "ABSENT"
            missing.append(label)
        src = ", ".join(p.name for p in srcs) or "—"
        if label not in cited:
            uncited.append(label)
            status += " UNCITED"
        print(f"{label:<11}{kind:<8}{sec:<6}{status:<16}{src}")

    if not check:
        OUT.mkdir(parents=True, exist_ok=True)
        for label, _kind, srcs, _cap, _sec, _p in items:
            for p in srcs:
                shutil.copy2(p, OUT / f"{final_name(label)}{p.suffix}")

        lines = ["# Paper A — figure and table captions\n",
                 "Generated by `analysis/assemble_manuscript.py`. Numbering follows "
                 "order of first citation; edit the mapping there, not here.\n"]
        for kind, head in (("figure", "## Figures"), ("table", "## Tables")):
            lines.append(head + "\n")
            for label, k, srcs, cap, sec, present in items:
                if k != kind:
                    continue
                mark = "" if present else "  *(not generated — see data/README.md)*"
                lines.append(f"**{label}.** {cap} First cited §{sec.rstrip("*")}.{mark}\n")
        (MANUSCRIPT / "captions.md").write_text("\n".join(lines))
        print(f"\n  wrote {len(list(OUT.iterdir()))} files to "
              f"{OUT.relative_to(ROOT)}/ and manuscript/captions.md")

    optional_absent = [l for l, _k, s_, _c, sec, p_ in items
                       if not p_ and needs_data(sec)]
    print(f"\n  cited {len(cited)}   unexpectedly absent {len(missing)}   "
          f"uncited {len(uncited)}   awaiting data {len(optional_absent)}")
    if optional_absent:
        print(f"  awaiting data (expected on a clean clone): "
              f"{', '.join(optional_absent)}")
    if missing:
        print(f"  ABSENT  {', '.join(missing)}")
    if uncited:
        print(f"  UNCITED {', '.join(uncited)}")
    ok = not missing and not uncited
    if check:
        print("  PASS" if ok else "  FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
