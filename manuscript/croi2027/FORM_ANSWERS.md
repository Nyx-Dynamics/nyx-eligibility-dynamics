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

## ⚠ Prior or Anticipated Publication — needs your call

> "Have any data or analyses in this abstract been published, posted as a preprint, submitted
> for publication with publication anticipated before CROI 2027, or **otherwise made publicly
> available**?"

Facts you are answering against:

- The full analysis, code and test suite are in a **public GitHub repository**,
  `Nyx-Dynamics/nyx-eligibility-dynamics`. That is plainly "otherwise made publicly available."
- The **predecessor** analysis — manuscript QAIV24714, submitted to JAIDS May 2026 and declined
  after review — is archived at **Zenodo 10.5281/zenodo.20344293**. Its central empirical
  conclusions are *not* carried forward and are explicitly superseded, but the deposit is
  public.
- Nothing in *this* abstract has been submitted to a journal or posted as a preprint.

A defensible answer is **Yes**, naming the public repository and the superseded Zenodo deposit.
It is your call, and it turns on whether a public methods repository counts for CROI's purpose.

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
