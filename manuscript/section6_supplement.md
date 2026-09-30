# Paper A — Supplement (draft rev. 1)

> Material moved out of the main text at the narrowing. None of it establishes
> the central result; each item demonstrates, parameterises or stress-tests it.
> Numbering continues the main text's supplementary series.

---

## S1. Site-level carceral exposure parameters

For the site-level sensitivity of §S2 we use the nine United States counties hosting PURPOSE 4 (NCT06101342), chosen because it is the cleanest available anchor for carceral geography in an HIV prevention trial. The registry record describes a phase 2, open-label, multicentre, randomised study of the pharmacokinetics and safety of twice-yearly subcutaneous lenacapavir for pre-exposure prophylaxis in people who inject drugs in the United States, with eligibility from 18 years and no upper bound, nine locations, and **181 participants enrolled**; it began in December 2023 and reached actual primary completion in July 2026.

Two things follow. The ≥18 frame is why adult PWID mortality from ALIVE is the appropriate source in §3.4 rather than a younger-cohort estimate. And at 181 participants across nine sites — roughly twenty each — **no site-level empirical claim would be supportable from this trial even in principle**, which is part of why §S2 is a break-even calculation rather than a correction. **No efficacy estimate from this trial is corrected or commented on**; it is a phase 2 pharmacokinetics and safety study and reports none.

The nine registry locations map to counties as follows, and the mapping is one-to-one: Los Angeles and San Diego, California; Miami, Florida (Miami-Dade); Baltimore, Maryland (Baltimore City); Newark, New Jersey (Essex); The Bronx, New York; Philadelphia, Pennsylvania; Houston, Texas (Harris); and Morgantown, West Virginia (Monongalia).

Jail and prison counts are taken at county level for 2019, the last year with harmonized county-level estimates across all nine counties. **2019 is a fixed pre-pandemic structural anchor and is not assumed to be conservative** — the data disprove that reading. Post-2019 jail trajectories are heterogeneous in both magnitude and direction: relative to 2019, jail populations stand at 0.46 in the Bronx and 0.70 in San Diego, but 1.02 in Miami-Dade, 1.05 in Monongalia and 1.09 in Essex. Four of nine counties are at or above their 2019 level, so a single national multiplier would have been wrong in direction for them. A secondary analysis updates the jail component with the most recent local data while retaining the 2019 prison component, county-level post-2019 prison counts being unavailable.

Incarceration rates are published against total or 15–64 populations while trial eligibility is 18+, so a denominator conversion is required. A national 15–64 to 18+ ratio of 0.8333 was replaced with county-specific ratios from Census Population Estimates 2019, which range from 0.834 (Miami-Dade) to 0.908 (Harris). The national factor systematically understated exposure in counties with younger adult age structures, by up to 12.4%. Consistent with §3.5, the correction is applied to the denominator only.

---

## S2. Site-specific break-even relative acquisition hazards

To indicate the range of $\eta$ at which the composed boundary would cross unity in real catchments, we evaluated nine United States counties with published jail and prison occupancy, using county-specific age denominators (Table S3b). Break-even $\eta$ ranged from 0.04 (San Diego) to 0.55 (Baltimore City); in two counties, Bronx and Miami-Dade, the boundary never crosses unity for any $\eta\in[0,1]$.

The trial enrolled 181 participants across those nine sites, so roughly twenty each; no site-level empirical claim would be supportable from it even in principle. **This is a sensitivity range, not an epidemiologic claim about any site.** It states the value $\eta$ would have to take for the two selection mechanisms to stop cancelling, given that county's carceral occupancy. It does not assert that $\eta$ takes that value anywhere, and no trial estimate is corrected on its basis. Its purpose is to show that the break-even value lies inside the plausible interval implied by the only available incidence comparison, so the question is empirical rather than hypothetical.

---

## S3. Comparison with covariate-reweighting methods

Covariate transport by reweighting — matching the survey population to the trial-eligible population on measured covariates — addresses a different failure and does not remove this one. In a population where the observable and target covariate distributions coincide, which is the counterfactual-placebo case of interest, reweighting removes 0% of the bias: the naive and reweighted estimates are identical at 0.0387 against a truth of 0.0400, both attenuated by 3.3% (Table S2). Where the distributions differ, reweighting performs as designed, removing 91.3% and 96.8% of a much larger composition-driven bias in the two enriched cases.

The reason is structural. Reweighting corrects the *composition* of the sampled population; it cannot correct the within-stratum duration component, which is below unity in every stratum, so any weighted average of within-stratum factors remains below unity. The two methods are complementary rather than alternative: reweighting for covariate imbalance, the weight $w_t$ for eligibility dynamics.
