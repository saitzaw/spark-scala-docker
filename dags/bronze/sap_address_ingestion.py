from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "airflow",
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="sap_address_ingestion",
    start_date=datetime(2025, 9, 1),
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
    tags=["spark", "bronze", "sap"],
) as dag:

    adr6_task = BashOperator(
        task_id="adr6_to_bronze",
        bash_command="/opt/airflow/dags/scripts/spark_submit.sh adr6 ",
    )

    adrc_task = BashOperator(
        task_id="adrc_to_bronze",
        bash_command="/opt/airflow/dags/scripts/spark_submit.sh adrc ",
    )

    adrct_task = BashOperator(
        task_id="adrct_to_bronze",
        bash_command="/opt/airflow/dags/scripts/spark_submit.sh adrct ",
    )

    adrt_task = BashOperator(
        task_id="adrt_to_bronze",
        bash_command="/opt/airflow/dags/scripts/spark_submit.sh adrt ",
    )

    adr6_task >> adrc_task >> adrct_task >> adrt_task
