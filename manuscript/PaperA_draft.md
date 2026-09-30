# Temporary Loss of Eligibility and Bias in Cross-Sectional HIV Incidence Estimation

*A. C. Demidont, Nyx Dynamics LLC. ORCID 0000-0002-9216-8569.*

**Version 2** · 30 September 2026


> Assembled draft. Regenerate with `python3 analysis/assemble_draft.py`; edit the section files, not this.


## Abstract

Cross-sectional HIV incidence estimation from recency assays underpins counterfactual-placebo designs in prevention trials, where randomised placebo control is no longer ethically available. These estimators are defined on a population eligible at the time of survey, yet eligibility can change between infection and sampling — through incarceration, displacement, hospitalisation, migration or death. Existing frameworks treat survey-time eligibility as a primitive and bound the problem by assuming that few individuals move, which is not the case in the populations for which counterfactual designs are most often required.

We retain the estimand, recency function and assumptions of the established framework and refine the eligibility indicator as the observable marginal of a finite-state process comprising an observable state, temporarily unobservable states permitting return, and an absorbing state. Allowing HIV acquisition in every living state rather than only while observable, we obtain the probability limit of the adjusted estimator as an integral of the recency function against a historical observability weight.

Temporary loss of eligibility is not inherently biasing. Under stable living-state composition, a demographically stationary observable susceptible pool, state-invariant acquisition, infection-independent movement and no absorbing loss, losses and returns cancel exactly — for any admissible recency function and at any occupancy of unobservable states. Cancellation holds within stationary strata and therefore under arbitrary heterogeneity in movement propensity, so concentration of movement in a high-propensity minority does not generate bias. Bias requires a specific symmetry failure: absorbing loss, state-dependent acquisition, infection-dependent movement, or non-stationarity. At sourced mortality of 0.040 per year the attenuation is 2.1%. State-dependent acquisition can attenuate or inflate, is the governing parameter, and is not identifiable from routine surveillance; we report it as a sensitivity axis rather than a corrected estimate. Analytic results were verified against an independently written generative simulator sharing no code with the derivation.

Occupancy of temporarily unobservable states cannot by itself establish that a cross-sectional incidence estimate is biased, or in which direction. Absorbing and temporary loss are not interchangeable, and correction is warranted only where a named condition fails.

**Keywords:** cross-sectional HIV incidence; recent infection testing algorithm; eligibility; selection bias; identifiability; counterfactual placebo; people who inject drugs

---

## 1. Introduction

Randomised placebo control is no longer ethically available for HIV pre-exposure prophylaxis efficacy trials. Where an effective agent exists, the comparator must be constructed rather than randomised, and cross-sectional incidence estimation from recency assays has become the primary means of doing so. A single survey of an at-risk population, combined with an assay that distinguishes recent from long-standing infection, yields an estimate of the background incidence a trial population would have experienced without the intervention. The estimator of Kassanjee and colleagues, placed on a formal footing by Gao and Bannick, now anchors this design.

The estimator is defined on an eligible population. Eligibility is assessed at the moment of survey: an individual contributes if they are alive, present in the catchment, and reachable for screening. Infection, however, occurred earlier — potentially up to two years earlier, the span the recency window covers. Over that interval people move. They enter and leave custody, are displaced or rehoused, are hospitalised, migrate, and die. Some who were observable when they acquired HIV are not observable when the survey is taken; others who were unobservable at acquisition have returned by then.

Existing treatments handle this by bounding it. Gao and Bannick require that restricted incidence and prevalence equal their unrestricted counterparts over the window, and note that the condition holds approximately when only a small proportion of subjects move in and out of the eligible population over the relevant span. That is a sufficient condition, and a reasonable one to assume when movement is rare. It is silent on what happens when movement is common — which is precisely the case in the populations where counterfactual-placebo designs are most needed. Among people who inject drugs in United States catchments, six to eight per cent of person-time is spent in custody alone, and the figure is higher in some cities.

The natural expectation is that this biases the estimator downward. People who disappear from an observable population cannot be counted by an estimator defined on it, and the individuals most likely to disappear are those whose circumstances also place them at highest risk. The expectation is intuitive, it motivated our own earlier work on this problem, and it is wrong in the general case.

What determines bias is not whether people leave but whether the flow is symmetric. Infections withheld from the recent count — acquired while observable, unobservable at survey — are offset by infections returned to it, acquired while unobservable and observable again by survey. Whether the two balance depends on the structure of the movement process, not on its volume. This paper identifies the conditions under which they balance exactly, and the specific ways the balance can fail.

Two features of the existing formalism make the question easy to get wrong, and both are worth stating at the outset. First, the recency function used by Gao and Bannick conditions on eligibility at survey and therefore carries no eligibility-survival component, whereas Kassanjee's original formulation embeds one. Eligibility dynamics must consequently enter *once*, explicitly, through a population process — and a treatment that both models the transitions and deflates the recency window has counted the same mechanism twice. Second, the population process operates upstream of, and composes with rather than replaces, the survey-attendance and prior-testing selection formalised by Pan and colleagues. Collapsing custody, mortality, attendance and testing-based exclusion into a single structural hazard makes double-counting nearly unavoidable; we keep the stages separate as an explicit modelling rule.

### Where this sits in the literature

The line from the Kassanjee estimator through Gao and Bannick's formalisation has been extended in three directions: prior-test information, covariate transport for population heterogeneity, and selection arising from survey attendance and prior-testing exclusion. Each of these takes eligibility at survey as a primitive — a time-indexed indicator whose value is given. We extend the same line by modelling the dynamics of that indicator.

The move is stated simply. Gao and Bannick define eligibility $A(t)$ as an indicator; we retain their estimand, their recency function and their assumptions, and refine $A(t)$ as the observable marginal of a stochastic state process $Z(t)$. That permits eligibility to evolve between infection and sampling, and yields the conditions under which such movement cancels exactly and the mechanisms by which it does not. This is an additive extension rather than an alternative framework: the existing results are recovered as the special case in which the process is inert.

We emphasise that the extension is in the formal treatment of eligibility, not in the assay calibration. The principal result holds for any admissible recency function, so no particular mean duration of recent infection is load-bearing; §3.2 records the calibration families the empirical evaluation spans and why they are not to be read as independent support for one another.

### Contributions

We refine the eligibility indicator rather than replace it, writing $A(t)=\mathbb{1}\{Z(t)=E\}$ for a process $Z$ on a finite state space comprising an observable state, temporarily unobservable living states permitting return, and an absorbing state. Within that refinement:

1. We derive the expected recent-infection count allowing HIV acquisition in **every** living state, not only while observable, and obtain the probability limit of the adjusted estimator as an integral of the recency function against a historical observability weight.

2. We show that under stable living-state composition, a demographically stationary observable susceptible pool, state-invariant acquisition, infection-independent movement and no absorbing loss, temporary losses and returns cancel **exactly**. The cancellation is independent of the recency function and of the occupancy of unobservable states, and it survives arbitrary heterogeneity in movement propensity — so concentration of carceral contact in a high-propensity minority, which is the empirical reality, does not by itself generate bias.

3. We characterise the four mechanisms that break the cancellation — absorbing loss, state-dependent acquisition, infection-dependent movement, and non-stationarity — and give the direction of bias each produces.

4. We compose the process with the screening-stage selection of Pan and colleagues, recovering their expression exactly in the appropriate limit and showing how eligibility dynamics displace the zero-bias attendance boundary.

5. We parameterise each mechanism from published sources, verify the analytic results against an independently written generative simulator sharing no code with the derivation, and report the parameter that governs the answer as a sensitivity axis rather than a point estimate.

### What this paper does not do

It does not assert that any published trial estimate is biased, or by how much. The relative acquisition hazard in unobservable states is the parameter that determines whether and in which direction bias arises, and it is not identifiable from the surveillance data ordinarily available; we therefore report the value it would have to take for cancellation to fail, rather than a correction. At empirically sourced rates the surviving effect is a few per cent, which we state plainly in §5.5 because an earlier version of this analysis claimed considerably more.

The contribution is structural. It replaces a question that cannot be answered usefully — how much of the population is temporarily unobservable — with questions that can: whether acquisition differs across states, whether the catchment is demographically stationary, and how much loss is irreversible over the recency window.

### Organisation

§2 develops the state-space refinement, the general recent-count identity, the probability limit, the cancellation theorem and its corollaries, the failure modes, and the composition with screening-stage selection. §3 parameterises each quantity from published sources and states for each whether it is sourced, derived, assumed, or unidentified. §4 reports the numerical results, including recovery of the reference framework and the independent Monte Carlo validation. §5 discusses the implications for design and reporting, the limitations, and the relation to the superseded analysis from which this work derives.

---

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

## 3. Empirical parameterisation

### 3.1 Scope, and what the parameterisation is for

§2 is a structural result: it states when transient eligibility loss cancels and which asymmetries break the cancellation. Deciding whether those asymmetries are large enough to matter in a real deployment requires values. This section supplies them, and states for each whether it is **sourced** from published data, **derived** from sourced quantities, **assumed**, or **unidentified**.

The purpose is a sensitivity analysis, not a fitted model. No parameter is estimated from the trial data the method would be applied to, and none is tuned to produce a conclusion. Where a quantity cannot be identified from available evidence — which is the case for the single most consequential one — it is carried as a free axis and reported across its plausible range rather than fixed at a point.

The illustrative setting throughout is cross-sectional incidence estimation among people who inject drugs (PWID) in United States catchments, with temporary unobservability arising predominantly from custody. That choice is driven by data availability: carceral occupancy and sojourn are published at national, state and county level, whereas displacement and prolonged hospitalisation are not. It is not a claim that custody is the only or the dominant mechanism.

### 3.2 The recency function

Two recency bases are used. For reproducing published quantities we adopt the gamma form of Pan et al., with window parameter 163 d and shadow 260 d; integrated over $T^*=2$ y this gives $\Omega_{T^*}=151$ d. The window parameter and $\Omega_{T^*}$ are distinct quantities and are easily conflated, so both are reported wherever the basis is named.

Independently, we re-estimated $\varphi$ from the CEPHIA public-use dataset (Zenodo 10.5281/zenodo.4900634) following the `XSRecency` procedure: Evaluation Panel, LAg-Sedia consolidated final result, subtypes A1/B/C/D, logit polynomial in years since estimated date of detectable infection, fitted by GEE clustered on participant with an independence working correlation. For subtype C with ODn $\le1.5$ and viral load $>75$ copies/mL, MDRI is 182.4 d (95% CI 161–213, 194 participants); Table S1 reports every algorithm fitted, and Figure S2A the resulting curve against the parametric bases. Pan's published 163 d falls inside that interval, and the estimate is stable across polynomial degree and fit horizon.

**The assay basis is not load-bearing for the principal result.** Corollary 2 states that $w_t\equiv1$ implies $\hat\lambda/\lambda_E=1$ for *any* admissible $\varphi$, so nothing in §2 depends on which recency calibration is adopted. What follows therefore establishes a robustness envelope for the empirical evaluation, not a validation of any particular MDRI.

**Methodological lineage is not calibration lineage, and the values below are not independent estimates of a common quantity.** Pan's 163 d is stated as relevant for subtype C using the LAg-EIA assay *and viral load*, and traces to Kassanjee et al. (2016), in which the CEPHIA consortium optimised viral-load criteria and thresholds across more than 2,000 candidate algorithms. Our re-estimate uses the CEPHIA public-use data with the same assay-plus-viral-load construction, so it is a replication within that lineage: it shows the published basis is reproducible from source, and Pan's value falls inside our interval, but both descend from the same consortium panel.

Duong et al. (2015) sit in a separate calibration family. They recalibrated the LAg-Avidity assay against more than 250 seroconversion panels assembled independently of CEPHIA and report, by binomial regression over all data points, MDRI of 130 d (95% CI 118–142) at ODn $\le1.5$ with proportion false-recent 1.6%; by subtype, 129 d for B, 122 d for AE, 109 d for A&D and 152 d for C.

The two families differ systematically, and the criterion rather than the panel explains it. Duong classifies on the assay alone; Pan's basis and our re-estimate additionally require detectable viral load — precisely the optimisation Kassanjee et al. (2016) introduced, which lengthens MDRI while lowering the false-recent rate by removing virally suppressed long-term infections from the recent category. The ordering is what that construction predicts. The families are therefore consistent rather than discrepant, but they characterise different algorithms and are not to be averaged or presented as mutual support.

| calibration family | subtype-C MDRI | viral-load criterion |
|---|---|---|
| Duong-type | 130–152 d | none |
| CEPHIA-derived | 163–182 d | required |
| **bases evaluated in §4** | **94–251 d** | — |

§4 evaluates the cancellation across six recency bases spanning $\Omega_{T^*}$ from 94 d to 251 d, a range encompassing the principal LAg calibration regimes considered here. The claim is not that the families independently estimate a common truth; it is that the result survives both, and substantially more.

**The trial this work is motivated by sits in the CEPHIA family, and our re-estimate reproduces its parameter.** The PURPOSE 2 statistical analysis plan adopts MDRI 184 d (relative standard error 7%) and false-recency rate 1.5% (rSE 70%) for the Sedia LAg-EIA at $T=2$ y, citing Kassanjee et al. (2016) and classifying an infection as recent when ODn $\le1.5$ **and** HIV-1 RNA exceeds 75 copies/mL. That is the same assay, the same cutoff pair and the same source as our own re-estimate, which gives 182.4 d — a difference of 1.6 d. We report this as a reproduction check on the CEPHIA lineage, not as independent support: it establishes that the parameter a live trial is using is recoverable from the public data, which is a different and more useful claim.

The same protocol records that the Sedia LAg-EIA package insert carries MDRI 130 d (95% CI 118–142) — numerically Duong's value — for a $T=1$ y cutoff with a viral-load threshold of 1000 copies/mL. The two-family structure described above is therefore visible inside the trial's own documentation, and the gap between an insert value and an adopted value is a difference of algorithm and cutoff rather than of evidence quality.

**$\beta_{T^*}=0$ is a simplification, not a claim about the assay.** Duong's proportion false-recent of 1.6% at the working cutoff, and PURPOSE 2's adopted 1.5%, are the empirical scale of the parameter Theorem 1 sets to zero; a non-zero false-recency rate enters the adjusted estimator by the route Gao & Bannick already specify.

**A methodological observation on the calibration base.** Gao and Bannick's simulation studies repurpose the longitudinal sampling structure of the Duong dataset while defining synthetic recency tests of their own, whereas later applied analyses in this line use CEPHIA-derived parameters. The empirical calibration base underlying the methodological literature is therefore narrower than the number of papers suggests. That is an argument for reporting across recency-function families rather than for treating agreement with any single calibration as external validation.

The same data show that Gao & Bannick's Assumption B.1 — a constant false-recency rate beyond $T^*$ — does not hold, and that the direction of the violation depends on who is counted. Among treatment-naive, non-elite-controller visits the raw test-recent proportion declines from 4.6% at 730–1095 d to 3.3% at 1095–1825 d to zero beyond ($n=1{,}603$). Across all visits in the same frame it instead **rises** in the final bin — 19.4%, 16.9%, 30.8% ($n=1{,}886$) — because antiretroviral treatment drives LAg ODn back down, so treated individuals re-enter the recent category at long infection duration. Neither tail is flat (Figure S2B). We record this rather than assume it away, and it is a further reason the viral-load criterion matters: it is what removes the treated from the recent category. §4 evaluates the cancellation across recency functions of materially different shape for the same reason.

### 3.3 Background testing rate

$\theta$ enters only through the screening-stage composition of §2.7. NHBS 2018 across 23 metropolitan statistical areas reports that 57% of PWID tested for HIV in the preceding 12 months. Under a Poisson inter-test process this implies $\theta=-\ln(0.43)=0.844\ \mathrm{y}^{-1}$, a mean inter-test interval of 1.18 y.

The Poisson assumption is not innocuous and is retained deliberately. Calibrating a uniform inter-test distribution to the same observation gives gaps $\mathrm{Unif}[0,2.905]$, a mean interval of 1.45 y, and a systematically more favourable zero-bias boundary. Poisson is therefore the conservative choice as well as the one Pan's main analysis uses. §4.6 reports what changes under the uniform variant.

### 3.4 Absorbing loss

$\mu_E$ is all-cause mortality in the observable susceptible pool. The ALIVE cohort of PWID in Baltimore reports 37.2 deaths per 1,000 person-years for 2015 to February 2020 and 39.6 per 1,000 in 2020; age-standardised rates rose from 23 to 45 per 1,000 person-years between 1988 and 2018. We adopt $\mu_E=0.040\ \mathrm{y}^{-1}$ as the central value with 0.037–0.045 as the sourced range, and evaluate to 0.10 to bracket a more severe fentanyl-era cohort than ALIVE observed.

Permanent out-migration from the catchment enters $X$ identically to death and is **not sourced**. Different-county mover rates from the American Community Survey are the obvious anchor and were not retrieved. Any non-zero migration adds to $\mu_E$, so the values used are a lower bound on absorbing loss, and §4.4 should be read accordingly.

### 3.5 Occupancy of unobservable states

$q$ is the stationary share of person-time spent temporarily unobservable. It was derived by three routes that do not share inputs.

**Route A — prevalence × duration.** NHBS 2018 gives past-12-month incarceration among PWID of 21.0% (not homeless) and 43.3% (homeless) across 23 cities. Combined with a BJS mean jail stay of 32 d and assumptions about episode count, this yields $q$ from 1.84% (21%, one episode) to 7.59% (43.3%, two episodes).

**Route B — point-prevalence ratio.** In steady state a cross-sectional share equals a person-time share. Degenhardt et al. (2026) report injection-drug-use prevalence among incarcerated people in North America of 13.4% (95% CI 10.3–16.8), corresponding to 246,500 (190,500–308,500) incarcerated people who have injected. Against an estimated 3.70 M US PWID in 2018 (Bradley et al. 2023), $q=6.66\%$ (5.15–8.34%). This route uses no BJS input.

**Route C — BJS rates with enrichment.** US adult imprisonment of 453 per 100,000 scaled by the national jail:prison ratio and by the injection enrichment implied by Degenhardt gives $q=6.70\%$.

Routes B and C agree to 0.04 percentage points despite sharing no data source, and the jail multiplier is independently validated: BJS jail (253 per 100,000 adults) plus prison (453) is 706, against 698 from the multiplier construction, accurate to 1%. We adopt $q\approx6\text{–}8\%$ nationally, and where the two custody types are separated, $q_J=0.03$ and $q_P=0.05$.

One construction was rejected. Jail incarceration peaks at ages 25–34 (480 per 100,000) and 35–44 (426), the bands PWID predominantly occupy, and age-standardising to a PWID structure gives a 1.40× uplift. Applying that uplift *and* the injection enrichment double-counts, because part of the enrichment ratio exists precisely because PWID occupy high-incarceration age bands. The age correction is therefore applied to denominators only (§S1), never layered on the enrichment.

### 3.6 Return rates

$\beta_k$ is the rate of return from unobservable state $k$ to $E$, the reciprocal of mean sojourn. BJS *Jail Inmates in 2023* gives a mean 32 d in custody for July 2022–June 2023 (36 d male, 19 d female; 43 d in jails with average daily population $\ge 2{,}500$), so $\beta_J=365.25/32=11.4\ \mathrm{y}^{-1}$. BJS *Time Served in State Prison, 2018* gives mean time served from initial admission to initial release of 2.7 y, so $\beta_P=0.37\ \mathrm{y}^{-1}$.

That mean carries a caveat the exponential sojourn does not capture. The median time served is 1.3 y against a mean of 2.7 y, whereas an exponential with mean 2.7 y has median 1.87 y. The true distribution is therefore more right-skewed than exponential: more short stays and a longer tail than the model represents. This does not affect Corollary 2, which requires stationarity rather than exponential sojourns, and Corollary 3 admits arbitrary stationary mixtures. It does mean that where sojourn length enters the magnitude of an effect (Corollary 5), a single-exponential prison state is an approximation, and a two-component mixture would represent the release distribution better.

The two differ by a factor of 31 and cannot be collapsed. A 32-day sojourn is short relative to $T^*=2$ y and approaches its within-living-state equilibrium quickly; a 2.7-year sojourn is comparable with $T^*$ and behaves as quasi-absorbing over the recency window. Applying a jail-length return rate to combined jail-and-prison occupancy conflates them, and is an error we made in earlier work on this problem.

Entry rates are not specified independently. Given occupancy and sojourn, $\alpha_k=\beta_kq_k/q_E$ follows, which is the identification used throughout: a long sojourn at fixed occupancy implies a *small* entry rate.

### 3.7 In-custody mortality

$\mu'$ is mortality in unobservable states. BJS gives 167 per 100,000 in local jails, 330 in state prisons and 259 in federal prisons for 2019 — 0.0017 to 0.0033 y$^{-1}$, an order of magnitude below community PWID mortality. Custody is a mortality refuge during the stay.

More useful is that $\mu'$ does not matter. Sweeping it from 0.002 to 0.100 — a fiftyfold change — moves the composed zero-bias boundary by 0.007, because at 4–8% of person-time the death rate in that state has almost no leverage. $\mu'$ can be fixed anywhere reasonable without affecting any conclusion and needs no further sourcing. This is a negative result that reduces the sourcing burden rather than shifting the answer, and it confirms that death in custody is not a material removal channel: removal during custody is the transient mechanism, not mortality.

### 3.8 Demographic stability of the catchment

Condition (2) of Corollary 2 requires a demographically stationary observable susceptible pool, $g_E\equiv1$. Tempalski et al. (2013) report median PWID prevalence across US MSAs falling from 104.4 to 91.5 per 10,000 aged 15–64 between 1992 and 2007, and describe the period 2002–2007 as relatively stable. We take $\rho\approx0$ over a two-year recency window. A catchment with material growth or decline violates condition (2), and §4.1 shows that condition is not optional.

### 3.9 Relative acquisition hazard — unidentified

$\eta_k=\lambda_k/\lambda_E$ is **not sourced and cannot be identified** from available data, and it is the parameter to which the results are most sensitive. Identification would require acquisition compared during custody and during community person-time within the same population; state-level HIV surveillance cannot supply it.

The only directly relevant evidence is a meta-analysis of 36 predominantly prospective cohort studies (Gough et al. 2010) giving pooled HIV incidence of 0.08 per 100 person-years among the continuously incarcerated against 1.14 per 100 among PWID recruited from treatment and 2.78 among street-recruited PWID — crude cross-study ratios of 0.03 to 0.07. Separately, a Georgia prison investigation documented 88 known seroconversions during incarceration with genetic evidence of within-prison transmission, establishing $\eta_P>0$.

These establish that a non-zero custodial acquisition hazard substantially below community PWID incidence is empirically plausible. They do not identify a contemporary value. They are heterogeneous historical studies rather than matched PWID followed inside and outside custody; "continuously incarcerated" is not synonymous with PWID; and the literature speaks to prison rather than to short jail episodes. We therefore use them as an **overlay band, never as a fitted value**, and do not collapse $\eta_J$ and $\eta_P$ to a common $\eta$ except where a common value is reported explicitly as such.

### 3.11 Summary, and what this parameterisation licenses

| symbol | meaning | status | value used |
|---|---|---|---|
| $\Omega_{T^*}$ | mean duration of recent infection | sourced | 151 d (gamma 163/260); CEPHIA re-estimate 182.4 d (161–213) |
| $\theta$ | background HIV testing rate | sourced | 0.844 y$^{-1}$ (Poisson) |
| $c$ | testing-based exclusion cutoff | **sourced** | 0.25 y = 3 months, per protocol |
| $\mu_E$ | absorbing loss from $E$ | sourced (mortality only) | 0.040 y$^{-1}$; range 0.037–0.045; evaluated to 0.10 |
| migration | permanent exit | **not sourced** | omitted; $\mu_E$ is therefore a lower bound |
| $q$ | unobservable occupancy | derived, three routes | 6–8%; $q_J=0.03$, $q_P=0.05$ |
| $\beta_J$ | return from jail | sourced | 11.4 y$^{-1}$ (32 d) |
| $\beta_P$ | return from prison | sourced | 0.37 y$^{-1}$ (2.7 y) |
| $\mu'$ | in-custody mortality | sourced, non-influential | 0.002 y$^{-1}$ |
| $\rho$ | catchment growth | sourced | $\approx0$ |
| $\eta_k$ | relative acquisition hazard | **unidentified** | free axis, 0 to 1.8; literature overlay 0.03–0.07 for prison |

**Licensed.** Evaluating the magnitude of each failure mechanism of §2.6 at values a reader can recompute from published sources, and locating the break-even $\eta$ at which the composed boundary crosses unity.

**Not licensed.** Any statement that a named trial's incidence estimate is biased, or by how much. Any point estimate of $\eta$. Any claim that the values above characterise a population other than US PWID catchments, or that custody is the dominant unobservability mechanism in any specific setting.

**Stated limitations.** State-level jail rates are unpublished, so the jail component applies a national jail:prison ratio and the *ordering* of occupancy across sites is more reliable than its level. The injection enrichment is North-America-wide applied per state, understating between-state spread if enrichment correlates with incarceration. BJS imprisonment counts sentenced prisoners, so pretrial detention enters only through the jail component. Degenhardt's numerator is "ever injected" against Bradley's current-injection denominator, which biases Route B upward.

**Falsifiability.** Every occupancy is a published rate times two stated constants, so any reader can recompute it, and the construction makes a testable prediction: if PURPOSE 4 reports screening-to-enrolment attrition by site, Newark and the Bronx should show the least observability loss and Houston the most.

---

## 4. Results

All quantities are evaluated on the recency basis of Pan et al. unless stated otherwise: a gamma $\varphi$ with window parameter 163 d and shadow 260 d, giving $\Omega_{T^*}=151$ d over $T^*=2$ y. The background HIV testing rate is $\theta=0.844\,\mathrm{y}^{-1}$, from the NHBS estimate that 57% of people who inject drugs report testing within 12 months under a Poisson inter-test process. The testing-based exclusion cutoff is $c=0.25$ y, which is the three-month criterion specified in the PURPOSE 2 protocol rather than a rounded ninety days. Carceral occupancies and sojourns, where used, are $q_J=0.03$ with mean stay 32 d and $q_P=0.05$ with mean time served 2.7 y.

Results are reported in the order the argument requires, and the order matters because the levels differ in what they establish. §4.1 checks that the framework is recovered where it should be. §4.2 gives the general result, which is exact and holds for any admissible recency function. §4.3 verifies it against an independent implementation. §4.4 and §4.5 quantify the two mechanisms that break it, sweeping each parameter over a plausible range rather than asserting a value. §4.6 tests what the conclusions depend on. Nothing after §4.3 is needed to establish the result; it is needed to say how large the departures are when the conditions fail.

### 4.1 Recovery of the reference framework

Setting $w_t\equiv1$ reduces the composed expression of §2.7 to the limiting estimation error of Pan et al. Across all nine cells of their published table — three testing rates crossed with attendance ratios spanning $r=0$ to $r=1$ — the two agree to within $0.030\times10^{-3}$ on the log scale, the largest discrepancy occurring at $c=0$, $\theta=2$ (Table 1). The agreement is to the precision at which their values are published, and we treat it as exact recovery rather than as an independent result.

The same limit reproduces Gao & Bannick's Theorem 2 when $\mathcal{L}=\{E\}$ and no transitions are present, provided the observable susceptible pool is demographically stationary. That proviso is not decorative: with a single living state and no transitions but a pool growing at rate $\rho$, $w_t(u)=e^{-\rho u}\not\equiv1$ and the estimator is biased. Corollary 1 therefore requires condition (2) of Corollary 2 explicitly.

### 4.2 Exact cancellation

Under the five conditions of Corollary 2, $\hat\lambda/\lambda_E=1$ to machine precision. Figure 1 shows the historical observability weight under each mechanism separately, and Figure 2 the resulting ratio across occupancy and sojourn. On a 4001-point quadrature grid the deviation is $0.0$; on the coarser 1201-point grid used during development it is $2.2\times10^{-16}$. The result held across nine combinations of stationary occupancy and mean sojourn, spanning $q\in\{0.01,0.03,0.15\}$ and sojourns from 32 d to 2.7 y, and across three recency functions of materially different shape. Cancellation is a property of the flow balance, not of the assay: Corollary 2 gives $\hat\lambda/\lambda_E=1$ for any admissible $\varphi$, and the numerical evaluation confirms rather than establishes it.

Two features of the result are worth isolating because each is a plausible objection that does not hold.

**Occupancy does not bound the effect.** Raising unobservable occupancy to $q_J=0.15$ leaves the cancellation exact. What breaks it is asymmetry, not volume.

**Concentration of movement does not break it.** Under Corollary 3, cancellation holds within each stationary stratum and therefore under arbitrary mixing. Evaluated over four stratifications of increasing skew — homogeneous; 20% of the population at three times mean occupancy; 10% at six times; and a three-stratum mixture at eight, two and residual times mean — the cancellation is $1.000000000$ in every case (Table 3). This matters because carceral contact and residential instability are strongly recurrent, and a natural objection is that a high-propensity minority accounts for most unobservable person-time. It does, and the estimator is unaffected. The marginal movement process of such a mixture need not be Markov.

The two stationarity conditions are not interchangeable. A pool whose composition is stable but whose size grows satisfies condition (1) and not (2), and is biased; the case is isolated as M4a.

### 4.3 Independent Monte Carlo validation

The analytic limit was checked against an individual-level generative simulator built to the population construction of Pan et al. — constant prevalence and incidence giving a flat infection-duration density on $[0,U_{\max}]$ with $U_{\max}=p/\lambda(1-p)=3.62$ y, equilibrium renewal testing histories, and the stop-when-positive rule. The simulator admits acquisition in every living state, drawing the state at infection with probability proportional to $\pi_k\eta_k$. It imports no analytic expression, so the comparison is between two independent routes rather than a restatement of one.

Across seven population scenarios — the cancellation case, absorbing loss at $\mu_E=0.04$ and $0.10\,\mathrm{y}^{-1}$, acquisition at $\eta\in\{0,0.3,1.8\}$, and the $q_J=0.15$ stress test — the simulated ratio agrees with Theorem 2 within $|t|\le1.22$ on 23 degrees of freedom, over 24 independent replicates of $1.5\times10^{7}$ individuals per cell (Figure 3). Across twelve screening configurations the composed limiting estimation error agrees within $|t|\le2.20$.

Two design points are load-bearing. Each cell uses a disjoint block of random seeds: $\eta$ and $r$ enter the estimator as deterministic weights, so a single shared population would suffice arithmetically, but it makes residuals perfectly correlated and reduces an agreement test to a sign test on one realisation. And the agreement statistic is referred to $t_{N-1}$ rather than to a normal, because the replicate standard error is itself estimated; at small replicate counts the two differ substantially.

### 4.4 Magnitude of the first failure: absorbing loss

Absorbing loss is the only mechanism that admits no compensating return flow, and it is the one case with a closed form: Corollary 4 gives $w_t(u)=e^{-\mu u}$ exactly, so the ratio is the recency function's own Laplace transform normalised by $\Omega_{T^*}$. At empirically sourced rates its magnitude is modest. With $\mu_E=0.040\,\mathrm{y}^{-1}$ — all-cause mortality among adults who inject drugs, from the ALIVE cohort — the weight is $w_t(u)=e^{-\mu u}$ and

$$
\hat\lambda/\lambda_E \to \Omega_\mu/\Omega_{T^*} = 0.9786 ,
$$

an attenuation of 2.1% (Table 2). At $\mu_E=0.10\,\mathrm{y}^{-1}$ the ratio is 0.9479.

Absorbing loss also displaces the composed zero-bias boundary of §2.7. Without dynamics that boundary is $r^\star=e^{-\theta c}=0.8098$; mortality raises it monotonically, to 0.8967 at $\mu_E=0.040$. The boundary reaches unity — the point at which the two selection mechanisms no longer cancel at equal attendance — at $\mu_{\mathrm{crit}}=0.0852\,\mathrm{y}^{-1}$, approximately 2.1 times the sourced rate. Susceptible mortality does not offset the effect: losses from the susceptible pool are replaced by entry, not by return.

### 4.5 Magnitude of the second failure: state-dependent acquisition

State-dependent acquisition is the mechanism by which temporarily unobservable states re-enter as a bias source despite Corollary 2, and it is the parameter to which the composed boundary is most sensitive. Because $\eta$ is not identifiable from available data (§3.9), it is swept over its plausible range rather than fixed. Holding occupancy and sojourn at the values above and varying a common relative hazard $\eta$ in the unobservable states, the boundary falls monotonically from $r^\star=1.047$ at $\eta=0$ through 1.008 at $\eta=0.25$ to 0.894 at $\eta=1$ (Table S3a). Figure S1 separates the jail and prison hazards, showing the $r^\star=1$ contour over the $(\eta_J,\eta_P)$ surface; the two cannot be collapsed because their sojourns differ by a factor of thirty. The break-even value — the $\eta$ at which $r^\star$ crosses unity — lies between 0.25 and 0.50.

The direction of bias is set by $\eta$ and not by occupancy. Under the census limit with mortality, $\hat\lambda/\lambda_E=0.944$ at $\eta=0$, $0.955$ at $\eta=0.3$, and $1.007$ at $\eta=1.8$: acquisition suppressed relative to the observable state attenuates the estimate, acquisition elevated inflates it. Reporting occupancy alone therefore cannot establish that an estimate is biased, or in which direction.

$\eta$ is the load-bearing unmeasured parameter of this analysis. It cannot be identified from state-level surveillance, which would require studies comparing acquisition during custody with acquisition during community person-time in the same population. The only directly relevant estimate we located is Gough et al. (2010), reporting HIV incidence of 0.08 per 100 person-years during continuous incarceration against 1.14–2.78 per 100 person-years in comparable community populations, implying $0<\eta\ll1$ for continuous custody. That estimate is old, is specific to continuous incarceration rather than to short jail stays, and no contemporary estimate specific to people who inject drugs exists. We therefore present $\eta$ as a sensitivity axis with any literature range overlaid rather than fitted, and make no claim about its value in any real population.

### 4.6 What the conclusions depend on

Substituting $w_t$ into the framework of Pan et al. moves the zero-bias boundary from $r^\star=e^{-\theta c}$ to

$$
r^\star_w = e^{-\theta c}\Big[1+(\Omega_{T^*}-\Omega_w)/K_w\Big] ,
$$

and setting $w_t\equiv1$ recovers their expression exactly (§4.1). The composed boundary is therefore an eligibility-dynamics correction to a quantity they derived, not a replacement for it.

Under a Poisson inter-test process the no-dynamics boundary is exactly free of the recency function. Evaluated over six gamma bases spanning $\Omega_{T^*}$ from 94 d to 251 d — a range encompassing the principal LAg calibration regimes considered here, both the Duong-type algorithms without a viral-load criterion and the CEPHIA-derived algorithms with one (§3.2) — $r^\star$ is $0.8098$ on every basis, with spread $0.0$ (Table S4). The invariance is provable and follows from memorylessness rather than from any property of the estimator.

That exactness does not extend to other testing processes, and the distinction matters because a *rectangular recency window* is a property of the assay while a *uniform inter-test distribution* is a property of testing behaviour. Under the uniform variant of Pan et al., invariance survives only approximately: relative spread across the same six bases is 0.37% for gaps $\mathrm{Unif}[0,3]$ and 0.18% for $\mathrm{Unif}[0,4]$. Two generalisations fail outright. The identity $r^\star=\Pr(S>c)$ is specific to the Poisson case: under $\mathrm{Unif}[0,3]$, $P_0=0.8403$ while $r^\star\approx0.902$. And matching the mean gap does not recover the boundary — the mean-matched Poisson rate $\theta=2/b$ gives $r^\star=0.847$ against the uniform process's 0.902.

---

## 5. Discussion

### 5.1 Principal finding

Temporary loss of eligibility does not, by itself, bias cross-sectional HIV incidence estimation. Under stable living-state composition, a demographically stationary observable susceptible pool, state-invariant acquisition, infection-independent movement and no absorbing loss, the infections withheld from the recent count — acquired while observable, unobservable at survey — are offset exactly by the infections returned to it, acquired while unobservable and observable again by survey. The offset is an identity, not an approximation, and it holds independently of the recency function, of the occupancy of unobservable states, and of arbitrary heterogeneity in movement propensity.

This reverses the natural intuition, which is that people disappearing from an observable population must distort an estimator defined on it. What matters is not that they leave but whether the flow is symmetric. Bias requires a specific, nameable violation: absorbing loss, state-dependent acquisition, infection-dependent movement, or non-stationarity.

The practical consequence is a change in the question to ask of a study population. "How much of the population is temporarily unobservable?" is close to uninformative; the cancellation holds at 15% occupancy as exactly as at 1%. The informative questions are whether acquisition differs between observable and unobservable states, whether the pool is demographically stationary, and how much irreversible loss occurs over the recency window.

### 5.2 Relation to existing frameworks

The result refines rather than displaces the framework of Gao and Bannick, and the extension is in the formal treatment of eligibility rather than in assay calibration: the principal result holds for any admissible recency function, so no particular mean duration of recent infection is load-bearing. Their eligibility indicator is retained and given internal structure: $A(t)=\mathbb{1}\{Z(t)=E\}$ for a process on a finite state space. Their Assumption C — that restricted incidence and prevalence equal their unrestricted values over the window — is the point of contact. They state that it holds approximately when only a small proportion of subjects move in and out of the eligible population over a span of $c$, and hold it fixed throughout. Our results say something more specific: the small-proportion condition is sufficient but far from necessary, because at $\eta_k\equiv1$ and stationarity the proportion may be large and the estimator remains exact.

Composition with Pan and colleagues is a nesting rather than a competition, and the nesting condition is worth stating precisely. Their framework is recovered when $w_t\equiv1$, which requires *both* that the living-state process contributes nothing, $s_t\equiv1$, and that the pool is demographically stationary, $g_E\equiv1$. Eligibility stability alone is insufficient: a stationary catchment with non-zero mortality still has $s_t<1$. Of the two halves, $\rho=0$ is empirically defensible and $s_t\equiv1$ is the half that fails, which is why the composed boundary differs from theirs at realistic mortality.

Covariate transport by reweighting addresses a different failure and the two are complementary rather than alternative. Reweighting corrects the composition of the sampled population with respect to measured covariates. It cannot correct a within-stratum duration effect, which is below unity in every stratum, so no weighted average of such factors escapes it. In the counterfactual-placebo setting the target population *is* the trial population, drawn from the same screened pool, so the covariate distributions coincide and reweighting removes exactly none of this bias — as §S3 shows. That is not a deficiency of the method but a statement that the two problems are orthogonal, and the composed expression carries both mechanisms simultaneously.

Prior-test-informed estimation likewise addresses an adjacent problem. It repairs misclassification of recency using prior test results rather than selection into the sample, and its own assumption that attendance and infection time are independent of duration is flagged there as violated by stop-when-positive testing. The awareness-driven non-entry it defers to future work is not the same as removal from observability after acquisition, which is the mechanism here.

A methodological point falls out of holding these apart. It is tempting to merge custody, mortality, attendance, known-HIV avoidance and recent-testing exclusion into a single structural hazard. Resisting that, and keeping the staged notation — population availability, then attendance, then testing-based eligibility — caught two double-counting errors during this work: adding a prevalence to a rate, and age-standardising an exposure before applying an enrichment ratio that already contained the age effect. We state stage separation as an explicit modelling rule rather than a stylistic preference.

### 5.3 The mechanism is already recognised in trial documentation

One consequence of the composition in §2.7 is not novel to this paper, and it is worth saying so. The PURPOSE 2 statistical analysis plan states that although its eligibility criteria require no HIV testing in the three months before screening, testing in the preceding three to twelve months may still affect the counterfactual incidence estimate: people tested shortly before screening skew the screened set toward known HIV-negative status, because those recently diagnosed are excluded from screening, and the plan concludes that both a two-year and a one-year recency cutoff would *underestimate* the background rate.

That is the prior-testing selection formalised by Pan and colleagues, identified in the protocol of a live trial and signed as to direction. What the protocol does not do is quantify it jointly with the population process that precedes it, which is what §2.7 supplies. The contribution here is therefore not the observation that the exclusion criterion matters — the trialists say so themselves — but a composed expression in which the eligibility process and the screening-stage selection can be evaluated together, and a statement of when the former contributes nothing.

### 5.4 Implications for design and reporting

Three consequences follow, and they differ from what would follow from treating all eligibility loss as biasing.

**Transient unobservability requires no correction** under the stated conditions. Establishing that those conditions hold may still require the movement process to be examined; what the theorem removes is the need to correct for it, not the need to check it.

**Absorbing loss should be modelled**, with its magnitude assessed against the rate at which the zero-bias boundary reaches unity for the study's own testing rate and exclusion cutoff. That threshold is a property of the design, not a universal constant.

**State-dependent acquisition is the parameter to elicit.** Occupancy and sojourn determine the magnitude of its effect once $\eta_k\ne1$, but they do not determine its direction or its existence. Because sojourn enters separately from occupancy, states with comparable occupancy but different sojourn distributions — a 32-day jail episode and a 2.7-year prison term — must be parameterised separately rather than pooled. Where $\eta_k$ cannot be estimated, the appropriate reporting form is a sensitivity surface with any literature-informed range overlaid rather than fitted.

### 5.5 Magnitude

At empirically sourced rates the surviving effect is small. Absorbing loss at PWID all-cause mortality of 0.040 y$^{-1}$ attenuates the estimator by 2.1%, and moving the composed zero-bias boundary above unity requires roughly twice that rate. Against the sampling variability of any realistic cross-sectional survey, a 2% attenuation is not the dominant source of error.

We state this plainly because it is the honest reading and because the alternative was tried. The analysis this work supersedes claimed a deflation of 8.9–27.3% from the same structural mechanism. That range does not survive: it was obtained under an implicit assumption of zero acquisition in unobservable states, and correcting that assumption cancels most of the effect. The scale of the direct effect is percent, not tens of percent.

The result that survives is structural rather than numerical. It states when a correction is needed and when it is not, and identifies which parameter governs the answer. A method that tells you a correction is unnecessary is worth having even when the correction it dispenses with would have been small, because the same reasoning identifies the conditions under which it would not be.

### 5.6 The parameter that cannot be measured

The relative acquisition hazard in temporarily unobservable states is the load-bearing unknown, and it is not identifiable from the data ordinarily available. State-level HIV surveillance cannot supply it: identification requires acquisition compared during custody and during community person-time within the same population, which is a narrow and separate literature.

The best available evidence — a meta-analysis of 36 predominantly prospective cohorts reporting 0.08 HIV infections per 100 person-years among the continuously incarcerated against 1.14 to 2.78 in comparable community populations — establishes that a non-zero hazard substantially below community incidence is plausible, and a documented prison outbreak establishes that it is not zero. It does not identify a contemporary value, it concerns continuous incarceration rather than short jail episodes, and "continuously incarcerated" is not synonymous with people who inject drugs. Using it as a point estimate would manufacture precision that does not exist.

The site-level analysis of §S2 is therefore presented as a break-even calculation rather than a correction: it reports the value $\eta$ would have to take for the two selection mechanisms to stop cancelling in a given catchment, given that catchment's carceral occupancy. Across nine counties that value ranges from 0.04 to 0.55, and in two it is never reached. What makes this worth reporting is not the individual numbers but that the range overlaps the interval the available incidence comparison suggests — so the question is empirical rather than hypothetical, and a study designed to answer it would resolve the matter.

### 5.7 Limitations

**Assumptions we do not make** are worth naming because their absence is easy to miss. The cancellation requires stationarity, not reversibility or detailed balance, and describing it as requiring reversible movement understates it. It does not require exponential sojourns: arbitrary mixtures of stationary strata inherit it, and the marginal movement process of such a mixture need not be Markov. It does not require $\eta_k\le1$; acquisition may be higher in an unobservable state, which inflates rather than attenuates. And it requires no differential hazard between infected and uninfected individuals — in a demographically stationary catchment none is needed, which inverts an argument made in the superseded analysis.

**Assumptions we do make, and which may fail.** The transition process is taken to be time-homogeneous and Markov; recidivism gives real history dependence, and a fully general semi-Markov treatment is out of scope. Infection is taken not to alter the movement law, which diagnosis may well do. Most consequentially, assay response is taken to be independent of the path through the state space: if time in custody alters ART exposure, viral suppression or the biomarker trajectory, then the recency function is path-dependent and the estimator departs from our expression by a route none of our failure modes covers. That mechanism is plausible and untested.

**Inherited assumptions that are violated in real data.** A constant false-recency rate beyond the recency window does not hold in the CEPHIA data, where the test-recent proportion declines to zero rather than plateauing. We record this rather than assume it away, and evaluate the cancellation across recency functions of different shape for that reason, but the adjusted estimator's own requirement remains.

**Unsourced inputs.** Permanent out-migration enters the absorbing state identically to death and is not sourced here, so the absorbing-loss figures are a lower bound. The exclusion-cutoff convention, the reliance on a national jail-to-prison ratio in the absence of published state jail rates, and the "ever injected" numerator in one of the occupancy routes are each stated in §3 and each would move the numbers modestly rather than the conclusions.

**Scope.** The empirical illustration is US catchments of people who inject drugs with custody as the dominant unobservability mechanism, chosen because that is where occupancy and sojourn are published. Displacement, prolonged hospitalisation and institutional care fit the same state space but are not parameterised here, and nothing in this work establishes that custody dominates in any specific setting.

### 5.8 Relation to a superseded analysis

This work derives from an analysis submitted elsewhere and declined after review, whose central empirical conclusion it withdraws. Two errors were found in post-review reanalysis. A jail-length return rate had been applied to combined jail-and-prison occupancy, conflating sojourn scales that differ by a factor of thirty. More consequentially, the expected recent-infection count had been derived under an implicit assumption that no acquisition occurs while an individual is temporarily unobservable — the special case $\eta_k=0$, which is empirically untenable. Generalising the numerator to admit acquisition in every living state is what produces the cancellation result, and what removes the empirical claim.

We describe this because the superseded analysis is publicly archived and because the reasoning is instructive: the error was not in any calculation but in an assumption that was never stated, and it was invisible until the numerator was written in a form general enough for the assumption to appear as a parameter value. That is an argument for stating the acquisition hazard explicitly in this class of model, which is what $\eta_k$ does.

### 5.9 Conclusion

Eligibility loss should not be treated as inherently biasing in cross-sectional HIV incidence estimation. Temporary, bidirectional movement cancels exactly under identifiable symmetry conditions, and correction is warranted only where a named condition fails. Absorbing and temporary loss are therefore not interchangeable, and state-specific acquisition — not the occupancy of unobservable states — is the parameter that determines whether and in which direction an estimate is biased. Occupancy alone cannot establish that an estimate is wrong.

---

---

## Supplement


### S1. Site-level geography

For the site-level sensitivity of §S2 we use the nine United States counties hosting PURPOSE 4 (NCT06101342), chosen because it is the cleanest available anchor for carceral geography in an HIV prevention trial. The registry record describes a phase 2, open-label, multicentre, randomised study of the pharmacokinetics and safety of twice-yearly subcutaneous lenacapavir for pre-exposure prophylaxis in people who inject drugs in the United States, with eligibility from 18 years and no upper bound, nine locations, and **181 participants enrolled**; it began in December 2023 and reached actual primary completion in July 2026.

Two things follow. The ≥18 frame is why adult PWID mortality from ALIVE is the appropriate source in §3.4 rather than a younger-cohort estimate. And at 181 participants across nine sites — roughly twenty each — **no site-level empirical claim would be supportable from this trial even in principle**, which is part of why §S2 is a break-even calculation rather than a correction. **No efficacy estimate from this trial is corrected or commented on**; it is a phase 2 pharmacokinetics and safety study and reports none.

The nine registry locations map to counties as follows, and the mapping is one-to-one: Los Angeles and San Diego, California; Miami, Florida (Miami-Dade); Baltimore, Maryland (Baltimore City); Newark, New Jersey (Essex); The Bronx, New York; Philadelphia, Pennsylvania; Houston, Texas (Harris); and Morgantown, West Virginia (Monongalia).

Jail and prison counts are taken at county level for 2019, the last year with harmonized county-level estimates across all nine counties. **2019 is a fixed pre-pandemic structural anchor and is not assumed to be conservative** — the data disprove that reading. Post-2019 jail trajectories are heterogeneous in both magnitude and direction: relative to 2019, jail populations stand at 0.46 in the Bronx and 0.70 in San Diego, but 1.02 in Miami-Dade, 1.05 in Monongalia and 1.09 in Essex. Four of nine counties are at or above their 2019 level, so a single national multiplier would have been wrong in direction for them. A secondary analysis updates the jail component with the most recent local data while retaining the 2019 prison component, county-level post-2019 prison counts being unavailable.

Incarceration rates are published against total or 15–64 populations while trial eligibility is 18+, so a denominator conversion is required. A national 15–64 to 18+ ratio of 0.8333 was replaced with county-specific ratios from Census Population Estimates 2019, which range from 0.834 (Miami-Dade) to 0.908 (Harris). The national factor systematically understated exposure in counties with younger adult age structures, by up to 12.4%. Consistent with §3.5, the correction is applied to the denominator only.

---

### S2. Break-even acquisition hazard by site

To indicate the range of $\eta$ at which the composed boundary would cross unity in real catchments, we evaluated nine United States counties with published jail and prison occupancy, using county-specific age denominators (Table S3b). Break-even $\eta$ ranged from 0.04 (San Diego) to 0.55 (Baltimore City); in two counties, Bronx and Miami-Dade, the boundary never crosses unity for any $\eta\in[0,1]$.

The trial enrolled 181 participants across those nine sites, so roughly twenty each; no site-level empirical claim would be supportable from it even in principle. **This is a sensitivity range, not an epidemiologic claim about any site.** It states the value $\eta$ would have to take for the two selection mechanisms to stop cancelling, given that county's carceral occupancy. It does not assert that $\eta$ takes that value anywhere, and no trial estimate is corrected on its basis. Its purpose is to show that the break-even value lies inside the plausible interval implied by the only available incidence comparison, so the question is empirical rather than hypothetical.

---

### S3. Comparison with covariate reweighting

Covariate transport by reweighting — matching the survey population to the trial-eligible population on measured covariates — addresses a different failure and does not remove this one. In a population where the observable and target covariate distributions coincide, which is the counterfactual-placebo case of interest, reweighting removes 0% of the bias: the naive and reweighted estimates are identical at 0.0387 against a truth of 0.0400, both attenuated by 3.3% (Table S2). Where the distributions differ, reweighting performs as designed, removing 91.3% and 96.8% of a much larger composition-driven bias in the two enriched cases.

The reason is structural. Reweighting corrects the *composition* of the sampled population; it cannot correct the within-stratum duration component, which is below unity in every stratum, so any weighted average of within-stratum factors remains below unity. The two methods are complementary rather than alternative: reweighting for covariate imbalance, the weight $w_t$ for eligibility dynamics.

---

## Figures and tables


Generated by `analysis/assemble_manuscript.py`. Numbering follows order of first citation; edit the mapping there, not here.

### Figures

**Figure 1.** Historical observability weight $w_t(u)$ by mechanism: absorbing loss, transient movement, and the two combined. Transient movement alone leaves $w_t\equiv1$. First cited §4.2.

**Figure 2.** Exact cancellation is invariant to occupancy and sojourn. $\hat\lambda/\lambda_E$ against the share of person-time spent unobservable, across sojourn lengths, under the five conditions of Corollary 2. First cited §4.2.

**Figure 3.** Analytic predictions against an independently written generative simulator. (A) Census sampling, seven population scenarios. (B) Composed with the screening and prior-testing stages. All 19 comparisons agree within $|t|=2.20$ on 23 degrees of freedom. First cited §4.3.

**Figure S2.** Empirical recency function from the CEPHIA public-use dataset. (A) The subtype-C fit against the two parametric bases. (B) Raw test-recent proportion by duration bin, all bins beyond $T^*$: among treatment-naive visits it declines to zero, across all visits it rises, so Gao \& Bannick's Assumption B.1 fails in both directions. First cited §3.2.

**Figure S1.** Zero-bias boundary over the $(\eta_J,\eta_P)$ surface at $q_J=3\%$, $q_P=5\%$, with the $r^\star=1$ contour. First cited §4.5.

### Tables

**Table 1.** Recovery of the published limiting estimation error at $w_t\equiv1$, all nine cells. First cited §4.1.

**Table 2.** Attenuation and the composed zero-bias boundary against absorbing loss $\mu$. First cited §4.4.

**Table 3.** Cancellation under stationary frailty mixtures of increasing skew in movement propensity. First cited §4.2.

**Table S1.** CEPHIA MDRI and shadow period by algorithm and subtype. First cited §3.2.

**Table S2.** Covariate reweighting against the duration mechanism, three target-population cases. First cited §S3.

**Table S3a.** Zero-bias boundary against a common relative acquisition hazard $\eta$. First cited §4.5.

**Table S3b.** Break-even $\eta$ by site county. Illustrative; not an epidemiologic claim about any county. First cited §S2.

**Table S4.** Boundary invariance across recency bases, by inter-test process. First cited §4.6.

---

## References


Assembled for the split. The predecessor manuscript's bibliography
(`Demidont_KassanjeeBias_references.bib`) lives on that repository's `master`
branch and covers only part of this list — every item in §1 below except
Kassanjee, and almost nothing in §2, entered during the recomputation.

**All 17 DOIs and 3 PMIDs below were resolved against Crossref or Europe PMC on
29 September 2026**, and the entries added from the reference archive were checked
against the PDFs themselves, not transcribed from the working notes. Two year
discrepancies surfaced and are recorded at the end.

---

### 1. Estimator and design literature

1. **Kassanjee R, McWalter TA, Bärnighausen T, Welte A.** A new general biomarker-based incidence estimator. *Epidemiology* 2012;23(5):721–728. doi:[10.1097/EDE.0b013e3182576c07](https://doi.org/10.1097/EDE.0b013e3182576c07)

2. **Kassanjee R, Pilcher CD, Busch MP, et al.** Viral load criteria and threshold optimization to improve HIV incidence assay characteristics. *AIDS* 2016;30(15):2361–2371. doi:[10.1097/QAD.0000000000001209](https://doi.org/10.1097/QAD.0000000000001209)
   *§3.2: the CEPHIA viral-load optimisation from which Pan's 163 d MDRI derives. Establishes that Pan's basis and our CEPHIA re-estimate share a data lineage and are not independent of each other.*

3. **Gao F, Bannick M.** Statistical considerations for cross-sectional HIV incidence estimation based on recency test. *Statistics in Medicine* 2022;41(8):1446–1461. doi:[10.1002/sim.9296](https://doi.org/10.1002/sim.9296)
   *The framework this paper refines. Assumption C is the point of contact.*

4. **Pan J, Bannick M, Gao F.** Estimating HIV cross-sectional incidence using recency tests from a non-representative sample. *American Journal of Epidemiology* 2026. doi:[10.1093/aje/kwag075](https://doi.org/10.1093/aje/kwag075)
   *Screening-stage selection; the limiting estimation error composed with in §2.7 and recovered in §4.1.*

5. **Wang Q, Duerr A, Gao F.** Addressing population heterogeneity for HIV incidence estimation based on recency test. *Statistics in Medicine* 2025;44(18–19). doi:[10.1002/sim.70216](https://doi.org/10.1002/sim.70216)
   *Covariate transport by reweighting; compared in §4.8.*

6. **Bannick M, Donnell D, Hayes R, et al.** An enhanced cross-sectional HIV incidence estimator that incorporates prior HIV test results. *Statistics in Medicine* 2024;43(17):3125–3139. doi:[10.1002/sim.10112](https://doi.org/10.1002/sim.10112)
   *PT-RITA. Repairs misclassification rather than selection; see Discussion.*

7. **Klock E, Wilson E, Fernandez RE, et al.** Validation of population-level HIV-1 incidence estimation by cross-sectional incidence assays in the HPTN 071 (PopART) trial. *Journal of the International AIDS Society* 2021;24(12). doi:[10.1002/jia2.25830](https://doi.org/10.1002/jia2.25830)

8. **Gao F, Dasgupta S, Pasalar S, et al.** Comparing approaches for estimating counterfactual HIV incidence among populations with high vulnerability to HIV in Lima, Peru: a multi-study comparative analysis. *Journal of the International AIDS Society* 2026;29(9). doi:[10.1002/jia2.70204](https://doi.org/10.1002/jia2.70204)
   *Motivates the counterfactual-placebo application in §1.*

---

### 2. Empirical parameters

9. **Duong YT, Kassanjee R, Welte A, et al.** Recalibration of the limiting antigen avidity EIA to determine mean duration of recent infection in divergent HIV-1 subtypes. *PLoS ONE* 2015;10(2):e0114947. doi:[10.1371/journal.pone.0114947](https://doi.org/10.1371/journal.pone.0114947)
   *§3.2: independent MDRI. By binomial regression over >250 seroconversion panels, 130 d (118–142) at ODn ≤1.5 with PFR 1.6%; by subtype 129 d (B), 122 d (AE), 109 d (A&D), 152 d (C). The subtype-C value sits on the Ω_T\* = 151 d of the basis adopted here, from a different panel and method.*

10. **Degenhardt L, Hickman M, Altice FL, et al.** The global epidemiology of injecting drug use, HIV, viral hepatitis and tuberculosis among people who are incarcerated: a multistage systematic review. *International Journal of Drug Policy* 2026;150:105062. doi:[10.1016/j.drugpo.2025.105062](https://doi.org/10.1016/j.drugpo.2025.105062). PMC13058553
   *§3.5, Route B: IDU prevalence among incarcerated in North America, 13.4% (95% CI 10.3–16.8).*

11. **Bradley H, Hall EW, Asher A, et al.** Estimated number of people who inject drugs in the United States. *Clinical Infectious Diseases* 2023;76(1):96–102. doi:[10.1093/cid/ciac543](https://doi.org/10.1093/cid/ciac543)
   *§3.5: denominator of 3.70 M US PWID.*

12. **Feder KA, Sun J, Rudolph JE, et al.** Mortality by cause of death during year 1 of the COVID-19 pandemic in a cohort of older adults from Baltimore, Maryland who have injected drugs. *International Journal of Drug Policy* 2022;109:103842. doi:[10.1016/j.drugpo.2022.103842](https://doi.org/10.1016/j.drugpo.2022.103842)
   *§3.4: ALIVE all-cause mortality, 37.2 and 39.6 per 1,000 person-years.*

13. **Sun J, Mehta SH, Astemborski J, et al.** Mortality among people who inject drugs: a prospective cohort followed over three decades in Baltimore, MD, USA. *Addiction* 2022;117(3):646–655. doi:[10.1111/add.15659](https://doi.org/10.1111/add.15659)
    *§3.4: age-standardised trend, 23 → 45 per 1,000 person-years, 1988–2018.*

14. **Tempalski B, Pouget ER, Cleland CM, et al.** Trends in the population prevalence of people who inject drugs in US metropolitan areas 1992–2007. *PLoS ONE* 2013;8(6):e64789. doi:[10.1371/journal.pone.0064789](https://doi.org/10.1371/journal.pone.0064789). PMID 23755143
    *§3.8: catchment demographic stability, ρ ≈ 0.*

15. **Gough E, Kempf MC, Graham L, et al.** HIV and hepatitis B and C incidence rates in US correctional populations and high risk groups: a systematic review and meta-analysis. *BMC Public Health* 2010;10:777. doi:[10.1186/1471-2458-10-777](https://doi.org/10.1186/1471-2458-10-777). PMID 21176146, PMC3016391
    *§3.9: the only directly relevant evidence on η. Overlay band, never a fitted value.*

16. **Handanagic S, Finlayson T, Burnett JC, Broz D, Wejnert C; National HIV Behavioral Surveillance Study Group.** HIV infection and HIV-associated behaviors among persons who inject drugs — 23 metropolitan statistical areas, United States, 2018. *MMWR Morbidity and Mortality Weekly Report* 2021;70(42):1459–1465. PMID 34673746
    *§3.3: 57% tested in the preceding 12 months, giving θ = −ln(0.43) = 0.844 y⁻¹. Also §3.5, Route A: past-12-month incarceration 21.0% and 43.3%.*

17. **Centers for Disease Control and Prevention.** HIV transmission among male inmates in a state prison system — Georgia, 1992–2005. *MMWR Morbidity and Mortality Weekly Report* 2006;55(15):421–426. PMID 16628181
    *§3.9: 88 documented seroconversions during incarceration; establishes η_P > 0.*

---

### 3. Data sources and software

18. **CEPHIA public-use dataset.** Consortium for the Evaluation and Performance of HIV Incidence Assays. Zenodo. doi:[10.5281/zenodo.4900634](https://doi.org/10.5281/zenodo.4900634)
    *§3.2: recency function re-estimation. Not redistributed with this work.*

19. **Bannick M, Gao F.** *XSRecency: cross-sectional incidence estimation.* R package, MIT. github.com/mbannick/XSRecency; release 0.2.0, 21 August 2023, commit `2811002`; `main` at `7c1243c5`, 7 July 2025. Companion simulation code: github.com/mbannick/RITA-plus-sims, release `v081723`. *§3.2 and §4.1. Two contract details were read from the 0.2.0 source rather than assumed. `get.gamma.params` (`R/phi-functions.R`) is byte-identical in 0.2.0 and `main` — shape = W/(2H−W), rate = 1/(2H−W) — so our implementation matches either, and `tests/test_gamma_params_match_xsrecency` asserts it. `createRitaCephia` (`R/get-rita-data.R`) did change: 0.2.0 documents `ui` as infection duration in days with no conversion, `main` documents years and divides by 365.25 at line 207. Our procedure works in years and matches `main`; following the 0.2.0 vignette against `main` would double-convert.*

20. **Zeng Z.** *Jail Inmates in 2023 – Statistical Tables.* Bureau of Justice Statistics, US Department of Justice; April 2025. NCJ 309965. *§3.5–3.6: mean 32 d in custody July 2022–June 2023; adult jail incarceration rate by age; all-adult rate 253 per 100,000.*

21. **Kaeble D.** *Time Served in State Prison, 2018.* Bureau of Justice Statistics; March 2021. NCJ 255662. *§3.6: mean time served from initial admission to initial release 2.7 y (median 1.3 y), giving β_P = 0.37/y.*

**Bureau of Justice Statistics.** *Prisoners* series. US Department of Justice. *§3.5 Route C only: adult imprisonment rate 453 per 100,000. **Edition not yet pinned** — the series is not among the tables committed under `data/bjs/`, and the 2020 edition reports a COVID-depressed 358 per 100,000, so the figure belongs to a different year. Route C is one of three routes to q and agrees with the BJS-free Route B to 0.04 percentage points, so no conclusion rests on it alone.*

22. **Carson EA.** *Mortality in Local Jails, 2000–2019 – Statistical Tables.* Bureau of Justice Statistics; December 2021. NCJ 301368. And *Mortality in State and Federal Prisons, 2001–2019 – Statistical Tables.* Bureau of Justice Statistics; December 2021. NCJ 300953. *§3.7: 167, 330 and 259 deaths per 100,000. Source tables are committed under `data/bjs/`.*

23. **Maruschak LM.** *HIV in Prisons, 2020 – Statistical Tables.* Bureau of Justice Statistics; May 2022. NCJ 302601. *Cited only to establish that the incarcerated population is not predominantly PWID, so HIV prevalence cannot substitute for injection prevalence in §3.5. Source tables committed under `data/bjs/`.*

24. **US Census Bureau.** Population Estimates Program, vintage 2019, county characteristics (`cc-est2019-alldata`). *§3.10: county-specific 15–64 to 18+ ratios, 0.834–0.908.*

25. **Vera Institute of Justice.** *Incarceration Trends* county-level jail and prison populations. *§3.10: the 2019 anchor and post-2019 jail trajectories. County prison series ends at 2019.*

26. **Kelley CF, Acevedo-Quiñones M, Agwu AL, et al.** Twice-yearly lenacapavir for HIV prevention in men and gender-diverse persons. *New England Journal of Medicine* 2025;392(13):1261–1276. doi:[10.1056/NEJMoa2411858](https://doi.org/10.1056/NEJMoa2411858)
    *PURPOSE 2 (NCT04925752). §3.2, §3.3 and §5.3: the protocol and statistical analysis plan supply the three-month testing exclusion, the adopted assay parameters (MDRI 184 d, FRR 1.5%, ODn ≤1.5 with VL >75, T = 2 y), and the plan's own statement that prior testing in the preceding 3–12 months would underestimate the background rate.*

27. **Parkin N, Gao F, Grebe E, et al.** Facilitating next-generation pre-exposure prophylaxis clinical trials using HIV recent infection assays: a consensus statement from the Forum HIV Prevention Trial Design Project. *Clinical Pharmacology and Therapeutics* 2023;114(1):29–40. doi:[10.1002/cpt.2830](https://doi.org/10.1002/cpt.2830)
    *The RAWG recommendations from which the T = 2 y default derives.*

28. **ClinicalTrials.gov.** PURPOSE 4: NCT06101342. Study of lenacapavir and emtricitabine/tenofovir disoproxil fumarate for pre-exposure prophylaxis in people who inject drugs. *§3.10 and §4.7. Phase 2, open-label, multicentre, randomised; pharmacokinetics and safety; eligibility 18 years and older with no upper bound; nine US locations; 181 participants enrolled; start December 2023, actual primary completion July 2026. Registry record consulted 29 September 2026. No efficacy estimate is corrected or commented on; the trial reports none.*

29. **Demidont AC.** Software repository for *Calibration-to-deployment mismatch in HIV prevention trials*. Zenodo 2026. doi:[10.5281/zenodo.20344293](https://doi.org/10.5281/zenodo.20344293)
    *The superseded predecessor analysis. Cited for provenance; its central empirical conclusions are not carried forward. Disclosed under prior publication.*

---

### Verification notes

**Verified against the supplied PDFs (30 September 2026).** Three checks were run against the
reference archive rather than against metadata:

- **Degenhardt Table 1, North America row** reads 13·4 (10·3, 16·8) and 246,500 (190,500,
  308,500) — confirming §3.5 Route B exactly as written. The regional supplement tables carry
  several nearby values for other outcomes (13·0, 13·6) and for the United States alone (13·1);
  these are not the quantity cited and should not be substituted for it.
- **The Degenhardt supplement records a methodological caveat worth carrying**: for most regions
  a prevalence ratio was pooled only where two or more countries had estimates, but North
  America and Australasia were exceptions where a single country sufficed. The North American
  figure is correspondingly less well supported than its interval suggests.
- **The recency-basis provenance was traced and one claim withdrawn.** An earlier draft of §3.2
  presented Duong 2015, Pan's 163 d and our CEPHIA re-estimate as three-way corroboration. They
  are not independent: Pan's value traces to Kassanjee 2016, a CEPHIA viral-load optimisation,
  and our re-estimate uses the same consortium data and the same assay-plus-viral-load
  construction. Duong is the only external anchor, and it measures a different algorithm —
  assay alone, without the viral-load criterion. §3.2 now states the two lineages and why
  Duong's values are systematically shorter.
- **Handanagic 2021 authorship** was corrected from a corporate CDC attribution to the named
  authors after reading the article's own byline.



Two dates in the working notes were wrong in the drafts' favour, and both are now stated as the print year:

| item | working note | Crossref | used |
|---|---|---|---|
| Bradley | 2023 | issued 2022, **print 2023**, 76(1):96–102 | 2023 |
| Sun | 2022 | issued 2021, **print 2022**, 117(3):646–655 | 2022 |

Online-first and print years differ for both; the volume numbers confirm the print year.

**Items 17–24 are grey literature, datasets and software** and carry no DOI. They need the exact report edition, NCJ number where applicable, and an access date before submission. `docs/audit/computation_record.md` Appendix C records that the four BJS folders could not be opened locally, and that neither the *Survey of Prison Inmates 2016* (NCJ 252641) nor the 2007–2009 drug-use report contains an injection-route variable — which is why item 8 supplies that quantity instead.

**Not cited and deliberately so.** The BJS jail drug-intoxication figure of 184 per 100,000 appears in a page summary and exceeds the all-cause rate, so it is almost certainly a count rather than a rate. It is not used anywhere and should not be cited without checking the underlying table.

---

# Drafting notes

*Editorial. Not part of the manuscript; collected here so the body reads clean.*


### From `section0_abstract.md`

**Length.** Unstructured version is 332 words; structured is 202 (measured, not estimated). Common limits: *Statistics in Medicine* 250 unstructured, *American Journal of Epidemiology* 250 unstructured, *Epidemiology* 250 structured, preprints.org none. **The unstructured version is over for every journal target and must be cut to ~250 before submission** — it is currently written for the preprint, where length is free. The paragraph on heterogeneity and the simulator sentence are the first two cuts; the five conditions can compress to "five stated conditions" as the structured version already does.

**Claims audit.** Every quantity appears in §3–§4 and is regenerated by `make figures`. No named trial is called biased; no point estimate of η is given; no corroboration is claimed for the recency basis.

**Not decided.** Whether to signal the superseded predecessor in the abstract. §5.8 carries it in full and the reference list cites it. Most venues would not expect it here; a preprint posting may warrant one clause, since the predecessor is publicly archived under an overlapping title.

**Title.** Set to the CROI-compliant form, which also satisfies the general rule against stating conclusions in a title. If the target venue has no such rule, *Temporary Loss of Eligibility Cancels Exactly in Cross-Sectional HIV Incidence Estimation* is the stronger and more citable form.

### From `section1_introduction.md`

**Reusable from the predecessor:** only the opening context — counterfactual-placebo motivation, the Kassanjee/Gao framework, the PURPOSE-era trials. Everything downstream of its second paragraph argues the withdrawn thesis and is not adapted.

**One inherited error worth not repeating.** The predecessor's introduction wrote the window as $\int_0^T P_R(t)\,dt$ and then described it as assuming every individual infected within the window is observable at screening. That conflates the two formulations: Kassanjee's $P_R$ *contains* an eligibility-survival component, which is exactly what Gao and Bannick's $\varphi$ conditions away. The paragraph beginning "Two features of the existing formalism" exists to forestall that confusion, and it should not be cut for length.

**Trial citations to add.** PURPOSE 1 (NCT04994509) and PURPOSE 2 (NCT04925752) with their primary reports, if the motivating paragraph is to name them as the predecessor did. PURPOSE 4 (NCT06101342) is already cited in §3.10 and §4.7; note that it is phase 2 and is used only as a carceral-geography anchor.

**Prior-work disclosure.** §5.8 carries it. A single forward-reference in §1 is an option — "an earlier version of this analysis" in the penultimate paragraph is currently the only signal — but most journals prefer it later or in a cover letter.

**Length** ~1,050 words. If compressed, the paragraph on the two notational traps and the "what this paper does not do" section should survive; the contributions list can become prose.

### From `section2_theory.md`

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

### From `section3_parameterisation.md`

**References to complete.** NHBS MMWR 2021;70(42); Feder 2022 doi:10.1016/j.drugpo.2022.103842; Sun 2022 doi:10.1111/add.15659; Degenhardt 2026 doi:10.1016/j.drugpo.2025.105062; Bradley 2023 doi:10.1093/cid/ciac543; Tempalski 2013 PMID 23755143; Gough 2010 doi:10.1186/1471-2458-10-777; BJS *Jail Inmates in 2023* and *Prisoners* series; Census PEP 2019 `cc-est2019-alldata`. The bibliography lives on the predecessor repository's `master` branch, not `main`.

**Do not import the audit record's scenario conclusions.** Appendices A.3, G.1 and I.3 report zero-bias boundaries and "crosses" verdicts computed under the restricted model with $\eta_k=0$, before the cancellation theorem. Those are now the $\eta=0$ corner of the sensitivity surface, not conclusions. §4 reports the surface; §3 must not smuggle the corner back in as a headline.

**Resolved.** $c$ was flagged as possibly discrepant on the belief that PURPOSE specifies 90 days. The protocol specifies **three months** — "HIV-1 status unknown at screening and no prior HIV-1 testing within the last 3 months" — so $c=0.25$ y is exact rather than an approximation, and the "90 d" gloss was the error. Out-migration remains unsourced and should either be retrieved from ACS or explicitly scoped out in the limitations.

**Possible relocation.** §3.2's CEPHIA re-estimate is arguably a result rather than an input. It is placed here because §4 treats $\varphi$ as given; move it if the empirical fit is to carry weight of its own.

### From `section4_results.md`

**Depends on §3.** Every sourced parameter used above — $\mu_E=0.040$ from ALIVE, $\theta=0.844$ from NHBS, the carceral occupancies and sojourns from BJS, the county denominators from Census PEP — must be established in §3 with provenance. §4 cites them; it does not justify them. Provenance is currently in `docs/audit/computation_record.md` Appendices A–C and F–I.

**Numbering is final and machine-checked.** The mapping from generated output to manuscript number lives in `analysis/assemble_manuscript.py`; `make manuscript` writes the numbered files to `outputs/manuscript/` and regenerates `manuscript/captions.md`, and `make check-refs` exits non-zero if any numbered item is missing or uncited. An earlier provisional mapping had the Monte Carlo figure as Figure 2 and the $\eta$ surface as Figure 3, neither of which matched the text; three figures were uncited entirely. Renumber by editing that script, not the prose.

**Resolved.** The exclusion cutoff was flagged as possibly discrepant against a supposed 90-day PURPOSE window. The protocol specifies **three months**, so $c=0.25$ y is exact and $r^\star=e^{-\theta c}=0.8098$ stands. No constant, figure or boundary changes.

**Deliberately absent.** No claim that any published trial estimate is biased or by how much. No value asserted for $\eta$. No claim that cancellation requires reversibility — stationarity suffices. No claim of boundary exactness beyond the Poisson inter-test case.

**Not yet drafted.** A subsection reporting the empirical $\varphi$ fit (CEPHIA MDRI 182.4 d, 95% CI 161–213, subtype C) and the observed violation of Gao & Bannick's Assumption B.1 — the test-recent proportion falls 9.9% → 5.8% → 0 across 730–1095, 1095–1825 and >1825 d. This belongs either here or in §3 depending on whether the fit is treated as input or as result.

Two further analyses are reported in the supplement because they demonstrate rather than establish. §S2 evaluates the break-even $\eta$ at which the composed boundary crosses unity in nine real catchments, using the site geography parameterised in §S1; §S3 compares the mechanism with covariate transport by reweighting, which addresses a different failure and removes none of this one in the case of interest.

### From `section5_discussion.md`

**Deliberately absent**, per the constraints set during the reanalysis: no claim that any named trial's estimate is biased or by how much; no point estimate of $\eta$; no replacement empirical assertion of comparable ambition to the withdrawn one; no claim of boundary exactness beyond the Poisson inter-test case.

**§5.8 placement.** Some journals prefer a prior-work disclosure in Methods or a cover letter rather than in Discussion. The material is written to move intact if so. It should not be cut: the predecessor is publicly archived and cited in the reference list, and a reader who finds it independently should find it already addressed.

**Reviewer 1 of the predecessor** objected that eligibility dynamics act on numerator and denominator alike and would largely cancel. That objection was correct, and §5.1 concedes it by proving it. Consider whether to say so explicitly — it is a strong move in a cover letter and a weak one in a Discussion.

**Length.** ~2,100 words. If the target journal wants 1,200, §5.2 compresses to a paragraph per framework and §5.6 to a single paragraph, with the detail moving to the supplement; §5.1, §5.4, §5.5 and §5.8 should survive intact.
