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
    dag_id='football_fixture_pipeline',
    default_args=default_args,
    schedule='@weekly',
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['football', 'api', 'fixture']
) as dag:
    seasons = ['2022', '2023', '2024'] # Add as necessary but created for api limits reason (Remove if unlimited and catchup = True)

    dim_fixture = BashOperator(
        task_id='dim_fixture',
        bash_command='cd /opt/airflow/footballapi_sports_DEProject && dbt run --select +dim_fixture'
    )
    
    validates = []

    for season in seasons:
        extract_fixture = BashOperator(
            task_id=f'extract_fixture_{season}',
            bash_command=f'python /opt/airflow/scripts/fixture_runner.py {season}'
        )

        validate_fixture = BashOperator(
            task_id=f'validate_fixture_{season}',
            bash_command=f'python /opt/airflow/data_validation/runners/fact_runner.py {season}'
        )
        
        extract_fixture >> validate_fixture

        validates.append(validate_fixture)

    validates >> dim_fixture