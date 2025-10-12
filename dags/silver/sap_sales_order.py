# sap_sale_orders.py : version 1.00 Date: 2025-10-05
#######################################################################
# Scheduler Sale orders using BashOperator
#######################################################################
#    Scheduler process from bronze to silver zone in delta format with SCD type 2.
#    version: 1.00 Author: Saithiha Zaw Date: 2025-10-05 Create
#######################################################################
#   Table list to ingest
# 1. VBAK - Sales Document: Header Data
# 2. VBAP - Sales Document: Item Data
# 3. VBEP - Sales Document: Schedule Line Data
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
    dag_id="sap_sales_documents",
    start_date=datetime(2025, 9, 1),
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
    tags=["sap", "silver", "S&D_sales"]
) as dag:

    sale_header_task = BashOperator(
        task_id="sale_header_to_silver",
        bash_command='bash -lc "/opt/airflow/dags/scripts/delta_spark_submit.sh sap_silver sales sale_orders_header" ',
    )

    sale_lines_task = BashOperator(
        task_id="sale_lines_to_silver",
        bash_command='bash -lc "/opt/airflow/dags/scripts/delta_spark_submit.sh sap_silver sales sale_orders_lines" ',
    )

    sale_schedule_task = BashOperator(
        task_id="sale_schedule_to_silver",
        bash_command='bash -lc "/opt/airflow/dags/scripts/delta_spark_submit.sh sap_silver sales sale_schedule" ',
    )

   
    # Task dependencies
    sale_header_task >> sale_lines_task >> sale_schedule_task
   

