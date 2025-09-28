#!/bin/bash
# Usage: ./spark_submit.sh <job_name>
# Example: ./spark_submit.sh adr6

JOB_NAME=$1

if [ -z "$JOB_NAME" ]; then
  echo "No job name provided!"
  echo "Usage: $0 <job_name>"
  exit 1
fi

/opt/spark/bin/spark-submit \
  --master spark://spark-master:7077 \
  --packages org.apache.hadoop:hadoop-aws:3.3.2,com.amazonaws:aws-java-sdk-bundle:1.12.262 \
  --conf spark.log.type=INFO \
  --conf spark.interface.name=VTLINK \
  --conf spark.eventLog.enabled=true \
  --conf spark.eventLog.dir=/tmp \
  "/opt/spark/jobs/pyspark/src/sap_bronze/${JOB_NAME}.py"
