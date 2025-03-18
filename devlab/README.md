## Environment configuration and deployment

See the master `README.md` file for the basic downloading of all the containers and library/jar files and building various containers images used and then see the "Run the stack - Example 1" lower down.

### Variables and Variables and Variables...

There is sadly no easy way to do this as this is not a small stack, of a single product.

- Start by going into `conf` directory and see the various files there.

- Followed by the `.env` file and then the docker-compose file.

- Also take note of the `configs` section in the `docker-compose.yml` file. These files are mapped into the various services.


### Flink configuration variables.

See the `docker-compose.yaml` file for the various variables passed into the Flink containers.

We use a combination of `enviroment:` values and values from files passed in via the `volumes:` section.

Some of them originate out of the `.env` file, for the Hive environment some originate out of the `hive.env` file and some out of `flink-conf-sc.yaml`.

You will also find the logging parameter files are specified in the `configs` section and then mapped into the containers in the services.

### Hive site configuration file/AWS S3 credentials for Flink usage.

Take note that the flink images are build with `hive-site.xml` copied it, this file also contains the credentuals for the MinIO S3 environment.


### PostgreSQL configuration, 

The credentials are sourced from the `.env` file and the start parameters out of `conf/postgresql.conf` & `conf/pg_hba.conf`.



## Run the stack - Example 1

### Basic last setup steps.

1. `make run`

2. `make ps`  -> until all stable, give is 20-30 seconds.

3. `make deploy` -> this will kick off a couple of scripts to create topics and various flink tables and jobs.

4. `make rp1`  -> run for 20seconds & then execute `make sp1` -> this is to give us some data in the Mongo collection used later as source for a schema.

5. `docker compose exec flink-jobmanager /bin/bash`

6. Paste contents of `devlab/creFlinkFlows/creCdcTableNorth.bsh`

or

6. `make deployCdcTableNorth`

### Our Data Generator's.

1. To run Python container app (1) - telemetry_north

`make rp1`          -> New Mongo->Paimon CDC flow. App 1, **telemetry_north** collection

2. Stop app (1)

`make sp1`


### Our Pipeline out of Paimon for real time processing.

Lets create some objects in flink to move the above paimon tables/data onwards to Kafka using FlinkSQL. This will take the North Paimon based table from above and instantiate flink Tables and from there do some magic onwards into Kafka. 

1. creFlinkAggNorth.sql

`make fsql`

Now copy paste the various lines from the above file.

2. Restart Python container app (1) - telemetry_north

`make rp1`


Thats the finish of the first set of ... examples...


## Run the stack - Example 2

Now onto the MongoDB replication example.

This is where you first cleanup and then redo all of this... but instead of executing creCdcTableNorth.bsh you execute creCdcDB.bsh above... and then you can proceed from here onwards.

Lets start.

1. Run Python container app (2) - telemetry_south

`make rp2`          -> New Mongo->Paimon CDC flow. App 2, **telemetry_south** collection

2. Stop app (2)

`make sp2` 

This would now have created a new collection for us to work with, and a "schema" structure, and since we've configured out FlinkCDC to replicate the entire MongoDB we would now also have a new Paimon table.

We can now execute the below to extend our aggregation jobs on Flink and Kafka.

2. creFlinkAggSouth.sql

`make fsql`

Now copy paste the various lines from the above file.
