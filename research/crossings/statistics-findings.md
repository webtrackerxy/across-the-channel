# Phase 1A statistics: findings

Research date: 11 September 2026. Every claim is `source_checked_pending_independent_review`, with `approved_for_application: false`.

## Files

Scripts are in `research/`; their outputs are in `research/crossings/`. The draft registry files were merged into `research/sources.json`, `research/claims.json` and `research/raw/manifest.json`.

| Script | Output |
| --- | --- |
| `extract_decisions.py` | `asylum-decisions-by-arrival-year.csv` |
| `reconcile_series.py` | `annual-series-vintages.csv` and `published-occupancy.csv` (37 rows) |
| (merged) | 19 new sources, 43 `STAT-` claims and 7 raw-file manifest entries, now in the main registries |

- Run `reconcile_series.py`, then `extract_decisions.py` (see `research/README.md` for the full order). Both use the Python standard library only.
- `reconciliation.md` gives the full reconciliation narrative.
- New raw files saved in `research/raw/`:
  - `illegal-entry-routes-to-the-uk-detailed-dataset-jun-2026.xlsx` (`HO-IER-DETAILED-2026Q2`)
  - Earlier summary-table vintages: `HO-TABLES-2021Q4`, `HO-TABLES-2022Q4`, `HO-TABLES-2024Q4`, `HO-TABLES-2025Q4`, `HO-TABLES-2026Q1`
  - The ICIBI report PDF (`ICIBI-DOVER-2022-REPORT`)

## 1. Asylum outcomes by arrival year

**Source.** `HO-IER-DETAILED-2026Q2`, sheets Data_IER_D02 and Data_IER_D03, published 27 August 2026.

**Definitions** (dataset Notes sheet, notes 18–26):
- Counts are **people** (main applicants and dependants), not claims.
- Years are **arrival years**, not claim or decision years.
- Only claims made within 14 days of arrival are included.
- Outcomes are the first (initial) decision as at extraction. For 2023–2025 arrivals this includes decisions up to 15 July 2026. Pre-2023 cohorts were not revised in this release, and their extraction date is not stated.
- Only records that could be matched between arrival and asylum data are included.

**Checks built into the script:**
- D03 outcomes sum to D02 claims, for people and for main applicants.
- D02 totals equal IER_02d in `HO-TABLES-2026Q2`.

Per-year claims are `STAT-ASYLUM-OUTCOMES-2018` to `-2025`, and the total is `STAT-ASYLUM-OUTCOMES-2018-2025`. Per-year grant rates are `STAT-GRANTRATE-2018` to `-2025`.

| Arrival year | People with claim | Grants | Refused | Withdrawn | Admin outcome | Awaiting | Grant rate (HO definition) | Grants ÷ all outcomes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2018 | 280 | 145 | 129 | 5 | 1 | 0 | 52.9% | 51.8% |
| 2019 | 1,813 | 815 | 948 | 41 | 4 | 5 | 46.2% | 45.1% |
| 2020 | 8,276 | 4,166 | 3,458 | 405 | 176 | 71 | 54.6% | 50.8% |
| 2021 | 25,276 | 15,872 | 5,082 | 3,111 | 923 | 288 | 75.7% | 63.5% |
| 2022 | 41,188 | 17,178 | 7,093 | 9,862 | 6,266 | 789 | 70.8% | 42.5% |
| 2023 | 27,610 | 10,758 | 10,881 | 4,272 | 1,086 | 613 | 49.7% | 39.8% |
| 2024 | 35,276 | 13,732 | 14,784 | 4,272 | 681 | 1,807 | 48.2% | 41.0% |
| 2025 | 39,952 | 18,743 | 14,016 | 2,214 | 471 | 4,508 | 57.2% | 52.9% |
| 2018–2025 | 179,671 | 81,409 | 56,391 | 24,182 | 9,608 | 8,081 | 59.1% | 47.4% |

**Grants** = Grant of Protection + Grant of Other Leave.

**Grant rate (Home Office definition).** Grants ÷ (grants + refused), excluding withdrawn claims and administrative outcomes.
- The definition is published in `HO-ASYLUM-SB-2026Q1`, the notes to Table 1.
- The Home Office does not publish per-year rates for arrival cohorts, so ours are DERIVED_STATISTIC.
- Main-applicant (case) rates are also in the CSV. For 2018–2025 the case rate is 59.5%.

**Grants ÷ all outcomes** = grants ÷ (grants + refused + withdrawn + administrative). This is **not** the Home Office rate. It is shown only because the choice of denominator changes the result a lot: 2022 is 70.8% on the Home Office definition but 42.5% on all outcomes.

**Decided share of claims.** The Home Office's "received an initial decision" counts grants and refusals only. On that basis, 76.7% of 2018–2025 claims had been decided.

**Earlier vintage.** The YE March 2026 chapter (`STAT-HO-GRANTRATE-2018-2025-MAR2026`) reported, for people:
- 178,845 with a claim
- 132,894 decided: 79,589 granted and 53,305 refused
- 12,538 awaiting
- 33,413 withdrawn or administrative
- A 60% grant rate on cases (72,236 of 119,637)

The June 2026 dataset supersedes these figures; do not mix the two vintages.

**Commons Library check** (`STAT-HOCL-DECISIONS-RECON`, `HOCL-CBP-10590`). All of its rounded figures match our June 2026 totals: about 180,000 claims; 138,000 decided (77%); 81,000 granted (59%); 56,000 refused; about 8,000 awaiting; 19% withdrawn or administrative. The briefing calls these "applications", but the Home Office counts people.

**Cautions:**
- Recent cohorts still have many cases pending (2025: 4,508 awaiting), so their rates may shift.
- These are initial decisions only; no appeal or final-outcome data are available.
- Asylum-claim shares are in the CSV as a cross-check only. IER_02d claim shares belong to another workstream.

## 2. Published vs calculated occupancy

The Home Office publishes average people per boat **only in narrative text**. The pinned IER_02a table (`HO-TABLES-2026Q2`) and the small-boat time series (`HO-SB-ACTIVITY-2026-09-10`, sheets SB_01/SB_02) have no average column.

A published figure exists for every calendar year, and each one equals our people ÷ boats figure from IER_02a rounded to a whole number (`STAT-OCC-PUBLISHED-MATCH`):

| Year | Published | Calculated | Claim | Sources |
| --- | ---: | ---: | --- | --- |
| 2018 | 7 | 6.95 | `STAT-PUBOCC-2018` | `HO-2021-NARRATIVE`, `HO-2022-NARRATIVE`, `HO-2023-NARRATIVE`, `HO-2026Q2` |
| 2019 | 11 | 11.24 | `STAT-PUBOCC-2019` | `HO-2021-NARRATIVE`, `HO-2022-NARRATIVE` |
| 2020 | 13 | 13.21 | `STAT-PUBOCC-2020` | `HO-2021-NARRATIVE`, `HO-2022-NARRATIVE`, `HO-2023-NARRATIVE` |
| 2021 | 28 | 27.59 | `STAT-PUBOCC-2021` | `HO-2021-NARRATIVE`, `HO-2022-NARRATIVE`, `HO-2024-NARRATIVE` |
| 2022 | 41 | 41.24 | `STAT-PUBOCC-2022` | `HO-2022-NARRATIVE`, `HO-2023-NARRATIVE`, `HO-2025`, `HO-2026Q1-NARRATIVE` |
| 2023 | 49 | 48.90 | `STAT-PUBOCC-2023` | `HO-2023-NARRATIVE`, `HO-2024-NARRATIVE` |
| 2024 | 53 | 52.97 | `STAT-PUBOCC-2024` | `HO-2024-NARRATIVE`, `HO-2025` |
| 2025 | 62 | 61.71 | `STAT-PUBOCC-2025` | `HO-2025` |
| 2026 Jan–Jun | not published | 65.30 | — | none found; partial year |

**Other published periods:**

| Period | Published | Calculated | Claim or source |
| --- | ---: | ---: | --- |
| YE Jun 2026 | 65 | 65.31 | `STAT-PUBOCC-YEJUN2026` |
| YE Mar 2026 | 63 | 63.04 | `STAT-PUBOCC-YEMAR2026` |
| FY 2025/26 | 63 | 63.04 | `STAT-PUBOCC-BSC-FY2025-26` (`BSC-2026`, footnote 35; April–March span assumed) |
| YE Jun 2025 | 56 | 56.39 | `STAT-PUBOCC-YEJUN2025` |
| September and November 2025 | 71 each | 70.61 and 70.85 | `STAT-PUBOCC-MONTHLY-RECORD-2025` |

Published values recorded only in `published-occupancy.csv`, without a separate claim:
- YE Mar 2022: 29 (`HO-2025Q1-NARRATIVE`)
- YE Mar 2024: 50 (`HO-2025Q1-NARRATIVE`)
- YE Mar 2025: 54 (`HO-2025Q1-NARRATIVE`)
- YE Jun 2024: 51 (`HO-2025Q2-NARRATIVE`)
- June 2025: 65 (`HO-2025Q2-NARRATIVE`)
- August–October 2022: 45 (`HO-2022-NARRATIVE`)

**YE March 2024 mismatch** (`STAT-OCC-YEMAR2024-MISMATCH`).
- `HO-2026Q1-NARRATIVE` (published 21 May 2026, updated 16 July 2026) says, in section 2.2: "54 people per boat in the YE March 2024".
- Our calculation from IER_02a gives 49.73 for April 2023–March 2024 and 54.32 for April 2024–March 2025.
- The Home Office's own earlier release, `HO-2025Q1-NARRATIVE` (22 May 2025), gives 50 for YE March 2024 and 54 for YE March 2025.
- The later sentence is therefore probably mislabelled (`STAT-OCC-YEMAR2024-LABEL-HYPOTHESIS`: HYPOTHESIS, MEDIUM). Do not cite 54 for YE March 2024.

**Limitations:**
- Published values are whole numbers, so differences under 0.5 cannot be detected.
- Average occupancy is not rated vessel capacity.

## 3. Reconciliation across vintages

Full detail is in `reconciliation.md`; `annual-series-vintages.csv` holds the comparison data. The pinned series is `HO-TABLES-2026Q2`, IER_02a.

**2018–2021 are identical in all six vintages checked, down to monthly values** (`STAT-VINTAGE-2018-2021-STABLE`):

| Year | People | Boats |
| --- | ---: | ---: |
| 2018 | 299 | 43 |
| 2019 | 1,843 | 164 |
| 2020 | 8,466 | 641 |
| 2021 | 28,526 | 1,034 |

The vintages checked run from the first release on 24 February 2022 to the pinned release on 27 August 2026: `HO-TABLES-2021Q4`, `-2022Q4`, `-2024Q4`, `-2025Q4`, `-2026Q1`, `-2026Q2`.

**2022 was revised** (`STAT-VINTAGE-2022-REVISION`):
- `HO-TABLES-2022Q4` (February 2023) gave 45,755 people and 1,109 boats.
- From `HO-TABLES-2024Q4` (February 2025) onwards the figures are 45,774 people and 1,110 boats.
- The changes are in July–September 2022 people and September boats. Later notes attribute 2022 Q3 to casework systems.
- The intermediate vintage that first made the revision was not identified.

**2023–2025 are stable** (`STAT-VINTAGE-2023-2025-STABLE`):
- 2023 and 2024 are unchanged from the December 2024 vintage to June 2026.
- 2025 (41,472 people, 672 boats) is unchanged across the December 2025, March 2026 and June 2026 vintages, at monthly level.
- June 2026 note 5 says January 2025–March 2026 small-boat data were revised, yet the IER_02a totals for those months did not change. The revision may affect only breakdowns such as nationality or age; this is unverified.

**Matched-record totals are lower by design.** IER_02d and IER_D02 give matched arrivals of 285, 1,833, 8,406, 28,023, 45,478, 28,200, 35,898 and 40,595 for 2018–2025. They are lower because records are matched to asylum data and extracted on different dates. Use them only as denominators for claim and decision shares.

**Commons Library** (`STAT-HOCL-ANNUAL-RECON`, `HOCL-CBP-10590`, dated 2 September 2026 in the API record). Its summary matches the pinned series:

| Commons Library figure | Pinned value |
| --- | --- |
| 299 in 2018 | 299 |
| about 46,000 in 2022 | 45,774 |
| 41,000 in 2025 | 41,472 |
| 205,000 from 2018 to June 2026 | 204,517 |
| 7 per boat in 2018; 65 in YE June 2026 | 7 and 65 |

It gives no boat counts.

**ICIBI 236 / 286 / 299** (`STAT-ICIBI-2018-FIGURES`; sources `ICIBI-DOVER-2022-REPORT` and `ICIBI-DOVER-2022`).

What the report says:
- Paragraph 2.1 says numbers rose "from 236 in 2018 to 28,526 in 2021". The press notice repeats 236 and attributes it to "Home Office statistics".
- Paragraph 4.1 and Figure 1 give 286 for 2018, 1,834 for 2019, 8,486 for 2020 and 28,526 for 2021. The table's percentage-increase column reads 541%, 362% and 236%.
- Figure 1 cites no data source. Its footnote says only "Calendar year".

Explanation of 236 (`STAT-ICIBI-236-HYPOTHESIS`, HYPOTHESIS, MEDIUM):
- 236 is exactly the 2020-to-2021 percentage increase in the report's own Figure 1 (28,526 ÷ 8,486 = 3.36).
- Paragraph 2.1 most likely copied that percentage as if it were the 2018 count.

Explanation of 286 (`STAT-ICIBI-286-HYPOTHESIS`, HYPOTHESIS, LOW):
- The Figure 1 values probably came from Home Office operational data supplied during the inspection.
- The report went to the Home Office for factual checking on 8 February 2022 (paragraph 1.4). That was before the first official release on 24 February 2022 (`HO-TABLES-2021Q4`), which already gave 299, 1,843 and 8,466.
- 286 and 1,834 are close to the matched-record totals of 285 and 1,833, but 8,486 does not match 8,406. This remains unconfirmed.

Conclusion: 299 is the official statistic in every vintage checked. Do not use 236 or 286 in the series.

## 4. Departure-country coverage

No official UK statistical output reviewed breaks small-boat arrivals down by departure country or launch location (`STAT-DEPARTURE-NOT-DISAGGREGATED`, DOCUMENTED_EVENT, HIGH within the reviewed outputs).

What was checked:
- **Detailed dataset (`HO-IER-DETAILED-2026Q2`).** The List_of_Fields sheet has only these variables: year/quarter, method of entry, nationality, region, sex, age group, and asylum/NRM fields.
- **Summary tables (`HO-TABLES-2026Q2`).** Same scope; no departure variable.
- **Time series (`HO-SB-ACTIVITY-2026-09-10`; file `raw/small-boats-2026-09-04.ods`, existing ID `HO-DAILY-2026-09-04`).** Columns cover migrants arrived, boats arrived, uncontrolled landings, migrants prevented and events prevented only.
- **Weekly summary.** Prevention figures are operational estimates supplied by French authorities. They count people prevented from departing France or returned to France.
- **User guide (`HO-USER-GUIDE-2026-08`).** Describes exclusions and juxtaposed controls in France and Belgium, but no departure variable.
- **Commons Library summary (`HOCL-CBP-10590`).** Gives no departure breakdown.
- **Border Security Commander's report (`BSC-2026`).** Mentions launches from Belgium only qualitatively ("a small number further north in Belgium"; taxi boats departing from the Belgian coast), without counts. The existing claims `BELGIUM-2026` and `BELGIUM-EXPLANATION` already cover this.

Do not label the series "departures from France". Absence of a published breakdown does not show that the Home Office holds no such data.

## Unverified items and gaps

- **Commons Library full briefing.** The page, PDF and XLSX returned HTTP 403 (Cloudflare), and the Chrome extension was not connected. Only the summary from the Parliament data API was read. Its tables, charts and earlier versions were not checked.
- **Belgian departure counts.** A web search snippet attributed "17 small boat launches from Belgium" in 2026 to news coverage. It was not retrieved, so no claim was made.
- **Committee oral evidence.** The evidence cited by `OXFORD-QA-2026-09` (committees.parliament.uk/oralevidence/17917) returned HTTP 403. Belgian and French primary sources are still needed.
- **Vintage coverage.** 12 of about 18 quarterly Home Office vintages were not checked, including the one that first revised 2022.
- **Note 5 revision.** It is unclear what the stated January 2025–March 2026 revision actually changed, since IER_02a totals did not move.
- **ICIBI Figure 1 source.** The data source and extraction date are unconfirmed; `STAT-ICIBI-236-HYPOTHESIS` and `STAT-ICIBI-286-HYPOTHESIS` are unconfirmed by the ICIBI.
- **Home Office correction.** No correction to the YE March 2024 "54" sentence has been issued.
- **Outcome data.** There are no appeal or final-outcome data by arrival cohort. The extraction date for pre-2023 decisions is not stated.
- **Asylum support.** No linkage from these cohorts to asylum support or geography exists in these datasets.

## Conflicts with existing research

- **236 vs 299.** `research/data-gaps.md` (Priority 3) and the notes on existing source `ICIBI-DOVER-2022` treat this as unresolved. It is now explained in `STAT-ICIBI-236-HYPOTHESIS`, reviewed in Phase 2 ([critical-review.md](../critical-review.md)).
- **`BSC-2026` date.** The existing record gives published 16 July 2026 and updated 6 August 2026. The GOV.UK content API reports first publication of the accessible HTML version as 6 August 2026.
- **`HO-DAILY-2026-09-04`.** It is listed in `raw/manifest.json` but missing from `research/sources.json`.
- **Classification scheme.** `research/claims.json` still uses the old classes (such as OBSERVED FACT). The new `STAT-` claims use the six-class scheme.
- **Departure-country class.** `STAT-DEPARTURE-NOT-DISAGGREGATED` uses DOCUMENTED_EVENT as the nearest fit for a documented property of the data. Review this in Phase 2.
- **`research/report.md`** (since replaced by `research/executive-summary.md`). It said parliamentary synthesis was not done. This workstream now covers the Commons Library summary.
- **Denominators.** IER_02d/IER_D02 matched totals, such as 285 for 2018, differ from the IER_02a arrival counts. They must not be substituted into the annual series.
