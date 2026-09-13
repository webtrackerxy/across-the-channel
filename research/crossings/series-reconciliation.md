# Reconciliation of the annual small-boat series

Research date 11 September 2026. The pinned series is `HO-TABLES-2026Q2` (IER_02a, published 27 August 2026). This note records differences and does not overwrite anything. The comparisons are reproduced by `reconcile_series.py`, which writes `annual-series-vintages.csv` and `published-occupancy.csv`.

## 1. Home Office table vintages

Six vintages were compared programmatically, with monthly sums checked against totals in each:

| Vintage | Published |
| --- | --- |
| `HO-TABLES-2021Q4` | 24 Feb 2022 (first release of the series) |
| `HO-TABLES-2022Q4` | 23 Feb 2023 |
| `HO-TABLES-2024Q4` | 27 Feb 2025 |
| `HO-TABLES-2025Q4` | 26 Feb 2026 |
| `HO-TABLES-2026Q1` | 21 May 2026 |
| `HO-TABLES-2026Q2` | 27 Aug 2026 (pinned) |

| Year | Pinned people / boats | Differences in earlier vintages |
| --- | --- | --- |
| 2018 | 299 / 43 | None: identical monthly values in all six vintages |
| 2019 | 1,843 / 164 | None |
| 2020 | 8,466 / 641 | None |
| 2021 | 28,526 / 1,034 | None |
| 2022 | 45,774 / 1,110 | Feb 2023 vintage: **45,755 / 1,109**. July–Sept people were 3,687 / 8,631 / 7,964 (now 3,673 / 8,574 / 8,054) and September boats were 179 (now 180). The revised figures appear in the Feb 2025 vintage, which cites casework systems for 2022 Q3. The intermediate vintage that first revised it was not identified. |
| 2023 | 29,437 / 602 | None in the Dec 2024 to Jun 2026 vintages |
| 2024 | 36,816 / 695 | None in the Dec 2024 to Jun 2026 vintages |
| 2025 | 41,472 / 672 | None in the Dec 2025, Mar 2026 and Jun 2026 vintages, at monthly level |

June 2026 note 5 says January 2025 to March 2026 small-boat data "has been revised". However, the IER_02a monthly people and boat counts for 2025 and Jan–Mar 2026 are identical in the March 2026 and June 2026 vintages. The revision may affect breakdowns such as nationality or age rather than totals; this is unverified. Only 6 of about 18 quarterly vintages were checked.

**Matched-record totals differ by design.** IER_02d and IER_D02 give matched arrivals of 285, 1,833, 8,406, 28,023, 45,478, 28,200, 35,898 and 40,595 for 2018–2025. They are lower than IER_02a because arrival records are matched to asylum/NRM records and extracted on different dates (notes 19–20 and 23). Use them only as denominators for claim and decision shares, never as arrival counts.

## 2. House of Commons Library

`HOCL-CBP-10590`, *Statistics on small boat Channel crossings*, dated 2 September 2026 in the API record.

The commonslibrary.parliament.uk page and the researchbriefings PDF/XLSX both returned HTTP 403 (Cloudflare challenge), and the Chrome extension was not connected. The title, date and full summary text were instead retrieved from the official Parliament linked-data API (`lda.data.parliament.uk/researchbriefings.json?identifier=CBP-10590`).

The summary is consistent with the pinned series:
- 299 in 2018 (exact).
- "Around 46,000" in 2022 (45,774).
- "41,000" in 2025 (41,472).
- 205,000 detected from 2018 to June 2026 (204,517).
- 7 people per boat in 2018 and 65 in YE June 2026.

It gives no boat counts. Its asylum-outcome figures (about 180,000; 138,000 decided or 77%; 81,000 granted or 59%; 56,000 refused; about 8,000 awaiting; 19% withdrawn or administrative) match the June 2026 detailed dataset's people totals exactly (see `STAT-HOCL-DECISIONS-RECON`). The briefing calls these "applications", but the Home Office counts people, including dependants.

**Not done:** the briefing's own tables and charts could not be inspected, and no earlier Commons Library vintage was compared.

## 3. The 2018 discrepancy: ICIBI 236 vs pinned 299

**Finding:** the ICIBI report itself contains two different 2018 figures, and neither is the Home Office official statistic.

- **Paragraph 2.1** (summary of conclusions): "increased from 236 in 2018 to 28,526 in 2021". The press notice repeats 236 and attributes it to "Home Office statistics".
- **Paragraph 4.1 and Figure 1**: "In 2018, a total of 286 migrants reached the UK". Figure 1 lists 2018 286; 2019 1,834 (541%); 2020 8,486 (362%); 2021 28,526 (**236%**). Footnote 5 says only "Calendar year", and no data source is stated.
- **Home Office**: 299, 1,843, 8,466, 28,526 in every vintage from the first official release (24 Feb 2022) to the pinned one.

**Explanation for 236 (`STAT-ICIBI-236-HYPOTHESIS`, HYPOTHESIS, MEDIUM).** 236 is exactly the percentage increase from 2020 to 2021 in the report's own Figure 1 (28,526 / 8,486 = 3.36, an increase of 236%). The same table gives 286 for 2018. The most likely explanation is a transcription error in paragraph 2.1 that was carried into the press notice. The ICIBI has not confirmed this.

**Explanation for 286 (`STAT-ICIBI-286-HYPOTHESIS`, HYPOTHESIS, LOW).** Figure 1 was probably built from Home Office operational data supplied during the inspection. The report went to the Home Office for factual checking on 8 February 2022 (paragraph 1.4), before the first official release on 24 February 2022. 286 and 1,834 are close to the matched-record totals (285 and 1,833 in IER_02d/IER_D02), but 8,486 is not (8,406). This remains unconfirmed.

**Conclusion:** 299 is the official statistic in every vintage checked; keep it. Do not use 236 or 286 in the series. This resolves the open item in `research/data-gaps.md` Priority 3. The Phase 2 numeric spot-check confirmed 299 against the pinned IER_02a table (`ANNUAL-2018`, [critical-review.md](../critical-review.md)).

## 4. Published vs calculated occupancy

See `published-occupancy.csv`, which has 37 rows. Every published calendar-year average from 2018 to 2025 (7, 11, 13, 28, 41, 49, 53, 62) equals our calculated people / boats from the pinned IER_02a, rounded to a whole number. The rolling, financial-year and monthly figures also match, with one exception:

- The **YE March 2026** release (published 21 May 2026, updated 16 July 2026) states "54 people per boat in the YE March 2024".
- The calculated values are 49.73 for April 2023–March 2024 and 54.32 for April 2024–March 2025.
- The Home Office's own **YE March 2025** release gives 50 for YE March 2024 and 54 for YE March 2025.

The later sentence is therefore probably mislabelled (`STAT-OCC-YEMAR2024-MISMATCH`, `STAT-OCC-YEMAR2024-LABEL-HYPOTHESIS`). The 54 should not be cited for YE March 2024.

No published average was found for **January–June 2026**; the only calculated value is 65.30. The IER_02a summary tables and the small-boat time series (SB_01/SB_02) contain no average column. Published averages appear only in the narrative text of releases and in the BSC report (63 in 2025/26, which cites the release).

## 5. Asylum-decision vintages

The YE March 2026 chapter (`HO-ASYLUM-SB-2026Q1`) reported, for people:
- 178,845 with a claim.
- 132,894 decided: 79,589 granted and 53,305 refused.
- 12,538 awaiting a decision.
- 33,413 withdrawn or given an administrative outcome.
- A 60% grant rate on cases.

The June 2026 detailed dataset (decisions to 15 July 2026 for 2023–2025 arrivals) gives, for people:
- 179,671 with a claim.
- 137,800 decided: 81,409 granted and 56,391 refused.
- 8,081 awaiting a decision.
- 33,790 withdrawn or given an administrative outcome.
- A 59.1% grant rate for people and 59.5% for main applicants.

Treat these as different vintages; do not mix them.
