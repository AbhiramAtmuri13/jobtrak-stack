from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
import os

# Add scripts folder to sys.path so we can import fetch_jobs.py
sys.path.append(os.path.join(os.path.dirname(__file__), '../../scripts'))

from fetch_jobs import fetch_and_store_jobs  # this function should be defined in your fetch_jobs.py

with DAG(
    dag_id="jobtrak_fetch_jobs_dag",
    start_date=datetime(2023, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["jobtrak"],
) as dag:
    fetch_jobs_task = PythonOperator(
        task_id="fetch_and_store_jobs",
        python_callable=fetch_and_store_jobs,
    )
