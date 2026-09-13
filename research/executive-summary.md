# Small-boat crossings, 2018–2026: executive summary

As of 11 September 2026. This release covers Channel crossings up to arrival in the UK: the crossing research and the crossing scenarios. Phase 1A covers crossing statistics, vessels, geography, route distances and explanations; the crossing scenarios come from Phase 1C. After-arrival and asylum-support research is not part of this release.

**Status:** source-checked, **critically reviewed** ([critical-review.md](critical-review.md)) and **approved with conditions** on 11 September 2026 ([approval.json](approval.json)). In this release, 202 of 221 claims are approved for application use and 19 are withheld; the registry holds 109 sources and 221 claims. Method: [methodology.md](methodology.md). Gaps and discrepancies: [data-gaps.md](data-gaps.md).

## Bottom line

- **More people per boat.** Detected people per detected boat rose every year, from 6.95 in 2018 to 61.71 in 2025, and was 65.31 in the year to June 2026. This is well established as an average of detected arrivals; it is not the load of individual boats.
- **Load is not capacity.** Heavier loading of similar-sized boats is at least as well evidenced as bigger boats. No increase in engine power, fuel capacity or range is established.
- **Geography: conclusion C.** Officials consistently describe a wider launch area, but the distribution of departures is unmeasured and one longer loaded crossing is reported. Officials attribute the wider launch geography to enforcement displacement and taxi-boat tactics; none cites vessel capability.
- **The project's starting hypothesis** ("larger boats enable longer routes") is **not supported** (LOW). It should appear only as a labelled scenario.

## 1. How much has average occupancy changed?

Source: Home Office IER_02a, June 2026 release (`HO-TABLES-2026Q2`). Counts are OFFICIAL_STATISTIC; averages are DERIVED_STATISTIC (people ÷ boats).

| Period | People | Boats | People per boat | Home Office published |
| --- | ---: | ---: | ---: | ---: |
| 2018 | 299 | 43 | 6.95 | 7 |
| 2019 | 1,843 | 164 | 11.24 | 11 |
| 2020 | 8,466 | 641 | 13.21 | 13 |
| 2021 | 28,526 | 1,034 | 27.59 | 28 |
| 2022 | 45,774 | 1,110 | 41.24 | 41 |
| 2023 | 29,437 | 602 | 48.90 | 49 |
| 2024 | 36,816 | 695 | 52.97 | 53 |
| 2025 | 41,472 | 672 | 61.71 | 62 |
| **2026, January–June only** | **11,884** | **182** | **65.30** | not published |

Claims: `ANNUAL-*`, `OCCUPANCY-*` and `STAT-PUBOCC-*`. The 2026 row covers January–June only and is not comparable with full years: compare it with January–June 2025 (58.26). The series has method changes in 2022 Q3 and January 2025 (IER notes 2 and 9).

- **Published figures.** Each Home Office calendar-year figure equals our calculation rounded to a whole number (`STAT-OCC-PUBLISHED-MATCH`). The Home Office publishes averages only in narrative releases, never in tables.
- **2022 compared with 2025.** People fell 9.40%, boats fell 39.46%, and people per boat rose 49.65% (`COMPARISON-2022-2025`). Year-on-year changes are in `YOY-2019` to `YOY-2025`.
- **Highest months.** Counting only months with at least 10 boats, the highest averages were November 2025 (70.85; 2,338 people in 33 boats) and September 2025 (70.61). The Home Office reports both as 71, a record (`PEAK-OCCUPANCY-MONTHS`, `STAT-PUBOCC-MONTHLY-RECORD-2025`).
- **Who arrived in 2025.** The most common recorded nationalities were Eritrean (7,583), Afghan (4,801), Iranian (4,505), Sudanese (4,447) and Somali (3,806). 5,629 were aged 17 or under and 34,441 were male (`NATIONALITY-2025`, `AGE-SEX-2025`).
- **Asylum claims.** 90.2% (2021) to 98.9% (2019) of arrivals had an asylum claim recorded, by arrival year; 98.4% in 2025 (`ASYLUM-CLAIM-SHARE`).
- **Initial decisions.** Using the Home Office definition, grants ÷ (grants + refusals), grant rates for 2018–2025 arrivals ranged from 46.2% (2019) to 75.7% (2021). The whole period comes to 59.1%, with 8,081 people still awaiting a decision (`STAT-GRANTRATE-*`, `STAT-ASYLUM-OUTCOMES-2018-2025`). The denominator matters: for 2022, grants as a share of all outcomes is 42.5%. These figures count people, by arrival year, and cover initial decisions only.
- **Stability of the series.** Figures for 2018–2021 are identical in every release checked. 2022 was revised once, to 45,774 people and 1,110 boats (`STAT-VINTAGE-*`). The ICIBI's "236 in 2018" is probably a transcription error (`STAT-ICIBI-236-HYPOTHESIS`); 299 is the official figure.
- **No departure-country split.** No official UK statistic breaks arrivals down by departure country (`STAT-DEPARTURE-NOT-DISAGGREGATED`). Do not call the series "departures from France".

## 2. Have the boats become larger?

**Somewhat, at the upper end.** Confidence is MEDIUM for the direction and LOW for the size of the change (`VES-KEY-ANSWER`, a HYPOTHESIS).

- **Length.** Evidence to the Cranston Inquiry gives an average of about 7.5 m in November 2021 and "now typically 8–10 m". This is the only comparison over time, and it rests on one evidence item (`VES-CRANSTON-LENGTH`).
- **Seizures.** The NCA seized 10 m boats in 2026, estimated at about 80 people each (`VES-SEIZURES-2024-2026`). A 15 m boat is mentioned only in news reports (`VES-SNSM-230-15M`, LOW).
- **Heavier loading of similar boats is at least as well evidenced:**
  - Boats of about 8 m carried 30–33 people in 2021. Seized 8 m boats in 2025 were "typically" used for 50–60.
  - A boat "designed to carry 20" had 67 aboard in 2026 (`VES-CPS-2026-LOADS`).
  - Officials link overloading to scarce equipment and to groups choosing to load more people (`VES-BSC-OVERLOADING-SUPPLY`, `VES-NCA-NSA-LOAD`).
- **No vessel series can be built.** There is no representative year-by-year series of length, rated capacity, engine power or fuel. Show vessel evidence as dated examples labelled by how representative they are, never as a trend line or a growing boat. Details: [crossings/vessel-findings.md](crossings/vessel-findings.md) and [crossings/vessel-evidence.csv](crossings/vessel-evidence.csv) (99 observations).

## 3. Has operational range increased?

**Not established.** No source gives a horsepower figure, fuel volume or endurance for any year.

- **Engines.** Officials describe them as small and "under-powered" (`VES-UNDERPOWERED`).
- **Speed.** MAIB calculated about 3 knots for an overloaded boat in 2022 (`VES-MAIB-2022-SPEED`). Heavier loads on the same engines reduce speed.
- **Longer passages occur as single documented events in 2026.**
  - Veules-les-Roses: 173 people rescued (`VES-PREMAR-2026-08-VEULES`).
  - Baie de Seine: about 140 people (`VES-PREMAR-2026-09-SEINE`). News reports say this boat went from Utah Beach to Portsmouth, 156.6 km in a straight line.
- **Southern launch or rescue locations were also recorded in 2021 and 2024,** before larger boats were reported. No distance travelled is known for those cases.

## 4. Is crossing geography changing?

**Conclusion C: isolated longer crossings exist, but no trend is established** (`GEO-PART4-CONCLUSION`, MEDIUM). Details: [geography/geographic-findings.md](geography/geographic-findings.md).

- **What officials describe.** Launch areas spread south of the Dunkirk–Calais core (`GEO-FR-2021-DEPARTURE-GEOGRAPHY`, `GEO-FR-2024-SOUTHWARD`). Belgian coastal departures appeared in early 2026 (`BELGIUM-2026`, `GEO-BE-2026-COUNTS`).
- **Belgian figures are different measures.** Belgian officials quoted by VRT gave 15 departures by 25 March and 33 interventions in 2026. The Commons Library gives 32 launch attempts in January–April. Belgian police describe the launches as taxi legs to French waters, with none after 1 May 2026.
- **Why not B (gradual expansion).** No source publishes departures by département or coastal sector for any year, and the brief requires such a distribution to establish a trend.
- **Evidence against expansion:**
  - Seine-Maritime departures already appear in 2021.
  - Southern launches often run north to pick up passengers, so the launch area spreads more than the loaded crossing does.
  - The Normandy crossing is a single case.
- **Straight-line distances.** Across 17 documented start-and-end pairs, only 4 include the cross-Channel leg: 35.4 km (Cap Blanc-Nez to the Dover approach) up to 156.6 km (Utah Beach to Portsmouth, both ends from news reports). Coastal taxi legs reach 116.5 km (Yport to Berck) (`GEO-ROUTE-DISTANCES`). These are straight lines between documented endpoints, never tracks.
- **The event file is biased toward the periphery.** [crossings/crossing-events.geojson](crossings/crossing-events.geojson) has 35 events, found partly by searching peripheral place names. It must not be used to count or trend.
- **French 2025 figures use different definitions.** The French 2025 review gives 49,966 people aboard 795 boats attempting the crossing, 6,177 rescued, 63 people per boat and 45% taxi boats (`GEO-FR-2025-ATTEMPTS`, `GEO-FR-2025-TAXI-OCCUPANCY`). These do not match the UK arrival counts. The review has no geographic breakdown and no open licence, so link and paraphrase only.

## 5. What are the strongest alternative explanations?

No UK or French official source attributes changes to a single cause (`EXP-BSC-NO-ATTRIBUTION`). The explanation matrix has 16 hypotheses: [geography/explanation-matrix.csv](geography/explanation-matrix.csv). Details: [geography/explanations-findings.md](geography/explanations-findings.md).

| Explanation | Support | Scope |
| --- | --- | --- |
| Weather and sea conditions | HIGH | Daily and seasonal timing only: 84% of arrivals fall on 35% of days (`EXP-COND-REDDAY-SHARE`). It does not explain yearly levels, and the red-day index includes behavioural inputs |
| Shift from lorries and ports to boats, 2018–2020 | MEDIUM | Consistent across sources, but the ICIBI called the Home Office's own account "inconclusive" |
| Enforcement displacement and smuggler adaptation | MEDIUM | The consensus of official narratives for wider launch geography, taxi boats and the Belgian launches; untested by independent data |
| Overloading under supply constraints, client profile and tactics | MEDIUM | Given at least as much weight as larger boats |
| Nationality and demand shifts | MEDIUM | For example, the 2023 fall in Albanian arrivals |
| UK deterrence policy, French prevention, the 2025–26 French at-sea doctrine, tides, fuel, a rescue "pull factor" | LOW | Little or no evidence; the only causal rescue study (Mediterranean) contradicts a pull factor |

Prevented-share figures (`EXP-PREVENTED-SHARE`, LOW) mix definitions and count repeat attempts, so they cannot show whether enforcement worked. No peer-reviewed study quantifies displacement, launch-method risk or route length in the Channel.

## What must not appear in the visualization

- Occupancy presented as rated capacity or seaworthiness.
- A trend line or animation of boat size, engine power, fuel or range.
- Straight-line pairs drawn or described as navigated tracks.
- Counts or trends taken from the event sample.
- The series labelled "departures from France".
- Causal attribution of any year-to-year change. Competing explanations can appear side by side.
- The red-day index used as a weather control.
- Grant rates without their definition and denominator.
- 54 people per boat for YE March 2024, or 236 or 286 for 2018.
- Provisional daily 2026 data joined onto the quarterly series.
- Full-year comparisons that use January–June 2026.

## Scenarios (Phase 1C)

Scenarios are hypothetical arithmetic on stated assumptions, classified SCENARIO and stored in [`scenarios/`](scenarios/). They are not forecasts.

- **Crossings.** Against a July 2025–June 2026 baseline of 33,374 people on 511 boats (65.31 per boat): REDUCTION 256 boats × 65.31 = 16,720; CONTINUATION 33,374; EXPANSION 1,110 boats × 70.85 = 78,642. EXPANSION combines the 2022 boat count with November 2025 occupancy, which never occurred together, and exceeds every observed year.

## Phase 2 review outcome

H1 partly supported (an average of detected arrivals); H2 not supported (not established); H3 partly supported (launch extent widened, distribution unmeasured); H4 cannot be determined (not examined, a data gap). A numeric spot-check of 36 random claims found no numeric mismatches. Corrections, pipeline changes required before Phase 3, and the full list of what must not appear are in [critical-review.md](critical-review.md).

## Discrepancies found (for Phase 2)

- **Home Office YE March 2024 figure.** One release says 54 for YE March 2024; the correct value is 50 (54 is YE March 2025) (`STAT-OCC-YEMAR2024-MISMATCH`).
- **ICIBI 2018 figures.** The report gives both 236 and 286 against the official 299 (`STAT-ICIBI-2018-FIGURES`).
- **French annual reviews.** Editions disagree for 2019, 2022 and 2023 (`GEO-FR-SERIES-REVISIONS`). The 2025 review uses 795 for both boats and operations.
- **French inquiry.** Its 2025 maritime attempts figure appears as both 63,899 and 22,427.
- **Oxford returns share.** The Migration Observatory's "around 1%" of arrivals returned under the pilot recalculates to 1.44% (`EXP-OXFORD-RETURNS-SHARE`).
- **Prevention shares** differ across sources and time bases.
- **`BSC-2026` publication date.** 16 July or 6 August 2026 for the accessible version.
- **One CPS release** gives both 82 and 84 people aboard.

## Next

1. Complete the "Required before Phase 3" corrections (conditions of approval).

The open gaps are listed in [data-gaps.md](data-gaps.md).
