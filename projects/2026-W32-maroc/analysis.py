"""
2026-W32-maroc : Analyse des données marocaines
=================================================
Ce script charge, nettoie et visualise des données fictives marocaines
(population urbaine par ville et région) pour produire un rapport hebdomadaire.

Usage:
    python analysis.py

Produit:
    - figures/population_by_region.png
    - figures/top_cities_population.png
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration
sns.set_theme(style="whitegrid")
os.makedirs("figures", exist_ok=True)

# --- 1. Données simulées ---
data = {
    "city": [
        "Casablanca", "Rabat", "Fès", "Marrakech", "Tanger", "Meknès",
        "Oujda", "Kénitra", "Témara", "Safi", "El Jadida", "Nador",
        "Taza", "Chefchaouen", "Dèsirat", "Dakhla", "Laâyoune", "Taroudant",
        "Tiznit", "Benguirie"
    ],
    "region": [
        "Grand Casablanca-Safi", "Rabat-Salé-Zemmour-Kénitra", "Fès-Meknès",
        "Sud-Comptes", "Tanger-Tétouan-Al Hoceima", "Fès-Meknès",
        "Oriental", "Rabat-Salé-Zemmour-Kénitra", "Rabat-Salé-Zemmour-Kénitra",
        "Grand Casablanca-Safi", "Sud-Comptes", "Rabat-Salé-Zemmour-Kénitra",
        "Tanger-Tétouan-Al Hoceima", "Tanger-Tétouan-Al Hoceima",
        "Oriental", "Sud-Comptes", "Sud-Comptes", "Sud-Comptes",
        "Sud-Comptes", "Fès-Meknès"
    ],
    "population": [
        3421000, 1800000, 1100000, 985000, 850000, 650000,
        520000, 480000, 420000, 380000, 360000, 290000,
        180000, 170000, 160000, 140000, 130000, 110000,
        105000, 95000
    ]
}

df = pd.DataFrame(data)

# --- 2. Analyse : Top 10 villes ---
top_10 = df.nlargest(10, "population")

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    data=top_10,
    x="population",
    y="city",
    hue="region",
    dodge=False,
    palette="viridis",
    ax=ax
)
ax.set_title("Top 10 villes marocaines par population (2026)", fontsize=14, weight="bold")
ax.set_xlabel("Population (habitants)")
ax.set_ylabel("Ville")
ax.legend(title="Région", fontsize=8)
plt.tight_layout()
plt.savefig("figures/top_cities_population.png", dpi=150)
plt.close()

# --- 3. Analyse : Population par région ---
by_region = df.groupby("region")["population"].sum().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(
    x=by_region.values,
    y=by_region.index,
    palette="mako",
    ax=ax
)
ax.set_title("Population totale par région (2026)", fontsize=14, weight="bold")
ax.set_xlabel("Population totale (habitants)")
ax.set_ylabel("Région")
plt.tight_layout()
plt.savefig("figures/population_by_region.png", dpi=150)
plt.close()

print("📊 Analyse terminée. Graphiques générés dans 'figures/'.")
