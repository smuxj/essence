# ⛽ Prix carburant — Fontainebleau & alentours

Prix des carburants en temps quasi-réel dans un rayon de 25 km autour de Fontainebleau (77300).

**Source officielle** : [donnees.roulez-eco.fr](https://donnees.roulez-eco.fr) — mis à jour toutes les 10 min par le gouvernement.

## Mise en place

### 1. Créer le repo GitHub

```bash
git init
git add .
git commit -m "initial"
gh repo create gazole-finder --public --push
```

### 2. Activer GitHub Pages

Dans Settings → Pages → Source : **GitHub Actions** → choisir le fichier `update-data.yml` comme source, ou utiliser **Deploy from branch** → `main` → `/` (root).

### 3. Déclencher la première mise à jour

Dans l'onglet **Actions** du repo, cliquer sur le workflow *"Mise à jour des prix carburant"* → **Run workflow**.

Après ~30 secondes, `data.json` est généré et la page s'affiche correctement.

## Personnaliser

Dans `fetch_data.py` :
- `HOME_LAT` / `HOME_LON` : changer le centre de recherche
- `RAYON_KM` : ajuster le rayon (20–30 km recommandé)
- `MAX_AGE_J` : ancienneté max des prix (défaut 3 jours)
- `CARBURANTS` : liste des carburants à inclure

## Structure

```
index.html          ← page web (lit data.json)
data.json           ← généré par la GitHub Action
fetch_data.py       ← script Python de récupération
.github/workflows/
  update-data.yml   ← tourne toutes les heures
```
