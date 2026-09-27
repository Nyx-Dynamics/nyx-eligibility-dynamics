"""
Recover Pan et al. (AJE 2026) Table 1 by setting w == 1.

This is the null check for the composition in manuscript 2.7: with no
eligibility dynamics the generalised limiting error must equal their published
expression. Uses the arXiv basis (window 101 d / shadow 194 d) because that is
what their table was computed on.
"""
from _common import banner, phi_for, write_table
import numpy as np
from src.pan_composition import lel

LAM = 0.032
PUBLISHED = [  # c, theta, r, published bias x 1e-3
    (0.00, 1.0, 0.0, -9.95), (0.00, 1.0, 0.6, -3.98), (0.00, 2.0, 0.0, -15.03),
    (0.25, 1.0, 0.0, -5.93), (0.25, 1.0, 0.6, -1.36), (0.25, 1.0, 1.0, 1.68),
    (0.25, 2.0, 0.0, -8.97), (0.25, 2.0, 0.6, -0.10), (0.25, 2.0, 1.0, 5.82),
]


def main():
    banner("Pan et al. Table 1 recovery (w == 1), arXiv basis 101/194")
    phi = phi_for("pan_arxiv")
    ones = np.ones_like(phi.grid)
    rows, worst = [], 0.0
    print(f"{'c':>5}{'theta':>7}{'r':>5}{'computed':>11}{'published':>11}{'diff':>9}")
    for c, th, r, pub in PUBLISHED:
        got = 1e3 * LAM * (np.exp(lel(phi, ones, r=r, c=c, theta=th)) - 1)
        d = got - pub
        worst = max(worst, abs(d))
        print(f"{c:>5.2f}{th:>7.1f}{r:>5.1f}{got:>11.2f}{pub:>11.2f}{d:>9.3f}")
        rows.append([c, th, r, f"{got:.3f}", pub, f"{d:.4f}"])
    print(f"\n  max |diff| = {worst:.4f} x 1e-3   (tolerance 0.05)")
    assert worst < 0.05, "Pan recovery outside tolerance"
    write_table(rows, ["c", "theta", "r", "computed_x1e3", "published_x1e3", "diff"],
                "table1_pan_recovery.csv")


if __name__ == "__main__":
    main()
