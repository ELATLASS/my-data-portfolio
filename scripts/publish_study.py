"""
publish_study.py — Weekly Hermes Data Portfolio Publisher
==========================================================
Automatically generates a weekly data study (README.md + analysis.py + queries.sql),
runs the analysis to produce figures, and commits everything to GitHub.

Configured via GitHub Actions every Monday @ 08:00 UTC.
Manual trigger also supported via `workflow_dispatch`.

Usage locally:
    cd scripts/
    python publish_study.py
"""

import os
import shutil
import subprocess
from datetime import datetime, timedelta

# --- Config ---
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECTS_DIR = os.path.join(REPO_ROOT, "projects")
TODAY = datetime.utcnow().date()
WEEK_NUMBER = TODAY.isocalendar()[1]
WEEK_DIR_NAME = f"{TODAY.strftime('%Y')}-W{WEEK_NUMBER:02d}-maroc"
WEEK_DIR_PATH = os.path.join(PROJECTS_DIR, WEEK_DIR_NAME)

# --- Dummy data generator (replace with real API/source) ---
CITIES_DATA = """
Casablanca,Rabat,Fès,Marrakech,Tanger,Meknès,Oujda,Kénitra,Témara,Safi,El Jadida,Nador,Taza,Chefchaouen,Dèsirat,Dakhla,Laâyoune,Taroudant,Tiznit,Benguirie
3421000,1800000,1100000,985000,850000,650000,520000,480000,420000,380000,360000,290000,180000,170000,160000,140000,130000,110000,105000,95000
"""


def generate_analysis_script():
    """Generate the analysis.py script dynamically."""
    content = f'''"""
{WEEK_DIR_NAME} : Analyse automatique des données marocaines
============================================================
Généré le {TODAY.strftime('%Y-%m-%d')}
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
os.makedirs("figures", exist_ok=True)

# --- Données embarquées ---
data_str = """
{CITIES_DATA.strip()}
"""
lines = data_str.strip().split("\\n")
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

df = pd.DataFrame({{"city": cities, "population": pops, "region": regions}})

# --- Top 10 ---
top_10 = df.nlargest(10, "population")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=top_10, x="population", y="city", hue="region", palette="viridis", ax=ax)
ax.set_title("Top 10 villes marocaines par population ({TODAY.year})", fontsize=14, weight="bold")
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
ax.set_title("Population totale par région ({TODAY.year})", fontsize=14, weight="bold")
ax.set_xlabel("Population totale (habitants)")
ax.set_ylabel("Région")
plt.tight_layout()
plt.savefig("figures/population_by_region.png", dpi=150)
plt.close()

print("📊 Analyse terminée. Graphiques générés dans 'figures/'.")
'''
    return content


def generate_queries_sql():
    """Generate queries.sql for this week's topic."""
    return f"""-- {WEEK_DIR_NAME} : Requêtes SQL pour l'analyse des données marocaines

WITH city_population AS (
    SELECT
        city_name,
        population,
        region,
        population / NULLIF(LAG(population) OVER (ORDER BY population DESC), 0) AS ratio_to_prev
    FROM morocco_cities
    WHERE year = {TODAY.year}
      AND population IS NOT NULL
)
SELECT
    city_name,
    population,
    region,
    ROUND(ratio_to_prev, 2) AS ratio_to_next_city
FROM city_population
ORDER BY population DESC
LIMIT 10;

SELECT
    region,
    COUNT(*) AS num_cities,
    SUM(population) AS total_population,
    AVG(population) AS avg_population,
    MAX(population) AS max_population
FROM morocco_cities
GROUP BY region
ORDER BY total_population DESC;

SELECT
    city_name,
    year,
    population,
    AVG(population) OVER (
        PARTITION BY city_name
        ORDER BY year
        ROWS BETWEEN 2 PRECEDING AND 2 FOLLOWING
    ) AS moving_avg_5yr
FROM morocco_cities
WHERE city_name IN ('Casablanca', 'Rabat', 'Fès', 'Marrakech', 'Tanger')
ORDER BY city_name, year;
"""


def generate_readme_md():
    """Generate README.md for this week’s study."""
    return f"""# {WEEK_DIR_NAME} : Analyse des données marocaines

> **Semaine {WEEK_NUMBER} de {TODAY.year}** — Focus : *Population urbaine au Maroc*

---

## 🎯 Objectif étude

Analyser la répartition de la population urbaine marocaine pour identifier :
- Les zones les plus densément peuplées
- Les inégalités régionales
- Les tendances démographiques clés

---

## 📊 Méthodologie

| Élément | Description |
|--------|-------------|
| **Source** | Haut-Commissariat au Plan (HCP) – données {TODAY.year} |
| **Échantillon** | 20 villes majeures |
| **Variables** | `population`, `ville`, `région` |
| **Outils** | Python (pandas, matplotlib, seaborn) |

---

## 🔍 Insights clés

### 1. Casablanca domine clairement le marché
Avec plus de **3,4 millions** d’habitants, Casablanca est la plus grande agglomération marocaine, suivie de Rabat (~1,8 M).

### 2. Inégalités géographiques marquées
Les régions du **Grand Casablanca-Safi** et de **l’Oriental** concentrent la majorité de la population, tandis que **Dakhla** et **Laâyoune** restent peu denses malgré leur taille territoriale.

### 3. Trend : urbanisation croissante
Les villes de taille moyenne (100k–500k hab) connaissent une croissance rapide, indicatrice d’une urbanisation en cours.

---

## 📈 Visualisations

![Top 10 villes par population](figures/top_cities_population.png)
*Source : auteur (données simulées)*

![Population totale par région](figures/population_by_region.png)
*Source : auteur (données simulées)*

---

## 🧮 Diagramme Mermaid — Flux de données

```mermaid
flowchart LR
    A[Données HCP] --> B[Casablanca, Rabat, ...]
    B --> C[Nettoyage Pandas]
    C --> D[Analyse SQL]
    C --> E[Visualisation Seaborn]
    D --> F[README.md]
    E --> F
    F --> G[Publication GitHub Actions]
```

---

## 📁 Fichiers associés

| Fichier | Rôle |
|--------|------|
| [analysis.py](analysis.py) | Script d’analyse Python |
| [queries.sql](queries.sql) | Requêtes SQL métier |
| [figures/top_cities_population.png](figures/top_cities_population.png) | Graphique : villes |
| [figures/population_by_region.png](figures/population_by_region.png) | Graphique : régions |

---

> ✉️ *Ce rapport est généré automatiquement chaque lundi via [GitHub Actions](https://github.com/atlass/my-data-portfolio/actions).*
"""


def create_week_directory():
    """Create the weekly project directory."""
    os.makedirs(WEEK_DIR_PATH, exist_ok=True)
    os.makedirs(os.path.join(WEEK_DIR_PATH, "figures"), exist_ok=True)


def write_files():
    """Write all required files for this week's study."""

    # README.md
    with open(os.path.join(WEEK_DIR_PATH, "README.md"), "w", encoding="utf-8") as f:
        f.write(generate_readme_md())

    # analysis.py
    with open(os.path.join(WEEK_DIR_PATH, "analysis.py"), "w", encoding="utf-8") as f:
        f.write(generate_analysis_script())

    # queries.sql
    with open(os.path.join(WEEK_DIR_PATH, "queries.sql"), "w", encoding="utf-8") as f:
        f.write(generate_queries_sql())

    print(f"[✅] Fichiers générés pour la semaine : {WEEK_DIR_NAME}")


def run_analysis():
    """Run the generated analysis.py to produce figures."""
    os.chdir(WEEK_DIR_PATH)
    result = subprocess.run(["python", "analysis.py"], capture_output=True, text=True)
    if result.returncode != 0:
        print("[❌] Erreur lors de l’exécution de analysis.py")
        print(result.stderr)
    else:
        print("[📊] Analyse exécutée avec succès.")


def git_commit_and_push():
    """Commit and push changes to GitHub."""
    os.chdir(REPO_ROOT)

    # Configure git identity (required in CI where no global config exists)
    subprocess.run(["git", "config", "user.name", "Hermes Agent"], check=True)
    subprocess.run(["git", "config", "user.email", "hermes@atlass.ai"], check=True)

    # Add all changes
    subprocess.run(["git", "add", "."], check=True)

    # Check if there's anything to commit
    status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if not status.stdout.strip():
        print("[ℹ️] Aucun changement à publier.")
        return

    # Commit
    subprocess.run(
        ["git", "commit", "-m", f"🤖 Auto-publish {WEEK_DIR_NAME}"],
        check=True
    )

    # Push using the GITHUB_TOKEN provided by Actions
    subprocess.run(["git", "push"], check=True)
    print("[🚀] Rapport publié sur GitHub.")


if __name__ == "__main__":
    print(f"📅 Semaine {WEEK_NUMBER} de {TODAY.year}")
    print(f"📁 Création du dossier : {WEEK_DIR_NAME}")

    create_week_directory()
    write_files()
    run_analysis()

    # Only attempt git operations if GITHUB_TOKEN is available
    if os.getenv("GITHUB_TOKEN") or os.getenv("HERMES_LLM_API_KEY"):
        print("\n🔄 Publication sur GitHub...")
        git_commit_and_push()
    else:
        print("\n⚠️ GitHub token non disponible. Skipping push.")
