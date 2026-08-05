# My Data Portfolio

A weekly automated data study journal, generated and published via GitHub Actions using [Hermes Agent](https://github.com/nousresearch/hermes-agent).

## Structure

```
my-data-portfolio/
├── projects/
│   ├── 2026-W32-maroc/
│   │   ├── README.md
│   │   ├── analysis.py
│   │   ├── queries.sql
│   │   └── figures/
│   └── ...
├── scripts/
│   └── publish_study.py
├── .github/workflows/
│   └── publish_study.yaml
└── README.md
```

## How it works

Each Monday at 08:00 UTC, a GitHub Action:
1. Checks out this repo
2. Installs Python 3.11 + dependencies (`pandas`, `seaborn`, `matplotlib`, `hermes-agent`)
3. Runs `scripts/publish_study.py`
4. Generates a new weekly folder with:
   - `README.md` (insights + Mermaid diagram)
   - `analysis.py` (data pipeline)
   - `queries.sql` (SQL analysis)
   - `figures/*.png` (charts)
5. Commits and pushes back to `main`

## Manual trigger

From the Actions tab → "Weekly Hermes Data Portfolio Publisher" → Run workflow.

## License

MIT — by [Atlass/Nous Research](https://nousresearch.com)
# Redeploy trigger mer.  5 août 2026 02:13:00
