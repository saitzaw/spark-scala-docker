name := "SparkRDD"

version := "0.1"

scalaVersion := "2.12.18"

// libraryDependencies += "org.apache.spark" %% "spark-core" % "3.5.0"

libraryDependencies ++= Seq(
 "org.apache.spark" %% "spark-core" % "3.5.0" % Provided,
  "org.apache.spark" %% "spark-sql"  % "3.5.0" % Provided,
  "org.scalatest"    %% "scalatest"  % "3.2.17" % Test //
)
