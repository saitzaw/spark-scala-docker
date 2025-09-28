# info 
PySpark releted job here 

## submit command 

### to read logs.txt 
```sh 
spark-submit \
  --master spark://spark-master:7077 \
  --conf spark.input.path=/opt/spark/data/logs.txt \
  --conf spark.log.type=INFO \
  --conf spark.interface.name=VTLINK \
  /opt/spark/jobs/pyspark/src/read_txt_log.py
```

### Ingestion data to  MINIO delta lake
### ADR6 
```sh 
spark-submit \
  --master spark://spark-master:7077 \
  --packages org.apache.hadoop:hadoop-aws:3.3.2,com.amazonaws:aws-java-sdk-bundle:1.12.262 \
  --conf spark.log.type=INFO \
  --conf spark.interface.name=VTLINK \
  --conf spark.eventLog.enabled=true \
  --conf spark.eventLog.dir=/tmp \
  /opt/spark/jobs/pyspark/src/sap_bronze/adr6.py
``` 

### ADRC 
```sh 
spark-submit \
  --master spark://spark-master:7077 \
  --packages org.apache.hadoop:hadoop-aws:3.3.2,com.amazonaws:aws-java-sdk-bundle:1.12.262 \
  --conf spark.log.type=INFO \
  --conf spark.interface.name=VTLINK \
  --conf spark.eventLog.enabled=true \
  --conf spark.eventLog.dir=/tmp \
  /opt/spark/jobs/pyspark/src/sap_bronze/adrc.py
```