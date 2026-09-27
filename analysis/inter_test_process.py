"""
Table S4: the zero-bias boundary is exactly phi-free under a Poisson inter-test
process and only approximately so under Pan's uniform variant (Supplement S.6).

Why this table exists. A rectangular recency WINDOW is an assay basis; a uniform
INTER-TEST distribution is a property of testing behaviour. Conflating the two is
the error that determined the sign of the predecessor manuscript's joint bias
factor, so the distinction is computed rather than asserted. See
docs/audit/computation_record.md section 5 and docs/PROVENANCE.md.

Two false generalisations are reported alongside, because both are tempting:

  * r* = Pr(S > c) holds only under Poisson. Under Uniform[0,3], P_0 = 0.8403
    while r* is about 0.90;
  * matching the MEAN gap does not match the boundary. Uniform[0,b] has mean gap
    b/2, and the mean-matched Poisson rate 2/b gives a materially different r*.
"""
import sys
import numpy as np
from _common import banner, write_table, C_PURPOSE
from src.eligibility_dynamics import gamma_phi, default_grid
from src.pan_composition import (r_star_general, PoissonInterTest,
                                 UniformInterTest, boundary_no_dynamics)

GRID = default_grid(4001)

# Six bases spanning the plausible MDRI range, including the two published Pan
# bases. Wide on purpose: a narrow span would make invariance look better than
# it is.
BASES = [(97, 180), (101, 194), (130, 220), (163, 260), (182, 290), (300, 400)]


def main():
    banner("Inter-test process vs assay basis")
    phis = [gamma_phi(w, h, GRID) for w, h in BASES]
    ones = np.ones_like(GRID)
    mdri = [p.mdri_days for p in phis]
    print(f"  {len(phis)} bases, MDRI {min(mdri):.0f}-{max(mdri):.0f} d "
          f"(integrated to T* = 2 y)\n")

    procs = [("Exponential, theta=1", PoissonInterTest(1.0)),
             ("Exponential, theta=0.844 (NHBS)", PoissonInterTest(0.8439)),
             ("Uniform[0,3]", UniformInterTest(3.0)),
             ("Uniform[0,4]", UniformInterTest(4.0))]

    rows = []
    print(f"{'inter-test model':<34}{'P_0':>8}{'r* range':>18}"
          f"{'spread':>9}{'rel':>8}  invariance")
    for name, proc in procs:
        rs = np.array([r_star_general(p, ones, C_PURPOSE, proc) for p in phis])
        spread = float(np.ptp(rs))
        rel = spread / rs.mean()
        if isinstance(proc, PoissonInterTest):
            kind = "exact (provable)"
            assert abs(rs.mean() - boundary_no_dynamics(proc.theta, C_PURPOSE)) < 1e-9
        else:
            kind = f"approximate, {rel * 100:.2f}%"
        print(f"{name:<34}{proc.P0(C_PURPOSE):>8.4f}"
              f"{f'{rs.min():.4f}-{rs.max():.4f}':>18}"
              f"{spread:>9.4f}{rel * 100:>7.2f}%  {kind}")
        rows.append([name, f"{proc.P0(C_PURPOSE):.4f}", f"{rs.min():.4f}",
                     f"{rs.max():.4f}", f"{spread:.5f}", f"{rel:.5f}", kind])

    write_table(rows, ["inter_test_model", "P0", "r_star_min", "r_star_max",
                       "spread", "relative_spread", "invariance"],
                "tableS4_inter_test_process.csv")

    phi = gamma_phi(163, 260, GRID)
    print("\n  Two false generalisations:")
    u3 = UniformInterTest(3.0)
    r_u = r_star_general(phi, ones, C_PURPOSE, u3)
    print(f"    r* = Pr(S>c)?  Uniform[0,3]: P_0 = {u3.P0(C_PURPOSE):.4f} but "
          f"r* = {r_u:.4f}  ({r_u - u3.P0(C_PURPOSE):+.4f})")
    matched = PoissonInterTest(u3.theta_equivalent)
    r_m = r_star_general(phi, ones, C_PURPOSE, matched)
    print(f"    mean gap enough? Uniform[0,3] mean gap 1.5 y -> Poisson "
          f"theta = {u3.theta_equivalent:.4f} gives r* = {r_m:.4f}  "
          f"({r_m - r_u:+.4f} vs the uniform process)")
    print("\n  Claim exactness only for the Poisson case.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
