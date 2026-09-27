"""Fixtures for the theorem-level suite."""
import json, sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.eligibility_dynamics import (                      # noqa: E402
    default_grid, gamma_phi, rectangular_phi, generator, S1_closed,
)

GRID = default_grid(1201)


@pytest.fixture(scope="session")
def phi_gamma():
    """Pan AJE basis, the default for empirical statements."""
    return gamma_phi(163, 260, GRID)


@pytest.fixture(scope="session")
def phi_pan_arxiv():
    """Pan arXiv basis: window 101 d / shadow 194 d -> shape 0.352, rate 1.273."""
    return gamma_phi(101, 194, GRID)


@pytest.fixture(scope="session")
def phi_rectangular():
    """Rectangular recency WINDOW -- an assay basis, not an inter-test process."""
    return rectangular_phi(180, GRID)


@pytest.fixture(scope="session")
def phi_cephia():
    """
    Stand-in for an empirically fitted phi with a deliberately different shape,
    so phi-independence claims are not tested against near-identical curves.
    """
    return gamma_phi(300, 400, GRID)


@pytest.fixture
def closed_form_S1():
    """(nstate) -> (Generator, analytic S1 callable). Only 2 and 3 are provided."""
    def build(nstate):
        if nstate == 2:
            alpha, beta, mu = 0.5, 11.4, 0.04
            q = alpha / (alpha + beta)
            Q = generator(q={"O": q}, betas={"O": beta}, mus={"E": mu, "O": mu})
            a = Q[0, 1]
            return Q, (lambda u: S1_closed(u, a, beta, mu, mu))
        if nstate == 3:
            mu = 0.03
            Q = generator(q={"J": 0.03, "P": 0.05},
                          betas={"J": 11.4, "P": 0.37},
                          mus={"E": mu, "J": mu, "P": mu})
            from scipy.linalg import expm
            M = np.asarray(Q)
            return Q, (lambda u: np.array([expm(M * x)[0, 0]
                                           for x in np.atleast_1d(u)]))
        raise ValueError("only 2- and 3-state analytic forms are implemented")
    return build


@pytest.fixture
def mixture_builder():
    """Stationary strata preserving a target mean occupancy. None = residual."""
    def build(q_mean, weights, multipliers):
        resid = [i for i, m in enumerate(multipliers) if m is None]
        fixed = [(w, m) for w, m in zip(weights, multipliers) if m is not None]
        q_res = {}
        for s, qm in q_mean.items():
            used = sum(w * m * qm for w, m in fixed)
            wr = sum(weights[i] for i in resid)
            q_res[s] = (qm - used) / wr if wr else 0.0
            if q_res[s] < 0:
                pytest.skip("infeasible mixture")
        out = []
        for w, m in zip(weights, multipliers):
            q = {s: (q_res[s] if m is None else m * q_mean[s]) for s in q_mean}
            if sum(q.values()) >= 0.95:
                pytest.skip("infeasible mixture")
            pi = {"E": 1.0 - sum(q.values()), **q}
            Q = generator(q=q, betas={"J": 11.4, "P": 0.37},
                          mus={k: 0.0 for k in ("E", *q)})
            out.append((w, pi, Q, 1.0))
        return out
    return build


def _cephia_paths():
    return sorted(ROOT.glob("data/cephia_public_use_dataset_*.csv"))


def _has_local_cephia() -> bool:
    return bool(_cephia_paths())


@pytest.fixture
def local_cephia_csv():
    if not _has_local_cephia():
        pytest.skip("CEPHIA dataset not retrieved; see data/README.md")
    return _cephia_paths()[0]


@pytest.fixture
def cephia_expected():
    p = ROOT / "data" / "fixtures" / "cephia_expected.json"
    if not p.exists():
        pytest.skip("cephia_expected.json absent; run analysis/empirical_phi.py")
    return json.loads(p.read_text())
