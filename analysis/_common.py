"""Shared setup for analysis entry points."""
from __future__ import annotations
import csv, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
from src.eligibility_dynamics import gamma_phi, default_grid          # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT / "outputs" / "tables"
FIGURES = ROOT / "outputs" / "figures"

# Created on import, for every entry point. Rendered figures are not tracked, so
# a fresh clone has no outputs/figures at all; leaving each script to mkdir for
# itself meant the directory existed only if one of the scripts that happened to
# do so had already run. That is a clean-tree-only failure, which is exactly the
# kind a developer never sees.
for _d in (TABLES, FIGURES):
    _d.mkdir(parents=True, exist_ok=True)

# Bases used throughout. 163/260 is the Pan AJE basis and is the DEFAULT for
# empirical statements; 101/194 is the Pan arXiv basis and is used only where a
# published number must be reproduced.
BASES = {
    "pan_aje":    (163, 260),
    "pan_arxiv":  (101, 194),
    "sedia_like": (173, 306),
}
DEFAULT_BASIS = "pan_aje"

# Sourced parameters. Provenance in docs/audit/computation_record.md.
THETA_NHBS = float(-np.log(1 - 0.57))   # NHBS 2018: 57% tested in past 12 mo
C_PURPOSE = 0.25                        # PURPOSE 90-day testing exclusion
MU_PWID = 0.040                         # ALIVE all-cause, adult PWID
BETA_JAIL = 365.25 / 32.0               # BJS mean jail stay 32 d
BETA_PRISON = 1.0 / 2.7                 # BJS mean time served ~2.7 y
MU_CUSTODY = 0.002                      # BJS in-custody mortality; non-influential


def phi_for(name: str = DEFAULT_BASIS, n: int = 2001):
    w, s = BASES[name]
    return gamma_phi(w, s, default_grid(n))


def write_table(rows, header, name: str) -> Path:
    p = TABLES / name
    with p.open("w", newline="") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(header)
        wr.writerows(rows)
    print(f"  wrote {p.relative_to(ROOT)}")
    return p


def banner(title: str):
    print(f"\n{title}\n{'-' * len(title)}")
