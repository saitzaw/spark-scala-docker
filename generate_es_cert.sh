#!/bin/bash

set -e

echo "[INFO] Cleaning and preparing directories..."
rm -rf certs esdata http_ca.crt
mkdir -p certs esdata
chmod -R 777 certs esdata

echo "[INFO] Generating CA certificate..."
docker run --rm \
  -v "$(pwd)/certs:/certs" \
  docker.elastic.co/elasticsearch/elasticsearch:8.15.3 \
  bin/elasticsearch-certutil ca --silent --pem -out /certs/ca.zip

echo "[INFO] Unzipping CA certificate..."
docker run --rm \
  -v "$(pwd)/certs:/certs" \
  docker.elastic.co/elasticsearch/elasticsearch:8.15.3 \
  bash -c "cd /certs && unzip -o ca.zip"

echo "[INFO] Generating node certificate with empty password..."
docker run --rm \
  -v "$(pwd)/certs:/certs" \
  docker.elastic.co/elasticsearch/elasticsearch:8.15.3 \
  bin/elasticsearch-certutil cert --silent \
    --ca-cert /certs/ca/ca.crt \
    --ca-key /certs/ca/ca.key \
    --out /certs/certs.zip \
    --dns es01 \
    --ip 127.0.0.1 \
    --pass ""

echo "[INFO] Unzipping node certificate and renaming to http.p12..."
docker run --rm \
  -v "$(pwd)/certs:/certs" \
  docker.elastic.co/elasticsearch/elasticsearch:8.15.3 \
  bash -c "cd /certs && unzip -o certs.zip && cp certs/* http.p12"

echo "[INFO] Starting Elasticsearch and Kibana..."
docker compose up -d

echo "[INFO] Waiting for Elasticsearch to initialize..."
sleep 20

echo "[INFO] Extracting HTTP CA cert for curl usage..."
docker cp es01:/usr/share/elasticsearch/config/certs/http_ca.crt ./http_ca.crt

echo "[SUCCESS] TLS cert and HTTP CA are ready."

