
-- Set this so that the operators are separate in the Flink WebUI.
SET 'pipeline.operator-chaining.enabled' = 'false';

-- display mode
-- SET 'sql-client.execution.result-mode' = 'table';

SET 'execution.runtime-mode' = 'streaming';
-- SET 'execution.runtime-mode' = 'batch';

-- Set checkpoint to happen every minute
SET 'execution.checkpointing.interval' = '30s';

USE c_hive.db;

-- c_hive.db used for transfer virtual tables
-- c_paimon used for data originating/destine from/to our paimon on s3 store

-- Full copy/Push of the Paimon to the Kafka topic
CREATE OR REPLACE TABLE c_hive.db.t_f_avro_telemetry (
     sensorId           STRING
    ,siteId             STRING
    ,deviceId           STRING
    ,unit               STRING
    ,ts                 TIMESTAMP(3)
    ,measurement        DOUBLE
    ,WATERMARK FOR ts AS ts
    ,PRIMARY KEY (deviceId, siteId, sensorId) NOT ENFORCED
) WITH (
     'connector'                                 = 'upsert-kafka'
    ,'topic'                                     = 'avro_telemetry'
    ,'properties.bootstrap.servers'              = 'broker:29092'
    ,'properties.group.id'                       = 'testGroup'
    ,'value.format'                              = 'avro-confluent'
    ,'value.avro-confluent.schema-registry.url'  = 'http://schema-registry:9081'
    ,'key.format'                                = 'json'
);


--    ,lat                STRING
--    ,long               STRING

-- https://repo.maven.apache.org/maven2/org/apache/flink/flink-avro-confluent-registry/1.9.1/flink-avro-confluent-registry-1.9.1.jar
-- SERDE
-- https://docs.confluent.io/platform/current/connect/userguide.html#configuring-key-and-value-converters

SET 'pipeline.name' = 'Paimon Telemetry - (t_f_avro_telemetry) -> Kafka (avro_telemetry)';

-- populated via rp1
INSERT INTO c_hive.db.t_f_avro_telemetry
  SELECT 
       JSON_VALUE(metadata, '$.sensorId') as sensorId
      ,JSON_VALUE(metadata, '$.siteId')   as siteId
      ,JSON_VALUE(metadata, '$.deviceId') as deviceId
      ,JSON_VALUE(metadata, '$.unit')     as unit
      ,TO_TIMESTAMP(FROM_UNIXTIME(CAST(JSON_VALUE(ts, '$.$date') AS BIGINT) / 1000)) as ts
      ,CAST(measurement AS DOUBLE) as measurement             
  FROM
    c_paimon.iot.telemetry;


-- Time  based Aggregated and Windowed
CREATE OR REPLACE TABLE c_hive.db.t_f_avro_telemetry_5min (
     sensorId           STRING
    ,siteId             STRING
    ,deviceId           STRING
    ,unit               STRING
    ,min_val            DOUBLE
    ,avg_val            DOUBLE
    ,max_val            DOUBLE
    ,stddev_val         DOUBLE
    ,window_start       TIMESTAMP(3)
    ,window_end         TIMESTAMP(3)
--    ,PRIMARY KEY (siteId, deviceId, sensorId) NOT ENFORCED
) WITH (
     'connector'                                 = 'kafka'
    ,'topic'                                     = 'avro_telemetry_5min'
    ,'properties.bootstrap.servers'              = 'broker:29092'
    ,'properties.group.id'                       = 'testGroup'
    ,'value.format'                              = 'avro-confluent'
    ,'value.avro-confluent.schema-registry.url'  = 'http://schema-registry:9081'
    ,'key.format'                                = 'json'
    ,'key.fields'                                = 'sensorId'
);

SET 'pipeline.name' = 'Telemetry_5min - (t_f_avro_telemetry_5min) -> Kafka (avro_telemetry_5min)';

INSERT INTO c_hive.db.t_f_avro_telemetry_5min
  SELECT  
     sensorId
    ,siteId
    ,deviceId
    ,unit
    ,min(measurement)         as min_val
    ,avg(measurement)         as avg_val
    ,max(measurement)         as max_val
    ,stddev_samp(measurement) as stddev_val
    ,window_start
    ,window_end
  FROM TABLE ( 
      TUMBLE(TABLE c_hive.db.t_f_avro_telemetry, DESCRIPTOR(ts), INTERVAL '2' MINUTE))
  GROUP BY siteId, deviceId, sensorId, unit, window_start, window_end;