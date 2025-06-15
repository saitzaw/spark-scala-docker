from datetime import datetime
from airflow import DAG
from airflow.models import Variable
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 6, 1),
    'retries': 1,
}

with DAG(
    dag_id='submit_crm_spark_job',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    description='Run Scala Spark CRM job via spark-submit',
) as dag:
    
    db_jar = Variable.get("DATABASE_JAR_FILE1")
    spark_master_url = Variable.get("SPARK_MASTER_URL", default_var='spark://spark-master:7077')
    db_user = Variable.get("SPARK_DB_USER")
    db_pass = Variable.get("SPARK_DB_PASS")
    db_url = Variable.get("SPARK_DB_URL")


    submit_crm_job = SparkSubmitOperator(
        task_id='run_old_single_view_crm',
        application='/opt/spark/jobs/scala/target/scala-2.12/oldsingleviewcrm_2.12-0.1.jar',
        conn_id='spark_default',  # or leave blank if not using Spark hook
        java_class='OldSingleViewCRM',
        jars=db_jar,
        conf={
            'spark.master': spark_master_url,
            'spark.db.user': db_user, 
            'spark.db.pass': db_pass,
            'spark.db.url': db_url,
        },
        dag=dag,
    )

    submit_crm_job
