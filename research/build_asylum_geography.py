"""Join Home Office asylum support by local authority to ONS boundaries and population; stdlib only.

Run: python3 research/build_asylum_geography.py [data_dir]
Inputs in research/asylum/ (or data_dir): asylum-support-long.csv, asylum-support-national.csv,
ho-rates-per-10000.csv, la-lookup.csv, la-code-changes.csv, population.csv, uk-local-authorities.geojson.
Writes the snapshot, dispersal, regional, quarterly and change tables, two GeoJSON layers and
asylum-summary.json to the same directory. Observed data only: no scenarios, no causal labels.

Terminology (research-asylum Part 12): these are people receiving asylum support. The data do not
identify small-boat arrivals, so nothing here describes where small-boat arrivals live.
"""
import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "asylum"
SNAPSHOT = "2026-06-30"
# First quarter-end with a full local-authority breakdown: before it, Section 98 (up to 37,142 people)
# is not broken down by local authority (Asy_D11 notes 14–16). Dispersal at this date still includes
# Section 4 recipients housed in hotels (note 6, until 31 March 2023).
BASELINE = "2022-12-31"
START = "2022-03-31"
REVIEW = "source_checked_pending_independent_review"

# Published accommodation labels -> analysis categories. Unmapped labels stop the build.
CATEGORIES = {
    "dispersal accommodation": "dispersal",
    "contingency accommodation - hotel": "contingency_hotel",
    "contingency accommodation - other": "contingency_other",
    "initial accommodation": "initial",
    "subsistence only": "subsistence_only",
    "other accommodation": "other",
}
CATEGORY_ORDER = ["dispersal", "contingency_hotel", "contingency_other", "initial", "subsistence_only", "other"]
# Splits cannot be harmonised by aggregation. The only one in scope moved about 8.56 ha (0.03% of
# Barnsley's area) from Barnsley to Sheffield on 1 April 2025, with no published population. Old
# Barnsley is treated as continuing into new Barnsley: a documented approximation. Others stop the build.
SPLIT_PRIMARY = {"E08000016": "E08000038"}
# Published local-authority names that normalisation cannot match, mapped by hand to codes.
NAME_OVERRIDES = {}
UNALLOCATED = re.compile(r"^(unknown|not known|other|unallocated|not recorded|n/a)\b", re.I)
# Change categories compare the baseline and snapshot quarter-ends (a research choice).
SUBSTANTIAL_PCT, SUBSTANTIAL_PEOPLE = 50.0, 50


def read_csv(name):
    with (DATA / name).open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(name, rows, fields=None):
    with (DATA / name).open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields or list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def norm(text):
    text = text.lower().replace("&", " and ").replace("–", "-").replace("’", "'")
    text = re.sub(r",?\s*city of\b|\bcity of\s+", " ", text)
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def label(text):
    return " ".join(text.lower().replace("–", "-").replace("—", "-").split())


def rate(people, population):
    return None if people is None or not population else people / population * 10000


def fmt(value, places=6):
    return "" if value is None else f"{value:.{places}f}"


def pct_change(new, old):
    return None if new is None or not old else (new - old) / old * 100


def main():
    lookup = {r["la_code"]: r for r in read_csv("la-lookup.csv")}
    changes = read_csv("la-code-changes.csv")
    successor = {}
    for c in changes:
        if c["old_code"] == c["new_code"]:
            continue
        if c["change_type"] == "split":
            assert c["old_code"] in SPLIT_PRIMARY, f"split cannot be harmonised by aggregation: {c}"
            successor[c["old_code"]] = SPLIT_PRIMARY[c["old_code"]]
        else:
            successor.setdefault(c["old_code"], c["new_code"])

    def harmonise(code):
        seen = set()
        while code in successor and code not in seen:
            seen.add(code)
            code = successor[code]
        return code

    names = {norm(r["la_name"]): code for code, r in lookup.items()}
    for c in changes:
        names.setdefault(norm(c["old_name"]), harmonise(c["new_code"]))
    names.update({norm(k): v for k, v in NAME_OVERRIDES.items()})

    # Boundaries must match the lookup exactly.
    boundaries = json.loads((DATA / "uk-local-authorities.geojson").read_text())
    feature_codes = [f["properties"]["localAuthorityCode"] for f in boundaries["features"]]
    assert len(feature_codes) == len(set(feature_codes)), "duplicate boundary codes"
    assert set(feature_codes) == set(lookup), (
        f"boundary/lookup mismatch: {sorted(set(feature_codes) ^ set(lookup))[:10]}")

    # Population, harmonised to the current codes by summing merged predecessors.
    population = defaultdict(dict)
    pop_sources = set()
    for r in read_csv("population.csv"):
        code = harmonise(r["la_code"])
        year = int(r["mid_year"])
        population[code][year] = population[code].get(year, 0) + int(r["population"])
        pop_sources.add(r["source_id"])
    missing_pop = [c for c in lookup if not population.get(c)]
    assert not missing_pop, f"no population for {missing_pop[:10]}"
    latest_year = max(max(years) for years in population.values())
    # Nations publish mid-year estimates at different times (Northern Ireland lags), so each local
    # authority uses its latest available mid-year, recorded per row, as the Home Office does in Reg_02.
    snapshot_years = {c: max(y for y in population[c] if y <= int(SNAPSHOT[:4])) for c in lookup}
    assert min(snapshot_years.values()) >= latest_year - 1, "population more than one year behind the latest"

    def population_for(code, date):
        year = int(date[:4])
        years = population[code]
        usable = [y for y in years if y <= year] or [min(years)]
        chosen = max(usable)
        return years[chosen], chosen

    # Asylum support: map each published row to a current code and an analysis category.
    unmatched, unmapped_labels = defaultdict(int), set()
    cells = defaultdict(int)          # (date, code, category) -> people
    support_cells = defaultdict(int)  # (date, code, support_type) -> people
    suppressed = defaultdict(int)     # (date, code) -> count of blank cells
    suppressed_cat = defaultdict(int)  # (date, code, category) -> count of blank cells
    published_cats = defaultdict(set)  # date -> categories broken down by local authority that quarter
    unallocated = defaultdict(int)    # date -> people not attributable to an LA
    source_ids = set()
    for r in read_csv("asylum-support-long.csv"):
        if r["date"] < START:
            continue
        source_ids.add(r["source_id"])
        name = r["la_name_published"].strip()
        people = int(r["people"]) if r["people"].strip() else None
        # Rows without a local authority (e.g. 'Unknown', or groups the source does not break down)
        # count towards national reconciliation only; their accommodation label may be 'N/A - ...'.
        if not r["la_code_published"].strip() and UNALLOCATED.match(name):
            unallocated[r["date"]] += people or 0
            continue
        category = CATEGORIES.get(label(r["accommodation_type"]))
        if category is None:
            unmapped_labels.add(r["accommodation_type"])
            continue
        if r["la_code_published"].strip():
            code = harmonise(r["la_code_published"].strip())
        else:
            code = names.get(norm(name))
        if code not in lookup:
            unmatched[(name, r["la_code_published"])] += people or 0
            continue
        published_cats[r["date"]].add(category)
        if people is None:
            suppressed[(r["date"], code)] += 1
            suppressed_cat[(r["date"], code, category)] += 1
            continue
        cells[(r["date"], code, category)] += people
        support_cells[(r["date"], code, r["support_type"].strip())] += people
    assert not unmapped_labels, f"unmapped accommodation labels: {sorted(unmapped_labels)}"
    assert not unmatched, f"unmatched local authorities: {dict(unmatched)}"

    dates = sorted({d for d, _, _ in cells})
    assert SNAPSHOT in dates, f"snapshot {SNAPSHOT} missing; latest is {dates[-1]}"
    present = defaultdict(set)
    for d, code, _ in list(cells) + list(suppressed_cat):
        present[d].add(code)
    support_types = sorted({s for _, _, s in support_cells})

    def people_at(date, code, category=None):
        """People for an LA at a date. Asy_D11 omits local authorities with nobody supported (Reg_02
        lists them as 0), so absence is zero for categories broken down by local authority that quarter.
        A category not broken down that quarter, or with a suppressed cell, is None (unknown is not zero).
        Totals sum the known categories and are lower bounds when people are unallocated or suppressed."""
        if date not in published_cats:
            return None
        if category:
            if category not in published_cats[date] or suppressed_cat.get((date, code, category)):
                return None
            return cells.get((date, code, category), 0)
        return sum(cells.get((date, code, c), 0) for c in published_cats[date])

    def lower_bound(date, code):
        return unallocated.get(date, 0) > 0 or suppressed.get((date, code), 0) > 0

    # National reconciliation: LA sums plus unallocated rows vs the national table.
    national = defaultdict(int)
    for r in read_csv("asylum-support-national.csv"):
        if r["date"] >= START and r["people"].strip():
            national[r["date"]] += int(r["people"])
    reconciliation = []
    for d in dates:
        la_sum = sum(people_at(d, c) or 0 for c in lookup)
        reconciliation.append({
            "date": d, "local_authority_sum": la_sum, "unallocated": unallocated.get(d, 0),
            "national_total": national.get(d), "difference": None if d not in national
            else la_sum + unallocated.get(d, 0) - national[d],
            "suppressed_cells": sum(v for (dd, _), v in suppressed.items() if dd == d)})

    def region_of(code):
        r = lookup[code]
        return r["region_code"], r["region_name"], r["country"]

    # 1. Snapshot by local authority.
    snapshot_rows = []
    for code in sorted(lookup):
        pop, pop_year = population_for(code, SNAPSHOT)
        total = people_at(SNAPSHOT, code)
        dispersal = people_at(SNAPSHOT, code, "dispersal")
        row = {
            "la_code": code, "la_name": lookup[code]["la_name"],
            "country": lookup[code]["country"], "region_code": lookup[code]["region_code"],
            "region_name": lookup[code]["region_name"], "population": pop, "population_mid_year": pop_year,
            "present_in_source": code in present[SNAPSHOT],
            "total_asylum_support": "" if total is None else total,
        }
        for cat in CATEGORY_ORDER:
            value = people_at(SNAPSHOT, code, cat)
            row[cat] = "" if value is None else value
        for s in support_types:
            row["support_" + re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")] = support_cells.get((SNAPSHOT, code, s), 0)
        row.update({
            "total_per_10000": fmt(rate(total, pop)), "dispersal_per_10000": fmt(rate(dispersal, pop)),
            "suppressed_cells": suppressed.get((SNAPSHOT, code), 0),
            "total_is_lower_bound": lower_bound(SNAPSHOT, code),
            "reporting_date": SNAPSHOT, "source_ids": ";".join(sorted(source_ids | pop_sources)),
            "classification": "OFFICIAL_STATISTIC (counts); DERIVED_STATISTIC (rates)", "review_status": REVIEW,
        })
        snapshot_rows.append(row)
    write_csv("asylum-support-local-authority.csv", snapshot_rows)

    # 2. Dispersal accommodation, with absolute and per-10,000 ranks.
    with_values = [r for r in snapshot_rows if r["dispersal"] not in ("", 0)]  # ranks only where present
    uk_dispersal = sum(r["dispersal"] for r in with_values)
    by_abs = sorted(with_values, key=lambda r: (-r["dispersal"], r["la_code"]))
    by_rate = sorted(with_values, key=lambda r: (-float(r["dispersal_per_10000"]), r["la_code"]))
    abs_rank = {r["la_code"]: i for i, r in enumerate(by_abs, 1)}
    rate_rank = {r["la_code"]: i for i, r in enumerate(by_rate, 1)}
    dispersal_rows = [{
        "la_code": r["la_code"], "la_name": r["la_name"], "region_name": r["region_name"],
        "country": r["country"], "dispersal_accommodation": r["dispersal"], "population": r["population"],
        "population_mid_year": r["population_mid_year"], "dispersal_per_10000": r["dispersal_per_10000"],
        "has_dispersal": r["dispersal"] != "" and r["dispersal"] > 0,
        "share_of_uk_dispersal_pct": fmt(r["dispersal"] / uk_dispersal * 100) if r["dispersal"] != "" and uk_dispersal else "",
        "rank_absolute": abs_rank.get(r["la_code"], ""), "rank_per_10000": rate_rank.get(r["la_code"], ""),
        "reporting_date": SNAPSHOT, "present_in_source": r["present_in_source"],
    } for r in snapshot_rows]
    write_csv("dispersal-accommodation.csv", dispersal_rows)

    # 3. Regional summary (English regions; Wales, Scotland and Northern Ireland as nations).
    regions = defaultdict(lambda: {"population": 0, "las": 0, "las_with_dispersal": 0,
                                   **{c: 0 for c in CATEGORY_ORDER}, "total": 0})
    for r in snapshot_rows:
        g = regions[(r["region_code"], r["region_name"], r["country"])]
        g["population"] += r["population"]
        g["las"] += 1
        if r["dispersal"] != "" and r["dispersal"] > 0:
            g["las_with_dispersal"] += 1
        for c in CATEGORY_ORDER:
            g[c] += r[c] or 0
        g["total"] += r["total_asylum_support"] or 0
    regional_rows = [{
        "region_code": k[0], "region_name": k[1], "country": k[2], "population": g["population"],
        "local_authorities": g["las"], "local_authorities_with_dispersal": g["las_with_dispersal"],
        "total_asylum_support": g["total"], **{c: g[c] for c in CATEGORY_ORDER},
        "total_per_10000": fmt(rate(g["total"], g["population"])),
        "dispersal_per_10000": fmt(rate(g["dispersal"], g["population"])),
        "share_of_uk_dispersal_pct": fmt(g["dispersal"] / uk_dispersal * 100) if uk_dispersal else "",
        "reporting_date": SNAPSHOT,
    } for k, g in sorted(regions.items())]
    write_csv("regional-summary.csv", regional_rows)

    # 4. Quarterly history on current codes.
    quarterly_rows = []
    for d in dates:
        for code in sorted(lookup):
            pop, pop_year = population_for(code, d)
            for cat in CATEGORY_ORDER + ["total"]:
                value = people_at(d, code, None if cat == "total" else cat)
                quarterly_rows.append({
                    "date": d, "la_code": code, "la_name": lookup[code]["la_name"], "category": cat,
                    "people": value, "population": pop, "population_mid_year": pop_year,
                    "per_10000": fmt(rate(value, pop)),
                    "is_lower_bound": cat == "total" and lower_bound(d, code)})
    write_csv("historical-quarterly.csv", quarterly_rows)

    # 5. Change between the baseline and snapshot quarter-ends, per local authority.
    def classify(new, old):
        if new is None or old is None:
            return "not_comparable"
        diff = new - old
        pct = pct_change(new, old)
        if diff >= SUBSTANTIAL_PEOPLE and (pct is None or pct >= SUBSTANTIAL_PCT):
            return "increased_substantially"
        if -diff >= SUBSTANTIAL_PEOPLE and pct is not None and pct <= -SUBSTANTIAL_PCT:
            return "decreased_substantially"
        return "relatively_stable"

    change_rows = []
    for code in sorted(lookup):
        base_pop, base_year = population_for(code, BASELINE)
        snap_pop, snap_year = population_for(code, SNAPSHOT)
        row = {"la_code": code, "la_name": lookup[code]["la_name"], "region_name": lookup[code]["region_name"],
               "baseline_date": BASELINE, "snapshot_date": SNAPSHOT}
        for cat in ("total", "dispersal", "contingency_hotel"):
            old = people_at(BASELINE, code, None if cat == "total" else cat) if BASELINE in dates else None
            new = people_at(SNAPSHOT, code, None if cat == "total" else cat)
            row.update({
                f"{cat}_baseline": "" if old is None else old, f"{cat}_snapshot": "" if new is None else new,
                f"{cat}_change": "" if None in (old, new) else new - old,
                f"{cat}_change_pct": fmt(pct_change(new, old)),
                f"{cat}_per_10000_change": "" if None in (old, new) else fmt(rate(new, snap_pop) - rate(old, base_pop)),
                f"{cat}_category": classify(new, old)})
        row.update({"population_mid_years": f"{base_year};{snap_year}",
                    "rule": f"substantial = change of at least {SUBSTANTIAL_PEOPLE} people and {SUBSTANTIAL_PCT:.0f}%"})
        change_rows.append(row)
    write_csv("asylum-change-2022-2026.csv", change_rows)

    # 6. GeoJSON layers (research-asylum Part 10 properties). Geometry is copied from the boundary file.
    by_code = {r["la_code"]: r for r in snapshot_rows}
    common = lambda r: {
        "localAuthorityCode": r["la_code"], "localAuthorityName": r["la_name"], "population": r["population"],
        "populationMidYear": r["population_mid_year"], "reportingDate": SNAPSHOT,
        "presentInSource": r["present_in_source"], "sourceIds": r["source_ids"].split(";"),
        "reviewStatus": REVIEW, "approvedForApplication": False}
    for name, extra in (
        ("asylum-support.geojson", lambda r: {
            "totalAsylumSupport": r["total_asylum_support"] if r["total_asylum_support"] != "" else None,
            "dispersalAccommodation": r["dispersal"] if r["dispersal"] != "" else None,
            "hotelAccommodation": r["contingency_hotel"] if r["contingency_hotel"] != "" else None,
            "per10000": float(r["total_per_10000"]) if r["total_per_10000"] else None}),
        ("dispersal-accommodation.geojson", lambda r: {
            "dispersalAccommodation": r["dispersal"] if r["dispersal"] != "" else None,
            "per10000": float(r["dispersal_per_10000"]) if r["dispersal_per_10000"] else None,
            "rankAbsolute": abs_rank.get(r["la_code"]), "rankPer10000": rate_rank.get(r["la_code"])}),
    ):
        features = [{"type": "Feature", "id": f["properties"]["localAuthorityCode"], "geometry": f["geometry"],
                     "properties": {**common(by_code[f["properties"]["localAuthorityCode"]]),
                                    **extra(by_code[f["properties"]["localAuthorityCode"]])}}
                    for f in boundaries["features"]]
        (DATA / name).write_text(json.dumps({
            "type": "FeatureCollection",
            "metadata": {"title": "Geographic distribution of people receiving asylum support" if name.startswith("asylum")
                         else "Dispersal accommodation by local authority",
                         "reporting_date": SNAPSHOT, "population_mid_years": sorted(set(snapshot_years.values())),
                         "note": "People receiving asylum support; the data do not identify small-boat arrivals.",
                         "generated_by": "research/build_asylum_geography.py"},
            "features": features}, separators=(",", ":")) + "\n")

    # 7. Summary: top 20s, concentration, reconciliation, Home Office rate cross-check.
    def top(rows, key, n=20):
        return [{"la_code": r["la_code"], "la_name": r["la_name"], "value": r[key]} for r in rows[:n]]

    by_total = sorted((r for r in snapshot_rows if r["total_asylum_support"] != ""),
                      key=lambda r: (-r["total_asylum_support"], r["la_code"]))
    by_total_rate = sorted((r for r in snapshot_rows if r["total_per_10000"]),
                           key=lambda r: (-float(r["total_per_10000"]), r["la_code"]))
    cumulative, las_for = 0, {}
    for i, r in enumerate(by_abs, 1):
        cumulative += r["dispersal"]
        for threshold in (50, 80):
            if threshold not in las_for and uk_dispersal and cumulative / uk_dispersal * 100 >= threshold:
                las_for[threshold] = i
    # Home Office regional table: compare its supported-person counts with our totals, and its rate
    # (published, or implied from the population it states it used) with ours.
    count_diffs, rate_diffs = [], []
    for r in read_csv("ho-rates-per-10000.csv"):
        if r["date"] != SNAPSHOT:
            continue
        code = harmonise(r["la_code_published"].strip()) if r["la_code_published"].strip() else names.get(norm(r["la_name_published"]))
        if code not in by_code or not r["supported_asylum_seekers"].strip():
            continue
        theirs = int(r["supported_asylum_seekers"])
        ours = by_code[code]["total_asylum_support"]
        count_diffs.append((abs((ours or 0) - theirs), code, ours, theirs))
        if r["rate_per_10000_published"].strip():
            their_rate = float(r["rate_per_10000_published"])
        elif r["population_used"].strip():
            their_rate = theirs / int(r["population_used"]) * 10000
        else:
            continue
        if by_code[code]["total_per_10000"]:
            rate_diffs.append((abs(float(by_code[code]["total_per_10000"]) - their_rate), code))
    summary = {
        "generated_by": "research/build_asylum_geography.py", "reporting_date": SNAPSHOT,
        "population_mid_year_latest": latest_year, "review_status": REVIEW,
        "population_mid_years_used": {str(y): sum(1 for v in snapshot_years.values() if v == y)
                                      for y in sorted(set(snapshot_years.values()))},
        "split_approximations": SPLIT_PRIMARY,
        "terminology": "People receiving asylum support; not a count of small-boat arrivals.",
        "local_authorities": len(lookup),
        "local_authorities_present_in_source": len(present[SNAPSHOT]),
        "local_authorities_with_dispersal": sum(1 for r in dispersal_rows if r["has_dispersal"]),
        "uk_totals_from_local_authorities": {c: sum(r[c] or 0 for r in snapshot_rows) for c in CATEGORY_ORDER}
        | {"total": sum(r["total_asylum_support"] or 0 for r in snapshot_rows)},
        "top20_total_absolute": top(by_total, "total_asylum_support"),
        "top20_total_per_10000": top(by_total_rate, "total_per_10000"),
        "top20_dispersal_absolute": top(by_abs, "dispersal"),
        "top20_dispersal_per_10000": top(by_rate, "dispersal_per_10000"),
        "dispersal_concentration": {
            "share_top10_pct": fmt(sum(r["dispersal"] for r in by_abs[:10]) / uk_dispersal * 100, 2) if uk_dispersal else "",
            "share_top20_pct": fmt(sum(r["dispersal"] for r in by_abs[:20]) / uk_dispersal * 100, 2) if uk_dispersal else "",
            "local_authorities_holding_50pct": las_for.get(50), "local_authorities_holding_80pct": las_for.get(80)},
        "change_rule": f"{BASELINE} vs {SNAPSHOT}; substantial = at least {SUBSTANTIAL_PEOPLE} people and {SUBSTANTIAL_PCT:.0f}%",
        "change_counts": {cat: {k: sum(1 for r in change_rows if r[f"{cat}_category"] == k)
                                for k in ("increased_substantially", "decreased_substantially", "relatively_stable", "not_comparable")}
                          for cat in ("total", "dispersal", "contingency_hotel")},
        "national_reconciliation": reconciliation,
        "coverage_by_quarter": [{"date": d, "categories_by_local_authority": sorted(published_cats[d]),
                                 "unallocated_people": unallocated.get(d, 0)} for d in dates],
        "absence_rule": "Asy_D11 omits local authorities with nobody supported; they are counted as 0 for "
                        "categories broken down by local authority that quarter.",
        "home_office_regional_cross_check": {
            "count_matched": len(count_diffs),
            "count_exact": sum(1 for d in count_diffs if d[0] == 0),
            "largest_count_differences": [{"la_code": c, "ours": o, "home_office": t} for _, c, o, t in sorted(count_diffs, reverse=True)[:5]],
            "rate_matched": len(rate_diffs),
            "max_abs_rate_difference_per_10000": fmt(max(rate_diffs)[0], 3) if rate_diffs else "",
            "note": "Rate differences are expected where the Home Office used a different population estimate."},
    }
    (DATA / "asylum-summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    snap = next(x for x in reconciliation if x["date"] == SNAPSHOT)
    print(f"{len(dates)} quarters {dates[0]}..{dates[-1]}; {len(present[SNAPSHOT])}/{len(lookup)} LAs present at {SNAPSHOT}")
    print(f"snapshot LA sum {snap['local_authority_sum']}, unallocated {snap['unallocated']}, "
          f"national {snap['national_total']}, difference {snap['difference']}")
    print(f"dispersal {uk_dispersal} in {summary['local_authorities_with_dispersal']} LAs; population mid-{latest_year}")


if __name__ == "__main__":
    main()
