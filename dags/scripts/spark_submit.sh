#!/bin/bash

# Version: 1.01 Date: 2025-10-04
#############################################################
# Script to submit Spark job to Spark cluster in Docker
#############################################################
# Usage: ./spark_submit.sh <medallion> <zone> <job_name>
# Example: ./spark_submit.sh sap_bronze address adr6
# Author: Sai Thiha Zaw Version: 1.00 Date: 2025-09-28 Create
# Author: Sai Thiha Zaw Version: 1.01 Date: 2025-10-04 Expand to accept zone and job name as arguments
# 
#############################################################

MEDALLION=$1
ZONE=$2
JOB_NAME=$3

if [ -z "$MEDALLION" ] || [ -z "$ZONE" ] || [ -z "$JOB_NAME" ] ; then
  echo "No job name provided!"
  echo "Usage: $0 <medallion> <zone> <job_name>"
  exit 1
fi

docker exec spark-master /opt/spark/bin/spark-submit \
  --master spark://spark-master:7077 \
  --packages org.apache.hadoop:hadoop-aws:3.3.2,com.amazonaws:aws-java-sdk-bundle:1.12.262 \
  --conf spark.log.type=INFO \
  --conf spark.interface.name=VTLINK \
  --conf spark.eventLog.enabled=true \
  --conf spark.eventLog.dir=/tmp \
  "/opt/spark/jobs/pyspark/src/${MEDALLION}/${ZONE}/${JOB_NAME}.py"
