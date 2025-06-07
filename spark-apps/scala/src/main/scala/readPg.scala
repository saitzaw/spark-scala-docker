import org.apache.spark.{SparkConf,SparkContext}
import org.apache.spark.sql.SparkSession


object PostgresReader {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder()
      .appName("ReadPostgreSQLwithScala")
      .master("local[*]")
      .getOrCreate()

    val conf = spark.sparkContext.getConf

    val dbUser = conf.get("spark.db.user", "INFO")
    val dbPass = conf.get("spark.db.pass", "VTLINK")
    val dbStr = conf.get("spark.db.url", "URL")
    val tableName = conf.get("spark.db.table", "TABLE")

    val jdbcUrl = dbStr
    val connectionProperties = new java.util.Properties()
    connectionProperties.setProperty("user", dbUser)
    connectionProperties.setProperty("password", dbPass)
    connectionProperties.setProperty("driver", "org.postgresql.Driver")

    val df = spark.read
      .jdbc(jdbcUrl, tableName, connectionProperties)

    df.show(10)
    spark.stop()
  }
}
