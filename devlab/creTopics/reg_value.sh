#!/bin/bash

# Register Schema's on local topics
schema=$(cat ../../app_iot1/avro/factory_iot-value.avsc | sed 's/\"/\\\"/g' | tr -d "\n\r")
SCHEMA="{\"schema\": \"$schema\", \"schemaType\": \"AVRO\"}"
curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  --data "$SCHEMA" \
  http://localhost:9081/subjects/factory_iot-value/versions
