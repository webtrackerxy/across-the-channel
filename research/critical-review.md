# Phase 2 critical review

As of 11 September 2026. This is the Phase 2 critical review required by the research brief. It covers hypotheses H1–H4 (H5, about asylum support, is outside this crossings release), and cross-cutting checks on causation, selection bias, misleading statistics, map symbols and framing. It also includes a numeric spot-check and answers to the research brief's final questions.

**Status:** reviewed and **approved with conditions** on 11 September 2026; see [Decision](#decision) and [approval.json](approval.json).

## How the review was done

- **Independent reviewers.** Six reviewers worked in parallel on branch `research/phase1c-integration`, without access to the authors' reasoning:
  - H1
  - H2
  - H3 and H4
  - H5 (asylum support; not part of this release)
  - cross-cutting framing and bias
  - numeric spot-check
- **Limits.** They could only read files. Anything they cited from outside the registry had to come with a URL, an exact quote and a note that it was a new lead.
- **Verification.** The lead researcher then checked every finding used here against the pinned files or the retrieved page. One finding relevant to this release was corrected in the process:
  - One quote's page reference: CBP-9681 page 17, not page 9.
- **Reproducibility.** Changes to data-producing scripts are marked below as applied, or as required before Phase 3.

## Verdicts

| Hypothesis | Verdict | Confidence |
| --- | --- | --- |
| H1: boats carry substantially more people | **Partly supported.** Detected people per detected boat rose every year, from 6.95 (2018) to 61.71 (2025). This is an average, not the load of individual boats | HIGH for the average; MEDIUM for "boats carry more"; LOW for individual boats |
| H2: larger capacity means greater range | **Not supported (not established).** The available qualitative evidence runs against it | MEDIUM that there is no support; LOW that it is physically disproved |
| H3: crossing geography is becoming more dispersed | **Partly supported.** The launch area has widened (officials, qualitative); the distribution of departures is unmeasured | MEDIUM |
| H4: longer routes could change UK maritime-response requirements | **Cannot be determined.** Not examined in Phase 1; this is a data gap | LOW |

## H1. Small boats are carrying substantially more people than in earlier years

**Verdict: partly supported.** Detected people per detected boat rose in every calendar year, from 6.95 (2018) to 61.71 (2025). This is an average over detected arrivals, not the load of individual boats or a measure of boat size.

- **Supporting.** `ANNUAL-2018`–`ANNUAL-2025`, `OCCUPANCY-*`, and the Home Office's published averages (`STAT-OCC-PUBLISHED-MATCH`, `published-occupancy.csv`) agree. The rise holds within seasons: January–June averages rise from 13.77 (2020) to 58.26 (2025). It holds against recent years too: +50% on 2022 (`COMPARISON-2022-2025`). Revisions are negligible (`STAT-VINTAGE-2018-2021-STABLE`, `STAT-VINTAGE-2022-REVISION`). A French series, counted separately, rises the same way (`GEO-FR-2025-TAXI-OCCUPANCY`).
- **Contradicting or limiting.**
  - Counts are of people and boats "detected arriving to, or heading for, the UK" (IER notes 10–11, verified).
  - There are two method changes. 2022 Q3 figures come from casework systems (IER note 9). From January 2025, "enhanced data processing and matching methods" were used (IER note 2).
  - The Home Office counts boats differently from events: its boat figures "will be higher than the Ministry of Defence's figures where boats arriving together would be counted as one" (daily series `small-boats-2026-09-04.ods`, note 1, verified).
  - The 2018 base is 43 boats, 32 of them in November–December.
- **Missing.** No boat-level distribution of people aboard exists, apart from the Home Office bands in `EXP-COND-BOAT-BANDS`. There is no series by vessel type, and no published effect of the January 2025 change.
- **Alternatives.** Changes in the mix of vessel types; taxi-boat pickups and deliberately larger groups per launch (`VES-NCA-NSA-LOAD`); detection effects. Counting changes could affect single-year moves, especially 2024→2025, but cannot produce a steady ninefold rise that French data also show.
- **Confidence.** HIGH that detected people per detected boat rose substantially. MEDIUM for "boats carry more people". LOW for any statement about typical or individual boats.

## H2. Larger passenger capacity means vessels have greater range

**Verdict: not supported. More precisely, not established, and the available qualitative evidence runs against it.** No source links size or load to range.

- **Supporting (weak).** Two 2026 Normandy passages with heavily loaded boats: about 173 people (`VES-PREMAR-2026-08-VEULES`) and about 140 people over about 24 hours from Utah Beach to Portsmouth (`VES-UTAH-PORTSMOUTH-2026`). These are single, escorted events, with no fuel or engine data.
- **Contradicting.**
  - Speed falls with load (Cranston para 3.26; `VES-MAIB-2022-SPEED` about 3 kn; `VES-UNDERPOWERED`).
  - Border officials, reported by the Commons Library: "gangs are now using poorer quality boats, engines and fuel, which result in slower and more dangerous journeys with greater chances of failure" (CBP-9681 p.17, verified; attributed).
  - A journalist's evidence to the Assemblée nationale: "quelques milliers d'euros d'essence en plus, quelques passagers en moins" (AN-2998 fn 422, verified; attributed). Range is framed as a logistics trade-off, not a property of larger boats.
  - Wider launch geography is attributed to enforcement displacement and taxi boats (`EXP-BSC-DISPLACEMENT-SOUTH`, `EXP-CBP-TAXI-MECHANISM`).
- **Missing.** Engine power, fuel volume, consumption or endurance for any year. Whether twin engines are new: AN-2998 says boats are "équipées d'un ou deux moteurs hors-bord de faible puissance" (verified). A representative length distribution.
- **Confidence.** MEDIUM that no evidence supports H2. LOW that it is physically disproved: the counter-case is qualitative and attributed, and the claim that "load reduces range" is reasoning, not a sourced result.

## H3. Crossing geography is becoming more dispersed

**Verdict: partly supported.** Official sources agree that the launch area has widened since 2021. No source measures whether the share of departures outside the Dunkirk–Calais core has changed.

- **Supporting.**
  - 2021: departures "mainly between Dunkirk and Calais", with "rare" events towards Dieppe (`GEO-FR-2021-DEPARTURE-GEOGRAPHY`).
  - 2024: departure zones extended "as far as Dieppe" (`GEO-FR-2024-SOUTHWARD`).
  - 2025–26: launches "further south in France and a small number further north in Belgium" (`GEO-BSC-DISPLACEMENT`).
  - The gendarmerie told the Assemblée nationale that migrants and smugglers "se sont reportés toujours plus au sud pour embarquer" (moved ever further south to embark) (AN-2998, footnote 324, verified; not yet a claim).
  - The 6 September 2026 CROSS Jobourg case was "inhabituel pour la zone" (unusual for the zone) (`GEO-NORMANDY-2026-PREMAR`).
- **Contradicting or limiting.** Activity is still concentrated in the CROSS Gris-Nez zone (`GEO-FR-GRISNEZ-2024`). Southern launches often run north to pick up passengers first (`GEO-TAXI-YPORT-BERCK-2026`, `GEO-TAXI-DIEPPE-STELLA-2025`). Belgian launches paused after 1 May 2026 (`GEO-BE-2026-PAUSE`).
- **Missing.** Any representative distribution of launch sites by year (`route-analysis.json`: `representative_distribution_available: false`). The event file is a selected sample, deliberately searched by peripheral place names.
- **Alternatives.** Prefecture notices are issued selectively. Taxi-boat tactics widen the launch point, not the loaded crossing. Enforcement displacement explains the change but does not measure it.
- **Confidence: MEDIUM.**
- **Change to the Part 4 conclusion.** Keep C, but split it:
  - The launch extent has widened; officials say so consistently, though only qualitatively.
  - The distribution trend is unmeasured.
  - Say "one longer loaded crossing is reported" (Utah Beach–Portsmouth, endpoints from news), not "isolated longer crossings". The other long legs are coastal taxi legs.

## H4. Longer routes could materially change UK maritime-response requirements

**Verdict: cannot be determined; not examined in Phase 1.** This is a data gap, not a rejected hypothesis.

- **Relevant evidence (verified).**
  - Cranston Inquiry executive summary (5 February 2026): "HM Coastguard and Border Force were reluctant to deploy more than one, as this would have reduced the availability of an already insufficient number of assets on the following day."
  - Cranston Recommendation 3: "There should be regular assessments by HM Coastguard of the adequacy of the available assets and human resources to respond to both current and reasonably foreseeable levels of small boat activity."
  - Border Security Command annual report 2025–26: "BSC Maritime is the main organisation tasked by Maritime and Coastguard Agency (MCA) to interdict and rescue migrants crossing the Channel (over 90% in FY25/26)".
  - The 6 September 2026 Normandy case drew on French assets under CROSS Jobourg, a different set from the Dover Strait ones (`raw/premar-2026-09-06-baie-de-seine-140.html`).
- **Missing.**
  - HM Coastguard incident, tasking and response-time data by sector.
  - Any assessment made under Cranston Recommendation 3.
  - The government's response to Cranston (an interim response is a lead, not read).
  - A CROSS Jobourg migrant-incident series.
- **Alternatives.** Demand for response depends on the number of boats, occupancy and simultaneous launches, not only on distance.
- **Confidence: LOW.** The mechanism is plausible, and capacity is sensitive to how much activity there is, but nothing measures the effect of distance.

## Cross-cutting findings

Severity: HIGH means it would mislead a reader of the visualization.

### Causation

- **HIGH.** The closing question, "What happens if capacity and geographic reach continue to increase?" (`src/story/scenes.ts`, `docs/story.md`, implementation plan scene 14), takes H2 and H3 as given. Reword it: "What if boat numbers, occupancy or launch areas changed?"
- **MEDIUM.** `geography/explanations-findings.md` states weather and displacement as causes in the researchers' own voice. Rewrite as attributions.
- **MEDIUM.** Explanation-matrix rows `EXP-H05` and `EXP-H10` list pattern-matching and reasoning as evidence. Relabel as context or inference.
- **MEDIUM.** The executive summary reads the prevented share against the 2023 funding deal, which implies no enforcement effect. Drop that comparison.

### Selection bias

- **HIGH.** The 35 crossing events (34 of them REPORTED LOCATION) were partly found by searching peripheral place names. Show them only as labelled selected examples, never as counts, density or a timeline.
- **MEDIUM.** Vessel evidence comes from seizures, prosecutions and "record" news items. The consensus among official narratives on displacement is untested.
- **MEDIUM.** `EXP-BF-MECHANISMS` (advocacy analysis, unverified) is used against H2. Downgrade it.

### Misleading statistics

- **MEDIUM.** January–June 2026 is placed next to full years.
- **MEDIUM.** The 2022–2025 comparison uses the peak boat year as its base. Always show the full series next to it.
- **MEDIUM.** EXPANSION applies one month's occupancy (33 boats) to a whole year.
- **MEDIUM.** Scenario outputs carry false precision.

### Symbology and framing

- **HIGH.** The prototype draws straight lines lifted into 11 km arcs. Its "wider" arcs have no documented pairs behind them.
- **MEDIUM.** Area-level events drawn as pins. Colour-only scenario distinctions.

### Frozen prototype conflicts (for Phase 5)

| Locator | Problem |
| --- | --- |
| `src/story/scenes.ts` scene `scenarios` | The closing question assumes rising capacity and reach |
| `src/scenarios/model.ts` `expansion` | 800 × 80 with `footprint: 'wider'`: couples geography to occupancy, and 80 exceeds any observed month (70.85) |
| `src/map/scenarioLayer.ts` | Invented "wider" arcs with no documented pairs |
| `src/data/crossings.json` 2026 | Provisional daily data to 3 September (16,513 people, 244 boats) in the annual bars |
| `src/scenarios/model.ts` `low`, `continuation` | Not the research presets: should be REDUCTION 256 × 65.31 and CONTINUATION 511 × 65.31 |
| `src/components/ScenarioControls.tsx` | Occupancy slider to 150 with no observed-range marker; "Explore wider geographic connections" |
| `src/App.tsx` | "Whether larger vessels enable longer routes remains an open research question": the research rates H2 not supported |

## Numeric spot-check

A separate reviewer drew a stratified random sample of 36 claims (`random.seed(20260911)`: 12 OFFICIAL_STATISTIC, 8 DERIVED_STATISTIC, 6 DOCUMENTED_EVENT, 5 REPORTED_EVENT and 5 ASY-/SCN- claims). Each figure was checked against the pinned source at its locator, and every derived claim was recalculated.

- **Result:** 32 matched, 1 partly matched and 3 could not be checked. There were no numeric mismatches.
  - That is 97% of the 33 checkable claims.
  - All eight derived calculations reproduced exactly.
  - Every figure from the spreadsheets, press releases and HTML reports reproduced.
- **The partial match:** `EXP-FR-DOCTRINE-PRACTICE` said the Boulogne and Dunkirk prosecutors confirmed the testimony. The report says the prosecutors concerned confirmed it, and quotes only Dunkirk. Corrected.
- **Not checkable:**
  - `STAT-PUBOCC-2021`: the 2021 narrative is not pinned, but the value is consistent with IER_02a.
  - `VES-SNSM-230-15M`: the source is not pinned.
  - `PATH-RINGFENCED-HOTELS-2024` (an after-arrival claim, not in this release): PDF text only, and no PDF text tool is available.
- **Registry gaps:** five sources had pinned files but no `local_path` (`HO-2026Q2`, `HO-CONDITIONS-2025`, `NCA-VESSELS-2021`, `BSC-2026`, `OXFORD-2026`). Fixed. Several cited sources are still not pinned: the 2021, 2022 and 2024 Home Office narratives, `HO-ASYLUM-SB-2026Q1` and the FranceInfo article.
- **Method note:** the IER detailed dataset mixes "Main Applicant" and "Main applicant". Any extraction must compare labels case-insensitively.

## Corrections applied in this review

These changes are in `claims.json`, `sources.json`, `raw/manifest.json`, `scenarios/` and the research documents.

| Item | Change |
| --- | --- |
| `OCCUPANCY-*`, `YOY-*`, `COMPARISON-2022-2025` | Limitations now say counts are "detected arriving to, or heading for, the UK" and give the 2022 Q3 and January 2025 series breaks |
| `OCCUPANCY-2026` | Partial-year caveat; compare only with January–June 2025 or the year ending June 2026 |
| `YOY-2019` | Small-base caveat (43 boats) |
| `VES-KEY-ANSWER` | MEDIUM → LOW. The 15 m remark removed as trend evidence; notes that 10 m boats were already reported in 2021 |
| `GEO-PART4-CONCLUSION` | "Isolated longer crossings" → "one longer loaded crossing is reported". The widening of the launch area is separated from the unmeasured distribution |
| `WEATHER` | OFFICIAL_STATISTIC HIGH → HYPOTHESIS MEDIUM |
| `EXP-CBP-2023-ALBANIA` | OFFICIAL_STATISTIC → HYPOTHESIS (attribution) |
| `EXP-PREVENTED-SERIES` | OFFICIAL_STATISTIC → REPORTED_EVENT |
| `EXP-PREVENTED-SHARE`, `EXP-BF-MECHANISMS`, `VES-UTAH-DISTANCE` | → LOW |
| `VES-CPS-2026-LOADS` | REPORTED_EVENT → DOCUMENTED_EVENT; prosecution assertions flagged |
| `EXP-FR-DOCTRINE-PRACTICE` | Overstatement corrected |
| New claims | `REV-CBP9681-POORER-BOATS`, `REV-AN-FUEL-PASSENGERS`, `REV-AN-DGGN-SOUTHWARD` (attributed, HYPOTHESIS); `REV-CRANSTON-ASSET-SHORTFALL-2021`, `REV-CRANSTON-REC3`, `REV-BSC-MARITIME-TASKING` (DOCUMENTED_EVENT) |
| Sources | Cranston executive summary pinned (`REV-SRC-CRANSTON-EXEC-2026`); five missing `local_path` values filled |
| Scenarios | Presentation rules: rounding, hatching or a dashed outline, and text labels |
| Documents | Executive summary, data gaps, methodology, README and plan status |

## Required before Phase 3

| Area | Change |
| --- | --- |
| Crossing events and geocoding | Recode `EVENT-POINTE-AUX-OIES-2025-03-02` as named_area, at least 5 km (geocoded to a holiday cottage). Treat communes and "off X" locations as named_area, at least 5 km |
| Documented routes | Retype `ROUTE-2025-09-28-DIEPPE-TO-STELLA` as detection→pickup; the launch point is unknown |
| `vessel-evidence.csv` | Rename `passenger_capacity` to `estimated_load` (E011, E058, E071, E078, E082, E098, E099) |
| Utah Beach–Portsmouth | Reconcile 153 km (`VES-UTAH-DISTANCE`) with 156.6 km (route-analysis.json) to one endpoint pair |
| Scenarios (Phase 7) | Round displayed values. Mark scenario displays with hatching or a dashed outline plus text |

## Part 20 answers

1. **How much has average occupancy changed?** Detected people per detected boat rose every year, from 6.95 (2018) to 61.71 (2025); it was 65.31 in the year to June 2026. It is an average, not boat load or capacity. Method changes in 2022 Q3 and January 2025.
2. **Have the vessels themselves become larger?** Weak evidence only. Load per boat rose (official statistics). A rise in typical length rests on one inquiry item (LOW). The largest boats were about 10 m in 2021 and still about 10 m in 2026.
3. **Has operational range increased?** Not established. No engine, fuel or endurance data exist. The qualitative evidence runs against it: slower, poorer boats, and a fuel-versus-passengers trade-off.
4. **Is crossing geography changing?** Officials consistently describe a wider launch area (MEDIUM). The distribution of departures is unmeasured. One longer loaded crossing is reported.
5. **Strongest alternative explanations?** Enforcement displacement, taxi-boat tactics, supply constraints, weather windows, and counting or detection changes. None is officially attributed as the single cause.

Questions 6–12 concern asylum support and linkage and are outside this release.

13. **Important gaps:**
    - Boat-level load distribution.
    - Vessel dimensions and propulsion over time.
    - A representative launch-site distribution.
    - Maritime-response data by sector (H4).
14. **Scenarios that can legitimately be modelled:** arithmetic crossing scenarios (boats × occupancy) with stated assumptions. Nothing that predicts policy or models range or routes.
15. **Claims that must not appear.** See the list below.

## Must not appear in the final visualization (Part 20, question 15)

These add to the lists in [executive-summary.md](executive-summary.md).

**Crossings and vessels**

1. "Boats are bigger", "capacity has increased", "bigger boats travel further", "longer-range boats", "more powerful engines", or a growing-boat graphic.
2. "Each or a typical boat carries 62 or 65 people". Averages must say "detected people ÷ detected boats".
3. "Ninefold since 2018" without the small-base caveat. January–June 2026 or provisional daily 2026 data next to full years.
4. "Record 71 per boat" without "one month, 33 boats".

**Crossing geography**

5. "Route", "track", "path" or "journey distance" for straight lines.
6. Animated, curved or flowing lines, including the prototype's "wider" arcs.
7. Arrows from Belgium, Normandy or the Somme to England.
8. Pins for area-level events.
9. Heatmaps, counts or timelines from the event sample.
10. "Longer crossings are increasing" or "longer routes strain UK rescue". H3's distribution is unmeasured and H4 is unevaluated.

**Unsupported or attributed figures**

11. The 27-hour Utah figure.
12. "Up to 33,000 attempts stopped".
13. "Over 80%" taxi-boat success; "more than 60%" Chinese-branded engines; "4 in 5".
14. The prevented share as evidence of enforcement effect, and the Albanian attribution as fact.
15. `EXP-BF-MECHANISMS` without qualification.

**Scenarios and framing**

16. Scenario maps without hatching and a text label.
17. The closing question in its current form.

## Decision

**Approved with conditions, 11 September 2026**, by the project owner ("I approved", confirmed with "ok" and "allow it"). The record is [approval.json](approval.json).

- **Approved for application use:** 323 of 344 claims in the full research; 202 of 221 in this crossings release. That is HIGH- and MEDIUM-confidence claims, plus SCENARIO claims for labelled scenario use only.
- **Withheld:** 21 claims in the full research (19 in this release), listed with reasons in `approval.json`:
  - LOW-confidence observed claims, which are leads needing corroboration;
  - claims containing figures that must not appear: `EXP-BSC-SEIZURES-2025`, `EXP-CBP-TAXI-MECHANISM`, `VES-CHINA-ENGINES-2025` and `PATH-HOTEL-COUNTS-2026` (an after-arrival claim, not in this release).
- **Conditions:** the "Required before Phase 3" corrections must be completed before Phase 3 uses the affected outputs.
- **Display rules:** the "Must not appear" list still applies to approved claims, and only approved claims may be displayed.
- **Map layers:** research GeoJSON layers stay unapproved; application data is built and approved in Phase 3.
