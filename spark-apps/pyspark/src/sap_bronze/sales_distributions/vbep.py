# vbep.py : version 1.00 Date 2025-10-04
##################################################################################
#    Sales Document: Schedule Line Data
###################################################################################
#    ETL process for SAP vbep data from landing to bronze zone in parquet format.
#    version: 1.00 Author: Sai Thiha Zaw Date: 2025-10-04 Create 
###################################################################################

import os
from pathlib import Path
from dotenv import load_dotenv
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, lit, DataFrame, to_date, date_format, trim 


# --- Config loading ---
def load_config(env_path: Path | None = None) -> dict:
    if env_path:
        load_dotenv(env_path)
    else:
        default_env = Path(__file__).resolve().parent.parent.parent / ".env"
        load_dotenv(default_env)
    cfg = {
        "JDBC_URL": os.getenv("JDBC_URL"),
        "DB_USER": os.getenv("POSTGRES_USER"),
        "DB_PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "SPARK_MASTER": os.getenv("SPARK_MASTER", "local[*]"),
        "PG_JAR": os.getenv("PG_JAR"),
        "PG_DRIVER": os.getenv("PG_DRIVER"),
        "EVENT_LOG_DIR": os.getenv("EVENT_LOG_DIR", "/tmp"),
        "MINIO_USER": os.getenv("MINIO_USER"),
        "MINIO_PASSWORD": os.getenv("MINIO_PASSWORD"),
        "LANDING_URI": os.getenv("LANDING_URI", "s3a://landing/SAP/vbep.csv"),
        "BRONZE_URI": os.getenv("BRONZE_URI", "s3a://bronze/sap/vbep/"),
        "S3_ENDPOINT": os.getenv("S3_ENDPOINT", "http://minio:9000"),
    }
    return cfg


# --- Spark session ---
def build_spark(cfg: dict) -> SparkSession:
    return (
        SparkSession.builder
        .appName("VBFA_BRONZE")
        .master(cfg["SPARK_MASTER"])
        .config("spark.hadoop.fs.s3a.endpoint", cfg["S3_ENDPOINT"])
        .config("spark.hadoop.fs.s3a.access.key", cfg["MINIO_USER"])
        .config("spark.hadoop.fs.s3a.secret.key", cfg["MINIO_PASSWORD"])
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
        .config("spark.eventLog.enabled", "true")
        .getOrCreate()
    )

#######################################################################
# Key date fields to normalize
#######################################################################
# EDATU - Schedule Line Delivery Date
# TDDAT - Delivery Date
# MBDAT - Material Document Date in Document (Material Availability Date)
# LDDAT - Delivery Date
# WADAT - Goods issue date (When it really left warehouse)
# handoverdate
#######################################################################
# --- Pure transform ---
def transform(df: DataFrame) -> DataFrame:
    # normalize date_from
    df = df.withColumn(
        "edatu",
            when((col("edatu").isNull()) | trim(col("edatu)" == "")), lit('9999-12-31')).otherwise(
                date_format(to_date(col("edatu"),"dd/MM/yyyy"), "yyyy-MM-dd")
        )
       ).withColumn(
        "tddat",
            when((col("tddat").isNull()) | trim(col("tddat)" == "")), lit('9999-12-31')).otherwise(
                date_format(to_date(col("tddat"),"dd/MM/yyyy"), "yyyy-MM-dd")
        )
       ).withColumn(
        "mbdat",
            when((col("mbdat").isNull()) | trim(col("mbdat)" == "")), lit('9999-12-31')).otherwise(
                date_format(to_date(col("mbdat"),"dd/MM/yyyy"), "yyyy-MM-dd")
        )
       ).withColumn(
        "lddat",
            when((col("lddat").isNull()) | trim(col("lddat)" == "")), lit('9999-12-31')).otherwise(
                date_format(to_date(col("lddat"),"dd/MM/yyyy"), "yyyy-MM-dd")
        )
       ).withColumn(
        "wadat",
            when((col("wadat").isNull()) | trim(col("wadat)" == "")), lit('9999-12-31')).otherwise(
                date_format(to_date(col("wadat"),"dd/MM/yyyy"), "yyyy-MM-dd")
        )
       ).withColumn(
        "handoverdate",
            when((col("handoverdate").isNull()) | trim(col("handoverdate)" == "")), lit('9999-12-31')).otherwise(
                date_format(to_date(col("handoverdate"),"dd/MM/yyyy"), "yyyy-MM-dd")
        )
       )
    return df

#######################################################################
# Read raw data from landing zone, transform and write to bronze zone
#######################################################################

# --- IO wrappers (thin) ---
def read_landing(spark: SparkSession, uri: str) -> DataFrame:
    return (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(uri)
    )

def write_bronze(df: DataFrame, uri: str) -> None:
    # legacy datetime behavior for parquet consistency
    df.sparkSession.conf.set("spark.sql.parquet.datetimeRebaseModeInWrite", "LEGACY")
    df.write.mode("overwrite").parquet(uri)

#######################################################################
# Main ETL process
#######################################################################
def main():
    cfg = load_config()
    spark = build_spark(cfg)
    df = read_landing(spark, cfg["LANDING_URI"])
    out = transform(df)
    write_bronze(out, cfg["BRONZE_URI"])

if __name__ == "__main__":
    main()