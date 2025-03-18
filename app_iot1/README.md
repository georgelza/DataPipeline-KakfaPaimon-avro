# Python based IoT TimeSeries data generator

## Overview

This is our Python application that attempt to create as realistic as possible sensor data/readings.

The configuration is control via the `runX.sh`, `.pwd` and `app_iot1/conf/Full.json` files and via the environment variables configured in `devlab/docker-compose.yml`.

At this stage it only pushes a payload to a Kafka cluster, with a single topic, with the various factories/sites siteId forming the key field.



