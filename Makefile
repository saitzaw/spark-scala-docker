build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down --rmi all

dev:
	docker exec -it spark-master bash