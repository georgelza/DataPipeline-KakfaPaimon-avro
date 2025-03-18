
-- https://paimon.apache.org/docs/0.7/how-to/creating-catalogs/#creating-a-catalog-with-filesystem-metastore


USE CATALOG default_catalog;

CREATE CATALOG c_hive WITH (
  'type'          = 'hive',
  'hive-conf-dir' = './conf/'
);

USE CATALOG c_hive;

CREATE DATABASE IF NOT EXISTS c_hive.db;

SHOW DATABASES;


-- Paimon on S3
USE CATALOG default_catalog;

CREATE CATALOG c_paimon WITH (
     'type'                      = 'paimon'
    ,'catalog-type'              = 'hive'
    ,'hive-conf-dir'             = './conf/'
    ,'warehouse'                 = 's3a://warehouse/paimon/'
    ,'table-default.file.format' = 'parquet'
);


-- -- With above we just create table on storage, table inherites type from catalog definition

-- Create the below table to test the process of sinking into paimon on S3/MinIO

USE CATALOG c_paimon;

CREATE DATABASE IF NOT EXISTS c_paimon.iot;

SHOW DATABASES;