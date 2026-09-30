# Paper A — Section 2: Theory (rev. 5)

**Title:** Temporary Loss of Eligibility and Bias in Cross-Sectional HIV Incidence Estimation

Notation follows Gao & Bannick (*Stat Med* 2022;41:1446–61) throughout. Their eligibility indicator is refined, not replaced. Rev. 2 (26 Sep 2026): general historical composition in Theorem 2; $w_t(u)$ propagated into §2.7; Corollary 5 asymptotics corrected; FRR and Wang claims narrowed; dimensional ambiguity removed; proofs added. Rev. 3 (26 Sep 2026): sampling factor $\kappa_t$ added to Theorem 1; demographic stationarity separated from state stationarity in Corollaries 1–2; Remark 1 double-counting claim narrowed; failure-mode count scoped and M4 split; implications 1 and 3 reworded; $w_t$ removed from the transition arrow; Remark 5 stated in terms of $\Omega_w$ rather than pointwise $w_t$. Rev. 4 (26 Sep 2026): neutral sampling named in Theorem 1's hypothesis; $\beta_{T^*}=0$ inherited explicitly in Theorem 2. Rev. 5 (30 Sep 2026): unfrozen and aligned with the positioning settled for §§1, 3 and 5 — Remark 4a states the $\varphi$-independence of Corollary 2 explicitly, and §2.1 states the additive-extension claim in the form the rest of the paper uses.

---

## 2. Theory

### 2.1 Notation, state space, and estimand

Let $T$ be the calendar time of HIV infection and $t$ the calendar time of cross-sectional sampling, and write $U = t-T$ for infection duration. Following Gao & Bannick, let $A(t)$ indicate eligibility at $t$ — whether the individual would be eligible for inclusion in a cross-sectional survey of the target population, a minimum requirement being that they are alive.

We refine $A(t)$ rather than redefine it. The estimand, the recency function and the assumptions of the established framework are retained unchanged; the only new primitive is the process $Z(t)$ below, and setting that process inert recovers the existing results exactly (Corollary 1). The extension is therefore additive rather than alternative, and it is an extension in the formal treatment of eligibility — not in assay calibration, which Remark 4a shows is not load-bearing here. Let $Z(t)$ be a stochastic process on

$$
\mathcal{S} = \mathcal{L}\cup\{X\}, \qquad \mathcal{L}=\{E, O_1,\dots,O_m\},
$$

where

- $E$ — **observable**: alive, resident in the catchment, reachable for trial screening;
- $O_1,\dots,O_m$ — **temporarily unobservable** living states permitting return to $E$ (custody, long-distance displacement, prolonged hospitalisation);
- $X$ — **absorbing**: death or permanent departure from the catchment.

Gao & Bannick's indicator is the $E$-marginal of this process:

$$
A(t) = \mathbb{1}\{Z(t)=E\}.
$$

Their definitions carry over unchanged: $\varphi(u) = \Pr(M\in\mathcal{R}\mid T=t-u,\,A(t)=1)$ is the duration-specific test-recent probability, $\Omega_{T^*}=\int_0^{T^*}\varphi(u)\,du$ the mean duration of recent infection, $\beta_{T^*}$ the false-recency rate, and

$$
\lambda(t)=\Pr(T=t\mid T\ge t,\,A(t)=1),\qquad p(t)=\Pr(T\le t\mid A(t)=1).
$$

**Remark 1 (why $\varphi$, not $P_R$).** Gao & Bannick's Remark 1 notes that Kassanjee's original window period is $\int_0^{T^*}P_R(u)\,du$ with

$$
P_R(u)=\Pr\big(A(t)=1,\ M\in\mathcal{R}\mid T=t-u,\ A(t-u)=1\big),
$$

which embeds an eligibility-survival component, whereas $\varphi(u)$ conditions on $A(t)=1$ and does not. We adopt $\varphi$, so that eligibility dynamics appear **once**, explicitly, in the transition process of §2.2. Because $\varphi$ conditions on eligibility at $t$, eligibility dynamics must enter separately through the population transition process — multiplying $\varphi$ by a transition weight is precisely how Theorem 1 does so. The error to avoid is doing both: once the transition is represented explicitly through $P_1(u)$ or $w_t(u)$, additionally replacing $\Omega_{T^*}$ by a survival-deflated window counts the same process twice.

**Estimand.** We target

$$
\lambda_E(t) = \text{HIV incidence per unit observable susceptible person-time at } t,
$$

Gao & Bannick's $\lambda(t)$ under the refinement above, and the quantity a counterfactual-placebo design requires, since trial enrollees are drawn from $\{Z(t)=E\}$. Where state-specific acquisition hazards differ, write $\lambda_k(\tau)$ for state $k\in\mathcal{L}$ and define **relative acquisition hazards**

$$
\eta_k(\tau) = \lambda_k(\tau)/\lambda_E(\tau), \qquad \eta_E\equiv 1 .
$$

### 2.2 The eligibility-transition process

Let $Q_0,Q_1$ be the generators of $Z(\cdot)$ before and after infection, each on $\mathcal{S}$ with $X$ absorbing, and let $P_1(u)=\exp(Q_1u)$. Define the **return vector** restricted to living states,

$$
\mathbf{p}_E(u) = \big([P_1(u)]_{kE} : k\in\mathcal{L}\big)^{\!\top},
$$

and collect susceptible counts over living states only,

$$
\mathbf{n}_0(\tau) = \big(n_{0k}(\tau):k\in\mathcal{L}\big)^{\!\top},
\qquad
\boldsymbol\lambda(\tau)=\big(\lambda_k(\tau):k\in\mathcal{L}\big)^{\!\top}.
$$

Restricting to $\mathcal{L}$ avoids any question of susceptible person-time in the absorbing state.

> **Assumption E.1 (Markov movement).** $Z(\cdot)$ is a time-homogeneous Markov jump process on $\mathcal{S}$ with $X$ absorbing.
>
> **Assumption E.2 (path-independent assay response).** Given $U=u$ and $Z(t)=E$, the assay response is independent of $\{Z(s):s<t\}$: $\varphi(u)$ does not depend on the route by which the individual reached $E$.
>
> **Assumption E.3 (infection-independent movement).** $Q_1=Q_0$.

E.1 concerns memory structure; E.3 concerns whether infection alters the transition law. They are stated separately because they fail differently and because M3 in §2.6 requires E.3 to have an identity of its own.

**Remark 2 (scope of E.1).** E.1 is not required for the cancellation result to survive unobserved heterogeneity in movement propensity: Corollary 3 permits arbitrary mixtures of stationary Markov strata, whose marginal process need not itself be Markov. A general semi-Markov or history-dependent treatment is beyond the present scope.

### 2.3 The generalised recent-count identity

**Theorem 1.** *Under E.1–E.2, neutral cross-sectional sampling with inclusion probability $\kappa_t$ common to observable HIV-positive and HIV-negative individuals, and $\beta_{T^*}=0$ so that $\varphi(u)=0$ for $u>T^*$,*

$$
\boxed{\;
\mathbb{E}[N_{\mathrm{rec}}(t)]
=
\kappa_t\!\int_0^{T^*}\!
\varphi(u)\;
\mathbf{n}_0(t-u)^{\!\top}\mathrm{diag}\big(\boldsymbol\lambda(t-u)\big)\,\mathbf{p}_E(u)
\;du,
\qquad
\mathbb{E}[N_-(t)] = \kappa_t\, n_{0E}(t),
\;}
$$

*where $\kappa_t\in(0,1]$ is the probability that an observable individual is included in the cross-sectional sample, assumed common to HIV-positive and HIV-negative observable individuals.*

*Proof.* Consider susceptibles in living state $k$ during $[t-u-\mathrm{d}u,\,t-u)$. Their number is $n_{0k}(t-u)$ and each acquires infection in that interval with probability $\lambda_k(t-u)\,\mathrm{d}u + o(\mathrm{d}u)$, so the expected number of incident infections in state $k$ is $n_{0k}(t-u)\lambda_k(t-u)\,\mathrm{d}u$. By E.1 each such individual occupies state $\ell$ at $t$ with probability $[P_1(u)]_{k\ell}$; those with $\ell=E$ satisfy $A(t)=1$ and are eligible for sampling. By E.2 each eligible individual of duration $u$ is classified test-recent with probability $\varphi(u)$, irrespective of path. Each observable individual enters the sample with probability $\kappa_t$. Summing over $k\in\mathcal{L}$ gives integrand $\kappa_t\varphi(u)\sum_{k}n_{0k}(t-u)\lambda_k(t-u)[P_1(u)]_{kE}$; integrating over $u\in[0,T^*)$ and using $\varphi(u)=0$ beyond $T^*$ yields the first identity. The second holds because the HIV-negative sample is drawn from susceptibles with $Z(t)=E$, each included with the same probability $\kappa_t$. $\blacksquare$

Because $\kappa_t$ multiplies both expectations it cancels in Theorem 2, and the stage separation is preserved: population dynamics, then neutral cross-sectional sampling, then $Q$, then $C$. Selection that is *not* neutral between observable positives and negatives is Pan's $Q$, treated in §2.7, not $\kappa_t$.

Expanded, the integrand is

$$
\lambda_E n_{0E}(t-u)[P_1(u)]_{EE}
+\sum_{j=1}^{m}\lambda_{O_j} n_{0O_j}(t-u)[P_1(u)]_{O_jE},
$$

so the observed recent count receives contributions from infections acquired in **every** living state, weighted by the probability of having returned to $E$ by $t$. Infections acquired while temporarily unobservable and followed by re-entry are counted; infections acquired in $E$ and followed by exit are not.

**Remark 3 (false recency).** The principal results below are derived for $\beta_{T^*}=0$. With $\beta_{T^*}>0$ the identity acquires an additive term $\beta_{T^*}\mathbb{E}\big[N_+^{(U>T^*)}\big]$ and the adjusted estimator's denominator becomes $\Omega_{T^*}-\beta_{T^*}T^*$; the corresponding expressions are given in the supplement. We make no general claim that nonzero FRR is innocuous once the selection processes of §2.7 are composed. We note only that a bias factor reported as a ratio of mean durations alone, rather than of $(\Omega_{T^*}-\beta_{T^*}T^*)$ terms, is incorrect for the adjusted estimator.

**Remark 4 (both sides of the population process).** Theorem 1 addresses the objection that eligibility dynamics act on the HIV-negative denominator as well as on recent positives. Both appear explicitly: the numerator integrates $\mathbf{n}_0(t-u)$ across the recency window, the denominator evaluates $n_{0E}$ at $t$. No cancellation is assumed; whether one occurs is settled in §2.5.

### 2.4 Probability limit of the adjusted estimator

Define the **transition–acquisition weight** and the **source-evolution factor**

$$
s_t(u)
=
\frac{\displaystyle\sum_{k\in\mathcal{L}}\pi_k(t-u)\,\eta_k(t-u)\,[P_1(u)]_{kE}}{\pi_E(t-u)},
\qquad
g_E(u;t)=\frac{n_{0E}(t-u)}{n_{0E}(t)},
$$

with $\pi_k(\tau)=n_{0k}(\tau)/\sum_{\ell\in\mathcal{L}}n_{0\ell}(\tau)$, and let

$$
\boxed{\;w_t(u) = s_t(u)\,g_E(u;t)\;}
$$

be the **historical observability weight**.

**Theorem 2.** *Under the conditions of Theorem 1 — in particular $\beta_{T^*}=0$ — together with Gao & Bannick's assumptions A.1–A.2 (snapshot) or B.1–B.2 (adjusted), and local constancy of $\lambda_E$ over $[t-T^*,t]$,*

$$
\boxed{\;
\frac{\hat\lambda}{\lambda_E}
\;\xrightarrow{\;p\;}\;
\frac{\displaystyle\int_0^{T^*}\varphi(u)\,w_t(u)\,du}{\Omega_{T^*}}
\;}
$$

*and $\hat\lambda$ is consistent for $\lambda_E(t)$ if and only if the $\varphi$-weighted average of $w_t$ equals one.*

*Proof.* By Theorem 1 and the law of large numbers, $\hat\lambda \to \mathbb{E}[N_{\mathrm{rec}}]/(\mathbb{E}[N_-]\,\Omega_{T^*})$, in which $\kappa_t$ cancels. Write $n_{0k}(t-u)=N_0(t-u)\pi_k(t-u)$ with $N_0=\sum_{\ell\in\mathcal{L}}n_{0\ell}$, and $\lambda_k(t-u)=\lambda_E\eta_k(t-u)$ using local constancy of $\lambda_E$. Then

$$
\mathbb{E}[N_{\mathrm{rec}}]
=\lambda_E\!\int_0^{T^*}\!\!\varphi(u)N_0(t-u)\sum_{k}\pi_k(t-u)\eta_k(t-u)[P_1(u)]_{kE}\,du .
$$

Substituting $N_0(t-u)=n_{0E}(t-u)/\pi_E(t-u)$ gives $N_0(t-u)\sum_k(\cdot) = n_{0E}(t-u)\,s_t(u)$, and dividing by $\mathbb{E}[N_-]=n_{0E}(t)$ converts $n_{0E}(t-u)$ to $g_E(u;t)$. $\blacksquare$

**Corollary 0 (constant-growth special case).** If the living-state composition is stable over the window and $n_{0E}$ grows at constant rate $\rho$, then $s_t(u)=s(u)$ with $\pi$ evaluated anywhere in the window and $g_E(u;t)=e^{-\rho u}$, so $w_t(u)=s(u)e^{-\rho u}$.

This is the form used in the empirical sections. The general statement is retained in Theorem 2 because composition drift is itself one of the bias mechanisms (M4), and factorising $\pi$ at $t$ would assume it away.

### 2.5 Corollaries

**Corollary 1 (Gao–Bannick recovery).** If $\mathcal{L}=\{E\}$ and $Q_1$ has no transitions, then $s_t(u)\equiv1$ and $w_t(u)=g_E(u;t)$. If in addition the observable susceptible pool is demographically stationary, $g_E\equiv1$, then $w_t\equiv1$ and $\hat\lambda\to\lambda_E$, recovering Gao & Bannick's Theorem 2 under their Assumption C — which supplies the equivalent stability condition.

**Corollary 2 (exact cancellation under transient movement).** *Suppose that*

1. *the movement process is **state-stationary**: $\boldsymbol\pi^{\!\top}Q_1=\mathbf{0}^{\!\top}$, so living-state proportions are stable;*
2. *the observable susceptible pool is **demographically stationary**: $g_E(u;t)\equiv1$;*
3. *acquisition is state-invariant, $\eta_k\equiv1$;*
4. *movement is infection-independent (E.3);*
5. *there is no absorbing loss.*

*Then $\hat\lambda\to\lambda_E$ exactly.*

*Proof.* By (1), (4) and (5), $\boldsymbol\pi^{\!\top}P_1(u)=\boldsymbol\pi^{\!\top}$ for all $u\ge0$. With (3),

$$
s_t(u)=\frac{\boldsymbol\pi^{\!\top}P_1(u)\mathbf{e}_E}{\pi_E}=\frac{\pi_E}{\pi_E}=1 ,
$$

and by (2) $g_E\equiv1$, so $w_t\equiv1$. Theorem 2 then gives $\hat\lambda\to\lambda_E$. $\blacksquare$

Conditions (1) and (2) are distinct and both are required. State-stationarity fixes the *proportions* occupying $E,O_1,\dots,O_m$; it does not fix the *total*. A susceptible pool whose composition is stable but whose size grows at rate $\rho$ has $s_t\equiv1$ but $g_E(u;t)=e^{-\rho u}$, hence $w_t\not\equiv1$ and the estimator is biased — the case isolated as M4 in §2.6.

**Movement into and out of temporarily unobservable states does not, by itself, bias the estimator.** The loss of individuals infected in $E$ and unobservable at $t$ is offset exactly by individuals infected while unobservable who have returned to $E$ by $t$. Stationarity suffices — detailed balance is not required — so the result concerns transient or bidirectional movement, not reversibility.

**Remark 4a (the cancellation does not depend on the assay).** Corollary 2 gives $\hat\lambda/\lambda_E=1$ whenever $w_t\equiv1$, and $w_t$ is a property of the population process alone: it contains no assay quantity. The conclusion therefore holds for **every admissible recency function** — any $\varphi$ satisfying A.1–A.2 or B.1–B.2 — and for every value of $\Omega_{T^*}$. No mean duration of recent infection is load-bearing for the result.

This matters for what must be defended. A claim resting on a particular calibration inherits every dispute about that calibration, and the recency literature has two distinct lineages whose values differ by roughly forty per cent (§3.2). Corollary 2 is insulated from that disagreement by construction: $\varphi$ enters Theorem 2 only through $\Omega_w/\Omega_{T^*}$, which is unity when $w_t\equiv1$ regardless of the shape of $\varphi$. Where $\varphi$ does matter is in the *magnitude* of departures once a condition fails, and in the boundary of §2.7 — and even there Remark 5 shows the boundary itself is $\varphi$-free under a Poisson testing process.

**Corollary 3 (unobserved heterogeneity in movement propensity).** *Let the population comprise latent strata $z$ with weights $w_z$, each satisfying conditions (1)–(5) of Corollary 2 with its own stationary $\boldsymbol\pi_z$, generator $Q_z$ and incidence $\lambda_z$. Then*

$$
\hat\lambda \;\xrightarrow{\;p\;}\; \frac{\sum_z w_z\pi_{E,z}\lambda_z}{\sum_z w_z\pi_{E,z}},
$$

*the observable-susceptible-weighted mean incidence, which is the estimand. Cancellation is preserved under arbitrary stationary mixing.*

*Proof.* Applying Corollary 2 within stratum $z$, $\mathbb{E}[N_{\mathrm{rec},z}]=\lambda_z\pi_{E,z}\Omega_{T^*}$ up to the common scale, and $\mathbb{E}[N_{-,z}]\propto\pi_{E,z}$. Summing numerators and denominators over strata,

$$
\hat\lambda\to\frac{\sum_z w_z\lambda_z\pi_{E,z}\Omega_{T^*}}{\big(\sum_z w_z\pi_{E,z}\big)\Omega_{T^*}}
=\frac{\sum_z w_z\pi_{E,z}\lambda_z}{\sum_z w_z\pi_{E,z}} .
$$

Stratum $z$ contributes observable susceptible person-time proportional to $w_z\pi_{E,z}$, so this weighted mean is exactly incidence per observable susceptible person-time. $\blacksquare$

Corollary 3 matters because carceral contact and residential instability are strongly recurrent: a minority of the population accounts for most time spent unobservable. Concentration of movement in a high-propensity subgroup does not manufacture bias, and the marginal movement process of the mixture need not be Markov.

**Corollary 4 (absorbing loss only).** If the sole transition is $E\to X$ at rate $\mu$, then $w_t(u)=e^{-(\mu+\rho)u}$ and

$$
\frac{\hat\lambda}{\lambda_E}\to\frac{\int_0^{T^*}\varphi(u)e^{-(\mu+\rho)u}du}{\Omega_{T^*}}<1
\quad\text{for }\mu+\rho>0 .
$$

In a demographically stationary catchment $\rho=0$ and attenuation is governed by $\mu$ alone. Susceptible mortality does not offset it: losses from the susceptible pool are replaced by entry, not by return.

**Corollary 5 (transient and absorbing transitions jointly).** With both $E\leftrightarrow O_j$ and $E,O_j\to X$ present, $s_t(u)$ contains a fast component associated with redistribution among living states and a slower component associated with irreversible loss to $X$; the two are separated by the spectrum of $Q_1$. States whose mean sojourn is short relative to $T^*$ approach their within-living-state equilibrium rapidly and contribute approximately a level shift over most of the recency window, whereas states whose mean sojourn is comparable with $T^*$ retain substantial memory of the initial state and behave as quasi-absorbing over the window. Sojourn length therefore matters independently of occupancy: two states with identical stationary occupancy but $\beta_jT^*\gg1$ versus $\beta_jT^*\sim1$ contribute differently to $w_t$.

### 2.6 Failure modes

Within the eligibility-transition model, four distinct mechanisms break the conditions of Corollary 2. Consistency can also fail through assumptions outside that model — E.2 (path-dependent assay response), Gao & Bannick's epidemic assumptions, local constancy of $\lambda_E$, FRR behaviour under the selection processes of §2.7, or misspecification of the state space itself. E.2 in particular is not academic: if time spent in a custodial or institutional state alters ART exposure, viral suppression, or the biomarker process, then $\varphi(u\mid\text{path})\ne\varphi(u)$ and the estimator departs from Theorem 2 by a route the table below does not cover.

| Mechanism | Violates | Direction |
|---|---|---|
| **M1. Absorbing loss.** $\mu>0$: death or permanent departure, no return flow. | Corollary 2's no-absorbing-loss condition | Attenuation, $\hat\lambda<\lambda_E$ |
| **M2. State-dependent acquisition.** $\eta_k\ne1$ for some $k$. | Corollary 2's state-invariance | $\hat\lambda<\lambda_E$ if $\eta_k<1$; inflation if $\eta_k>1$ |
| **M3. Infection-dependent movement.** $Q_1\ne Q_0$. | E.3 | Sign depends on which transitions differ |
| **M4a. Demographic non-stationarity.** $g_E(u;t)\ne1$; under scalar growth $g_E=e^{-\rho u}$. | Corollary 2, condition (2) | $\rho>0$: attenuation; $\rho<0$: inflation |
| **M4b. Composition drift.** $\boldsymbol\pi(t-u)$ varying across the window. | Corollary 2, condition (1) | Either sign, depending on which states gain weight and their $\eta_k$ |

M1 is the only mechanism that cannot in principle be offset by a compensating flow, because $X\nrightarrow E$. M2 is how temporarily unobservable states re-enter as a bias source despite Corollary 2: the cancellation is a statement about symmetry of flow *at equal acquisition hazard*, and a state in which acquisition is suppressed returns fewer infections than it withholds. M4b is why Theorem 2 retains $\boldsymbol\pi(t-u)$ rather than $\boldsymbol\pi(t)$: factorising the composition at $t$ would assume the mechanism away.

### 2.7 Composition with screening-stage selection

The process above operates **upstream** of the selection mechanisms formalised by Pan, Bannick & Gao (*Am J Epidemiol* 2026), whose framework begins with individuals present in the source population at $t$ and asks whether they attend screening ($Q$) and satisfy a testing-based criterion ($C=\mathbb{1}\{S>c\}$, $S$ being time since most recent HIV test). The stages compose:

$$
\underbrace{\text{population at }t-u \;\xrightarrow{\;P_1(u)\;}\; \text{observable source at }t}_{\text{historical weight } w_t(u);\ \text{this paper}}
\;\xrightarrow{\;Q\;}\;\text{screened}\;\xrightarrow{\;C\;}\;\text{cross-sectional survey}.
$$

Note that $w_t(u)$ is a weight, not a transition probability: it incorporates $\eta_k$ and demographic scaling and may exceed one.

Substituting the **full** historical weight $w_t(u)$ — not the transition component alone — into their limiting estimation error gives

$$
\mathrm{LEL} = \log\!\big[\Omega_w - (1-r\,e^{\theta c})K_w\big] - \log\Omega_{T^*},
$$

$$
\Omega_w=\int_0^{T^*}\!\varphi(u)w_t(u)\,du,
\qquad
K_w=\int_c^{T^*}\!\varphi(u)w_t(u)\big[1-e^{\theta(c-u)}\big]du,
$$

with $r=q_1/q_0$ their selective attendance ratio and $\theta$ the background testing rate. Setting $w_t\equiv1$ recovers their expression exactly.

**Remark 5 (the zero-bias boundary).** With $w_t\equiv1$, $\mathrm{LEL}=0$ requires $1-re^{\theta c}=0$, giving $r^\star=e^{-\theta c}$ — a threshold independent of $\varphi$. Under a Poisson testing process this is exact and follows from memorylessness; the recency function governs the magnitude of bias away from the boundary, not its location. Eligibility dynamics move the boundary to

$$
r^\star_w = e^{-\theta c}\Big[1+\big(\Omega_{T^*}-\Omega_w\big)/K_w\Big],
$$

Whenever $\Omega_w<\Omega_{T^*}$ and $K_w>0$, the boundary shifts upward, widening the region of $r$ over which incidence is underestimated; $w_t(u)<1$ throughout the recency window is sufficient but not necessary. This distinction matters because $\eta_k>1$ is admitted, so $w_t$ may exceed one on part of the window while $\Omega_w$ remains below $\Omega_{T^*}$. Eligibility dynamics therefore interact with screening-stage selection rather than merely adding to it.

**Remark 6 (relation to covariate transport).** Wang, Duerr & Gao (*Stat Med* 2025) address a distinct mismatch — differing distributions of baseline covariates $X$ between sampled and target populations — corrected by reweighting. When the movement-relevant covariate distribution is the same in the cross-sectional and target populations, reweighting leaves the within-stratum duration component of $w_t$ unchanged. When those distributions differ, Wang-style weighting removes the compositional component while leaving the residual transition-duration component. The mechanisms are composable rather than competing.

### 2.8 Design implications

Three consequences follow, and they differ from what would follow from treating all eligibility loss as biasing.

1. **Transient unobservability requires no bias correction** under the conditions of Corollary 2. Corollaries 2 and 3 make this a theorem rather than an approximation, and it holds under arbitrary heterogeneity in movement propensity. Establishing that those conditions hold may still require the movement process to be examined; what the theorem removes is the need to correct for it, not the need to check it.
2. **Absorbing loss should be modelled**, with its magnitude assessed against the rate at which the zero-bias boundary reaches unity for the trial's $\theta$ and $c$.
3. **State-dependent acquisition is the primary symmetry-breaking parameter to elicit; occupancy and sojourn dynamics determine the magnitude of its effect once $\eta_k\ne1$.** Where $\eta_k$ cannot be estimated, the appropriate reporting form is a sensitivity surface over the relevant $\eta$, with any literature-informed range overlaid rather than fitted. Because sojourn length enters separately from occupancy (Corollary 5), states with comparable occupancy but different sojourn distributions must be parameterised separately rather than pooled.

---

## Drafting notes (not for submission)

- §2.1 reuses Gao & Bannick's symbols so the refinement is visibly additive. The only new primitive is $Z(t)$.
- Vectors are restricted to $\mathcal{L}=\mathcal{S}\setminus\{X\}$ throughout, so no reader need wonder about susceptible person-time in the absorbing state.
- Remark 1 pre-empts the double-counting error present in the earlier manuscript version; keep it in the main text.
- Remark 3 deliberately does **not** claim FRR is innocuous under composition with §2.7; that would require a proof not yet written.
- Remark 4 is the explicit answer to Reviewer 1's first objection; cite it in the response letter.
- Corollary 2 is the central result and should be signposted in the abstract.
- Theorem 2 keeps $\pi(t-u)$ rather than $\pi(t)$ because composition drift is mechanism M4; the $\pi(t)$ factorisation was verified to be inexact under drift (error $6.7\times10^{-4}$ in a test case where the general form was exact to $5\times10^{-15}$).
- E.3 is stated separately from E.1 so that M3 has an assumption to violate. Do not merge them.
- Remark 2 states the narrow, defensible claim about E.1 — mixtures of stationary Markov strata — rather than promising a general non-Markov relaxation that is not derived.
- §2.7 follows §2.5–2.6 so that composition applies to an already-characterised process. This ordering prevented two double-counting errors during development and is part of the argument.
- Numerical values are deliberately absent: $\mu_{\mathrm{crit}}$, the $\eta$ surfaces and the site parameterisation belong in §4 and the supplement.

- $\kappa_t$ is carried explicitly rather than absorbed into $\mathbf{n}_0$ so that a statistics reader can see the sampling stage is neutral, and so that non-neutral selection is visibly Pan's $Q$ and not hidden in the sampling factor.
- Corollary 2's conditions (1) and (2) are numbered because conflating state stationarity with demographic stationarity was an actual error in rev. 2: $\boldsymbol\pi^{\!\top}Q=\mathbf 0^{\!\top}$ fixes proportions, not totals, and a composition-stable pool growing at rate $\rho$ has $s_t\equiv1$ but $g_E=e^{-\rho u}$.
- M4 is split because the two sub-mechanisms have different sign behaviour: scalar growth signs deterministically, composition drift does not.

- Both theorem statements now name every condition in the italic hypothesis rather than leaving any to be discovered in the derivation — a direct response to Reviewer 1's request that assumptions be stated explicitly.

### Status

Proofs are written for Theorems 1–2 and Corollaries 2–3. Corollaries 1, 4 and 5 follow by direct substitution and need at most two lines each. No further modelling, surveillance variable, simulation or theoretical extension is required by the main argument.

§2 was frozen at rev. 4 and unfrozen at rev. 5 to add Remark 4a and the additive-extension statement in §2.1, both of which bring it into line with the positioning settled later for §§1, 3 and 5. The mathematics is unchanged: no theorem, corollary, assumption or proof was altered.
