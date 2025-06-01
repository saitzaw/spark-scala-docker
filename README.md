# data engineering in Scala 
    Data engineering needs complex infrastrucre setup and install huge dependencies. However, thanks to containerization, we can build the DEV, QUA and PRD environment.  

# Build the project 
    - make build 

# Run the docker compose 
    - make up 
    Note: wait 2 to 3 mins to settle 
# Stop the docker compose 
    - make down 

# Enter the spark server 
    - make dev

# Build the jar file 
```
cd /opt/spark/jobs/scala
sbt package 
```

# output jar location 
```
/opt/spark/jobs/scala/target/scala-2.12
```

# spark submit 
    This process needs to do in the master node 
```
spark-submit \
  --class readTxtLog \
  --master spark://spark-master:7077 \
  --conf spark.input.path=/opt/spark/data/logs.txt \
  --conf spark.log.type=INFO \
  --conf spark.interface.name=VTLINK \
  /opt/spark/jobs/scala/target/scala-2.12/sparkrdd_2.12-0.1.jar
```

# Next plan 
- Full ETL pipeline in Scala 
- integration with Apache Airflow 
- CI/CD 
- Data profiler 
- integration with Aapche Kafka 

