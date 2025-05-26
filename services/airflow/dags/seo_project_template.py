from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
import os

DEFAULT_ARGS = {"owner": "seo", "depends_on_past": False}

with DAG(
    dag_id="seo_project_template",
    description="Crawl + Parse for a given domain",
    default_args=DEFAULT_ARGS,
    schedule_interval="@weekly",
    start_date=days_ago(0),
    catchup=False,
) as dag:

    start_url = os.getenv("START_URL") or '{{ var.value.START_URL }}'

    crawl = BashOperator(
        task_id="crawl",
        bash_command=f"scrapy crawl generic_site -a start_url={start_url}",
        env={
            "SUPABASE_URL": os.getenv("SUPABASE_URL"),
            "SUPABASE_SERVICE_ROLE": os.getenv("SUPABASE_SERVICE_ROLE"),
        },
    )