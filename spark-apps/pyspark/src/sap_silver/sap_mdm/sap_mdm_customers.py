#!/usr/bin/env python3
#  sap_mdm_customers.py : version 1.00 Date 2025-10-12
#########################################################################################################
#    MASTER DATA FOR CUSTOMERS
#########################################################################################################
#    ETL process for SAP VBAK data from bronze to silver zone in delta format with SCD type 2.
#    version: 1.00 Author: Sai Thiha Zaw Date: 2025-10-12 Create 
#########################################################################################################


import os
from pathlib import Path
from datetime import datetime
from pyspark.sql import SparkSession, DataFrame, functions as F
from dotenv import load_dotenv

# =========================
# --- Config loading ---
# =========================
def load_config(env_path: Path | None = None) -> dict:
    if env_path:
        load_dotenv(env_path)
    else:
        default_env = Path(__file__).resolve().parents[2] / ".env"
        load_dotenv(default_env)

    cfg = {
        "SPARK_MASTER": os.getenv("SPARK_MASTER", "local[*]"),
        "EVENT_LOG_DIR": os.getenv("EVENT_LOG_DIR", "/tmp"),
        "S3_ENDPOINT": os.getenv("S3_ENDPOINT", "http://minio:9000"),
        "MINIO_USER": os.getenv("MINIO_USER"),
        "MINIO_PASSWORD": os.getenv("MINIO_PASSWORD"),
        # SAP client filter
        "SAP_CLIENT": os.getenv("SAP_CLIENT"),  # e.g. "100" or None
        # Bronze/Silver roots or explicit paths
        "BRONZE_ROOT": os.getenv("BRONZE_ROOT", "s3a://bronze/sap"),
        "SILVER_ROOT": os.getenv("SILVER_ROOT", "s3a://silver/sap"),
        # Optional explicit overrides (take precedence if present)
        "BRONZE_BUT000_URI": os.getenv("BRONZE_VBAK_URI","s3a://bronze/sap/but000/"), 
        "BRONZE_BUT020_URI": os.getenv("BRONZE_VBAK_URI","s3a://bronze/sap/but020/"), 
        "BRONZE_ADRC_URI": os.getenv("BRONZE_VBAK_URI","s3a://bronze/sap/adrc/"), 
        "BRONZE_ADR6_URI": os.getenv("BRONZE_VBAK_URI","s3a://bronze/sap/adr6/"), 
        "SILVER_MDM_CUST_URI": os.getenv("SILVER_SO_HDR_URI", "s3a://silver/sap/mdm_customers"), 
        # Metastore (optional, but nice)
        "HIVE_DB": os.getenv("HIVE_DB", "silver_sap"),
        "ENABLE_SSL": os.getenv("S3_SSL", "false").lower() in ("1", "true", "yes"),
    }
    # Resolve effective paths
    cfg["SRC_BUT000"] = cfg["BRONZE_BUT000_URI"] or f'{cfg["BRONZE_ROOT"].rstrip("/")}/but000/'
    cfg["SRC_BUT020"] = cfg["BRONZE_BUT020_URI"] or f'{cfg["BRONZE_ROOT"].rstrip("/")}/but020/'
    cfg["SRC_ADRC"] = cfg["BRONZE_ADRC_URI"] or f'{cfg["BRONZE_ROOT"].rstrip("/")}/adrc/'
    cfg["SRC_ADR6"] = cfg["BRONZE_ADR6_URI"] or f'{cfg["BRONZE_ROOT"].rstrip("/")}/adr6/'
    cfg["TGT_PATH"] = cfg["SILVER_MDM_CUST_URI"] or f'{cfg["SILVER_ROOT"].rstrip("/")}/mdm_customers/'
    cfg["TGT_TABLE"] = f'{cfg["HIVE_DB"]}.mdm_customers'
    return cfg


# =========================
# --- Spark session ---
# =========================
def build_spark(cfg: dict) -> SparkSession:
    builder = (
        SparkSession.builder
        .appName("SILVER_MDM_CUSTOMER")
        .master(cfg["SPARK_MASTER"])
        # Delta Lake
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        # S3A / MinIO
        .config("spark.hadoop.fs.s3a.endpoint", cfg["S3_ENDPOINT"])
        .config("spark.hadoop.fs.s3a.access.key", cfg["MINIO_USER"])
        .config("spark.hadoop.fs.s3a.secret.key", cfg["MINIO_PASSWORD"])
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", str(cfg["ENABLE_SSL"]).lower())
        .config("spark.hadoop.fs.s3a.fast.upload", "true")
        # QoL
        .config("spark.eventLog.enabled", "true")
        .config("spark.eventLog.dir", cfg["EVENT_LOG_DIR"])
        .config("spark.sql.sources.partitionOverwriteMode", "dynamic")
    )
    return builder.getOrCreate()


# =========================
# --- Create temp view  ---
# =========================
def _read_delta(spark: SparkSession, path: str) -> DataFrame:
    return spark.read.format("parquet").load(path)

def _apply_client(df: DataFrame, sap_client: str | None) -> DataFrame:
    if not sap_client or "mandt" not in [c.lower() for c in df.columns]:
        return df
    return df.withColumn("mandt", F.col("mandt").cast("string")).filter(F.col("mandt")==sap_client)

def create_temp_view(spark: SparkSession, cfg: dict):
    but000_df = _apply_client(_read_delta(spark, cfg["SRC_BUT000"]), cfg["SAP_CLIENT"])
    but020_df = _apply_client(_read_delta(spark, cfg["SRC_BUT020"]), cfg["SAP_CLIENT"])
    adrc_df   = _apply_client(_read_delta(spark, cfg["SRC_ADRC"]),   cfg["SAP_CLIENT"])
    adr6_df   = _apply_client(_read_delta(spark, cfg["SRC_ADR6"]),   cfg["SAP_CLIENT"])
   
    but000_df.createOrReplaceTempView("but000")
    but020_df.createOrReplaceTempView("but020")
    adrc_df.createOrReplaceTempView("adrc")
    adr6_df.createOrReplaceTempView("adr6")


# =========================
# --- Pure transform ---
# =========================
def transform(spark: SparkSession, cfg: dict) -> F.DataFrame:
   
    sql = """
        WITH address_rank AS (
        SELECT
            partner,
            address_number,
            ROW_NUMBER() OVER (
            PARTITION BY partner
            ORDER BY COALESCE(addr_valid_from, date_from) DESC, address_number
            ) AS rn
        FROM but020
        WHERE is_deleted = 0
        ),
        email_rank AS (
        SELECT
            a.address_number,
            e.smtp_addr,
            ROW_NUMBER() OVER (
            PARTITION BY a.address_number
            ORDER BY COALESCE(e.flgdefault, 0) DESC, e.consnumber
            ) AS rn
        FROM adrc a
        JOIN adr6 e
            ON e.address_number = a.address_number
        WHERE e.smtp_addr IS NOT NULL AND TRIM(e.smtp_addr) <> ''
        )
        SELECT
        b.partner   AS bp_id,
        b.name_org1 AS customer_name,
        a.street,
        a.city1     AS city,
        a.country   AS country,
        er.smtp_addr AS email
        FROM but000 b
        LEFT JOIN address_rank ar
        ON ar.partner = b.partner AND ar.rn = 1
        LEFT JOIN adrc a
        ON a.address_number = ar.address_number
        LEFT JOIN email_rank er
        ON er.address_number = a.address_number AND er.rn = 1
        -- optional: WHERE b.client = '100'
        ;
    """
    df = spark.sql(sql)

    (df.write
        .format("delta")
        .mode("overwrite")
        .partitionBy("country")
        .save(cfg["TGT_PATH"])
    )


def main():
    cfg = load_config()
    spark = build_spark(cfg)
    create_temp_view(spark, cfg)
    transform(spark, cfg)
    spark.stop()


if __name__ == "__main__":
    main()


