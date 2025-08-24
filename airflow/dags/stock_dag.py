from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import sys

# make sure Python can find our scripts folder
sys.path.append(os.path.join(os.path.dirname(__file__), "../scripts"))
from fetch_data import fetch_and_store_stock_data

# Default DAG arguments
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Define the DAG
with DAG(
    dag_id="stock_data_pipeline",
    default_args=default_args,
    description="Fetch daily stock data from Alpha Vantage and store in Postgres",
    schedule_interval="@daily",   # runs once every day
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    fetch_and_store = PythonOperator(
        task_id="fetch_and_store",
        python_callable=fetch_and_store_stock_data,
    )

    fetch_and_store
