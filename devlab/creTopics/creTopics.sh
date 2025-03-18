#!/bin/bash

export COMPOSE_PROJECT_NAME=pipeline

docker compose exec broker kafka-topics \
 --create -topic factory_iot \
 --bootstrap-server localhost:9092 \
 --partitions 1 \
 --replication-factor 1

# Lets list topics, excluding the default Confluent Platform topics
docker compose exec broker kafka-topics \
 --bootstrap-server localhost:9092 \
 --list | grep -v '_confluent' |grep -v '__' |grep -v '_schemas' | grep -v 'default' | grep -v 'docker-connect'

#./reg_telemetry.sh