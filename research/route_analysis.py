#!/usr/bin/env python3
"""Part 4 route distance analysis (reproducible, stdlib only).

Reads documented-routes.geojson and crossing-events.geojson (same directory) and
writes route-analysis.json with:
  * haversine great-circle distances for each documented origin/destination pair;
  * distance bounds from endpoint uncertainty (d +/- (u_origin + u_destination));
  * distribution statistics per pair type;
  * the sector/year spread of documented launch/departure locations and UK-side
    locations in the (non-representative) event sample;
  * the Part 4 conclusion with reasoning and limitations.

A straight segment is NOT a navigated track; it is a lower bound on any path.
Usage: python3 route_analysis.py
"""
import json
import math
import statistics
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
R_KM = 6371.0088  # IUGG mean Earth radius
KM_PER_NM = 1.852


def haversine_km(a, b):
    (lon1, lat1), (lon2, lat2) = a, b
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi, dlmb = p2 - p1, math.radians(lon2 - lon1)
    h = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlmb / 2) ** 2
    return 2 * R_KM * math.asin(math.sqrt(h))


def summary(values):
    if not values:
        return None
    return {"n": len(values), "min_km": round(min(values), 1), "median_km": round(statistics.median(values), 1),
            "max_km": round(max(values), 1)}


def main():
    routes = json.loads((HERE / "geography" / "documented-routes.geojson").read_text(encoding="utf-8"))["features"]
    events = json.loads((HERE / "crossings" / "crossing-events.geojson").read_text(encoding="utf-8"))["features"]

    pairs = []
    for f in routes:
        p = f["properties"]
        a, b = f["geometry"]["coordinates"]
        d = haversine_km(a, b)
        uo = p["origin"]["uncertainty_km"] or 0.0
        ud = p["destination"]["uncertainty_km"] or 0.0
        pairs.append({
            "id": p["id"], "event_id": p["event_id"], "event_date": p["event_date"], "year": int(p["event_date"][:4]),
            "pair_type": p["pair_type"], "includes_cross_channel_leg": p["includes_cross_channel_leg"],
            "origin": p["origin"]["name"], "origin_precision": p["origin"]["location_precision"],
            "destination": p["destination"]["name"], "destination_precision": p["destination"]["location_precision"],
            "distance_km": round(d, 1), "distance_nm": round(d / KM_PER_NM, 1),
            "endpoint_uncertainty_km": round(uo + ud, 1),
            "distance_bounds_km": [round(max(0.0, d - uo - ud), 1), round(d + uo + ud, 1)],
            "relative_uncertainty": round((uo + ud) / d, 2) if d else None,
        })

    by_type = defaultdict(list)
    for x in pairs:
        by_type[x["pair_type"]].append(x["distance_km"])
    distribution = {k: summary(v) for k, v in sorted(by_type.items())}

    # Spread of documented launch/departure locations in the event sample.
    launch_roles = {"launch_site", "departure_area", "first_detection_at_sea", "prevented_launch_site"}
    uk_roles = {"uk_disembarkation", "uk_arrival_area", "uk_reception_area"}
    spread = defaultdict(lambda: {"sectors": Counter(), "latitudes": [], "event_ids": []})
    uk_side = []
    for f in events:
        p = f["properties"]
        date = p["event_date"]
        year = int(date[:4]) if date else None
        roles = [l for l in p["documented_locations"] if l["role"] in launch_roles]
        if year and roles:
            s = spread[year]
            s["sectors"][p["origin_sector"] or "unknown"] += 1
            s["event_ids"].append(p["id"])
            for l in roles:
                if l["coordinates"]:
                    s["latitudes"].append(l["coordinates"][1])
        for l in p["documented_locations"]:
            if l["role"] in uk_roles:
                uk_side.append({"event_id": p["id"], "year": year, "role": l["role"], "name": l["name"],
                                "location_precision": l["location_precision"]})
    spread_out = {}
    for y in sorted(spread):
        s = spread[y]
        spread_out[str(y)] = {
            "events_with_launch_or_departure_location": len(s["event_ids"]),
            "sectors": dict(sorted(s["sectors"].items())),
            "latitude_range": [round(min(s["latitudes"]), 3), round(max(s["latitudes"]), 3)] if s["latitudes"] else None,
            "event_ids": s["event_ids"],
        }

    out = {
        "schema_version": 1,
        "as_of": "2026-09-11",
        "method": {
            "distance": "Haversine great-circle distance on a sphere, R = 6371.0088 km; 1 nm = 1.852 km.",
            "uncertainty": "Bounds = distance +/- (origin uncertainty_km + destination uncertainty_km), floored at 0. Exact-coordinate endpoints use the small uncertainty stated in the events file.",
            "meaning": "Straight line between documented endpoints of the same event; not a navigated track and a lower bound on any real path.",
            "inputs": ["documented-routes.geojson", "crossing-events.geojson", "geocoding-log.json (via the GeoJSON)"],
            "classification": "DERIVED_STATISTIC",
        },
        "pairs": pairs,
        "distance_distribution_by_pair_type": distribution,
        "sample_spread_of_launch_or_departure_locations_by_year": {
            "warning": ("Selected, non-representative event sample assembled partly by searching for peripheral place names. "
                        "Counts reflect search strategy and press-notice practice, not the distribution of departures."),
            "by_year": spread_out,
        },
        "uk_side_locations_in_sample": uk_side,
        "representative_distribution_available": False,
        "representative_distribution_note": ("No French or UK official source retrieved in this pass publishes departures, attempts or rescues by "
                                             "département or coastal sector for any year 2018-2026. The Préfecture maritime annual reviews 2019-2025 "
                                             "give façade-wide totals and qualitative statements only; the Home Office series is not disaggregated "
                                             "by departure location. The only sector counts found are partial: Seine-Maritime prevented departures "
                                             "(2024 full year vs 2025 to 20 Aug, prefecture via ICI) and Belgian-coast departures/interventions in 2026 "
                                             "(federal police via VRT)."),
        "official_qualitative_statements": [
            {"source_id": "FR-REVIEW-2021", "year_described": 2021, "statement": "Departures mainly between Dunkirk and Calais, increasingly extending south as far as Berck; a few rare events towards Dieppe."},
            {"source_id": "FR-REVIEW-2024", "year_described": 2024, "statement": "Extension of departure zones south as far as Dieppe, 'mechanically' lengthening crossing durations (official interpretation)."},
            {"source_id": "BSC-2026", "year_described": "2025-26", "statement": "Signs of potential geographic displacement: some launches from beaches further south in France and a small number further north in Belgium."},
            {"source_id": "FR-NOTICE-2026-09-06", "year_described": 2026, "statement": "Departure of a migrant boat described as unusual for the western Baie de Seine zone."},
        ],
        "evidence_against_expansion": [
            "FR-REVIEW-2021: in 2021 departures were still mainly between Dunkirk and Calais.",
            "Seine-Maritime departures are documented as early as March 2021 (FR-NOTICE-2021-03-09), so southern activity is not new in 2024-2026.",
            "Several southern launches are taxi-boat legs that travel north to pick up passengers on the Pas-de-Calais coast before crossing (Dieppe -> Stella-Plage 2025; Yport -> Berck 2026; Baie de Somme -> Berck 2025): the launch spreads more than the loaded crossing.",
            "Belgian police describe Belgian launches as taxi legs towards France; boats were escorted into French waters; no boats or interventions on the Belgian coast after 1 May 2026 (VRT-2026-06-03).",
            "In 2024, 45,203 of the migrants involved in operations were counted in the CROSS Gris-Nez zone (FR-REVIEW-2024 p.6); migrant activity in the CROSS Jobourg (western Channel) zone was described as unusual in 2026.",
            "The Normandy (Utah Beach -> Portsmouth) crossing is a single case.",
        ],
        "conclusion": {
            "selected": "C",
            "label": "Isolated longer crossings exist but no trend is established",
            "confidence": "MEDIUM",
            "reasoning": [
                "A (concentration) is supported for the bulk of activity: French reviews place the dedicated rescue system in the Dover Strait/CROSS Gris-Nez zone and, for 2021, locate departures mainly between Dunkirk and Calais; the 2024 migrant involvement count is almost entirely in the Gris-Nez zone. But this zone runs from the Belgian border into Seine-Maritime, so A cannot be tested at sector level.",
                "B (gradual expansion) is suggested by consistent official qualitative statements (2021: to Berck, rare Dieppe; 2024: to Dieppe; 2025-26 BSC: further south and into Belgium) and by 2024-2026 notices from the Somme, Seine-Maritime and Normandy. It is not established because no representative annual distribution by sector exists in the retrieved sources, as the brief requires.",
                "Longer documented legs exist (straight-line: Yport -> Berck 116.5 km; Dieppe -> Stella-Plage 71.2 km; Utah Beach -> Portsmouth, reported endpoints, 156.6 km, versus 35.4 km for Cap Blanc-Nez -> Dover), but they are isolated, selected cases; the coastal legs precede a pickup further north and are not longer loaded crossings.",
                "Belgian launches in early 2026 rose from 0-2 per year to 15 by late March and 33 interventions by early June, then stopped after 1 May 2026: a documented short-lived episode, not a sustained trend.",
            ],
            "what_would_change_it": "A French official annual series of departures/attempts by département or coastal sector (préfecture du Nord/Pas-de-Calais/Somme/Seine-Maritime, Ministère de l'Intérieur) for 2019-2026, or a UK series by departure area.",
        },
        "limitations": [
            "Pair types are heterogeneous; only 4 pairs involve the cross-Channel leg and none is a full launch-to-landfall navigated distance with both endpoints precise.",
            "Named-area endpoints (5-20 km uncertainty) dominate the error for short pairs (relative uncertainty often > 50%).",
            "The Utah Beach -> Portsmouth pair rests on news reporting for both endpoints; the Premar notice documents only the boat west of the Baie de Seine heading to the UK.",
            "Press notices are issued selectively (notable operations); their geography is not a sampling frame.",
        ],
    }
    (HERE / "geography" / "route-analysis.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for x in pairs:
        print(f"{x['id']:48s} {x['distance_km']:7.1f} km  bounds {x['distance_bounds_km']}")


if __name__ == "__main__":
    main()
