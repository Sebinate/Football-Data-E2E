{{ 
    config(
        materialized='table',
        unique_key='date_day'
    )
}}

{{ dbt_date.get_date_dimension("2020-01-01", "2030-12-31") }}