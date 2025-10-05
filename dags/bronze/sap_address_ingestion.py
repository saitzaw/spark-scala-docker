# sap_address_ingestion : version 1.01 Date: 2025-10-04
#######################################################################
# Scheduler Address ingestion using BashOperator
#######################################################################
#    Scheduler process from landing to bronze zone in parquet format.
#    version: 1.00 Author: Saithiha Zaw Date: 2025-09-28 Create
#    version: 1.01 Author: Saithiha Zaw Date: 2025-10-04 Modify to use BashOperator
#######################################################################

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
    tags=["address", "bronze", "sap"]
) as dag:

    adr6_task = BashOperator(
        task_id="adr6_to_bronze",
        bash_command='bash -lc "/opt/airflow/dags/scripts/spark_submit.sh sap_bronze address adr6" ',
    )

    adrc_task = BashOperator(
        task_id="adrc_to_bronze",
        bash_command='bash -lc "/opt/airflow/dags/scripts/spark_submit.sh sap_bronze address adrc" ',
    )

    adrct_task = BashOperator(
        task_id="adrct_to_bronze",
        bash_command='bash -lc "/opt/airflow/dags/scripts/spark_submit.sh sap_bronze address adrct" ',
    )

    adr6_task >> adrc_task >> adrct_task 
