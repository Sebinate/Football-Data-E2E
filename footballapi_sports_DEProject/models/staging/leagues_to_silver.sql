{{ config(materialized='view') }}

WITH league_source AS (
    SELECT $1 AS json_payload,
    METADATA$FILENAME AS s3_file_path
    FROM @{{ source('football_api_source', 'S3_RAW_STAGE') }}/api_football/leagues/
)

SELECT
    (json_payload:league:id)::INT AS league_id,
    (json_payload:league:name)::VARCHAR AS league_name,
    (json_payload:league:type)::VARCHAR AS league_type,
    (json_payload:league:logo)::VARCHAR AS league_logo,
    (json_payload:country:name)::VARCHAR AS league_country_name,
    (json_payload:country:code)::CHAR(6) AS league_country_code,
    (json_payload:country:flag)::VARCHAR AS league_country_flag,
    REGEXP_SUBSTR(s3_file_path, 'load_date=([^/]+)', 1, 1, 'e')::DATE AS data_load_date,
    CURRENT_TIMESTAMP() AS transformed_at

FROM league_source