# Data

No participant-level or licensed data are redistributed here.

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
