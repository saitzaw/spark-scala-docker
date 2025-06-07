import org.apache.spark.sql.SparkSession 
import org.apache.spark.SparkContext 
import java.util.Properties

object OldSingleViewCRM {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder()
      .appName("OldSingleViewCRM")
      .master("local[*]")
      .getOrCreate()

    val sc = spark.sparkContext

    // Assuming the configuration is set in the SparkContext
    val dbUser = sc.getConf.get("spark.db.user", "INFO")
    val dbPass = sc.getConf.get("spark.db.pass", "VTLINK")
    val dbStr = sc.getConf.get("spark.db.url", "URL")

    // JDBC URL and properties
    val jdbcUrl = dbStr
    val connectionProperties = new java.util.Properties()
    connectionProperties.setProperty("user", dbUser)
    connectionProperties.setProperty("password", dbPass)
    connectionProperties.setProperty("driver", "org.postgresql.Driver")

    // adding the SQL for single view 
    val crmSql =
      """
        |(
        |SELECT
        |    c.id AS customer_id,
        |    c.name AS customer_name,
        |    c.industry,
        |    c.region,
        |    c.phone AS customer_phone,
        |    c.website,
        |    c.tags,
        |    c.metadata::jsonb ->> 'customer_tier' AS customer_tier,
        |
        |    ct.full_name AS contact_name,
        |    ct.email AS contact_email,
        |    ct.phone AS contact_phone,
        |    ct.title AS contact_title,
        |
        |    l.full_name AS lead_name,
        |    l.email AS lead_email,
        |    l.phone AS lead_phone,
        |    l.status AS lead_status,
        |    l.source AS lead_source,
        |    l.metadata AS lead_metadata,
        |
        |    o.name AS opportunity_name,
        |    o.value AS opportunity_value,
        |    o.stage AS opportunity_stage,
        |    o.close_date,
        |    o.probability,
        |    o.notes AS opportunity_notes,
        |
        |    a.subject AS last_activity_subject,
        |    a.activity_type AS last_activity_type,
        |    a.notes AS last_activity_notes,
        |    a.context::jsonb ->> 'duration_minutes' AS activity_duration,
        |
        |    ord.id AS latest_order_id,
        |    ord.order_date,
        |    ord.total_amount,
        |
        |    t.amount AS last_transaction_amount,
        |    t.timestamp as transaction_date
        |
        |FROM customers c
        |LEFT JOIN contacts ct ON ct.customer_id = c.id
        |LEFT JOIN leads l ON l.assigned_to IS NOT NULL AND l.metadata::jsonb ->> 'region' = c.region
        |LEFT JOIN opportunities o ON o.customer_id = c.id
        |LEFT JOIN activities a ON a.contact_id = ct.id
        |LEFT JOIN orders ord ON ord.customer_id = c.id
        |LEFT JOIN (
        |    SELECT DISTINCT ON (order_id)
        |        id,
        |        order_id,
        |        amount,
        |        timestamp
        |    FROM transactions
        |    ORDER BY order_id, timestamp DESC
        |) AS t ON t.order_id = ord.id
        |) AS crm_view
        |""".stripMargin

    // Read data from PostgreSQL
    val df = spark.read
      .jdbc(jdbcUrl, crmSql, connectionProperties)

    df.show(10)
    
    spark.stop()
  }
}