# Étude W33 : Pluie, Sécheresse et Opportunités Agricoles au Maroc (2000-2025)

> **Semaine 33 de 2026** — **Période:** 2000-2025 | **44 villes marocaines** | **13,156 mois analysés**

**Sources:** Open-Meteo Historical API, FAOSTAT Morocco, ONICL Morocco, DroughtWatch Morocco (ML model ROC AUC: 0.91)

---

## 📊 Résumé

Le Maroc subit une **variabilité croissante des précipitations**. Sur 13,156 mois analysés (44 villes × 26 ans), **14.7% des mois** sont classifiés comme sécheresse (SPI ≤ -1.0). Les pics de sécheresse (2001: 39.6%, 2017: 22.0%) ont coïncidé avec des baisses agricoles de 20-30%. Malgré cela, la production céréalière a augmenté de **+100-150%** grâce à l'intensification et l'irrigation. Les régions du Sud (Laâyoune-Sakia: 3 mm/mois) restent les plus vulnérables.

**Dashboard associé:** [../../dashboards/w33/index.html](../../dashboards/w33/index.html)

---

## 📈 Données sources

| Donnée | Source | Format |
|---|---|---|
| Données climatiques mensuelles | Open-Meteo Historical API | 13,156 mois (44 villes × 308 mois) |
| Production agricole | FAOSTAT Morocco | CSV: blé tendre, blé dur, orge, olives |
| Prix céréales | ONICL Morocco | MAD/quintal |
| Classification SPI | CGIAR/ICARDA | 7 catégories (Near Normal → Extremely Dry) |

- **Fichiers sources:** [`data/morocco_climate_features.csv`](data/morocco_climate_features.csv), [`data/morocco_climate_data.csv`](data/morocco_climate_data.csv), [`data/morocco_agriculture.csv`](data/morocco_agriculture.csv), [`data/moroccan_cities.csv`](data/moroccan_cities.csv)

---

## 🔧 Pipeline

```
📥 Open-Meteo API (climate) + FAOSTAT (agriculture)
🧹 Nettoyage & feature engineering (pandas, 17 features)
🔍 Analyse SPI (Standardized Precipitation Index)
📊 Classification régionale + tendances temporelles
🌾 Corrélation pluie/production + opportunités agricoles
📝 Rapport Markdown + infographie PNG
🚀 Publication GitHub Actions
```

**Fréquence de mise à jour:** Hebdomadaire (automatisé via CI)  
**Créé par:** El Atlassi · [Source](https://github.com/ELATLASS/my-data-portfolio)

---

## 1️⃣ Analyse climatique nationale

### Précipitations (2000-2025)
- **Moyenne mensuelle:** 24 mm (min: 0 mm, max: 765 mm)
- **Saison la plus pluvieuse:** Hiver (38 mm/mois)
- **Saison la plus sèche:** Été (3.8 mm/mois)

### Sécheresse (SPI)
| Catégorie | Mois | % |
|---|---|---|
| Normal (Near Normal) | 9,033 | 68.7% |
| Sécheresse modérée | 1,180 | 9.0% |
| Sécheresse sévère (SPI ≤ -1.5) | 754 | 5.7% |
| Excès de pluie | 1,566 | 11.9% |

### Années marquantes
| Année | SPI moyen | % mois secs | Type |
|---|---|---|---|
| **2010** | +0.83 | 1.3% | Très humide |
| **2018** | +0.76 | 2.8% | Très humide |
| **2001** | -0.77 | 39.6% | Très sèche |
| **2017** | -0.29 | 22.0% | Sèche |
| **2024** | -0.17 | 21.0% | Sèche |

---

## 2️⃣ Analyse régionale

| Région | Précip. (mm/mois) | % Sécheresse | Niveau de risque |
|---|---|---|---|
| Tanger-Al Hoceima | 51.1 | 5.7% | Faible |
| Béni Mellal-Khénifra | 44.2 | 8.0% | Modéré |
| Fès-Meknès | 43.7 | 7.1% | Modéré |
| Rabat-Salé-Kénitra | 39.4 | 5.2% | Faible |
| Drâa-Tafilalet | 12.6 | 6.5% | Élevé |
| Laâyoune-Sakia | 3.1 | 3.6% | Très élevé |

---

## 3️⃣ Production agricole (2000 vs 2025)

| Culture | 2000 (tonnes) | 2025 (tonnes) | Variation |
|---|---|---|---|
| Blé tendre | 1.8M | 4.5M | **+150%** |
| Blé dur | 0.7M | 1.7M | **+143%** |
| Orge | 1.4M | 2.8M | **+100%** |
| Olives | 0.45M | 0.56M | **+24%** |

---

## 4️⃣ Opportunités agricoles

### 4.1 Irrigation goutte-à-goutte
- **Économie d'eau:** 30-50% vs irrigation classique
- **Priorité:** Drâa-Tafilalet, Laâyoune-Sakia, Guelmim-Oued Noun

### 4.2 Agriculture IoT
- **Projet local:** [AmaneAI](https://github.com/najzdev/AmaneAi) — assistant IA en Darija/Amazigh
- **Fonctionnalités:** Capteurs d'humidité, irrigation automatisée, détection maladies

### 4.3 Cultures résistantes
- **Oliviers:** Plus résistant (>30% de variation de prix stable)
- **Légumineuses:** Pois chiches, lentilles (fixent l'azote)

### 4.4 Agroforesterie
- **Approche:** Arbres fruitiers + cultures céréalières
- **Impact:** +20-30% résilience face à la sécheresse

---

## 📁 Fichiers associés

| Fichier | Rôle |
|---|---|
| [rapport_detail.md](rapport_detail.md) | Rapport complet détaillé |
| [figures/infographie.png](figures/infographie.png) | Infographie synthétique |
| [data/morocco_climate_features.csv](data/morocco_climate_features.csv) | Données climatiques (3.5 MB) |
| [data/morocco_climate_data.csv](data/morocco_climate_data.csv) | Données brutes Open-Meteo (730 KB) |
| [data/morocco_agriculture.csv](data/morocco_agriculture.csv) | Production agricole FAOSTAT |
| [data/moroccan_cities.csv](data/moroccan_cities.csv) | Coordonnées des 44 villes |

---

> ✉️ *Ce rapport est généré automatiquement chaque lundi via [GitHub Actions](https://github.com/ELATLASS/my-data-portfolio/actions).*

**Cycle :** Lundi 08:00 UTC | **Créé par :** El Atlassi