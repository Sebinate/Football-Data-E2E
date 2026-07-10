{{ 
    config(
        materialized='table',
        unique_key='venue_id'
        ) 
}}

WITH silver_venue AS (
    SELECT * FROM {{ ref('teams_to_silver') }}
),

cleaned_standardized AS (
    SELECT
        team_venue_id AS venue_id,
        TRIM(team_venue_name) AS venue_name,
        TRIM(team_venue_address) AS venue_address,
        TRIM(team_city) AS venue_city,
        COALESCE(team_capacity, 0) AS venue_capacity,
        LOWER(TRIM(team_surface)) AS venue_surface,
        data_load_date,
        loaded_at,
        CURRENT_TIMESTAMP() AS transformed_at
    FROM silver_venue
),

deduplicated AS (
    SELECT *
    FROM cleaned_standardized
    QUALIFY ROW_NUMBER() OVER(
        PARTITION BY venue_id
        ORDER BY data_load_date DESC, loaded_at DESC
    ) = 1
)

SELECT * FROM deduplicated