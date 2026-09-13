# Data gaps and open questions

As of 11 September 2026, after the Phase 1A (crossings) research pass, the crossing scenarios (Phase 1C) and the Phase 2 review. This release covers Channel crossings up to arrival in the UK; after-arrival and asylum-support gaps are not included. The research was approved with conditions ([approval.json](approval.json)); these gaps must stay visible and still limit what may be shown.

## Resolved or advanced in Phase 1A

- **French 2025 operational review:** read (`FR-REVIEW-2025`). It has no geographic breakdown and no open licence.
- **French reviews 2019–2024:** downloaded and read. They give coast-wide totals only; no 2018 review exists on the index.
- **Departure and UK arrival inventories:** a departure-area inventory and a separate UK interception and disembarkation inventory now exist. Launch, pickup, rescue, reception and destination roles are kept distinct.
- **Belgian 2026 departures:** corroborated through Belgian officials quoted by VRT. No Belgian primary document has been read.
- **2018 figure (236 vs 299):** explained as a probable ICIBI transcription error (`STAT-ICIBI-236-HYPOTHESIS`). This is pending review; 299 stays the official figure.
- **Home Office releases:** six of about 18 table vintages cross-checked. One 2022 revision was found.
- **Departure country:** confirmed that no official UK series breaks arrivals down by departure country.
- **Published averages:** Home Office people-per-boat figures recorded and reconciled with ours.
- **MAIB:** full 2021 and 2022 investigation reports reviewed.
- **Peer-reviewed literature:** 7 papers identified. 4 were read in full or in their relevant sections; 3 only in abstract.
- **Registry fix:** `HO-DAILY-2026-09-04` added to the source registry.

## Priority 1: geographic evidence

- **Sector-level departure series.** This is the key gap. No French or UK source publishes departures by département or coastal sector for any year, and without one the geography conclusion cannot move from C to B. Next sources to try:
  - Senate report r24-304
  - Assemblée nationale written questions
  - Cour des comptes
  - Nord, Pas-de-Calais, Somme and Seine-Maritime prefecture summaries
- **Belgian primary sources.** The Belgian federal police page returned HTTP 403, and the Belgian figures differ between VRT and the Commons Library.
- **Normandy landfall.** The Portsmouth landfall of 6 September 2026 rests on one news report. InfoMigrants and ITV could not be retrieved, and the Langstone Harbour detail is unverified.
- **Unused material.** Some Premar notices name sites not yet encoded. The MAIB drift annexes are unused, and drift models must never be shown as tracks.
- **Gazetteer limits.** No gazetteer match was found for La Brèche (Utah Beach) or Tug Haven, and the Western Jet Foil point is a proxy.
- **Event sample.** The event file over-represents the periphery and cannot be used for counts or trends.

## Priority 2: vessel characteristics and causal claims

- **Vessel series.** There is no representative series of length, beam, rated capacity, engine power, fuel volume, endurance or range, and nothing measured for 2018–2020.
- **Boats carrying more than 80 people.** A reported Home Office analysis was not found; the news article returned 404.
- **Chinese-branded engines.** The figure of more than 60% in 2025 has no published basis or denominator.
- **Blocked or unread sources:**
  - Europol releases (JavaScript-only pages)
  - Home Affairs Committee oral evidence from 16 October 2025 and 4 February 2026, the source of the taxi-boat success rate over 80%
  - Joint Committee on Human Rights report HC 885
  - Commons Library briefing CBP-10590 (full text blocked)
- **Wood (2025).** The full text is needed before its effect sizes can be cited.
- **No evidence found** on tides, or on propulsion and fuel over time.
- **French primary data unread:** DGEF land and sea series, Getlink's written answer, and the Le Monde article on the at-sea doctrine.
- **Evidence against the hypotheses.** Keep searching for it as well as for supporting evidence. Lack of a verified engine or fuel trend is a gap, not disproof.

## Priority 3: statistical and source reconciliation

- **Unchecked releases.** Twelve Home Office table vintages were not checked, including the one that first revised 2022.
- **Note 5 revision.** It is unclear what the January 2025–March 2026 revision changed, since IER_02a totals did not move.
- **Asylum outcomes.** No appeal or final-outcome data exist by arrival cohort, and the extraction date for pre-2023 decisions is not stated.
- **Grant rates for recent arrivals** will change as pending cases are decided; 4,508 people who arrived in 2025 were still awaiting a decision.
- **Matched-record totals** (IER_02d, IER_D02) are denominators for claim and decision shares only. Never substitute them into the annual series.
- **Provisional data.** Keep provisional operational data (for example the September 2026 time series) as a separate, dated series.
- **Licences:**
  - The daily time series states only Crown copyright, so the Open Government Licence needs confirming.
  - Préfecture maritime material requires written authorisation: link and paraphrase only.
  - NCA, Oxford, news and research-paper terms are unchecked.
  - Basemap and data reuse licences must be settled before implementation.

## Discrepancies to carry into Phase 2

Each is recorded in the claim registry:

- **YE March 2024 occupancy.** A Home Office release says 54; the correct value is 50 (`STAT-OCC-YEMAR2024-MISMATCH`).
- **ICIBI 2018 figures.** 236 and 286 against 299 (`STAT-ICIBI-2018-FIGURES`).
- **French annual reviews.** Editions disagree (`GEO-FR-SERIES-REVISIONS`), and the 2025 review uses 795 for both boats and operations.
- **French inquiry.** Its 2025 maritime attempts figure appears as both 63,899 and 22,427.
- **Oxford returns share.** "Around 1%" against our recalculated 1.44% (`EXP-OXFORD-RETURNS-SHARE`).
- **Prevention shares** differ across the Home Affairs Committee, the BSC and calendar-year calculations (`EXP-PREVENTED-SHARE`). Their inputs for 2018–2023 are not yet transcribed.
- **`BSC-2026` publication date.** 16 July or 6 August 2026.
- **One CPS release** gives both 82 and 84 people aboard.
- **Classification to review.** `STAT-DEPARTURE-NOT-DISAGGREGATED` is recorded as DOCUMENTED_EVENT, which is a nearest fit for a property of the data.
- **Confidence levels.** Those carried over from the initial pass need reassessing.

## Scenario limitations (Phase 1C)

- **Plausibility is not assessed.** Scenarios are arithmetic on stated assumptions (`scenarios/assumptions.json`); none is a forecast or has an estimated probability.
- **Research choices.** REDUCTION's halving of arriving boats is an illustrative choice, not an evidence-based value.
- **EXPANSION** combines two observed maxima that never occurred together (2022 boats, November 2025 occupancy).

## Gaps found in the Phase 2 review

- **H4 (maritime response) was not examined in Phase 1.** Needed: HM Coastguard incident, tasking and response-time data by sector; any assessment under Cranston Recommendation 3 (`REV-CRANSTON-REC3`); the government response to the Cranston Inquiry (interim response not read); a CROSS Jobourg migrant-incident series.
- **Vessel propulsion.** Whether twin engines are new (the French inquiry says boats have "un ou deux moteurs"); no engine, fuel or endurance data for any year.
- **Unpinned sources** cited by claims: the 2021, 2022 and 2024 Home Office narratives, `HO-ASYLUM-SB-2026Q1` and the FranceInfo article. PDF-only evidence could not be spot-checked because no PDF text tool is installed.

## Required before Phase 3

Pipeline corrections listed in [critical-review.md](critical-review.md): event precision recoding (Pointe aux Oies geocoded to a holiday cottage), the Dieppe–Stella pair type, `passenger_capacity` renamed to `estimated_load`, the Utah Beach–Portsmouth distance reconciled, and scenario presentation rules.

## Approval

Approved with conditions on 11 September 2026 ([approval.json](approval.json)). The "Required before Phase 3" corrections above are conditions of approval.

## Completion gate

Phase 1 can close when these conditions are met:

- All research-brief questions have a documented answer or a documented evidence gap after further searching.
- Source metadata is complete for the claims used.
- Counts are reconciled.
- Geographic coverage is explicit.
- Unsupported causal statements are excluded.

A question does not need a positive finding to close. Phase 2 critical review is a separate pass. Do not set `approved_for_application` to true until review and human approval are complete.
