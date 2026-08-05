# My Data Portfolio

A weekly automated data study journal, generated and published via GitHub Actions using [Hermes Agent](https://github.com/nousresearch/hermes-agent).

## 📊 Live Dashboard

**https://elatlass.github.io/my-data-portfolio/**

## Structure

```
my-data-portfolio/
├── dashboards/              ← Visual dashboards (Chart.js, KPI cards)
│   ├── w28/index.html      (Hybride FR↔MA trade flows)
│   ├── w29/index.html      (Maroc Population)
│   ├── w30/index.html      (Maroc Population)
│   ├── w31/index.html      (Maroc Population)
│   └── w32/index.html      (Maroc Population)
├── studies/                 ← Raw study data & analysis
│   ├── maroc/               (W29-W32: 4 weekly studies)
│   ├── france/              (empty, ready for next week)
│   └── hybrid/              (W28: FR↔MA trade)
├── scripts/
│   └── publish_study.py    ← Weekly publisher (3 topics)
├── .github/workflows/
│   ├── publish_study.yaml  ← Weekly generation (Mon 08:00 UTC)
│   └── pages.yml           ← Pages deploy workflow
├── index.html              ← Main portfolio landing page
├── README.md
└── requirements.txt        ← Minimal deps (no Python deps needed)
```

## Weekly Publication Cycle

Every Monday at 08:00 UTC, Hermes Agent publishes **3 topics**:

| Topic | Folder | Source |
|---|---|---|
| 🇲🇦 **Maroc** | `studies/maroc/` | HCP (population/demographics) |
| 🇫🇷 **France** | `studies/france/` | INSEE/Eurostat (economic indicators) |
| 🌍 **Hybrid** | `studies/hybrid/` | Eurostat Comext (FR↔MA trade) |

Each topic gets its own dashboard in `dashboards/wXX/` with:
- KPI cards (dark palette)
- Chart.js visualizations (bar, doughnut, grouped bar)
- Detailed data tables
- Key insights section
- Dark/Light theme toggle

## Workflows

| Workflow | Trigger | Purpose |
|---|---|---|
| **Deploy to GitHub Pages** | Push to `main` | Deploys site to Pages |
| **Weekly Hermes Publisher** | Mon 08:00 UTC + manual | Generates 3 topics + dashboards |
| **Dependabot Updates** | PR creation | Dependency updates |
| **pages-build-deployment** | Pages build | Internal Pages deployment |

## Tech Stack

- **Static site**: HTML + Chart.js (CDN) + CSS custom properties
- **CI/CD**: GitHub Actions
- **Hosting**: GitHub Pages (modern build)
- **Data**: HCP, INSEE, Eurostat (simulated for portfolio)
- **Auth**: GitHub token (`GITHUB_TOKEN`)

## License

MIT
