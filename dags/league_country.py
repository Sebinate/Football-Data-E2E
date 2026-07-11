from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'data_engineering_team',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='football_metadata_pipeline',
    default_args=default_args,
    schedule='@yearly',
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['football', 'api', 'metadata']
) as dag:
    seasons = ['2022', '2023', '2024'] # Add as necessary but created for api limits reason (Remove if unlimited and catchup = True)
    
    dim_date = BashOperator(
        task_id='dim_date',
        bash_command='cd /opt/airflow/footballapi_sports_DEProject && dbt run --select dim_date'
    )

    dim_league = BashOperator(
        task_id='dim_leage',
        bash_command=f'cd /opt/airflow/footballapi_sports_DEProject && dbt run --select +dim_leagues'
    )

    dim_team = BashOperator(
        task_id='dim_team',
        bash_command=f'cd /opt/airflow/footballapi_sports_DEProject && dbt run --select +dim_venues +dim_teams'
    )

    extract_league = BashOperator(
        task_id='extract_league_season',
        bash_command='python /opt/airflow/scripts/league_runner.py' 
    )
    
    for season in seasons:
        extract_team = BashOperator(
            task_id=f'extract_team_{season}',
            bash_command=f'python /opt/airflow/scripts/teams_runner.py {season}'
        )

        extract_team >> dim_team

    extract_league >> dim_league

