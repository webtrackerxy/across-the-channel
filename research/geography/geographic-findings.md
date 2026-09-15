# Geographic findings: crossing geography and route distances (Parts 3–4)

Status: Phase 1A research, 11 September 2026. Source-checked by the researcher, then reviewed in Phase 2 ([critical-review.md](../critical-review.md)) and approved with conditions on 11 September 2026 ([approval.json](../approval.json)); approval is per claim. Claims use the `GEO-*` IDs in [claims.json](../claims.json); sources are in [sources.json](../sources.json); events are in [crossing-events.geojson](../crossings/crossing-events.geojson); documented pairs are in [documented-routes.geojson](documented-routes.geojson), with calculations in [route-analysis.json](route-analysis.json).

## Bottom line

**Part 4 conclusion: C.** Isolated longer crossings exist, but no trend is established (`GEO-PART4-CONCLUSION`, HYPOTHESIS, MEDIUM).

- **Qualitative expansion.** French and UK officials describe launch areas extending south of the Dunkirk–Calais core, and briefly into Belgium in early 2026. Documented events now reach the Somme, Seine-Maritime and, once, western Normandy.
- **Why this is not B.** No source retrieved publishes a representative annual distribution of departures by département or sector, so gradual expansion (B) cannot be established under the brief's own test.
- **Why A is only partly supported.** The bulk of documented migrant activity is in the CROSS Gris-Nez zone. That zone runs from the Belgian border into Seine-Maritime, so "concentrated around the Dover Strait" can be supported only at that coarse scale.

## 1. French 2025 operational review (FR-REVIEW-2025)

- **Title:** *Bilan annuel des opérations de la Préfecture maritime de la Manche et de la mer du Nord 2025*.
- **Published:** 30 January 2026, the date of the linking communiqué (`FR-REVIEW-2025-PAGE`); the PDF was created the same day.
- **Format:** 7 pages exported from PowerPoint, with no text layer. I read it by rendering each page to an image.
- **Licence:** no open licence. The Premar legal notice requires express written authorisation for reproduction (`FR-PREMAR-LEGAL`), so these sources are for linking and paraphrase only.

What it contains:

- **p.2 key figures.** 7,730 people saved in 2,753 CROSS-coordinated operations. Of these, **6,177 were migrants, in 795 operations**.
- **p.3 map.** Shows the CROSS Gris-Nez/Jobourg boundary (in Seine-Maritime), départements, ports, traffic separation schemes and marine protected areas. It has **no migration geography**.
- **p.4 migration paragraph:**
  - **49,966 people aboard 795 boats attempted** to cross from France to the UK (`GEO-FR-2025-ATTEMPTS`).
  - **6,177 were rescued; 25 died and 2 are missing** (`GEO-FR-2025-RESCUES`).
  - People per boat were 26 (2021), 45 (2023) and 63 (2025). Ten boats carried more than 100 people. **45% of boats were taxi boats**: 8–10 m inflatables launched away from gathering areas that run along the coast to collect passengers near the shore (`GEO-FR-2025-TAXI-OCCUPANCY`).
- **p.4 flow diagram.** A departure is detected and reported to CROSS Gris-Nez. If the boat is in distress or asks for help, a French asset rescues the occupants and they are taken in charge on the quay (préfecture de département). If not, the boat is monitored until it passes into the British responsibility zone, where the Maritime and Coastguard Agency and Home Office take over.
- **No breakdown by département, beach or coastal sector.**

**Definitions are not interchangeable:**

| Term | Meaning |
| --- | --- |
| Attempts / people aboard | People on boats that set out; the counting rule is not published |
| Operations | Rescue operations, which are not boats (795 appears as both on different pages) |
| Rescued ("secourues") | People taken aboard French assets; mostly landed in France |
| People involved ("impliquées") | Everyone in a rescue operation, used in earlier reviews |
| UK arrivals | The Home Office measure, which is different again |

A secondary figure of "49,996" is a transcription error; the PDF reads 49,966.

## 2. Earlier French annual reviews (2019–2024)

Reviews for 2019–2025 were downloaded from the Premar index (`FR-BILANS-INDEX`). No 2018 review is listed.

- **What they give.** Façade-wide annual series: operations, people involved, people rescued and deaths (`GEO-FR-SERIES-2018-2024`).
- **What they lack.** None gives departures by département or sector.
- **2024 key figures (`GEO-FR-GRISNEZ-2024`).** 45,203 migrants were involved in operations, shown under CROSS Gris-Nez. Of the 82 deaths in the Gris-Nez sector, 72 were migration-related.
- **Vintages disagree (`GEO-FR-SERIES-REVISIONS`):**
  - 2019: 271 events and 2,758 migrants in the 2019 review, later recounted as 203 and 2,294.
  - 2022 people involved: 51,786 in earlier reviews, 51,870 in the 2024 review.
  - 2023: the 2023 and 2024 reviews give different people, deaths and rescued figures.
  - Per-boat averages for 2022–2023 differ between editions.
  - The column definitions change from edition to edition.

  Use one vintage per series.

Qualitative geographic statements:

- **2021 (`GEO-FR-2021-DEPARTURE-GEOGRAPHY`).** Departures "mainly between Dunkirk and Calais", increasingly extending south to Berck, with rare events towards Dieppe.
- **2024 (`GEO-FR-2024-SOUTHWARD`).** Departure zones extended south as far as Dieppe. The review's claim that this "mechanically" lengthens crossing durations is an official interpretation (`GEO-FR-2024-DURATION`, HYPOTHESIS).
- **Explanations (for Part 5).**
  - The shift from tunnel and ferries to boats since 2018 (`GEO-FR-2018-SHIFT-EXPLANATION`).
  - Onshore enforcement limits flows at sea, but networks adapt (`GEO-FR-2023-ENFORCEMENT-ADAPTATION`).
  - Larger, fuller boats after May 2022 (`GEO-FR-2022-LARGER-BOATS`).

Only one sector-level count was found. It is secondary: Seine-Maritime prefecture figures reported by ICI. There were 19 prevented departures (455 people) in 2025 up to 20 August, against 5 onshore interventions (111 people) and 4 failed attempts (87 people) in all of 2024 (`GEO-SEINE-MARITIME-2025`). It covers a partial year, one département and prevented departures only.

## 3. Departure-area inventory

**Roles are kept separate:**

- **launch site:** where the boat enters the water;
- **passenger pickup site:** where taxi boats board people;
- **rescue or stranding location;**
- **French disembarkation port;**
- **intended destination.**

Every location is area-level unless noted. None is a track.

| Area | Evidence | Role(s) documented | Years | Claim IDs |
| --- | --- | --- | --- | --- |
| **Dunkirk region** (Leffrinckoucke, Malo-les-Bains, Dunkerque, Petit-Fort-Philippe, Gravelines) | MAIB 2021 ("beach near Dunkirk"); Premar notices 2025 | Launch sites; pickup (Malo-les-Bains, 28 Sep 2025); rescues offshore; landings at Dunkerque port and Calais | 2021–2025 | GEO-MAIB-2021-ENDPOINTS, GEO-FR-NOTICES-CORE, GRAVELINES-2025 |
| **Calais region** (Walde lighthouse, Calais, Cap Blanc-Nez) | Premar 2025; MAIB 2022 ("Calais/Dunkirk area") | Launch (Cap Blanc-Nez); strandings on sandbanks; landings at Calais | 2022–2025 | GEO-MAIB-2022-ENDPOINTS, GEO-2025-04-18-UK-HANDOVER |
| **Boulogne region** (Wimereux, Ambleteuse, Equihen, Écault, Hardelot) | Premar 2024–2026 | Launch sites; beaching and relaunch (Écault); landings at Boulogne-sur-Mer | 2024–2026 | GEO-FR-NOTICES-CORE |
| **Southern Pas-de-Calais** (Stella-Plage, Berck-sur-Mer) | Premar 2025–2026 | Mainly **passenger pickup sites** for boats launched further south | 2025–2026 | GEO-SOMME-DEPARTURES, GEO-TAXI-DIEPPE-STELLA-2025, GEO-TAXI-YPORT-BERCK-2026 |
| **Somme** (Baie de Somme, Saint-Valery-sur-Somme, Cayeux-sur-Mer) | Premar 2024–2026 | Launch sites; stranding (Saint-Valery) | 2024–2026 | GEO-SOMME-DEPARTURES |
| **Seine-Maritime** (Berneval-le-Grand, Dieppe, Varengeville-sur-Mer, Yport) | Premar 2021, 2024–2026; ICI 2025 | At-sea detections and rescues; launch (Yport); prevented departure (Varengeville); landings at Dieppe or Boulogne | **2021**, 2024–2026 | GEO-SEINE-MARITIME-NOTICES, GEO-SEINE-MARITIME-2025 |
| **Normandy west / Cotentin** (Utah Beach, Baie de Seine) | Premar 6 Sep 2026 (boat, ~140 people, "unusual for the zone"); ICI/AFP (departure from La Brèche, Utah Beach) | One launch site (news-reported) | 2026, single case | GEO-NORMANDY-2026-PREMAR, GEO-NORMANDY-2026-ENDPOINTS |
| **Belgian coast** (De Panne, Koksijde/Oostduinkerke, Nieuwpoort, Middelkerke) | BSC 2026; VRT quoting federal and local police and the governor | Beach and Nieuwpoort-marina departures; **taxi legs to France**; boats escorted into French waters | Jan–Apr 2026; none after 1 May 2026 | BELGIUM-2026, GEO-BSC-DISPLACEMENT, GEO-BE-2026-COUNTS, GEO-BE-2026-ESCORT, GEO-BE-TAXI-TO-FRANCE, GEO-BE-2026-PAUSE |

**Corroborating the BSC's Belgian examples.** Belgian official statements, reported by VRT, corroborate the occurrence:

- 15 departures by 25 March 2026, against 0–2 a year before;
- 14 in March and 12 in April up to the 18th;
- 33 interventions in 2026, and none after 1 May.

The Belgian police describe these as launch or pickup changes, with boats sailing along the coast to France before crossing. They are not longer direct Belgium–UK crossings. The Belgian federal police web page returned HTTP 403 during maintenance, so no Belgian primary document was read.

## 4. UK interception and disembarkation inventory

| Location | Role | Evidence | Claim IDs |
| --- | --- | --- | --- |
| Dover (Port of Dover) | Disembarkation from Border Force cutters and lifeboats | MAIB 2021: Valiant disembarked 98 at Dover; MAIB 2022: survivors to Dover; FR-REVIEW-2023: 22–23 landed at Port of Dover (12 Aug 2023) | GEO-DOVER-DISEMBARK-2021, GEO-MAIB-2022-ENDPOINTS, GEO-DOVER-DISEMBARK-2023 |
| Tug Haven and Western Jet Foil (Dover) | Reception and initial processing | ICIBI 2022 (existing claim) and 2023 | DOVER-RECEPTION, GEO-WJF-MANSTON-2023 |
| Manston (Kent) | Processing centre, not a landing site | ICIBI 2023 | GEO-WJF-MANSTON-2023 |
| UK search and rescue region, Dover approaches | Handover from French surveillance to UK rescue | Premar 18 Apr 2025; FR-REVIEW-2025 p.4 flow diagram | GEO-2025-04-18-UK-HANDOVER |
| Eastney, Portsmouth (Hampshire) | Reported landfall of the Normandy boat, 6 Sep 2026 | ICI/AFP (marina d'Eastney), BBC (Eastney Landing, lifeboats from Bembridge and Yarmouth) and ITV (Eastney Marina, RNLI lifeboat station); news only, no UK official confirmation | GEO-NORMANDY-2026-ENDPOINTS |

Home Office statistics give no landing locations. The daily page shows 625 people in 8 boats on 6 September 2026 (`HO-LAST7-2026-09-10`), which cannot be attributed to a site. Reception ports are not intended destinations or interception points.

## 5. Crossing events file

[crossing-events.geojson](../crossings/crossing-events.geojson) has **35 events**:

- **Updated seed events:** the 3 original events, migrated to the new schema. GRAVELINES and MAIB-2021 are now DOCUMENTED_EVENT; BELGIUM-2026 stays REPORTED_EVENT.
- **Point geometry:** 31 events.
- **Null geometry:** 4 events, used for offshore areas without a position or where no location is stated.

Coordinates come from one of two places:

- **The source document itself.** Only the MAIB positions: exact_coordinates, OBSERVED or REPORTED.
- **OpenStreetMap Nominatim.** Every query and result is logged in [geocoding-log.json](geocoding-log.json), written by [geocode_places.py](../geocode_places.py). These points are named_place or named_area, with an uncertainty of 1.5–20 km.

Each event also carries `documented_locations` listing every role (launch, pickup, rescue, disembarkation) separately. The file is built by [build_geography.py](../build_geography.py).

**Coverage bias.** Events were found partly by searching for peripheral place names (Dieppe, Somme, Belgium, Normandy) in order to test expansion, so the file over-represents the periphery. It must not be used to count or trend.

## 6. Route distance analysis (Part 4)

[documented-routes.geojson](documented-routes.geojson) contains **17 straight-line pairs**. Both endpoints of each pair are documented within the same event, and every pair carries `geometry_meaning: "straight line between documented endpoints, not a navigated track"`. Distances are calculated by [route_analysis.py](../route_analysis.py) (haversine, R = 6371.0088 km). Bounds are the distance plus or minus the sum of both endpoint uncertainties (`GEO-ROUTE-DISTANCES`).

| Pair type | n | Range (km) | Notes |
| --- | --- | --- | --- |
| Departure → at-sea casualty position | 2 | 45.0–60.9 | MAIB 2021 and 2022; departure points are named area or region (±15–20 km) |
| Departure → UK reception area | 1 | 35.4 | Cap Blanc-Nez → Dover approach (2025) |
| Departure → UK arrival area | 1 | 152.8 (147.8–157.8) | Utah Beach → Eastney, Portsmouth (2026); both endpoints from news |
| Rescue position → UK disembarkation | 1 | 29.0 | MAIB 2022 found position → Dover |
| Launch → passenger pickup (coastal) | 4 | 2.9–116.5 | Leffrinckoucke → Malo 2.9; Baie de Somme → Berck 21.4; Dieppe → Stella-Plage 71.2; Yport → Berck 116.5 |
| Launch → stranding (coastal) | 1 | 46.7 | Baie de Somme → Hardelot |
| Departure or rescue → French landing port | 7 | 5.7–61.4 | Return legs, not crossings; Cayeux → Boulogne 61.4 |

Spread over time in the sample (not representative):

- 2021–2024 launch locations are all in Nord and northern Pas-de-Calais, apart from the Seine-Maritime rescues.
- The 2025–2026 sample spans latitude 49.4–51.1°N, from Normandy to Belgium.
- This mostly reflects how the sample was assembled and which notices were published.

UK-side locations in the sample are Dover (2021, 2022, 2023) and, in 2026, Portsmouth (reported).

**Evidence against expansion:**

- In 2021, departures were still mainly between Dunkirk and Calais.
- Seine-Maritime activity already existed in 2021, so it is not new.
- Southern launches often feed pickups further north: Dieppe → Stella-Plage and Yport → Berck. The launch area spreads more than the loaded crossing does.
- Belgian launches were taxi legs to France and stopped after 1 May 2026.
- The Normandy crossing is a single case.
- In 2024, migrant involvement was concentrated in the Gris-Nez zone.

**Conclusion:**

- **C is selected, with MEDIUM confidence.** The reasoning and limitations are recorded in `route-analysis.json` (`conclusion`).
- **What would move it to B:** an official annual series of departures by département or sector.

## 7. Gaps and unverified leads

- **No sector-level departure series.** None was found from Premar, the Nord, Pas-de-Calais, Somme or Seine-Maritime prefectures, the Ministère de l'Intérieur, or the UK (Priority 1 gap remains open). Next: Senate and Assemblée nationale reports, Cour des comptes, and préfecture du Pas-de-Calais annual summaries. Snippets mentioned Assemblée nationale written questions, which were not read.
- **No 2018 French annual review** on the Premar index. 2018 figures come only from later tables (78 events, 586 people, 77% in November–December).
- **Belgian primary sources not read.** politie.be returned 403 during maintenance. Belgian figures rest on VRT quotes of officials.
- **Normandy landfall not confirmed officially.** Eastney, Portsmouth rests on ICI/AFP and BBC News (15 September 2026 update: the BBC names Eastney Landing and lifeboats from Bembridge and Yarmouth, which is consistent with the earlier Langstone Harbour/RNLI snippet). InfoMigrants (HTTP 403) could still not be retrieved; the ITV Meridian text, supplied by the project owner on 15 September, names Eastney Marina and the RNLI Portsmouth Lifeboat Station after Southampton and Portsmouth ports declined the landing (`ITV-2026-09-09`). The Home Office daily data cannot confirm a location.
- **Unused material.** Premar notices name more sites than are encoded, for example the 9 February 2025 rescues off Gravelines and Boulogne. MAIB drift annexes were not used, and derived drift must never be shown as a track.
- **Gazetteer gaps.** Nominatim did not match "La Brèche" (Utah Beach) or "Tug Haven". The Western Jet Foil point is a proxy ("Western Docks Revival Project"). The Pointe aux Oies point is a gîte of that name.
- **MAIB report files.** They were placed in raw/ by a parallel task; merge the source IDs `MAIB-REPORT-7-2023` and `MAIB-REPORT-9-2024` with that task's records.
- **Replacement record.** `FR-REVIEW-2025` in sources.json is a full replacement for the existing record.
