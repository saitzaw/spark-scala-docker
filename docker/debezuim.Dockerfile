FROM debezium/connect:2.5

# Download Confluent Avro converters
ADD https://packages.confluent.io/maven/io/confluent/kafka-connect-avro-converter/7.6.1/kafka-connect-avro-converter-7.6.1.jar /kafka/libs/
ADD https://packages.confluent.io/maven/io/confluent/common-config/7.6.1/common-config-7.6.1.jar /kafka/libs/
ADD https://packages.confluent.io/maven/io/confluent/common-utils/7.6.1/common-utils-7.6.1.jar /kafka/libs/
