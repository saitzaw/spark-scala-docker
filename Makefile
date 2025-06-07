build:
	docker compose build

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