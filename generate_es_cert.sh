#!/bin/bash

set -e

VOLUME_PATH=$(docker volume inspect elasticsearch-setup_certs -f '{{ .Mountpoint }}')

echo "[INFO] Creating Elasticsearch certificate..."

docker run --rm \
  --name elastic-certgen \
  -v certs:/certs \
  docker.elastic.co/elasticsearch/elasticsearch:8.15.3 \
  bin/elasticsearch-certutil ca --silent --pem -out /certs/ca.zip

docker run --rm \
  --name elastic-certgen \
  -v certs:/certs \
  docker.elastic.co/elasticsearch/elasticsearch:8.15.3 \
  bash -c "cd /certs && unzip -o ca.zip"

docker run --rm \
  --name elastic-certgen \
  -v certs:/certs \
  docker.elastic.co/elasticsearch/elasticsearch:8.15.3 \
  bin/elasticsearch-certutil cert --silent \
    --ca-cert /certs/ca/ca.crt \
    --ca-key /certs/ca/ca.key \
    --out /certs/certs.zip \
    --dns es01 \
    --ip 127.0.0.1

docker run --rm \
  -v certs:/certs \
  docker.elastic.co/elasticsearch/elasticsearch:8.15.3 \
  bash -c "cd /certs && unzip -o certs.zip && cp certs/* http.p12"

echo "[INFO] Copying http_ca.crt for CURL..."
docker compose -f docker-compose.elasticsearch.yml up -d
sleep 20
docker cp es01:/usr/share/elasticsearch/config/certs/http_ca.crt ./http_ca.crt

echo "[SUCCESS] TLS cert and HTTP CA are ready."
