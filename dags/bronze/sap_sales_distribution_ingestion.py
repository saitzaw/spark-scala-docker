# sap_sales_distibution_ingestion.py : version 1.01 Date: 2025-10-04
#######################################################################
# Scheduler S&D ingestion using BashOperator
#######################################################################
#    Scheduler process from landing to bronze zone in parquet format.
#    version: 1.00 Author: Saithiha Zaw Date: 2025-10-05 Create
#######################################################################
#   Table list to ingest
#   1. VBRK - Sales Document: Header Data
#   2. VBRP - Sales Document: Item Data
#   3. VBFA - Sales Document Flow
#   4. VBAK - Sales Document: Header Data
#   5. VBAP - Sales Document: Item Data
#   6. VBEP - Sales Document: Schedule Line Data
#   7. VBUK - Sales Document: Header Status and Administrative Data
#   8. VBUP - Sales Document: Item Status
#   9. LIKP - SD Document: Delivery Header Data
#  10. LIPS - SD Document: Delivery: Item Data
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
    dag_id="sap_sales_distribution_ingestion",
    start_date=datetime(2025, 9, 1),
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
    tags=["sap", "bronze", "S&D"]
) as dag:

    vbrk_task = BashOperator(
        task_id="vbrk_to_bronze",
        bash_command='bash -lc "/opt/airflow/dags/scripts/spark_submit.sh sap_bronze sales_distributions vbrk" ',
    )

    vbrp_task = BashOperator(
        task_id="vbrp_to_bronze",
        bash_command='bash -lc "/opt/airflow/dags/scripts/spark_submit.sh sap_bronze sales_distributions vbrp" ',
    )

    vbfa_task = BashOperator(
        task_id="vbfa_to_bronze",
        bash_command='bash -lc "/opt/airflow/dags/scripts/spark_submit.sh sap_bronze sales_distributions vbfa" ',
    )

    vbak_task = BashOperator(
        task_id="vbak_to_bronze",
        bash_command='bash -lc "/opt/airflow/dags/scripts/spark_submit.sh sap_bronze sales_distributions vbak" ',
    )

    vbap_task = BashOperator(
        task_id="vbap_to_bronze",
        bash_command='bash -lc "/opt/airflow/dags/scripts/spark_submit.sh sap_bronze sales_distributions vbap" ',
    )

    vbep_task = BashOperator(
        task_id="vbep_to_bronze",
        bash_command='bash -lc "/opt/airflow/dags/scripts/spark_submit.sh sap_bronze sales_distributions vbep" ',
    )

    vbuk_task = BashOperator(
        task_id="vbuk_to_bronze",
        bash_command='bash -lc "/opt/airflow/dags/scripts/spark_submit.sh sap_bronze sales_distributions vbuk" ',
    )   

    vbup_task = BashOperator(
        task_id="vbup_to_bronze",
        bash_command='bash -lc "/opt/airflow/dags/scripts/spark_submit.sh sap_bronze sales_distributions vbup" ',
    )    

    likp_task = BashOperator(
        task_id="likp_to_bronze",
        bash_command='bash -lc "/opt/airflow/dags/scripts/spark_submit.sh sap_bronze sales_distributions likp" ',
    )

    lips_task = BashOperator(
        task_id="lips_to_bronze",
        bash_command='bash -lc "/opt/airflow/dags/scripts/spark_submit.sh sap_bronze sales_distributions lips" ',
    )
    # Task dependencies
    vbrk_task >> vbrp_task >> vbfa_task >> vbak_task >> vbap_task >> vbep_task >> vbuk_task >> vbup_task >> likp_task >> lips_task 
   

