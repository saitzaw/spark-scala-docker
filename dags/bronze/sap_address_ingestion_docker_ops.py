# sap_address_ingestion_docker_ops : version 1.00 Date: 2025-10-04
#######################################################################
# Address ingestion using DockerOperator
#######################################################################
#    Scheduler process from landing to bronze zone in parquet format.
#    version: 1.00 Author: Saithiha Zaw Date: 2025-09-28 Create
########################################################################

from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.models import Variable

from docker.types import Mount


HOST_APPS = Variable.get("HOST_SPARK_APPS")
HOST_LOGS = Variable.get("HOST_SPARK_LOGS")
# In-container paths (must match your Spark containers)
IN_APPS = "/opt/spark/jobs"
IN_LOGS = "/opt/spark/spark-events"

SPARK_IMAGE = "spark-image"   # built from docker/spark.Dockerfile
NETWORK = "enterprise-data-lakehouse_default" 

default_args = {
    "owner": "airflow",
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}

def spark_task(task_id: str, medallion:str, zone: str, table: str) -> DockerOperator:
    return DockerOperator(
        task_id=task_id,
        image=SPARK_IMAGE,
        command=[
            "spark-submit",
            "--master", "spark://spark-master:7077",
            "--packages", "org.apache.hadoop:hadoop-aws:3.3.2,com.amazonaws:aws-java-sdk-bundle:1.12.262",
            "--conf", "spark.eventLog.enabled=true",
            "--conf", f"spark.eventLog.dir={IN_LOGS}",
            f"{IN_APPS}/pyspark/src/{medallion}/{zone}/{table}.py",

        ],
        network_mode=NETWORK,
        auto_remove=True,
        mount_tmp_dir=False,  # we control the mounts explicitly
        mounts=[
            Mount(source=HOST_APPS, target=IN_APPS, type="bind", read_only=True),
            Mount(source=HOST_LOGS, target=IN_LOGS, type="bind"),
        ],
    )

with DAG(
    dag_id="sap_address_ingestion_docker_ops",
    start_date=datetime(2025, 9, 1),
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
    tags=["spark", "bronze", "sap"],
) as dag:

    adr6  = spark_task("adr6_to_bronze", "bronze_sap","address","adr6")
    adrc  = spark_task("adrc_to_bronze", "bronze_sap","address","adrc")
    adrct = spark_task("adrct_to_bronze", "bronze_sap","address","adrct")


    adr6 >> adrc >> adrct 
