-- 2026-W28-hybride : Requêtes SQL pour l'analyse des flux commerciaux FR-Maroc

-- Top 5 produits exportés vers le Maroc
WITH fr_ma_exports AS (
    SELECT product, export_fr_maroc, region
    FROM trade_flows
    WHERE year = 2026
      AND country_pair = 'FR->MA'
)
SELECT
    product,
    export_fr_maroc,
    region,
    ROUND(export_fr_maroc * 100.0 / SUM(export_fr_maroc) OVER(), 2) AS pct_share
FROM fr_ma_exports
ORDER BY export_fr_maroc DESC
LIMIT 5;

-- Top 5 produits importés depuis le Maroc
WITH fr_ma_imports AS (
    SELECT product, import_fr_maroc, region
    FROM trade_flows
    WHERE year = 2026
      AND country_pair = 'MA->FR'
)
SELECT
    product,
    import_fr_maroc,
    region,
    ROUND(import_fr_maroc * 100.0 / SUM(import_fr_maroc) OVER(), 2) AS pct_share
FROM fr_ma_imports
ORDER BY import_fr_maroc DESC
LIMIT 5;

-- Balance commerciale totale par région marocaine
SELECT
    region,
    SUM(export_fr_maroc) AS total_exports,
    SUM(import_fr_maroc) AS total_imports,
    SUM(export_fr_maroc - import_fr_maroc) AS net_balance,
    ROUND(AVG(export_fr_maroc - import_fr_maroc), 2) AS avg_balance_per_product
FROM trade_flows
WHERE year = 2026
GROUP BY region
ORDER BY net_balance DESC;

-- Croissance YoY des échanges (2025 vs 2026)
SELECT
    product,
    SUM(CASE WHEN year = 2026 THEN export_fr_maroc ELSE 0 END) AS exports_2026,
    SUM(CASE WHEN year = 2025 THEN export_fr_maroc ELSE 0 END) AS exports_2025,
    ROUND(
        (SUM(CASE WHEN year = 2026 THEN export_fr_maroc ELSE 0 END) -
         SUM(CASE WHEN year = 2025 THEN export_fr_maroc ELSE 0 END)) * 100.0 /
        NULLIF(SUM(CASE WHEN year = 2025 THEN export_fr_maroc ELSE 0 END), 0),
        2
    ) AS yoy_growth_pct
FROM trade_flows
GROUP BY product
ORDER BY yoy_growth_pct DESC;
