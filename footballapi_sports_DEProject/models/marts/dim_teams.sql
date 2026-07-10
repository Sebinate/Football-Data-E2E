{{
    config(
        materialized='table',
        unique_key='team_id'
        )
}}

WITH silver_teams AS (
    SELECT * FROM {{ ref('teams_to_silver') }}
    {% if is_incremental() %}
        WHERE data_load_date >= (SELECT MAX(data_load_date) FROM {{ this }})
    {% endif %}
),

cleaned_standardized AS (
    SELECT 
        team_id,
        TRIM(team_name) AS team_name,
        TRIM(COALESCE(team_code, 'N/A')) AS team_code,
        TRIM(COALESCE(team_logo, 'N/A')) AS team_logo,
        data_load_date,
        loaded_at,
        CURRENT_TIMESTAMP() AS transformed_at
    FROM silver_teams
),

deduplicated AS (
    SELECT *
    FROM cleaned_standardized
    QUALIFY ROW_NUMBER() OVER(
        PARTITION BY team_id
        ORDER BY data_load_date DESC, loaded_at DESC
    ) = 1
)

SELECT * FROM deduplicated