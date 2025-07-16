build:
	docker compose build

dev-spark-up:
	 docker compose up spark-master spark-worker jupyter minio

dev-streaming-up:
	 docker compose up spark-master spark-worker kafka zookeeper minio

dev-airflow-up:
	 docker compose up airflow-webserver airflow-scheduler redis postgres spark-master spark-worker minio

dev-kafka-up:
	 docker compose up kafka zookeeper debezium postgres 

dev-dbt-up:
	 docker compose up dbt postgres	

up:
	docker compose up -d

down:
	docker compose down 

clean:
	docker compose down -rmi all

rebuild:
	docker compose down --rmi all -v
	docker compose up --build -d

dev:
	docker exec -it spark-master bash

da:
	docker exec -it spark-jupyter bash 

pg:
	docker exec -it postgres bash

airflow-init-db:
	docker exec -it airflow-webserver airflow db init

airflow-migrate:
	docker exec -it airflow-webserver airflow db migrate

airflow-create-user:
	docker exec -it airflow-webserver airflow users create \
		--username admin \
		--firstname Admin \
		--lastname User \
		--role Admin \
		--email admin@jjhome@gmail.com
		--password admin1234

web:
	docker exec -it airflow-webserver bash

scheduler:
	docker exec -it airflow-scheduler bash

redis:
	docker exec -it redis bash

airflow-dags-list:
	docker exec -it airflow-webserver airflow dags list

kafka-logs:
	docker logs kafka

spark-logs:
	docker logs spark-master

spark-worker-logs:
	docker logs spark-worker

airflow-logs:
	docker logs airflow-webserver

postgres-logs:
	docker logs postgres

kafka-data-clean: 
	rm -rf kafka-data/*

dbt-shell:
	docker exec -it dbt bash

dbt-debug:
	docker exec -it dbt dbt debug