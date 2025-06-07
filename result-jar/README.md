# this folder collect the jar file in my testing 
- use this class name 

## Table for Jar

| # | class name | jar file |
|:-:|:----------:|:--------:|
|1| readTxtLog | sparkrdd_2.12-0.1.jar | 
|2| PostgresReader | pg-spark_2.12-0.1.jar | 
|3| OldSingleViewCRM | oldsingleviewcrm_2.12-0.1.jar | 

# To submit the using spark 
-  Remark change your user, postgres DB and  password 

### posgres readrer 

```postgres reader 
spark-submit \
  --class PostgesReader \
  --master local[*] \
  --jars /opt/spark/jobs/scala/lib/postgresql-42.7.1.jar \
  --conf spark.db.user=user \
  --conf spark.db.pass=password \
  --conf spark.db.url=jdbc:postgresql://postgres:5432/sparkdb \
  --conf spark.db.table=table \
  /opt/spark/jobs/scala/target/scala-2.12/pg-spark_2.12-0.1.jar
```

### CRM single view 
```
spark-submit \
  --class OldSingleViewCRM \
  --master local[*] \
  --jars /opt/spark/jobs/scala/lib/postgresql-42.7.1.jar \
  --conf spark.db.user=user \
  --conf spark.db.pass=password \
  --conf spark.db.url=jdbc:postgresql://postgres:5432/sparkdb \
  /opt/spark/jobs/scala/target/scala-2.12/oldsingleviewcrm_2.12-0.1.jar
```