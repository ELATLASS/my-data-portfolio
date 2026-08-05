"""
2026-W30-maroc : Analyse automatique des données marocaines
============================================================
Généré le 2026-07-20
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
os.makedirs("figures", exist_ok=True)

# --- Données embarquées ---
data_str = """
Casablanca,Rabat,Fès,Marrakech,Tanger,Meknès,Oujda,Kénitra,Témara,Safi,El Jadida,Nador,Taza,Chefchaouen,Dèsirat,Dakhla,Laâyoune,Taroudant,Tiznit,Benguirie
3421000,1800000,1100000,985000,850000,650000,520000,480000,420000,380000,360000,290000,180000,170000,160000,140000,130000,110000,105000,95000
"""
lines = data_str.strip().split("\n")
cities = lines[0].split(",")
pops = [int(x) for x in lines[1].split(",")]

regions = [
    "Grand Casablanca-Safi", "Rabat-Salé-Zemmour-Kénitra", "Fès-Meknès",
    "Sud-Comptes", "Tanger-Tétouan-Al Hoceima", "Fès-Meknès",
    "Oriental", "Rabat-Salé-Zemmour-Kénitra", "Rabat-Salé-Zemmour-Kénitra",
    "Grand Casablanca-Safi", "Sud-Comptes", "Rabat-Salé-Zemmour-Kénitra",
    "Tanger-Tétouan-Al Hoceima", "Tanger-Tétouan-Al Hoceima",
    "Oriental", "Sud-Comptes", "Sud-Comptes", "Sud-Comptes",
    "Sud-Comptes", "Fès-Meknès"
]

df = pd.DataFrame({"city": cities, "population": pops, "region": regions})

# --- Top 10 ---
top_10 = df.nlargest(10, "population")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=top_10, x="population", y="city", hue="region", palette="viridis", ax=ax)
ax.set_title("Top 10 villes marocaines par population (2026)", fontsize=14, weight="bold")
ax.set_xlabel("Population (habitants)")
ax.set_ylabel("Ville")
ax.legend(title="Région", fontsize=8)
plt.tight_layout()
plt.savefig("figures/top_cities_population.png", dpi=150)
plt.close()

# --- Par région ---
by_region = df.groupby("region")["population"].sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=by_region.values, y=by_region.index, palette="mako", ax=ax)
ax.set_title("Population totale par région (2026)", fontsize=14, weight="bold")
ax.set_xlabel("Population totale (habitants)")
ax.set_ylabel("Région")
plt.tight_layout()
plt.savefig("figures/population_by_region.png", dpi=150)
plt.close()

print("📊 Analyse terminée. Graphiques générés dans 'figures/'.")
