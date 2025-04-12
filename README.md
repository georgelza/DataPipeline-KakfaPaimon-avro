# Building a Kafka to Apache Paimon Sync Pipeline

## Overview

Data pulled from Kafka Topics using Apache Flink: **paimon_flink_action** frame work. -> [Apache Paimon Quick Start](https://paimon.apache.org/docs/0.9/flink/quick-start/)


Data to be stored as **Apache Parquet** and **Apache Avro** onto **MinIO S3** Object store, using a **Apache Hive Metastore** as catalog with Apache Paimon Open table format.


### Modules and Versions

- Apache Flink 1.19.1-scala_2.12-java11 on Hadoop version: 3.3.4
- Flink CDC 3.2   - required by Flink 1.19.x
- Apache Paimon 0.9.0
- Confluent Kafka 7.7.1
- Ubuntu 24.04 LTS
- Hive Metastore 3.1.3 on Hadoop 3.3.5
- PostgreSQL 12
- Python 3.13


## IoT Payload

Below is a list of the various payloads that can be created.

NBBBBBB - Please Note... if you were following my previous blogs in the series, you would notice it was REQUIRED TO modify the original IoT Payload -> We moved `siteId` to root level of the payload.

This was caused by the pull/infer schema/create table/push data pipeline we creating using Avro serialized data and the schema Registry integratio example. The topic key is "imagined" to be the primary key on the table, even though no key/index is created and well we know siteId's are not unique.  

Then you will see on the topic itself, the payload is now nested undera after tag, with a before being null, this is required bythe Debezium Avro source connector.


### Basic min IoT Payload

```json5
{
    "ts" : 123421452622,
    "siteId" : 1009,
    "metadata" : {
        "deviceId" : 1042,
        "sensorId" : 10180,
        "unit" : "Psi"
    },
    "measurement" : 1013.3997
}
```

### Basic min IoT Payload, with a human readable time stamp


```json5
{
    "ts" : 123421452622,
    "siteId" : 1009,
    "metadata" : {
        "deviceId" : 1042,
        "sensorId" : 10180,
        "unit" : "Psi",
        "ts_human" : "2024-10-02T00:00:00.869Z"
    },
    "measurement" : 1013.3997
}
```


### Modified IoT Payload -> schema evolution, we add location tag.

```json5
{
    "ts" : 123421452622,
    "siteId" : 1009,
    "metadata" : {
        "deviceId" : 1042,
        "sensorId" : 10180,
        "unit" : "Psi",
        "ts_human" : "2024-10-02T00:00:00.869Z",
        "location": {
            "latitude": -26.195246, 
            "longitude": 28.034088
        }
    },
    "measurement" : 1013.3997
}
```

### Modified IoT Payload -> schema evolution, here we further deviceType tag.

```json5
{
    "ts" : "2024-10-02T00:00:00.869Z",
    "siteId" : 1009,
    "metadata" : {
        "deviceId" : 1042,
        "sensorId" : 10180,
        "unit" : "Psi",
        "ts_human" : "2024-10-02T00:00:00.869Z",
        "location": {
            "latitude": -26.195246, 
            "longitude": 28.034088
        },
        "deviceType" : "Oil Pump"
    },
    "measurement" : 1013.3997
}
```


## To run the project.



### See various configuration settings and passwords in:

0. devlab/docker_compose.yml

1. .pwd in app_iot1 in runX.sh

2. devlab/.env

3. devlab/conf/hive.env

4. devlab/conf/hive-site.xml

### Download containers and libraries

1. cd infrastructure

2. make pullall

3. make buildall


### Build various containers

1. cd devlab

2. ./getlibs.sh

3. make build

4. Now, to run it please stay in devlab and refer to README.md in there...



## Projects / Components

- [One-Click Database Synchronization from Kafka Topic to Paimon Using Flink CDC](https://paimon.apache.org/docs/0.9/), navigate to Engine Flink and then down into CDC Ingestion.

- [Apache Flink](https://flink.apache.org)

- [Ververica](https://www.ververica.com)

- [Apache Kafka](https://kafka.apache.org)

- [Confluent Kafka](https://kafka.apache.org)

- [Apache Paimon](https://paimon.apache.org)

- [Apache Parquet File format](https://parquet.apache.org)

- [Apache Avro](https://avro.apache.org)


## Misc Notes

### Flink Libraries

As I was travelling while writing this blog and did not want to pull the libraries on every build I decided to downlaod them once into the below directory and then copy them on build into container. Just a different way less bandwidth and also slightly faster.

The `devlab/data/flink/lib` directories will house our Java libraries required by our Flink stack. 

Normally I'd include these in the Dockerfile as part of the image build, but during development it's easier if we place them here and then mount the directories into the containers at run time via our `docker-compose.yml` file inside the volume specification for the flink-* services.

This makes it simpler to add/remove libraries as we simply have to restart the flink container and not rebuild it.

Additionally, as the `flink-jobmanager`, `flink-taskmanager` use the same libraries doing it tis way allows us to use this one set, thus also reducing the disk space and the container image size.

The various files are downloaded by executing the `getlibs.sh` file located in the `devlab/` directory.


### Flink base container images

    
docker pull arm64v8/flink:1.19-scala_2.12-java11


- https://flink.apache.org/downloads/#apache-flink-jdbc-connector-320
- https://flink.apache.org/downloads/#apache-flink-kafka-connector-330
- https://flink.apache.org/downloads/#apache-flink-mongodb-connector-120
   


## Kafka Connectors

### MongoDB provided Connector, source/sink

- hub/mongodb/kafka-connect-mongodb

### MongoDB by Debezium provided Connector, source

- hub/debezium/debezium-connector-mongodb


### Flink source connector

- https://nightlies.apache.org/flink/flink-cdc-docs-release-3.2/docs/connectors/flink-sources/mongodb-cdc/


## Manual pull of all source containers images from `hub.docker.com`


### Get Confluent CP Cluster

```
docker pull confluentinc/cp-kafka:7.7.1
docker pull confluentinc/cp-schema-registry:7.7.1
docker pull confluentinc/cp-enterprise-control-center:7.7.1
docker pull confluentinc/cp-ksqldb-server:7.7.1
docker pull confluentinc/cp-ksqldb-cli:7.7.1
docker pull confluentinc/cp-kcat:7.7.1
docker pull confluentinc/cp-kafka-connect-base:7.7.1
```
or    
```
docker pull confluentinc/cp-server:7.7.1 --platform linux/arm64
```

## Uncategorized notes

Some misc notes:

[Apache Flink FLUSS](https://www.linkedin.com/posts/polyzos_fluss-is-now-open-source-activity-7268144336930832384-ds87?utm_source=share&utm_medium=member_desktop)

[Apache Flink Deployment](https://nightlies.apache.org/flink/flink-docs-release-1.19/docs/deployment/resource-providers/standalone/docker/)    
    
[Apache Flink SQL Connector](https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-kafka/)

[Apache Flink MongoDB CDC Setup](https://nightlies.apache.org/flink/flink-cdc-docs-release-3.2/docs/connectors/flink-sources/mongodb-cdc/)

[Troubleshooting Apache Flink SQL S3 problems](https://www.decodable.co/blog/troubleshooting-flink-sql-s3-problems)

### Flink Cluster

[how-to-set-up-a-local-flink-cluster-using-docker](https://medium.com/marionete/how-to-set-up-a-local-flink-cluster-using-docker-0a0a741504f6)

### RocksDB

[Using RocksDB State Backend in Apache Flink: When and How](https://flink.apache.org/2021/01/18/using-rocksdb-state-backend-in-apache-flink-when-and-how/)


### DuckDB

[Can hashtag#duckdb revolutionize the data lake experience?](https://www.linkedin.com/posts/mehd-io_duckdb-activity-7265743807625723905-_OO4/?utm_source=share&utm_medium=member_desktop)

[Youtube: Can DuckDB revolutionize the data lake experience?](https://www.youtube.com/watch?v=CDzqDpCNjiY&feature=youtu.be)


### Log4J Logging levels

[Log4J Logging Levels](https://logging.apache.org/log4j/2.x/manual/customloglevels.html)
    
- The Flink jobmanager and taskmanager log levels can be modified by editing the various `devlab/conf/*.properties` files.


### Great quick reference for docker compose

[A Deep dive into Docker Compose by Alex Merced](https://dev.to/alexmercedcoder/a-deep-dive-into-docker-compose-27h5)


### Consider using secrets for sensitive information

[How to use sectrets with Docker Compose](https://docs.docker.com/compose/how-tos/use-secrets/)


### Enabling Prometheus monitoring on Minio with grafana dashboard

[Enabling Prometheus Scraping of Minio](https://min.io/docs/minio/linux/operations/monitoring/metrics-and-alerts.html)

[Grafana Dashboards](https://min.io/docs/minio/linux/operations/monitoring/grafana.html#minio-server-grafana-metrics)


### By:

George

[georgelza@gmail.com](georgelza@gmail.com)

[https://www.linkedin.com/in/george-leonard-945b502/](https://www.linkedin.com/in/george-leonard-945b502/)