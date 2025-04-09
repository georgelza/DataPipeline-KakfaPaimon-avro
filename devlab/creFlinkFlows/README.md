
# Data Flows

1. creCat.sql

Will create the 2 cataloges and their containing databases

- c_hive and DB: hive

- c_paimon and DB: iot

2. creCdcTopic.bsh

Here we will create the process that will sink the data from the source Kafka topic into the Paimon table using the Flink paimon action framework.    

Our data will be pushed into `c_paimin.iot.factory_iot` table.

- The Flink source document that will help us here is: [Kafka CDC](https://paimon.apache.org/docs/0.9/flink/cdc-ingestion/kafka-cdc/).




## Primary data flow:

We can now build our streaming pipeline.


## Diagnosing problems.

During my initial build of course like anything new, you battle, things might not work 100% first time round.

One of my questions was, how to specify my schema-registry, as that would allow Paimon store to know what the table structure needs to be for the data on the Kafka topic.


For this I had 3 unknowns... and a 3rd point, how to validate...

1. How do I specify the value.
    
    - See: [additional-kafka_config](https://paimon.apache.org/docs/master/cdc-ingestion/kafka-cdc/#additional-kafka_config)

2. Do I specify it with http://<target>:port or just <>:port
    
    Now, important to remember, the job-manager is a container... and if you specify that target ass 127.0.0.1 then it refers to itself, so change it to the hostname, my case, schema-registry as per the docker-compose.yml file

3. and then could my job manager reach it, for this the following document and the curl command executed on my job-manager answered the question.

    - [Schema Registry](https://docs.confluent.io/platform/current/schema-registry/develop/using.html)

    curl -X GET http://schema-registry:9081/subjects 