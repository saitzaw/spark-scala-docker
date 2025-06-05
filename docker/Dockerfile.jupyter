# === Base Image: Python 3.12.9 with JDK ===
FROM python:3.12.9-bullseye AS spark-jupyter-base

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        openjdk-11-jdk \
        curl \
        unzip \
        sudo \
        vim \
        build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# === Set environment variables ===
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV SPARK_VERSION=3.5.5
ENV SPARK_HOME=/opt/spark
ENV PYSPARK_PYTHON=python3
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

# === Install Spark ===
RUN mkdir -p $SPARK_HOME && \
    curl -fSL https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz | \
    tar -xz --strip-components=1 -C $SPARK_HOME

# === Install Python packages ===
RUN pip install --no-cache-dir \
    python-dotenv \
    notebook \
    jupyterlab \
    pyspark==3.5.5 \
    findspark

# === Install Delta Lake, Iceberg, Hudi JARs ===
RUN mkdir -p $SPARK_HOME/jars && \
    curl -Lo $SPARK_HOME/jars/iceberg-spark-runtime-3.4_2.12-1.4.3.jar https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-3.4_2.12/1.4.3/iceberg-spark-runtime-3.4_2.12-1.4.3.jar && \
    curl -Lo $SPARK_HOME/jars/delta-core_2.12-2.4.0.jar https://repo1.maven.org/maven2/io/delta/delta-core_2.12/2.4.0/delta-core_2.12-2.4.0.jar && \
    curl -Lo $SPARK_HOME/jars/delta-spark_2.12-3.2.0.jar https://repo1.maven.org/maven2/io/delta/delta-spark_2.12/3.2.0/delta-spark_2.12-3.2.0.jar && \
    curl -Lo $SPARK_HOME/jars/delta-storage-3.2.0.jar https://repo1.maven.org/maven2/io/delta/delta-storage/3.2.0/delta-storage-3.2.0.jar && \
    curl -Lo $SPARK_HOME/jars/hudi-spark3-bundle_2.12-0.15.0.jar https://repo1.maven.org/maven2/org/apache/hudi/hudi-spark3-bundle_2.12/0.15.0/hudi-spark3-bundle_2.12-0.15.0.jar

# === Working directory for notebooks ===
WORKDIR /opt/workspace
RUN mkdir -p /opt/workspace

# === Expose Jupyter port ===
EXPOSE 8888

# === Start Jupyter ===
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]