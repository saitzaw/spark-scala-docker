import org.scalatest.funsuite.AnyFunSuite
import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.rdd.RDD
import scalaRDD._

class ScalaRDDTest extends AnyFunSuite {

  var sc: SparkContext = _

  def createContext(): SparkContext = {
    val conf = new SparkConf().setAppName("rddReadTxtTest").setMaster("local[*]")
    new SparkContext(conf)
  }

  test("logTypeRdd should filter lines with specified log type and ignore numeric lines") {
    sc = createContext()
    val data = Seq("12345", "INFO something happened", "DEBUG this is debug", "INFO another event")
    val rdd: RDD[String] = sc.parallelize(data)

    val result = logTypeRdd(rdd, "INFO").collect()
    assert(result.length == 2)
    assert(result.contains("INFO something happened"))
    assert(result.contains("INFO another event"))

    sc.stop()
  }

  test("makeIpRdd should extract IP addresses for matching logType and interface") {
    sc = createContext()
    val data = Seq(
      "INFO connection on VTLINK from 192.168.1.1",
      "INFO connection on OTHER from 10.0.0.1",
      "DEBUG ignore this",
      "INFO VTLINK 8.8.8.8"
    )
    val rdd: RDD[String] = sc.parallelize(data)

    val ipRddFunc = makeIpRdd()
    val result = ipRddFunc(rdd, "INFO", "VTLINK", logTypeRdd).collect().flatten

    assert(result.contains("192.168.1.1"))
    assert(result.contains("8.8.8.8"))
    assert(!result.contains("10.0.0.1"))

    sc.stop()
  }
}
