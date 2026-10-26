#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Récupère le flux officiel roulez-eco.fr et génère data.json
avec TOUTES les stations de France métropolitaine (Corse incluse).
Le filtrage par ville / rayon se fait côté navigateur (index.html).
"""

import io, json, zipfile, urllib.request
from datetime import datetime, timezone
from xml.etree import ElementTree as ET

MAX_AGE_J  = 3
DATA_URL   = "https://donnees.roulez-eco.fr/opendata/instantane"

CARBURANTS = ["Gazole", "SP95", "SP98", "E10", "E85", "GPLc"]

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
req = urllib.request.Request(DATA_URL, headers={"User-Agent": "GazoleFinder/7.0"})
with urllib.request.urlopen(req, timeout=60) as r:
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
    # France métropolitaine + Corse (écarte les coordonnées aberrantes et les DOM-TOM)
    if not (41 < lat < 52 and -6 < lon < 11):
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
        # format compact : [prix en €/L, âge en heures]
        prix_dict[nom] = [round(val, 3), round(age * 24)]

    if not prix_dict:
        continue

    adr_el   = pdv.find("adresse")
    ville_el = pdv.find("ville")
    adresse  = (adr_el.text   or "").strip() if adr_el   is not None else ""
    ville    = (ville_el.text or "").strip() if ville_el is not None else ""
    cp       = pdv.get("cp", "")

    stations.append((pdv.get("id", ""), {
        "adresse": adresse,
        "ville":   ville,
        "cp":      cp,
        "lat":     round(lat, 5),
        "lon":     round(lon, 5),
        "prix":    prix_dict,
    }))

# Ordre stable (par id de station) => des commits git beaucoup plus légers
stations.sort(key=lambda t: t[0])
stations = [s for _, s in stations]

output = {
    "updated":  datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "stations": stations,
}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, separators=(",", ":"))

print(f"{len(stations)} stations écrites dans data.json")
