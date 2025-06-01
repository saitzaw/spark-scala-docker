import re
import time
from pyspark.sql import SparkSession

# -----------------------
# Spark Session Setup
# -----------------------
# Create a Spark session
spark = SparkSession.builder.appName("FunPySpark").master("local[*]").getOrCreate()

# Get the Spark context from the session
sc = spark.sparkContext


# -----------------------
# Argument Parsing
# -----------------------
conf = sc.getConf()
input_path = conf.get("spark.input.path", "/opt/spark/data/log.txt")
log_type = conf.get("spark.log.type", "INFO")
interface_name = conf.get("spark.interface.name", "VTLINK")

# read a text file
# and print the first 10 lines
rdd = sc.textFile(input_path)


# -----------------------
# Decorators
# -----------------------
# log_time decorator to measure execution time of functions
# This decorator can be used to wrap any function to log its execution time
def log_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time() - start:.2f} sec")
        return result
    return wrapper

# cleaned_rdd decorator to remove header lines from RDDs
# This decorator filters out lines that are headers (e.g., lines that contain only digits)
def cleaned_rdd(func):
  def wrapper(rdd, *args, **kwargs):
    remove_header_rdd = rdd.filter(lambda line: not line.strip().isdigit())
    return func(remove_header_rdd, *args, **kwargs)
  return wrapper


# -----------------------
# RDD Transformations
# -----------------------
# log_type_rdd function to filter RDDs based on log type
@log_time
@cleaned_rdd
def log_type_rdd(rdd, log_type):
    return rdd.filter(lambda line: log_type in line)

# make_ip_rdd function to extract IP addresses from RDDs
def make_ip_rdd():
  ip_pattern = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")

  @log_time
  def ip_rdd(rdd, log_type, interface_name, func):

      return (
          func(rdd, log_type)
          .filter(lambda line: interface_name in line)
          .map(lambda line: ip_pattern.findall(line))
          .filter(lambda ips: len(ips) > 0)
      )
  return ip_rdd


# -----------------------
# Main Logic
# -----------------------
ip_rdd_func = make_ip_rdd()
ip_result = ip_rdd_func(rdd, log_type, interface_name, log_type_rdd)

for ip_list in ip_result.collect():
    print(ip_list)

spark.stop()