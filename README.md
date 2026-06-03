# ⛽ Prix carburant — Fontainebleau & alentours

Site web affichant les prix des carburants en temps quasi-réel autour de Fontainebleau (77300), avec recherche par ville et carte interactive.

**→ [smuxj.github.io/essence](https://smuxj.github.io/essence)**

---

## Fonctionnalités

- Prix en temps réel (Gazole, SP95, SP98, E10, E85, GPL)
- Recherche par ville avec autocomplétion
- Slider de rayon (5 à 50 km)
- Carte interactive avec marqueurs colorés selon le prix
- Clic sur une station dans le tableau → zoom sur la carte
- Lien Google Maps pour chaque station
- Mise à jour automatique toutes les heures via GitHub Actions

## Source des données

[donnees.roulez-eco.fr](https://donnees.roulez-eco.fr) — flux officiel du gouvernement français, mis à jour en continu.

## Stack

- HTML / CSS / JS vanilla
- [Leaflet](https://leafletjs.com) pour la carte (OpenStreetMap)
- [Nominatim](https://nominatim.org) pour le géocodage des villes
- GitHub Actions pour la récupération automatique des données
- GitHub Pages pour l'hébergement

## Structure

```
index.html                        — page web
fetch_data.py                     — script de récupération des données
data.json                         — données générées automatiquement
.github/workflows/update-data.yml — GitHub Action (toutes les heures)
```

## Mise à jour manuelle des données

Onglet **Actions** → *Mise à jour des prix carburant* → **Run workflow**

---

*Projet généré avec l'aide de [Claude](https://claude.ai) (Anthropic).*
