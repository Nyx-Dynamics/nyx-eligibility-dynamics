"""
r* threshold for Pan et al. (AJE 2026) LEL with post-infection observability s(u),
evaluated on FOUR recency bases: three parametric gammas + an empirical CEPHIA phi.

r*(gamma)   = selective-attendance ratio at which LEL = 0.
r*(gamma=0) = exp(-theta*c) exactly, independent of phi  (from Pan Supp S.7.1).
r* > 1      => underestimation for EVERY r <= 1, i.e. Pan's Table 1 "?" cell resolved.

CEPHIA public-use dataset: Zenodo 10.5281/zenodo.4900634
Gamma construction matches XSRecency::get.gamma.params (365.25 d/yr):
    shape = W/(2H - W), rate = 1/(2H - W)     W = window/MDRI, H = shadow
"""
import numpy as np, pandas as pd
from scipy import stats
from scipy.optimize import brentq
from sklearn.isotonic import IsotonicRegression

YR, TSTAR = 365.25, 2.0
U = np.linspace(0.0, TSTAR, 4001)

def gamma_phi(window_d, shadow_d):
    W, H = window_d / YR, shadow_d / YR
    rate = 1.0 / (2 * H - W)
    return 1 - stats.gamma.cdf(U, W * rate, scale=1 / rate)

def cephia_phi(csv, recent=lambda df: df["ODn"] < 1.5):
    """Empirical monotone phi(u) from LAg-Sedia ODn, treatment-naive, non-elite-controller."""
    cols = ["assay", "assay_result_field", "assay_result_value", "days_since_eddi",
            "on_treatment_at_visit", "viral_load_closest_to_visit",
            "ever_designated_as_elite_controller"]
    df = pd.read_csv(csv, usecols=cols, low_memory=False)
    df = df[(df.assay == "LAg-Sedia") & (df.assay_result_field == "ODn")].copy()
    df["ODn"] = pd.to_numeric(df.assay_result_value, errors="coerce")
    df["u_d"] = pd.to_numeric(df.days_since_eddi, errors="coerce")
    df["vl"] = pd.to_numeric(df.viral_load_closest_to_visit, errors="coerce")
    df = df.dropna(subset=["ODn", "u_d"])
    df = df[(df.u_d >= 0) & (~df.on_treatment_at_visit.astype(bool))
            & (~df.ever_designated_as_elite_controller.astype(bool))]
    iso = IsotonicRegression(increasing=False, out_of_bounds="clip")
    iso.fit(df.u_d.values / YR, recent(df).astype(int).values)
    return np.clip(iso.predict(U), 0, 1), len(df)

def summarise(phi):
    Om = np.trapezoid(phi, U)
    return Om * YR, np.trapezoid(U * phi, U) / Om * YR      # MDRI (d), shadow (d)

def LEL(phi, r, c, theta, gamma):
    """Pan Supp S.7.1 generalised with observability s(u) = exp(-gamma*u)."""
    s = np.exp(-gamma * U)
    Om, Oms = np.trapezoid(phi, U), np.trapezoid(phi * s, U)
    m = U >= c
    K = np.trapezoid((phi * s * (1 - np.exp(theta * (c - U))))[m], U[m])
    return np.log(Oms - (1 - r * np.exp(theta * c)) * K) - np.log(Om)

def r_star(phi, c, theta, gamma):
    try:
        return brentq(lambda r: LEL(phi, r, c, theta, gamma), 0, 12)
    except ValueError:
        return float("nan")

if __name__ == "__main__":
    import sys
    bases = {"gamma 101/194 (Pan arXiv)": gamma_phi(101, 194),
             "gamma 163/260 (Pan AJE)":   gamma_phi(163, 260),
             "gamma 173/306 (Sedia-like)": gamma_phi(173, 306)}
    if len(sys.argv) > 1:                      # path to cephia CSV
        phi, n = cephia_phi(sys.argv[1])
        bases[f"CEPHIA empirical (n={n})"] = phi

    print(f"{'basis':<28}{'MDRI d':>8}{'shadow d':>10}")
    for lab, phi in bases.items():
        print(f"{lab:<28}" + "%8.1f%10.1f" % summarise(phi))

    print(f"\nr* at c=0.25 y   (r*>1 means underestimation for every r<=1)")
    print(f"{'basis':<28}{'theta':>6}{'g=0':>8}{'g=.05':>8}{'g=.10':>8}{'g=.20':>8}")
    for lab, phi in bases.items():
        for th in (0.5, 1.0, 2.0):
            row = "".join("%8.3f" % r_star(phi, 0.25, th, g) for g in (0, .05, .10, .20))
            print(f"{(lab if th == 0.5 else ''):<28}{th:>6.1f}{row}")
    print(f"\ntheory, g=0, any phi: " + " / ".join("%.3f" % np.exp(-t*0.25) for t in (0.5,1,2)))
