# data engineering in Scala 
    Data engineering needs complex infrastrucre setup and install huge dependencies. However, thanks to containerization, we can build the DEV, QUA and PRD environment.  

# Build the project 
    - make build 

# Run the docker compose 
    - make up 
    Note: wait 2 to 3 mins to settle 


# Check the spark master UI 
![Spark Architecture](asserts/spark-master.png)

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
    This process needs to do in the master node and run this command 
```
/opt/spark/bin
```
Then run the spark-submit to get the result
```
spark-submit \
  --class readTxtLog \
  --master spark://spark-master:7077 \
  --conf spark.input.path=/opt/spark/data/logs.txt \
  --conf spark.log.type=INFO \
  --conf spark.interface.name=VTLINK \
  /opt/spark/jobs/scala/target/scala-2.12/sparkrdd_2.12-0.1.jar
```
### Pyspark submit

```
PYSPARK_DRIVER_PYTHON=python3 spark-submit \
  --master spark://spark-master:7077 \
  --conf spark.input.path=/opt/spark/data/logs.txt \
  --conf spark.log.type=INFO \
  --conf spark.interface.name=VTLINK \
  /opt/spark/jobs/pyspark/src/read_txt_log.py
```



# check the process in UI
![Spark Architecture](asserts/spark-application.png)

# Load data to postgresl 
## Enter the postgresql docker image 
```
make pg 
```
## psql command to enter the postresql 
```
psql -U sparkuser -d sparkdb
```

### Sample to add simple sql 
```
\i /path/to/07_dml_seed_crm_orders.sql
```
### create and insert all seed values in pg using 
Remark: init.sh is in the sql_scripts folder
```
./init.sh 
```

# Check the defautl route to interactive with DBeaver 
```
ip route | grep default 
```
The Sample output is -> default via 172.23.224.1 dev eth0 proto kernel 

# PG connection and check for single view
- Add the requried data to connection and use the default IP addess get from the ip route, in this case the jdbc connecting is using 172.23.224.1 this ip address

![Single View](asserts/postsqlDBeaver.png)


# Business values 
- OLD CRM system is monolithic and need to modernize 
- Migration to more compact and useful data strcture 
- 

# Next plan 
- Full ETL pipeline in Scala 
- integration with Apache Airflow 
- CI/CD 
- Data profiler 
- integration with Aapche Kafka
