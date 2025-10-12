#!/usr/bin/env python3

# fact_sale_orders.py : version 1.00 Date: 2025-10-05
#######################################################################
# Scheduler Warehouse using BashOperator
#######################################################################
#    Scheduler process from silver to gold zone in delta format.
#    version: 1.00 Author: Saithiha Zaw Date: 2025-10-05 Create
#######################################################################
#   Table list to ingest
# 1. VBAK - Sales Document: Header Data
# 2. VBAP - Sales Document: Item Data
# 3. VBEP - Sales Document: Schedule Line Data
#######################################################################

#!/usr/bin/env python3
import os
from pathlib import Path
from datetime import date

from pyspark.sql import SparkSession, functions as F
from dotenv import load_dotenv

# =========================
# --- Config loading ---
# =========================
def load_config(env_path: Path | None = None) -> dict:
    if env_path:
        load_dotenv(env_path)
    else:
        default_env = Path(__file__).resolve().parent.parent.parent / ".env"
        load_dotenv(default_env)

    cfg = {
        "SPARK_MASTER": os.getenv("SPARK_MASTER", "local[*]"),
        "EVENT_LOG_DIR": os.getenv("EVENT_LOG_DIR", "/tmp"),
        "S3_ENDPOINT": os.getenv("S3_ENDPOINT", "http://minio:9000"),
        "MINIO_USER": os.getenv("MINIO_USER"),
        "MINIO_PASSWORD": os.getenv("MINIO_PASSWORD"),

        # Client filter (optional)
        "SAP_CLIENT": os.getenv("SAP_CLIENT"),

        # Silver locations (SCD2) – defaults point to your MinIO buckets
        "SILVER_ROOT": os.getenv("SILVER_ROOT", "s3a://silver/sap"),
        "SILVER_SO_HDR_URI": os.getenv("SILVER_SO_HDR_URI", "s3a://silver/sap/sales_order_header_scd2/"),
        "SILVER_SO_ITM_URI": os.getenv("SILVER_SO_ITM_URI", "s3a://silver/sap/sales_order_item_scd2/"),
        "SILVER_VBEP_URI":   os.getenv("SILVER_VBEP_URI",   "s3a://silver/sap/sales_schedule_line_scd2/"),
        
        # replace GOLD_DB with GOLD_ROOT + per-table paths
        "GO LD_ROOT": os.getenv("GOLD_ROOT", "s3a://gold/sap"),
        "GO LD_SO_ITEM_FACT_URI": os.getenv("GOLD_SO_ITEM_FACT_URI"),
        "GO LD_SO_SCHED_FACT_URI": os.getenv("GOLD_SO_SCHED_FACT_URI"),
        "GO LD_SO_ITEM_PIT_URI": os.getenv("GOLD_SO_ITEM_PIT_URI"),
        # Metastores
        "HIVE_DB": os.getenv("HIVE_DB", "silver_sap"),   # where Silver tables may be registered
        "GOLD_DB": os.getenv("GOLD_DB", "gold_sap"),     # where we write Gold

        # Optional PIT as-of (YYYY-MM-DD)
        "ASOF_DATE": os.getenv("ASOF_DATE"),
        
        

        # SSL toggle
        "ENABLE_SSL": os.getenv("S3_SSL", "false").lower() in ("1", "true", "yes"),
    }

    # Resolved paths (keep as-is; we always prefer path reads for Silver)
    cfg["SRC_SILVER_HDR"] = cfg["SILVER_SO_HDR_URI"] or f'{cfg["SILVER_ROOT"].rstrip("/")}/sales_order_header_scd2/'
    cfg["SRC_SILVER_ITM"] = cfg["SILVER_SO_ITM_URI"] or f'{cfg["SILVER_ROOT"].rstrip("/")}/sales_order_item_scd2/'
    cfg["SRC_SILVER_VBEP"]= cfg["SILVER_VBEP_URI"]   or f'{cfg["SILVER_ROOT"].rstrip("/")}/sales_schedule_line_scd2/'

    # after cfg is built
    gold_root = cfg.get("GOLD_ROOT", "s3a://gold/sap").rstrip("/")

    cfg["TGT_ITEM_FACT_PATH"]  = cfg.get("GOLD_SO_ITEM_FACT_URI",  f"{gold_root}/sales_order_item_fact/")
    cfg["TGT_SCHED_FACT_PATH"] = cfg.get("GOLD_SO_SCHED_FACT_URI", f"{gold_root}/sales_schedule_line_fact/")
    cfg["TGT_ITEM_PIT_PATH"]   = cfg.get("GOLD_SO_ITEM_PIT_URI",   f"{gold_root}/sales_order_item_pit/")

    return cfg

# =========================
# --- Spark session ---
# =========================
def build_spark(cfg: dict) -> SparkSession:
    builder = (
        SparkSession.builder
        .appName("GOLD_SALES_BUILD")
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
def current(df):
    return df.where("is_current = true")

def pit(df, asof_str):
    # validity window: [start_ts, end_ts)
    return df.where(
        (F.col("start_ts") <= F.to_timestamp(F.lit(asof_str))) &
        (F.coalesce(F.col("end_ts"), F.to_timestamp(F.lit("9999-12-31"))) > F.to_timestamp(F.lit(asof_str)))
    )

def read_delta_path(spark: SparkSession, path: str):
    return spark.read.format("delta").load(path)

# =========================
# --- Main build ---
# =========================
def main():
    cfg = load_config()
    spark = build_spark(cfg)


    # ---- Load Silver (SCD2) from paths ----
    hdr = read_delta_path(spark, cfg["SRC_SILVER_HDR"])
    itm = read_delta_path(spark, cfg["SRC_SILVER_ITM"])
    sch = read_delta_path(spark, cfg["SRC_SILVER_VBEP"])

    # Client filter if provided
    if cfg.get("SAP_CLIENT"):
        for name, df in [("hdr", hdr), ("itm", itm), ("sch", sch)]:
            locals()[name] = df.where(F.col("client") == cfg["SAP_CLIENT"])
        hdr, itm, sch = locals()["hdr"], locals()["itm"], locals()["sch"]

    # ---------- VBEP rollups at item grain (CURRENT) ----------
    sch_cur = current(sch).select("client","sales_order","sales_item","sched_date","confirmed_qty_src")
    req_delivery = (sch_cur.where(F.col("sched_date").isNotNull())
                            .groupBy("client","sales_order","sales_item")
                            .agg(F.min("sched_date").alias("req_delivery_date")))
    first_conf = (sch_cur.where((F.col("sched_date").isNotNull()) & (F.col("confirmed_qty_src") > 0))
                          .groupBy("client","sales_order","sales_item")
                          .agg(F.min("sched_date").alias("first_confirmed_date")))
    last_conf = (sch_cur.where((F.col("sched_date").isNotNull()) & (F.col("confirmed_qty_src") > 0))
                         .groupBy("client","sales_order","sales_item")
                         .agg(F.max("sched_date").alias("last_confirmed_date")))
    totals = (sch_cur.groupBy("client","sales_order","sales_item")
                     .agg(F.sum(F.coalesce(F.col("confirmed_qty_src"), F.lit(0.0))).alias("confirmed_qty_src_total")))
    vbep_item = (req_delivery
                 .join(first_conf, ["client","sales_order","sales_item"], "left")
                 .join(last_conf,  ["client","sales_order","sales_item"], "left")
                 .join(totals,     ["client","sales_order","sales_item"], "left"))

    # ---------- GOLD 1: Item Fact (CURRENT) ----------
    hdr_cur = current(hdr).select(
        "client","sales_order","sales_org","dist_channel","division",
        "order_date","currency"
    )
    itm_cur = current(itm).select(
        "client","sales_order","sales_item",
        "material_id","plant","storage_loc",
        "order_qty","qty_uom","net_value_doccur","currency",
        "pricing_date","item_cat","rej_reason"
    )

    fact_item_cur = (itm_cur.alias("i")
        .join(hdr_cur.alias("h"), ["client","sales_order"], "left")
        .join(vbep_item.alias("e"), ["client","sales_order","sales_item"], "left")
        .withColumn("confirmed_qty_src_total", F.coalesce(F.col("confirmed_qty_src_total"), F.lit(0.0)))
        .withColumn("open_qty",
            F.when(F.col("order_qty").isNotNull(),
                   F.col("order_qty") - F.col("confirmed_qty_src_total")).otherwise(F.lit(None)))
        .select(
            F.col("i.client"),
            F.col("i.sales_order"),
            F.col("i.sales_item"),
            "material_id","plant","storage_loc",
            "order_qty","qty_uom",
            "net_value_doccur",
            F.col("i.currency").alias("item_currency"),
            "pricing_date","item_cat","rej_reason",
            "sales_org","dist_channel","division",
            "order_date",
            "req_delivery_date","first_confirmed_date","last_confirmed_date",
            "confirmed_qty_src_total","open_qty"
        )
    )

    (fact_item_cur.write.format("delta").mode("overwrite")
   .option("overwriteSchema","true")
   .save(cfg["TGT_ITEM_FACT_PATH"]))

    # ---------- GOLD 2: Schedule-line Fact (CURRENT) ----------
    fact_sched_cur = (current(sch)
        .select(
            "client","sales_order","sales_item","sched_line",
            "sched_date",
            "confirmed_qty_src","order_qty_sched",
            "delivery_block","req_type","schedule_type",
            "goods_issue_date","loading_date","transport_plan_date","resched_date","mfg_date"
        ))
    (fact_sched_cur.write.format("delta").mode("overwrite")
   .option("overwriteSchema","true")
   .save(cfg["TGT_SCHED_FACT_PATH"]))

    # ---------- GOLD 3: Item PIT (AS-OF) ----------
    asof = cfg["ASOF_DATE"] or str(date.today())
    hdr_pit = pit(hdr, asof).select(
        "client","sales_order","sales_org","dist_channel","division",
        "order_date","currency"
    )
    itm_pit = pit(itm, asof).select(
        "client","sales_order","sales_item",
        "material_id","plant","storage_loc",
        "order_qty","qty_uom","net_value_doccur","currency",
        "pricing_date","item_cat","rej_reason"
    )
    sch_pit = pit(sch, asof).select("client","sales_order","sales_item","sched_date","confirmed_qty_src")

    req_delivery_p = (sch_pit.where(F.col("sched_date").isNotNull())
        .groupBy("client","sales_order","sales_item")
        .agg(F.min("sched_date").alias("req_delivery_date")))
    first_conf_p = (sch_pit.where((F.col("sched_date").isNotNull()) & (F.col("confirmed_qty_src")>0))
        .groupBy("client","sales_order","sales_item")
        .agg(F.min("sched_date").alias("first_confirmed_date")))
    last_conf_p = (sch_pit.where((F.col("sched_date").isNotNull()) & (F.col("confirmed_qty_src")>0))
        .groupBy("client","sales_order","sales_item")
        .agg(F.max("sched_date").alias("last_confirmed_date")))
    totals_p = (sch_pit.groupBy("client","sales_order","sales_item")
        .agg(F.sum(F.coalesce(F.col("confirmed_qty_src"),F.lit(0.0))).alias("confirmed_qty_src_total")))
    vbep_item_p = (req_delivery_p
        .join(first_conf_p, ["client","sales_order","sales_item"], "left")
        .join(last_conf_p,  ["client","sales_order","sales_item"], "left")
        .join(totals_p,     ["client","sales_order","sales_item"], "left"))

    fact_item_pit = (itm_pit.alias("i")
        .join(hdr_pit.alias("h"), ["client","sales_order"], "left")
        .join(vbep_item_p.alias("e"), ["client","sales_order","sales_item"], "left")
        .withColumn("confirmed_qty_src_total", F.coalesce(F.col("confirmed_qty_src_total"), F.lit(0.0)))
        .withColumn("open_qty",
            F.when(F.col("order_qty").isNotNull(),
                   F.col("order_qty") - F.col("confirmed_qty_src_total")).otherwise(F.lit(None)))
        .withColumn("asof_date", F.lit(asof).cast("date"))
        .select(
            "asof_date",
            F.col("i.client"),
            F.col("i.sales_order"),
            F.col("i.sales_item"),
            "material_id","plant","storage_loc",
            "order_qty","qty_uom",
            "net_value_doccur",
            F.col("i.currency").alias("item_currency"),
            "pricing_date","item_cat","rej_reason",
            "sales_org","dist_channel","division",
            "order_date",
            "req_delivery_date","first_confirmed_date","last_confirmed_date",
            "confirmed_qty_src_total","open_qty"
        )
    )
    
    (fact_item_pit.write.format("delta").mode("overwrite")
   .option("overwriteSchema","true")
   .save(cfg["TGT_ITEM_PIT_PATH"]))


    spark.stop()

if __name__ == "__main__":
    main()
