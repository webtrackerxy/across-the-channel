# Vessel evolution, 2018–2026: findings (Phase 1A)

Research date: 11 September 2026. Status: first evidence pass, reviewed in Phase 2 ([critical-review.md](../critical-review.md)) and approved with conditions on 11 September 2026 ([approval.json](../approval.json)); approval is per claim.

Files in this folder:

- [vessel-evidence.csv](vessel-evidence.csv): 99 rows, one per documented observation.
- [claims.json](../claims.json): 32 `VES-*` claims.
- [sources.json](../sources.json): 26 `VES-*` source records. Existing IDs `NCA-VESSELS-2021`, `BSC-2026`, `OXFORD-2026`, `NCA-NSA-2026` and `HO-TABLES-2026Q2` are reused, not re-registered.
- [manifest-entries.json](../raw/manifest.json): 19 raw files saved to `research/raw/` in this pass.

## Key question: has carrying capacity increased, operational range increased, or both?

**Answer: the number of people carried per boat has increased. Some boats have also got larger at the upper end. There is no evidence that operational range has increased.**

| Component | Finding | Confidence |
| --- | --- | --- |
| People per arriving boat | Rose from 6.95 (2018) to 61.71 (2025); 65.30 in January–June 2026. Official statistics: existing `OCCUPANCY-*` claims, source `HO-TABLES-2026Q2` | HIGH |
| Physical size (length) | Modest increase in typical length, with larger boats at the upper end. The evidence is attributed and not representative | MEDIUM (direction); LOW (magnitude) |
| Tighter loading of similar boats | Boats in the same ~8 m class are reported carrying roughly 1.5–2 times more people than in 2021 | MEDIUM |
| Rated or safe capacity | Not measurable. The boats are uncertified. One prosecution cites a design load of 20 against 67 people aboard | Not established |
| Engine power | No horsepower figure verified for any year. Engines are consistently described as small or under-powered | Not established (gap) |
| Fuel capacity | Only container counts: 2 in 2021, at least 1 extra tank in 2022, fuel packed in "go kits" in 2026. No volumes | Not established (gap) |
| Operational range | Longer passages are documented in 2026 as single events. Long southern departures are also documented in 2021 and 2024. There is no endurance or range trend | Not established; an increase is **not supported** as a trend |

Overall confidence in this synthesis (`VES-KEY-ANSWER`, classified HYPOTHESIS) is **MEDIUM**. It is our interpretation of mixed and selected evidence.

## Supporting evidence

### Larger boats

- **Early boats (undated).** Evidence to the Cranston Inquiry says that when crossings first began to increase, the boats were 4–6 m rigid-hull inflatables such as yacht tenders. They were "overloaded to carry around 16 people", and some craft were improvised. A Border Force witness said early boats crossed with about 14–16 people, and that "as the small boats got bigger" loads exceeded what the cutters could handle. (`VES-EARLY-BOATS`; source `VES-CRANSTON-2026`, para 3.25 fn 20 and para 6.29)
- **December 2021 NCA alert.** The NCA reported "a trend towards larger inflatables, sometimes up to 10 metres in length". It described them as unbranded and purpose-made, and said other boats were adapted "to increase capacity and improve rigidity". (`VES-NCA-2021-ALERT`; source `NCA-VESSELS-2021`)
- **MAIB 2021 background.** MAIB describes inflatables "from small inflatables intended for use as tenders ... to larger boats of up to 10m". These carried "routinely 40 to 50, occasionally up to 80 or more" people. (`VES-MAIB-2021-CONTEXT`; source `MAIB-REPORT-7-2023`, s1.8)
- **2021 compared with "now".** The Cranston Inquiry received evidence that in November 2021 boats averaged 7.5 m and about 32 people, and are "now typically 8 metres to 10 metres". (`VES-CRANSTON-LENGTH`; source `VES-CRANSTON-2026`, para 3.25)
  - This is the only verified comparison of length across time.
  - It rests on one evidence item, and its method and date are not stated.
- **2026 upper end.** The NCA seized 25 ten-metre boats with 25 Parsun engines at Felixstowe on 18 July 2026, estimated at about 80 people each. (`VES-SEIZURES-2024-2026`; source `VES-NCA-2026-07-22`) Separately, the media quoted an SNSM station director as saying 15 m boats are increasingly seen. (`VES-SNSM-230-15M`, LOW; source `VES-FRANCEINFO-2026-08-10`)

### Heavier loading

- **2021–2022 observations (boats 7.4–8 m):**
  - About 33 people on the boat lost on 24 November 2021, an MAIB estimate. (`VES-MAIB-2021-BOAT`; `MAIB-REPORT-7-2023`)
  - About 30 people, from a coastguard helicopter's estimate the same night. (`VES-MAIB-2021-CONTEXT`)
  - 33 and 28 people in two French rescues on 9 March 2021. (`FR-NOTICE-2021-03-09`; source `FR-NOTICE-2021-03-09`)
  - About 47 people on the 7.4 m boat of 14 December 2022. (`VES-MAIB-2022-BOAT`; `MAIB-REPORT-9-2024`)
- **2025, same length class.** 25 boats of about 8 m seized in Bulgaria were "typically" used to carry 50–60 people. (`VES-SEIZURES-2024-2026`; source `VES-NCA-2025-07-31`)
- **2026 estimates and observations:**
  - The NCA's estimate for 25 boats seized in Bulgaria in June 2026 implies at least about 68 people per boat. This is our derivation from an NCA planning figure. (`VES-NCA-IMPLIED-LOAD-2026`; `VES-NCA-2026-07-01`)
  - CPS releases record loads of more than 70, 74, 67, 83 and 96 people. In one case the prosecution said the boat "was designed to carry 20 passengers" and 67 were aboard. (`VES-CPS-2026-LOADS`; sources `VES-CPS-2026-06-10`, `VES-CPS-2026-06-24`, `VES-CPS-2026-07-31`)
  - French notices record 173 people rescued from one boat and about 140 aboard another. (`VES-PREMAR-2026-08-VEULES`, `VES-PREMAR-2026-09-SEINE`; sources `VES-PREMAR-2026-08-04`, `FR-NOTICE-2026-09-06`)

### Official interpretations of loading (HYPOTHESIS, attributed)

- The NCA says criminal groups "increased the number of migrants per boat to enable more arrivals". (`VES-NCA-NSA-LOAD`; `NCA-NSA-2026`)
- The Border Security Commander links overloading to "making the most of available supplies". The report also says "intelligence indicated a sharp reduction in equipment flows in early 2025". (`VES-BSC-OVERLOADING-SUPPLY`; `BSC-2026`)
- The Cranston Inquiry describes decks "often reinforced with wood or metal to allow more people to be carried". (`VES-CRANSTON-DESIGN`; `VES-CRANSTON-2026`, para 3.26)

### Longer passages do occur (single events relevant to range)

- **3–4 August 2026.** A boat's departure was reported in the Veules-les-Roses sector (Seine-Maritime) on 3 August. It was still under way the next morning in the French search-and-rescue region, close to the UK region, when its engine caught fire. 173 people were rescued. (`VES-PREMAR-2026-08-VEULES`; `VES-PREMAR-2026-08-04`)
- **5–6 September 2026.** About 140 people were aboard a boat west of the Baie de Seine heading for the UK. The Préfecture maritime called such a departure unusual for the area. (`VES-PREMAR-2026-09-SEINE`; `FR-NOTICE-2026-09-06`)
  - Local media report that it left Utah Beach and arrived at Eastney, Portsmouth; the BBC reported the crossing had taken about 10 hours. An earlier "about 24 hours" was an inference from the ICI timeline and has been withdrawn. (`VES-UTAH-PORTSMOUTH-2026`; `ICI-2026-09-07`; `BBC-2026-09-07`)
  - The straight-line distance is about 153 km (82 nm), our calculation. (`VES-UTAH-DISTANCE`)

## Contradicting evidence (H2: larger boats enable longer routes)

1. **Long southern departures predate the larger boats.**
   - On 9 March 2021 an ~8 m semi-rigid boat with 33 people set out off Berneval-le-Grand (Seine-Maritime) and was brought to Dieppe. (`FR-NOTICE-2021-03-09`)
   - On 1 May 2024, 66 people were rescued off Dieppe. (`VES-PREMAR-2024-DIEPPE`; source `FR-NOTICE-2024-05-01`, URL unverified)
   - So distant departures happened with ordinary-sized, lightly loaded boats, years before 10–15 m boats were reported.
2. **A southern launch does not mean a long loaded crossing.** On 22 July 2026 a boat put to sea off Yport (Seine-Maritime) and had an engine failure. It stayed at sea overnight under French monitoring, then at dawn on 23 July beached at Berck-sur-Mer to take on more people. (`VES-PREMAR-2026-07-YPORT`; `FR-NOTICE-2026-07-22`)
   - The distance from launch to landing is not the same as a longer open-sea passage with a full load.
   - Taxi-boat pickups are described by the NCA and BSC (existing `TAXI-BOATS`, `BSC-TACTICS`).
3. **No documented upgrade in propulsion.**
   - Officials describe engines as "hugely under-powered" (NCA, March 2026) and "under-powered" (NCA, July 2026). The Cranston Inquiry describes "a small outboard motor capable only of slow speeds". (`VES-UNDERPOWERED`; sources `VES-NCA-2026-03-25`, `VES-NCA-2026-07-22`, `VES-CRANSTON-2026`)
   - The documented engine types are a Chinese copy of a Yamaha two-stroke in 2022 and Chinese-branded Parsun outboards between 2019 and 2026. (`VES-MAIB-2022-BOAT`, `VES-SAVAS-SUPPLY`, `VES-CHINA-ENGINES-2025`; sources `MAIB-REPORT-9-2024`, `VES-NCA-2026-01-07-SAVAS`, `VES-GOVUK-2026-01-28-CHINA`)
   - With the same small engine, a heavier load lowers speed, which works against range. The Cranston Inquiry (para 3.26) says speed "is likely to be reduced by overcrowding". In one case the prosecution said overloading severely restricts "speed, manoeuvrability and seaworthiness". (`VES-CPS-2026-06-24`)
4. **Speed evidence.** MAIB calculated an average of about 3 knots for an overloaded 7.4 m boat in 2022. (`VES-MAIB-2022-SPEED`)
   - At that speed the straight line from Utah Beach to Portsmouth would take about 27 hours.
   - The 2026 Normandy passage fits a slow boat with enough fuel for about a day. It does not show more speed or power, and its fuel arrangements are unknown.
5. **A competing explanation for the new geography.** The BSC report attributes launches "further south in France" and from Belgium to enforcement displacement. (Existing `BELGIUM-EXPLANATION` and `BSC-TACTICS`; source `BSC-2026`)
   - The NCA attributes the change to taxi-boat tactics.
   - French notices describe monitoring and escorting long passages, and occupants refusing assistance. Surviving a long passage may partly reflect that escorting rather than what the boat can do.
6. **Seaworthiness is still poor.**
   - 2021: the floor failed after about 4 hours. (`VES-MAIB-2021-BOAT`)
   - 2022: the floor tore after about 3.5 hours. (`VES-MAIB-2022-BOAT`)
   - 2026: an engine failure in July and an engine fire in August. (`VES-PREMAR-2026-07-YPORT`, `VES-PREMAR-2026-08-VEULES`)
   - The Cranston Inquiry and BSC describe the boats as uncertified, fragile and overloaded, and say waves over 1 m are likely to swamp them. (`VES-CRANSTON-DESIGN`, `VES-BSC-FUEL-BURNS`)
   - Nothing indicates boats built for longer open-water endurance.

## Evidence that higher occupancy reflects tighter loading of similar boats

- **Same length class, heavier loads.**
  - About 8 m and 30–33 people in 2021 (`VES-MAIB-2021-BOAT`, `VES-MAIB-2021-CONTEXT`, `FR-NOTICE-2021-03-09`). About 8 m and "typically" 50–60 people in 2025 (`VES-SEIZURES-2024-2026`).
  - In 2021, boats of up to 10 m "routinely" carried 40–50 people (`VES-MAIB-2021-CONTEXT`). The NCA's July 2026 estimate is about 80 per 10 m boat (`VES-SEIZURES-2024-2026`).
- **One case with a stated design load.** A boat "designed to carry 20 passengers" had 67 aboard in April 2026. (`VES-CPS-2026-LOADS`) This is one statement about one boat.
- **Official attributions.** The BSC attributes overloading to supply constraints (`VES-BSC-OVERLOADING-SUPPLY`). The NCA's 2026 National Strategic Assessment attributes it to deliberately increasing numbers per boat (`VES-NCA-NSA-LOAD`).
- **Arithmetic from existing claims.** Between 2022 and 2025, boats fell 39.46% while people fell 9.40% (`COMPARISON-2022-2025`). Loading, boat size or both must have changed, and the statistics cannot tell which.

**Conclusion:** both mechanisms are supported. Tighter loading of boats in the same length class is at least as well evidenced as larger boats, but the split between them cannot be quantified.

## Missing evidence

- **Dimensions.** There is no representative or year-by-year series of length, beam or tube diameter. Nothing covers 2018–2020 except the undated "early" description, and there is almost nothing for 2023–2024.
- **Engine power.** No horsepower figure appears in any verified source for any year.
- **Fuel.** There are no volumes and no data on consumption, endurance or tank specifications.
- **Rated capacity.** None exists: the Cranston Inquiry says the boats "are not built to any recognised EU or UK standard".
- **Counts by boat type.** There is no official split of arrivals or boats by type (inflatable, RHIB or other). Home Office notes say only that RHIBs, dinghies and kayaks are "most common". The Home Office detailed dataset (IER_D01–D05) has no boat-level fields.
- **Occupancy distribution.** No official per-boat occupancy distribution, such as the share of boats carrying more than 80 people, was retrieved.
- **Engine origin.** The figure of more than 60% Chinese-branded engines in 2025 has no published basis or denominator. (`VES-CHINA-ENGINES-2025`)
- **Range data.** There are no French or UK data on crossing duration, distance travelled, launch-to-landing distance or running out of fuel.
- **French annual reviews.** The 2019–2025 operational reviews contained no vessel characteristics in their text. Several are image-based and could not be machine-read.

## Alternative explanations for rising occupancy (other than size or range)

- **Supply scarcity.** Seizures and supply-chain disruption push groups to load each available boat more heavily. (`VES-BSC-OVERLOADING-SUPPLY`, HYPOTHESIS; seizure context in `VES-SEIZURES-2024-2026` and `VES-SEIZURE-COUNTS`)
- **More people per launch.** With fewer launch opportunities, groups load more people each time. Relevant factors are French beach enforcement, simultaneous launches and taxi boats. (`VES-NCA-NSA-LOAD`; existing `BSC-TACTICS`, `TAXI-BOATS`)
- **Weather windows.** Home Office analysis relates arrivals to crossing conditions (existing `WEATHER`). MAIB cites Border Force data that 96% of crossings were attempted when predicted wave height was under 0.5 m (`VES-MAIB-2021-CONTEXT`). When good windows are scarce, loads per window may rise.
- **Boarding during the journey.** Passengers are picked up in the water or from later beaches, as in the Yport–Berck case. (`VES-PREMAR-2026-07-YPORT`)
- **Counting and definitions.** Home Office counts differ for boats versus events, and data are revised between vintages (see the notes to `HO-TABLES-2026Q2`).

## Confidence summary

| Statement | Confidence |
| --- | --- |
| Official people per boat rose substantially | HIGH |
| Typical boats have become somewhat longer (about 7.5–8 m in 2021 to 8–10 m) | MEDIUM for direction, LOW for magnitude |
| Boats of the same size class carry more people (tighter loading) | MEDIUM |
| Engine power, fuel capacity or operational range increased | Not established; absence of evidence, not disproof |
| Larger boats caused longer routes (H2) | Not supported. Contradicting evidence exists, and competing explanations (enforcement displacement, taxi boats, escorting) are unresolved |

## Can a year-by-year vessel series be built?

**No.** The verified observations of dimensions, engines and fuel are:

- **2021:** several single incidents and qualitative assessments.
- **2022:** one investigated casualty.
- **2023:** one conviction (no dimensions) and an NCA estimate of one supplier's share.
- **2024:** one rescue (no dimensions), one Eurojust arrest and one seizure.
- **2025:** one seizure batch with a stated length.
- **2026:** a handful of seizures, prosecutions and rescues.

Nothing was measured for 2018–2020, and definitions differ between sources: inflated length, length overall and aerial estimates. The only defensible annual series is **people per arriving boat**, from Home Office statistics. Present vessel evidence as dated, labelled examples with their representativeness shown. Never present it as a trend line or an animated "growing boat".

## Selection biases affecting incident, seizure and court evidence

- **MAIB investigations.** MAIB only investigates very serious casualties in or near the UK search-and-rescue region, so its sample is boats that failed.
  - The 2022 boat was judged "poorly built compared to the many others that had been recovered and inspected in the preceding years". It was also "the only vessel to fail" of the similarly loaded boats that night, so it was not typical. (`MAIB-REPORT-9-2024`)
  - For 2021, MAIB had no French evidence and never examined the boat. (`MAIB-REPORT-7-2023`)
- **Seizures.**
  - Seizures are intelligence-led, publicised selectively, and reflect the routes that law enforcement targets (Bulgaria, Germany, Felixstowe).
  - The capacity figures in seizure releases are NCA estimates used to express impact.
  - Cumulative counts combine boats with engines, use different scopes, and cannot be reconciled with each other. (`VES-SEIZURE-COUNTS`)
  - Seized equipment may differ from the equipment that reaches the water.
- **French maritime notices.** These report rescues, incidents and unusual events, so routine crossings are under-represented and escorted long passages over-represented. Counts are usually people rescued ("personnes secourues"), which may differ from the number aboard.
- **Court records.** They cover only pilots charged under the endangerment offence, in force since 5 January 2026, which probably selects overcrowded or dangerous crossings. One release contradicts itself: "82 others" in the text against 84 people listed in its notes. (`VES-CPS-2026-07-31`)
- **News.** Coverage concentrates on record loads (128, 165, 230 people), and boat lengths quoted in the news are often unmeasured remarks.
- **Estimates.** Aerial and survivor estimates are imprecise, and length definitions vary.
- **Time clustering.** Evidence bunches in 2021, around the fatal incident and the inquiry, and in 2026, around the new offence and seizure publicity. This can create an apparent change that is really a change in the available sources.

## Unverified leads (no claims made)

- **Boats carrying more than 80 people.** A PA-reported Home Office analysis gave 33 such boats in the year to April 2025, up from 8 in the year to April 2022. The article URL returned 404 and the underlying analysis was not found. The same snippet said dinghies are typically made to carry up to 20 people safely.
- **9.2 m × 2.9 m dinghy with a 40 hp outboard.** Attributed to LBC (Canterbury Crown Court, 29 July). This came from a search snippet only; the LBC article I retrieved did not contain these details.
- **Parliamentary sources.** Commons Library briefing CBP-10590 and the Home Affairs Committee report HC 199 (July 2022) both returned HTTP 403, so parliamentary evidence on the boats is unread.
- **Europol releases.** The pages for "21 arrested ... nautical equipment" and Operational Task Force Dune load their text with JavaScript and could not be retrieved. The Eurojust release (`VES-EUROJUST-2024-11-14`) was retrieved.
- **Boats made to order.** Mail on Sunday reporting (2023) that Chinese and Turkish firms make boats to order. Snippet only.
- **15 m boat with 230 people, and the July 2026 record of 165.** The 15 m figure comes from Euronews and the 165 record from news reports. No official notice was found for either.
- **Peer-reviewed research.** None was found on Channel boats, engines or fuel burns. The Journal of Travel Medicine fuel-burn study concerns the Mediterranean.
- **MAIB drift-analysis annexes** (BMT, Forensic Oceanography, NASH Maritime) were not read. They are drift models, not vessel tracks.
- **Savas release.** The original NCA URL now returns 404, so a WiredGov mirror is used (`VES-NCA-2026-01-07-SAVAS`).
- **Dieppe notice.** The URL of the Préfecture maritime notice of 1 May 2024 is unresolved (`FR-NOTICE-2024-05-01`).

## Implications for the story

- Lead with occupancy from the official statistics.
- Show vessel evidence as dated examples, each labelled with how representative it is.
- Illustrate boats as uncertified 7–10 m inflatables and show the uncertainty. Label any 10–15 m depiction as an upper-end report from 2026.
- Do not depict engine power, fuel capacity or range increasing over time.
- Present the 2026 Normandy passages as documented single events. Show them alongside the 2021 and 2024 southern departures and the enforcement-displacement hypothesis.
