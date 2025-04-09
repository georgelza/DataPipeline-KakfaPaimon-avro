#######################################################################################################################
#
#
#  	Project     	    : 	TimeSeries Data generation via Python Application 
#
#   File                :   connection.py
#
#   Description         :   This tries to simulate sources (this case factories at the mooment) as realist as possible.
#
#   Created     	    :   10 May 2025
#
#   Changelog           :   Modified from original from previous blog that posted to Mongo to now to post to Kafka.
#                       :   To make is "nice" i added allot of code to avro serialize/encode the payload in this version.
#                       :   the payload itself can be slightly modified by changing 0 to 1 the fllowing variables: 
#                       :   TSHUMAN, STRUCTMOD and DEVICETYPE in the runX.sh file or the docker compose.yamo environment variables section.
#
#   JSON Viewer         :   https://jsonviewer.stack.hu
#
#   Notes               :   
#
#   json to avro schema	: http://www.dataedu.ca/avro
#
########################################################################################################################

__author__      = "George Leonard"
__email__       = "georgelza@gmail.com"
__version__     = "3.2.0"
__copyright__   = "Copyright 2024, - G Leonard"


import json, socket, os

# from confluent_kafka import avro, Producer, KafkaError, KafkaException
# from confluent_kafka.avro import CachedSchemaRegistryClient, MessageSerializer

from confluent_kafka import avro, KafkaException, KafkaError
from confluent_kafka.avro import AvroProducer 


from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.schema_registry import Schema


def createConnectionToStore(config_params, site, logger):
        
    if site["data_persistence"] == 1:   
        return createFileConnection(config_params, site["siteId"], logger)

    else:  
        return avro_producer(config_params, site["siteId"], logger)    
#        return createKafkaProducer(config_params, site["siteId"], logger)

    # end if
# end createConnectionToStore


def savePayloadToStore(connection, site, mode, payload, topic, logger):
    
    if site["data_persistence"] == 1:
        return writeToFile(connection, site["siteId"], mode, payload, logger)
    
    else:
        # Change to Kafka
        return postToKafka(connection, site["siteId"], mode, payload, topic, logger)
        
    # end if
# end savePayloadToStore


def closeConnectionToStore(connection, site, mode, logger):
    
    if site["data_persistence"] == 1:
        closeFileConnection(connection, site["siteId"], mode, logger)
            
    # end if
    
# end closeConnectionToStore


""" 
Lets create to write json strings to a file.
This will be json structured flattened into a single line.
"""
def createFileConnection(config_params, siteId, logger):
    
    file = None
    
    try:
        filename    = config_params["FILEROOT"] + "_" + str(siteId) + ".json"

        if filename != "": 
            file = open(filename, 'a')  # Open the file in append mode
            
            if file != None:
                logger.debug('connection.createFileConnection - Filename {filename} OPENED'.format(
                    filename = filename
                ))   
                return file

            else:
                return -1
            
            #end if            
        # end if                                 
                       
    except IOError as err:
        logger.critical('connection.createFileConnection - {siteId} - FAILED IO Err: {err} '.format(
            siteId = siteId,
            err    = err
        ))
        
        return -1
    
    # end try
# end createFileConnection


def writeToFile(file, siteId, mode, payload, logger):

    try:

        if file:        
            if mode == 0:
                mode = "writeOne"
                # Convert the payload dictionary to a JSON string
                payload_json = json.dumps(payload)
                file.write(payload_json + '\n')  # Add a newline at the end

            else:

                mode = "writeMany"
                for record in payload:
                    # Convert each payload to a JSON string and write it to the file
                    payload_json = json.dumps(record)
                    file.write(payload_json + '\n')  # Write each payload on a new line
                    
            # end if
                        
            return 1
   
    except IOError as err:
        logger.error('connection.writeToFile - {siteId} - mode {mode} - FAILED, IO Err: {err}'.format(
            siteId = siteId,
            mode   = mode,
            err    = err
        ))
        
        return -1

    # end try
# end writeToFile


def closeFileConnection(file, siteId, mode, logger):
    
    if file:
        try:
            file.close()
            
        except IOError as err:
            logger.error('connection.closeFileConnection - {siteId} - mode {mode} - FAILED, Err: {err}'.format(
                siteId = siteId,
                mode   = mode,
                err    = err
            ))
                        
        # end try
    # endif
# end close_file


def error_cb(err, logger):
    """ The error callback is used for generic client errors. These
        errors are generally to be considered informational as the client will
        automatically try to recover from all errors, and no extra action
        is typically required by the application.
        For this example however, we terminate the application if the client
        is unable to connect to any broker (_ALL_BROKERS_DOWN) and on
        authentication errors (_AUTHENTICATION). """
    
    logger.error('Client error: {err}'.format(
        err    = err
    ))
    
    if err.code() == KafkaError._ALL_BROKERS_DOWN or err.code() == KafkaError._AUTHENTICATION:
        # Any exception raised from this callback will be re-raised from the
        # triggering flush() or poll() call.
        raise KafkaException(err)

# end error_cb


def load_avro_schema_from_file(siteId, logger):
    
    key_schema      = None
    value_schema    = None
    
    try:
        key_schema   = avro.load('./avro/factory_iot-key.avsc')
        value_schema = avro.load('./avro/factory_iot-value.avsc')

    except Exception as err:
        logger.fatal('connection.load_avro_schema_from_file - FAILED, for: {siteId}, Other Err: {err}'.format(
            siteId  = siteId,
            err     = err
        ))

    return key_schema, value_schema
#end


def get_schema_from_schema_registry(schema_registry_url, schema_registry_subject, siteId, logger):
    
    sr              = None
    latest_version  = None
    
    try:
        sr = SchemaRegistryClient({'url': schema_registry_url})
        latest_version = sr.get_latest_version(schema_registry_subject)
        
    except KafkaError as kerr:
        logger.fatal('connection.get_schema_from_schema_registry - FAILED, for: {siteId}, Kafka Err: {kerr}'.format(
            siteId  = siteId,
            kerr    = kerr
        ))
    
    except Exception as err:
        logger.fatal('connection.get_schema_from_schema_registry - FAILED, for: {siteId}, Other Err: {err}'.format(
            siteId  = siteId,
            err     = err
        ))
        
    return sr, latest_version
#end


def register_schema(schema_registry_url, schema_registry_subject, schema_str, siteId, logger):

    sr          = None
    schema_id   = None
        
    try:
        sr          = SchemaRegistryClient({'url': schema_registry_url})
        schema      = Schema(schema_str, schema_type="AVRO")
        schema_id   = sr.register_schema(subject_name=schema_registry_subject, schema=schema)

    except KafkaError as kerr:
        logger.fatal('connection.register_schema - FAILED, for: {siteId}, Kafka Err: {kerr}'.format(
            siteId  = siteId,
            kerr    = kerr
        ))
    
    except Exception as err:
        logger.fatal('connection.register_schema - FAILED, for: {siteId}, Other Err: {err}'.format(
            siteId  = siteId,
            err     = err
        ))

    return schema_id
#end 


# https://github.com/confluentinc/confluent-kafka-python/blob/master/examples/avro_producer.py
def avro_producer(config_params, siteId, logger):
    
    producer = -1
    
    try:

        # schema_id = register_schema(schema_registry_url, schema_registry_subject, schema_str, siteId, logger)
        # schema_id = register_schema(schema_registry_url, schema_registry_subject, schema_str, siteId, logger)

        # key schema registry
        key_sr, key_latest_version = get_schema_from_schema_registry(
            schema_registry_url     = config_params["KAFKA_SCHEMAREGISRY"], 
            schema_registry_subject = config_params["KAFKA_TOPIC"]+"-key",
            siteId                  = siteId, 
            logger                  = logger
        )

        key_avro_serializer = AvroSerializer(
            schema_registry_client  = key_sr,
            schema_str              = key_latest_version.schema.schema_str,
            conf                    = {
                'auto.register.schemas': True
            }
        )

        # value chema registry
        value_sr, value_latest_version = get_schema_from_schema_registry(
            schema_registry_url     = config_params["KAFKA_SCHEMAREGISRY"], 
            schema_registry_subject = config_params["KAFKA_TOPIC"]+"-value",
            siteId                  = siteId, 
            logger                  = logger
        )

        value_avro_serializer = AvroSerializer(
            schema_registry_client  = value_sr,
            schema_str              = value_latest_version.schema.schema_str,
            conf                    = {
                'auto.register.schemas': True
            }
        )

        # Kafka Producer
        producer = SerializingProducer({
            'bootstrap.servers':    config_params["BOOTSTRAP_SERVERS"],
            'security.protocol':    config_params["SECURITY_PROTOCOL"],
            'key.serializer':       key_avro_serializer,
            'value.serializer':     value_avro_serializer,
            'delivery.timeout.ms':  120000, # set it to 2 mins
            'enable.idempotence':   True
        })
        
    except KafkaError as kerr:
        logger.fatal('connection.avro_producer - FAILED, for: {siteId}, Kafka Err: {kerr}'.format(
            siteId  = siteId,
            kerr    = kerr
        ))
    
    except Exception as err:
        logger.fatal('connection.avro_producer - FAILED, for: {siteId}, Other Err: {err}'.format(
            siteId  = siteId,
            err     = err
        ))
    
    return producer
#end


# https://www.youtube.com/watch?v=HX0yx5YX284    
def createKafkaProducer(config_params, siteId, logger):
    
 
    producer = None  # Ensure it's initialized

    key_schema, value_schema = load_avro_schema_from_file()
    
    # Create producer
    try:
        # Core Producer Connection  
        if config_params["SECURITY_PROTOCOL"] != "PLAINTEXT" :
            conf = {
                'bootstrap.servers':    config_params["BOOTSTRAP_SERVERS"],
                'sasl.mechanism':       config_params["SASL_MECHANISMS"],
                'security.protocol':    config_params["SECURITY_PROTOCOL"],
                'sasl.username':        config_params["SASL_USERNAME"],
                'sasl.password':        config_params["SASL_PASSWORD"],
                'schema.registry.url' : config_params["KAFKA_SCHEMAREGISRY"],
                'client.id':            socket.gethostname(),
                'error_cb':             error_cb
            }
        else:
            conf = {
                "bootstrap.servers":    config_params["BOOTSTRAP_SERVERS"],
                "security.protocol":    config_params["SECURITY_PROTOCOL"],
                "sasl.mechanism":       config_params["SASL_MECHANISMS"],
                'schema.registry.url' : config_params["KAFKA_SCHEMAREGISRY"],
                'client.id':            socket.gethostname(),
                'error_cb':             error_cb
            }        
        # end        

        if key_schema != None and value_schema != None:
            producer = AvroProducer(
                conf,
                default_key_schema   = key_schema,
                default_value_schema = value_schema
            )

                
    except KafkaError as kerr:
        logger.fatal('connection.createKafkaProducer.AvroProducer - FAILED, for: {siteId}, Kafka Err: {kerr}'.format(
            siteId  = siteId,
            kerr    = kerr
        ))
    
    except Exception as err:
        logger.fatal('connection.createKafkaProducer.AvroProducer - FAILED, for: {siteId}, Other Err: {err}'.format(
            siteId  = siteId,
            err     = err
        ))

    #end try 

    logger.info("Kafka Producer instantiated for: {siteId}, {connection}".format(
        siteId     = siteId,
        connection = producer
    ))
    
    logger.info("")
    
    return producer

#end createKafkaProducer


# 
# look at for avro producer using class type
# https://github.com/confluentinc/confluent-kafka-python/blob/master/examples/avro_producer.py
# https://www.redpanda.com/blog/produce-consume-apache-avro-tutorial
# https://gist.github.com/OneCricketeer/4db67f51fcaa02776340237762950b67
# https://medium.com/@mrugankray/create-avro-producer-for-kafka-using-python-f9029d9b2802

def postToKafka(producer, key, mode, payloadmsg, topic, logger):
    
    topic  = topic[0]
    keyval = {"siteId": key}

    if producer is None :
        logger.error("Kafka producer is None, skipping produce.")
        return 0

    else:
    
        if mode == 0:
            mode = "PostOne"
                                    
            logger.debug('Payload before serialization: key: {key}, value: {val}'.format(
                key = key,
                val = payloadmsg
            ))
            

            # Produce message (raw key, Avro-serialized value)
            try:                       
                producer.produce(
                    topic   = topic, 
                    key     = keyval,
                    value   = val
                )

                producer.poll(0)
                
            except KafkaError as kerr:
                logger.error('connection.postTokafka - mode {mode} - FAILED, for: {key}, Kafka Err: {kerr}'.format(
                    mode  = mode,
                    key   = key,
                    kerr  = kerr
                ))
                return 0

            except Exception as err:
                logger.error('connection.postTokafka - mode {mode} - FAILED, for: {key}, Other Err: {err}'.format(
                    mode = mode,
                    key  = key,
                    err  = err
                ))
                return 0
                
            # end try
            return 1

        else:          
            mode = "PostMany"
                        
            for val in payloadmsg:      
                               
                logger.debug('Payload before serialization: key: {key}, value: {val}'.format(
                    key = key,
                    val = payloadmsg
                ))

                # Produce message (raw key, Avro-serialized value)
                try:
                    
                    producer.produce(
                        topic   = topic,    
                        key     = keyval,
                        value   = val
                    )
                    
                    producer.flush()  # Ensure message is sent
            
                except KafkaError as kerr:
                    logger.error('connection.postTokafka - mode {mode} - FAILED, for: {key}, Kafka Err: {kerr}'.format(
                        mode  = mode,
                        key   = key,
                        kerr  = kerr
                    ))
                    return 0

                except Exception as err:
                    logger.error('connection.postTokafka - mode {mode} - FAILED, for: {key}, Other Err: {err}'.format(
                        mode = mode,
                        key  = key,
                        err  = err
                    ))
                    return 0

            #end for
            return 1                
            
        # end if
#end post_to_kafka


def delivery_callback(err, msg, logger):
    """Delivery report callback called (from flush()) on successful or failed delivery of the message."""
    if err is not None:
        logger.error('Failed to deliver message: {}'.format(err.str()))
        
    else:
        #pass
        logger.info('Produced to: {} [{}] @ {}'.format(msg.topic(), msg.partition(), msg.offset()))

    #end if
    
#end acked
