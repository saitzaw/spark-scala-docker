FROM python:3.10.13-slim

RUN apt-get update && apt-get install -y build-essential git curl

# Change dbt-spark to dbt-postgres if you're using PostgreSQL
RUN pip install --upgrade pip && \
    pip install dbt-spark pandas dbt-postgres

ENV DBT_PROFILES_DIR=/usr/app/profiles
WORKDIR /usr/app
