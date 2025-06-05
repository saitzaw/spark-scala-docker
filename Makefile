build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down --rmi all

dev:
	docker exec -it spark-master bash

da:
	docker exec -it spark-jupyter bash 

pg:
	docker exec -it postgres bash