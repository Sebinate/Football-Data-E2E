{{ 
    config(
        materialized='incremental',
        unique_key='fixture_id'
    )
}}

WITH silver_fixtures AS (
    SELECT * FROM {{ ref('fixture_to_silver') }}
    {% if is_incremental() %}
        WHERE data_load_date >= (SELECT MAX(data_load_date) FROM {{ this }})
    {% endif %}
),

dim_teams AS (
    SELECT * FROM {{ ref('dim_teams') }}
),

dim_venues AS (
    SELECT * FROM {{ ref('dim_venues') }}
),

dim_leagues AS (
    SELECT * FROM {{ ref('dim_leagues') }}
),

dim_date AS (
    SELECT * FROM {{ ref('dim_date') }}
),

mapped AS (
    SELECT 
        f.fixture_id,
        TRIM(f.fixture_referee) AS fixture_referee,
        TRIM(f.fixture_timezone) AS fixture_timezone,
        
        -- DATES
        f.fixture_date AS fixture_at,
        TO_DATE(f.fixture_date) AS fixture_date,
        TO_TIME(f.fixture_date) AS fixture_time,
        COALESCE(v.venue_id, -1) AS fixture_venue,
        f.fixture_status,
        f.fixture_length,
        COALESCE(l.league_id, -1) AS fixture_league,
        f.fixture_season,
        f.fixture_round,
        COALESCE(home.team_id, -1) AS fixture_home_team,
        COALESCE(away.team_id, -1) AS fixture_away_team,
        COALESCE(f.fixture_home_win, FALSE) AS fixture_home_win,
        COALESCE(f.fixture_away_win, FALSE) AS fixture_away_win,
        CASE
            WHEN NOT COALESCE(f.fixture_home_win, FALSE) 
             AND NOT COALESCE(f.fixture_away_win, FALSE) THEN TRUE
            ELSE FALSE
        END AS fixture_is_draw,
        f.fixture_home_fulltime_goals,
        f.fixture_away_fulltime_goals,
        f.fixture_home_halftime_score AS fixture_home_halftime_goals,
        f.fixture_away_halftime_score AS fixture_away_halftime_goals,
        f.data_load_date,
        f.loaded_at,
        CURRENT_TIMESTAMP() AS transformed_at
        
    FROM silver_fixtures AS f
    LEFT JOIN dim_teams AS home
        ON UPPER(TRIM(f.fixture_home_team)) = UPPER(TRIM(home.team_name))
    LEFT JOIN dim_teams AS away
        ON UPPER(TRIM(f.fixture_away_team)) = UPPER(TRIM(away.team_name))
    LEFT JOIN dim_venues AS v
        ON UPPER(TRIM(f.fixture_name)) = UPPER(TRIM(v.venue_name))
    LEFT JOIN dim_leagues AS l
        ON UPPER(TRIM(f.fixture_league)) = UPPER(TRIM(l.league_name))
),

deduplicated AS (
    SELECT *
    FROM mapped
    QUALIFY ROW_NUMBER() OVER(
        PARTITION BY fixture_id
        ORDER BY data_load_date DESC, loaded_at DESC
    ) = 1
)

SELECT * FROM deduplicated