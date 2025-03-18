.DEFAULT_GOAL := help
include ../.env

VERSION=1.0.0
HADOOP_VERSION=3.3.5
HIVE_VERSION=3.1.3

define HELP

Available commands:

- basehadoop: Build the Apache Hadoop base image project

- basehive: Build the Apache Hive base image project

- build: Build this project

- run: Run the project

- stop: Stop the project

- down: Down the project

- hms: Connect to Hive Metastore container

- hive: Connect to Hive Server2 container

- pg: Connect to Postgres container

- ps: Show all running containers

- logs: Show logs

- watch: Watch logs

endef

export HELP
help:
	@echo "$$HELP"
.PHONY: help

custom_ca:
ifdef CUSTOM_CA
	cp -rf $(CUSTOM_CA)/* ca_certificates/ || cp -f $(CUSTOM_CA) ca_certificates/
endif


basehadoopx:
	docker build --build-arg REPO_NAME=${REPO_NAME} -t ${REPO_NAME}/hadoop-base-$(HADOOP_VERSION)-java8:$(VERSION) ./basehadoop

basehivex:
	docker build --build-arg REPO_NAME=${REPO_NAME} -t ${REPO_NAME}/hive-base-$(HIVE_VERSION)-java8:$(VERSION) ./basehive 

build:  basehadoopx basehivex		
	docker build --build-arg REPO_NAME=${REPO_NAME} -t ${REPO_NAME}/hive-metastore-$(HIVE_VERSION)-java8:$(VERSION) ./hive-metastore 
	docker build --build-arg REPO_NAME=${REPO_NAME} -t ${REPO_NAME}/hive-hiveserver2-$(HIVE_VERSION)-java8:$(VERSION) ./hive-hiveserver2
	
run:
	docker compose -p ${COMPOSE_PROJECT_NAME} up -d

stop:
	docker compose stop

down:	
	docker compose down

hms: 
	docker compose exec -it metaserver bash

hive:
	docker compose exec -it hiveserver2 bash

pg: 
	docker compose exec -it postgres bash

ps:
	docker compose ps

logs:
	docker compose logs

watch:
	watch docker compose ps