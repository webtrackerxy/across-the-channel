#!/usr/bin/env python3
"""Geocode named places cited in the Phase 1A geography evidence.

Queries the public OpenStreetMap Nominatim search API (one request per second,
per its usage policy) and writes every query and the top result verbatim to
geocoding-log.json. Coordinates from this log are gazetteer representative
points for NAMED PLACES; they are not observed vessel positions. Location
precision and uncertainty are assigned separately in crossing-events.geojson.

Usage: python3 geocode_places.py   (writes geocoding-log.json beside this file)
Stdlib only.
"""
import json
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "geography" / "geocoding-log.json"
ENDPOINT = "https://nominatim.openstreetmap.org/search"
UA = "boats-3d-view-research/phase1a (evidence geocoding; contact via project owner)"

# key -> free-text query. Keys are referenced from crossing-events.geojson.
PLACES = {
    # Nord (59)
    "gravelines": "Gravelines, Nord, France",
    "petit-fort-philippe": "Petit-Fort-Philippe, Gravelines, France",
    "dunkerque-port": "Port de Dunkerque, Dunkerque, France",
    "dunkerque": "Dunkerque, Nord, France",
    "malo-les-bains": "Malo-les-Bains, Dunkerque, France",
    "leffrinckoucke": "Leffrinckoucke, Nord, France",
    # Pas-de-Calais (62)
    "calais": "Calais, Pas-de-Calais, France",
    "phare-de-walde": "Phare de Walde, Marck, France",
    "cap-blanc-nez": "Cap Blanc-Nez, France",
    "ambleteuse": "Ambleteuse, Pas-de-Calais, France",
    "wimereux": "Wimereux, Pas-de-Calais, France",
    "pointe-aux-oies": "Pointe aux Oies, Wimereux, France",
    "boulogne-sur-mer": "Boulogne-sur-Mer, Pas-de-Calais, France",
    "equihen-plage": "Équihen-Plage, Pas-de-Calais, France",
    "ecault": "Écault, Saint-Étienne-au-Mont, France",
    "hardelot": "Hardelot-Plage, Neufchâtel-Hardelot, France",
    "stella-plage": "Stella-Plage, Cucq, France",
    "berck-sur-mer": "Berck, Montreuil-sur-Mer, Pas-de-Calais, France",
    # Somme (80)
    "baie-de-somme": "Baie de Somme, France",
    "saint-valery-sur-somme": "Saint-Valery-sur-Somme, Somme, France",
    "cayeux-sur-mer": "Cayeux-sur-Mer, Somme, France",
    # Seine-Maritime (76)
    "berneval-le-grand": "Berneval-le-Grand, Seine-Maritime, France",
    "dieppe": "Dieppe, Seine-Maritime, France",
    "varengeville-sur-mer": "Varengeville-sur-Mer, Seine-Maritime, France",
    "yport": "Yport, Seine-Maritime, France",
    # Normandy west / Manche (50)
    "baie-de-seine": "Baie de Seine, France",
    "utah-beach-la-breche": "La Brèche, Sainte-Marie-du-Mont, Manche, France",
    "utah-beach": "Utah Beach, Sainte-Marie-du-Mont, France",
    "iles-saint-marcouf": "Îles Saint-Marcouf, France",
    # Belgium (West Flanders)
    "de-panne": "De Panne, West-Vlaanderen, Belgium",
    "oostduinkerke": "Oostduinkerke, Koksijde, Belgium",
    "koksijde": "Koksijde, West-Vlaanderen, Belgium",
    "nieuwpoort": "Nieuwpoort, West-Vlaanderen, Belgium",
    "middelkerke": "Middelkerke, West-Vlaanderen, Belgium",
    "bredene": "Bredene, West-Vlaanderen, Belgium",
    # United Kingdom
    "dover": "Dover, Kent, United Kingdom",
    "port-of-dover": "Port of Dover, Dover, United Kingdom",
    "western-jet-foil": "Western Docks, Dover, United Kingdom",
    "tug-haven": "Tug Haven, Dover, United Kingdom",
    "manston": "Manston, Kent, United Kingdom",
    "langstone-harbour": "Langstone Harbour, Hampshire, United Kingdom",
    "portsmouth": "Portsmouth, Hampshire, United Kingdom",
}


def query(q):
    params = urllib.parse.urlencode({"q": q, "format": "jsonv2", "limit": 1, "addressdetails": 0})
    req = urllib.request.Request(f"{ENDPOINT}?{params}", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def main():
    log = {
        "service": "OpenStreetMap Nominatim search API",
        "endpoint": ENDPOINT,
        "data_licence": "ODbL 1.0, © OpenStreetMap contributors",
        "retrieved_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "note": "Top result per query, stored verbatim. Representative points for named places only.",
        "results": {},
    }
    for key, q in PLACES.items():
        try:
            res = query(q)
            top = res[0] if res else None
            log["results"][key] = {
                "query": q,
                "matched": bool(top),
                "display_name": top.get("display_name") if top else None,
                "lat": float(top["lat"]) if top else None,
                "lon": float(top["lon"]) if top else None,
                "osm_type": top.get("osm_type") if top else None,
                "osm_id": top.get("osm_id") if top else None,
                "category": top.get("category") if top else None,
                "type": top.get("type") if top else None,
                "boundingbox": top.get("boundingbox") if top else None,
            }
        except Exception as exc:  # record failures rather than inventing values
            log["results"][key] = {"query": q, "matched": False, "error": str(exc)}
        time.sleep(1.1)
    OUT.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT} ({sum(1 for v in log['results'].values() if v.get('matched'))}/{len(PLACES)} matched)")


if __name__ == "__main__":
    main()
