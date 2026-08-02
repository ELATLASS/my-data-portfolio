-- 2026-W32-maroc : Requêtes SQL pour l'analyse des données marocaines

-- Exemple : Top 10 villes par population (source fictive)
WITH city_population AS (
    SELECT
        city_name,
        population,
        region,
        population / NULLIF(LAG(population) OVER (ORDER BY population DESC), 0) AS ratio_to_prev
    FROM morocco_cities
    WHERE year = 2026
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

-- Exemple : Distribution géographique par région
SELECT
    region,
    COUNT(*) AS num_cities,
    SUM(population) AS total_population,
    AVG(population) AS avg_population,
    MAX(population) AS max_population
FROM morocco_cities
GROUP BY region
ORDER BY total_population DESC;

-- Exemple : Croissance urbaine (fenêtre glissante sur 5 ans)
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