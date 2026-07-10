{{
    config(
        materialized='table',
        unique_key='league_id'
        )
}}

WITH silver_leagues AS (
    SELECT * FROM {{ ref('leagues_to_silver') }}
),

cleaned_standardized AS (
    SELECT
        league_id,
        TRIM(league_name) AS league_name,
        LOWER(TRIM(league_type)) AS league_type,
        COALESCE(league_logo, 'N/A') AS league_logo,
        COALESCE(TRIM(league_country_name), 'N/A') AS league_country_name,
        COALESCE(league_country_code, 'N/A') AS league_country_code,
        COALESCE(league_country_flag, 'N/A') AS league_country_flag,
        data_load_date,
        loaded_at,
        CURRENT_TIMESTAMP() AS transformed_at
    FROM silver_leagues
),

deduplicated AS (
    SELECT *
    FROM cleaned_standardized
    QUALIFY ROW_NUMBER() OVER(
        PARTITION BY league_id
        ORDER BY data_load_date DESC, transformed_at DESC
    ) = 1
)

SELECT * FROM deduplicated