from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.models import Variable
from datetime import datetime, timedelta

default_args = {"retries": 1, "retry_delay": timedelta(minutes=5)}

with DAG(
    dag_id=f"seo_{Variable.get('PROJECT_ID')}",
    schedule_interval="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args=default_args,
) as dag:

    crawl = BashOperator(
        task_id="crawl",
        bash_command="python /opt/airflow/crawler/run.py --start-url '{{ var.value.START_URL }}' --project '{{ var.value.PROJECT_ID }}'",
        env={
            "SUPABASE_URL": Variable.get("SUPABASE_URL"),
            "SUPABASE_SERVICE_ROLE": Variable.get("SUPABASE_SERVICE_ROLE"),
        },
    )
