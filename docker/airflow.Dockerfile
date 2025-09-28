FROM apache/airflow:2.9.2

USER root

# # Install Temurin OpenJDK 11
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends wget gnupg ca-certificates && \
#     wget -O - https://packages.adoptium.net/artifactory/api/gpg/key/public | gpg --dearmor -o /usr/share/keyrings/adoptium.gpg && \
#     echo "deb [signed-by=/usr/share/keyrings/adoptium.gpg] https://packages.adoptium.net/artifactory/deb bullseye main" > /etc/apt/sources.list.d/adoptium.list && \
#     apt-get update && \
#     apt-get install -y temurin-11-jre && \
#     apt-get clean && rm -rf /var/lib/apt/lists/*

# ENV JAVA_HOME=/usr/lib/jvm/temurin-11-jre-amd64
# ENV PATH=$JAVA_HOME/bin:$PATH

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        unzip \
        sudo \
        vim \
        build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y wget gnupg ca-certificates && \
    wget -qO - https://packages.adoptium.net/artifactory/api/gpg/key/public | apt-key add - && \
    echo "deb https://packages.adoptium.net/artifactory/deb bookworm main" > /etc/apt/sources.list.d/adoptium.list && \
    apt-get update && \
    apt-get install -y temurin-11-jdk curl unzip sudo vim build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
ENV JAVA_HOME=/usr/lib/jvm/temurin-11-jdk-amd64

# === Set environment variables ===
ENV SPARK_VERSION=3.5.5
ENV SPARK_HOME=/opt/spark
ENV PYSPARK_PYTHON=python3
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

# === Install Spark ===
RUN mkdir -p $SPARK_HOME && \
    curl -fSL https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz | \
    tar -xz --strip-components=1 -C $SPARK_HOME


USER airflow

# Install pyspark without constraints
RUN pip install --no-cache-dir pyspark==3.5.5 findspark


# === Install Python packages ===
RUN pip install --no-cache-dir \
    python-dotenv \
    apache-airflow-providers-apache-spark \
    apache-airflow-providers-apache-kafka \
    --constraint https://raw.githubusercontent.com/apache/airflow/constraints-2.9.2/constraints-3.12.txt


USER root
# === Install Delta Lake, Iceberg, Hudi JARs ===
RUN mkdir -p $SPARK_HOME/jars && \
    curl -Lo $SPARK_HOME/jars/iceberg-spark-runtime-3.4_2.12-1.4.3.jar https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-3.4_2.12/1.4.3/iceberg-spark-runtime-3.4_2.12-1.4.3.jar && \
    curl -Lo $SPARK_HOME/jars/delta-core_2.12-2.4.0.jar https://repo1.maven.org/maven2/io/delta/delta-core_2.12/2.4.0/delta-core_2.12-2.4.0.jar && \
    curl -Lo $SPARK_HOME/jars/delta-spark_2.12-3.2.0.jar https://repo1.maven.org/maven2/io/delta/delta-spark_2.12/3.2.0/delta-spark_2.12-3.2.0.jar && \
    curl -Lo $SPARK_HOME/jars/delta-storage-3.2.0.jar https://repo1.maven.org/maven2/io/delta/delta-storage/3.2.0/delta-storage-3.2.0.jar && \
    curl -Lo $SPARK_HOME/jars/hudi-spark3-bundle_2.12-0.15.0.jar https://repo1.maven.org/maven2/org/apache/hudi/hudi-spark3-bundle_2.12/0.15.0/hudi-spark3-bundle_2.12-0.15.0.jar
