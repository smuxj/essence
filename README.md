# ⛽ Prix carburant — France

Site web affichant les prix des carburants en temps quasi-réel dans toute la France métropolitaine, avec recherche par ville ou code postal et carte interactive.

**→ [smuxj.github.io/essence](https://smuxj.github.io/essence)**

---

## Fonctionnalités

- Prix en temps réel (Gazole, SP95, SP98, E10, E85, GPL)
- Toutes les stations de France métropolitaine (~10 000), Corse incluse
- Recherche par ville ou code postal avec autocomplétion
- Mémorisation de la dernière ville, du rayon, du carburant et du tri (stockage local du navigateur) : on retrouve sa recherche à chaque visite
- Slider de rayon (5 à 50 km)
- Carte interactive avec marqueurs colorés selon le prix et cercle du rayon de recherche
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

## Contributeurs

- [@smuxj](https://github.com/smuxj) — auteur du projet
- [Claude](https://claude.ai) (Anthropic) — co-auteur : couverture France entière et mémorisation des préférences (v1.4.0)

---

*Projet généré avec l'aide de [Claude](https://claude.ai) (Anthropic).*
