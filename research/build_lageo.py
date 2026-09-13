#!/usr/bin/env python3
"""Phase 1B local-authority geography and population build (standard library only).

Reads pinned source files in research/raw/ (see manifest-entries.json) and writes,
inside research/asylum/:

  uk-local-authorities.geojson  ONS LAD (May 2026) BUC boundaries, WGS84, 5 dp
  la-lookup.csv                 one row per LAD in the May 2026 vintage
  la-code-changes.csv           LAD code/boundary changes 2022-01-01..2026-06-30 (ONS CHD)
  population.csv                mid-year estimates 2021-2025 as published (ONS/NRS/NISRA)
  manifest-entries.json         SHA-256 of every raw file used
  build-report.json             checks and cross-checks

Run:  python3 research/build_lageo.py
"""
import csv
import datetime
import hashlib
import io
import json
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
RESEARCH = HERE
OUT = os.path.join(RESEARCH, "asylum")
RAW = os.path.join(RESEARCH, "raw")
RETRIEVED = "2026-09-11"

BOUNDARY_VINTAGE = "May 2026"
WINDOW = (datetime.date(2022, 1, 1), datetime.date(2026, 6, 30))
LAD_ENTITIES = ("E06", "E07", "E08", "E09", "W06", "S12", "N09")
YEARS = range(2021, 2026)

# Source IDs (see sources.json in this folder)
S_BUC = "LAGEO-ONS-LAD-MAY2026-BUC"
S_LU = "LAGEO-ONS-WD26-LU-MAY2026"
S_LU25 = "LAGEO-ONS-LAD25-RGN25-LU"
S_DEC25 = "LAGEO-ONS-LAD-DEC2025-BUC"
S_CHD = "LAGEO-ONS-CHD-JUN2026"
S_SI1328 = "LAGEO-UKSI-2024-1328"
S_BFE = "LAGEO-ONS-LAD-BFE-AREAS"
S_EW25 = "LAGEO-ONS-MYE-EW-MID2025"
S_EWTS = "LAGEO-ONS-MYEB-EW-2011-2025"
S_UK24 = "LAGEO-ONS-MYE-UK-MID2024"
S_NRS25 = "LAGEO-NRS-MYE-MID2025"
S_NRSTS = "LAGEO-NRS-MYE-TIMESERIES-2025"
S_NISRA24 = "LAGEO-NISRA-MYE-MID2024"
S_NISRA25 = "LAGEO-NISRA-MYE-MID2025-ANNOUNCEMENT"
S_ONSLIC = "LAGEO-ONS-GEOGRAPHY-LICENCES"
S_NISRALIC = "LAGEO-NISRA-CROWN-COPYRIGHT"
S_ONSUKPAGE = "LAGEO-ONS-MYE-UK-DATASET-PAGE"
S_ONSEWPAGE = "LAGEO-ONS-MYE-EW-DATASET-PAGE"

ONS_FILE = "https://www.ons.gov.uk/file?uri=/peoplepopulationandcommunity/populationandmigration/populationestimates/datasets/"
ARC = "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/"
ITEM = "https://www.arcgis.com/sharing/rest/content/items/"

# file in raw/, source_id, url, status
RAW_FILES = [
    ("lageo-ons-lad-may2026-uk-buc.geojson", S_BUC,
     "https://hub.arcgis.com/api/download/v1/items/fe180cafba734c6c8c5ad41ee960d30b/geojson?redirect=true&layers=0",
     "downloaded_and_inspected"),
    ("lageo-arcgis-item-fe180cafba734c6c8c5ad41ee960d30b.json", S_BUC,
     ITEM + "fe180cafba734c6c8c5ad41ee960d30b?f=json", "downloaded_and_inspected"),
    ("lageo-ons-wd26-lad26-ctyua26-rgn26-ctry26-uk-lu.csv", S_LU,
     "https://hub.arcgis.com/api/download/v1/items/79e0950fa93446b996d0f3f95537ab6d/csv?redirect=true&layers=0",
     "downloaded_and_inspected"),
    ("lageo-arcgis-item-79e0950fa93446b996d0f3f95537ab6d.json", S_LU,
     ITEM + "79e0950fa93446b996d0f3f95537ab6d?f=json", "downloaded_and_inspected"),
    ("lageo-ons-lad25-rgn25-en-lu-v2.csv", S_LU25,
     "https://hub.arcgis.com/api/download/v1/items/1c17a07ff8fc44218883049f0afa3de1/csv?redirect=true&layers=0",
     "downloaded_and_inspected"),
    ("lageo-arcgis-item-1c17a07ff8fc44218883049f0afa3de1.json", S_LU25,
     ITEM + "1c17a07ff8fc44218883049f0afa3de1?f=json", "downloaded_and_inspected"),
    ("lageo-ons-lad-dec2025-uk-buc-codes.json", S_DEC25,
     ARC + "Local_Authority_Districts_DEC_2025_Boundaries_UK_BUC/FeatureServer/0/query?where=1%3D1&outFields=LAD25CD%2CLAD25NM&returnGeometry=false&f=json",
     "downloaded_and_inspected"),
    ("lageo-arcgis-item-837dd9c41a7b458c974caf6e4ca56e7b.json", S_DEC25,
     ITEM + "837dd9c41a7b458c974caf6e4ca56e7b?f=json", "downloaded_and_inspected"),
    ("lageo-arcgis-item-a4d56f9755be48b0a78c120e499fa9df.json", S_BFE,
     ITEM + "a4d56f9755be48b0a78c120e499fa9df?f=json", "downloaded_and_inspected"),
    ("lageo-arcgis-item-5ff5bb9a2db54a4392935040a8ad433e.json", S_BFE,
     ITEM + "5ff5bb9a2db54a4392935040a8ad433e?f=json", "downloaded_and_inspected"),
    ("lageo-ons-code-history-database-jun2026.zip", S_CHD,
     ITEM + "e0bc41722b1a4b76a6ecfff14f91cbb4/data", "downloaded_and_inspected"),
    ("lageo-arcgis-item-e0bc41722b1a4b76a6ecfff14f91cbb4.json", S_CHD,
     ITEM + "e0bc41722b1a4b76a6ecfff14f91cbb4?f=json", "downloaded_and_inspected"),
    ("lageo-uksi-2024-1328-barnsley-sheffield-made.html", S_SI1328,
     "https://www.legislation.gov.uk/uksi/2024/1328/made", "page_inspected"),
    ("lageo-ons-lad-dec2024-bfe-barnsley-sheffield-area.json", S_BFE,
     ARC + "Local_Authority_Districts_December_2024_Boundaries_UK_BFE/FeatureServer/0/query?where=LAD24CD+IN+%28%27E08000016%27%2C%27E08000019%27%29&outFields=LAD24CD%2CLAD24NM%2CShape__Area&returnGeometry=false&f=json",
     "downloaded_and_inspected"),
    ("lageo-ons-lad-may2026-bfe-barnsley-sheffield-area.json", S_BFE,
     ARC + "Local_Authority_Districts_May_2026_Boundaries_UK_BFE/FeatureServer/0/query?where=LAD26CD+IN+%28%27E08000038%27%2C%27E08000039%27%29&outFields=LAD26CD%2CLAD26NM%2CShape__Area&returnGeometry=false&f=json",
     "downloaded_and_inspected"),
    ("lageo-ons-mye25tablesew.xlsx", S_EW25,
     ONS_FILE + "estimatesofthepopulationforenglandandwales/mid20252023localauthorityboundaries/mye25tablesew.xlsx",
     "downloaded_and_inspected"),
    ("lageo-ons-myebtablesenglandwales20112025.xlsx", S_EWTS,
     ONS_FILE + "estimatesofthepopulationforenglandandwales/mid2011tomid2025detailedtimeseries/myebtablesenglandwales20112025.xlsx",
     "downloaded_and_inspected"),
    ("lageo-ons-ew-population-estimates-dataset-page.html", S_ONSEWPAGE,
     "https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/datasets/estimatesofthepopulationforenglandandwales",
     "page_inspected"),
    ("lageo-ons-mye24tablesuk.xlsx", S_UK24,
     ONS_FILE + "populationestimatesforukenglandandwalesscotlandandnorthernireland/mid2024/mye24tablesuk.xlsx",
     "downloaded_and_inspected"),
    ("lageo-ons-uk-population-estimates-dataset-page.html", S_ONSUKPAGE,
     "https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/datasets/populationestimatesforukenglandandwalesscotlandandnorthernireland",
     "page_inspected"),
    ("lageo-nrs-data-mid-year-population-estimates-mid-2025.xlsx", S_NRS25,
     "https://www.nrscotland.gov.uk/media/15rlr1vf/data-mid-year-population-estimates-mid-2025.xlsx",
     "downloaded_and_inspected"),
    ("lageo-nrs-mid-2025-population-estimates-page.html", S_NRS25,
     "https://www.nrscotland.gov.uk/publications/mid-2025-population-estimates/", "page_inspected"),
    ("lageo-nrs-mid-year-population-estimates-time-series-data.xlsx", S_NRSTS,
     "https://www.nrscotland.gov.uk/media/kmepnkhq/mid-year-population-estimates-time-series-data.xlsx",
     "downloaded_and_inspected"),
    ("lageo-nisra-mye24-pop-totals.xlsx", S_NISRA24,
     "https://www.nisra.gov.uk/system/files/statistics/2025-09/MYE24-POP_TOTALS.xlsx",
     "downloaded_and_inspected"),
    ("lageo-nisra-2024-mye-publication-page.html", S_NISRA24,
     "https://www.nisra.gov.uk/publications/2024-mid-year-population-estimates-northern-ireland-and-estimates-population-aged-85",
     "page_inspected"),
    ("lageo-govuk-nisra-mye2025-announcement.html", S_NISRA25,
     "https://www.gov.uk/government/statistics/announcements/2025-mid-year-population-estimates-for-northern-ireland-including-estimates-of-the-population-aged-85",
     "page_inspected"),
    ("lageo-ons-geography-licences-page.html", S_ONSLIC,
     "https://www.ons.gov.uk/methodology/geography/licences", "page_inspected"),
    ("lageo-nisra-crown-copyright-page.html", S_NISRALIC,
     "https://www.nisra.gov.uk/crown-copyright", "page_inspected"),
]


def raw(name):
    return os.path.join(RAW, name)


# ---------------------------------------------------------------- xlsx reader
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
RNS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"


def _col(ref):
    n = 0
    for ch in re.match(r"[A-Z]+", ref).group(0):
        n = n * 26 + ord(ch) - 64
    return n - 1


class Workbook:
    """Minimal streaming xlsx reader: shared strings, inline strings, numbers."""

    def __init__(self, path):
        self.z = zipfile.ZipFile(path)
        self.shared = []
        if "xl/sharedStrings.xml" in self.z.namelist():
            for _, el in ET.iterparse(self.z.open("xl/sharedStrings.xml")):
                if el.tag == NS + "si":
                    self.shared.append("".join(t.text or "" for t in el.iter(NS + "t")))
                    el.clear()
        wb = ET.fromstring(self.z.read("xl/workbook.xml"))
        rels = ET.fromstring(self.z.read("xl/_rels/workbook.xml.rels"))
        rmap = {r.get("Id"): r.get("Target") for r in rels}
        self.sheets = {}
        for s in wb.iter(NS + "sheet"):
            target = rmap[s.get(RNS + "id")].lstrip("/")
            self.sheets[s.get("name")] = target if target.startswith("xl/") else "xl/" + target

    def rows(self, name):
        with self.z.open(self.sheets[name]) as fh:
            for _, el in ET.iterparse(fh):
                if el.tag != NS + "row":
                    continue
                out = []
                for c in el.iter(NS + "c"):
                    idx = _col(c.get("r"))
                    out.extend([None] * (idx - len(out)))
                    t, v = c.get("t"), c.find(NS + "v")
                    if t == "s":
                        val = self.shared[int(v.text)] if v is not None else None
                    elif t == "inlineStr":
                        val = "".join(x.text or "" for x in c.iter(NS + "t"))
                    elif t == "str":
                        val = v.text if v is not None else None
                    elif v is not None and v.text is not None:
                        try:
                            val = float(v.text)
                        except ValueError:
                            val = v.text
                    else:
                        val = None
                    out.append(val)
                el.clear()
                yield out


def as_int(x):
    f = float(x)
    if f != int(f):
        raise ValueError("non-integer population %r" % x)
    return int(f)


# ---------------------------------------------------------------- lookup
def read_csv_bom(path):
    with open(path, encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def build_lookup(report):
    rows = read_csv_bom(raw("lageo-ons-wd26-lad26-ctyua26-rgn26-ctry26-uk-lu.csv"))
    lads = {}
    for r in rows:
        code = r["LAD26CD"]
        if r["CTRY26CD"] == "E92000001":
            rc, rn = r["RGN26CD"], r["RGN26NM"]
        else:  # Wales, Scotland, Northern Ireland: nation as region
            rc, rn = r["CTRY26CD"], r["CTRY26NM"]
        rec = (r["LAD26NM"], r["CTRY26NM"], rc, rn)
        if code in lads and lads[code] != rec:
            raise SystemExit("inconsistent lookup rows for %s: %r vs %r" % (code, lads[code], rec))
        lads[code] = rec
    for code, (_, _, rc, _) in lads.items():
        if not rc:
            raise SystemExit("no region for %s" % code)

    # Cross-check England against the dedicated LAD-to-region lookup (April 2025, V2)
    lu25 = {r["LAD25CD"]: (r["LAD25NM"], r["RGN25CD"]) for r in read_csv_bom(raw("lageo-ons-lad25-rgn25-en-lu-v2.csv"))}
    eng = {c: v for c, v in lads.items() if c.startswith("E")}
    report["lookup"] = {
        "lad_count": len(lads),
        "ward_rows": len(rows),
        "by_prefix": count_prefix(lads),
        "crosscheck_lad25_rgn25_v2": {
            "england_codes_2026": len(eng),
            "england_codes_2025_lookup": len(lu25),
            "codes_only_in_2026": sorted(set(eng) - set(lu25)),
            "codes_only_in_2025_lookup": sorted(set(lu25) - set(eng)),
            "region_mismatches": sorted(c for c in set(eng) & set(lu25) if eng[c][2] != lu25[c][1]),
            "name_mismatches": sorted(c for c in set(eng) & set(lu25) if eng[c][0] != lu25[c][0]),
        },
    }
    return lads


def count_prefix(codes):
    out = {}
    for c in codes:
        out[c[:3]] = out.get(c[:3], 0) + 1
    return dict(sorted(out.items()))


# ---------------------------------------------------------------- boundaries
def round_ring(ring):
    pts = []
    for x, y in ring:
        p = [round(x, 5), round(y, 5)]
        if not pts or p != pts[-1]:
            pts.append(p)
    if pts and pts[0] != pts[-1]:
        pts.append(list(pts[0]))
    return pts if len(pts) >= 4 else None


def round_polygon(poly, dropped):
    out = []
    for i, ring in enumerate(poly):
        r = round_ring(ring)
        if r is None:
            if i == 0:
                dropped["polygons"] += 1
                return None
            dropped["holes"] += 1
            continue
        out.append(r)
    return out


def build_boundaries(lads, report):
    path = raw("lageo-ons-lad-may2026-uk-buc.geojson")
    with open(path, encoding="utf-8") as fh:
        src = json.load(fh)
    crs = (src.get("crs") or {}).get("properties", {}).get("name")
    if crs not in ("urn:ogc:def:crs:OGC:1.3:CRS84", "EPSG:4326"):
        raise SystemExit("unexpected CRS %r; conversion needed" % crs)

    dropped = {"polygons": 0, "holes": 0}
    features, seen, problems = [], {}, []
    minx = miny = 999.0
    maxx = maxy = -999.0
    for f in src["features"]:
        p = f["properties"]
        code = p["LAD26CD"]
        seen[code] = seen.get(code, 0) + 1
        g = f["geometry"]
        polys = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
        newpolys = [q for q in (round_polygon(pp, dropped) for pp in polys) if q]
        if not newpolys:
            problems.append("%s: geometry collapsed after rounding" % code)
            continue
        # sanity: coordinates plausible for the UK in lon/lat, and ONS LONG/LAT inside bbox
        xs = [pt[0] for pp in newpolys for ring in pp for pt in ring]
        ys = [pt[1] for pp in newpolys for ring in pp for pt in ring]
        bx0, bx1, by0, by1 = min(xs), max(xs), min(ys), max(ys)
        minx, maxx, miny, maxy = min(minx, bx0), max(maxx, bx1), min(miny, by0), max(maxy, by1)
        if not (bx0 - 0.01 <= p["LONG"] <= bx1 + 0.01 and by0 - 0.01 <= p["LAT"] <= by1 + 0.01):
            problems.append("%s: ONS LONG/LAT (%s, %s) outside feature bbox" % (code, p["LONG"], p["LAT"]))
        if code not in lads:
            problems.append("%s: boundary feature has no lookup row" % code)
            continue
        name, country, rc, rn = lads[code]
        if name != p["LAD26NM"]:
            problems.append("%s: name differs boundary=%r lookup=%r" % (code, p["LAD26NM"], name))
        geom = ({"type": "Polygon", "coordinates": newpolys[0]} if len(newpolys) == 1 and g["type"] == "Polygon"
                else {"type": "MultiPolygon", "coordinates": newpolys})
        features.append({
            "type": "Feature",
            "properties": {
                "localAuthorityCode": code,
                "localAuthorityName": name,
                "country": country,
                "regionCode": rc,
                "regionName": rn,
                "boundaryVintage": BOUNDARY_VINTAGE,
                "sourceIds": [S_BUC, S_LU],
            },
            "geometry": geom,
        })
    features.sort(key=lambda f: f["properties"]["localAuthorityCode"])
    out = os.path.join(OUT, "uk-local-authorities.geojson")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump({"type": "FeatureCollection", "features": features}, fh, ensure_ascii=False, separators=(",", ":"))
        fh.write("\n")
    size = os.path.getsize(out)
    if not (-9.0 < minx and maxx < 2.1 and 49.8 < miny and maxy < 61.0):
        problems.append("overall bbox outside expected UK lon/lat range: %r" % [minx, miny, maxx, maxy])
    report["boundaries"] = {
        "source_crs": crs,
        "source_features": len(src["features"]),
        "output_features": len(features),
        "output_bytes": size,
        "output_megabytes": round(size / 1048576, 3),
        "bbox_lonlat": [minx, miny, maxx, maxy],
        "dropped_after_rounding": dropped,
        "duplicate_codes": sorted(c for c, n in seen.items() if n > 1),
        "problems": problems,
    }
    return {f["properties"]["localAuthorityCode"] for f in features}, seen


def write_lookup(lads):
    out = os.path.join(OUT, "la-lookup.csv")
    with open(out, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["la_code", "la_name", "country", "region_code", "region_name", "boundary_vintage", "source_id"])
        for code in sorted(lads):
            name, country, rc, rn = lads[code]
            w.writerow([code, name, country, rc, rn, BOUNDARY_VINTAGE, S_LU])


# ---------------------------------------------------------------- code changes
def chd_date(s):
    s = (s or "").strip().split(" ")[0]
    return datetime.datetime.strptime(s, "%d/%m/%Y").date() if s else None


def chd_rows(z, name):
    with z.open(name) as fh:  # CHD CSVs are not valid UTF-8 throughout; latin-1 is lossless for ASCII codes
        yield from csv.DictReader(io.TextIOWrapper(fh, encoding="latin-1", newline=""))


def ha(path, code_field):
    with open(path, encoding="utf-8") as fh:
        d = json.load(fh)
    return {f["attributes"][code_field]: f["attributes"]["Shape__Area"] / 10000.0 for f in d["features"]}


def build_code_changes(lads, report):
    z = zipfile.ZipFile(raw("lageo-ons-code-history-database-jun2026.zip"))
    pairs, renames = [], []
    for r in chd_rows(z, "Changes.csv"):
        if r["ENTITYCD"] not in LAD_ENTITIES:
            continue
        d = chd_date(r["OPER_DATE"])
        if not (WINDOW[0] <= d <= WINDOW[1]):
            continue
        if r["GEOGCD"] == r["GEOGCD_P"]:
            renames.append({"code": r["GEOGCD"], "name": r["GEOGNM"], "previous_name": r["GEOGNM_P"],
                            "si": (r["SI_ID"] + " " + r["SI_TITLE"]).strip(), "date": d.isoformat()})
            continue
        pairs.append({"old": r["GEOGCD_P"], "old_name": r["GEOGNM_P"], "new": r["GEOGCD"], "new_name": r["GEOGNM"],
                      "date": d.isoformat(), "si_id": r["SI_ID"], "si_title": r["SI_TITLE"]})

    hist, max_oper = {}, None
    for r in chd_rows(z, "ChangeHistory.csv"):
        d = chd_date(r["OPER_DATE"])
        if d and (max_oper is None or d > max_oper):
            max_oper = d
        if r["ENTITYCD"] in LAD_ENTITIES:
            hist.setdefault(r["GEOGCD"], []).append(r)

    succ, pred = {}, {}
    for p in pairs:
        succ.setdefault(p["old"], set()).add(p["new"])
        pred.setdefault(p["new"], set()).add(p["old"])

    bfe_old = ha(raw("lageo-ons-lad-dec2024-bfe-barnsley-sheffield-area.json"), "LAD24CD")
    bfe_new = ha(raw("lageo-ons-lad-may2026-bfe-barnsley-sheffield-area.json"), "LAD26CD")

    rows, splits = [], []
    for p in sorted(pairs, key=lambda x: (x["date"], x["new"], x["old"])):
        o, n = p["old"], p["new"]
        si = "SI %s, %s" % (p["si_id"], p["si_title"])
        if len(succ[o]) > 1:
            ctype = "split"
            others = ", ".join(sorted(succ[o] - {n}))
            note = ("SPLIT: %s maps to more than one successor (%s and %s); cannot be harmonised by simple aggregation. %s."
                    % (o, n, others, si))
            splits.append(o)
        elif len(pred[n]) > 1 and all(len(succ[q]) == 1 for q in pred[n]):
            ctype = "merge"
            note = ("Whole-district merge into %s with %s; %s maps only to %s in the CHD Changes table, so data on %s can be "
                    "summed into %s. %s." % (n, ", ".join(sorted(pred[n] - {o})), o, n, o, n, si))
        elif "boundary" in p["si_title"].lower():
            ctype = "boundary_change"
            note = ("%s recoded to %s after its boundary changed; it also received territory from %s. %s."
                    % (o, n, ", ".join(sorted(pred[n] - {o})) or "none", si))
        else:
            ctype = "recode"
            note = "Code change without recorded boundary change. %s." % si
        if o in bfe_old or n in bfe_new:
            note += (" SI 2024/1328 art. 3 transfers an area from Barnsley to Sheffield. Derived from ONS BFE Shape__Area:"
                     " Barnsley E08000016 %.2f ha (Dec 2024) -> E08000038 %.2f ha (May 2026), loss %.2f ha;"
                     " Sheffield E08000019 %.2f ha -> E08000039 %.2f ha, gain %.2f ha. Population of the transferred"
                     " area is not published in the sources used; population.csv keeps E08000016/E08000019 as published." % (
                         bfe_old["E08000016"], bfe_new["E08000038"], bfe_old["E08000016"] - bfe_new["E08000038"],
                         bfe_old["E08000019"], bfe_new["E08000039"], bfe_new["E08000039"] - bfe_old["E08000019"]))
        if n not in lads:
            note += " WARNING: successor not in May 2026 lookup."
        if o in lads:
            note += " WARNING: predecessor still in May 2026 lookup."
        rows.append([o, p["old_name"], n, p["new_name"], p["date"], ctype, S_CHD, note])

    out = os.path.join(OUT, "la-code-changes.csv")
    with open(out, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["old_code", "old_name", "new_code", "new_name", "effective_date", "change_type", "source_id", "notes"])
        w.writerows(rows)

    # Barnsley -> Sheffield transfer, derived from BFE areas
    transfer = None
    if "E08000016" in bfe_old and "E08000038" in bfe_new:
        transfer = {
            "barnsley_loss_ha": round(bfe_old["E08000016"] - bfe_new["E08000038"], 2),
            "sheffield_gain_ha": round(bfe_new["E08000039"] - bfe_old["E08000019"], 2),
        }
    counts = {}
    for r in rows:
        counts[r[5]] = counts.get(r[5], 0) + 1
    report["code_changes"] = {
        "rows": len(rows),
        "by_type": counts,
        "split_old_codes": sorted(set(splits)),
        "name_changes_excluded": renames,
        "chd_latest_operative_date_any_entity": max_oper.isoformat() if max_oper else None,
        "lad_entities_changed_after_2025_04_01": sorted(
            c for c, rs in hist.items()
            if any((chd_date(r["OPER_DATE"]) or datetime.date.min) > datetime.date(2025, 4, 1) for r in rs)),
        "barnsley_sheffield_transfer_area_derived": transfer,
    }
    return rows


# ---------------------------------------------------------------- population
PUB_ONS, PUB_NRS, PUB_NISRA = ("Office for National Statistics", "National Records of Scotland",
                               "Northern Ireland Statistics and Research Agency")
GV_EW = "Local authorities as of April 2023 (ONS ladcode23)"
GV_SC = "Council areas, 2019 boundaries (NRS)"
GV_NI = "Local Government Districts 2014 (NISRA LGD2014)"


def build_population(report):
    pop = {}  # (code, year) -> row
    names = {}

    # England and Wales: ONS MYEB3, mid-2011 to mid-2025 (released 29 July 2026), 2023 LA boundaries
    wb = Workbook(raw("lageo-ons-myebtablesenglandwales20112025.xlsx"))
    header = None
    for r in wb.rows("MYEB3"):
        if header is None:
            if r and r[0] == "ladcode23":
                header = r
            continue
        if not r or not r[0]:
            continue
        code, name = r[0], r[1]
        for y in YEARS:
            val = r[header.index("population_%d" % y)]
            pop[(code, y)] = [code, name, y, as_int(val), GV_EW, PUB_ONS, S_EWTS]
        names[code] = name

    # Cross-check mid-2025 against the mid-2025 E&W release table MYE2 (All ages)
    wb = Workbook(raw("lageo-ons-mye25tablesew.xlsx"))
    mye2, ew_totals = {}, {}
    for r in wb.rows("MYE2 - Persons"):
        if r and isinstance(r[0], str) and re.match(r"^[EWK]\d{8}$", r[0]):
            if r[0][:3] in LAD_ENTITIES:
                mye2[r[0]] = as_int(r[3])
            elif r[0] in ("K04000001", "E92000001", "W92000004"):
                ew_totals[r[0]] = as_int(r[3])
    ew_diff = sorted(c for c in mye2 if pop.get((c, 2025), [None] * 4)[3] != mye2[c])

    # Scotland: NRS time series Table 3 (released 14 July 2026)
    wb = Workbook(raw("lageo-nrs-mid-year-population-estimates-time-series-data.xlsx"))
    header = None
    scot_total = {}
    for r in wb.rows("Table 3"):
        if header is None:
            if r and isinstance(r[0], str) and r[0].strip().startswith("Area type"):
                header = [str(x).strip() if x is not None else None for x in r]
            continue
        if not r or len(r) < 4 or r[3] != "Persons":
            continue
        if r[0].strip() == "Country" and r[1] == "S92000003":
            scot_total = {y: as_int(r[header.index(str(y))]) for y in YEARS}
        if r[0].strip() != "Council area":
            continue
        code, name = r[1], r[2]
        for y in YEARS:
            pop[(code, y)] = [code, name, y, as_int(r[header.index(str(y))]), GV_SC, PUB_NRS, S_NRSTS]
        names[code] = name

    # Cross-check Scotland mid-2025 against the NRS mid-2025 data table 1
    wb = Workbook(raw("lageo-nrs-data-mid-year-population-estimates-mid-2025.xlsx"))
    nrs25 = {}
    for r in wb.rows("Table 1"):
        if r and len(r) > 4 and r[2] == "Council area" and r[3] == "Persons":
            nrs25[r[1]] = as_int(r[4])
    sc_diff = sorted(c for c in nrs25 if pop.get((c, 2025), [None] * 4)[3] != nrs25[c])
    sc_vals = [v[3] for k, v in pop.items() if k[0].startswith("S12")]
    sc_round10 = sum(1 for v in sc_vals if v % 10 == 0)

    # Northern Ireland: NISRA MYE24 population totals (published 11 September 2025), unrounded
    wb = Workbook(raw("lageo-nisra-mye24-pop-totals.xlsx"))
    ni_total = {}
    for r in wb.rows("Flat"):
        if not r or len(r) < 6 or r[4] != "Unrounded" or not isinstance(r[3], float):
            continue
        y = int(r[3])
        if y not in YEARS:
            continue
        if r[1] == "N92000002":
            ni_total[y] = as_int(r[5])
        elif str(r[0]).startswith("2. Local Government Districts"):
            pop[(r[1], y)] = [r[1], r[2], y, as_int(r[5]), GV_NI, PUB_NISRA, S_NISRA24]
            names[r[1]] = r[2]

    # ONS UK mid-2024 (released 26 September 2025): UK total and per-LA comparison
    wb = Workbook(raw("lageo-ons-mye24tablesuk.xlsx"))
    uk24, uk24_totals = {}, {}
    for r in wb.rows("MYE2 - Persons"):
        if r and isinstance(r[0], str) and re.match(r"^[EWSNK]\d{8}$", r[0]):
            if r[0][:3] in LAD_ENTITIES:
                uk24[r[0]] = as_int(r[3])
            elif r[0] in ("K02000001", "K03000001", "K04000001", "E92000001", "W92000004", "S92000003", "N92000002"):
                uk24_totals[r[0]] = as_int(r[3])
    cmp24 = {"identical": 0, "different": 0, "missing_in_population_csv": [], "sum_diff_by_prefix": {}}
    for c, v in uk24.items():
        mine = pop.get((c, 2024))
        if mine is None:
            cmp24["missing_in_population_csv"].append(c)
            continue
        if mine[3] == v:
            cmp24["identical"] += 1
        else:
            cmp24["different"] += 1
        k = c[0]
        cmp24["sum_diff_by_prefix"][k] = cmp24["sum_diff_by_prefix"].get(k, 0) + mine[3] - v

    rows = [pop[k] for k in sorted(pop)]
    out = os.path.join(OUT, "population.csv")
    with open(out, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["la_code", "la_name", "mid_year", "population", "geography_vintage", "publisher", "source_id"])
        w.writerows(rows)

    by_year = {}
    for (c, y), r in pop.items():
        by_year.setdefault(y, {"E": 0, "W": 0, "S": 0, "N": 0, "rows": 0})
        by_year[y][c[0]] += r[3]
        by_year[y]["rows"] += 1
    nations_by_year = {y: sorted({c[0] for (c, yy) in pop if yy == y}) for y in YEARS}
    complete_years = [y for y in YEARS if nations_by_year[y] == ["E", "N", "S", "W"]]
    report["population"] = {
        "rows": len(rows),
        "sums_by_year_and_nation_prefix": by_year,
        "nations_by_year": nations_by_year,
        "latest_mid_year_all_uk_nations": max(complete_years) if complete_years else None,
        "latest_mid_year_any_nation": max(nations_by_year[y] and y for y in YEARS),
        "ew_mid2025_vs_mye25tablesew_mismatches": ew_diff,
        "ew_mid2025_published_totals": ew_totals,
        "ew_mid2025_sum_of_las_equals_K04000001": sum(mye2.values()) == ew_totals.get("K04000001"),
        "scotland_mid2025_vs_nrs_table1_mismatches": sc_diff,
        "scotland_published_totals": scot_total,
        "scotland_council_values_divisible_by_10": "%d of %d" % (sc_round10, len(sc_vals)),
        "ni_published_totals_unrounded": ni_total,
        "ons_uk_mid2024_totals": uk24_totals,
        "ons_uk_mid2024_vs_population_csv_2024": cmp24,
    }
    return pop


# ---------------------------------------------------------------- manifest
def write_manifest():
    entries = []
    for name, sid, url, status in RAW_FILES:
        p = raw(name)
        h = hashlib.sha256()
        with open(p, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
        entries.append({"file": "raw/" + name, "sha256": h.hexdigest(), "bytes": os.path.getsize(p),
                        "retrieved_at": RETRIEVED, "source_id": sid, "url": url, "status": status})
    # After the Phase 1B merge these entries live in raw/manifest.json; check they still match.
    with open(os.path.join(RAW, "manifest.json"), encoding="utf-8") as fh:
        listed = {e["file"]: e["sha256"] for e in json.load(fh)["files"]}
    for e in entries:
        assert listed.get(e["file"]) == e["sha256"], "raw file differs from manifest: " + e["file"]
    return entries


# ---------------------------------------------------------------- checks
def run_checks(lads, boundary_codes, boundary_counts, pop, changes, report):
    successors = {r[2]: r for r in changes}
    predecessors = {r[0]: r for r in changes}
    lookup = set(lads)
    checks = {
        "lookup_codes_without_boundary": sorted(lookup - boundary_codes),
        "boundary_codes_without_lookup": sorted(boundary_codes - lookup),
        "lookup_codes_with_multiple_boundary_features": sorted(c for c in lookup if boundary_counts.get(c, 0) > 1),
        "population": {},
    }
    for y in (report["population"]["latest_mid_year_all_uk_nations"], max(YEARS)):
        pop_codes = {c for (c, yy) in pop if yy == y}
        missing = sorted(lookup - pop_codes)
        extra = sorted(pop_codes - lookup)
        checks["population"][str(y)] = {
            "lookup_codes_without_population": [
                {"code": c, "name": lads[c][0],
                 "explanation": ("successor in la-code-changes.csv (%s from %s); population published on predecessor code"
                                 % (successors[c][5], successors[c][0])) if c in successors
                 else ("Northern Ireland mid-%d not yet published by NISRA" % y if c.startswith("N09") else "UNEXPLAINED")}
                for c in missing],
            "population_codes_not_in_lookup": [
                {"code": c, "explanation": ("predecessor in la-code-changes.csv (%s to %s)" % (predecessors[c][5], predecessors[c][2]))
                 if c in predecessors else "UNEXPLAINED"} for c in extra],
        }
    unexplained = [m for y in checks["population"].values()
                   for m in y["lookup_codes_without_population"] + y["population_codes_not_in_lookup"]
                   if m["explanation"] == "UNEXPLAINED"]
    checks["unexplained_mismatch_count"] = len(unexplained)
    checks["pass_one_boundary_per_lookup_code"] = not (checks["lookup_codes_without_boundary"]
                                                       or checks["boundary_codes_without_lookup"]
                                                       or checks["lookup_codes_with_multiple_boundary_features"])
    report["checks"] = checks


def main():
    report = {"generated_for": "Phase 1B lageo", "retrieved_at": RETRIEVED, "boundary_vintage": BOUNDARY_VINTAGE}
    lads = build_lookup(report)
    boundary_codes, counts = build_boundaries(lads, report)
    write_lookup(lads)

    # Vintage evidence: Dec 2025 and May 2026 code/name sets
    with open(raw("lageo-ons-lad-dec2025-uk-buc-codes.json"), encoding="utf-8") as fh:
        dec25 = {f["attributes"]["LAD25CD"]: f["attributes"]["LAD25NM"] for f in json.load(fh)["features"]}
    report["vintage_comparison_dec2025_vs_may2026"] = {
        "dec2025_codes": len(dec25), "may2026_codes": len(lads),
        "only_dec2025": sorted(set(dec25) - set(lads)), "only_may2026": sorted(set(lads) - set(dec25)),
        "name_differences": sorted(c for c in set(dec25) & set(lads) if dec25[c] != lads[c][0]),
    }

    changes = build_code_changes(lads, report)
    pop = build_population(report)
    run_checks(lads, boundary_codes, counts, pop, changes, report)
    report["manifest_files"] = len(write_manifest())

    with open(os.path.join(OUT, "lageo-build-report.json"), "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=1, ensure_ascii=False, default=str)
        fh.write("\n")

    c = report["checks"]
    print("features: %d, geojson bytes: %d (%.3f MB)" % (report["boundaries"]["output_features"],
          report["boundaries"]["output_bytes"], report["boundaries"]["output_megabytes"]))
    print("lookup rows: %d; code-change rows: %d %s; splits: %s" % (
        len(lads), len(changes), report["code_changes"]["by_type"], report["code_changes"]["split_old_codes"]))
    print("population rows: %d; latest mid-year for all UK nations: %s" % (
        report["population"]["rows"], report["population"]["latest_mid_year_all_uk_nations"]))
    print("one boundary per lookup code: %s" % c["pass_one_boundary_per_lookup_code"])
    for y, v in c["population"].items():
        for m in v["lookup_codes_without_population"]:
            print("  mid-%s lookup code without population: %s %s -> %s" % (y, m["code"], m["name"], m["explanation"]))
        for m in v["population_codes_not_in_lookup"]:
            print("  mid-%s population code not in lookup: %s -> %s" % (y, m["code"], m["explanation"]))
    if report["boundaries"]["problems"]:
        print("boundary problems:", report["boundaries"]["problems"])
    print("unexplained mismatches: %d" % c["unexplained_mismatch_count"])
    ok = (c["pass_one_boundary_per_lookup_code"] and c["unexplained_mismatch_count"] == 0
          and not report["boundaries"]["problems"])
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
