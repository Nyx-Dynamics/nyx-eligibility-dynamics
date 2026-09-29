# Submission form — field by field

Every field on the CROI 2027 General Abstract Submission form, with a recommended answer and
where it comes from. **Answers marked ⚠ need your decision; I have recorded a recommendation,
not a fact.** Form closes **1 October, 5:00 PM PDT**.

---

## Abstract text — 2,500 characters total

The counter is **total across all four sections**, not per section. We use **2,270**, leaving
230 spare. Paste from `SUBMIT.txt`, one section per field.

> "Do not include section headings in the text as they will automatically be added by the
> submission system."

`SUBMIT.txt` carries no inline `BACKGROUND:` labels for exactly this reason. Copy only the text
between the `--- FIELD n of 4 ---` scaffolding lines.

| field | characters |
|---|---|
| Background | 405 |
| Methods | 579 |
| Results | 871 |
| Conclusions | 415 |
| **total** | **2,270 of 2,500** |

---

## Title — 255 characters

**Temporary Loss of Eligibility and Bias in Cross-Sectional HIV Incidence Estimation** — 82
characters.

> "Enter a concise, descriptive title that identifies the subject of the research **without
> stating the results or conclusions.**"

The earlier assertive title, *…Cancels Exactly in…*, stated the result and was withdrawn
against this rule. See README.md.

---

## Selections

| field | recommended | note |
|---|---|---|
| **Category** | ⚠ Epidemiology of HIV and Emerging Viral Infections in Adults | The letter code "Q" came from the working brief and is **not verified** against CROI's published category list. Check it against the list the form links before selecting. |
| **Study Focus** | ⚠ likely none / not applicable | This is a methods and estimation paper, not a focus area. Check the dropdown before assuming. |
| **Study Population** | ⚠ likely none | The submitted abstract names no population. The stress-test row uses carceral occupancy, but no population-specific claim is made and none should be implied by this field. |
| **Case Report or Meta-Analysis** | No | Neither. |
| **Search Terms** (up to 5) | HIV incidence; cross-sectional survey; recency assay; bias; statistical methods | Use *Other Search Term* if the list lacks these. |
| **Clinical Trial** | No | No trial data are used. The work concerns how placebo incidence would be reconstructed for one. |
| **Commercial Communication Firm** | No | No paid third party. |
| **Graphic Submission** | Yes | One PNG. |
| **Research Group** | No | Single author, single affiliation. |

---

## ⚠ Use of Artificial Intelligence — answer **Yes**

> "Did you use an artificial intelligence (AI) tool in developing the research or preparing
> this abstract?"

**Yes.** Claude (Anthropic) was used for the analytic derivation, the simulation and figure
code, and drafting. All analytic results were checked against an independently written
generative simulator sharing no code, and the full derivation, implementation and test suite
are public. The author is responsible for correctness.

Under-disclosing is the expensive error here: CROI states that failure to adhere to its
policies "may result in the withdrawal of the abstract."

---

## Prior or Anticipated Publication — answer **Yes**, listing the Zenodo deposit

> "Have any data or analyses in this abstract been published, posted as a preprint, submitted
> for publication with publication anticipated before CROI 2027, or otherwise made publicly
> available?"

**Yes.** Paste-ready text:

> Yes. Two items are publicly available; neither has been published in a journal nor posted as
> a preprint.
>
> (1) The predecessor analysis that the present work supersedes — manuscript QAIV24714,
> "Calibration-to-Deployment Mismatch in HIV Prevention Trials: How Structural Censoring Biases
> Counterfactual Incidence Estimates", submitted to *JAIDS* in May 2026 and declined after
> external review — has its software repository publicly archived at Zenodo,
> **DOI 10.5281/zenodo.20344293** (v9.0.0, 22 May 2026, CC-BY-4.0). Its central empirical
> conclusions are **not** carried forward into this abstract. The present work corrects and
> supersedes them, and the correction is the reason this abstract exists.
>
> (2) The derivation, implementation and test suite behind this abstract are in a public
> repository, **github.com/Nyx-Dynamics/nyx-eligibility-dynamics** (MIT). No result in this
> abstract has been submitted to a journal or posted as a preprint.

**Verified 29 September 2026**: the DOI resolves to `zenodo.org/records/20344293`, record is
public, titled *"Software Repository for Calibration-to-Deployment Mismatch in HIV Prevention
Trials…"*, version v9.0.0, published 2026-05-22, licence CC-BY-4.0.

**Do not list Zenodo 10.5281/zenodo.4900634.** That is the CEPHIA public-use dataset — a
third-party input the analysis consumes, not a publication of yours. Listing it would misstate
what has been made public.

Disclosing the superseded deposit is the right call even though its conclusions are withdrawn:
the question asks what is publicly available, not what is still believed, and a reviewer who
finds the predecessor independently should find it already declared.

---

## ⚠ Prior or Anticipated Presentation

No prior or accepted presentation known to me. Confirm against your own record.

---

## Policy confirmations

| policy | note |
|---|---|
| Coauthor Review | Only one author is listed. If anyone else should be, they must review and approve first. |
| Accepted Abstracts Must Be Presented | In-person attendance required at CROI 2027, San Diego, 21–24 March 2027. |
| Financial Disclosure | Must be completed through the CROI Dashboard **before** presenting. |
| Media Consent | Standard. |
| **Copyright** | Submitting **transfers copyright of the abstract** to the CROI Foundation on acceptance. This does not affect the repository: the code is MIT and the study data remain yours. Worth reading before you tick it. |

---

## Graphic

`croi_eligibility_panelA.png` — PNG, 4 × 4 in at 600 dpi, **one panel**, 98 of 100 counted
words. Compliance detail in README.md.
