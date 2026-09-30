# Data

No participant-level or licensed data are redistributed here.

**One exception, and it is not an exception to that rule.** `data/bjs/` holds 102 BJS
statistical tables as published CSVs. They are US Government works in the public domain,
aggregate rather than participant-level, and each file carries its own citation block naming
the report, NCJ number, author and version date. They are committed so that §3.7 can be
checked against its source rather than against a summary. Publisher PDFs and supplements are
**not** committed and are gitignored; see `manuscript/references.md`.

## Retrieval

**CEPHIA public-use dataset** — Zenodo 10.5281/zenodo.4900634. Place the CSV at
`data/cephia_public_use_dataset_20210604.csv` (gitignored). Tests requiring it skip when absent.

**Vera Institute Incarceration Trends** — `incarceration_trends_county.csv` from
github.com/vera-institute/incarceration-trends (`main`).

**BJS** — Prisoners and Jail Inmates statistical-tables series, bjs.ojp.gov.

**Census PEP** — county age structure, `cc-est2019-alldata-<STATE>.csv`.

## fixtures/

Small derived files sufficient to run the suite offline. `p4_county.csv`,
`county_agedenom.csv` and `p4_final.csv` are aggregate county-level values with no
individual records.

**Before committing anything CEPHIA-derived, verify the dataset's redistribution terms.**
The intended pattern is synthetic inputs with the real schema for functional tests, plus a
frozen `cephia_expected.json` holding only MDRI, CI bounds and reference curve points — not
participant-derived rows.
