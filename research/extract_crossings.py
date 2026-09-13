"""Reproduce Phase 1A crossing statistics from the pinned Home Office ODS; stdlib only.

Run: python3 research/extract_crossings.py
Reads IER_02a (monthly people/boats), IER_02b (nationality), IER_02c (age/sex) and
IER_02d (asylum claims/NRM referrals by arrival year), checks internal consistency,
and writes CSVs under research/crossings/. The workbook is never modified.
This is research preprocessing, not application implementation.
"""
import csv
import json
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "crossings"
SOURCE_ID = "HO-TABLES-2026Q2"
NS = {
    "table": "urn:oasis:names:tc:opendocument:xmlns:table:1.0",
    "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
}
TABLE_NS = "{" + NS["table"] + "}"
MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]
MONTH_END = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
FULL_YEARS = range(2018, 2026)
LATEST_YEAR, LATEST_MONTHS = 2026, 6
REVIEW = "source_checked_pending_independent_review"


def rows(table, width):
    """Yield each row as exactly `width` logical cells, expanding repeated columns."""
    for row in table.findall("table:table-row", NS):
        values = []
        for cell in row:
            if cell.tag not in (TABLE_NS + "table-cell", TABLE_NS + "covered-table-cell"):
                continue
            text = " ".join("".join(p.itertext()) for p in cell.findall(".//text:p", NS))
            repeat = int(cell.get(TABLE_NS + "number-columns-repeated", "1"))
            values.extend([text] * min(repeat, max(0, width - len(values))))
        yield (values + [""] * width)[:width]


def count(text):
    """Parse a published count. Blank and 'z' (not applicable) are unknown, never zero."""
    text = text.strip().replace(",", "")
    return None if text in ("", "z") else int(text)


def ratio(numerator, denominator):
    return None if not denominator or numerator is None else numerator / denominator


def pct_change(new, old):
    return None if new is None or not old else (new - old) / old * 100


def fmt(value):
    return "" if value is None else f"{value:.6f}"


def write_csv(name, records):
    with (OUT / name).open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)


def month_end(year, month):
    leap = month == 2 and year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    return f"{year}-{month:02d}-{MONTH_END[month - 1] + leap:02d}"


def main():
    source = next(s for s in json.loads((ROOT / "sources.json").read_text())["sources"] if s["id"] == SOURCE_ID)
    provenance = {
        "source_id": SOURCE_ID,
        "source_publication_date": source["publication_date"],
        "source_url": source["url"],
        "retrieved_at": source["retrieved_at"],
        "review_status": REVIEW,
    }
    with ZipFile(ROOT / source["local_path"]) as book:
        root = ET.fromstring(book.read("content.xml"))
    tables = {t.get(TABLE_NS + "name"): t for t in root.findall(".//table:table", NS)}
    OUT.mkdir(exist_ok=True)

    # IER_02a: monthly people and boats; totals checked against the published Total column.
    data = list(rows(tables["IER_02a"], 14))
    assert data[4][1:13] == MONTHS
    monthly, annual = {}, {}
    for year in range(2018, LATEST_YEAR + 1):
        covered = LATEST_MONTHS if year == LATEST_YEAR else 12
        pair = {}
        for kind in ("arrivals", "boats"):
            row = next(r for r in data if r[0].startswith(f"{year} {kind}"))
            values = [count(v) for v in row[1:13]]
            assert all(v is not None and v >= 0 for v in values[:covered]), (year, kind)
            assert all(v is None for v in values[covered:]), (year, kind)
            total = count(row[13])
            assert sum(values[:covered]) == total, (year, kind)
            monthly[(year, kind)] = values
            pair[kind] = total
        annual[year] = (pair["arrivals"], pair["boats"], covered)

    # Independent cross-check: the June 2026 narrative's rolling year (July 2025–June 2026).
    for kind, expected in (("arrivals", 33374), ("boats", 511)):
        assert sum(monthly[(2025, kind)][6:]) + sum(monthly[(2026, kind)][:6]) == expected, kind

    # Home Office published averages (whole numbers, narrative releases; see reconcile_series.py).
    # Several releases may repeat a year's figure; they must agree and match our rounded calculation.
    published = {}
    for r in csv.DictReader((OUT / "published-occupancy.csv").open()):
        if r["year_or_period"].isdigit():
            published.setdefault(int(r["year_or_period"]), []).append(r)

    annual_rows = []
    for year, (people, boats, covered) in annual.items():
        releases = published.get(year, [])
        published_value = None
        if releases:
            values = {int(r["published_value"]) for r in releases}
            assert len(values) == 1, (year, values)
            published_value = values.pop()
            assert int(people / boats + 0.5) == published_value, (year, published_value)
        partial = covered < 12
        prior = annual.get(year - 1)
        comparable = prior is not None and not partial
        occupancy = ratio(people, boats)
        annual_rows.append({
            "year": year, "period_start": f"{year}-01-01",
            "period_end": month_end(year, covered),
            "period_type": "calendar_year_to_date" if partial else "calendar_year",
            "months_covered": covered, "people": people, "boats": boats,
            "average_people_per_boat": fmt(occupancy),
            "average_formula": "people / boats",
            # Filled only where the Home Office publishes its own figure; blank is not published.
            "published_average_people_per_boat": "" if published_value is None else published_value,
            "published_average_source_ids": ";".join(sorted({r["source_id"] for r in releases})),
            "people_change_pct": fmt(pct_change(people, prior[0])) if comparable else "",
            "boats_change_pct": fmt(pct_change(boats, prior[1])) if comparable else "",
            "occupancy_change_pct": fmt(pct_change(occupancy, ratio(prior[0], prior[1]))) if comparable else "",
            "change_basis": f"calendar {year} vs calendar {year - 1}" if comparable else "",
            "counts_classification": "OFFICIAL_STATISTIC",
            "derived_classification": "DERIVED_STATISTIC",
            "data_status": "official_statistics_subject_to_revision",
            "source_table": "IER_02a",
            "source_rows": f"{year} arrivals; {year} boats; Total column",
            **provenance,
        })
    write_csv("annual-crossings.csv", annual_rows)

    monthly_rows = []
    for year in range(2018, LATEST_YEAR + 1):
        for m in range(1, 13):
            people, boats = monthly[(year, "arrivals")][m - 1], monthly[(year, "boats")][m - 1]
            if people is None:
                continue  # Months after the pinned cutoff are unpublished, not zero.
            monthly_rows.append({
                "year": year, "month": m, "period_start": f"{year}-{m:02d}-01",
                "period_end": month_end(year, m), "people": people, "boats": boats,
                # A month with no boats has no defined average; left blank, never zero.
                "average_people_per_boat": fmt(ratio(people, boats)),
                "average_formula": "people / boats",
                "counts_classification": "OFFICIAL_STATISTIC",
                "derived_classification": "DERIVED_STATISTIC",
                "data_status": "official_statistics_subject_to_revision",
                "source_table": "IER_02a",
                "source_rows": f"{year} arrivals; {year} boats; {MONTHS[m - 1]} column",
                **provenance,
            })
    write_csv("monthly-crossings.csv", monthly_rows)

    # IER_02b: nationality by period. Rows must sum to the Total row, which must match IER_02a.
    data = list(rows(tables["IER_02b"], 13))
    header = next(i for i, r in enumerate(data) if r[0] == "Nationality")
    periods = data[header][1:11]
    assert periods[:8] == [str(y) for y in FULL_YEARS]
    assert periods[8:] == ["Year ending June 2025", "Year ending June 2026"]
    body = [r for r in data[header + 1:] if r[0]]
    total_row = next(r for r in body if r[0] == "Total")
    totals = [count(v) for v in total_row[1:11]]
    nationality_rows = []
    for r in body:
        if r[0] == "Total":
            continue
        for label, value in zip(periods, r[1:11]):
            nationality_rows.append({"nationality": r[0], "period": label, "people": count(value)})
    for i, label in enumerate(periods):
        assert sum(x["people"] for x in nationality_rows if x["period"] == label) == totals[i], label
    for year in FULL_YEARS:
        assert totals[year - 2018] == annual[year][0], year
    assert totals[9] == 33374
    write_csv("nationality-by-period.csv", [{
        **x, **period_bounds(x["period"]),
        "classification": "OFFICIAL_STATISTIC", "source_table": "IER_02b",
        "note": "Latest recorded nationality at extraction; may be revised (IER_02b notes 12–15).",
        **provenance,
    } for x in nationality_rows])

    # IER_02c: age group and sex. Sex rows sum to their age group; groups sum to Total.
    data = list(rows(tables["IER_02c"], 11))
    header = next(i for i, r in enumerate(data) if r[0] == "Age group and sex")
    assert data[header][1:11] == periods
    body = [r for r in data[header + 1:] if r[0]]
    age_rows, group, group_totals, sex_sums = [], None, {}, {}
    for r in body:
        values = [count(v) for v in r[1:11]]
        if r[0] == "Total":
            assert [sum(t[i] for t in group_totals.values()) for i in range(10)] == values
            continue
        if r[0] in ("Male", "Female", "Unknown"):
            sex_sums[group] = [a + b for a, b in zip(sex_sums[group], values)]
            sex = r[0]
        else:
            group, sex = r[0], "All"
            group_totals[group] = values
            sex_sums[group] = [0] * 10
        for label, value in zip(periods, values):
            age_rows.append({"age_group": group, "sex": sex, "period": label, "people": value})
    for g, values in group_totals.items():
        if g != "Not currently recorded":
            assert sex_sums[g] == values, g
    write_csv("age-sex-by-period.csv", [{
        **x, **period_bounds(x["period"]),
        "classification": "OFFICIAL_STATISTIC", "source_table": "IER_02c",
        "note": "Ages may be revised, e.g. after age assessment (IER_02c note 16).",
        **provenance,
    } for x in age_rows])

    # IER_02d: asylum claims/NRM referrals by arrival year. Categories must sum to total arrivals.
    data = list(rows(tables["IER_02d"], 10))
    header = next(i for i, r in enumerate(data) if r[0] == "Year")
    assert data[header][1:9] == [str(y) for y in FULL_YEARS]
    lookup = {r[0]: [count(v) for v in r[1:9]] for r in data[header + 1:] if r[0]}
    keys = ["with asylum claim only", "with NRM referral only",
            "with an asylum claim and an NRM referral", "with no asylum claim and no NRM referral"]
    claim_rows = []
    for i, year in enumerate(FULL_YEARS):
        parts = [lookup[k][i] for k in keys]
        total = lookup["Total arrivals"][i]
        assert sum(parts) == total, year
        asylum = parts[0] + parts[2]
        claim_rows.append({
            "arrival_year": year, "total_arrivals_matched_table": total,
            "asylum_claim_only": parts[0], "nrm_referral_only": parts[1],
            "asylum_claim_and_nrm_referral": parts[2], "no_asylum_claim_or_nrm_referral": parts[3],
            "people_with_asylum_claim": asylum,
            "asylum_claim_share": fmt(ratio(asylum, total)),
            "asylum_claim_share_formula": "(asylum claim only + asylum claim and NRM referral) / total arrivals in IER_02d",
            "ier_02a_people": annual[year][0],
            "counts_classification": "OFFICIAL_STATISTIC",
            "derived_classification": "DERIVED_STATISTIC",
            "source_table": "IER_02d",
            "note": ("People, not claims; by arrival date; claims within 14 days of arrival. Totals differ "
                     "slightly from IER_02a because of extraction dates (IER_02d notes 17–20)."),
            **provenance,
        })
    write_csv("asylum-claims-by-arrival-year.csv", claim_rows)

    # Highest-occupancy months. Small denominators make monthly averages volatile, so the
    # ranking is limited to months with at least MIN_BOATS boats and reports boats alongside.
    MIN_BOATS = 10
    ranked = sorted((r for r in monthly_rows if r["boats"] >= MIN_BOATS),
                    key=lambda r: float(r["average_people_per_boat"]), reverse=True)
    summary = {
        "generated_by": "research/extract_crossings.py",
        "source_id": SOURCE_ID,
        "review_status": REVIEW,
        "highest_occupancy_months": {
            "rule": f"Months with at least {MIN_BOATS} boats, ranked by people / boats.",
            "classification": "DERIVED_STATISTIC",
            "months": [{k: r[k] for k in ("year", "month", "people", "boats", "average_people_per_boat")}
                       for r in ranked[:10]],
        },
        "highest_occupancy_month_by_year": [
            {k: r[k] for k in ("year", "month", "people", "boats", "average_people_per_boat")}
            for year in range(2018, LATEST_YEAR + 1)
            for r in [max((x for x in monthly_rows if x["year"] == year and x["boats"] >= MIN_BOATS),
                          key=lambda x: float(x["average_people_per_boat"]), default=None)] if r
        ],
    }
    (OUT / "crossings-summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    for row in annual_rows:
        print(row["year"], row["people"], row["boats"], row["average_people_per_boat"][:5], row["period_type"])
    print(f"Verified {len(annual) * 2} monthly sums, the rolling-year cross-check, "
          f"{len(periods)} nationality and age/sex period totals, and {len(claim_rows)} IER_02d category sums.")


def period_bounds(label):
    if label.isdigit():
        return {"period_start": f"{label}-01-01", "period_end": f"{label}-12-31", "period_type": "calendar_year"}
    year = int(label[-4:])
    return {"period_start": f"{year - 1}-07-01", "period_end": f"{year}-06-30", "period_type": "year_ending_june"}


if __name__ == "__main__":
    main()
