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

6. Paste command from `devlab/creFlinkFlows/2.creCdcTopic.bsh`


### Our Data Generator's.

1. To run Python container app (1) - factory_iot

`make rp1`          -> New Kafka->Paimon Action Framework flow. App 1, **factory_iot** collection

2. Stop app (1)

`make sp1`

You ca similarly execute `rp2` and `rp3` each of which expands the contents of the payload.