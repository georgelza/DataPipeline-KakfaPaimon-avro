
.DEFAULT_GOAL := help
include .env

define HELP

Available commands:

- build: Build all the images from the downloaded infrastructure components. After this execute "make run", followed by "make deploy" and then "make app".

- buildapp: Just build the docker app image.

- run: This will call core.
- deploy: This will create the Kafka topics, schema entries, all the Hive catalogs, Flink tables, flink inserts jobs etc.

- rp#: Run workload creator/the Python app -> Post onto Kafka Topic
- sp#: Stop Python app

- stop: Stop the project.
- start: Start a stopped project.
- down: Tear down the project, clean directories.
- ps: Show all running containers.

- logs: Show/tail logs.
- logsf: Stream logs.

- watch: Watch logs.
- ksql: Open KSql.
- fsql: Open Flink Jobmanager and start sql-client.
- jm: Open a bash terminal inside Jobmanager.

endef

export HELP
help:
	@echo "$$HELP"
.PHONY: help


build: 
	cd flink; make build
	cd ../app_iot1; make build

buildapp:
	cd ../app_iot1; make build

#	docker rmi $(docker images -q --filter "dangling=true")

run: 
	docker compose -p pipeline up -d broker schema-registry control-center  \
		minio mc flink-jobmanager flink-taskmanager \
		postgres metastore hiveserver2  --remove-orphans

# 		minio mc flink-jobmanager flink-taskmanager \

deploy: createcat
 
createcat:
	docker compose exec flink-jobmanager /opt/flink/bin/sql-client.sh -f /sql/creCat.sql
	
# This will CDC a single topic to a Paimon Table
deployCdcTopic: 
	docker compose exec flink-jobmanager /bsh/creCdcTopic.bsh	


# Run Python app  101,104
rp1:
	docker compose -p pipeline up -d iot1_datagen

# Stop Python app
sp1:
	docker compose stop iot1_datagen

# Run Python app  102,105
rp2:
	docker compose -p pipeline up -d iot2_datagen

# Stop Python app
sp3:
	docker compose stop iot2_datagen

# Run Python app  103,106
rp3:
	docker compose -p pipeline up -d iot3_datagen

# Stop Python app
sp2:
	docker compose stop iot3_datagen

stop:
	docker compose stop

start:
	docker compose start

down:	
	docker compose down
	cd data/minio; rm -rf * 
	cd data/postgres; rm -rf *
	cd data/warehouse; rm -rf *
	cd data/flink; rm -rf checkpoints logs rocksdb

ps:
	docker compose ps

logs:
	docker compose logs

logsf:
	docker compose logs -f

watch:
	watch docker compose ps


fsql:
	docker compose exec flink-jobmanager /opt/flink/bin/sql-client.sh

jm:
	docker compose exec flink-jobmanager /bin/bash
