# adrct.py : version 1.02 Date: 2025-10-05
#########################################################################################################
#    Title / Salutation Info
#########################################################################################################
#    ETL process for SAP ADRT data from landing to bronze zone in parquet format.
#    version: 1.00 Author: Saithiha Zaw Date: 2025-09-28 Create
#    version: 1.01 Author: Saithiha Zaw Date: 2025-10-04 Modify to improve readiability and testability
#    version: 1.02 Author: Sai Thiha Zaw Date: 2025-10-05 Fix pyspark import DataFrame
#########################################################################################################

import os
from pathlib import Path
from dotenv import load_dotenv
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, when, lit

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
        "LANDING_URI": os.getenv("LANDING_URI", "s3a://landing/SAP/adrt.csv"),
        "BRONZE_URI": os.getenv("BRONZE_URI", "s3a://bronze/sap/adrt/"),
        "S3_ENDPOINT": os.getenv("S3_ENDPOINT", "http://minio:9000"),
    }
    return cfg


# --- Spark session ---
def build_spark(cfg: dict) -> SparkSession:
    return (
        SparkSession.builder
        .appName("ADRT_BRONZE")
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

# --- Pure transform ---
def transform(df: DataFrame) -> DataFrame:
    # NOTE: assign the rename
    df = df.withColumnRenamed("addrnumber", "address_number")\
            .withColumnRenamed("persnumber", "personnel_number")\
            .withColumnRenamed("langu", "language")
    
    # normalize date_from
    df = df.withColumn(
    "date_from",
        when(
                col("date_from") == "0001-01-01",
                lit("1900-01-01")
            ).otherwise(
                col("date_from")
            )
        )
    return df

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

def main():
    cfg = load_config()
    spark = build_spark(cfg)
    df = read_landing(spark, cfg["LANDING_URI"])
    out = transform(df)
    write_bronze(out, cfg["BRONZE_URI"])

if __name__ == "__main__":
    main()
