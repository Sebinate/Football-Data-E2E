{{ config(materialized='view') }}

WITH fixtures_source AS (
    SELECT $1 AS json_payload,
    METADATA$FILENAME AS s3_file_path
    FROM @{{ source('football_api_source', 'S3_RAW_STAGE') }}/api_football/fixtures/
)

SELECT
    (json_payload:fixture:id)::INT AS fixture_id,
    (json_payload:fixture:referee)::VARCHAR AS fixture_referee,
    (json_payload:fixture:timezone)::VARCHAR AS fixture_timezone,
    (json_payload:fixture:date)::TIMESTAMP_TZ AS fixture_date,
    (json_payload:fixture:venue:name)::VARCHAR AS fixture_name,
    (json_payload:status:short)::VARCHAR AS fixture_status,
    (json_payload:status:elapsed)::INT AS fixture_length,
    (json_payload:league:name)::VARCHAR AS fixture_league,
    (json_payload:league:season)::INT AS fixture_season,
    (json_payload:league:round)::VARCHAR AS fixture_round,
    (json_payload:teams:home:name)::VARCHAR AS fixture_home_team,
    (json_payload:teams:home:winner)::BOOLEAN AS fixture_home_win,
    (json_payload:teams:away:name)::VARCHAR AS fixture_away_team,
    (json_payload:teams:away:winner)::BOOLEAN AS fixture_away_win,
    (json_payload:goals:home)::INT AS fixture_home_fulltime_goals,
    (json_payload:goals:away)::INT AS fixture_away_fulltime_goals,
    (json_payload:score:halftime:home)::INT AS fixture_home_halftime_score,
    (json_payload:score:halftime:away)::INT AS fixture_away_halftime_score,

    REGEXP_SUBSTR(s3_file_path, 'load_date=([^/]+)', 1, 1, 'e')::DATE AS data_load_date,
    CURRENT_TIMESTAMP() AS transformed_at

FROM fixtures_source