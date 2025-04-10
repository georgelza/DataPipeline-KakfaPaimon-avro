#!/bin/bash

export curhome=$(pwd)
echo $curhome

echo "--> Install JARs: Flink's Kafka connector" 
mkdir -p $curhome/data/flink/lib/kafka 
cd $curhome/data/flink/lib/kafka

wget https://repo1.maven.org/maven2/com/fasterxml/jackson/core/jackson-annotations/2.17.0/jackson-annotations-2.17.0.jar
wget https://repo1.maven.org/maven2/com/fasterxml/jackson/core/jackson-core/2.17.0/jackson-core-2.17.0.jar
wget https://repo1.maven.org/maven2/com/fasterxml/jackson/core/jackson-databind/2.17.0/jackson-databind-2.17.0.jar
wget https://packages.confluent.io/maven/io/confluent/kafka-avro-serializer/7.7.1/kafka-avro-serializer-7.7.1.jar
wget https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.7.1/kafka-clients-3.7.1.jar
wget https://packages.confluent.io/maven/io/confluent/kafka-schema-registry-client/7.7.1/kafka-schema-registry-client-7.7.1.jar
wget https://packages.confluent.io/maven/io/confluent/kafka-schema-serializer/7.7.1/kafka-schema-serializer-7.7.1.jar
cd $curhome


echo "--> Install JARs: Flink's connector" 
mkdir -p $curhome/data/flink/lib/flink 
cd $curhome/data/flink/lib/flink
wget https://repo1.maven.org/maven2/com/google/guava/failureaccess/1.0.2/failureaccess-1.0.2.jar
wget https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-kafka/3.2.0-1.19/flink-sql-connector-kafka-3.2.0-1.19.jar 
wget https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-parquet/1.19.1/flink-sql-parquet-1.19.1.jar 
wget https://repo.maven.apache.org/maven2/org/apache/flink/flink-avro/1.19.1/flink-avro-1.19.1.jar
wget https://repo1.maven.org/maven2/org/apache/avro/avro/1.11.3/avro-1.11.3.jar


cd $curhome


echo "--> Install JARs: Flink's Hive Metastore connector (Catalogs)" 
mkdir -p $curhome/data/flink/lib/hive
cd $curhome/data/flink/lib/hive
wget https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-hive-3.1.3_2.12/1.19.1/flink-sql-connector-hive-3.1.3_2.12-1.19.1.jar
wget https://repo.maven.apache.org/maven2/org/apache/hive/hive-exec/3.1.3/hive-exec-3.1.3.jar 
wget https://repo.maven.apache.org/maven2/org/apache/hive/hive-metastore/3.1.3/hive-metastore-3.1.3.jar
cd $curhome

echo "--> Install JARs: Flinks for Hive & Hadoop and AWS S3" 
mkdir -p $curhome/data/flink/lib/hadoop 
cd $curhome/data/flink/lib/hadoop
wget https://repo1.maven.org/maven2/org/apache/commons/commons-configuration2/2.1.1/commons-configuration2-2.1.1.jar
wget https://repo1.maven.org/maven2/commons-logging/commons-logging/1.1.3/commons-logging-1.1.3.jar
wget https://repo1.maven.org/maven2/org/apache/flink/flink-hadoop-compatibility_2.12/1.19.1/flink-hadoop-compatibility_2.12-1.19.1.jar
wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-auth/3.3.4/hadoop-auth-3.3.4.jar 
wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-common/3.3.4/hadoop-common-3.3.4.jar 
wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-hdfs-client/3.3.4/hadoop-hdfs-client-3.3.4.jar 
wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-mapreduce-client-core/3.3.4/hadoop-mapreduce-client-core-3.3.4.jar 
wget https://repo1.maven.org/maven2/org/apache/hadoop/thirdparty/hadoop-shaded-guava/1.1.1/hadoop-shaded-guava-1.1.1.jar
wget https://repo1.maven.org/maven2/org/codehaus/woodstox/stax2-api/4.2.1/stax2-api-4.2.1.jar 
wget https://repo1.maven.org/maven2/com/fasterxml/woodstox/woodstox-core/5.3.0/woodstox-core-5.3.0.jar 
cd $curhome



echo "--> Install JARs: Flink's Paimon, Mongo & JDBC Connector, Catalogs & CDC" 
mkdir -p $curhome/data/flink/lib/paimon 
cd $curhome/data/flink/lib/paimon
wget https://repo1.maven.org/maven2/org/apache/paimon/paimon-flink-1.19/0.9.0/paimon-flink-1.19-0.9.0.jar 
wget https://repo1.maven.org/maven2/org/apache/paimon/paimon-flink-action/0.9.0/paimon-flink-action-0.9.0.jar 
wget https://repo.maven.apache.org/maven2/org/apache/paimon/paimon-hive-connector-3.1/0.9.0/paimon-hive-connector-3.1-0.9.0.jar
wget https://repo1.maven.org/maven2/org/apache/paimon/paimon-s3/0.9.0/paimon-s3-0.9.0.jar
cd $curhome