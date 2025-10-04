# vbak.py : version 1.00 Date 2025-10-04
##################################################################################
#    Sales order header (Sales Order Document: SD Document Header)
###################################################################################
#    ETL process for SAP vbak data from landing to bronze zone in parquet format.
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
        "LANDING_URI": os.getenv("LANDING_URI", "s3a://landing/SAP/vbak.csv"),
        "BRONZE_URI": os.getenv("BRONZE_URI", "s3a://bronze/sap/vbak/"),
        "S3_ENDPOINT": os.getenv("S3_ENDPOINT", "http://minio:9000"),
    }
    return cfg


# --- Spark session ---
def build_spark(cfg: dict) -> SparkSession:
    return (
        SparkSession.builder
        .appName("VBAK_BRONZE")
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
# ERDAT - Creation Date
# AUDAT - Order Date
# VDATU - Request Delivery Date
# BSTDK - Purchase Order Date
# AEDAT - Date of Last Change
# ERZET - Time of Entry (creation)
# FMDAT - Material Availability Date (Actual Goods Issue Date / Delivery Completion Date)
#######################################################################
# --- Pure transform ---
def transform(df: DataFrame) -> DataFrame:
    # normalize date_from
    df = df.withColumn(
        "erdat",
            when((col("erdat").isNull()) | trim(col("erdat)" == ""))), lit('9999-12-31')).otherwise(
                date_format(to_date(col("erdat"),"dd/MM/yyyy"), "yyyy-MM-dd")
       ).withColumn(
        "audat",
            when((col("audat").isNull()) | trim(col("audat)" == ""))), lit('9999-12-31')).otherwise(
        date_format(to_date(col("audat"),"dd/MM/yyyy"), "yyyy-MM-dd")
       ).withColumn(    
        "vdatu",
        when((col("vdatu").isNull()) | trim(col("vdatu)" == ""))), lit('9999-12-31')).otherwise(
        date_format(to_date(col("vdatu"),"dd/MM/yyyy"), "yyyy-MM-dd")
       ).withColumn(
           "bstdk",
        when((col("bstdk").isNull()) | trim(col("bstdk)" == ""))), lit('9999-12-31')).otherwise(
        date_format(to_date(col("bstdk"),"dd/MM/yyyy"), "yyyy-MM-dd")
       ).withColumn(
           "aedat",
        when((col("aedat").isNull()) | trim(col("aedat)" == ""))), lit('9999-12-31')).otherwise(
        date_format(to_date(col("aedat"),"dd/MM/yyyy"), "yyyy-MM-dd")
       ).withColumn(
           "fmbdat",
        when((col("fmbdat").isNull()) | trim(col("fmbdat)" == ""))), lit('9999-12-31')).otherwise(
        date_format(to_date(col("fmbdat"),"dd/MM/yyyy"), "yyyy-MM-dd")
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