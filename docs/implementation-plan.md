# Implementation plan

Accepted: 11 September 2026. Revised: 11 September 2026 for the expanded research brief. Inputs: `research.md` (original research brief) and `story.md`.

## Scope and status

12 September 2026: the user authorized [narration implementation Phase 1](narration/narration-implementation-plan.md), covering script, tests and a review transcript. The research was later approved with conditions on 11 September 2026 ([approval.json](../research/approval.json)); see Status below.

Build an evidence-based, mobile-responsive interactive 3D geospatial story about UK small-boat crossings from 2018 to 2026, up to arrival in the UK, with separately labelled future scenarios. The UK arrivals series is not disaggregated by departure country; do not describe it as exclusively departures from France.

Research must be completed, critically reviewed and approved by a human before application work resumes. Research must not assume that increasing passengers per arriving boat demonstrates increased physical capacity, seaworthiness, engine range or longer routes.

Status, 11 September 2026:

- Research: the crossings research (Phase 1A) and the crossing scenarios (Phase 1C) have a complete first pass: 109 sources, 221 claims, reproducible extraction, scenario and validation scripts, and an [executive summary](../research/executive-summary.md). The critical review is complete ([critical-review.md](../research/critical-review.md)), and the research was approved with conditions on 11 September 2026 ([approval.json](../research/approval.json)): 202 of 221 claims are approved for application use. Phase 3 may start once the "Required before Phase 3" corrections are done.
- Application: a Day 1 MVP (React, MapLibre, Three.js, tests, release docs) was built before research review, under user authorization. It is a **frozen prototype** from commit `edc0c4b`: no feature work until research approval, then it is revised to this plan (Phase 5).

## Decisions

Resolved on 11 September 2026 where the research brief conflicted with the original plan, research or MVP:

| Topic | Decision | Consequence |
| --- | --- | --- |
| Lower-arrivals scenario | **REDUCTION** | Replaces LOW. Rename in the MVP, docs and tests during Phase 5 |
| Scenario boat variable | **Arriving boats** | The brief's `successfulBoats` means arriving boats as counted by the Home Office. No departure-success rate is introduced without evidence |
| Evidence classification | **Six classes plus HIGH/MEDIUM/LOW confidence** | Migrate all 32 existing claims; keep each claim's confidence rationale |
| MVP application | **Frozen prototype** | Revised in Phase 5 after research approval |
| Event coordinates | Latitude/longitude only with an explicit location type and precision | Area-level reports keep null or area geometry; no false points |

## Architecture

Use React with strict TypeScript, MapLibre GL JS for geography, and Three.js for selective 3D elements. Static application with an offline research/data pipeline; no backend.

Pipeline: sources → normalized evidence → validation → versioned application data → declarative scenes → React interface and map renderer. A separate scenario engine consumes explicit assumptions.

- Data pipeline: normalize source data, calculate metrics, preserve provenance, validate generated assets.
- Story controller: active scene, selected year, camera targets, navigation, narrative progression.
- Map renderer: MapLibre lifecycle; Channel layers; camera transitions.
- Three.js renderer: MapLibre custom layer sharing its camera; reusable geometry/materials and explicit GPU cleanup.
- React interface: narration, charts, evidence drawer, navigation, scenario controls, accessible data view.

Keep animation outside React state. Lazy-load maps and 3D assets. Supply reduced-motion behaviour and a readable alternative when WebGL is unavailable. Use conventional charts for numeric comparisons and 3D only where it communicates information. Label illustrative boat models; do not imply verified dimensions.

## Scene model

Each scene declares its ID, title, narration, evidence classification, claim/dataset references, camera and transition, map layers, chart configuration, interactions, reduced-motion behaviour and accessible text equivalent.

Provisional sequence, following `story.md`:

| # | Scene | Purpose | Presentation |
| --- | --- | --- | --- |
| 1 | Dover Strait | Establish geography | Regional map and labelled coasts |
| 2 | Occupancy over time | People per arriving boat | Annual/monthly chart beside the map |
| 3 | 2022 versus 2025 | Compare people, boats and occupancy | Source-backed comparison |
| 4 | Why occupancy matters | Explain the arithmetic | Interactive decomposition |
| 5 | Crossing geography | Documented locations and the geography conclusion | Areas/events by location type, with uncertainty |
| 6 | Distributed geography | Hypothetical wider footprint | Distinct scenario overlay |
| 7 | Capacity × boat count | Explore assumptions | Occupancy and arriving-boat controls |
| 8 | Future scenarios | REDUCTION, CONTINUATION, EXPANSION | Presets exposing assumptions |
| 9 | Closing question | Summarize uncertainty | “What happens if capacity and geographic reach continue to increase?” |

The closing question is hypothetical. Story wording is provisional until the evidence supports it.

## Data model

| Entity | Required fields |
| --- | --- |
| Source | ID, publisher, title, URL, publication/retrieval dates, version, licence, table/locator |
| Claim | Statement, sources, classification, confidence (HIGH/MEDIUM/LOW) and rationale, review status, dates, geography |
| Annual/monthly record | Period start/end, people, arriving boats, published average (if any), calculated average, completeness, sources |
| Vessel evidence | Date, attribute (length, construction, engine, fuel, capacity, seizure, supply chain), value, context, representativeness, claims |
| Crossing event | Type, date, location type, geometry (nullable), location precision, origin/destination area, passengers, vessel, claims |
| Documented route | Origin/destination references, location types, geodesic distance, method, uncertainty, claims |
| Derived metric | Value, units, formula, input references, precision and rounding |
| Scenario | Horizon, assumptions, rationale, outputs |
| Scene | Narrative, evidence, camera, layers, controls, accessible alternative |

Evidence classifications: OFFICIAL_STATISTIC, DOCUMENTED_EVENT, DERIVED_STATISTIC, REPORTED_EVENT, HYPOTHESIS, SCENARIO. Working definitions to confirm in Phase 1:

- OFFICIAL_STATISTIC: a figure published in official statistics.
- DOCUMENTED_EVENT: an event recorded in a primary official or investigative source.
- REPORTED_EVENT: an event described second-hand or attributed (news, operational summaries).

Migrate existing OBSERVED FACT claims to OFFICIAL_STATISTIC or DOCUMENTED_EVENT case by case, and reassess confidence rather than mapping it mechanically. Classification is distinct from source quality and confidence.

Location types are a separate field: OBSERVED LOCATION, REPORTED LOCATION, DERIVED CORRIDOR, ILLUSTRATIVE ROUTE. Only the first two are historical locations; a derived corridor is an analytical product, and an illustrative route belongs to scenarios or explanatory graphics.

Rules:

- All visible factual statistics require source metadata and traceable derivations.
- Occupancy = total people / total arriving boats, using matching periods and definitions. Store the published and calculated figures and flag discrepancies. Do not average rounded monthly averages.
- Treat 2026 as partial-year until a complete annual release exists; expose the cutoff and avoid unqualified full-year comparisons. Keep provisional daily data in a separate, dated series.
- Unknown is not zero. Retain revisions.
- Preserve location precision; area-level reports must not become falsely precise points. Do not infer exact vessel tracks or general trends from selected incidents. Compute distances only for documented origin/destination pairs.
- Do not infer causes from spatial correlation.
- Scenario routes must be distinguishable without relying on colour alone. Geographic expansion does not automatically change arrivals.

Scenario arithmetic:

- Crossings: modelled arrivals = assumed arriving boats × assumed average occupancy. If controls use maximum capacity, expose a separate utilization assumption.
- Scenarios are not predictions and are stored separately from observed data.

## Structure

```text
research/
  executive-summary.md
  methodology.md
  sources.json
  claims.json
  critical-review.md
  data-gaps.md
  README.md
  validation.md
  raw/                        # Pinned source files + manifest.json
  crossings/
    annual-crossings.csv
    monthly-crossings.csv
    vessel-evidence.csv
    crossing-events.geojson
  geography/
    documented-routes.geojson
    route-analysis.json
    geographic-findings.md
  scenarios/
    assumptions.json
    capacity-scenarios.json
story/
  narration.md
  storyboard.md
scripts/                      # Data extraction, normalization and validation
src/                          # Frozen MVP; revised in Phase 5
validation/
  fact-check.md
  accessibility.md
  performance.md
```

Migration of existing research files:

| Current file | New location |
| --- | --- |
| `report.md` | Split into `executive-summary.md` and `methodology.md` |
| `open-questions.md` | `data-gaps.md` |
| `annual-crossings.csv` | `crossings/annual-crossings.csv` |
| `events.geojson` | `crossings/crossing-events.geojson` |
| `routes.geojson` | `geography/documented-routes.geojson` |
| `mvp-2026-snapshot.json` | Stays in place until Phase 5 |

`analysis/` from the original plan is folded into `research/geography/`. Moving files required a path update in `scripts/build_data.py`, the one change allowed in the frozen app, so that `yarn check` keeps passing. `research/extract_annual.py` was replaced by `research/extract_crossings.py`. Scene definitions must not depend on renderer implementation. Charts, evidence panels and data alternatives share validated records.

## Phases and completion gates

| Phase | Work | Gate | Status |
| --- | --- | --- | --- |
| 1A Crossings research | Annual/monthly series, nationality and asylum outcomes by arrival year, vessel evidence, crossing geography, route distances, explanation matrix | Claims have provenance; the geography conclusion is A, B or C from the evidence | First pass complete; reviewed in Phase 2 and approved with conditions |
| 1C Research scenarios | Crossing scenarios with stated assumptions | Scenario data separated from observed data | First pass complete (`research/scenarios/`); reviewed in Phase 2 and approved with conditions |
| 2 Critical review | Independent skeptical review of hypotheses H1–H4, plus causation, selection bias, misleading statistics/symbology and framing | Unsupported claims removed or labelled hypotheses | Complete (`research/critical-review.md`); pipeline corrections listed as required before Phase 3 |
| — Human approval | Present findings for approval | Approval recorded; only then set `approved_for_application` | Approved with conditions, 11 September 2026 (`research/approval.json`) |
| 3 Data engineering | Normalize approved data into versioned application data | Every display metric traces to inputs | Pending |
| 4 Story and UX | Revised storyboard, narration, mobile/data alternatives | No unsupported new claims; storyboard approved | Pending |
| 5 MVP revision | Rename LOW to REDUCTION, migrate evidence labels, consume the new pipeline, add scene controller support for new scenes | One complete accessible scene per section with validated data | Pending (MVP frozen) |
| 6 Historical experience | Crossing map, charts, comparisons, selective 3D | Evidence and uncertainty preserved | Pending |
| 7 Scenarios | Controls, calculations, presets and distinct overlays | Assumptions visible; scenarios unmistakable | Pending |
| 8 Validation/release preparation | Tests, factual audit, accessibility, performance, dependencies | Checks pass and limitations documented | Pending |

## Phase 1 approach

Source priority: Home Office; other UK government departments; NCA; Border Security Command; Parliament and the Commons Library; official UK statistical agencies; French government; French maritime authorities; UK maritime authorities; peer-reviewed research; then Reuters, BBC and other established news organizations. Avoid political social-media posts, advocacy graphics without primary data, unsourced migration websites and anonymous claims. News may identify events but must not replace official statistics.

Record competing explanations and evidence against each hypothesis. Carry forward the gaps and discrepancies in `research/data-gaps.md`.

Capture publication dates, URLs, source locators, definitions, classifications, confidence rationale, temporal coverage and geographic precision. Distinguish numeric verification from independent critical review. Mark research incomplete where tables, geometry or evidence cannot be verified.

Research is complete only when primary sources are recorded, calculations are reproducible, geographic data is validated, observed and scenario data are separated, important claims are critically reviewed, and data limitations are documented.

## Validation and release preparation

- Test calculations, zero denominators, missing data, period matching and scenario inputs.
- Test story navigation, scene transitions, mobile layouts, keyboard interaction, reduced motion and data-only access.
- Audit every visible factual claim against the claim registry; fail unsupported claims.
- Measure the 60 FPS target on defined desktop/mobile devices, plus bundle size, LCP, memory, draw calls and GeoJSON size. Optimize based on measurements.
- Verify map lifecycle and GPU disposal, dependencies, secrets, CSP, tile/API terms, attribution and data licensing.
- `yarn check` exists in the MVP (data check, unit tests, TypeScript, build, browser tests). Extend it with research-data validation in Phase 3.
- Update README.md, docs/project/ARCHITECTURE.md, docs/project/METHODOLOGY.md, docs/project/DATA_SOURCES.md, docs/project/SCENARIO_MODEL.md and docs/project/AI_USAGE.md. Document actual contributions and human review honestly, including that the MVP preceded research review.

Deployment is a separate release action after the above work is concrete and reviewable.

## UI amendment — 11 September 2026

The user authorized changes to the existing Day 1 interface: switchable themes, design foundations, font-size controls, WCAG AA improvements, autoplay, a shared full-window map/chart view, and highlighted routes. This amendment does not approve the separate research registry.

Implemented in the local MVP: semantic dark/light tokens and live foundations dialog; persistent 100–200% text controls; responsive map/chart workspace with notes and data alternatives; explicit 14-step playback with pause, pace and restart; native dialogs and accessible map pan controls; highlighted indicative Dover–Calais connection and amber hypothetical scenario connections. See docs/project/DESIGN_SYSTEM.md and docs/project/ACCESSIBILITY.md for behavior and verification scope.
