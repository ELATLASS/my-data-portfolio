"""
2026-W28-hybride : Échanges commerciaux UE-Maroc (Flux FR-Maroc)
===============================================================
Analyse des flux commerciaux entre la France et le Maroc.

Source : Eurostat comext + HCP (données simulées pour le test)
Variables : produit, volume (M€), direction (export/import), région marocaine de destination
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
os.makedirs("figures", exist_ok=True)

# --- Données simulées : échanges France-Maroc 2026 ---
data = {
    "product": [
        "Automobiles", "Électronique", "Textile/Habillement", "Produits agricoles",
        "Engrais/minerais", "Produits chimiques", "Matières premières", "Métaux"
    ],
    "export_fr_maroc": [15200, 6800, 4200, 3800, 9500, 3100, 2200, 5400],
    "import_fr_maroc": [2800, 3500, 1900, 12500, 1100, 2200, 8000, 3900],
    "region": [
        "Tangier", "Casablanca", "Rabat", "Fès",
        "Tanger", "Casablanca", "Oriental", "Casablanca"
    ]
}

df = pd.DataFrame(data)

# Chart 1: Trade balance by product (horizontal bar)
fig, ax = plt.subplots(figsize=(10, 6))
df["balance"] = df["export_fr_maroc"] - df["import_fr_maroc"]
df["color"] = df["balance"].apply(lambda x: "green" if x > 0 else "red")
sns.barplot(
    data=df,
    y="product",
    x="balance",
    hue="color",
    palette={"green": "green", "red": "red"},
    legend=False,
    ax=ax
)
ax.set_title("🇫🇷→🇲🇦 Échanges France-Maroc 2026 : Balance par produit (M€)", fontsize=14, weight="bold")
ax.set_xlabel("Balance commerciale (M€)")
ax.set_ylabel("Produit")
plt.tight_layout()
plt.savefig("figures/trade_balance_by_product.png", dpi=150)
plt.close()

# Chart 2: Heatmap — export vs import
fig, ax = plt.subplots(figsize=(8, 5))
trade_matrix = df[["export_fr_maroc", "import_fr_maroc"]].set_index(df["product"])
sns.heatmap(
    trade_matrix,
    annot=True,
    fmt=".0f",
    cmap="RdYlGn",
    center=5000,
    cbar_kws={"label": "Volume (M€)"},
    ax=ax
)
ax.set_title("🔥 Heatmap flux commerciaux FR↔MA par produit (M€)", fontsize=14, weight="bold")
plt.tight_layout()
plt.savefig("figures/trade_heatmap_fr_ma.png", dpi=150)
plt.close()

print("📊 Analyse des échanges FR-Maroc terminée. Graphiques générés dans 'figures/'.")
