# Research assets

Status: this release covers Channel crossings up to arrival in the UK: the Phase 1A crossings research and the crossing scenarios from Phase 1C. The Phase 2 critical review is done ([critical-review.md](critical-review.md)), and the research was approved with conditions on 11 September 2026 ([approval.json](approval.json)): 202 of the 221 claims in this release are approved for application use. After-arrival and asylum-support research is not included. Start with [executive-summary.md](executive-summary.md). The plan is [../docs/implementation-plan.md](../docs/implementation-plan.md).

## Layout

| Path | Contents |
| --- | --- |
| `executive-summary.md` | Phase 1 findings and what must not be visualized |
| `methodology.md` | Source priority, classification, calculation and location rules |
| `approval.json` | Human approval record: decision, conditions, approval rule and withheld claims |
| `critical-review.md` | Phase 2 review: H1–H5 verdicts, cross-cutting checks, numeric spot-check, corrections, Part 20 answers, the decision needed |
| `data-gaps.md` | Open gaps, discrepancies and the completion gate |
| `sources.json` | 109 sources: publication and retrieval dates, inspection status, licence, caveats |
| `claims.json` | 221 claims: classification, confidence and rationale, evidence locators, calculations |
| `raw/` | Pinned source files; `raw/manifest.json` gives URLs and SHA-256 hashes. Only the manifest and the five files from the initial import are versioned. The rest are git-ignored because of size and licences (some sources forbid reproduction). Re-download them from the manifest URLs and check the hashes; `validate_research.py` needs them locally |
| `crossings/` | Annual and monthly series, nationality, age and sex, asylum claims and decisions, published occupancy, release vintages, vessel evidence, crossing events, findings |
| `geography/` | Documented start-and-end pairs, route analysis, geocoding log, explanation matrix, findings |
| `mvp-2026-snapshot.json` | Provisional 2026 record used only by the frozen MVP |
| `scenarios/` | Phase 1C: `assumptions.json`, `capacity-scenarios.json` (REDUCTION, CONTINUATION, EXPANSION and a boats x occupancy grid) and `scenario-claims.json` (crossing scenarios only in this release). Hypothetical arithmetic on stated assumptions; never observed data and not forecasts |

## Reproduce

All scripts use the Python standard library and never modify files in `raw/`. Run them in this order, because `extract_crossings.py` reads the published-occupancy file that `reconcile_series.py` writes:

```sh
python3 research/reconcile_series.py    # release vintages; published vs calculated occupancy
python3 research/extract_decisions.py   # asylum decisions by arrival year (detailed dataset)
python3 research/extract_crossings.py   # annual, monthly, nationality, age/sex, asylum-claim CSVs
python3 research/build_geography.py     # crossing events and documented pairs, from the geocoding log
python3 research/route_analysis.py      # straight-line distances and the Part 4 conclusion
python3 research/validate_research.py   # registry, hash, arithmetic and GeoJSON checks
```

Not runnable in this release: `build_scenarios.py` and the after-arrival scripts (`extract_asylum_support.py`, `build_lageo.py`, `build_asylum_geography.py`, `extract_ho_reg_history.py`) are kept unchanged, but their inputs are not included. The files in `scenarios/` are filtered from a full build.

`geocode_places.py` queries OpenStreetMap Nominatim over the network. Run it only when adding places; every query and result is logged in `geography/geocoding-log.json`.

## Conventions

- **Classifications:** OFFICIAL_STATISTIC, DOCUMENTED_EVENT, DERIVED_STATISTIC, REPORTED_EVENT, HYPOTHESIS and SCENARIO. Confidence is HIGH, MEDIUM or LOW, with a rationale. See [methodology.md](methodology.md).
- **Unknown values:** unknown is never zero. Months after the pinned cutoff and months with no boats have blank averages.
- **Precision:** values keep six decimal places; display uses two.
- **Locations:** each has a location type and precision, and area-level points state `uncertainty_km`. Straight-line pairs are not tracks.
- **Licences:** Préfecture maritime material is link-and-paraphrase only (no open licence). Check each source's `licence` field before reuse.
