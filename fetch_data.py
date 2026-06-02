#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Récupère le flux officiel roulez-eco.fr et génère data.json
filtré autour de Fontainebleau (rayon 25 km, vol d'oiseau).
"""

import io, json, math, zipfile, urllib.request
from datetime import datetime, timezone
from xml.etree import ElementTree as ET

HOME_LAT   = 48.4047   # Fontainebleau
HOME_LON   = 2.7014
RAYON_KM   = 25
MAX_AGE_J  = 3
DATA_URL   = "https://donnees.roulez-eco.fr/opendata/instantane"

CARBURANTS = ["Gazole", "SP95", "SP98", "E10", "E85", "GPLc"]

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat/2)**2
         + math.cos(math.radians(lat1))
         * math.cos(math.radians(lat2))
         * math.sin(dlon/2)**2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def ptv(val):
    try:
        return float(val) / 100_000.0
    except (TypeError, ValueError):
        return None

def age_jours(s):
    if not s:
        return 9999
    s = s.strip()
    for fmt in ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]:
        try:
            dt = datetime.strptime(s, fmt).replace(tzinfo=timezone.utc)
            return (datetime.now(timezone.utc) - dt).total_seconds() / 86400
        except ValueError:
            pass
    return 9999

print("Téléchargement du flux officiel…")
req = urllib.request.Request(DATA_URL, headers={"User-Agent": "GazoleFinder/6.0"})
with urllib.request.urlopen(req, timeout=30) as r:
    raw = r.read()

with zipfile.ZipFile(io.BytesIO(raw)) as zf:
    xml_name = [n for n in zf.namelist() if n.endswith(".xml")][0]
    root = ET.fromstring(zf.read(xml_name))

stations = []
for pdv in root.findall("pdv"):
    lat = ptv(pdv.get("latitude"))
    lon = ptv(pdv.get("longitude"))
    if lat is None or lon is None:
        continue
    if not (41 < lat < 52 and -6 < lon < 11):
        continue
    dist = haversine(HOME_LAT, HOME_LON, lat, lon)
    if dist > RAYON_KM:
        continue

    prix_dict = {}
    for px in pdv.findall("prix"):
        nom = px.get("nom")
        if nom not in CARBURANTS:
            continue
        try:
            val = float(px.get("valeur", "").replace(",", "."))
        except (ValueError, AttributeError):
            continue
        if val <= 0:
            continue
        age = age_jours(px.get("maj"))
        if age > MAX_AGE_J:
            continue
        prix_dict[nom] = {"prix": round(val, 3), "age_h": round(age * 24, 1)}

    if not prix_dict:
        continue

    adr_el   = pdv.find("adresse")
    ville_el = pdv.find("ville")
    adresse  = (adr_el.text   or "").strip() if adr_el   is not None else ""
    ville    = (ville_el.text or "").strip() if ville_el is not None else ""
    cp       = pdv.get("cp", "")

    stations.append({
        "adresse": adresse,
        "ville":   ville,
        "cp":      cp,
        "lat":     round(lat, 5),
        "lon":     round(lon, 5),
        "dist_km": round(dist, 1),
        "prix":    prix_dict,
    })

stations.sort(key=lambda s: s["dist_km"])

output = {
    "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "centre": {"lat": HOME_LAT, "lon": HOME_LON, "label": "Fontainebleau 77300"},
    "rayon_km": RAYON_KM,
    "stations": stations,
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"{len(stations)} stations écrites dans data.json")
