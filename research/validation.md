# Research validation

First run: 11 September 2026, after the Phase 1A and 1B merges. Latest run: 12 September 2026, on the crossings release scope, with 109 sources and 221 claims; the validator also enforces the approval rule in [approval.json](approval.json). These are structural and arithmetic checks, not independent fact-checking. Critical review is recorded separately in [critical-review.md](critical-review.md).

`python3 research/validate_research.py` passes. It checks:

- **Sources:** all 109 have unique IDs and the required fields, and every local file exists.
- **Raw files:** every file in `raw/manifest.json` exists and matches its SHA-256 hash and size.
- **Claims:** all 221 have a valid classification (six-class scheme) and confidence (HIGH, MEDIUM or LOW), a rationale, and evidence with a known source and a locator. Approval flags follow the rule recorded in [approval.json](approval.json). Every DERIVED_STATISTIC has a formula, and its input claims and files exist.
- **Annual and monthly CSVs:** averages equal people ÷ boats, monthly values sum to annual totals, month coverage is correct, and months with no boats have blank averages.
- **Crossing claims:** the annual, occupancy, year-on-year and 2022–2025 comparison claims match the CSVs.
- **Classification columns** in every crossing CSV use the six-class scheme.
- **GeoJSON:**
  - Every event has a valid location type and precision.
  - Any geometry has a `geometry_source`; area or region points have `uncertainty_km`.
  - Straight-line pairs have `geometry_meaning`, and each endpoint has its own location type, precision and source.
  - All referenced claims exist.

Checks in the extraction scripts (each asserts and fails on mismatch):

- **`extract_crossings.py`:**
  - 18 monthly sums against the published totals.
  - The July 2025–June 2026 rolling total against the published narrative (33,374 people, 511 boats).
  - Nationality and age/sex totals against IER_02a.
  - IER_02d categories summing to that table's total.
  - Every published Home Office average agreeing across releases and matching our rounded calculation.
- **`extract_decisions.py`:** D03 outcomes sum to D02 claims, for people and for main applicants, and D02 totals match IER_02d.
- **`reconcile_series.py`, `build_geography.py` and `route_analysis.py`:** after being moved into `research/`, each reproduced its outputs byte for byte.

The frozen MVP's `yarn data:check` still passes against the moved annual CSV.

Not performed:

- Checking source content beyond what each research pass recorded.
- Verification of the unverified leads and blocked sources in [data-gaps.md](data-gaps.md).
