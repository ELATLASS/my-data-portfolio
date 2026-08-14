# Étude: Pluie, Sécheresse et Opportunités Agricoles au Maroc

**Date de publication:** Août 2026  
**Période d'analyse:** 2000-2025 (26 ans)  
**Auteur:** Équipe Info Maroc / Data Science Atlass  
**Source des données:** [DroughtWatch Morocco](https://github.com/OthmanSALAHI/drought-risk-detection-morocco) (Open-Meteo Historical API, FAOSTAT, ONICL)

---

## Contexte

Le Maroc fait face à un défi majeur du changement climatique : la variabilité des précipitations et la montée des risques de sécheresse. Cette étude analyse les tendances climatiques sur 26 ans (2000-2025), les impacts sur l'agriculture nationale, et identifie les opportunités d'adaptation pour le secteur agricole marocain.

---

## 1. Méthodologie

### Sources de données
| Donnée | Source | Couverture |
|---|---|---|
| Données climatiques | Open-Meteo Historical API | Mensuelle, 44 villes marocaines, 2000-2025 |
| Production agricole | FAOSTAT Morocco | Annuelle, 4 grandes cultures |
| Prix de référence | ONICL Morocco | Céréales (quintal) |

### Méthodes d'analyse
- **SPI (Standardized Precipitation Index):** Mesure la sécheresse relative sur une échelle normalisée. SPI ≤ -1.0 = sécheresse, SPI ≤ -1.5 = sécheresse sévère.
- **Analyse régionale:** Regroupement par 12 régions administratives marocaines.
- **Analyse temporelle:** Tendances annuelles et saisonnières.

---

## 2. Résultats climatiques

### 2.1 Précipitations nationales

| Indicateur | Valeur |
|---|---|
| **Précipitation moyenne mensuelle** | 24 mm |
| **Précipitation min/max** | 0 mm / 765 mm |
| **Mois étudiés** | 13,156 (44 villes × 26 ans × ~12 mois) |
| **Saison la plus pluvieuse** | Hiver (38 mm/mois) |
| **Saison la plus sèche** | Été (3.8 mm/mois) |

### 2.2 Sécheresse (SPI)

| Catégorie | Nombre de mois | Pourcentage |
|---|---|---|
| **Normal (Near Normal)** | 9,033 | 68.7% |
| **Sécheresse légère (Moderately Dry)** | 1,180 | 9.0% |
| **Sécheresse modérée (Severely Dry)** | 554 | 4.2% |
| **Sécheresse extrême (Extremely Dry)** | 200 | 1.5% |
| **Excès de pluie (Very/Extremely Wet)** | 1,566 | 11.9% |

**Total mois en sécheresse (SPI ≤ -1.0):** 1,934 mois (14.7%)  
**Total mois en sécheresse sévère (SPI ≤ -1.5):** 6,872 mois (5.2%)

### 2.3 Années marquantes

| Année | SPI moyen | % mois secs | Classification |
|---|---|---|---|
| **2010** | +0.83 | 1.3% | Très humide |
| **2018** | +0.76 | 2.8% | Très humide |
| **2003** | +0.20 | 10.4% | Normale |
| **2024** | -0.17 | 21.0% | Sèche |
| **2023** | -0.05 | 17.6% | Normale-sèche |
| **2025** | -0.03 | 21.6% | Normale-sèche |

### 2.4 Analyse régionale

| Région | Précip. moy (mm/mois) | Taux de sécheresse | Classification |
|---|---|---|---|
| **Tanger-Al Hoceima** | 51.1 | 5.7% | Moins vulnérable |
| **Béni Mellal-Khénifra** | 44.2 | 8.0% | Modérée |
| **Fès-Meknès** | 43.7 | 7.1% | Modérée |
| **Rabat-Salé-Kénitra** | 39.4 | 5.2% | Moins vulnérable |
| **Marrakech-Safi** | 22.1 | 6.8% | Modérée |
| **Casablanca-Settat** | 26.6 | 5.8% | Modérée |
| **Oriental** | 23.1 | 5.4% | Modérée |
| **Souss-Massa** | 19.1 | 5.5% | Modérée |
| **Drâa-Tafilalet** | 12.6 | 6.5% | Vulnérable |
| **Guelmim-Oued Noun** | 11.9 | 6.7% | Vulnérable |
| **Laâyoune-Sakia** | 3.1 | 3.6% | Extrêmement vulnérable |

---

## 3. Production agricole

### 3.1 Production par culture (2000 vs 2025)

| Culture | Production 2000 | Production 2025 | Variation |
|---|---|---|---|
| **Blé tendre** | 1.8M tonnes | 4.5M tonnes | **+150%** |
| **Blé dur** | 0.7M tonnes | 1.7M tonnes | **+143%** |
| **Orge** | 1.4M tonnes | 2.8M tonnes | **+100%** |
| **Olives** | 0.45M tonnes | 0.56M tonnes | **+24%** |

### 3.2 Rendements par hectare (2025)

| Culture | Rendement (tonnes/ha) | Prix (MAD/quintal) |
|---|---|---|
| Soft wheat | 0.857 | 250 MAD |
| Durum wheat | 0.778 | 270 MAD |
| Barley | 0.700 | 220 MAD |
| Olives | 0.804 | 550 MAD |

---

## 4. Opportunités agricoles

### 4.1 Irrigation goutte-à-goutte
- **Impact:** Réduction de la consommation d'eau de 30-50% par rapport à l'irrigation traditionnelle
- **Priorité:** Régions arides (Drâa-Tafilalet, Laâyoune-Sakia, Guelmim-Oued Noun)
- **Adoption:** Programme national Maroc Vert soutient la transition

### 4.2 Capteurs IoT & agriculture de précision
- **Projet pilote:** [AmaneAI](https://github.com/najzdev/AmaneAi) — plateformne IoT locale avec assistant IA en Darija/Amazigh
- **Fonctionnalités:** Surveillance en temps réel de l'humidité du sol, automatisation de l'irrigation, détection précoce de stress hydrique
- **Bénéfices:** Optimisation des rendements, réduction des pertes post-récolte

### 4.3 Cultures résistantes à la sécheresse
- **Oliviers:** Culture la plus résistante (>30% de taux de change, production stable malgré sécheresse)
- **Céréales tolérantes à la sécheresse:** Blé dur ressemblant, orge de montagne
- **Légumineuses:** Pois chiches, lentilles (fixent l'azote, nécessitent moins d'eau)

### 4.4 Agroforesterie
- **Combinaison:** Intégration d'arbres fruitiers (amandier, figuiers) avec les cultures céréalières
- **Bénéfices:** Protection contre l'érosion, régulation microclimatique, production diversifiée
- **Impact potentiel:** +20-30% de résilience face à la sécheresse

### 4.5 Résilience par région
| Région | Stratégie prioritaire |
|---|---|
| **Tanger-Al Hoceima** | Développement de l'irrigation efficace pour cimenter la résilience |
| **Fès-Meknès / Béni Mellal** | Expérimenter avec cultures résistantes + agroforesterie |
| **Drâa-Tafilalet** | Priorité irrigation goutte-à-goutte + cultures succulentes |
| **Laâyoune-Sakia** | Diversification vers cultures maraîchères sous abri + solaire-pompage |

---

## 5. Conclusions

1. **Trend hydrique:** Le Maroc subit une variabilité croissante des précipitations. Les années 2001, 2017, 2019-2021, 2023-2024 montrent des tendances sèches.

2. **Résilience agricole:** Malgré la pression hydrique, la production agricole a augmenté (+100-150% pour les céréales) grâce à l'intensification et au déploiement des technologies d'irrigation.

3. **Vulnérabilité régionale:** Les régions du Sud (Laâyoune-Sakia, Drâa-Tafilalet, Guelmim) restent les plus vulnérables à la sécheresse avec moins de 15 mm/mois de précipitations moyennes.

4. **Opportunités d'adaptation:** L'agroforesterie, l'irrigation goutte-à-goutte, et l'agriculture de précision (IoT) offrent des leviers concrets pour renforcer la résilience du secteur agricole marocain face au changement climatique.

---

## 📎 Ressources

- **Source des données:** [DroughtWatch Morocco - GitHub](https://github.com/OthmanSALAHI/drought-risk-detection-morocco)
- **Modèle de prédiction:** Histogram Gradient Boosting (CV ROC AUC: 0.91)
- **Données climatiques:** Open-Meteo Historical API (44 villes marocaines)
- **Données agricoles:** FAOSTAT Morocco, ONICL Morocco
- **Outil IoT:** [AmaneAI](https://github.com/najzdev/AmaneAi) — Agriculture intelligente au Maroc

---

*Étude générée automatiquement par l'équipe Info Maroc / Data Science Atlass — Août 2026*