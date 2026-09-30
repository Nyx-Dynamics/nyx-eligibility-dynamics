"""
Table S2: can covariate reweighting absorb the eligibility weight?

Wang, Duerr & Gao (Stat Med 2025) transport incidence between populations
differing in baseline covariates X by reweighting. Their estimator is

    lambda_0 = sum_i w_i pos_i (rpos_i - beta)
             / sum_i w_i (1 - pos_i) (Omega - beta T),

with w_i the predicted probability of trial membership from a logistic
regression on covariates, fitted among the HIV-negative. Structure checked
against their own implementation (github.com/qii-wang/
HIV-incidence-recency-heterogeneity, Simulation/Internal target population),
not inferred from the paper text.

Two features of that structure drive everything below. The weight multiplies the
numerator AND the denominator, so it cancels wherever it is constant. And it is a
function of measured covariates only, so it moves mass BETWEEN strata and can do
nothing WITHIN one.

The model here is the stratified idealisation of exactly that: reweighting can
replace the sampled composition g by the target composition h, but each stratum
keeps its own duration factor D_x. Where the two compositions coincide -- the
counterfactual-placebo case, in which the target population IS the trial
population -- the weight is constant, cancels, and reweighting removes exactly
nothing.

This is a statement about which problem each method solves, not a deficiency:
D_x < 1 in every stratum, so no weighted average of them reaches 1, and no
estimator that reweights on X alone could make it.
"""
from _common import banner, phi_for, write_table
import numpy as np
from src.eligibility_dynamics import generator, historical_weight, plim_ratio

MU = {0: 0.010, 1: 0.080}
LAM = {0: 0.020, 1: 0.060}


def D(phi, x):
    Q = generator(q={}, betas={}, mus={"E": MU[x]})
    return plim_ratio(phi, historical_weight(Q, pi={"E": 1.0}, eta={"E": 1.0},
                                             grid=phi.grid))


def main():
    banner("Wang-style reweighting vs the duration component")
    phi = phi_for()
    d = {x: D(phi, x) for x in (0, 1)}
    print(f"  within-stratum deflation:  D_0 = {d[0]:.4f}   D_1 = {d[1]:.4f}\n")
    cases = [("same X distribution (counterfactual-placebo case)",
              {0: .5, 1: .5}, {0: .5, 1: .5}),
             ("target enriched for high-removal", {0: .8, 1: .2}, {0: .3, 1: .7}),
             ("target enriched for low-removal", {0: .3, 1: .7}, {0: .8, 1: .2})]
    rows = []
    print(f"{'case':<48}{'truth':>9}{'naive':>9}{'Wang':>9}{'removed':>10}")
    for label, g, h in cases:
        truth = sum(h[x] * LAM[x] for x in (0, 1))
        naive = (sum(g[x] * LAM[x] * d[x] for x in (0, 1)) / sum(g.values()))
        wang = sum(h[x] * LAM[x] * d[x] for x in (0, 1))
        bn, bw = naive / truth - 1, wang / truth - 1
        removed = 0.0 if abs(bn) < 1e-12 else 100 * (1 - abs(bw) / abs(bn))
        print(f"{label:<48}{truth:>9.5f}{naive:>9.5f}{wang:>9.5f}{removed:>9.1f}%")
        rows.append([label, f"{truth:.5f}", f"{naive:.5f}", f"{wang:.5f}",
                     f"{bn:+.4f}", f"{bw:+.4f}", f"{removed:.1f}"])
    print("\n  Reweighting corrects composition, never the within-stratum duration")
    print("  component: D_x < 1 in every stratum, so any weighted average is < 1.")
    write_table(rows, ["case", "truth", "naive", "wang_reweighted",
                       "naive_bias", "wang_bias", "pct_removed"],
                "tableS2_wang_comparator.csv")


if __name__ == "__main__":
    main()
