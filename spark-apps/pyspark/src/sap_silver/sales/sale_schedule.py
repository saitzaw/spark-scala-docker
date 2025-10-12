#!/usr/bin/env python3

#  sale_schedule.py : version 1.00 Date 2025-10-05
#########################################################################################################
#    Sale schedule data in SCD type 2
#########################################################################################################
#    ETL process for SAP VBEP data from bronze to silver zone in delta format with SCD type 2.
#    version: 1.00 Author: Sai Thiha Zaw Date: 2025-10-05 Create 
#########################################################################################################

import os
from pathlib import Path
from datetime import datetime

from pyspark.sql import SparkSession, functions as F, Window
from delta.tables import DeltaTable
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
        "MINIO_USER": os.getenv("MINIO_USER", os.getenv("MINIO_ACCESS_KEY", "admin")),
        "MINIO_PASSWORD": os.getenv("MINIO_PASSWORD", os.getenv("MINIO_SECRET_KEY", "admin123")),
        "ENABLE_SSL": os.getenv("S3_SSL", "false").lower() in ("1","true","yes"),

        "SAP_CLIENT": os.getenv("SAP_CLIENT"),

        "BRONZE_ROOT": os.getenv("BRONZE_ROOT", "s3a://bronze/sap"),
        "SILVER_ROOT": os.getenv("SILVER_ROOT", "s3a://silver/sap"),
        "BRONZE_VBEP_URI": os.getenv("BRONZE_VBEP_URI"),  # optional override
        "SILVER_VBEP_URI": os.getenv("SILVER_VBEP_URI"),  # optional override

        "HIVE_DB": os.getenv("HIVE_DB", "silver_sap"),
    }
    cfg["SRC_VBEP"] = cfg["BRONZE_VBEP_URI"] or f'{cfg["BRONZE_ROOT"].rstrip("/")}/vbep/'
    cfg["TGT_PATH"] = cfg["SILVER_VBEP_URI"] or f'{cfg["SILVER_ROOT"].rstrip("/")}/sales_schedule_line_scd2/'
    cfg["TGT_TABLE"] = f'{cfg["HIVE_DB"]}.sales_schedule_line_scd2'
    return cfg

# =========================
# --- Spark session ---
# =========================
def build_spark(cfg: dict) -> SparkSession:
    builder = (
        SparkSession.builder
        .appName("SILVER_SALES_SCHEDULE_LINE_SCD2")
        .master(cfg["SPARK_MASTER"])
        # Delta
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        # MinIO / S3A
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
# --- Helpers ---
# =========================
BK = ["client","sales_order","sales_item","sched_line"]

TRACKED_ATTRS = [
    "sched_date",           # EDATU
    "confirmed_qty_src",    # BMENG
    "order_qty_sched"       # WMENG (schedule-line qty)
]

def has_col(df, name: str) -> bool:
    return name in df.columns

def null_if_blank(col):
    return F.when(F.trim(F.col(col))=="", F.lit(None)).otherwise(F.col(col))

def parse_sap_date(col):
    c = F.col(col).cast("string")
    return (
        F.when(c.isin("00000000","0000-00-00",""," "), F.lit(None))
         .when((F.length(c)==8) & (~c.contains("-")), F.to_date(c,"yyyyMMdd"))
         .when(c.contains("-"), F.to_date(c,"yyyy-MM-dd"))
         .when(c.contains("."), F.to_date(c,"dd.MM.yyyy"))
         .when(c.contains("/"), F.to_date(c,"dd/MM/yyyy"))
         .otherwise(F.lit(None))
    )

def parse_sap_time(col):
    """
    Parses SAP-style time fields (EZEIT, etc.) into HH:MM:SS format.
    Handles common SAP representations:
      - "083015"  -> 08:30:15
      - "83015"   -> 08:30:15
      - "08:30:15" -> stays as is
      - "000000", "", or null -> None
    """
    t = F.col(col).cast("string")

    return (
        F.when(t.isNull() | (F.trim(t) == "") | (t == "000000"), F.lit(None))
         .when(F.length(t) == 6, 
               F.concat_ws(":", 
                   F.substring(t, 1, 2), 
                   F.substring(t, 3, 2), 
                   F.substring(t, 5, 2)))
         .when(F.length(t) == 5, 
               F.concat_ws(":", 
                   F.lpad(F.substring(t, 1, 1), 2, "0"), 
                   F.substring(t, 2, 2), 
                   F.substring(t, 4, 2)))
         .otherwise(t)
    )

def add_if_missing(df, col_name, default_expr):
    return df if col_name in df.columns else df.withColumn(col_name, default_expr)

def attr_hash(df):
    return df.withColumn("_attr_hash",
        F.md5(F.concat_ws("||", *[F.col(c).cast("string") for c in TRACKED_ATTRS]))
    )

def delta_exists(spark: SparkSession, path: str) -> bool:
    try:
        DeltaTable.forPath(spark, path)
        return True
    except Exception:
        return False

# =========================
# --- Build snapshot (clean + dedup) ---
# =========================
def build_snapshot(spark: SparkSession, cfg: dict):
    vbep = spark.read.load(cfg["SRC_VBEP"])

    e = (
        vbep
        .withColumn("client", F.col("mandt"))
        .withColumn("sales_order", F.col("vbeln"))
        .withColumn("sales_item", F.col("posnr"))
        # schedule-line key: prefer ETENR; fall back to ETENE
        .withColumn("sched_line", F.coalesce(F.col("etenr").cast("string"), F.col("etene").cast("string")))
        # dates
        .withColumn("sched_date", parse_sap_date("edatu"))
        .withColumn("sched_time_txt", parse_sap_time("ezeit"))
        .withColumn("req_date", parse_sap_date("bddat"))      # requirement date (if used)
        .withColumn("resched_date", parse_sap_date("rsdat"))  # rescheduling date
        .withColumn("goods_issue_date", parse_sap_date("wadat"))
        .withColumn("loading_date", parse_sap_date("lddat"))
        .withColumn("transport_plan_date", parse_sap_date("tddat"))
        .withColumn("mfg_date", parse_sap_date("mbdat"))
        # quantities & UoM
        .withColumn("order_qty_sched", F.col("wmeng").cast("double"))   # schedule-qty
        .withColumn("confirmed_qty_src", F.col("bmeng").cast("double")) # confirmed
        .withColumn("uom_sales", F.col("vrkme"))
        .withColumn("uom_base",  F.col("meins"))
        .withColumn("uom_whse",  F.col("lmeng"))  # (if useful)
        .withColumn("umvkz", F.col("umvkz").cast("double"))  # numerator
        .withColumn("umvkn", F.col("umvkn").cast("double"))  # denominator
        # flags/indicators
        .withColumn("delivery_relevant", F.col("lfrel"))  # 'X' if relevant
        .withColumn("delivery_block", F.col("lifsp"))     # code if blocked
        .withColumn("req_type", F.col("etart"))           # requirement type
        .withColumn("schedule_type", F.col("ettyp"))      # schedule type
        # tech columns (safe defaults)
        .withColumn("_ingest_ts", F.coalesce(F.col("_ingest_ts"), F.current_timestamp()))
        .withColumn("_change_ts", F.col("_change_ts").cast("timestamp"))
    )

    if cfg["SAP_CLIENT"]:
        e = e.where(F.col("client")==cfg["SAP_CLIENT"])

    # Keep only rows with valid BK
    e = e.where(F.col("sales_order").isNotNull() & F.col("sales_item").isNotNull() & F.col("sched_line").isNotNull())

    # Dedup latest per BK: prefer change_ts > ingest_ts > sched_date > now
    order_ts = F.coalesce(F.col("_change_ts"), F.col("_ingest_ts"), F.col("sched_date").cast("timestamp"), F.current_timestamp())
    w = Window.partitionBy(*BK).orderBy(order_ts.desc_nulls_last())
    snap = (e.withColumn("_rn", F.row_number().over(w)).where(F.col("_rn")==1).drop("_rn"))

    # Attribute hash for SCD2 detection
    snap = attr_hash(snap.select(*(BK + TRACKED_ATTRS + ["_ingest_ts","_change_ts"])))
    return snap

# =========================
# --- SCD TYPE 2 ---
# =========================
def initial_load(spark: SparkSession, cfg: dict, snap):
    load_ts = F.lit(datetime.utcnow())
    out = (snap
           .withColumn("start_ts", load_ts)
           .withColumn("end_ts", F.lit(None).cast("timestamp"))
           .withColumn("is_current", F.lit(True))
           .withColumn("version", F.lit(1))
           .withColumn("sk_sched_line",
                       F.md5(F.concat_ws("||", *[F.col(k).cast("string") for k in BK])))
          )
    (out.write
        .format("delta")
        .mode("overwrite")
        .partitionBy("sched_date")
        .save(cfg["TGT_PATH"])
    )
    spark.sql(f"CREATE DATABASE IF NOT EXISTS {cfg['HIVE_DB']}")
    spark.sql(f"CREATE TABLE IF NOT EXISTS {cfg['TGT_TABLE']} USING DELTA LOCATION '{cfg['TGT_PATH']}'")

def incremental_load(spark: SparkSession, cfg: dict, snap):
    tgt = DeltaTable.forPath(spark, cfg["TGT_PATH"])
    load_time = datetime.utcnow()

    # 1) Expire changed active rows
    tgt_active = tgt.toDF().where("is_current = true").select(*(BK + ["_attr_hash"]))
    to_expire = (
        tgt_active.alias("t")
        .join(snap.select(*(BK + ["_attr_hash"])).alias("s"), on=BK, how="inner")
        .where(F.col("t._attr_hash") != F.col("s._attr_hash"))
        .select(*BK)
    )
    (tgt.alias("t")
        .merge(to_expire.alias("e"),
               " AND ".join([f"t.{k} = e.{k}" for k in BK]) + " AND t.is_current = true")
        .whenMatchedUpdate(set={"end_ts": F.lit(load_time), "is_current": F.lit(False)})
        .execute()
    )

    # 2) Insert new versions (new BKs + changed BKs)
    new_keys = snap.alias("s").join(
        tgt.toDF().where("is_current = true").select(*BK).alias("t"),
        on=BK, how="left_anti"
    ).select("s.*")
    changed_keys = snap.alias("s").join(to_expire.alias("e"), on=BK, how="inner").select("s.*")
    to_insert = new_keys.unionByName(changed_keys).dropDuplicates(BK)
    if to_insert.rdd.isEmpty():
        return

    prev_versions = tgt.toDF().groupBy(*BK).agg(F.max("version").alias("prev_ver"))
    staged = (
        to_insert.alias("s")
        .join(prev_versions.alias("v"), on=BK, how="left")
        .withColumn("version", F.coalesce(F.col("v.prev_ver") + F.lit(1), F.lit(1)))
        .withColumn("start_ts", F.lit(load_time))
        .withColumn("end_ts", F.lit(None).cast("timestamp"))
        .withColumn("is_current", F.lit(True))
        .withColumn("sk_sched_line",
                    F.md5(F.concat_ws("||", *[F.col(k).cast("string") for k in BK])))
        .select(
            *BK,
            *TRACKED_ATTRS,
            "_attr_hash","_ingest_ts","_change_ts",
            "start_ts","end_ts","is_current","version","sk_sched_line"
        )
    )
    (staged.write
        .format("delta")
        .mode("append")
        .partitionBy("sched_date")
        .save(cfg["TGT_PATH"])
    )

# =========================
# --- Main ---
# =========================
def main():
    cfg = load_config()
    spark = build_spark(cfg)
    snap = build_snapshot(spark, cfg)

    if not delta_exists(spark, cfg["TGT_PATH"]):
        initial_load(spark, cfg, snap)
    else:
        incremental_load(spark, cfg, snap)

    spark.stop()

if __name__ == "__main__":
    main()
