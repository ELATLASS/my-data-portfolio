"""
Étude: Coupe du Monde 2030 - Impact Maroc
==========================================
Analyse des stades, villes hôtes, projets d'infrastructure,
et impact économique de l'organisation de la Coupe du Monde 2030 au Maroc.

Source: Wikipedia - 2030 FIFA World Cup, FIFA bid documents
"""
import os
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

os.makedirs("figures", exist_ok=True)

# Dark theme colors - Atlass palette
BG = '#0b0f19'
PANEL = '#121a2b'
FG = '#e8ecf5'
MUT = '#7d8aa5'
ACCENT = '#9E2A2B'
ACCENT2 = '#E3A021'
ACCENT3 = '#14285A'
GREEN = '#4CAF50'
RED = '#f44336'
BLUE = '#2196F3'
YELLOW = '#f59e0b'
PURPLE = '#a855f7'

# Load data
with open("data/worldcup_maroc_2030.json", "r") as f:
    data = json.load(f)

# --- Figure 1: Host Cities & Stadiums ---
fig, ax = plt.subplots(figsize=(14, 8), facecolor=BG)
ax.set_facecolor(BG)

cities = list(data["host_cities"].keys())
capacities = [data["host_cities"][c]["capacity"] or 0 for c in cities]
colors = [BLUE if data["host_cities"][c]["status"] == "new" else GREEN for c in cities]
statuses = [data["host_cities"][c]["status"] for c in cities]

y_pos = np.arange(len(cities))
bars = ax.barh(y_pos, capacities, color=colors, height=0.6, edgecolor=BG)

# Add value labels
for i, (bar, status, city) in enumerate(zip(bars, statuses, cities)):
    cap = data["host_cities"][city]["capacity"]
    label = f"{cap:,}" if cap else "N/A"
    ax.text(bar.get_width() + 1000, bar.get_y() + bar.get_height()/2,
            f'{label} ({status})', ha='left', va='center', fontsize=8, color=FG)

ax.set_yticks(y_pos)
ax.set_yticklabels([f'{c}\n({data["host_cities"][c]["stadium"].split("(")[0].strip()})' for c in cities], fontsize=9, color=FG)
ax.invert_yaxis()
ax.set_xlabel('Capacité du stade', fontsize=10, color=MUT)
ax.set_title('Stades de la Coupe du Monde 2030 au Maroc', fontsize=14, fontweight='bold', color=FG)
ax.grid(axis='x', alpha=0.2, color=MUT)
for spine in ax.spines.values():
    spine.set_visible(False)

legend_elements = [
    plt.Rectangle((0,0),1,1, fc=GREEN, label='Rénovation'),
    plt.Rectangle((0,0),1,1, fc=BLUE, label='Nouveau stade'),
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=9, facecolor=BG, edgecolor=MUT, labelcolor=FG)

plt.tight_layout()
plt.savefig('figures/stades_2030.png', dpi=150, facecolor=BG, bbox_inches='tight')
plt.close()

# --- Figure 2: Impact économique ---
fig, ax = plt.subplots(figsize=(14, 6), facecolor=BG)
ax.set_facecolor(BG)

# Economic data
econ_labels = ['Investissement\ndirect (MAD)', 'Impact économique\ntotal (USD)',
               'Création\nemplois', 'Rooms\nhôteliers']
econ_values = [200e8, 2.5e9, 50000, 15000]
econ_colors = [PURPLE, BLUE, GREEN, YELLOW]

bars = ax.bar(range(len(econ_labels)), econ_values, color=econ_colors, edgecolor=BG, width=0.6)

# Format values
formatted = ['200M MAD', '$2.5B', '50,000', '15,000']
for bar, fmt in zip(bars, formatted):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(econ_values)*0.01,
            fmt, ha='center', va='bottom', fontsize=9, color=FG)

ax.set_xticks(range(len(econ_labels)))
ax.set_xticklabels(econ_labels, fontsize=9, color=FG)
ax.set_ylabel('Valeur', fontsize=10, color=MUT)
ax.set_title('Impact économique de la Coupe du Monde 2030 au Maroc', fontsize=14, fontweight='bold', color=FG)
for spine in ax.spines.values():
    spine.set_visible(False)
ax.grid(axis='y', alpha=0.2, color=MUT)
ax.tick_params(axis='y', labelsize=8, colors=MUT)

# Use log scale for better visualization
ax.set_yscale('log')

plt.tight_layout()
plt.savefig('figures/impact_economique.png', dpi=150, facecolor=BG, bbox_inches='tight')
plt.close()

# --- Figure 3: Distribution des équipes par pays hôte ---
fig, ax = plt.subplots(figsize=(10, 8), facecolor=BG)
ax.set_facecolor(BG)

host_shares = data["host_country_shares"]
countries = list(host_shares.keys())
shares = list(host_shares.values())
pie_colors = [ACCENT, BLUE, PURPLE]

wedges, texts, autotexts = ax.pie(shares, labels=countries, autopct='%1.0f%%',
                                   colors=pie_colors, startangle=90,
                                   textprops={'fontsize': 11, 'color': FG},
                                   wedgeprops={'edgecolor': BG, 'linewidth': 2})
for autotext in autotexts:
    autotext.set_color(FG)

ax.set_title('Distribution des matches par pays hôte (2030)', fontsize=14, fontweight='bold', color=FG)

plt.tight_layout()
plt.savefig('figures/repartition_matches.png', dpi=150, facecolor=BG, bbox_inches='tight')
plt.close()

# --- Figure 4: Infrastructure Projects ---
fig, ax = plt.subplots(figsize=(14, 6), facecolor=BG)
ax.set_facecolor(BG)

projects = [p["name"] for p in data["infrastructure_projects"]]
# Use a simple metric for comparison
project_metrics = []
for p in data["infrastructure_projects"]:
    if "length_km" in p:
        project_metrics.append(p["length_km"])
    elif "rooms_added" in p:
        project_metrics.append(p["rooms_added"] / 1000)
    elif "passengers_per_year" in p:
        project_metrics.append(p["passengers_per_year"] / 100000)
    elif "capacity_increase" in p:
        project_metrics.append(float(p["capacity_increase"].strip('%')) * 100)
    else:
        project_metrics.append(0)

bars = ax.barh(range(len(projects)), project_metrics, color=[BLUE, GREEN, YELLOW, PURPLE, ACCENT, RED][:len(projects)], height=0.5, edgecolor=BG)

# Labels
labels = []
for p in data["infrastructure_projects"]:
    if "length_km" in p:
        labels.append(f'{p["length_km"]} km')
    elif "rooms_added" in p:
        labels.append(f'{p["rooms_added"]:,} rooms')
    elif "passengers_per_year" in p:
        labels.append(f'{p["passengers_per_year"]/1e6:.1f}M pax/yr')
    elif "capacity_increase" in p:
        labels.append(f'+{p["capacity_increase"]}')
    else:
        labels.append('N/A')

for i, (bar, label) in enumerate(zip(bars, labels)):
    ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
            label, ha='left', va='center', fontsize=8, color=FG)

ax.set_yticks(range(len(projects)))
ax.set_yticklabels(projects, fontsize=9, color=FG)
ax.set_xlabel('Métriques clés', fontsize=10, color=MUT)
ax.set_title('Projets d\'infrastructure pour la Coupe du Monde 2030', fontsize=14, fontweight='bold', color=FG)
for spine in ax.spines.values():
    spine.set_visible(False)
ax.grid(axis='x', alpha=0.2, color=MUT)
ax.tick_params(axis='y', labelsize=8, colors=FG)

plt.tight_layout()
plt.savefig('figures/infrastructures.png', dpi=150, facecolor=BG, bbox_inches='tight')
plt.close()

print("✅ Figures Coupe du Monde 2030 générées:")
print("  - figures/stades_2030.png")
print("  - figures/impact_economique.png")
print("  - figures/repartition_matches.png")
print("  - figures/infrastructures.png")
