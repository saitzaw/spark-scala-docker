# sap_vendor_ingestion.py : version 1.01 Date: 2025-10-04
#######################################################################
# Scheduler S&D,MM,FI ingestion using BashOperator
#######################################################################
#    Scheduler process from landing to bronze zone in parquet format.
#    version: 1.00 Author: Saithiha Zaw Date: 2025-10-05 Create
#######################################################################
#   Table list to ingest
#   1. LFA1 - Vendor Master (Company Code)
#   2. BUT000 -  central Business Partner master data
#   3. BUT020 -  Business Partner Address Link Table
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
    dag_id="sap_vendor_partner_ingestion",
    start_date=datetime(2025, 9, 1),
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
    tags=["sap", "bronze", "S&D_MM_FI"]
) as dag:

    lfa1_task = BashOperator(
        task_id="lfa1_to_bronze",
        bash_command='bash -lc "/opt/airflow/dags/scripts/spark_submit.sh sap_bronze vendor lfa1" ',
    )

    but000_task = BashOperator(
        task_id="but000_to_bronze",
        bash_command='bash -lc "/opt/airflow/dags/scripts/spark_submit.sh sap_bronze partner but000" ',
    )

    but020_task = BashOperator(
        task_id="but020_to_bronze",
        bash_command='bash -lc "/opt/airflow/dags/scripts/spark_submit.sh sap_bronze partner but020" ',
    )

   
    # Task dependencies
    lfa1_task >> but000_task >> but020_task
   

