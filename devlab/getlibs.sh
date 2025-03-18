#!/bin/bash

export curhome=$(pwd)
echo $curhome

echo "--> Install JARs: Flink's Kafka connector" 
mkdir -p $curhome/data/flink/lib/kafka 
cd $curhome/data/flink/lib/kafka

wget https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-kafka/3.2.0-1.19/flink-sql-connector-kafka-3.2.0-1.19.jar 
wget https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-avro-confluent-registry/1.19.1/flink-sql-avro-confluent-registry-1.19.1.jar
wget https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-avro/1.19.1/flink-sql-avro-1.19.1.jar
wget https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-json/1.19.1/flink-sql-json-1.19.1.jar
wget https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-parquet/1.19.1/flink-sql-parquet-1.19.1.jar 
cd $curhome

echo "--> Install JARs: Flink's Hive Metastore connector (Catalogs)" 
mkdir -p $curhome/data/flink/lib/hive
cd $curhome/data/flink/lib/hive

wget https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-hive-3.1.3_2.12/1.19.1/flink-sql-connector-hive-3.1.3_2.12-1.19.1.jar
wget https://repo.maven.apache.org/maven2/org/apache/hive/hive-exec/3.1.3/hive-exec-3.1.3.jar 
wget https://repo.maven.apache.org/maven2/org/apache/hive/hive-metastore/3.1.3/hive-metastore-3.1.3.jar
cd $curhome

echo "--> Install JARs: Flinks for Hive & Hadoop" 
mkdir -p $curhome/data/flink/lib/hadoop 
cd $curhome/data/flink/lib/hadoop

wget https://repo1.maven.org/maven2/commons-logging/commons-logging/1.1.3/commons-logging-1.1.3.jar
wget https://repo1.maven.org/maven2/org/codehaus/woodstox/stax2-api/4.2.1/stax2-api-4.2.1.jar 
wget https://repo1.maven.org/maven2/com/fasterxml/woodstox/woodstox-core/5.3.0/woodstox-core-5.3.0.jar 
wget https://repo1.maven.org/maven2/org/apache/commons/commons-configuration2/2.1.1/commons-configuration2-2.1.1.jar
wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-auth/3.3.4/hadoop-auth-3.3.4.jar 
wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-hdfs-client/3.3.4/hadoop-hdfs-client-3.3.4.jar 
wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-mapreduce-client-core/3.3.4/hadoop-mapreduce-client-core-3.3.4.jar 
wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-common/3.3.4/hadoop-common-3.3.4.jar 
wget https://repo1.maven.org/maven2/org/apache/flink/flink-hadoop-compatibility_2.12/1.19.1/flink-hadoop-compatibility_2.12-1.19.1.jar
#wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar
#wget https://repo1.maven.org/maven2/org/apache/flink/flink-shaded-hadoop-2-uber/2.8.3-10.0/flink-shaded-hadoop-2-uber-2.8.3-10.0.jar
cd $curhome



echo "--> Install JARs: Flink's Paimon, Mongo & JDBC Connector, Catalogs & CDC" 
mkdir -p $curhome/data/flink/lib/paimon 
cd $curhome/data/flink/lib/paimon

wget https://repo.maven.apache.org/maven2/org/apache/paimon/paimon-hive-connector-3.1/0.9.0/paimon-hive-connector-3.1-0.9.0.jar
wget https://repo.maven.apache.org/maven2/org/apache/flink/flink-connector-jdbc/3.2.0-1.19/flink-connector-jdbc-3.2.0-1.19.jar 
wget https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-mongodb-cdc/3.2.0/flink-sql-connector-mongodb-cdc-3.2.0.jar
wget https://repo1.maven.org/maven2/org/apache/paimon/paimon-s3/0.9.0/paimon-s3-0.9.0.jar
wget https://repo1.maven.org/maven2/org/apache/paimon/paimon-flink-1.19/0.9.0/paimon-flink-1.19-0.9.0.jar 
wget https://repo1.maven.org/maven2/org/apache/paimon/paimon-flink-action/0.9.0/paimon-flink-action-0.9.0.jar 
wget https://repo1.maven.org/maven2/org/apache/flink/flink-shaded-hadoop-2-uber/2.8.3-10.0/flink-shaded-hadoop-2-uber-2.8.3-10.0.jar


# Test Paimon => S3/MinIO
#echo "--> Install JARs: Flink's Paimon, Mongo & JDBC Connector, Catalogs & CDC" 
#mkdir -p $curhome/data/flink/lib/mysql
#cd $curhome/data/flink/lib/mysql

#wget https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.27/mysql-connector-java-8.0.27.jar
#wget https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-mysql-cdc/3.1.0/flink-sql-connector-mysql-cdc-3.1.0.jar

# wget https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-mysql-cdc/3.2.0/flink-sql-connector-mysql-cdc-3.2.0.jar



# wget https://repo1.maven.org/maven2/org/apache/hadoop/thirdparty/hadoop-shaded-guava/1.2.0/hadoop-shaded-guava-1.2.0.jar 
# wget https://repo1.maven.org/maven2/org/apache/hadoop/thirdparty/hadoop-shaded-guava/1.1.1/hadoop-shaded-guava-1.1.1.jar 


cd $curhome