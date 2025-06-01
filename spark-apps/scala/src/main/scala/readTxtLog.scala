import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.rdd.RDD
import scala.util.matching.Regex
import java.time.Instant

object readTxtLog {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf().setAppName("").setMaster("local[*]")

    // RDD input path and log type can be set via command line arguments or default values
    val inputPath = conf.get("spark.input.path", "src/main/resources/logs.txt")
    val sc = new SparkContext(conf)
    // Read the input file into an RDD
    // You can change the path to your log file
    val rdd = sc.textFile(inputPath)

    // Remove headers (digits only) from the RDD
    val logType = conf.get("spark.log.type", "INFO")
    val interfaceName = conf.get("spark.interface.name", "VTLINK")

    // Function to filter and clean the RDD
    val ipRddFunc = makeIpRdd()
    val ipRdd = ipRddFunc(rdd, logType, interfaceName, logTypeRdd)

    // Collect and print the results
    ipRdd.collect().foreach(arr => println(arr.mkString(", ")))

    sc.stop()
    Thread.sleep(10000)
  }

// Logging decorator equivalent
  def logTime[T](func: => T, name: String): T = {
    val start = Instant.now().toEpochMilli
    val result = func
    val end = Instant.now().toEpochMilli
    println(s"$name took ${(end - start) / 1000.0} sec")
    result
  }

  // Higher-order function for removing headers (digits only)
  def cleanedRdd(rdd: RDD[String]): RDD[String] = {
    rdd.filter(line => !line.trim.matches("^\\d+$"))
  }

  // Equivalent to logTypeRdd function
  // Filters the RDD for lines containing a specific log type
  def logTypeRdd(rdd: RDD[String], logType: String): RDD[String] = {
    logTime({
      cleanedRdd(rdd).filter(line => line.contains(logType))
    }, "logTypeRdd")
  }

  // Factory function returning ip_rdd function
  def makeIpRdd(): (
    RDD[String], 
    String,
    String,
    (RDD[String],String) => RDD[String]) => RDD[Array[String]] = {
    val ipPattern: Regex = """\b(?:\d{1,3}\.){3}\d{1,3}\b""".r

    def ipRdd(
      rdd: RDD[String],
      logType: String,
      interfaceName: String,
      func: (RDD[String], String) => RDD[String]): RDD[Array[String]] = {
      logTime({
        func(rdd, logType)
          .filter(line => line.contains(interfaceName))
          .map(line => ipPattern.findAllIn(line).toArray)
          .filter(_.nonEmpty)
      }, "ipRdd")
    }
    ipRdd
  }
}