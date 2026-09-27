# Prototypes

Working scripts from the post-review reanalysis, carried over for reference. They are
**not** the paper's implementation: they predate the frozen theory in
`manuscript/section2_theory.md` and several embed superseded assumptions.

| file | status |
|---|---|
| `derive_s.py` | three-state `S_1(u)` closed form and `rho` — survives; fold into `src/eligibility_dynamics.py` |
| `mc_removal.py` | individual-level simulator to Pan Supp S.5 — survives; note the independent-seeds requirement |
| `lel_removal.py` | generalised LEL, validated against Pan Table 1 — survives |
| `lel_removal_cephia.py` | `r*` across recency bases including empirical phi — survives |
| `xcheck_xsrecency.py` | CEPHIA MDRI by logit-GEE — survives |

**All five assume the restricted numerator** (`eta_k = 0` outside `E`) and a single
unobservable state. Rewrite against Theorem 1 rather than copying. This directory should be
deleted once `src/` is complete.
