"""Validate the research bundle's structure, provenance and arithmetic; stdlib only.

Run: python3 research/validate_research.py
Checks sources, the raw-file manifest (hashes), the claim registry, crossing CSVs against
claims, and GeoJSON location rules. Exits non-zero on any failure. Structural and numeric
checks only: this is not fact-checking or critical review.
"""
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CLASSIFICATIONS = {"OFFICIAL_STATISTIC", "DOCUMENTED_EVENT", "DERIVED_STATISTIC",
                   "REPORTED_EVENT", "HYPOTHESIS", "SCENARIO"}
CONFIDENCE = {"HIGH", "MEDIUM", "LOW"}
LOCATION_TYPES = {"OBSERVED LOCATION", "REPORTED LOCATION", "DERIVED CORRIDOR", "ILLUSTRATIVE ROUTE"}
PRECISIONS = {"exact_coordinates", "facility", "named_place", "named_area", "region", "unknown"}
failures = []


def check(condition, message):
    if not condition:
        failures.append(message)
    return condition


def close(a, b, tolerance=1e-6):
    return abs(float(a) - float(b)) <= tolerance


def load_json(name):
    return json.loads((ROOT / name).read_text())


def validate_sources():
    sources = load_json("sources.json")["sources"]
    ids = [s["id"] for s in sources]
    check(len(ids) == len(set(ids)), "sources: duplicate IDs")
    for s in sources:
        for field in ("id", "publisher", "title", "url", "type", "status", "licence", "retrieved_at"):
            check(s.get(field), f"source {s.get('id')}: missing {field}")
        check("publication_date" in s, f"source {s['id']}: publication_date key missing (use null if unknown)")
        if s.get("local_path"):
            check((ROOT / s["local_path"]).exists(), f"source {s['id']}: missing local file {s['local_path']}")
    return {s["id"] for s in sources}


def validate_manifest(source_ids):
    for entry in load_json("raw/manifest.json")["files"]:
        path = ROOT / entry["file"]
        if not check(path.exists(), f"manifest: missing {entry['file']}"):
            continue
        data = path.read_bytes()
        check(hashlib.sha256(data).hexdigest() == entry["sha256"], f"manifest: hash mismatch {entry['file']}")
        if "bytes" in entry:
            check(len(data) == entry["bytes"], f"manifest: size mismatch {entry['file']}")
        check(entry["source_id"] in source_ids, f"manifest: unknown source {entry['source_id']}")


def load_approval():
    """The human approval record (research/approval.json), or None before approval."""
    path = ROOT / "approval.json"
    if not path.exists():
        return None
    approval = json.loads(path.read_text(encoding="utf-8"))
    check(approval.get("decision") in {"approved", "approved_with_conditions"}, "approval: invalid decision")
    check(approval.get("approved_on") and approval.get("approved_by"), "approval: missing approver or date")
    return approval


def validate_claims(source_ids):
    claims = load_json("claims.json")["claims"]
    ids = [c["id"] for c in claims]
    check(len(ids) == len(set(ids)), "claims: duplicate IDs")
    known = set(ids)
    approval = load_approval()
    withheld = {w["id"] for w in approval["withheld"]} if approval else set()
    if approval:
        check(withheld <= known, f"approval: withheld IDs not in registry {sorted(withheld - known)}")
        approved = sum(1 for c in claims if c.get("approved_for_application") is True)
        check(approval["counts"] == {"claims": len(claims), "approved": approved, "withheld": len(withheld)},
              "approval: counts do not match the registry")
    for c in claims:
        cid = c["id"]
        check(c.get("claim"), f"claim {cid}: empty statement")
        check(c.get("classification") in CLASSIFICATIONS, f"claim {cid}: invalid classification {c.get('classification')}")
        check(c.get("confidence") in CONFIDENCE, f"claim {cid}: invalid confidence {c.get('confidence')}")
        check(c.get("confidence_rationale"), f"claim {cid}: missing confidence rationale")
        check(c.get("review_status"), f"claim {cid}: missing review status")
        if not approval:
            check(c.get("approved_for_application") is False, f"claim {cid}: approval must remain false before review")
        elif c.get("approved_for_application") is True:
            # Approval needs a recorded human decision, Phase 2 review, and must respect the withholding rule.
            check(c.get("review_status") == "independently_reviewed_phase2", f"claim {cid}: approved without Phase 2 review")
            check(cid not in withheld, f"claim {cid}: approved but listed as withheld")
            check(c.get("classification") == "SCENARIO" or c.get("confidence") != "LOW",
                  f"claim {cid}: LOW-confidence observed claim cannot be approved")
        else:
            check(c.get("approved_for_application") is False and cid in withheld,
                  f"claim {cid}: not approved but missing from approval.json withheld list")
        check(c.get("evidence"), f"claim {cid}: no evidence")
        for e in c.get("evidence", []):
            check(e.get("source_id") in source_ids, f"claim {cid}: unknown source {e.get('source_id')}")
            check(e.get("locator"), f"claim {cid}: evidence without locator")
        calc = c.get("calculation")
        if c.get("classification") == "DERIVED_STATISTIC":
            check(calc and calc.get("formula"), f"claim {cid}: derived statistic without calculation formula")
        if calc:
            for ref in calc.get("input_claim_ids", []):
                check(ref in known, f"claim {cid}: unknown input claim {ref}")
            for ref in calc.get("input_files", []) + ([calc["output_file"]] if calc.get("output_file") else []):
                check((ROOT / ref).exists(), f"claim {cid}: missing file {ref}")
    return {c["id"]: c for c in claims}


def validate_crossings(claims):
    annual = {int(r["year"]): r for r in csv.DictReader((ROOT / "crossings/annual-crossings.csv").open())}
    monthly = list(csv.DictReader((ROOT / "crossings/monthly-crossings.csv").open()))
    for year, r in annual.items():
        people, boats = int(r["people"]), int(r["boats"])
        check(close(r["average_people_per_boat"], people / boats), f"annual {year}: average mismatch")
        rows = [m for m in monthly if int(m["year"]) == year]
        check(len(rows) == int(r["months_covered"]), f"annual {year}: month coverage mismatch")
        check(sum(int(m["people"]) for m in rows) == people, f"annual {year}: monthly people do not sum")
        check(sum(int(m["boats"]) for m in rows) == boats, f"annual {year}: monthly boats do not sum")
        claim = claims.get(f"ANNUAL-{year}")
        if check(claim, f"annual {year}: no ANNUAL claim"):
            check(claim["values"] == {"people": people, "boats": boats}, f"ANNUAL-{year}: values differ from CSV")
        occupancy = claims.get(f"OCCUPANCY-{year}")
        if check(occupancy, f"annual {year}: no OCCUPANCY claim"):
            check(close(occupancy["calculation"]["value"], people / boats), f"OCCUPANCY-{year}: value differs")
        yoy = claims.get(f"YOY-{year}")
        if yoy:
            for key in ("people_change_pct", "boats_change_pct", "occupancy_change_pct"):
                check(close(yoy["calculation"]["values"][key], round(float(r[key]), 2), 0.005),
                      f"YOY-{year}: {key} differs from CSV")
    for m in monthly:
        if int(m["boats"]):
            check(close(m["average_people_per_boat"], int(m["people"]) / int(m["boats"])),
                  f"monthly {m['year']}-{m['month']}: average mismatch")
        else:
            check(m["average_people_per_boat"] == "", f"monthly {m['year']}-{m['month']}: zero-boat average must be blank")
    comparison = claims.get("COMPARISON-2022-2025")
    if comparison:
        (p0, b0), (p1, b1) = [(int(annual[y]["people"]), int(annual[y]["boats"])) for y in (2022, 2025)]
        expected = {"people_pct": 100 * (p1 / p0 - 1), "boats_pct": 100 * (b1 / b0 - 1),
                    "occupancy_pct": 100 * ((p1 / b1) / (p0 / b0) - 1)}
        for key, value in expected.items():
            check(close(comparison["calculation"]["values"][key], value), f"COMPARISON-2022-2025: {key} differs")
    for path in sorted((ROOT / "crossings").glob("*.csv")):
        for i, row in enumerate(csv.DictReader(path.open()), 2):
            for key in ("classification", "counts_classification", "derived_classification"):
                if key in row:
                    check(row[key] in CLASSIFICATIONS, f"{path.name}:{i}: invalid {key} {row[key]}")


def validate_geojson(claims):
    for path in sorted(list((ROOT / "crossings").glob("*.geojson")) + list((ROOT / "geography").glob("*.geojson"))):
        data = json.loads(path.read_text())
        name = path.relative_to(ROOT)
        if not check(data.get("type") == "FeatureCollection", f"{name}: not a FeatureCollection"):
            continue
        ids = [f.get("id") or f.get("properties", {}).get("id") for f in data["features"]]
        check(all(ids) and len(ids) == len(set(ids)), f"{name}: feature IDs missing or duplicated")
        for f in data["features"]:
            p, fid, geometry = f.get("properties", {}), f.get("id"), f.get("geometry")
            check(p.get("classification") in CLASSIFICATIONS, f"{name} {fid}: invalid classification")
            check(p.get("approved_for_application") is False, f"{name} {fid}: approval must remain false")
            for ref in p.get("claim_ids", []):
                check(ref in claims, f"{name} {fid}: unknown claim {ref}")
            if geometry and geometry.get("type") == "LineString":
                # A documented pair: each endpoint carries its own location type and precision.
                check(p.get("geometry_meaning"), f"{name} {fid}: line without geometry_meaning")
                for role in ("origin", "destination"):
                    check_location(p.get(role) or {}, True, f"{name} {fid} {role}")
            else:
                check_location(p, geometry is not None, f"{name} {fid}")


def check_location(p, has_geometry, label):
    check(p.get("location_type") in LOCATION_TYPES, f"{label}: invalid location_type {p.get('location_type')}")
    check(p.get("location_precision") in PRECISIONS, f"{label}: invalid location_precision")
    if has_geometry:
        check(p.get("location_precision") != "unknown", f"{label}: geometry with unknown precision")
        check(p.get("geometry_source"), f"{label}: geometry without geometry_source")
        if p.get("location_precision") in ("named_area", "region"):
            check(p.get("uncertainty_km") is not None, f"{label}: area geometry without uncertainty_km")


def validate_asylum(source_ids):
    """Asylum-support outputs from build_asylum_geography.py; skipped until they exist."""
    base = ROOT / "asylum"
    if not (base / "asylum-support-local-authority.csv").exists():
        return
    lookup = {r["la_code"] for r in csv.DictReader((base / "la-lookup.csv").open())}
    rows = list(csv.DictReader((base / "asylum-support-local-authority.csv").open()))
    check({r["la_code"] for r in rows} == lookup, "asylum snapshot: local authorities differ from lookup")
    for r in rows:
        pop = int(r["population"])
        for count, per in (("total_asylum_support", "total_per_10000"), ("dispersal", "dispersal_per_10000")):
            if r[count] != "":
                check(close(r[per], int(r[count]) / pop * 10000), f"asylum {r['la_code']}: {per} mismatch")
            else:
                check(r[per] == "", f"asylum {r['la_code']}: {per} without a count")
        for s in r["source_ids"].split(";"):
            check(s in source_ids, f"asylum {r['la_code']}: unknown source {s}")
    dispersal = [r for r in csv.DictReader((base / "dispersal-accommodation.csv").open()) if r["rank_absolute"]]
    ranked = sorted(dispersal, key=lambda r: int(r["rank_absolute"]))
    check(all(int(a["dispersal_accommodation"]) >= int(b["dispersal_accommodation"]) for a, b in zip(ranked, ranked[1:])),
          "dispersal ranks not in descending order")
    summary = json.loads((base / "asylum-summary.json").read_text())
    for q in summary["national_reconciliation"]:
        if q["national_total"]:
            check(abs(q["difference"]) <= 0.005 * q["national_total"],
                  f"asylum {q['date']}: LA sum differs from national total by {q['difference']}")
    required = {"localAuthorityCode", "localAuthorityName", "population", "totalAsylumSupport", "dispersalAccommodation",
                "hotelAccommodation", "per10000", "reportingDate", "sourceIds"}
    for name in ("asylum-support.geojson", "dispersal-accommodation.geojson"):
        data = json.loads((base / name).read_text())
        codes = [f["properties"]["localAuthorityCode"] for f in data["features"]]
        check(set(codes) == lookup and len(codes) == len(lookup), f"{name}: features differ from lookup")
        for f in data["features"]:
            p = f["properties"]
            if name == "asylum-support.geojson":
                missing = required - set(p)
                check(not missing, f"{name} {p['localAuthorityCode']}: missing {sorted(missing)}")
            check(p.get("approvedForApplication") is False, f"{name} {p['localAuthorityCode']}: approval must remain false")
    # Asylum-support geography must never be labelled as where small-boat arrivals live (research-asylum Part 12).
    banned = re.compile(r"where small[- ]boat (migrants|arrivals) live", re.I)
    for path in base.iterdir():
        if path.suffix in (".csv", ".json", ".geojson"):
            check(not banned.search(path.read_text()), f"{path.name}: prohibited small-boat residence wording")


def main():
    source_ids = validate_sources()
    validate_manifest(source_ids)
    claims = validate_claims(source_ids)
    validate_crossings(claims)
    validate_geojson(claims)
    validate_asylum(source_ids)
    if failures:
        print(f"FAIL: {len(failures)} problem(s)")
        for message in failures:
            print(" -", message)
        sys.exit(1)
    asylum = " and asylum-support outputs" if (ROOT / "asylum" / "asylum-support-local-authority.csv").exists() else ""
    print(f"PASS: {len(source_ids)} sources, {len(claims)} claims, manifest hashes, crossing CSVs, GeoJSON rules{asylum}.")


if __name__ == "__main__":
    main()
