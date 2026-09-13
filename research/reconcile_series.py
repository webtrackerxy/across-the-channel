"""Reconcile the pinned annual small-boat series across Home Office vintages and
compare published average-people-per-boat figures with calculated values.

Standard library only. Run: python3 research/reconcile_series.py
Writes annual-series-vintages.csv and published-occupancy.csv next to this script.

Published averages are transcribed from Home Office narrative releases and the
Border Security Commander's report (retrieved 11 September 2026 via the GOV.UK
content API); calculated values use the pinned June 2026 IER_02a monthly data.
"""
import csv
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZipFile

HERE = Path(__file__).resolve().parent
RAW = HERE / "raw"
OUT = HERE / "crossings"
NS = {"table": "urn:oasis:names:tc:opendocument:xmlns:table:1.0",
      "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0"}
T = "{" + NS["table"] + "}"

# (source_id, publication_date, file, sheet)
VINTAGES = [
    ("HO-TABLES-2021Q4", "2022-02-24", "irregular-migration-to-the-uk-data-tables-year-ending-december-2021.ods", "Irr_02a"),
    ("HO-TABLES-2022Q4", "2023-02-23", "irregular-migration-to-the-UK-summary-tables-year-ending-December-2022.ods", "Irr_02a"),
    ("HO-TABLES-2024Q4", "2025-02-27", "irregular-migration-to-the-uk-summary-dec-2024.ods", "Irr_02a"),
    ("HO-TABLES-2025Q4", "2026-02-26", "illegal-entry-routes-to-the-uk-summary-dec-2025-tables.ods", "IER_02a"),
    ("HO-TABLES-2026Q1", "2026-05-21", "illegal-entry-routes-to-the-uk-summary-mar-2026-tables.ods", "IER_02a"),
    ("HO-TABLES-2026Q2", "2026-08-27", "illegal-entry-routes-to-the-uk-summary-jun-2026-tables.ods", "IER_02a"),
]
PINNED = "HO-TABLES-2026Q2"

# Figures stated in text rather than tables (retrieved and read 11 September 2026).
EXTERNAL = [
    ("ICIBI-DOVER-2022-REPORT", "2022-07-21", "ICIBI report, paragraph 4.1 Figure 1 'Number of migrant arrivals via a small boat' (footnote 5: calendar year); no data source stated",
     {2018: 286, 2019: 1834, 2020: 8486, 2021: 28526}),
    ("ICIBI-DOVER-2022-REPORT", "2022-07-21", "ICIBI report, paragraph 2.1 Summary of conclusions: 'increased from 236 in 2018 to 28,526 in 2021'",
     {2018: 236, 2021: 28526}),
    ("ICIBI-DOVER-2022", "2022-07-21", "ICIBI press notice body: '28,526 ... in 2021 ... a significant increase from 236 in 2018', attributed to 'Home Office statistics'",
     {2018: 236, 2021: 28526}),
    ("HOCL-CBP-10590", "2026-09-02", "Commons Library CBP-10590 summary (data.parliament.uk research-briefings API abstract): 299 in 2018; peak 'around 46,000' in 2022; 'rising again to 41,000 in 2025' (rounded)",
     {2018: 299, 2022: 46000, 2025: 41000}),
]

# Published averages: (period label, start, end, value, source_id, locator, publication date, notes)
PUBLISHED = [
    ("2018", "2018-01-01", "2018-12-31", 7, "HO-2021-NARRATIVE", "Irregular migration to the UK, YE Dec 2021: text before Chart 2 ('2018 (7 people)')", "2022-02-24", ""),
    ("2018", "2018-01-01", "2018-12-31", 7, "HO-2022-NARRATIVE", "Irregular migration to the UK, YE Dec 2022: 'Number of boats and people per boat', text after Figure 3", "2023-02-23", ""),
    ("2018", "2018-01-01", "2018-12-31", 7, "HO-2023-NARRATIVE", "Irregular migration to the UK, YE Dec 2023: 'Number of boats and people per boat', text after Figure 4 ('only 7 per boat in 2018')", "2024-02-29", ""),
    ("2018", "2018-01-01", "2018-12-31", 7, "HO-2026Q2", "Illegal entry routes YE Jun 2026: section 2.2, text after Figure 3 ('7 people per boat in the YE December 2018')", "2026-08-27", ""),
    ("2019", "2019-01-01", "2019-12-31", 11, "HO-2021-NARRATIVE", "Irregular migration to the UK, YE Dec 2021: text before Chart 2 ('2019 (11 people)')", "2022-02-24", ""),
    ("2019", "2019-01-01", "2019-12-31", 11, "HO-2022-NARRATIVE", "Irregular migration to the UK, YE Dec 2022: 'Number of boats and people per boat'", "2023-02-23", ""),
    ("2020", "2020-01-01", "2020-12-31", 13, "HO-2021-NARRATIVE", "Irregular migration to the UK, YE Dec 2021: text before Chart 2 ('2020 (13 people per small boat)')", "2022-02-24", ""),
    ("2020", "2020-01-01", "2020-12-31", 13, "HO-2022-NARRATIVE", "Irregular migration to the UK, YE Dec 2022: 'Number of boats and people per boat'", "2023-02-23", ""),
    ("2020", "2020-01-01", "2020-12-31", 13, "HO-2023-NARRATIVE", "Irregular migration to the UK, YE Dec 2023: 'Number of boats and people per boat' ('only 13 in 2020')", "2024-02-29", ""),
    ("2021", "2021-01-01", "2021-12-31", 28, "HO-2021-NARRATIVE", "Irregular migration to the UK, YE Dec 2021: text before Chart 2 ('In 2021, there were an average of 28 people per small boat')", "2022-02-24", ""),
    ("2021", "2021-01-01", "2021-12-31", 28, "HO-2022-NARRATIVE", "Irregular migration to the UK, YE Dec 2022: 'Number of boats and people per boat'", "2023-02-23", ""),
    ("2021", "2021-01-01", "2021-12-31", 28, "HO-2024-NARRATIVE", "How many people come to the UK irregularly?, YE Dec 2024: 'Number of boats and people per boat' ('compared to 28 in 2021')", "2025-02-27", ""),
    ("2022", "2022-01-01", "2022-12-31", 41, "HO-2022-NARRATIVE", "Irregular migration to the UK, YE Dec 2022: text after Figure 3 ('In 2022, there was an average of 41 people per small boat')", "2023-02-23", "Contemporaneous vintage counted 45,755 people and 1,109 boats for 2022 (later revised to 45,774 and 1,110)."),
    ("2022", "2022-01-01", "2022-12-31", 41, "HO-2023-NARRATIVE", "Irregular migration to the UK, YE Dec 2023: 'Number of boats and people per boat'", "2024-02-29", ""),
    ("2022", "2022-01-01", "2022-12-31", 41, "HO-2025", "Illegal entry routes YE Dec 2025: section 2.2 ('41 in YE December 2022')", "2026-02-26", ""),
    ("2022", "2022-01-01", "2022-12-31", 41, "HO-2026Q1-NARRATIVE", "Illegal entry routes YE Mar 2026: section 2.2 ('41 in the YE December 2022')", "2026-05-21", "Page updated 16 July 2026."),
    ("2023", "2023-01-01", "2023-12-31", 49, "HO-2023-NARRATIVE", "Irregular migration to the UK, YE Dec 2023: 'Number of boats and people per boat' ('49 people per boat in 2023')", "2024-02-29", ""),
    ("2023", "2023-01-01", "2023-12-31", 49, "HO-2024-NARRATIVE", "How many people come to the UK irregularly?, YE Dec 2024: 'Number of boats and people per boat' ('49 people per boat in 2023')", "2025-02-27", ""),
    ("2024", "2024-01-01", "2024-12-31", 53, "HO-2024-NARRATIVE", "How many people come to the UK irregularly?, YE Dec 2024: 'Number of boats and people per boat' ('53 people per boat in 2024')", "2025-02-27", ""),
    ("2024", "2024-01-01", "2024-12-31", 53, "HO-2025", "Illegal entry routes YE Dec 2025: section 2.2 ('53 people per boat in YE December 2024')", "2026-02-26", ""),
    ("2025", "2025-01-01", "2025-12-31", 62, "HO-2025", "Illegal entry routes YE Dec 2025: section 2.2 ('62 people per boat in YE December 2025')", "2026-02-26", ""),
    ("2026 January-June", "2026-01-01", "2026-06-30", None, "", "No published figure found", "", "Not published in any source reviewed (IER_02a has no average column; June 2026 narrative gives only the rolling YE June 2026 figure). Partial year; do not compare with full years."),
    ("Aug-Oct 2022", "2022-08-01", "2022-10-31", 45, "HO-2022-NARRATIVE", "Irregular migration to the UK, YE Dec 2022: 'Number of boats and people per boat' ('average of 45 people per small boat in these 3 months'; 518 boats)", "2023-02-23", "Contemporaneous vintage had 179 September 2022 boats (pinned: 180) and different Jul-Sep 2022 people figures."),
    ("YE Mar 2022", "2021-04-01", "2022-03-31", 29, "HO-2025Q1-NARRATIVE", "How many people come to the UK irregularly?, YE Mar 2025: 'Number of boats and people per boat' ('54 compared to 29 in the same period ending March 2022')", "2025-05-22", "Page updated 25 June 2025."),
    ("YE Mar 2024", "2023-04-01", "2024-03-31", 50, "HO-2025Q1-NARRATIVE", "How many people come to the UK irregularly?, YE Mar 2025: 'Number of boats and people per boat' ('compared with 50 people per boat in the previous year')", "2025-05-22", "Page updated 25 June 2025."),
    ("YE Mar 2024", "2023-04-01", "2024-03-31", 54, "HO-2026Q1-NARRATIVE", "Illegal entry routes YE Mar 2026: section 2.2 ('54 people per boat in the YE March 2024')", "2026-05-21", "CONFLICT: does not match the calculation (49.7) or the Home Office's own YE Mar 2025 release (50 for YE Mar 2024). 54 matches YE Mar 2025, so this is probably a labelling error. Do not use."),
    ("YE Mar 2025", "2024-04-01", "2025-03-31", 54, "HO-2025Q1-NARRATIVE", "How many people come to the UK irregularly?, YE Mar 2025: 'Number of boats and people per boat' ('54 people per boat in the year ending March 2025')", "2025-05-22", "Page updated 25 June 2025. Jan-Mar 2025 later revised (IER note 5)."),
    ("YE Jun 2024", "2023-07-01", "2024-06-30", 51, "HO-2025Q2-NARRATIVE", "How many people come to the UK irregularly?, YE Jun 2025: section 'Number of boats and people per boat' ('51 people per boat in the year ending June 2024')", "2025-08-21", "Page updated 20 October 2025."),
    ("YE Jun 2025", "2024-07-01", "2025-06-30", 56, "HO-2025Q2-NARRATIVE", "How many people come to the UK irregularly?, YE Jun 2025: 'Number of boats and people per boat' ('56 people per boat in the year ending June 2025')", "2025-08-21", "Jan-Jun 2025 data later revised (IER note 5)."),
    ("YE Jun 2025", "2024-07-01", "2025-06-30", 56, "HO-2026Q2", "Illegal entry routes YE Jun 2026: section 2.2 ('56 people per boat in the YE June 2025')", "2026-08-27", ""),
    ("June 2025 (month)", "2025-06-01", "2025-06-30", 65, "HO-2025Q2-NARRATIVE", "How many people come to the UK irregularly?, YE Jun 2025: 'The month of June 2025 saw an average of 65 people per boat'", "2025-08-21", "Described then as the highest monthly average on record."),
    ("September 2025 (month)", "2025-09-01", "2025-09-30", 71, "HO-2025", "Illegal entry routes YE Dec 2025: section 2.2 ('September and November ... 71 people per boat, the highest monthly average on record')", "2026-02-26", "Repeated in YE Mar 2026 and YE Jun 2026 narratives."),
    ("November 2025 (month)", "2025-11-01", "2025-11-30", 71, "HO-2025", "Illegal entry routes YE Dec 2025: section 2.2 ('September and November ... 71 people per boat')", "2026-02-26", "Repeated in YE Mar 2026 and YE Jun 2026 narratives."),
    ("YE Mar 2026", "2025-04-01", "2026-03-31", 63, "HO-2026Q1-NARRATIVE", "Illegal entry routes YE Mar 2026: section 2.2 ('63 people per boat in the YE March 2026')", "2026-05-21", "Page updated 16 July 2026."),
    ("FY 2025/26", "2025-04-01", "2026-03-31", 63, "BSC-2026", "Border Security Commander's annual report 2025 to 2026 (accessible HTML), section 'Impact of interventions in France and near neighbours' ('reaching a high of 63 in 2025/26'), footnote 35 cites the HO illegal entry routes release", "2026-07-16", "Financial year assumed April-March (same span as YE March 2026). Not an independent measurement."),
    ("YE Jun 2026", "2025-07-01", "2026-06-30", 65, "HO-2026Q2", "Illegal entry routes YE Jun 2026: section 2.2 ('65 people per boat in the YE June 2026')", "2026-08-27", ""),
]


def ods_rows(path, sheet):
    root = ET.fromstring(ZipFile(path).read("content.xml"))
    table = next(t for t in root.iter(T + "table") if t.get(T + "name") == sheet)
    for row in table.iter(T + "table-row"):
        vals = []
        for cell in row:
            if cell.tag not in (T + "table-cell", T + "covered-table-cell"):
                continue
            text = " ".join("".join(p.itertext()) for p in cell.findall(".//text:p", NS)).strip()
            vals.extend([text] * min(int(cell.get(T + "number-columns-repeated", "1")), max(0, 14 - len(vals))))
        yield (vals + [""] * 14)[:14]


def annual_series(path, sheet):
    """Return {(year, 'people'|'boats'): (total, [12 monthly values or None])} for either layout."""
    out, section = {}, None
    for row in ods_rows(path, sheet):
        first = row[0]
        low = first.lower()
        if low.startswith("total arrivals"):
            section = "people"
            continue
        if low.startswith("total incidents") or low.startswith("total boats"):
            section = "boats"
            continue
        m = re.match(r"^(\d{4})\s*(arrivals|boats)?", first)
        if not m or not row[13]:
            continue
        kind = {"arrivals": "people", "boats": "boats"}.get(m.group(2), section)
        months = [int(v.replace(",", "")) if v else None for v in row[1:13]]
        total = int(row[13].replace(",", ""))
        assert sum(v for v in months if v is not None) == total, (path.name, first, kind)
        out[(int(m.group(1)), kind)] = (total, months)
    return out


def main():
    series = {sid: annual_series(RAW / f, sheet) for sid, _, f, sheet in VINTAGES}
    pinned = series[PINNED]
    rows = []
    for sid, pub, f, sheet in VINTAGES:
        for year in range(2018, 2026):
            if (year, "people") not in series[sid]:
                continue
            p, b = series[sid][(year, "people")][0], series[sid][(year, "boats")][0]
            pp, pb = pinned[(year, "people")][0], pinned[(year, "boats")][0]
            monthly_same = all(series[sid][(year, k)][1] == pinned[(year, k)][1] for k in ("people", "boats"))
            rows.append({"source_id": sid, "publication_date": pub, "table": sheet, "locator": f"{sheet} {year} annual Total (monthly sums verified)",
                         "year": year, "people": p, "boats": b, "pinned_people": pp, "pinned_boats": pb,
                         "diff_people": p - pp, "diff_boats": b - pb, "monthly_values_identical_to_pinned": monthly_same,
                         "kind": "official_table"})
    for sid, pub, loc, values in EXTERNAL:
        for year, p in values.items():
            pp = pinned[(year, "people")][0]
            rows.append({"source_id": sid, "publication_date": pub, "table": "", "locator": loc, "year": year, "people": p,
                         "boats": "", "pinned_people": pp, "pinned_boats": pinned[(year, "boats")][0],
                         "diff_people": p - pp, "diff_boats": "", "monthly_values_identical_to_pinned": "",
                         "kind": "text_figure"})
    with (OUT / "annual-series-vintages.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    def calc(start, end):
        y0, m0 = int(start[:4]), int(start[5:7])
        y1, m1 = int(end[:4]), int(end[5:7])
        people = boats = 0
        y, m = y0, m0
        while (y, m) <= (y1, m1):
            vp, vb = pinned[(y, "people")][1][m - 1], pinned[(y, "boats")][1][m - 1]
            assert vp is not None and vb is not None, (y, m)
            people, boats = people + vp, boats + vb
            y, m = (y + 1, 1) if m == 12 else (y, m + 1)
        return people, boats

    out = []
    for label, start, end, value, sid, loc, pub, notes in PUBLISHED:
        people, boats = calc(start, end)
        avg = people / boats
        rounded = int(avg + 0.5)
        out.append({"year_or_period": label, "period_start": start, "period_end": end,
                    "published_value": "" if value is None else value, "source_id": sid, "locator": loc,
                    "publication_date": pub, "calculated_people": people, "calculated_boats": boats,
                    "calculated_people_per_boat": f"{avg:.6f}", "calculated_rounded": rounded,
                    "matches_published_after_rounding": "" if value is None else rounded == value,
                    "calculation_source": "HO-TABLES-2026Q2 IER_02a monthly values; people / boats over the same months",
                    "notes": notes})
    with (OUT / "published-occupancy.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    for r in rows:
        if r["diff_people"] or r["diff_boats"] or r["monthly_values_identical_to_pinned"] is False:
            print("DIFF", r["source_id"], r["year"], r["people"], r["boats"], r["diff_people"], r["diff_boats"], r["monthly_values_identical_to_pinned"])
    for r in out:
        print(r["year_or_period"], r["published_value"], r["source_id"], r["calculated_people_per_boat"], r["matches_published_after_rounding"])


if __name__ == "__main__":
    main()
