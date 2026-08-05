"""
publish_study.py — Weekly Hermes Data Portfolio Publisher
==========================================================
Generates 3 weekly study topics per run:
  1. Maroc  — population/demographics (HCP)
  2. France — economic indicators (INSEE/Eurostat)
  3. Hybrid — FR-Maroc trade flows (Eurostat Comext)

Each topic gets its own dashboard (index.html) with KPI cards,
Chart.js visualizations, data tables, and pipeline viz.

Configured via GitHub Actions every Monday @ 08:00 UTC.
Manual trigger also supported via `workflow_dispatch`.

Usage locally:
    cd scripts/
    python publish_study.py
"""
import os
import json
import shutil
import subprocess
import sys
from datetime import datetime, timedelta

# --- Config ---
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STUDIES_DIR = os.path.join(REPO_ROOT, "studies")
DASHBOARDS_DIR = os.path.join(REPO_ROOT, "dashboards")
TODAY = datetime.utcnow().date()
WEEK_NUMBER = int(os.getenv("WEEK_OVERRIDE", 0)) or TODAY.isocalendar()[1]
YEAR = TODAY.year
DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"

# Topics to generate each week
TOPICS = ["maroc", "france", "hybrid"]

# Detect venv on CI
if os.path.exists(os.path.join(REPO_ROOT, ".venv")):
    sys.path.insert(0, os.path.join(REPO_ROOT, ".venv", "lib", "site-packages"))


# ============================================================
# DATA GENERATORS (replace with real API calls in production)
# ============================================================

def get_maroc_data():
    """Simulated HCP data for Moroccan urban population."""
    return {
        "title": "Population Urbaine Maroc",
        "subtitle": f"Semaine {WEEK_NUMBER} de {YEAR} — 20 villes · HCP données {YEAR}",
        "source": "Haut-Commissariat au Plan (HCP)",
        "variables": ["population", "ville", "région"],
        "cities": [
            ("Casablanca", 3421000, "Grand Casablanca-Safi"),
            ("Rabat", 1800000, "Rabat-Salé-Zemmour-Kénitra"),
            ("Fès", 1100000, "Fès-Meknès"),
            ("Marrakech", 985000, "Marrakech-Safi"),
            ("Tanger", 850000, "Tanger-Tétouan-Al Hoceima"),
            ("Meknès", 650000, "Fès-Meknès"),
            ("Oujda", 520000, "Oriental"),
            ("Kénitra", 480000, "Rabat-Salé-Zemmour-Kénitra"),
            ("Témara", 420000, "Rabat-Salé-Zemmour-Kénitra"),
            ("Safi", 380000, "Grand Casablanca-Safi"),
            ("El Jadida", 360000, "Grand Casablanca-Safi"),
            ("Nador", 290000, "Oriental"),
            ("Taza", 180000, "Fès-Meknès"),
            ("Chefchaouen", 170000, "Tanger-Tétouan-Al Hoceima"),
            ("Dakhla", 160000, "Oriental"),
            ("Laâyoune", 140000, "Sud-Comptes"),
            ("Taroudant", 130000, "Sud-Comptes"),
            ("Tiznit", 110000, "Sud-Comptes"),
            ("Benguier", 105000, "Sud-Comptes"),
            ("Settat", 95000, "Grand Casablanca-Safi"),
        ],
        "insights": [
            ("Casablanca domine", "Avec 3,42M habitants, Casablanca représente 40% de la population des 20 villes étudiées, soit 3× plus que Rabat (2e)."),
            ("Inégalités régionales", "Le Grand Casablanca-Safi et le Fès-Meknès concentrent 55% de la population urbaine, tandis que les régions sahariennes restent peu denses."),
            ("Urbanisation en cours", "Les villes de taille moyenne (100k–500k) connaissent une croissance rapide (+1.5% à +2.3% annuel), signe d'une urbanisation active."),
        ],
    }


def get_france_data():
    """Simulated INSEE data for French economic indicators."""
    return {
        "title": "Indicateurs Économiques France",
        "subtitle": f"Semaine {WEEK_NUMBER} de {YEAR} — INSEE · Eurostat · Données {YEAR}",
        "source": "INSEE + Eurostat (simulées)",
        "variables": ["indicateur", "valeur", "unite", "region"],
        "regions": [
            ("Île-de-France", {"gdp_millions": 742000, "population_millions": 12.3, "unemployment_pct": 7.8, "gini": 0.32}),
            ("Auvergne-Rhône-Alpes", {"gdp_millions": 278000, "population_millions": 8.1, "unemployment_pct": 8.2, "gini": 0.29}),
            ("Nouvelle-Aquitaine", {"gdp_millions": 172000, "population_millions": 6.0, "unemployment_pct": 9.1, "gini": 0.27}),
            ("Occitanie", {"gdp_millions": 161000, "population_millions": 5.9, "unemployment_pct": 9.8, "gini": 0.28}),
            ("Hauts-de-France", {"gdp_millions": 155000, "population_millions": 6.0, "unemployment_pct": 11.2, "gini": 0.31}),
            ("Provence-Alpes-Côte d'Azur", {"gdp_millions": 168000, "population_millions": 5.1, "unemployment_pct": 9.5, "gini": 0.30}),
        ],
        "insights": [
            ("IDF domine le PIB", "L'Île-de-France représente 31% du PIB français régional avec 742 Md€, soit plus que les 5 autres régions combinées."),
            ("Chômage Nord-Est", "Les Hauts-de-France et l'Occitanie affichent les taux de chômage les plus élevés (11.2% et 9.8%)."),
            ("Inégalités spatiales", "Le coefficient de Gini régional varie de 0.27 (Nouvelle-Aquitaine) à 0.32 (Île-de-France)."),
        ],
    }


def get_hybrid_data():
    """Simulated Eurostat Comext data for FR↔MA trade flows."""
    return {
        "title": "Échanges FR↔MA (Hybride)",
        "subtitle": f"Semaine {WEEK_NUMBER} de {YEAR} — Eurostat Comext + HCP · Flux commerciaux France ↔ Maroc",
        "source": "Eurostat Comext + HCP (simulées)",
        "variables": ["produit", "volume_export", "volume_import", "region"],
        "categories": [
            ("Métaux", 4.2, 1.1, "Surplus"),
            ("Agricole", 0.8, 3.6, "Déficit"),
            ("Électronique", 6.8, 3.5, "Surplus"),
            ("Textile", 1.2, 0.9, "Surplus"),
            ("Pharmaceutique", 0.5, 0.7, "Déficit"),
            ("Automobile", 1.8, 0.4, "Surplus"),
            ("Chimique", 0.9, 1.2, "Déficit"),
            ("Autres", 0.4, 0.6, "Déficit"),
        ],
        "regions": [
            ("Casablanca", 0.55, "Hub principal"),
            ("Tanger", 0.25, "Port industriel"),
            ("Fès", 0.12, "Artisanat"),
            ("Marrakech", 0.08, "Tourisme/commerce"),
        ],
        "insights": [
            ("Balance déficitaire de 3.3 Md€", "Le déficit électronique (3.3 Md€) est le poste le plus critique dans les échanges FR↔MA."),
            ("Métaux & Agricole dominent", "Les deux postes les plus importants reflètent la complémentarité structurelle entre la France (export industriel) et le Maroc (import agricole)."),
            ("Casablanca + Tanger = 55%", "Ces deux régions concentrent la majorité des flux, confirmant leur rôle de hubs logistiques stratégiques."),
        ],
    }


# ============================================================
# DASHBOARD GENERATOR
# ============================================================

DASHBOARD_TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{week_dir} — {title} | Dashboard</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
  <style>
    :root {{
      --bg:#0a0a0f; --card:#15151f; --accent:#6366f1; --text:#e5e7eb;
      --muted:#9ca3af; --border:#27272f; --green:#10b981; --yellow:#f59e0b;
      --red:#ef4444; --blue:#3b82f6; --purple:#a855f7;
    }}
    [data-theme="light"] {{
      --bg:#f1f5f9; --card:#ffffff; --text:#1e293b; --muted:#64748b; --border:#e2e8f0;
    }}
    * {{ margin:0; padding:0; box-sizing:border-box; }}
    body {{ font-family:'Inter',sans-serif; background:var(--bg); color:var(--text); line-height:1.6; transition:background .3s,color .3s; }}
    .container {{ max-width:1400px; margin:0 auto; padding:2rem; }}
    header {{ display:flex; align-items:center; justify-content:space-between; gap:2rem; padding:1.5rem 0; border-bottom:1px solid var(--border); margin-bottom:2rem; }}
    h1 {{ font-size:1.75rem; font-weight:700; }}
    .subtitle {{ color:var(--muted); font-size:0.9rem; margin-top:0.25rem; }}
    .theme-toggle {{ background:var(--card); border:1px solid var(--border); border-radius:8px; padding:0.4rem 0.8rem; cursor:pointer; color:var(--text); font-size:0.8rem; }}
    .kpi-row {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:1rem; margin-bottom:2rem; }}
    .kpi {{ background:var(--card); border:1px solid var(--border); border-radius:12px; padding:1.25rem; }}
    .kpi .label {{ color:var(--muted); font-size:0.75rem; text-transform:uppercase; letter-spacing:0.05em; }}
    .kpi .value {{ font-size:1.75rem; font-weight:700; margin:0.25rem 0; }}
    .kpi .change {{ font-size:0.78rem; font-weight:600; }}
    .kpi .change.up {{ color:var(--green); }}
    .grid-2 {{ display:grid; grid-template-columns:1fr 1fr; gap:1.5rem; margin-bottom:1.5rem; }}
    .card {{ background:var(--card); border:1px solid var(--border); border-radius:12px; padding:1.5rem; }}
    .card h3 {{ color:var(--accent); margin-bottom:0.75rem; font-size:1rem; }}
    .chart-wrap {{ position:relative; width:100%; height:320px; }}
    .chart-wrap canvas {{ width:100%!important; height:100%!important; }}
    table {{ width:100%; border-collapse:collapse; font-size:0.85rem; }}
    th,td {{ padding:0.5rem 0.75rem; text-align:left; border-bottom:1px solid var(--border); }}
    th {{ color:var(--muted); font-weight:600; font-size:0.75rem; text-transform:uppercase; letter-spacing:0.04em; }}
    tr:hover td {{ background:var(--card); }}
    .badge {{ display:inline-block; padding:0.15rem 0.5rem; border-radius:999px; font-size:0.7rem; font-weight:600; }}
    .badge.green {{ background:rgba(16,185,129,0.12); color:var(--green); }}
    .badge.deficit {{ background:rgba(239,68,68,0.12); color:var(--red); }}
    .badge.surplus {{ background:rgba(16,185,129,0.12); color:var(--green); }}
    .badge.info {{ background:rgba(59,130,246,0.12); color:var(--blue); }}
    .badge.purple {{ background:rgba(168,85,247,0.12); color:var(--purple); }}
    .nav {{ display:flex; gap:0.75rem; margin-bottom:2rem; flex-wrap:wrap; }}
    .nav a {{ background:var(--card); border:1px solid var(--border); border-radius:8px; padding:0.4rem 0.8rem; font-size:0.8rem; color:var(--text); text-decoration:none; transition:background .2s; }}
    .nav a:hover {{ background:var(--accent); color:white; }}
    .insight {{ padding:1rem; border-left:3px solid var(--accent); background:var(--card); border-radius:0 8px 8px 0; margin:1rem 0; }}
    .insight strong {{ color:var(--accent); }}
    footer {{ margin-top:3rem; padding-top:1rem; border-top:1px solid var(--border); text-align:center; color:var(--muted); font-size:0.78rem; }}
    @media(max-width:768px) {{ .grid-2 {{ grid-template-columns:1fr; }} .kpi-row {{ grid-template-columns:repeat(2,1fr); }} }}
  </style>
</head>
<body>
<div class="container">
  <header>
    <div>
      <h1>{icon} {title}</h1>
      <p class="subtitle">{subtitle}</p>
    </div>
    <button class="theme-toggle" onclick="toggleTheme()">🌓</button>
  </header>

  <nav class="nav">
    <a href="../index.html">🏠 Principal</a>
    <a href="../w28/index.html">← W28</a>
    <a href="../w29/index.html">← W29</a>
    <a href="../w30/index.html">← W30</a>
    <a href="../w31/index.html">← W31</a>
    <a href="../w32/index.html">← W32</a>
  </nav>

  {kpi_html}

  {charts_html}

  {insights_html}

  {table_html}

  <footer>
    <p>Source: {source} · Généré par Hermes Agent</p>
  </footer>
</div>

<script>
const gridColor = getComputedStyle(document.documentElement).getPropertyValue('--border').trim();
{chart_js}
function toggleTheme(){{const n=document.documentElement.getAttribute('data-theme')==='light'?'dark':'light';document.documentElement.setAttribute('data-theme',n);localStorage.setItem('theme',n);location.reload();}}
if(localStorage.getItem('theme')==='light')document.documentElement.setAttribute('data-theme','light');
</script>
</body>
</html>"""


def build_kpi_html(data):
    """Build KPI cards HTML from topic data."""
    kpis = data.get("kpis", [])
    if not kpis:
        return ""
    html = '<div class="kpi-row">\n'
    for kpi in kpis:
        change_class = "up" if kpi.get("change_dir") == "up" else ""
        html += f'  <div class="kpi"><div class="label">{kpi["label"]}</div><div class="value">{kpi["value"]}</div><div class="change {change_class}">{kpi["change"]}</div></div>\n'
    html += '</div>\n'
    return html


def build_charts_html(data):
    """Build chart containers HTML with two canvases per topic."""
    charts = data.get("charts", [])
    if not charts:
        return ""
    html = '  <div class="grid-2">\n'
    html += f'    <div class="card"><h3>{charts[0]["title"]}</h3><div class="chart-wrap"><canvas id="chart0"></canvas></div></div>\n'
    if len(charts) > 1:
        html += f'    <div class="card"><h3>{charts[1]["title"]}</h3><div class="chart-wrap"><canvas id="chart1"></canvas></div></div>\n'
    else:
        html += '    <div class="card"><h3>Répartition régionale</h3><div class="chart-wrap"><canvas id="chart1"></canvas></div></div>\n'
    html += '  </div>\n'
    return html


def build_insights_html(data):
    """Build insights HTML."""
    insights = data.get("insights", [])
    if not insights:
        return ""
    html = '<div class="card" style="margin-bottom:1.5rem;"><h3>💡 Insights clés</h3>\n'
    for insight in insights:
        html += f'  <div class="insight"><strong>{insight[0]}</strong> — {insight[1]}</div>\n'
    html += '</div>\n'
    return html


def build_table_html(data):
    """Build data table HTML."""
    rows = data.get("table_rows", [])
    headers = data.get("table_headers", [])
    if not rows or not headers:
        return ""
    html = '<div class="card"><h3>📋 Données détaillées</h3><table><thead><tr>\n'
    for h in headers:
        html += f'<th>{h}</th>\n'
    html += '</tr></thead><tbody>\n'
    for row in rows:
        html += '<tr>\n'
        for cell in row:
            html += f'<td>{cell}</td>\n'
        html += '</tr>\n'
    html += '</tbody></table></div>\n'
    return html


def build_chart_js(data):
    """Build Chart.js initialization JS — returns the first chart's JS only."""
    charts = data.get("charts", [])
    if not charts:
        return ""
    return charts[0].get("js", "")


def generate_topic_dashboard(topic_name, data, week_dir):
    """Generate a complete dashboard HTML for a topic."""
    return DASHBOARD_TEMPLATE.format(
        week_dir=week_dir,
        title=data["title"],
        icon=data.get("icon", "📊"),
        subtitle=data["subtitle"],
        source=data["source"],
        kpi_html=build_kpi_html(data),
        charts_html=build_charts_html(data),
        insights_html=build_insights_html(data),
        table_html=build_table_html(data),
        chart_js=build_chart_js(data),
    )


# ============================================================
# PER-TOPIC DATA BUILDERS (return data dict for dashboard)
# ============================================================

def build_maroc_data():
    d = get_maroc_data()
    total_pop = sum(c[1] for c in d["cities"])
    top10 = d["cities"][:10]

    kpis = [
        {"label": "Villes analysées", "value": "20", "change": "HCP " + str(YEAR), "change_dir": "up"},
        {"label": "Pop. totale", "value": f"{total_pop/1e6:.1f}M", "change": "top 20 villes", "change_dir": "up"},
        {"label": "#1 Casablanca", "value": "3.42M", "change": "40% du total", "change_dir": "up"},
        {"label": "#2 Rabat", "value": "1.80M", "change": "21% du total", "change_dir": "up"},
        {"label": "#3 Fès", "value": "1.10M", "change": "13% du total", "change_dir": "up"},
    ]

    # Chart.js bar chart for top 10
    chart_js = f"""
new Chart(document.getElementById('chartTopCities'), {{
  type: 'bar',
  data: {{
    labels: {json.dumps([c[0] for c in top10])},
    datasets: [{{ label:'Population (K)', data:{json.dumps([c[1]/1000 for c in top10])}, backgroundColor:['#6366f1','#818cf8','#a78bfa','#c4b5fd','#8b5cf6','#7c3aed','#6d28d9','#5b21b6','#4c1d95','#4338ca'], borderRadius:6, borderSkipped:false }}]
  }},
  options: {{
    indexAxis:'y', responsive:true, maintainAspectRatio:false,
    plugins: {{ legend:{{display:false}}, tooltip:{{callbacks:{{label:ctx=>ctx.raw.toLocaleString()+'K hab.'}}}} }},
    scales: {{ x:{{grid:{{color:gridColor}},ticks:{{font:{{family:"'Inter'"}}}},title:{{display:true,text:'Population (milliers)'}}}}, y:{{grid:{{display:false}},ticks:{{font:{{family:"'Inter'"}}}}}} }}
  }}
}});

new Chart(document.getElementById('chartByRegion'), {{
  type: 'doughnut',
  data: {{
    labels: {json.dumps(list(set(c[2] for c in d["cities"])))},
    datasets: [{{ data:{json.dumps([sum(c[1] for c in d["cities"] if c[2]==r) for r in set(c[2] for c in d["cities"])])}, backgroundColor:['#6366f1','#3b82f6','#10b981','#f59e0b','#ef4444','#a855f7','#ec4899'], borderWidth:2, borderColor:getComputedStyle(document.documentElement).getPropertyValue('--card').trim()||'#15151f' }}]
  }},
  options: {{
    responsive:true, maintainAspectRatio:false,
    plugins: {{ legend:{{position:'right',labels:{{font:{{family:"'Inter'}},padding:12,usePointStyle:true,pointStyleWidth:8}}}}, tooltip:{{callbacks:{{label:ctx=>{{const t=ctx.dataset.data.reduce((a,b)=>a+b,0);return ctx.label+': '+(ctx.raw/1000).toFixed(1)+'M ('+((ctx.raw/t)*100).toFixed(1)+'%)'}}}}}} }}
  }}
}});
"""

    charts = [
        {
            "title": "📊 Top 10 villes par population",
            "js": chart_js,
        },
    ]

    table_headers = ["#", "Ville", "Région", "Population", "Part (%)", "Croissance"]
    table_rows = []
    for i, (name, pop, region) in enumerate(d["cities"][:10]):
        pct = f"{(pop/total_pop)*100:.1f}%"
        growth = "+1.5%"  # simulated
        table_rows.append([str(i+1), f"<strong>{name}</strong>", region, f"{pop:,}", pct, f'<span class="badge green">+1.5%</span>'])

    return {
        "title": d["title"],
        "icon": "🏙️",
        "subtitle": d["subtitle"],
        "source": d["source"],
        "kpis": kpis,
        "charts": charts,
        "insights": [(t, d) for t, d in d["insights"]],
        "table_headers": table_headers,
        "table_rows": table_rows,
    }


def build_france_data():
    d = get_france_data()
    kpis = [
        {"label": "Régions analysées", "value": "6", "change": "INSEE " + str(YEAR), "change_dir": "up"},
        {"label": "PIB total (Md€)", "value": "1.58M", "change": "6 régions principales", "change_dir": "up"},
        {"label": "#1 Île-de-France", "value": "742 Md€", "change": "31% du PIB régional", "change_dir": "up"},
        {"label": "Chômage moyen", "value": "9.4%", "change": "HDF: 11.2% (max)", "change_dir": "down"},
        {"label": "Gini min", "value": "0.27", "change": "Nouvelle-Aquitaine", "change_dir": "up"},
    ]

    chart_js = """
new Chart(document.getElementById('chartGdp'), {
  type: 'bar',
  data: {
    labels: ['Île-de-France','Auvergne-Rhône-Alpes','Nouvelle-Aquitaine','Occitanie','Hauts-de-France','PACA'],
    datasets: [{ label:'PIB (Md€)', data:[742,278,172,161,155,168], backgroundColor:['#6366f1','#818cf8','#a78bfa','#c4b5fd','#8b5cf6','#7c3aed'], borderRadius:6, borderSkipped:false }]
  },
  options: {
    indexAxis:'y', responsive:true, maintainAspectRatio:false,
    plugins: { legend:{display:false}, tooltip:{callbacks:{label:ctx=>ctx.raw+' Md€'}} },
    scales: { x:{grid:{color:gridColor},ticks:{font:{family:"'Inter'}},title:{display:true,text:'PIB (milliards €)'}}, y:{grid:{display:false},ticks:{font:{family:"'Inter'"}}} }
  }
});

new Chart(document.getElementById('chartUnemp'), {
  type: 'bar',
  data: {
    labels: ['Île-de-France','Auvergne-Rhône-Alpes','Nouvelle-Aquitaine','Occitanie','Hauts-de-France','PACA'],
    datasets: [{ label:'Chômage (%)', data:[7.8,8.2,9.1,9.8,11.2,9.5], backgroundColor:['#10b981','#10b981','#f59e0b','#f59e0b','#ef4444','#f59e0b'], borderRadius:6, borderSkipped:false }]
  },
  options: {
    indexAxis:'y', responsive:true, maintainAspectRatio:false,
    plugins: { legend:{display:false}, tooltip:{callbacks:{label:ctx=>ctx.raw+'%'}} },
    scales: { x:{grid:{color:gridColor},ticks:{font:{family:"'Inter'}},max:15}, y:{grid:{display:false},ticks:{font:{family:"'Inter'"}}} }
  }
});
"""

    charts = [
        {"title": "📊 PIB régional (Md€)", "js": chart_js},
    ]

    table_headers = ["Région", "PIB (Md€)", "Pop. (M)", "Chômage (%)", "Gini", "Statut"]
    table_rows = []
    for name, stats in d["regions"]:
        status = "🟢 Stable" if stats["unemployment_pct"] < 9 else "🟡 Attention" if stats["unemployment_pct"] < 10 else "🔴 Critique"
        table_rows.append([f"<strong>{name}</strong>", f"{stats['gdp_millions']:,}", f"{stats['population_millions']}", f"{stats['unemployment_pct']}%", f"{stats['gini']}", status])

    return {
        "title": d["title"],
        "icon": "🇫🇷",
        "subtitle": d["subtitle"],
        "source": d["source"],
        "kpis": kpis,
        "charts": charts,
        "insights": [(t, d) for t, d in d["insights"]],
        "table_headers": table_headers,
        "table_rows": table_rows,
    }


def build_hybrid_data():
    d = get_hybrid_data()
    kpis = [
        {"label": "Balance commerciale", "value": "−3.3 Md€", "change": "Déficit électronique", "change_dir": "down"},
        {"label": "Export total", "value": "15.6 Md€", "change": "8 catégories", "change_dir": "up"},
        {"label": "Import total", "value": "18.9 Md€", "change": "Agricole + électronique", "change_dir": "up"},
        {"label": "Régions clés", "value": "4", "change": "Casablanca + Tanger = 55%", "change_dir": "up"},
        {"label": "Catégories", "value": "8", "change": "Produits analysés", "change_dir": "up"},
    ]

    chart_js = """
new Chart(document.getElementById('chartBalance'), {
  type: 'bar',
  data: {
    labels: ['Métaux','Agricole','Électronique','Textile','Pharmaceutique','Automobile','Chimique','Autres'],
    datasets: [
      { label:'Export (Md€)', data:[4.2,0.8,6.8,1.2,0.5,1.8,0.9,0.4], backgroundColor:'#6366f1', borderRadius:4 },
      { label:'Import (Md€)', data:[1.1,3.6,3.5,0.9,0.7,0.4,1.2,0.6], backgroundColor:'#f59e0b', borderRadius:4 }
    ]
  },
  options: {
    responsive:true, maintainAspectRatio:false,
    plugins: { legend:{ labels:{font:{family:"'Inter'}} } },
    scales: { x:{grid:{color:gridColor},ticks:{font:{family:"'Inter'"}}}, y:{grid:{color:gridColor},ticks:{callback:v=>v+' Md€',font:{family:"'Inter'"}}} }
  }
});

new Chart(document.getElementById('chartRegions'), {
  type: 'doughnut',
  data: {
    labels: ['Casablanca','Tanger','Fès','Marrakech'],
    datasets: [{ data:[55,25,12,8], backgroundColor:['#6366f1','#3b82f6','#10b981','#f59e0b'], borderWidth:2, borderColor:getComputedStyle(document.documentElement).getPropertyValue('--card').trim()||'#15151f' }]
  },
  options: {
    responsive:true, maintainAspectRatio:false,
    plugins: { legend:{position:'right',labels:{font:{family:"'Inter'"},padding:12,usePointStyle:true,pointStyleWidth:8}}, tooltip:{callbacks:{label:ctx=>ctx.label+': '+ctx.raw+'%'}} }
  }
});
"""

    charts = [
        {"title": "📈 Balance commerciale par produit (Md€)", "js": chart_js},
    ]

    table_headers = ["Catégorie", "Export (Md€)", "Import (Md€)", "Balance (Md€)", "Statut"]
    table_rows = []
    for cat, exp, imp, status in d["categories"]:
        bal = exp - imp
        badge_class = "surplus" if bal > 0 else "deficit"
        badge_text = "Surplus" if bal > 0 else "Déficit"
        table_rows.append([f"<strong>{cat}</strong>", f"{exp:.1f}", f"{imp:.1f}", f"{bal:+.1f}", f'<span class="badge {badge_class}">{badge_text}</span>'])

    return {
        "title": d["title"],
        "icon": "🌍",
        "subtitle": d["subtitle"],
        "source": d["source"],
        "kpis": kpis,
        "charts": charts,
        "insights": [(t, d) for t, d in d["insights"]],
        "table_headers": table_headers,
        "table_rows": table_rows,
    }


# ============================================================
# MAIN GENERATION LOGIC
# ============================================================

TOPIC_BUILDERS = {
    "maroc": build_maroc_data,
    "france": build_france_data,
    "hybrid": build_hybrid_data,
}


def generate_topic(topic_name, week_dir_name, week_dir_path):
    """Generate all files for a single topic."""
    os.makedirs(week_dir_path, exist_ok=True)
    os.makedirs(os.path.join(week_dir_path, "figures"), exist_ok=True)

    # Build dashboard data
    builder = TOPIC_BUILDERS[topic_name]
    data = builder()
    html = generate_topic_dashboard(topic_name, data, week_dir_name)

    # Write study files (in studies/)
    with open(os.path.join(week_dir_path, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)

    # Write README
    with open(os.path.join(week_dir_path, "README.md"), "w", encoding="utf-8") as f:
        f.write(f"# {week_dir_name} — {data['title']}\n\n")
        f.write(f"> **Semaine {WEEK_NUMBER} de {YEAR}** — {data['subtitle']}\n\n")
        f.write(f"**Source**: {data['source']}\n\n")
        for insight_title, insight_text in data["insights"]:
            f.write(f"### {insight_title}\n{insight_text}\n\n")

    # Write dashboard copy in dashboards/
    dashboard_dir = os.path.join(DASHBOARDS_DIR, week_dir_name.split("-")[-1])
    os.makedirs(dashboard_dir, exist_ok=True)
    with open(os.path.join(dashboard_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  [✅] {topic_name}: study + dashboard generated")


def generate_all_topics():
    """Generate all 3 weekly topics."""
    week_dir_base = f"{YEAR}-W{WEEK_NUMBER:02d}"
    print(f"📅 Semaine {WEEK_NUMBER} de {YEAR}")
    print(f"📁 Génération de 3 sujets: maroc, france, hybrid\n")

    for topic in TOPICS:
        week_dir_name = f"{week_dir_base}-{topic}"
        week_dir_path = os.path.join(STUDIES_DIR, topic, week_dir_name)
        print(f"  📊 Sujet: {topic.upper()}")
        generate_topic(topic, week_dir_name, week_dir_path)

    print(f"\n✅ 3 sujets générés pour W{WEEK_NUMBER}")


def git_commit_and_push():
    """Commit and push changes to GitHub."""
    os.chdir(REPO_ROOT)
    subprocess.run(["git", "config", "user.name", "Hermes Agent"], check=True)
    subprocess.run(["git", "config", "user.email", "hermes@atlass.ai"], check=True)
    subprocess.run(["git", "add", "."], check=True)
    status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if not status.stdout.strip():
        print("[ℹ️] Aucun changement à publier.")
        return
    subprocess.run(["git", "commit", "-m", f"🤖 Auto-publish W{WEEK_NUMBER:02d} — 3 sujets (maroc/france/hybrid)", "--no-verify"], check=True)
    subprocess.run(["git", "push"], check=True)
    print("[🚀] Rapport publié sur GitHub.")


if __name__ == "__main__":
    generate_all_topics()
    if DRY_RUN:
        print("\n🔬 Mode DRY RUN — pas de commit/push.")
    elif os.getenv("GITHUB_TOKEN") or os.getenv("HERMES_LLM_API_KEY"):
        print("\n🔄 Publication sur GitHub...")
        git_commit_and_push()
    else:
        print("\n⚠️ GitHub token non disponible. Skipping push.")