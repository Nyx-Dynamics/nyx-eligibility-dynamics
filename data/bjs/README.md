# BJS statistical tables

Source tables behind §3.5–3.7. **US Government works, in the public domain** — which is why
these are committed while the publisher PDFs in the reference archive are not.

Downloaded from bjs.ojp.gov; each CSV carries its own citation block naming the report,
NCJ number, author and version date, so the provenance travels with the file.

| series | report | NCJ | used for |
|---|---|---|---|
| `hivp15st` | HIV in Prisons, 2015 – Statistical Tables | not embedded | not cited; retained as the earlier vintage. Its CSVs predate the citation block and carry no NCJ |
| `hivp20st` | HIV in Prisons, 2020 â Statistical Tables | 302601 | §3.5, negative control: HIV prevalence cannot substitute for injection prevalence |
| `mlj0019st` | Mortality in Local Jails, 2000–2019 – Statistical Tables | 301368 | §3.7 in-custody mortality, local jails |
| `msfp0119st` | Mortality in State and Federal Prisons, 2001–2019 – Statistical Tables | 300953 | §3.7 in-custody mortality, state and federal prisons |

## Not in this drop

The BJS **Prisoners** series is absent. It supplies one figure — the 453 per 100,000 adult
imprisonment rate used in Route C of §3.5 — and its edition is not pinned. Route C is one of
three routes to occupancy and agrees with the BJS-free Route B to 0.04 percentage points, so
no conclusion depends on it. The 2020 edition reports 358 per 100,000, depressed by the
pandemic, so the figure belongs to a different year.

Mean time served is **not** in the Prisoners series at all. It is *Time Served in State Prison,
2018* (Kaeble, NCJ 255662): 2.7 y mean, 1.3 y median. §3.6 previously attributed it to
*Prisoners* and now cites the right report.

## Verified against these tables

- **Local jail all-cause mortality 2019**: cause-specific rates per 100,000 sum to 166 (illness 77, suicide 49, drug/alcohol intoxication 26, accident 3, homicide 3, other 3, missing 5) against a published total of 167. BJS's own note says details may not sum to totals due to rounding.
- **The 184 figure is a count, not a rate.** `mlj0019stt01.csv` (number of deaths) gives 184 drug/alcohol-intoxication deaths in 2019; `mlj0019stt03.csv` (rate per 100,000) gives 26. An earlier note suspected this without being able to check it. Do not cite 184 as a rate.
- **Prison all-cause mortality 2019**: state components sum to 331 against a published 330;
  federal to 260 against 259. Same rounding pattern as the jails, and both confirm §3.7.
- **HIV in prisons**: 11,940 in custody of state and federal prisons at yearend 2020, confirming the figure used in §3.5.

