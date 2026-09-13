# Research methodology

As of 11 September 2026. Applies to Phase 1 research under the [implementation plan](../docs/implementation-plan.md). This document describes how evidence is collected, classified, calculated and checked. It is not a findings report; see [executive-summary.md](executive-summary.md).

## Source priority

1. Home Office
2. Other UK government departments
3. National Crime Agency
4. Border Security Command
5. UK Parliament and the House of Commons Library
6. ONS and other official UK statistical agencies (NRS, NISRA)
7. French government
8. French maritime authorities
9. UK maritime authorities (including MAIB)
10. Peer-reviewed research
11. Reuters, BBC and other established news organizations

News may identify events but does not replace official statistics where they exist. Political social-media posts, advocacy graphics without primary data, unsourced migration websites and anonymous claims are not used.

Every fact must come from a source retrieved and read during research. Facts are never taken from memory or search-result snippets. Sources that could not be retrieved are recorded as unverified leads or data gaps, and produce no claims.

## Registries

- [`sources.json`](sources.json): publisher, title, URL, publication and retrieval dates, type, inspection status, local copy, licence, coverage and caveats. A downloaded source is not necessarily reviewed; `status` says how far it was inspected.
- [`claims.json`](claims.json): each statement with its classification, confidence and rationale, evidence locators, geography, limitations, and a `calculation` block (formula, input claims or files, values) for derived statistics. `approved_for_application` is set only under a recorded human approval ([approval.json](approval.json)), after critical review.
- [`raw/manifest.json`](raw/manifest.json): pinned source files with URLs and SHA-256 hashes. Original files are never modified.

## Evidence classification

| Class | Meaning |
| --- | --- |
| OFFICIAL_STATISTIC | A figure or definition published in official statistics |
| DOCUMENTED_EVENT | An event recorded in a primary official or investigative source, such as a MAIB report, maritime prefecture notice or court record |
| DERIVED_STATISTIC | Our calculation, with formula and input references |
| REPORTED_EVENT | An event or observation described second-hand or attributed, such as news or operational summaries |
| HYPOTHESIS | A proposed explanation, including officials' and researchers' causal interpretations |
| SCENARIO | Hypothetical assumptions and outputs; never observed data |

Confidence is HIGH (direct source support within the stated scope), MEDIUM (attributed interpretation, qualitative trend or limited generalizability) or LOW (lead needing corroboration), always with a rationale. Confidence describes support for the limited statement, not a probability. Classification, source quality and confidence are separate judgements.

The 32 claims from the initial pass were migrated from the earlier five-class scheme on 11 September 2026; the mapping is recorded in `claims.json` under `migration`. Their confidence levels were carried over unchanged and are reassessed in the Phase 2 critical review.

## Crossing statistics

The pinned numeric vintage is the Home Office *Illegal entry routes to the UK summary tables, year ending June 2026* (published 27 August 2026). [`extract_crossings.py`](extract_crossings.py) reads it with the Python standard library and writes:

| File | Contents | Source table |
| --- | --- | --- |
| `crossings/annual-crossings.csv` | People, boats, average people per boat, year-on-year change | IER_02a |
| `crossings/monthly-crossings.csv` | Monthly people, boats and average people per boat | IER_02a |
| `crossings/nationality-by-period.csv` | Arrivals by recorded nationality | IER_02b |
| `crossings/age-sex-by-period.csv` | Arrivals by age group and sex | IER_02c |
| `crossings/asylum-claims-by-arrival-year.csv` | Asylum claims and NRM referrals by arrival year | IER_02d |
| `crossings/crossings-summary.json` | Highest-occupancy months | IER_02a |

Calculation rules:

- Average people per boat = total people / total arriving boats over the same period. Averages of monthly averages are never used.
- Year-on-year changes compare complete calendar years only. 2026 is January–June only and has no year-on-year change.
- A month with no boats has no average (blank, not zero). Months after the pinned cutoff are unpublished and are omitted, not zeroed.
- Highest-occupancy rankings include only months with at least 10 boats, because averages from very few boats are volatile. The threshold is a research choice.
- Values keep six decimal places; display uses two.
- The published average is stored separately from the calculated one wherever the Home Office publishes its own figure.

The script checks that monthly values sum to the published totals, that nationality and age/sex rows sum to their totals, that IER_02b totals match IER_02a, and that IER_02d categories sum to that table's total. It also reconciles July 2025–June 2026 against the published narrative (33,374 people, 511 boats).

Definitions and caveats carried from the source: counts are detected arrivals, including people detected in the Channel and brought to the UK. People intercepted and returned to France are excluded. The series is not disaggregated by departure country. The data comes from a live operational database subject to revision, with enhanced processing from January 2025. Asylum-claim figures count people, not claims, by arrival date. Provisional daily operational data (for example the September 2026 time series) is kept in a separate, dated series and is never appended to the quarterly statistics.

## Geography

Every location has a location type and a precision:

- Location type: OBSERVED LOCATION or REPORTED LOCATION for historical locations. DERIVED CORRIDOR is an analytical product; ILLUSTRATIVE ROUTE is for scenarios and explanatory graphics only.
- Precision: exact coordinates, facility, named place, named area, region or unknown.

A point geometry is recorded only when the source gives coordinates or names a precise fixed place, and it must state its `geometry_source`. A representative point for a named area or region must also state `uncertainty_km`. Otherwise the geometry is null.

Launch sites, passenger pickup sites, rescue locations, reception or disembarkation sites and intended destinations are kept distinct. Vessel tracks are never reconstructed. Lines between documented endpoints are labelled as straight lines, not navigated tracks. Distances are computed only for documented origin–destination pairs. Trends are not inferred from selected incidents; a claim of geographic expansion requires a representative distribution over time.

## Scenarios

[`build_scenarios.py`](build_scenarios.py) writes `scenarios/` from the observed outputs above. Scenarios are hypothetical arithmetic on stated assumptions. They are not forecasts, are classified SCENARIO, and are stored apart from observed data.

- **Crossings.** Modelled arrivals = assumed arriving boats × assumed average people per arriving boat, over an undated 12-month period. The baseline is July 2025–June 2026 (33,374 people, 511 boats). REDUCTION halves the boats and holds occupancy; CONTINUATION holds both; EXPANSION combines the highest calendar-year boats (2022) with the highest monthly occupancy among months with at least 10 boats (November 2025), a combination never observed. Occupancy is not capacity, and no departure, interception or utilisation rate is used.
- **Checks.** CONTINUATION reproduces the baseline.
- **This release** includes the crossing scenarios only. `build_scenarios.py` is kept unchanged, but it also needs after-arrival data that is not in this release, so it cannot be re-run here.

## Validation

[`validate_research.py`](validate_research.py) checks:

- sources, and raw-file hashes against the manifest
- claim schema, classifications, confidence and source references
- derived-claim inputs
- crossing CSV arithmetic against the annual, occupancy, year-on-year and comparison claims
- GeoJSON location rules

These are structural and numeric checks, not fact-checking. Independent critical review is Phase 2, and research approval is a human decision.

Source datasets do not always use consistent capitalisation (for example "Main Applicant" and "Main applicant" in the IER detailed dataset). Published labels are kept verbatim in outputs, and comparisons and aggregations match labels case-insensitively.

## Critical review (Phase 2)

[critical-review.md](critical-review.md) records the Part 18 review. Separate reviewers, without access to the authors' reasoning, each tried to disprove one area: H1, H2, H3–H4, H5, cross-cutting framing and bias, and a seeded random numeric spot-check of 36 claims. The lead researcher verified every finding used against the pinned files before changing any claim. Corrections to claims are applied in the registry. Changes to data-producing scripts owned by other workstreams are listed as "Required before Phase 3" so each can be reviewed separately.

```sh
python3 research/extract_crossings.py
python3 research/validate_research.py
```
