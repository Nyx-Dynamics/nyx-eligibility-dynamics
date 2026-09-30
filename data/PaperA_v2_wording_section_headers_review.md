# Paper A v2 — Wording and Section-Header Review

## Overall assessment

The manuscript is scientifically much cleaner than the earlier version, but several section headers still read as **commentary on the argument** rather than as the architecture of a finished statistical-methods paper.

The issue is not lack of clarity. In several places the headers are *too interpretive*: they tell the reader what to conclude, explain why a section exists, or narrate the history of the analysis. The strongest parts of the manuscript—the state-space definition, probability limit, cancellation theorem, failure modes, and simulation verification—already read like a formal methods paper. The headers should adopt that same register.

The simplest editorial rule is:

> **A section header should name the statistical object, analysis, or inferential function of the section—not tell the reader how the author interprets it.**

For example:

- **State-dependent acquisition** = methods-paper header.
- **The parameter that cannot be measured** = commentary.
- **Sensitivity to model assumptions** = methods-paper header.
- **What the conclusions depend on** = commentary.
- **Scope of inference** = methods-paper header.
- **What this paper does not do** = commentary.

---

## Recommended section-header revisions

| Current header | Recommended revision | Rationale |
|---|---|---|
| **Where this sits in the literature** | **Relation to Existing Methods** | Current wording is conversational and meta-discursive. |
| **Contributions** | **Methodological Contributions** | Slightly more formal; alternatively delete the subsection and let the paragraph stand in the Introduction. |
| **What this paper does not do** | **Scope of Inference** | Current version sounds defensive/referee-facing. |
| **Organisation** | Delete | The manuscript does not need a full roadmap subsection at this length. |
| **Design implications** | **Implications for Study Design** | More conventional journal phrasing. |
| **Scope, and what the parameterisation is for** | **Empirical Parameterization Strategy** | One of the most commentary-like headers. |
| **Relative acquisition hazard — unidentified** | **Relative Acquisition Hazard** | Identifiability should be stated in the text, not editorialized in the title. |
| **Summary, and what this parameterisation licenses** | **Parameter Summary and Inferential Scope** | “Licenses” sounds like commentary on the analysis. |
| **What the conclusions depend on** | **Sensitivity to Model Assumptions** | More statistical and more precise. |
| **Principal finding** | **Principal Results** | More conventional for a methods paper. |
| **Relation to existing frameworks** | **Relation to Existing Estimation Frameworks** | More specific. |
| **The mechanism is already recognised in trial documentation** | **Prior-Testing Selection in Trial Protocols** | Current wording is argumentative rather than descriptive. |
| **Implications for design and reporting** | **Implications for Study Design and Reporting** | Minor formalization. |
| **Magnitude** | **Magnitude of Bias Under Sourced Parameters** | “Magnitude” is too vague. |
| **The parameter that cannot be measured** | **Identifiability of the Relative Acquisition Hazard** | Current wording is commentary; proposed wording names the inferential problem. |
| **Relation to a superseded analysis** | **Relation to Previous Analysis** | Less self-referential and less process-oriented. |
| **Site-level geography** | **Site-Level Carceral Exposure Parameters** | Says what is actually being analyzed. |
| **Break-even acquisition hazard by site** | **Site-Specific Break-Even Relative Acquisition Hazards** | More technical and precise. |
| **Comparison with covariate reweighting** | **Comparison With Covariate-Reweighting Methods** | Minor formalization. |

---

## Results section: recommended structure

### Current

- 4.1 Recovery of the reference framework
- 4.2 Exact cancellation
- 4.3 Independent Monte Carlo validation
- 4.4 Magnitude of the first failure: absorbing loss
- 4.5 Magnitude of the second failure: state-dependent acquisition
- 4.6 What the conclusions depend on

### Recommended

- **4.1 Recovery of Existing Estimator Results**
- **4.2 Exact Cancellation Under Transient Movement**
- **4.3 Monte Carlo Verification**
- **4.4 Absorbing Loss**
- **4.5 State-Dependent Acquisition**
- **4.6 Sensitivity to Recency and Testing-Process Assumptions**

This is more consistent with the manuscript’s actual logic. The Results already have a clear inferential hierarchy:

1. recover the existing framework;
2. establish the exact result;
3. verify it independently;
4. examine the first failure mode;
5. examine the second failure mode;
6. assess dependence on modeling assumptions.

The headers do not need to narrate that hierarchy again.

---

## Internal bold mini-headings

Several internal bolded phrases also read as rebuttal points or commentary.

### Current

- **Occupancy does not bound the effect.**
- **Concentration of movement does not break it.**

### Recommended

- **Sensitivity to Unobservable-State Occupancy**
- **Heterogeneity in Movement Propensity**

Then let the first sentence state the result declaratively.

For example:

> Increasing unobservable-state occupancy to 15% leaves cancellation exact under the conditions of Corollary 2.

and:

> Cancellation also persists under arbitrary stationary mixtures with heterogeneous movement propensity.

This keeps the scientific force while removing the debate-like tone.

---

## Limitations section

The current internal structure is lucid but reads strongly like author commentary.

### Current

- **Assumptions we do not make are worth naming because their absence is easy to miss.**
- **Assumptions we do make, and which may fail.**
- **Inherited assumptions that are violated in real data.**
- **Unsourced inputs.**
- **Scope.**

### Recommended

- **Assumptions Not Required for Cancellation**
- **Model Assumptions and Potential Violations**
- **Inherited Estimator Assumptions**
- **Unmeasured or Externally Parameterized Quantities**
- **Scope and Generalizability**

This retains the transparency while moving the prose into a journal register.

---

## Discussion section: recommended structure

### Current

- 5.1 Principal finding
- 5.2 Relation to existing frameworks
- 5.3 The mechanism is already recognised in trial documentation
- 5.4 Implications for design and reporting
- 5.5 Magnitude
- 5.6 The parameter that cannot be measured
- 5.7 Limitations
- 5.8 Relation to a superseded analysis
- 5.9 Conclusion

### Recommended

- **5.1 Principal Results**
- **5.2 Relation to Existing Estimation Methods**
- **5.3 Interaction With Prior-Testing Selection**
- **5.4 Implications for Study Design and Reporting**
- **5.5 Magnitude Under Empirically Sourced Parameters**
- **5.6 Identifiability of State-Specific Acquisition**
- **5.7 Limitations**
- **5.8 Provenance of the Present Analysis** *(optional; preferably shortened substantially)*
- **5.9 Conclusion**

---

## Strong recommendation: shorten §5.8

The current section explaining the superseded analysis is transparent, but it shifts the manuscript into research-process narration. The scientifically important point is simply that the prior model:

1. pooled jail and prison sojourns incorrectly, and
2. implicitly set acquisition in unobservable states to zero.

That can be reduced to a short provenance statement such as:

> An earlier publicly archived analysis treated temporary unobservability as uniformly loss-generating and did not allow acquisition in all living states. The present formulation supersedes that analysis by explicitly incorporating state-specific acquisition and separate jail and prison sojourn processes. The resulting generalization yields the cancellation result developed here.

The manuscript does not need to narrate the rejection history, debugging sequence, or the fact that the hidden assumption became visible only after rewriting the numerator. Those details are intellectually interesting but not necessary to the methods argument.

---

## Prose that still reads as commentary

A few sentences retain the voice of the reconstruction process rather than the final paper.

### 1. Current

> The expectation is intuitive, it motivated our own earlier work on this problem, and it is wrong in the general case.

### Recommended

> This intuition does not hold in general. Whether temporary loss induces bias depends on the symmetry of flows between observable and unobservable states.

---

### 2. Current

> This is a negative result that reduces the sourcing burden rather than shifting the answer...

### Recommended

> The results were insensitive to in-custody mortality across the evaluated range; this parameter was therefore fixed for subsequent analyses.

---

### 3. Current

> We state this plainly because it is the honest reading and because the alternative was tried.

### Recommended

> At empirically sourced rates, the residual effect is modest.

Then report the 2.1% attenuation directly.

---

## General editorial principle

For each heading, ask:

> **Does this name the statistical object or analysis, or does it tell the reader how I interpret the analysis?**

Use the first type for headers. Put the second type in the prose.

The manuscript’s scientific core now reads like a serious statistical-methods paper. The section architecture is the main place where the older “working through the problem in public” voice remains. A largely mechanical conversion to noun-phrase, object-centered headings would make the paper feel substantially more mature without changing any substantive content.
