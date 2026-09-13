# Why might crossing patterns and geography change? Explanation matrix findings

Phase 1A. Research date: 11 September 2026. Status: source-checked, then reviewed in Phase 2 ([critical-review.md](../critical-review.md)) and approved with conditions on 11 September 2026 ([approval.json](../approval.json)); approval is per claim.

Files in this folder:

- [explanation-matrix.csv](explanation-matrix.csv): 16 hypotheses.
- [claims.json](../claims.json): claims prefixed `EXP-`.
- [sources.json](../sources.json): new sources prefixed `EXP-SRC-`.
- [manifest-entries.json](../raw/manifest.json): raw files saved to `research/raw/`.

The matrix also cites existing registry IDs (`BSC-2026`, `OXFORD-2026`, `HO-CONDITIONS-2025`, `HO-TABLES-2026Q2`, `HO-2026Q2`, `NCA-NSA-2026`, `NCA-LAUNCH-2026`, `NCA-VESSELS-2021`) and existing claims (for example `TAXI-BOATS`, `BELGIUM-EXPLANATION`, `WEATHER`).

## Method and limits

I read primary and secondary sources in full or in the stated sections; the source notes record which sections, and nothing rests on search snippets. For causal statements, the confidence column says how well the evidence supports the hypothesis *as a contributor*. It is not a probability, and it does not rank hypotheses against each other. Officials' causal statements are recorded as attributed `HYPOTHESIS` claims.

Neighbouring workstreams hold detail I deliberately did not duplicate. Vessel dimensions, engines and seizure rows belong to the vessel workstream; mapped launch and interception events belong to the geography workstream. I cite them here only at hypothesis level.

## Summary

No source separates the causes of crossing change. Every UK and French official source that addresses attribution declines to attribute. The Border Security Commander states it is "not possible to directly attribute changes in small boat arrivals to any single government intervention" (`EXP-BSC-NO-ATTRIBUTION`). Senior French officials told the French inquiry that the early-2026 fall owes more to weather and to reduced pressure at the Franco-Italian border than to enforcement (`EXP-FR-2026-DECLINE-ATTRIBUTION`). The Commons Library notes that UK-France effectiveness reviews are not published (`EXP-UKFR-2026-DEAL`).

What the evidence supports, in declining order:

1. **Weather and sea conditions govern day-to-day and seasonal timing** (`EXP-H07`, HIGH, scoped). Red days are 35% of days but carry 84% of arrivals. A peer-reviewed daily model finds waves, sea temperature and wind predict viable days, but only its abstract could be read (`EXP-WOOD-2025`). This confidence does not extend to multi-year trends.
2. **Route substitution from lorries and ports explains the 2018-2020 emergence of the route, in part** (`EXP-H14`, MEDIUM). Detected lorry and port entries fell as boats rose (`EXP-IER01-METHODS`), and French land-route interceptions fell from 57,137 (2016) to 3,217 (2025) (`EXP-AN-LAND-SEA`). However, the Chief Inspector called the Home Office's port-security explanation "inconclusive" in 2020 (`EXP-ICIBI-INCONCLUSIVE`), and the Home Office warns that detection differs by method (`EXP-HO-METHOD-CAVEAT`).
3. **Enforcement displacement plus organised-crime adaptation explains the observed geographic change** (`EXP-H01`, `EXP-H06`, MEDIUM). The observations are launches spread along the coast, inland rivers and canals, taxi boats, and in 2026 Belgium. Every source that explains them attributes them to beach enforcement, not to vessel capability. No launch-site time series exists.
4. **Occupancy growth reflects overloading under supply constraint, client profile and tactics, at least as much as larger boats** (`EXP-H05`, `EXP-H09`, MEDIUM). Accounts from the BSC, NCA, GI-TOC, Border Forensics, the French border police and the Commons Library converge on loading density and economics (`EXP-BSC-JIT-OVERLOADING`, `EXP-GITOC-OVERLOADING`, `EXP-DNPAF-PROFILE-PRICE`, `EXP-CBP-OVERCROWDING-ATTRIBUTION`). Larger craft are reported, but no representative dimension series exists.
5. **Demand and nationality shifts drive volumes** (`EXP-H13`, MEDIUM). This is supported by official nationality data (`EXP-NATIONALITY-YEJUN2026`), the 2023 Albanian fall (`EXP-CBP-2023-ALBANIA`), and the NCA and French border police assessments.

Weakest-supported explanations:

- **UK deterrence policy** (Illegal Migration Act, Rwanda, returns pilot) (`EXP-H04`, LOW). Rwanda never operated, and the returns pilot returned about 1% of arrivals in late 2025. The government's own impact assessment and commissioned review report insufficient evidence of deterrence (`EXP-IA-DETERRENCE-EVIDENCE`, `EXP-HO-DECISION-REA`, `EXP-NAO-RWANDA-VFM`).
- **UK-funded French prevention reducing arrivals** (`EXP-H03`, LOW). Prevention volumes are documented, but the prevented share of recorded attempts has not risen: about 42-47% in 2021-2023 and 35% in 2025 (`EXP-PREVENTED-SHARE`).
- **The 2025-26 French at-sea doctrine** (`EXP-H02`, LOW; too recent).
- **Tides** (`EXP-H08`, LOW; no evidence found).
- **Propulsion and fuel** (`EXP-H11`, LOW; no longitudinal data).
- **A search-and-rescue pull factor** (`EXP-H16`, LOW for the Channel; the only causal study, on the Mediterranean, contradicts it: `EXP-SAR-MED-2023`).

## The project's own hypothesis: larger boats enable longer routes (H2)

I found **no evidence supporting it and several lines of evidence against it** (matrix row `EXP-H10`, LOW).

- **Geography is explained otherwise.** The HAC (2021 launches further from ports), the BSC (further south and into Belgium), the Commons Library (taxi boats launched further away as monitoring expanded) and the French inquiry all attribute wider launch geography to enforcement pressure (`EXP-HAC-2021-INTERCEPTION`, `EXP-BSC-DISPLACEMENT-SOUTH`, `EXP-CBP-TAXI-MECHANISM`, `EXP-AN-DISPLACEMENT-CONCLUSION`). None attributes it to larger or longer-range boats.
- **A Belgian launch need not mean a longer loaded crossing.** The Commons Library reports that Belgian launches are typically taxi boats with a few people aboard that "travel back along the coastline to collect migrants waiting in French waters" (`EXP-CBP-BELGIUM-2026`). The 32 Belgian launch attempts in January-April 2026 therefore do not show longer loaded crossings.
- **Longer crossings were seen as a deterrent.** Longer journey time, strong currents and coastal density were previously believed to deter Belgian departures (Commons Library; MMC informants in late 2024: `EXP-MMC-DEPARTURE-SPREAD`).
- **Deaths have moved closer to France.** Border Forensics' analysis of French coastguard location data places recent deaths closer to French shores, not further out (`EXP-BF-MECHANISMS`). That analysis is unverified.
- **Overloading erodes capacity rather than adding range.** GI-TOC says that "in the majority of cases" boats are simply packed with more people (`EXP-GITOC-OVERLOADING`). The BSC and the Commons Library describe overloading as smugglers making the most of scarce supplies. The French inquiry describes boats of about ten metres "with one or two low-powered outboard engines".
- **Oxford's "some journeys may have become longer" is hedged.** It is tied to launch displacement and taxi boats, not to vessel size (`EXP-OXFORD-OCCUPANCY`).
- **No dataset exists.** None of the sources holds engine-power, fuel or range data. Absence of evidence is not disproof, but the hypothesis must stay a labelled scenario, not a historical claim.

## Home Office crossing-conditions analysis (HO-CONDITIONS-2025) in depth

**What it measures.** The analysis covers daily Met Office Red-Amber-Green likelihood that *at least one* crossing is attempted in the Dover Strait (red >55%, amber 35-55%, green <35%, using the PHIA yardstick), set against provisional arrivals from May 2021 to April 2025 (tables SB_01 and SB_02). It also tabulates boats by people-per-boat band.

**How it is built** (`EXP-COND-RAG-METHOD`). The inputs are forecast wave height plus "other environmental and non-environmental factors" (precipitation, surf on beaches, wind speed and direction, open-source forecasts, recent trends), projected over 10 days. The foundation analysis dates from 2019 and is "frequently revisited". Baselines "constantly evolv[e] to reflect sustained shifts in behaviour" and were re-set in April 2023. The page states that "no singular factor will directly correlate" with red days, and that the scale "does not consider ... availability of vessels". Expected volume is not covered.

**What it can show.**

- Arrivals concentrate on red days: 84% of arrivals on 35% of days (`EXP-COND-REDDAY-SHARE`).
- Seasonality: 65% of arrivals fall in July-December.
- The year to April 2025 had far more red days (190, against 106 the year before) (`EXP-COND-REDDAY-YEARS`, `EXP-COND-JANAPR-2025`).
- Mass-arrival days became rarer: 15 days with over 800 arrivals (20% of arrivals) from May 2021 to April 2023, against 4 days (5%) from May 2023 to April 2025 (`EXP-COND-LARGE-DAYS`).
- Boats with 70+ people rose from 18 to 202 across the same two-year periods (`EXP-COND-BOAT-BANDS`).

**What it cannot separate.**

1. **The index is endogenous.** Recent crossing trends are an input, and baselines move with behaviour. A rise in red days can partly reflect more attempts, not only better weather, so it cannot serve as an exogenous weather control.
2. **It records only whether any crossing happens, not how many.** It says nothing about loads, occupancy or geography.
3. **It excludes supply and enforcement.** Vessel availability, French prevention and tactics are all outside it.
4. **Its outcome is arrivals, not attempts.** People prevented by France are excluded, so a red day with heavy French interception looks the same as a quiet one.
5. **It covers one area only.** It uses Dover Strait conditions alone, so it cannot speak to Belgian or southern launches.

My derived check shows arrivals per red day of 309, 441, 293 and 212 across the four years (`EXP-COND-ARRIVALS-PER-REDDAY`). The year to April 2023 had the fewest red days (102) but the most arrivals (45,010, the Albanian surge). The index therefore does not explain year-to-year levels. The Commons Library notes that the Migration Observatory also doubts weather explains long-term increases.

## Parliamentary, audit and French institutional sources

- **Home Affairs Committee, HC 199 (18 July 2022), read via archive** (`EXP-SRC-HAC-2022`). The committee said it is "likely" that some of the increase came from tightened security on other routes; the small-boat share of clandestine entry rose from 11% (2019) to 50% (2020) (`EXP-HAC-DISPLACEMENT`). In 2021 the interception rate fell, partly because of calmer weather and partly because gangs launched further from the ports (`EXP-HAC-2021-INTERCEPTION`). Its 2021 prevention figures are mutually inconsistent (19,000 against more than 23,000; `EXP-HAC-2021-PREVENTION-FIGURES`).
- **House of Commons Library, CBP-9681 (13 May 2026), read via archive** (`EXP-SRC-HOCL-CBP9681-2026`). This is the key synthesis. It gives:
  - the prevention series 2018-2025 (`EXP-PREVENTED-SERIES`);
  - the 2023 fall as largely an Albanian effect (`EXP-CBP-2023-ALBANIA`);
  - the taxi-boat mechanism and its estimated success rate of over 80%, which is second-hand (`EXP-CBP-TAXI-MECHANISM`);
  - Belgian launch attempts, 32 in January-April 2026 against 2 in 2025 (`EXP-CBP-BELGIUM-2026`);
  - the £662 million 2026-29 deal and unpublished effectiveness reviews (`EXP-UKFR-2026-DEAL`);
  - the Home Office-commissioned finding of "insufficient evidence" that restrictive policy affects numbers.
- **NAO, UK-Rwanda Partnership costs (February 2024)** (`EXP-NAO-RWANDA-VFM`). The Permanent Secretary could not conclude on value for money because deterrence evidence was insufficient, so a ministerial direction was issued. No NAO report evaluating small-boat enforcement was found.
- **ICIBI (November 2020)** (`EXP-ICIBI-INCONCLUSIVE`). It called the port-security displacement explanation "inconclusive": lorry drops rose by a third in 2019, and the Calais trend was confounded by the 2016 camp clearance.
- **Assemblée nationale, rapport n° 2998 (registered 1 July 2026), tome 1** (`EXP-SRC-AN-2998-2026`).
  - It concludes that the Touquet and Sandhurst agreements displaced flows to maritime and then taxi-boat routes (`EXP-AN-DISPLACEMENT-CONCLUSION`).
  - It records DGEF land and sea figures (`EXP-AN-LAND-SEA`), the nationality and price shift (`EXP-DNPAF-PROFILE-PRICE`), and officials attributing the 2026 fall to weather and international context (`EXP-FR-2026-DECLINE-ATTRIBUTION`).
  - On the doctrine, it records a non-public 2022 "taxi-boat directive" limiting interception to boats with three or fewer people aboard, and reports that migrants are now aboard intercepted boats (`EXP-FR-DOCTRINE-PRACTICE`).
  - The rapporteure recommends abandoning at-sea interception; the president dissents.
  - **Internal inconsistency:** it gives 63,899 against 22,427 maritime attempts for 2025. My arithmetic suggests the first is arrivals plus preventions (41,472 + 22,476 = 63,948) and the second is close to preventions. It also cites the search-and-rescue study as "Nature" when it is Scientific Reports.
- **French Senate and Cour des comptes.** Search surfaced a Senate report (r24-304) mentioning CROSS Gris-Nez figures, but I did not read it. No Channel-specific Cour des comptes report was found.

## Literature review

### Peer-reviewed papers read (full text unless stated)

| Paper | DOI | What it shows | Limits |
| --- | --- | --- | --- |
| Rodríguez Sánchez, Wucherpfennig, Rischke & Iacus (2023), *Scientific Reports* 13:11014 (`EXP-SRC-SCIREP-2023`) | [10.1038/s41598-023-38119-4](https://doi.org/10.1038/s41598-023-38119-4) | Central Mediterranean 2011-2020, using Bayesian structural time-series counterfactuals. State-led and NGO rescue periods show no discernible effect on crossing attempts; Libyan coastguard pushbacks did affect flows. The only causal-inference study found. | Different route. The authors note they could not model some feedback mechanisms. Transfer to the Channel is untested. |
| Mayblin, Turner, Davies, Yemane & Isakjee (2024), *Journal of Ethnic and Migration Studies* 50(16) (`EXP-SRC-JEMS-2024`) | [10.1080/1369183X.2024.2349691](https://doi.org/10.1080/1369183X.2024.2349691) | Analysis of 345 policy texts (1962-2023) on 'stop the boats' and 'order at the border' framings. Its historical section says that by 2018 lorry drops were risky and unlikely to succeed, so people and smugglers adapted to boats, and that boats intensified in COVID as freight fell and lorry prices rose (`EXP-JEMS-ROUTE-SHIFT`). | Discourse analysis. The route-shift account relies on secondary sources and is not tested. |
| Davies, Isakjee, Mayblin & Turner (2021), *Ethnic and Racial Studies* 44(13) (`EXP-SRC-ERS-2021`) | [10.1080/01419870.2021.1925320](https://doi.org/10.1080/01419870.2021.1925320) | Postcolonial analysis with Calais fieldwork (2015-2019). It says 2020 Brexit stoppages, Calais industrial action and COVID reduced lorry and train opportunities and increased boat crossings (`EXP-ERS-2020-DISRUPTION`). Its fieldwork gives four reasons people are in Calais, including family in the UK and destitution in France. | Interpretive, not a quantitative test. Only the introduction and fieldwork sections were read. |
| Mayblin, Davies, Isakjee, Turner & Yemane (2024), *The Political Quarterly* 95(2) (`EXP-SRC-PQ-2024`) | [10.1111/1467-923X.13412](https://doi.org/10.1111/1467-923X.13412) | Argues that post-Brexit policy was performative and profitable for contractors. It describes the fortification of Calais as furthering the shift to boats from 2018. | Argument-led essay. |
| Wood (2025), *International Migration Review* (Dispatch from the Field), **abstract only** (`EXP-SRC-WOOD-2025`) | [10.1177/01979183251394003](https://doi.org/10.1177/01979183251394003) | A zero-inflated negative binomial model of daily arrivals. Waves, sea temperature and wind explain whether a day is viable; on viable days, arrivals are associated with past EU irregular immigration and with new or defunct return agreements (`EXP-WOOD-2025`). | Full text blocked, so effect sizes, data and coding are unverified. Single author writing in a personal capacity. |
| Turner, Isakjee, Mayblin, Davies & Yemane (2026), *Political Geography* 130:103603, **abstract only** (`EXP-SRC-POLGEO-2026`) | [10.1016/j.polgeo.2026.103603](https://doi.org/10.1016/j.polgeo.2026.103603) | Political economy of the "border security economy". It treats as "well documented" that policing and port fortification directed people to maritime routes. | Full text blocked; corrigendum not read. Not a test of causes. |
| Dobbernack (2025), *International Political Sociology* 19(1), **abstract only** (`EXP-SRC-IPS-2025`) | [10.1093/ips/olaf003](https://doi.org/10.1093/ips/olaf003) | Analysis of crisis discourse around the Illegal Migration Act in March 2023. | Not evidence on causes of crossing change; recorded only for completeness. |

**Gap.** I found no peer-reviewed study that quantifies enforcement displacement along the Channel coast, the maritime risk of different launch methods, or route length and geography. The Channel literature I retrieved is mostly critical or qualitative; the one statistical paper could be read only in abstract. OpenAlex searches for Channel/Calais/Dover small-boat work (2018-2026) returned mainly discourse and media studies; SSRN preprints (Brooks; "Bon Débarras ?") were not peer-reviewed and were not read.

### References followed from the Oxford Migration Observatory briefing (OXFORD-2026)

The page has no bibliography. I extracted the inline links and read these:

- ICIBI 2020 inspection (`EXP-SRC-ICIBI-2020`);
- IPPR, October 2022 (`EXP-SRC-IPPR-2022`, `EXP-IPPR-STAKEHOLDERS`);
- Mixed Migration Centre, March 2025 (`EXP-SRC-MMC-2025`);
- Illegal Migration Bill impact assessment, page 13 (`EXP-SRC-HO-IMB-IA-2023`);
- UK-France dangerous journeys agreement, landing page only (`EXP-SRC-UKFR-AGREEMENT-2025`).

I also read the Oxford text itself on occupancy, taxi boats, networks, prices and policy status (`EXP-OXFORD-OCCUPANCY`, `EXP-OXFORD-NETWORKS`, `EXP-OXFORD-PRICES`, `EXP-OXFORD-POLICY-STATUS`, `EXP-OXFORD-RETURNS-SHARE`). Not read: the UNHCR oral evidence (HAC 2849), BBC articles on barrages and dams at further coastal sites and on interception, the Home Office media blog statement of 2 May 2025, the Europol report and InfoMigrants on deaths at embarkation.

### Other non-peer-reviewed research read

- **GI-TOC, February 2024** (`EXP-SRC-GITOC-2024`). Truck costs rose after Brexit and COVID, making boats cheaper. Rising loads are mostly packing, only partly bigger boats. Kurdish networks control departures.
- **Border Forensics / University of Bristol, c. March 2026** (`EXP-SRC-BORDERFORENSICS-2026`). Deaths surged from 2023 while arrivals fell and moved closer to French shores. It attributes this to overcrowding and chaotic launches driven by supply disruption, surveillance and policing, which it says altered departure geography and created taxi boats. It also argues that arrivals-based occupancy understates density on departure (`EXP-BF-DENSITY-UNDERESTIMATE`).
- **Channel Crossings project final report, October 2025** (`EXP-SRC-CCP-2025`). Covers deflection effects, visibility and detection, and whether Rwanda deterred (`EXP-CCP-DETERRENCE`).
- **Home Office-commissioned decision-making review, 2022 study** (`EXP-SRC-HO-DECISION-2022`). Found insufficient evidence that restrictive policy changes numbers; networks and protection elsewhere shape destination.

## Discrepancies to carry into critical review

- **Prevention figures conflict across sources and units.** The HAC 2021 figures conflict internally. The BSC's "around a third" (financial year) sits against my calendar-year 35-47% (`EXP-PREVENTED-SHARE`). The French inquiry has its own internal inconsistency (63,899 against 22,427).
- **Occupancy measures conflict.** Home Office people per boat is 62 (calendar 2025) and 63 (BSC, 2025/26). The French maritime prefecture, via the inquiry, gives 63 for 2025. Border Forensics argues departure density is higher.
- **The early-2026 decline has competing official attributions.** The BSC links it to enforcement and deterrence (with caveats), the Hauts-de-France prefect to weather, and the Police aux frontières to upstream pressure.

## Unverified leads (no claims made)

- **Wood (2025) full text.** Effect sizes and return-agreement coding are needed before citing magnitudes.
- **Home Affairs Committee oral evidence.** The sessions of 16 October 2025 (HC 1321) and 4 February 2026 (HC 505, Q55, source of the taxi-boat success rate over 80%) were blocked (403).
- **Other parliamentary documents.** The Joint Committee on Human Rights report on the Channel (HC 885, 2023) and Commons Library CBP-10590 (statistics) were blocked and not archived.
- **Home Office small-boat activity data (SB_02).** The weekly prevention series was not downloaded directly, and the Commons Library's Belgian figures (its footnote 56) were not traced.
- **French primary data.** This covers DGEF land and sea series, Getlink's written answer (`EXP-AN-GETLINK-REBOUND`), maritime prefecture 2019-2025 reviews (saved in `research/raw/` by another workstream, not reviewed here), and the Le Monde article of 27 November 2025 on the doctrine.
- **Tides.** No study was found; a search returned only general tide material.
- **Other reports cited second-hand.** These are the Alarm Phone (January 2025) and Humans for Rights Network (December 2025) reports, the IOM Missing Migrants data, and the Senate report r24-304.
- **Remaining official sources.** These are the NAO's December 2025 asylum-system analysis (found, not read) and the Border Security, Asylum and Immigration Act text (policy status taken from Oxford).

## Recommendations for the story

- **Do not show a causal attribution for any year-to-year change.** Where needed, present competing explanations side by side, with the officials' own "cannot attribute" statements.
- **Label the geography as enforcement displacement.** Wider launch geography (taxi boats, Belgium 2026) can appear as reported examples with that label, but not as a trend and not as evidence of longer loaded crossings.
- **Keep "larger boats enable longer routes" as a scenario only.**
- **Do not use red days as a weather control.** If the crossing-conditions chart is used, state that the red-day index includes behavioural inputs.
