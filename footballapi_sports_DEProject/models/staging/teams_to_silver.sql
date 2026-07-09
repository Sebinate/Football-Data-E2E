{{ config(materialized='view') }}

WITH teams_source AS (
    SELECT $1 AS json_payload,
    METADATA$FILENAME AS s3_file_path
    FROM @{{ source('football_api_source', 'S3_RAW_STAGE') }}/api_football/teams/
)

SELECT
    (json_payload:team:id)::INT AS team_id,
    (json_payload:team:name)::VARCHAR AS team_name,
    (json_payload:team:code)::CHAR(3) AS team_code,
    (json_payload:team:logo)::VARCHAR AS team_logo,
    (json_payload:venue:name)::VARCHAR AS team_venue_name,
    (json_payload:venue:address)::VARCHAR AS team_venue_address,
    (json_payload:venue:city)::VARCHAR AS team_city,
    (json_payload:venue:capacity)::INT AS team_capacity,
    (json_payload:venue:surface)::VARCHAR AS team_surface,

    REGEXP_SUBSTR(s3_file_path, 'load_date=([^/]+)', 1, 1, 'e')::DATE AS data_load_date,
    CURRENT_TIMESTAMP() AS transformed_at

FROM teams_source