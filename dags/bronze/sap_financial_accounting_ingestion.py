# sap_financial_ingestion.py : version 1.01 Date: 2025-10-04
#######################################################################
# Scheduler FI ingestion using BashOperator
#######################################################################
#    Scheduler process from landing to bronze zone in parquet format.
#    version: 1.00 Author: Saithiha Zaw Date: 2025-10-05 Create
#######################################################################
#   Table list to ingest
#   1. BKPF - Accounting Document Header
#   2. BSEG - Accounting Document Segment
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
    dag_id="sap_financial_accounting_ingestion",
    start_date=datetime(2025, 9, 1),
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
    tags=["sap", "bronze", "FI"]
) as dag:

    bkpf_task = BashOperator(
        task_id="pkpf_to_bronze",
        bash_command='bash -lc "/opt/airflow/dags/scripts/spark_submit.sh sap_bronze financial_accounting bkpf" ',
    )

    bseg_task = BashOperator(
        task_id="bseg_to_bronze",
        bash_command='bash -lc "/opt/airflow/dags/scripts/spark_submit.sh sap_bronze financial_accounting bseg" ',
    )

   
    # Task dependencies
    bkpf_task >> bseg_task
   

