# ESTIMAND.md

**What $\lambda$ denotes, and why it is the thing most easily got wrong.**

If you have arrived from `nyx-kassanjee-letter`, this is the document to read first. The single most consequential change between that work and this one is not a parameter value or a correction factor — it is what the target quantity *is*. Everything else follows from getting this right.

---

## 1. The target

$$
\boxed{\;\lambda_E(t) \;=\; \text{HIV incidence per unit \textbf{observable susceptible} person-time at calendar time } t\;}
$$

"Observable" means: alive, resident in the catchment population, and reachable for trial screening. In the notation of Gao & Bannick (*Stat Med* 2022;41:1446–61) this is their $\lambda(t)$, defined conditional on eligibility $A(t)=1$.

This is the quantity a counterfactual-placebo design requires, because trial enrollees are drawn from the observable population. It is **not** incidence among everyone who was at risk, and it is **not** incidence among everyone alive.

## 2. The state space, and where $A(t)$ comes from

We do not replace Gao & Bannick's eligibility indicator; we refine it. Let $Z(t)$ be a process on

$$
\mathcal{S} = \mathcal{L}\cup\{X\},
\qquad
\mathcal{L} = \{E,\,O_1,\dots,O_m\},
$$

- $E$ — **observable**, as above;
- $O_j$ — **temporarily unobservable** living states permitting return to $E$: custody, long-distance displacement, prolonged hospitalisation;
- $X$ — **absorbing**: death or permanent departure from the catchment.

Then

$$
A(t) = \mathbb{1}\{Z(t) = E\}.
$$

Eligibility is the $E$-marginal of a richer process. Every quantity Gao & Bannick define — $\varphi(u)$, $\Omega_{T^*}$, $\beta_{T^*}$, $\lambda(t)$, $p(t)$ — keeps its definition unchanged. The only new primitive is $Z(t)$.

## 3. State-specific acquisition, and $\eta$

Acquisition can occur in any living state. Write $\lambda_k(\tau)$ for the acquisition hazard per susceptible person-time in state $k\in\mathcal{L}$, and define the **relative acquisition hazards**

$$
\eta_k(\tau) = \frac{\lambda_k(\tau)}{\lambda_E(\tau)},
\qquad
\eta_E \equiv 1 .
$$

$\eta$ is the parameter whose absence caused the error documented in the predecessor repository. A model written only in terms of infections originating in $E$ is the special case $\eta_k = 0$ for all $k\neq E$ — a substantive empirical claim (nobody acquires HIV in custody) rather than a modelling convenience, and one that is not supported.

## 4. Three quantities that are easy to conflate

| symbol | is | is not |
|---|---|---|
| $\varphi(u)$ | probability of testing recent at duration $u$, **given observable at survey** | Kassanjee's $P_R(u)$, which also contains eligibility survival |
| $s_t(u)$ | transition-and-acquisition weight: $\sum_k \pi_k(t-u)\eta_k(t-u)[P_1(u)]_{kE} / \pi_E(t-u)$ | a survival probability; it can exceed 1 when some $\eta_k>1$ |
| $g_E(u;t)$ | source-evolution factor $n_{0E}(t-u)/n_{0E}(t)$ | a property of individuals; it is a property of the pool |

Their product is the **historical observability weight** $w_t(u) = s_t(u)\,g_E(u;t)$, and the estimator's probability limit is $\int\varphi w_t / \Omega_{T^*}$.

**$w_t$ is a weight, not a transition probability.** It incorporates $\eta_k$ and demographic scaling and may exceed one. Do not draw it over a transition arrow.

## 5. Two stationarities, which are different

Because conflating them was an actual error in drafting:

- **State stationarity**: $\boldsymbol\pi^{\!\top}Q = \mathbf{0}^{\!\top}$. Living-state *proportions* are stable. Gives $s_t(u)\equiv1$ under $\eta\equiv1$.
- **Demographic stationarity**: $g_E(u;t)\equiv1$. The observable susceptible pool's *total* is stable.

A composition-stable pool growing at rate $\rho$ satisfies the first and not the second: $s_t\equiv1$ but $g_E = e^{-\rho u}$, so $w_t\not\equiv1$ and the estimator is biased. Both conditions are required for exact cancellation.

## 6. What this estimand does *not* commit you to

Two questions are frequently assumed to be the same and are not:

1. **Does eligibility loss create bias?** Not by itself. Transient movement cancels exactly under the conditions above.
2. **Is the estimand the one you want?** Separate question. $\lambda_E$ excludes person-time spent unobservable. A design whose target included acquisition during incarceration would need $\lambda_J,\lambda_P$ in the estimand itself, not merely as nuisance parameters. Either choice is defensible; it must be stated.

## 7. Relation to adjacent frameworks

| | addresses | relation |
|---|---|---|
| Gao & Bannick 2022 | formal assumptions of the cross-sectional estimator; $A(t)$ as a primitive | We refine $A(t)$; their Theorem 2 is our Corollary 1 |
| Pan, Bannick & Gao 2026 | selective screening attendance $Q$, testing-based exclusion $C$, among those present at $t$ | Their operators act **downstream** of $w_t(u)$; their expression is ours at $w_t\equiv1$ |
| Wang, Duerr & Gao 2025 | differing baseline covariate distributions between sampled and target populations | Removes the *compositional* component of bias; leaves the within-stratum duration component of $w_t$ |

The three are composable, not competing. They address heterogeneity **among** observable individuals, selection **at** the screening interface, and evolution **of** observability respectively.

---

*See `docs/ASSUMPTIONS.md` for the numbered assumption set (E.1–E.3, and the inherited A/B/C/D), and the manuscript §2 for statements and proofs.*
