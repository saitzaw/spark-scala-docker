""" adr6.py : version 1.00
ETL process for SAP ADR6 data from landing to bronze zone in parquet format.
version: 1.00
Author: Saithiha Zaw
Date: 2024-10-05
"""


import sys
import os
import pyspark
from pathlib import Path
from dotenv import load_dotenv
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, lit

## 
# Load from .env file
dotenv_path = Path(__file__).resolve().parent.parent / ".env"  
load_dotenv(dotenv_path)

jdbc_url = os.getenv("JDBC_URL")
db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
spark_master = os.getenv("SPARK_MASTER")
pg_jar = os.getenv("PG_JAR")
event_log_dir = os.getenv("EVENT_LOG_DIR")
pg_driver = os.getenv("PG_DIRIVER")
minio_user = os.getenv("MINIO_USER")
minio_pass = os.getenv("MINIO_PASSWORD")

# Initialize Spark session
spark = SparkSession.builder \
    .appName("ADR6") \
    .master(spark_master) \
    .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
    .config("spark.hadoop.fs.s3a.access.key", minio_user) \
    .config("spark.hadoop.fs.s3a.secret.key", minio_pass) \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false") \
    .config("spark.eventLog.enabled", "true") \
    .getOrCreate()

# read data from landing zone (adr6.csv)
df_landing = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv("s3a://landing/SAP/adr6.csv")

# configure spark to handle legacy datetime format
spark.conf.set("spark.sql.parquet.datetimeRebaseModeInWrite", "LEGACY")

# transformations (if any)
df_landing.withColumnRenamed("addrnumber", "address_number")

df_modify = df_landing.withColumn(
    "date_from",
    when(col("date_from") == "0001-01-01", lit("1900-01-01")).otherwise(col("date_from"))
)
# write data to bronze zone in parquet format
df_modify.write \
    .mode("overwrite") \
    .parquet("s3a://bronze/sap/adr6/")