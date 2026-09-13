"""Asylum claims and initial decisions for small-boat arrivals, by arrival year.

Standard library only. Reads the pinned Home Office "Illegal entry routes to the
UK detailed dataset, year ending June 2026" (XLSX, published 27 August 2026),
sheets Data_IER_D02 and Data_IER_D03, and writes
asylum-decisions-by-arrival-year.csv next to this script.

Run: python3 research/extract_decisions.py

Definitions (Home Office, detailed dataset Notes sheet and List_of_Fields):
- Figures count PEOPLE (main applicants and dependants), not asylum claims
  (note 18). Rows with applicant type "Main applicant" are also summed
  separately to give case-level (main applicant) counts.
- Periods are by date of small-boat ARRIVAL, not claim or decision date
  (notes 19, 25). Only claims made within 14 days of arrival are included.
- IER_D03 shows the first outcome (initial decision) as at extraction. For
  2023-2025 arrivals decisions are included up to 15 July 2026; pre-2023 data
  were not revised in this release (note 24).
- Outcome groups: Grant of Protection, Grant of Other Leave, Refused,
  Withdrawn, Administrative Outcome, plus "Awaiting initial decision".
- Home Office grant rate: "the percentage of claims that resulted in a grant
  of protection or some form of leave at initial decision, excluding
  withdrawn claims and claims which received an administrative outcome"
  (YE March 2026 chapter "How many small boat arrivals have claimed asylum
  or been referred to the National Referral Mechanism?"), i.e.
  (protection + other leave) / (protection + other leave + refused).
"""
import csv
import re
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from zipfile import ZipFile

HERE = Path(__file__).resolve().parent
RESEARCH = HERE
XLSX = RESEARCH / "raw" / "illegal-entry-routes-to-the-uk-detailed-dataset-jun-2026.xlsx"
SUMMARY_ODS = RESEARCH / "raw" / "illegal-entry-routes-to-the-uk-summary-jun-2026-tables.ods"
OUT = HERE / "crossings" / "asylum-decisions-by-arrival-year.csv"
SOURCE_ID = "HO-IER-DETAILED-2026Q2"
SOURCE_URL = "https://assets.publishing.service.gov.uk/media/6a85c41d3d82f78d5c514551/illegal-entry-routes-to-the-uk-dataset-jun-2026.xlsx"
YEARS = list(range(2018, 2026))

M = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
GROUPS = ["Grant of Protection", "Grant of Other Leave", "Refused", "Withdrawn",
          "Administrative Outcome", "Awaiting initial decision"]


def col_letters(ref):
    return re.match(r"[A-Z]+", ref).group(0)


class Workbook:
    def __init__(self, path):
        self.zip = ZipFile(path)
        self.strings = ["".join(t.text or "" for t in si.iter(M + "t"))
                        for si in ET.fromstring(self.zip.read("xl/sharedStrings.xml")).iter(M + "si")]
        rels = {r.get("Id"): r.get("Target")
                for r in ET.fromstring(self.zip.read("xl/_rels/workbook.xml.rels"))}
        self.sheets = {}
        for s in ET.fromstring(self.zip.read("xl/workbook.xml")).iter(M + "sheet"):
            target = rels[s.get(R + "id")]
            self.sheets[s.get("name")] = target.lstrip("/") if target.startswith("/") else "xl/" + target

    def rows(self, name):
        """Yield each row as {column letter: text value}."""
        for _, el in ET.iterparse(self.zip.open(self.sheets[name])):
            if el.tag != M + "row":
                continue
            row = {}
            for c in el.findall(M + "c"):
                v = c.find(M + "v")
                if c.get("t") == "s" and v is not None:
                    val = self.strings[int(v.text)]
                elif c.get("t") == "inlineStr":
                    val = "".join(x.text or "" for x in c.iter(M + "t"))
                else:
                    val = v.text if v is not None else ""
                row[col_letters(c.get("r"))] = val
            yield row
            el.clear()

    def records(self, name):
        """Yield dicts keyed by the header row (row 2 of each Data_ sheet)."""
        header = None
        for i, row in enumerate(self.rows(name)):
            if i == 1:
                header = {k: v.strip() for k, v in row.items()}
            elif i > 1 and row:
                yield {header[k]: v for k, v in row.items() if k in header}


def as_count(text):
    value = float(text)
    assert value >= 0 and value == int(value), text
    return int(value)


def ods_ier02d_totals(path):
    """Matched small-boat arrivals by year from summary table IER_02d (cross-check only)."""
    ns = {"table": "urn:oasis:names:tc:opendocument:xmlns:table:1.0",
          "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0"}
    t = "{" + ns["table"] + "}"
    root = ET.fromstring(ZipFile(path).read("content.xml"))
    table = next(x for x in root.iter(t + "table") if x.get(t + "name") == "IER_02d")
    rows = []
    for row in table.iter(t + "table-row"):
        vals = []
        for cell in row:
            text = " ".join("".join(p.itertext()) for p in cell.findall(".//text:p", ns))
            vals.extend([text] * min(int(cell.get(t + "number-columns-repeated", "1")), 12))
        rows.append(vals)
    header = next(r for r in rows if r and r[0] == "Year")
    out = {}
    for label in ("Total arrivals", "with asylum claim only", "with an asylum claim and an NRM referral"):
        row = next(r for r in rows if r and r[0] == label)
        out[label] = {int(header[i]): int(row[i].replace(",", "")) for i in range(1, 9)}
    return out


def pct(num, den):
    return "" if not den else f"{100 * num / den:.4f}"


def main():
    wb = Workbook(XLSX)
    cover = [r.get("A", "") for r in wb.rows("Cover_sheet")]
    assert "Illegal Entry Routes - Detailed Datasets" in cover and "Published: 27 August 2026" in cover, cover

    claims = Counter()          # (year, raised?) people
    claims_main = Counter()     # (year) main applicants with a claim
    for rec in wb.records("Data_IER_D02"):
        year = int(rec["Year"])
        n = as_count(rec["Arrivals"])
        raised = rec["Asylum claim"] == "Asylum claim raised"
        assert raised or rec["Asylum claim"] == "No asylum claim raised", rec
        claims[(year, raised)] += n
        if raised and rec["Applicant type"].strip().lower() == "main applicant":
            claims_main[year] += n

    outcomes = Counter()        # (year, group) people
    outcomes_main = Counter()   # (year, group) main applicants
    for rec in wb.records("Data_IER_D03"):
        year = int(rec["Year"])
        group = rec["Asylum Case Outcome Group"]
        assert group in GROUPS, group
        n = as_count(rec["Outcomes"])
        outcomes[(year, group)] += n
        if rec["Applicant type"].strip().lower() == "main applicant":
            outcomes_main[(year, group)] += n

    assert {y for y, _ in claims} == set(YEARS), sorted({y for y, _ in claims})
    ier02d = ods_ier02d_totals(SUMMARY_ODS)

    rows = []
    for year in YEARS + ["2018-2025"]:
        ys = YEARS if year == "2018-2025" else [year]
        g = {k: sum(outcomes[(y, k)] for y in ys) for k in GROUPS}
        gm = {k: sum(outcomes_main[(y, k)] for y in ys) for k in GROUPS}
        with_claim = sum(claims[(y, True)] for y in ys)
        without = sum(claims[(y, False)] for y in ys)
        main_claims = sum(claims_main[y] for y in ys)
        # Every person with a claim in D02 appears once in D03 (decided or awaiting).
        assert sum(g.values()) == with_claim, (year, sum(g.values()), with_claim)
        assert sum(gm.values()) == main_claims, (year, sum(gm.values()), main_claims)
        if year != "2018-2025":
            # Cross-check against the summary table IER_02d (same release).
            assert with_claim + without == ier02d["Total arrivals"][year], year
            assert with_claim == (ier02d["with asylum claim only"][year]
                                  + ier02d["with an asylum claim and an NRM referral"][year]), year
        grants = g["Grant of Protection"] + g["Grant of Other Leave"]
        grants_m = gm["Grant of Protection"] + gm["Grant of Other Leave"]
        substantive = grants + g["Refused"]
        substantive_m = grants_m + gm["Refused"]
        all_outcomes = substantive + g["Withdrawn"] + g["Administrative Outcome"]
        start = f"{ys[0]}-01-01"
        end = f"{ys[-1]}-12-31"
        rows.append({
            "arrival_year": year,
            "period_start": start,
            "period_end": end,
            "period_basis": "date of small-boat arrival (calendar year); claims made within 14 days of arrival; outcome = first (initial) decision as at extraction",
            "decision_cutoff": ("decisions up to 15 July 2026 (note 24)" if isinstance(year, int) and year >= 2023
                                else "pre-2023 arrivals not revised in this release; extraction date not stated (note 24)" if isinstance(year, int)
                                else "mixed: 2018-2022 not revised in this release; 2023-2025 decisions up to 15 July 2026"),
            "count_unit": "people (main applicants and dependants)",
            "small_boat_arrivals_matched": with_claim + without,
            "people_with_asylum_claim": with_claim,
            "people_without_asylum_claim": without,
            "asylum_claim_share_pct": pct(with_claim, with_claim + without),
            "grant_of_protection": g["Grant of Protection"],
            "grant_of_other_leave": g["Grant of Other Leave"],
            "grants_total": grants,
            "refused": g["Refused"],
            "withdrawn": g["Withdrawn"],
            "administrative_outcome": g["Administrative Outcome"],
            "awaiting_initial_decision": g["Awaiting initial decision"],
            "substantive_initial_decisions": substantive,
            "all_initial_outcomes": all_outcomes,
            "grant_rate_ho_definition_pct": pct(grants, substantive),
            "grant_rate_ho_formula": "(grant_of_protection + grant_of_other_leave) / (grant_of_protection + grant_of_other_leave + refused); excludes withdrawn and administrative outcomes (Home Office definition)",
            "grant_share_of_all_outcomes_pct": pct(grants, all_outcomes),
            "grant_share_of_all_outcomes_formula": "grants_total / (grants_total + refused + withdrawn + administrative_outcome); NOT the Home Office grant rate",
            "decided_share_of_claims_pct": pct(substantive, with_claim),
            "decided_share_formula": "substantive_initial_decisions / people_with_asylum_claim (Home Office 'received an initial decision (% of claims)' counts grants + refusals only)",
            "main_applicant_claims": main_claims,
            "main_applicant_grants": grants_m,
            "main_applicant_refused": gm["Refused"],
            "main_applicant_withdrawn_or_admin": gm["Withdrawn"] + gm["Administrative Outcome"],
            "main_applicant_awaiting": gm["Awaiting initial decision"],
            "main_applicant_grant_rate_ho_definition_pct": pct(grants_m, substantive_m),
            "counts_classification": "OFFICIAL_STATISTIC",
            "rates_classification": "DERIVED_STATISTIC",
            "source_id": SOURCE_ID,
            "source_url": SOURCE_URL,
            "source_publication_date": "2026-08-27",
            "table": "IER_D02; IER_D03",
            "locator": ("Data_IER_D02 (columns Year, Asylum claim, Applicant type, Arrivals) summed by Year; "
                        "Data_IER_D03 (columns Year, Asylum Case Outcome Group, Applicant type, Outcomes) summed by Year and outcome group"),
            "notes": ("Counts people not claims; arrival-date cohorts; outcomes may change on appeal or reconsideration; "
                      "matched records only (note 23), so totals differ slightly from IER_02a arrivals; "
                      "2023-2025 revised in this release (note 22); deceased outcomes 2023 Q1-2025 Q4 revised (note 26)."),
        })

    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    for r in rows:
        print(r["arrival_year"], r["people_with_asylum_claim"], r["grants_total"], r["refused"], r["withdrawn"],
              r["administrative_outcome"], r["awaiting_initial_decision"], r["grant_rate_ho_definition_pct"],
              r["main_applicant_grant_rate_ho_definition_pct"])
    print("Checks passed: D03 outcomes sum to D02 claims (people and main applicants); D02 totals match IER_02d.")


if __name__ == "__main__":
    main()
