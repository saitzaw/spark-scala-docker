# sap_financial_accounting_ingestion.py : version 1.01 Date: 2025-10-04
#######################################################################
# Scheduler S&D,MM,FI ingestion using BashOperator
#######################################################################
#    Scheduler process from landing to bronze zone in parquet format.
#    version: 1.00 Author: Saithiha Zaw Date: 2025-10-05 Create
#######################################################################
#   Table list to ingest
#   1. ADRT - Address (Text)
#   2. KNA1 - Customer Master (General)
#######################################################################


from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="sap_vendor_ingestion",
    start_date=datetime(2025, 9, 1),
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
    tags=["sap", "bronze", "FI"]
) as dag:

    adrt_task = BashOperator(
        task_id="pkpf_to_bronze",
        bash_command='bash -lc "/opt/airflow/dags/scripts/spark_submit.sh sap_bronze customer adrt" ',
    )

    kna1_task = BashOperator(
        task_id="bseg_to_bronze",
        bash_command='bash -lc "/opt/airflow/dags/scripts/spark_submit.sh sap_bronze customer kna1" ',
    )

   
    # Task dependencies
    adrt_task >> kna1_task
   

