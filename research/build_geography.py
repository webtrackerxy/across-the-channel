#!/usr/bin/env python3
"""Build crossing-events.geojson and documented-routes.geojson (Phase 1A, Parts 3-4).

Inputs: this file's event/route specifications (every fact traced to a source id
and locator) and geocoding-log.json (OpenStreetMap Nominatim results written by
geocode_places.py). Coordinates come from (a) the source document itself when it
states them (MAIB reports) or (b) the gazetteer log for named places. No track is
drawn; route LineStrings are straight segments between two documented endpoints of
the same event and are labelled as such.

Usage: python3 build_geography.py      Stdlib only.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOG = json.loads((HERE / "geography" / "geocoding-log.json").read_text(encoding="utf-8"))["results"]
REVIEW = "source_checked_pending_independent_review"

P = "https://www.premar-manche.gouv.fr/communiques-presse/"
SRC = {
    "FR-GRAVELINES-2025": (P + "operation-de-d-assistance-et-de-secours-de-81-personnes-au-large-de-gravelines-59", "2025-07-19"),
    "FR-NOTICE-2021-03-09": (P + "sauvetage-de-deux-embarcations-de-migrants-en-manche", "2021-03-09"),
    "FR-NOTICE-2024-05-01": (P + "operation-d-assistance-et-de-sauvetage-de-66-personnes-au-large-de-dieppe-76", "2024-05-01"),
    "FR-NOTICE-2024-12-13": (P + "operations-de-sauvetage-de-120-migrants-dans-le-secteur-du-pas-de-calais-62-et-de-la-somme-80", "2024-12-13"),
    "FR-NOTICE-2025-02-09": (P + "bilan-des-operations-d-assistance-et-de-sauvetage-en-mer-dans-le-detroit-du-pas-de-calais-le-9-fevrier-2025", "2025-02-09"),
    "FR-NOTICE-2025-03-02": (P + "bilan-des-operations-d-assistance-et-de-sauvetage-du-dimanche-2-mars-2025-dans-le-detroit-du-pas-de-calais", "2025-03-02"),
    "FR-NOTICE-2025-04-18": (P + "bilan-des-operations-d-assistance-et-de-sauvetage-du-vendredi-18-avril-2025-au-large-du-pas-de-calais-62-et-du-nord-59", "2025-04-18"),
    "FR-NOTICE-2025-09-28": (P + "bilan-des-operations-d-assistance-et-de-sauvetage-sur-les-cotes-du-nord-59-du-pas-de-calais-62-et-de-la-seine-maritime-76-7666", "2025-09-29"),
    "FR-NOTICE-2025-11-06": (P + "bilan-des-operations-d-assistance-et-de-sauvetage-au-large-des-cotes-du-pas-de-calais-107-personnes-secourues", "2025-11-07"),
    "FR-NOTICE-2026-06-15": (P + "bilan-des-operations-d-assistance-et-de-sauvetage-en-manche-et-mer-du-nord", "2026-06-16"),
    "FR-NOTICE-2026-07-22": (P + "bilan-des-operations-d-assistance-et-de-sauvetage-des-22-et-23-juillet-2026-33-personnes-secourues", "2026-07-24"),
    "FR-NOTICE-2026-09-06": (P + "operation-d-assistance-d-une-embarcation-de-migrants-a-l-ouest-de-la-baie-de-seine", "2026-09-06"),
    "FR-REVIEW-2023": ("https://www.premar-manche.gouv.fr/uploads/manche/dossiers/ba713861efa97db824c081234264a739.pdf", "2024-02-02"),
    "MAIB-2021-INCIDENT": ("https://www.gov.uk/maib-reports/flooding-and-partial-sinking-of-an-inflatable-migrant-boat-with-at-least-27-lives-lost", "2023-11-08"),
    "MAIB-REPORT-7-2023": ("https://assets.publishing.service.gov.uk/media/654b77e8e70413000dfc49f0/2023-07-MigrantBoatReport.pdf", "2023-11-08"),
    "MAIB-REPORT-9-2024": ("https://assets.publishing.service.gov.uk/media/6731eeaf0a2b4132b43d13a3/2024-9-InflatableMigrantBoat-Report.pdf", "2024-08-15"),
    "BSC-2026": ("https://www.gov.uk/government/publications/border-security-commanders-annual-report-2025-to-2026/border-security-commanders-annual-report-2025-to-2026-accessible", "2026-07-16"),
    "VRT-2026-02-10": ("https://www.vrt.be/vrtnws/nl/2026/02/10/meer-transmigranten-mensensmokkel-westkust-politie/", "2026-02-10"),
    "VRT-2026-03-25": ("https://www.vrt.be/vrtnws/nl/2026/03/24/al-15-boten-met-transmigranten-vastgesteld-op-zee-sinds-begin-di/", "2026-03-25"),
    "VRT-2026-04-18": ("https://www.vrt.be/vrtnws/nl/2026/04/18/transmigranten-kust-provinciaal-noodplan-opgestart-overleg-gouve/", "2026-04-18"),
    "VRT-2026-06-03": ("https://www.vrt.be/vrtnws/nl/2026/06/03/geen-bootjes-met-transmigranten-meer-aan-onze-kust-sinds-1-mei/", "2026-06-03"),
    "ICI-2025-08-20": ("https://www.ici.fr/infos/economie-social/traversees-de-la-manche-deja-deux-fois-plus-de-migrants-interceptes-en-seine-maritime-cette-annee-qu-en-2024-3325909", "2025-08-20"),
    "ICI-2026-09-07": ("https://www.ici.fr/normandie/manche-50/les-140-migrants-partis-de-la-manche-sont-arrives-en-angleterre-ou-une-manifestation-a-eclate-8847927", "2026-09-07"),
    "HO-LAST7-2026-09-10": ("https://www.gov.uk/government/publications/migrants-detected-crossing-the-english-channel-in-small-boats/migrants-detected-crossing-the-english-channel-in-small-boats-last-7-days", "2026-09-10"),
}


def ev(sid, locator):
    url, date = SRC[sid]
    return {"source_id": sid, "url": url, "publication_date": date, "locator": locator}


def gaz(key):
    r = LOG[key]
    if not r.get("matched"):
        raise SystemExit(f"gazetteer key {key} did not match; refusing to invent coordinates")
    coords = [round(r["lon"], 6), round(r["lat"], 6)]
    src = (f"OpenStreetMap Nominatim search; query '{r['query']}'; top result '{r['display_name']}' "
           f"({r['osm_type']} {r['osm_id']}, {r['category']}/{r['type']}); geocoding-log.json key '{key}'")
    return coords, src


def mid(k1, k2):
    a, _ = gaz(k1)
    b, _ = gaz(k2)
    coords = [round((a[0] + b[0]) / 2, 6), round((a[1] + b[1]) / 2, 6)]
    return coords, (f"Arithmetic midpoint of Nominatim results '{k1}' and '{k2}' (geocoding-log.json); "
                    "representative point for a named stretch of coast, not a site")


def dm(lat_deg, lat_min, lon_deg, lon_min, text):
    """Degrees + decimal minutes (N/E) from the source document."""
    return [round(lon_deg + lon_min / 60, 6), round(lat_deg + lat_min / 60, 6)], text


def L(role, name, ltype, prec, unc, cs=None, note=None):
    coords, src = cs if cs else (None, None)
    d = {"role": role, "name": name, "location_type": ltype, "location_precision": prec,
         "uncertainty_km": unc, "coordinates": coords, "geometry_source": src}
    if note:
        d["note"] = note
    return d


RL, OL = "REPORTED LOCATION", "OBSERVED LOCATION"

# ---------------------------------------------------------------------------
# Events. 'primary' is the index into 'locs' used as the Feature geometry (None -> null).
# ---------------------------------------------------------------------------
EVENTS = [
    dict(id="EVENT-GRAVELINES-2025", event_type="departure_reported_then_french_rescue", event_date="2025-07-19",
         date_precision="day", sector="FR-59-Nord",
         locs=[L("departure_area", "Secteur de Gravelines (59)", RL, "named_area", 5, gaz("gravelines")),
               L("french_disembarkation", "Calais (62), 'déposées à quai'", RL, "named_place", 3, gaz("calais"))],
         primary=0, origin_area="Gravelines sector, Nord (59), France",
         dest="Rescued at sea by PSP Cormoran after requesting assistance; all 81 landed at Calais (France)",
         passengers=81, boats=1, vessel_info=None, uk_arrival=False,
         claim_ids=["GRAVELINES-2025"], classification="DOCUMENTED_EVENT", confidence="HIGH",
         evidence=[ev("FR-GRAVELINES-2025", "Notice text: 'alerté du départ d'une embarcation de migrants dans le secteur de Gravelines (59)'; 'déposées à quai à Calais'")],
         notes="Migrated from the seed file (REPORTED EVENT -> DOCUMENTED_EVENT: primary official notice). French rescue; not a UK arrival."),
    dict(id="EVENT-MAIB-2021", event_type="maritime_casualty", event_date="2021-11-24", date_precision="day",
         sector="FR-59-Nord",
         locs=[L("last_reported_position", "Last reported position (MAIB)", RL, "exact_coordinates", 2,
                 dm(51, 9.045, 1, 45.568, "MAIB report 7/2023, marine casualty information (PDF p.11): 'Last reported position: 51° 09.045N 001° 45.568E'"),
                 note="Position reported from the boat by telephone/WhatsApp; MAIB states the exact sinking time and position are unknown."),
               L("departure_area", "Beach near Dunkirk, France (departed about 2100 UTC, 23 Nov 2021)", RL, "named_area", 15, gaz("dunkerque")),
               L("observed_position", "Bodies sighted by FV Saint Jacques II, about 9 nm from Calais", OL, "exact_coordinates", 1,
                 dm(51, 5.58, 1, 43.41, "MAIB report 7/2023 §1.3.3 (PDF p.14): '51° 05.58N 001° 43.41E, about 9 nautical miles (nm) from Calais'")),
               L("reported_position", "Mayday Relay position based on 0201 WhatsApp position", RL, "exact_coordinates", 2,
                 dm(51, 8.5, 1, 44.5, "MAIB report 7/2023 (PDF p.20): 'Small craft with 40 persons on board in position 51°08.5N 001°44.5E'"))],
         primary=0, origin_area="Beach near Dunkirk, France",
         dest="Intended: UK coastline; 27 bodies and two survivors recovered from French waters and taken to France",
         passengers=33, boats=1, vessel_info="Inflatable, length overall about 8 m (MAIB)", uk_arrival=False,
         claim_ids=["MAIB-2021", "GEO-MAIB-2021-ENDPOINTS"], classification="DOCUMENTED_EVENT", confidence="HIGH",
         evidence=[ev("MAIB-2021-INCIDENT", "Summary"),
                   ev("MAIB-REPORT-7-2023", "PDF p.9 synopsis; PDF p.11 vessel/voyage particulars ('Port of departure Near Dunkirk, France'); PDF p.14 §1.3.2-1.3.3; PDF p.20 Mayday Relay")],
         notes="Passenger figure is MAIB's 'about 33'. The Mayday-relay text said 40 persons; keep both. Positions are reported, not a track."),
    dict(id="EVENT-DOVER-VALIANT-2021-11-24", event_type="uk_disembarkation", event_date="2021-11-24", date_precision="day",
         sector=None,
         locs=[L("uk_disembarkation", "Dover (Border Force cutter Valiant berthed about 0816 UTC)", RL, "named_place", 2, gaz("port-of-dover"),
                 note="MAIB states 'Valiant berthed in Dover'; berth not specified. Gazetteer point is Port of Dover Eastern Docks.")],
         primary=0, origin_area="Three migrant boats met by Valiant in UK waters of the Dover Strait (UK incidents Charlie, Lima, November per trackers)",
         dest="Disembarked at Dover", passengers=98, boats=3, vessel_info=None, uk_arrival=True,
         claim_ids=["GEO-DOVER-DISEMBARK-2021"], classification="DOCUMENTED_EVENT", confidence="HIGH",
         evidence=[ev("MAIB-REPORT-7-2023", "PDF p.29 ('At 0816, Valiant berthed in Dover and began disembarking migrants'); PDF p.33 ('With 98 migrants on board ... returned to Dover')")],
         notes="UK disembarkation site, not an interception point or intended landfall."),
    dict(id="EVENT-BELGIUM-2026", event_type="reported_departure_pattern", event_date=None, date_precision="year",
         sector="BE-West-Flanders",
         locs=[L("departure_area", "Belgian coast (West Flanders): beaches and Nieuwpoort marina", RL, "region", None)],
         primary=None, origin_area="Belgian coast; Belgian federal police spokesperson: departures 'vanop een Belgisch strand of uit de jachthaven van Nieuwpoort'",
         dest="Westkust police: taxi-boat legs along the coast towards France before the crossing; 18 Apr 2026 boats escorted to French waters. UK arrivals are not disaggregated by departure country",
         passengers=None, boats=None, vessel_info=None, uk_arrival=None,
         claim_ids=["BELGIUM-2026", "GEO-BSC-DISPLACEMENT", "GEO-BE-2026-COUNTS", "GEO-BE-2026-PAUSE"],
         classification="REPORTED_EVENT", confidence="MEDIUM",
         evidence=[ev("BSC-2026", "Case study: UK France collaboration ('taxi boats departing from less convenient locations on the Belgian coast'); threat section ('a small number further north in Belgium')"),
                   ev("VRT-2026-03-25", "Quote of federal police spokesperson An Berger: 15 departures since early January; 0, 1 or max 2 per year before"),
                   ev("VRT-2026-06-03", "'In totaal zijn er dit jaar 33 interventies geweest met bootjes'; none since 1 May")],
         notes="Reporting period 2026 (January to at least May). Belgian primary police page (politie.be) returned HTTP 403/maintenance and was not read."),
    dict(id="EVENT-BELGIUM-2026-04-18", event_type="interception_and_escort", event_date="2026-04-18", date_precision="day",
         sector="BE-West-Flanders",
         locs=[L("interception_area", "Belgian coast between Oostduinkerke and Middelkerke (sightings also at Koksijde and Bredene)", RL, "named_area", 15, mid("oostduinkerke", "middelkerke"))],
         primary=0, origin_area="Belgian coast, West Flanders",
         dest="Police escorted the boats towards French waters", passengers=200, boats=5, vessel_info=None, uk_arrival=None,
         claim_ids=["GEO-BE-2026-ESCORT"], classification="REPORTED_EVENT", confidence="MEDIUM",
         evidence=[ev("VRT-2026-04-18", "Lead: 'Tussen Oostduinkerke en Middelkerke zijn afgelopen nacht en ochtend 5 boten onderschept met in totaal 200 transmigranten ... begeleiden richting Franse wateren'")],
         notes="News report quoting the provincial governor; passenger count approximate ('in totaal 200')."),
    dict(id="EVENT-KOKSIJDE-2026-02-08", event_type="departure_attempts", event_date="2026-02-08", date_precision="day_derived_from_relative_reference",
         sector="BE-West-Flanders",
         locs=[L("departure_area", "Koksijde (West Flanders)", RL, "named_area", 5, gaz("koksijde")),
               L("passenger_pickup_site", "Dunes of Oostduinkerke and Nieuwpoort (general description)", RL, "named_area", 8, None)],
         primary=0, origin_area="Koksijde; police describe pickups from the dunes of Oostduinkerke and Nieuwpoort",
         dest="Police chief: boats continue along the coastline towards France; the crossing is made from France",
         passengers=None, boats=3, vessel_info=None, uk_arrival=None,
         claim_ids=["GEO-BE-TAXI-TO-FRANCE"], classification="REPORTED_EVENT", confidence="MEDIUM",
         evidence=[ev("VRT-2026-02-10", "'dit jaar waren er al minstens 5 pogingen, waarvan 3 zondagnacht in Koksijde. Die nacht werden ook 13 transmigranten opgepakt'")],
         notes="Date derived: article published Tuesday 10 Feb 2026 refers to 'zondagnacht' (night of Sunday 8 Feb). 13 people arrested; passengers aboard not stated."),
    dict(id="EVENT-BERNEVAL-2021-03-09", event_type="attempted_crossing_french_rescue", event_date="2021-03-09", date_precision="day",
         sector="FR-76-Seine-Maritime",
         locs=[L("rescue_location", "Off Berneval-le-Grand (76), crossing attempt initiated", RL, "named_area", 5, gaz("berneval-le-grand")),
               L("french_disembarkation", "Dieppe", RL, "named_place", 3, gaz("dieppe"))],
         primary=0, origin_area="Off Berneval-le-Grand, Seine-Maritime (76) (launch site not stated)",
         dest="33 taken aboard Yser and Armoise; landed at Dieppe", passengers=33, boats=1,
         vessel_info="Semi-rigid boat about 8 m", uk_arrival=False,
         claim_ids=["GEO-SEINE-MARITIME-NOTICES"], classification="DOCUMENTED_EVENT", confidence="HIGH",
         evidence=[ev("FR-NOTICE-2021-03-09", "'une embarcation de migrants initie une dangereuse tentative de traversée de la Manche au large de Berneval-le-Grand (76)'; 'déposés à Dieppe'")],
         notes="Shows Seine-Maritime activity already in March 2021."),
    dict(id="EVENT-DIEPPE-2024-05-01", event_type="at_sea_rescue", event_date="2024-05-01", date_precision="day",
         sector="FR-76-Seine-Maritime",
         locs=[L("rescue_location", "Off Dieppe (76)", RL, "named_area", 10, gaz("dieppe")),
               L("french_disembarkation", "Port of Dieppe", RL, "named_place", 3, gaz("dieppe"))],
         primary=0, origin_area="Not stated; boat reported off Dieppe by the Dieppe semaphore",
         dest="66 rescued by VCSM Yser; landed at the port of Dieppe", passengers=66, boats=1, vessel_info=None, uk_arrival=False,
         claim_ids=["GEO-SEINE-MARITIME-NOTICES"], classification="DOCUMENTED_EVENT", confidence="HIGH",
         evidence=[ev("FR-NOTICE-2024-05-01", "'une embarcation de migrants se trouve au large de Dieppe (76)'; '66 naufragés ... déposés au port de Dieppe'")],
         notes="Passengers = people rescued; total aboard not stated."),
    dict(id="EVENT-HARDELOT-2024-12-13", event_type="at_sea_rescue", event_date="2024-12-13", date_precision="day",
         sector="FR-62-south-of-Boulogne",
         locs=[L("rescue_location", "Secteur de Hardelot (62)", RL, "named_area", 5, gaz("hardelot")),
               L("french_disembarkation", "Port of Boulogne-sur-Mer", RL, "named_place", 3, gaz("boulogne-sur-mer"))],
         primary=0, origin_area="Pas-de-Calais / Somme coasts (numerous departures that night)",
         dest="37 rescued by Borda after engine failure; landed at Boulogne-sur-Mer", passengers=37, boats=1, vessel_info=None, uk_arrival=False,
         claim_ids=["GEO-SOMME-DEPARTURES"], classification="DOCUMENTED_EVENT", confidence="HIGH",
         evidence=[ev("FR-NOTICE-2024-12-13", "'surveillance d'une embarcation de migrants dans le secteur de Hardelot (62)'; 'dépose à terre au port de Boulogne-sur-Mer'")]),
    dict(id="EVENT-AMBLETEUSE-2024-12-13", event_type="departure_reported_then_french_rescue", event_date="2024-12-13", date_precision="day",
         sector="FR-62-Calais-Boulogne",
         locs=[L("departure_area", "Off Ambleteuse (62), departure reported", RL, "named_area", 5, gaz("ambleteuse")),
               L("french_disembarkation", "Boulogne-sur-Mer", RL, "named_place", 3, gaz("boulogne-sur-mer"))],
         primary=0, origin_area="Ambleteuse, Pas-de-Calais (62)",
         dest="39 taken aboard Abeille Normandie, then the rest after engine loss; 75 landed at Boulogne-sur-Mer", passengers=75, boats=1,
         vessel_info=None, uk_arrival=False,
         claim_ids=["GEO-SOMME-DEPARTURES"], classification="DOCUMENTED_EVENT", confidence="HIGH",
         evidence=[ev("FR-NOTICE-2024-12-13", "'au large d'Ambleteuse (62), un autre départ de migrants est signalé'; 'ce sont 75 personnes qui sont secourues et ramenées à quai à Boulogne-sur-Mer'")]),
    dict(id="EVENT-SAINT-VALERY-2024-12-13", event_type="stranded_boat_rescue", event_date="2024-12-13", date_precision="day",
         sector="FR-80-Somme",
         locs=[L("stranding_location", "Port of Saint-Valery-sur-Somme (80)", RL, "named_place", 2, gaz("saint-valery-sur-somme"))],
         primary=0, origin_area="Somme coast (numerous departures reported off Pas-de-Calais and Somme)",
         dest="8 migrants recovered by SNSM Cayeux-sur-Mer semi-rigids and landed on the beach", passengers=8, boats=1,
         vessel_info=None, uk_arrival=False,
         claim_ids=["GEO-SOMME-DEPARTURES"], classification="DOCUMENTED_EVENT", confidence="HIGH",
         evidence=[ev("FR-NOTICE-2024-12-13", "'une embarcation échouée au niveau du port de Saint-Valéry-sur-Somme (80)'; 'huit migrants'")]),
    dict(id="EVENT-PETIT-FORT-PHILIPPE-2025-02-09", event_type="at_sea_rescue_partial", event_date="2025-02-09", date_precision="day",
         sector="FR-59-Nord",
         locs=[L("rescue_location", "Off Petit-Fort-Philippe (59)", RL, "named_area", 5, gaz("petit-fort-philippe"))],
         primary=0, origin_area="Not stated", dest="19 rescued by Abeille Normandie; boat with 40 others continued towards the British coast without requesting assistance",
         passengers=59, boats=1, vessel_info=None, uk_arrival=None,
         claim_ids=["GEO-FR-NOTICES-CORE"], classification="DOCUMENTED_EVENT", confidence="HIGH",
         evidence=[ev("FR-NOTICE-2025-02-09", "'au large de Petit-Fort-Philippe (59)'; '19 personnes sont alors secourues, tandis que l'embarcation, comptant 40 autres personnes poursuivi sa route vers les côtes britanniques'")]),
    dict(id="EVENT-MALO-2025-02-09", event_type="departure_reported_partial_rescue", event_date="2025-02-09", date_precision="day",
         sector="FR-59-Nord",
         locs=[L("departure_area", "Malo-les-Bains (59)", RL, "named_area", 3, gaz("malo-les-bains"))],
         primary=0, origin_area="Malo-les-Bains, Dunkerque (59)",
         dest="42 recovered by PSP Cormoran (2 injured airlifted to Boulogne-sur-Mer hospital); 17 continued without requesting assistance",
         passengers=59, boats=1, vessel_info=None, uk_arrival=None,
         claim_ids=["GEO-FR-NOTICES-CORE"], classification="DOCUMENTED_EVENT", confidence="HIGH",
         evidence=[ev("FR-NOTICE-2025-02-09", "'Une quatrième embarcation est signalée au départ de Malo-les-Bains (59)'; '42 personnes ... récupérées'; 'encore 17 personnes continue sa route'")]),
    dict(id="EVENT-BAIE-DE-SOMME-2025-02-09", event_type="launch_then_pickup_attempt", event_date="2025-02-09", date_precision="day",
         sector="FR-80-Somme",
         locs=[L("launch_site", "Secteur de la Baie de Somme (80)", RL, "named_area", 10, gaz("baie-de-somme")),
               L("passenger_pickup_site", "Beaches of Berck-sur-Mer (62), attempted embarkation", RL, "named_area", 4, gaz("berck-sur-mer"))],
         primary=0, origin_area="Baie de Somme sector (80); left early morning",
         dest="Attempted embarkation at Berck-sur-Mer (41 people unable to board rescued on the coast); 33 rescued at sea about 20:00 by PAM Jeanne Barret",
         passengers=33, boats=1, vessel_info=None, uk_arrival=False,
         claim_ids=["GEO-SOMME-DEPARTURES"], classification="DOCUMENTED_EVENT", confidence="HIGH",
         evidence=[ev("FR-NOTICE-2025-02-09", "'33 personnes sur une embarcation, partie tôt dans la matinée depuis le secteur de la Baie de Sommme. Cette opération fait suite à une tentative d'embarquement, au niveau des plages de Berck-sur-Mer (62)'")],
         notes="Launch site and passenger pickup site differ (taxi-boat pattern)."),
    dict(id="EVENT-POINTE-AUX-OIES-2025-03-02", event_type="departure_reported_partial_rescue", event_date="2025-03-02", date_precision="day",
         sector="FR-62-Calais-Boulogne",
         locs=[L("departure_area", "Near Wimereux (62), secteur de la Pointe aux Oies", RL, "named_place", 2, gaz("pointe-aux-oies"),
                 note="Nominatim matched a gîte named 'La Pointe aux Oies' on Chemin des Oies, Wimereux; used as proxy for the headland sector."),
               L("french_disembarkation", "Boulogne-sur-Mer", RL, "named_place", 3, gaz("boulogne-sur-mer"))],
         primary=0, origin_area="Wimereux, Pointe aux Oies sector (62)",
         dest="3 rescued by Géranium and landed at Boulogne-sur-Mer; the rest continued under French surveillance", passengers=None, boats=1,
         vessel_info=None, uk_arrival=None,
         claim_ids=["GEO-FR-NOTICES-CORE"], classification="DOCUMENTED_EVENT", confidence="HIGH",
         evidence=[ev("FR-NOTICE-2025-03-02", "'un départ d'embarcation de migrants proche de Wimereux (62), secteur de la Pointe aux Oies'; 'ramenées à Boulogne-sur-Mer'")]),
    dict(id="EVENT-BAIE-DE-SOMME-2025-03-02", event_type="launch_then_stranding", event_date="2025-03-02", date_precision="day",
         sector="FR-80-Somme",
         locs=[L("launch_site", "Off the Baie de Somme (80), left in the morning", RL, "named_area", 10, gaz("baie-de-somme")),
               L("stranding_location", "Beach near the north dyke of Hardelot (62)", RL, "named_place", 2, gaz("hardelot"))],
         primary=0, origin_area="Baie de Somme (80)",
         dest="Boat stranded on the beach near the north dyke of Hardelot; 54 aboard assisted; three injured (one critical)",
         passengers=54, boats=1, vessel_info="'embarcation de fortune'", uk_arrival=False,
         claim_ids=["GEO-SOMME-DEPARTURES"], classification="DOCUMENTED_EVENT", confidence="HIGH",
         evidence=[ev("FR-NOTICE-2025-03-02", "'une embarcation de fortune, parti le matin au large de la Baie de Somme'; '54 personnes à bord'; 'échouée sur la plage proche de la digue Nord de Hardelot'")]),
    dict(id="EVENT-CAP-BLANC-NEZ-2025-04-18", event_type="departure_monitored_to_uk_srr", event_date="2025-04-18", date_precision="day",
         sector="FR-62-Calais-Boulogne",
         locs=[L("departure_area", "Cap Blanc-Nez (62)", RL, "named_place", 2, gaz("cap-blanc-nez")),
               L("uk_reception_area", "British search and rescue region; victim declared dead 'à l'approche de Douvres'", RL, "named_area", 10, gaz("dover"))],
         primary=0, origin_area="Cap Blanc-Nez, Pas-de-Calais (62)",
         dest="Monitored by PSP Cormoran into the UK SRR, where British rescue services took charge; one person declared dead by British services approaching Dover",
         passengers=None, boats=1, vessel_info=None, uk_arrival=None,
         claim_ids=["GEO-2025-04-18-UK-HANDOVER"], classification="DOCUMENTED_EVENT", confidence="HIGH",
         evidence=[ev("FR-NOTICE-2025-04-18", "'une embarcation est signalée au départ du cap Blanc -Nez (62)'; 'jusqu'à arriver en zone de responsabilité (Search and Rescue Region) britannique'; 'déclarée décédée ... à l'approche de Douvres'")],
         notes="uk_arrival left null: the notice states British rescue took charge but does not state where occupants were landed."),
    dict(id="EVENT-GRAVELINES-2025-04-18", event_type="departure_reported_then_french_rescue", event_date="2025-04-18", date_precision="day",
         sector="FR-59-Nord",
         locs=[L("departure_area", "Gravelines (59), drifting boat after departure", RL, "named_area", 5, gaz("gravelines")),
               L("french_disembarkation", "Port of Dunkerque (59)", RL, "named_area", 10, gaz("dunkerque-port"),
                 note="Port of Dunkirk spans West (Loon-Plage) and East basins; berth not stated.")],
         primary=0, origin_area="Gravelines (59)", dest="All 9 occupants taken aboard VCSM Oyapock; landed at the port of Dunkerque",
         passengers=9, boats=1, vessel_info=None, uk_arrival=False,
         claim_ids=["GEO-FR-NOTICES-CORE"], classification="DOCUMENTED_EVENT", confidence="HIGH",
         evidence=[ev("FR-NOTICE-2025-04-18", "'une embarcation de migrants à la dérive au départ de Gravelines'; 'l'ensemble des 9 occupants ... au port de Dunkerque (59)'")]),
    dict(id="EVENT-EQUIHEN-2025-04-18", event_type="departure_reported_partial_rescue", event_date="2025-04-18", date_precision="day",
         sector="FR-62-south-of-Boulogne",
         locs=[L("departure_area", "Equihen-Plage (62)", RL, "named_place", 2, gaz("equihen-plage"))],
         primary=0, origin_area="Equihen-Plage (62)",
         dest="Tube deflation; 15 rescued by PSP Pluvier; others refused assistance and continued towards British waters",
         passengers=None, boats=1, vessel_info="Heavily loaded inflatable ('boudins')", uk_arrival=None,
         claim_ids=["GEO-FR-NOTICES-CORE"], classification="DOCUMENTED_EVENT", confidence="HIGH",
         evidence=[ev("FR-NOTICE-2025-04-18", "'une embarcation de migrants prend la mer depuis Equihen-Plage (62)'; '15 personnes sont secourues'; 'en direction des eaux britanniques'")]),
    dict(id="EVENT-EQUIHEN-2025-09-28", event_type="at_sea_rescue", event_date="2025-09-28", date_precision="day",
         sector="FR-62-south-of-Boulogne",
         locs=[L("departure_area", "Off the beach of Equihen (62)", RL, "named_place", 2, gaz("equihen-plage")),
               L("french_disembarkation", "Boulogne-sur-Mer", RL, "named_place", 3, gaz("boulogne-sur-mer"))],
         primary=0, origin_area="Plage d'Equihen (62)", dest="Propulsion failure; all 50 taken aboard Minck and landed at Boulogne-sur-Mer",
         passengers=50, boats=1, vessel_info=None, uk_arrival=False,
         claim_ids=["GEO-FR-NOTICES-CORE"], classification="DOCUMENTED_EVENT", confidence="HIGH",
         evidence=[ev("FR-NOTICE-2025-09-28", "'une embarcation transportant des migrants face à la plage d'Equihen (62)'; 'Les 50 occupants ... ramenés à quai à Boulogne-sur-Mer'")]),
    dict(id="EVENT-DIEPPE-STELLA-2025-09-28", event_type="taxi_boat_coastal_leg", event_date="2025-09-28", date_precision="day",
         sector="FR-76-Seine-Maritime",
         locs=[L("first_detection_at_sea", "Off Dieppe (76), group already 'en cours de passage par voie de mer' at about 04:30", RL, "named_area", 10, gaz("dieppe")),
               L("passenger_pickup_site", "North of Stella-Plage (62), embarkation of more migrants at 14:25", RL, "named_area", 5, gaz("stella-plage"))],
         primary=0, origin_area="Seine-Maritime coast off Dieppe (launch point not stated)",
         dest="Boat 'remonte le long des côtes vers le Nord', embarked more people north of Stella-Plage, then headed for the UK under French surveillance",
         passengers=None, boats=1, vessel_info=None, uk_arrival=None,
         claim_ids=["GEO-TAXI-DIEPPE-STELLA-2025"], classification="DOCUMENTED_EVENT", confidence="HIGH",
         evidence=[ev("FR-NOTICE-2025-09-28", "'un groupe de migrants en cours de passage par voie de mer au large de Dieppe'; 'l'embarcation qui remonte le long des côtes vers le Nord'; 'se dirige vers le Nord de Stella Plage pour embarquer d'autres migrants'")],
         notes="First detection off Dieppe and the passenger pickup north of Stella-Plage are about 71 km apart (straight line, see route-analysis.json); the boat then headed for the UK from the Pas-de-Calais coast."),
    dict(id="EVENT-ECAULT-2025-09-28", event_type="departure_beaching_relaunch_uk_pickup", event_date="2025-09-28", date_precision="day",
         sector="FR-62-south-of-Boulogne",
         locs=[L("launch_site", "Plage d'Écault (62)", RL, "named_place", 2, gaz("ecault")),
               L("uk_reception_area", "Recovered by British authorities (location not stated)", RL, "unknown", None, None)],
         primary=0, origin_area="Plage d'Écault (62)",
         dest="Beached at 07:00 and dropped 49 occupants (one adolescent died); relaunched 07:47; relocated off Cap d'Alprech; monitored until its occupants were taken aboard by British authorities",
         passengers=None, boats=1, vessel_info=None, uk_arrival=True,
         claim_ids=["GEO-FR-NOTICES-CORE"], classification="DOCUMENTED_EVENT", confidence="HIGH",
         evidence=[ev("FR-NOTICE-2025-09-28", "'vient juste de quitter la plage d'Ecault (62)'; 'y dépose 49 de ses occupants'; 'jusqu'au recueil de ses occupants par les autorités britanniques'")],
         notes="uk_arrival true because the notice states the occupants were taken aboard by British authorities; UK landing port not stated."),
    dict(id="EVENT-LEFFRINCKOUCKE-2025-09-28", event_type="taxi_boat_launch_and_pickup", event_date="2025-09-28", date_precision="day",
         sector="FR-59-Nord",
         locs=[L("launch_site", "Beach of Leffrinckoucke (59)", RL, "named_place", 2, gaz("leffrinckoucke")),
               L("passenger_pickup_site", "Beach of Malo-les-Bains (59), where a new group was waiting", RL, "named_place", 2, gaz("malo-les-bains")),
               L("french_disembarkation", "Calais (66 rescued)", RL, "named_place", 3, gaz("calais"))],
         primary=0, origin_area="Leffrinckoucke (59)",
         dest="Headed for the UK at 09:40; engine failure; 66 rescued by Ridens (landing planned at Calais); the rest continued towards the UK",
         passengers=None, boats=1, vessel_info=None, uk_arrival=None,
         claim_ids=["GEO-FR-NOTICES-CORE"], classification="DOCUMENTED_EVENT", confidence="HIGH",
         evidence=[ev("FR-NOTICE-2025-09-28", "'un départ d'embarcation est signalé au CROSS depuis la plage de Leffrinckoucke (59)'; 'en route vers la plage de Malo-les-Bains ou un nouveau groupe de migrant l'attend'; '66 personnes'; 'Le débarquement est prévu à Calais'")]),
    dict(id="EVENT-DUNKERQUE-2025-11-06", event_type="shipwreck_french_rescue", event_date="2025-11-06", date_precision="day",
         sector="FR-59-Nord",
         locs=[L("rescue_location", "Off Dunkerque (59)", RL, "named_area", None, None)],
         primary=None, origin_area="Not stated", dest="94 rescued by French state services after a boat foundered; landing port per boat not stated (notice lists Calais and Boulogne-sur-Mer for other operations)",
         passengers=94, boats=1, vessel_info=None, uk_arrival=False,
         claim_ids=["GEO-FR-NOTICES-CORE"], classification="DOCUMENTED_EVENT", confidence="HIGH",
         evidence=[ev("FR-NOTICE-2025-11-06", "'Suite au naufrage d'une embarcation au large de Dunkerque (59), 94 personnes ont été secourues'")],
         notes="Offshore area only; geometry null (no false point)."),
    dict(id="EVENT-WALDE-2025-11-06", event_type="stranded_boat_rescue", event_date="2025-11-06", date_precision="day",
         sector="FR-62-Calais-Boulogne",
         locs=[L("stranding_location", "Sandbank, secteur du phare de Walde (62)", RL, "named_area", 2, gaz("phare-de-walde")),
               L("french_disembarkation", "Calais", RL, "named_place", 3, gaz("calais"))],
         primary=0, origin_area="Not stated", dest="One boat: 1 rescued, landed at Calais, boat resumed its route; another: all 7 rescued, landed at Calais",
         passengers=None, boats=2, vessel_info=None, uk_arrival=None,
         claim_ids=["GEO-FR-NOTICES-CORE"], classification="DOCUMENTED_EVENT", confidence="HIGH",
         evidence=[ev("FR-NOTICE-2025-11-06", "'une embarcation de migrants est échouée sur un banc de sable dans le secteur du phare de Walde (62)'; 'l'ensemble des 7 personnes à bord demande assistance'")]),
    dict(id="EVENT-BERCK-2025-11-06", event_type="embarkation_phase_rescue", event_date="2025-11-06", date_precision="day",
         sector="FR-62-south-of-Boulogne",
         locs=[L("passenger_pickup_site", "Secteur Berck-sur-Mer (62), boat in difficulty during embarkation phase", RL, "named_area", 5, gaz("berck-sur-mer"))],
         primary=0, origin_area="Not stated (reported by Ault semaphore)",
         dest="1 person rescued from the water during embarkation; 1 more rescued during surveillance and landed at Boulogne-sur-Mer",
         passengers=None, boats=1, vessel_info=None, uk_arrival=None,
         claim_ids=["GEO-FR-NOTICES-CORE"], classification="DOCUMENTED_EVENT", confidence="HIGH",
         evidence=[ev("FR-NOTICE-2025-11-06", "'le sémaphore d'Ault reporte une embarcation de migrants en difficulté secteur Berck-sur-Mer (62)'; 'Au cours de la phase d'embarquement'")]),
    dict(id="EVENT-CAYEUX-2026-06-15", event_type="departure_reported_partial_rescue", event_date="2026-06-15", date_precision="day",
         sector="FR-80-Somme",
         locs=[L("departure_area", "Secteur de Cayeux-sur-Mer (80)", RL, "named_area", 5, gaz("cayeux-sur-mer")),
               L("french_disembarkation", "Port of Boulogne-sur-Mer", RL, "named_place", 3, gaz("boulogne-sur-mer"))],
         primary=0, origin_area="Cayeux-sur-Mer sector, Somme (80)", dest="3 taken aboard Abeille Normandie; landed at Boulogne-sur-Mer",
         passengers=None, boats=1, vessel_info=None, uk_arrival=None,
         claim_ids=["GEO-SOMME-DEPARTURES"], classification="DOCUMENTED_EVENT", confidence="HIGH",
         evidence=[ev("FR-NOTICE-2026-06-15", "'le sémaphore d'Ault (80) signale au CROSS le départ d'une embarcation depuis le secteur de Cayeux-sur-Mer (80)'; 'débarquées en sécurité au port de Boulogne-sur-Mer (62)'")]),
    dict(id="EVENT-DIEPPE-SEMAPHORE-2026-06-15", event_type="at_sea_rescue_partial", event_date="2026-06-15", date_precision="day",
         sector="FR-76-Seine-Maritime",
         locs=[L("first_detection_at_sea", "Reported by the Dieppe semaphore (76); position not stated", RL, "unknown", None, None),
               L("french_disembarkation", "Port of Boulogne-sur-Mer", RL, "named_place", 3, gaz("boulogne-sur-mer"))],
         primary=None, origin_area="Not stated; detected by Dieppe semaphore",
         dest="30 rescued aboard BSAA Argonaute during the crossing; landed at Boulogne-sur-Mer", passengers=None, boats=1,
         vessel_info=None, uk_arrival=None,
         claim_ids=["GEO-SEINE-MARITIME-NOTICES"], classification="DOCUMENTED_EVENT", confidence="HIGH",
         evidence=[ev("FR-NOTICE-2026-06-15", "'Une seconde embarcation est signalée par le sémaphore de Dieppe (76)'; 'trente personnes sont secourues ... débarquées à quai au port de Boulogne-sur-Mer'")]),
    dict(id="EVENT-YPORT-BERCK-2026-07-22", event_type="taxi_boat_coastal_leg", event_date="2026-07-22/2026-07-23", date_precision="day_range",
         sector="FR-76-Seine-Maritime",
         locs=[L("launch_site", "Taking to sea off Yport (76) (Fécamp semaphore)", RL, "named_area", 5, gaz("yport")),
               L("passenger_pickup_site", "Beach of Berck-sur-Mer (62), new people boarded at dawn 23 July", RL, "named_area", 4, gaz("berck-sur-mer"))],
         primary=0, origin_area="Yport, Seine-Maritime (76)",
         dest="Engine failure but continued; at dawn on 23 July reached Berck-sur-Mer beach and took on new people; 2 rescued by Minck during the chaotic embarkation",
         passengers=None, boats=1, vessel_info=None, uk_arrival=None,
         claim_ids=["GEO-TAXI-YPORT-BERCK-2026"], classification="DOCUMENTED_EVENT", confidence="HIGH",
         evidence=[ev("FR-NOTICE-2026-07-22", "'le sémaphore de Fécamp signale une autre embarcation de migrants prenant la mer au large d'Yport (76)'; 'A l'aube du 23 juillet, l'embarcation rallie la plage de Berck-sur-Mer (62) et fait monter à bord de nouvelles personnes'")],
         notes="Coastal leg Yport -> Berck of about 117 km (straight line, see route-analysis.json) before the passenger pickup; destination after pickup not stated."),
    dict(id="EVENT-BAIE-DE-SOMME-2026-07-22", event_type="embarkation_phase_rescue", event_date="2026-07-22", date_precision="day",
         sector="FR-80-Somme",
         locs=[L("passenger_pickup_site", "Off the Baie de Somme (80), embarkation attempt", RL, "named_area", 10, gaz("baie-de-somme"))],
         primary=0, origin_area="Baie de Somme (80)", dest="3 rescued by SDIS 62 during an embarkation attempt and returned to the beach",
         passengers=None, boats=1, vessel_info=None, uk_arrival=None,
         claim_ids=["GEO-SOMME-DEPARTURES"], classification="DOCUMENTED_EVENT", confidence="HIGH",
         evidence=[ev("FR-NOTICE-2026-07-22", "'le sémaphore d'Ault signale une embarcation de migrants ... au large de la Baie de Somme (80)'; 'Au cours d'une tentative d'embarquement, trois personnes sont secourues'")]),
    dict(id="EVENT-HARDELOT-2026-07-23", event_type="at_sea_rescue_partial", event_date="2026-07-23", date_precision="day",
         sector="FR-62-south-of-Boulogne",
         locs=[L("departure_area", "Secteur d'Hardelot (62)", RL, "named_area", 5, gaz("hardelot")),
               L("french_disembarkation", "Port of Calais", RL, "named_place", 3, gaz("calais"))],
         primary=0, origin_area="Hardelot sector (62)", dest="Lifejackets distributed by PSP Flamant; 28 rescued during the crossing and landed at Calais",
         passengers=None, boats=1, vessel_info=None, uk_arrival=None,
         claim_ids=["GEO-FR-NOTICES-CORE"], classification="DOCUMENTED_EVENT", confidence="HIGH",
         evidence=[ev("FR-NOTICE-2026-07-22", "'une embarcation de migrants est signalée ... dans le secteur d'Hardelot (62)'; '28 personnes ... débarquées au port de Calais (62)'")]),
    dict(id="EVENT-NORMANDY-2026-09-06", event_type="departure_to_uk_arrival_reported", event_date="2026-09-06", date_precision="day",
         sector="FR-50-Manche",
         locs=[L("launch_site", "La Brèche, Utah Beach, Sainte-Marie-du-Mont (Manche, 50) - per the mayor, reported by ICI/AFP", RL, "named_place", 3, gaz("utah-beach"),
                 note="Nominatim did not match 'La Brèche'; hamlet 'Utah-Beach' used; Premar does not state the departure point."),
               L("first_detection_at_sea", "West of the Baie de Seine, near the Îles Saint-Marcouf (CROSS Jobourg)", RL, "named_area", 10, gaz("iles-saint-marcouf")),
               L("uk_arrival_area", "Portsmouth, England (reported by ICI/AFP; landing site not verified)", RL, "named_area", 10, gaz("portsmouth"),
                 note="A search snippet named Langstone Harbour and RNLI lifeboats; the ITV page could not be retrieved, so this is unverified.")],
         primary=0, origin_area="Utah Beach, Manche (50), Normandy (reported)",
         dest="Premar: 'poursuit sa route vers le Royaume-Uni'; ICI/AFP: arrived at Portsmouth on 6 Sep 2026",
         passengers=140, boats=1, vessel_info="Inflatable ('embarcation pneumatique', ICI); ~140 aboard ('environ 140', Premar)", uk_arrival=True,
         claim_ids=["GEO-NORMANDY-2026-PREMAR", "GEO-NORMANDY-2026-ENDPOINTS"], classification="REPORTED_EVENT", confidence="MEDIUM",
         evidence=[ev("FR-NOTICE-2026-09-06", "'environ 140 migrants est signalée au CROSS Jobourg, à l'ouest de la baie de Seine'; 'poursuit sa route vers le Royaume-Uni'; 'Si le départ d'une embarcation de migrants est inhabituel pour la zone'"),
                   ev("ICI-2026-09-07", "'partis dans une embarcation pneumatique de Utah Beach ... arrivés à Portsmouth'; 'Selon le maire de Sainte-Marie-du-Mont ... partie de Le Brèche sur la plage d'Utah Beach'"),
                   ev("HO-LAST7-2026-09-10", "Row '6 September 2026': 625 migrants, 8 boats (all arrivals that day; cannot be attributed to this boat)")],
         notes="Occurrence, size and heading are DOCUMENTED by Premar; departure beach and landfall rest on news (REPORTED). Single isolated case."),
    dict(id="EVENT-VARENGEVILLE-2025-08-14", event_type="prevented_departure_onshore", event_date="2025-08-14", date_precision="day",
         sector="FR-76-Seine-Maritime",
         locs=[L("prevented_launch_site", "Varengeville-sur-Mer (76)", RL, "named_area", 3, gaz("varengeville-sur-mer"))],
         primary=0, origin_area="Varengeville-sur-Mer, Seine-Maritime (76)", dest="49 people taken in charge on land (prevented crossing)",
         passengers=49, boats=None, vessel_info=None, uk_arrival=False,
         claim_ids=["GEO-SEINE-MARITIME-2025"], classification="REPORTED_EVENT", confidence="MEDIUM",
         evidence=[ev("ICI-2025-08-20", "'La dernière traversée interceptée était le 14 août dernier, quand 49 personnes ont été prises en charge à Varengeville-sur-Mer'")]),
    dict(id="EVENT-CALAIS-DOVER-2023-08-12", event_type="shipwreck_split_disembarkation", event_date="2023-08-12", date_precision="day",
         sector=None,
         locs=[L("rescue_location", "Dover Strait; boat reported by a merchant ship (position not given)", RL, "unknown", None, None),
               L("french_disembarkation", "Port of Calais (36 saved by French assets)", RL, "named_place", 3, gaz("calais")),
               L("uk_disembarkation", "Port of Dover (22-23 saved by British assets)", RL, "named_place", 2, gaz("port-of-dover"))],
         primary=None, origin_area="Not stated (several boats put to sea in the night of 11-12 Aug 2023)",
         dest="French assets saved 36 (landed at Calais); British assets saved 22-23 (landed at Port of Dover); 6 victims",
         passengers=66, boats=1, vessel_info=None, uk_arrival=True,
         claim_ids=["GEO-DOVER-DISEMBARK-2023"], classification="DOCUMENTED_EVENT", confidence="HIGH",
         evidence=[ev("FR-REVIEW-2023", "PDF pp.15-16, §3.2.1 'Retour sur une opération ... marquante': '65 à 66 personnes probablement'; 'déposées au port de Calais'; 'déposées au port de Douvres'")],
         notes="uk_arrival true for the 22-23 people landed at Dover only. Passengers = upper estimate '65 à 66'."),
    dict(id="EVENT-MAIB-2022", event_type="maritime_casualty", event_date="2022-12-14", date_precision="day",
         sector="FR-59/62-Calais-Dunkirk",
         locs=[L("observed_position", "Position where FV Arcturus found the boat (approximately 14.6 nm NW of Boulogne-sur-Mer)", OL, "exact_coordinates", 1,
                 dm(50, 52.12, 1, 16.19, "MAIB report 9/2024, casualty information (PDF p.12): 'Approximately 50°52.12'N 001°16.19'E'; narrative p.4 '50°52.1'N 001°16.2'E'")),
               L("reported_position", "GPS position sent to a charity volunteer at 0153", RL, "exact_coordinates", 0.5,
                 dm(50, 50.3, 1, 21.1, "MAIB report 9/2024 (PDF p.2): 'GPS location of 50°50.3'N 001°21.1'E'")),
               L("departure_area", "A beach in the Calais/Dunkirk area (launched about 2330, 13 Dec 2022)", RL, "region", 20, mid("calais", "dunkerque")),
               L("uk_disembarkation", "Dover (survivors handed to Border Force and Kent Police)", RL, "named_place", 2, gaz("port-of-dover"))],
         primary=0, origin_area="Beach in the Calais/Dunkirk area, France ('Between Calais and Dunkirk')",
         dest="Intended: UK coastline; 39 survivors recovered; Arcturus and lifeboats made passage to Dover, where survivors were handed to Border Force",
         passengers=47, boats=1, vessel_info="Inflatable, length overall 7.4 m; Chinese copy of a Yamaha two-stroke outboard; at least one additional fuel tank (MAIB)",
         uk_arrival=True, claim_ids=["GEO-MAIB-2022-ENDPOINTS"], classification="DOCUMENTED_EVENT", confidence="HIGH",
         evidence=[ev("MAIB-REPORT-9-2024", "PDF p.2 (launch 'from a beach in the Calais/Dunkirk area'; 'around 47 people'); PDF p.4 (found position); narrative ('On arrival, the survivors were handed into the custody of waiting Border Force'); PDF p.12 particulars ('Port of departure Between Calais and Dunkirk')")],
         notes="Passengers: 'around 47' (survivors estimated 40-47). At least 8 died."),
]

# ---------------------------------------------------------------------------
# Documented origin/destination pairs (same event). Index refers to EVENT locs.
# ---------------------------------------------------------------------------
ROUTES = [
    ("ROUTE-MAIB-2021-DEP-TO-LASTPOS", "EVENT-MAIB-2021", 1, 0, "departure_to_at_sea_position", True),
    ("ROUTE-MAIB-2022-DEP-TO-FOUND", "EVENT-MAIB-2022", 2, 0, "departure_to_at_sea_position", True),
    ("ROUTE-MAIB-2022-FOUND-TO-DOVER", "EVENT-MAIB-2022", 0, 3, "rescue_position_to_uk_disembarkation", False),
    ("ROUTE-2025-04-18-BLANC-NEZ-TO-DOVER", "EVENT-CAP-BLANC-NEZ-2025-04-18", 0, 1, "departure_to_uk_reception_area", True),
    ("ROUTE-2026-09-06-UTAH-TO-PORTSMOUTH", "EVENT-NORMANDY-2026-09-06", 0, 2, "departure_to_uk_arrival_area", True),
    ("ROUTE-2025-09-28-DIEPPE-TO-STELLA", "EVENT-DIEPPE-STELLA-2025-09-28", 0, 1, "launch_to_passenger_pickup_coastal_leg", False),
    ("ROUTE-2025-09-28-LEFFRINCKOUCKE-TO-MALO", "EVENT-LEFFRINCKOUCKE-2025-09-28", 0, 1, "launch_to_passenger_pickup_coastal_leg", False),
    ("ROUTE-2026-07-22-YPORT-TO-BERCK", "EVENT-YPORT-BERCK-2026-07-22", 0, 1, "launch_to_passenger_pickup_coastal_leg", False),
    ("ROUTE-2025-02-09-SOMME-TO-BERCK", "EVENT-BAIE-DE-SOMME-2025-02-09", 0, 1, "launch_to_passenger_pickup_coastal_leg", False),
    ("ROUTE-2025-03-02-SOMME-TO-HARDELOT", "EVENT-BAIE-DE-SOMME-2025-03-02", 0, 1, "launch_to_stranding_coastal_leg", False),
    ("ROUTE-2025-07-19-GRAVELINES-TO-CALAIS", "EVENT-GRAVELINES-2025", 0, 1, "departure_to_french_disembarkation", False),
    ("ROUTE-2024-12-13-AMBLETEUSE-TO-BOULOGNE", "EVENT-AMBLETEUSE-2024-12-13", 0, 1, "departure_to_french_disembarkation", False),
    ("ROUTE-2025-04-18-GRAVELINES-TO-DUNKERQUE", "EVENT-GRAVELINES-2025-04-18", 0, 1, "departure_to_french_disembarkation", False),
    ("ROUTE-2025-09-28-EQUIHEN-TO-BOULOGNE", "EVENT-EQUIHEN-2025-09-28", 0, 1, "departure_to_french_disembarkation", False),
    ("ROUTE-2026-06-15-CAYEUX-TO-BOULOGNE", "EVENT-CAYEUX-2026-06-15", 0, 1, "departure_to_french_disembarkation", False),
    ("ROUTE-2021-03-09-BERNEVAL-TO-DIEPPE", "EVENT-BERNEVAL-2021-03-09", 0, 1, "rescue_location_to_french_disembarkation", False),
    ("ROUTE-2025-03-02-POINTE-AUX-OIES-TO-BOULOGNE", "EVENT-POINTE-AUX-OIES-2025-03-02", 0, 1, "departure_to_french_disembarkation", False),
]


def feature_for_event(e):
    locs = e["locs"]
    prim = locs[e["primary"]] if e["primary"] is not None else None
    geom = {"type": "Point", "coordinates": prim["coordinates"]} if prim and prim["coordinates"] else None
    places = [l["name"] for l in locs]
    props = {
        "id": e["id"], "event_type": e["event_type"], "event_date": e["event_date"], "date_precision": e["date_precision"],
        "places": places,
        "location_type": prim["location_type"] if prim else locs[0]["location_type"],
        "location_precision": prim["location_precision"] if prim else locs[0]["location_precision"],
        "uncertainty_km": prim["uncertainty_km"] if prim else None,
        "geometry_source": prim["geometry_source"] if prim else None,
        "geometry_role": prim["role"] if prim else None,
        "origin_area": e["origin_area"], "origin_sector": e["sector"],
        "destination_or_interception_area": e["dest"],
        "passengers": e["passengers"], "boats": e["boats"], "vessel_info": e["vessel_info"], "uk_arrival": e["uk_arrival"],
        "claim_ids": e["claim_ids"], "classification": e["classification"], "confidence": e["confidence"],
        "evidence": e["evidence"], "documented_locations": locs,
        "notes": e.get("notes"),
        "review_status": REVIEW, "approved_for_application": False,
    }
    if geom is None:
        props["location_precision"] = props["location_precision"] if props["location_precision"] in ("region", "unknown", "named_area") else "unknown"
    return {"type": "Feature", "id": e["id"], "geometry": geom, "properties": props}


def main():
    by_id = {e["id"]: e for e in EVENTS}
    feats = [feature_for_event(e) for e in EVENTS]
    events_fc = {
        "type": "FeatureCollection",
        "metadata": {
            "status": "phase1a_source_checked_not_map_ready",
            "as_of": "2026-09-11",
            "coverage": ("Selected documented and reported events only. Deliberately includes searches for peripheral areas "
                         "(Somme, Seine-Maritime, Normandy, Belgium) to test the expansion hypothesis, so the sample over-represents "
                         "the periphery. Not a complete or representative sample; do not compute trends from it."),
            "geometry_policy": ("Point only where the source gives coordinates (MAIB) or names a place precise enough; named-area "
                                "representative points carry location_precision named_area and uncertainty_km; otherwise null. "
                                "Rescue location != launch site != pickup site != disembarkation port != intended destination. No tracks."),
            "location_types": ["OBSERVED LOCATION", "REPORTED LOCATION", "DERIVED CORRIDOR", "ILLUSTRATIVE ROUTE"],
            "historical_location_types": ["OBSERVED LOCATION", "REPORTED LOCATION"],
            "gazetteer": "OpenStreetMap Nominatim (ODbL); queries and results in geocoding-log.json",
            "builder": "build_geography.py",
        },
        "features": feats,
    }
    (HERE / "crossings" / "crossing-events.geojson").write_text(json.dumps(events_fc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    rfeats = []
    for rid, eid, oi, di, ptype, cross in ROUTES:
        e = by_id[eid]
        o, d = e["locs"][oi], e["locs"][di]
        if not (o["coordinates"] and d["coordinates"]):
            raise SystemExit(f"{rid}: endpoint without coordinates")
        rfeats.append({
            "type": "Feature", "id": rid,
            "geometry": {"type": "LineString", "coordinates": [o["coordinates"], d["coordinates"]]},
            "properties": {
                "id": rid, "event_id": eid, "event_date": e["event_date"], "pair_type": ptype,
                "includes_cross_channel_leg": cross,
                "geometry_meaning": "straight line between documented endpoints, not a navigated track",
                "origin": {k: o[k] for k in ("role", "name", "location_type", "location_precision", "uncertainty_km", "geometry_source")},
                "destination": {k: d[k] for k in ("role", "name", "location_type", "location_precision", "uncertainty_km", "geometry_source")},
                "origin_sector": e["sector"],
                "claim_ids": e["claim_ids"] + ["GEO-ROUTE-DISTANCES"],
                "classification": "DERIVED_STATISTIC", "confidence": "MEDIUM" if e["confidence"] == "HIGH" else "LOW",
                "evidence": e["evidence"],
                "review_status": REVIEW, "approved_for_application": False,
            },
        })
    routes_fc = {
        "type": "FeatureCollection",
        "metadata": {
            "status": "phase1a_documented_pairs_only",
            "as_of": "2026-09-11",
            "geometry_meaning": "straight line between documented endpoints, not a navigated track",
            "scenario_routes_included": False,
            "warning": ("Pairs are heterogeneous: most are French coastal legs or French-rescue returns, not Channel crossings. "
                        "Only pairs with includes_cross_channel_leg=true involve the crossing, and none gives a full launch-to-landfall "
                        "navigated distance. Do not draw as tracks; do not infer route-length trends."),
            "builder": "build_geography.py", "analysis": "route_analysis.py -> route-analysis.json",
        },
        "features": rfeats,
    }
    (HERE / "geography" / "documented-routes.geojson").write_text(json.dumps(routes_fc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"events: {len(feats)} ({sum(1 for f in feats if f['geometry'])} with point geometry); routes: {len(rfeats)}")


if __name__ == "__main__":
    main()
