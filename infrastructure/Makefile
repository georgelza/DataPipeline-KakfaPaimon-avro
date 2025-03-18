.DEFAULT_GOAL := help

define HELP

Available commands:

- pullall: Pull all source images.
- buildall: Build all images.
- clean: Remove all *.gz files downloaded

- os: Docker Pull all source OS images.

- confluent: Pull all the Confluent Kafka source images.

- flink: Pull all the Apache Flink base image.

- db: Pull all our database images.

- S3: Pull our MinIO and MC console image.

- misc: Pull the additional images, acting as glue etc.


endef

export HELP
help:
	@echo "$$HELP"
.PHONY: help

pullall: os confluent flink db s3 misc hadoop hive

buildall: builddb buildflinkbase buildos buildopenjdk8 buildhive


# Base images used along the way, used to build 2nd level images.
# arm64/v8 used as base for all images except the app/*.
os: 
	docker pull arm64v8/ubuntu:24.04

confluent:
	docker pull confluentinc/cp-kafka:7.7.1
	docker pull confluentinc/cp-kafka-connect-base:7.7.1
	docker pull confluentinc/cp-schema-registry:7.7.1
	docker pull confluentinc/cp-ksqldb-server:7.7.1
	docker pull confluentinc/cp-ksqldb-cli:7.7.1
	docker pull confluentinc/cp-enterprise-control-center:7.7.1
	docker pull confluentinc/cp-kcat:7.7.1

flink:
	docker pull arm64v8/flink:1.19.1-scala_2.12-java11

db:
	docker pull mysql:8.0
	docker pull postgres:12	
	docker pull paradedb/paradedb:latest

s3: 
	docker pull minio/minio:latest
	docker pull minio/mc:latest

misc:
# 	Used for inspecting data in the various back end stores.
	docker pull python:3.12-bookworm
	docker pull codieplusplus/duckdb

hadoop:
	cd build-hive-openjdk8/basehadoop; mkdir stage; cd stage; wget https://downloads.apache.org/hadoop/common/hadoop-3.3.5/hadoop-3.3.5-aarch64.tar.gz

hive:
# hive 3.1.3 is located in the Archive section now.
	cd build-hive-openjdk8/basehive; mkdir stage; cd  stage; wget https://archive.apache.org/dist/hive/hive-3.1.3/apache-hive-3.1.3-bin.tar.gz
	cd build-hive-openjdk8/basehive; cd stage; wget https://downloads.apache.org/hadoop/common/hadoop-3.3.5/hadoop-3.3.5-aarch64.tar.gz
	cd build-hive-openjdk8/basehive; cd stage; wget http://www.congiu.net/hive-json-serde/1.3.8/cdh5/json-serde-1.3.8-jar-with-dependencies.jar 
	cd build-hive-openjdk8/basehive; cd stage; wget https://jdbc.postgresql.org/download/postgresql-42.7.4.jar


# Build images, not 100% all of whats needed, but these are all common images.
buildflinkbase:
	cd build-flink-base-1.19.1; make build

builddb:
	cd build-postgres-12.0; make build

buildos:
	cd ./build-ubuntu-os-24.04; make build

buildopenjdk8:
	cd build-ubuntu-os-openjdk8; make build

buildhive:
	cd build-hive-openjdk8; make build

