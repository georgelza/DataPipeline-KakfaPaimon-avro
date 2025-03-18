#######################################################################################################################
#
#
#  	Project     	    : 	TimeSeries Data generation via Python Application 
#
#   File                :   connection.py
#
#   Description         :   This tries to simulate sources (this case factories at the mooment) as realist as possible.
#
#   Created     	    :   22 November 2024
#
#   Changelog           :   Modified from original from previous blog that posted to Mongo to now to post to Kafka.
#                       :   To make is "nice" i added allot of code to json serialize/encode the payload.
#                       :   the payload itself can be slightly modified by changing 0 to 1 of
#                       :   TSHUMAN, STRUCTMOD and DEVICETYPE in the runX.sh file or the dockercompose environment variables section.
#
#   JSON Viewer         :   https://jsonviewer.stack.hu
#
#   Mongodb             :   https://www.mongodb.com/cloud/atlas      
#                       :   https://hub.docker.com/r/mongodb/mongodb-atlas-local
#
#   Notes               :   
#
#
########################################################################################################################

__author__      = "George Leonard"
__email__       = "georgelza@gmail.com"
__version__     = "3.0.0"
__copyright__   = "Copyright 2024, - G Leonard"


import json, socket

from confluent_kafka import SerializingProducer, KafkaError, KafkaException
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry.json_schema import JSONSerializer


def createConnectionToStore(config_params, site, logger):
        
    if site["data_persistence"] == 1:   
        return createFileConnection(config_params, site["siteId"], logger), None

    else:        
        return createKafkaProducer(config_params, site["siteId"], logger)

    # end if
# end createConnectionToStore


def savePayloadToStore(connection, json_serializer, site, mode, payload, topic, logger):
    
    if site["data_persistence"] == 1:
        return writeToFile(connection, site["siteId"], mode, payload, logger)
    
    else:
        # Change to Kafka
        return postToKafka(connection, json_serializer, site["siteId"], mode, payload, topic, logger)
        
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
        logger.critical('connection.createFileConnection - {siteId} - FAILED Err: {err} '.format(
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
        logger.error('connection.writeToFile - {siteId} - mode {mode} - FAILED, Err: {err}'.format(
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


class Payload(object):
    
    """
    Payload record

    Args:
        ts (integer): 
        metadata (dict): 
            siteId (integer)
            deviceId (integer)
            sensorId (integer)
            unit (string)
            ts_human (string)
            location (dict)
                Longitude (integer)
                Latitude (integer)
            deviceType (string)
        measurement(number)
        
    """

    def __init__(self, ts, metadata, measurement):
        self.ts                 = ts
        self.metadata           = metadata
        self.measurement        = measurement

# end


class Location(object):
    
    def __init__(self, longitude, latitude):
        self.longitude  = longitude
        self.latitude   = latitude

    def to_dict(self):
        return {
            "longitude":    self.longitude
           ,"latitude":     self.latitude
        }
# end


class Metadata(object):
    
    def __init__(self, siteId, deviceId, sensorId, unit, ts_human=None, location=None, deviceType=None):
        self.siteId     = siteId
        self.deviceId   = deviceId
        self.sensorId   = sensorId
        self.unit       = unit
        self.ts_human   = ts_human if ts_human else None
        self.location   = location if location else None
        self.deviceType = deviceType if deviceType else None

    def to_dict(self):
        
        # Compulsory fields
        data = {
            "siteId":   self.siteId,
            "deviceId": self.deviceId,
            "sensorId": self.sensorId,
            "unit":     self.unit,
        }

        # Optional Fields
        # Conditionally add `ts_human` => Human readable timestamp
        if self.ts_human:
            data["ts_human"] = self.ts_human

        # Conditionally add `location` if they exist
        if self.location:
            data["location"] = self.location.to_dict()
            
        # Conditionally add `deviceType` if they exist
        if self.deviceType:
            data["deviceType"] = self.deviceType

        return data
# end

        
# JSON Serializer
def obj_to_json(obj, ctx):
    
    return dict(
        ts          = obj.ts,
        metadata    = obj.metadata.to_dict(),  # Convert Metadata object to dictionary
        measurement = obj.measurement
    )
#end obj_to_json


# https://www.youtube.com/watch?v=HX0yx5YX284    
def createKafkaProducer(config_params, siteId, logger):
       
    connection          = None  # Ensure it's initialized
        
    # Core Producer Connection  
    if config_params["SECURITY_PROTOCOL"] != "PLAINTEXT" :
        producer_conf = {
            'bootstrap.servers':    config_params["BOOTSTRAP_SERVERS"],
            'sasl.mechanism':       config_params["SASL_MECHANISMS"],
            'security.protocol':    config_params["SECURITY_PROTOCOL"],
            'sasl.username':        config_params["SASL_USERNAME"],
            'sasl.password':        config_params["SASL_PASSWORD"],
            'client.id':            socket.gethostname(),
            'error_cb':             error_cb,
        }
    else:
        producer_conf = {
            "bootstrap.servers":    config_params["BOOTSTRAP_SERVERS"],
            "security.protocol":    config_params["SECURITY_PROTOCOL"],
            "sasl.mechanism":       config_params["SASL_MECHANISMS"],
            'client.id':            socket.gethostname(),
            'error_cb':             error_cb,
        }        
    # end

    try:
        # Create producer
        connection = SerializingProducer(producer_conf)
        
    except KafkaError as kerr:
         logger.error('connection.createKafkaProducer.SerializingProducer - FAILED, Err: {kerr}'.format(
            kerr=kerr
        ))
                
    except Exception as err:
        logger.error('connection.createKafkaProducer.SerializingProducer - FAILED, Err: {err}'.format(
            err=err
        ))

        return None, None  # Ensure failure is handled properly

    # end

    # Schema Definition  - Temp here for now
    json_schema_str = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "type": "object",
        "properties": {
            "ts": {
                "description": "Timestamp in milliseconds since epoch (UTC)",
                "type": "number",
            },
            "metadata": {
                "type": "object",
                "properties": {
                    "siteId": {
                        "description": "Factory ID",
                        "type": "number"
                    },
                    "deviceId": {
                        "description": "Machine ID",
                        "type": "number"
                    },
                    "sensorId": {
                        "description": "Sensor Id",
                        "type": "number"
                    },
                    "unit": {
                        "description": "Unit of Measure of the sensor",
                        "type": "string"
                    },
                    "ts_human": {
                        "description": "Timestamp in milliseconds since epoch (UTC)/ Human readable",
                        "type": "string",
                    },
                    "location": {
                        "type": "object",
                        "properties": {
                            "latitude": {
                                "description": "Latitude of the Site, if the factory is say a moving object it can be the current Latitude when measurement was read",
                                "type": "number"
                            },
                            "longitude": {
                                "description": "Longitude of the Site, if the factory is say a moving object it can be the current Longitude when measurement was read",
                                "type": "number"
                            }
                        }
                    },
                    "deviceType": {
                        "description": "Type of Machine",
                        "type": "string"
                    }
                },
                "required": [
                    "siteId",
                    "deviceId",
                    "sensorId",
                    "unit"
                ]
            },
            "measurement": {
                "description": "Measured value of sensor",
                "type": "number"
            }
        },
        "required": [
            "ts",
            "metadata",
            "measurement"
        ]
    }

        

    # Schema Registry Serializer
    try:
                
        schema_registry_client = SchemaRegistryClient(
            {"url": config_params["KAFKA_SCHEMAREGISRY"]}
        )
    
        json_serializer = JSONSerializer(
            schema_str             = json.dumps(json_schema_str), 
            schema_registry_client = schema_registry_client,
            to_dict                = obj_to_json,
        )
    
    except Exception as err:
        logger.error('connection.createKafkaProducer.JSONSerializer - FAILED, Err: {url}, {err}'.format(
            url = config_params["KAFKA_SCHEMAREGISRY"],
            err = err
        ))
        return None, None  # Ensure failure is handled properly

    # end


    logger.info("Kafka Producer instantiated for: {siteId}, {connection}".format(
        siteId     = siteId,
        connection = connection
    ))
    
    logger.info("")
    
    return connection, json_serializer

#end createKafkaProducer


def buildPayload(payloadobj, siteId, logger):

    # ts
    try:

        ts  = payloadobj.get("ts")
        
    except Exception as err:
        logger.error("Payload before serialization: buildPayload.ts: {siteId}, {err}".format(
            siteId  = siteId,
            err     = err
        ))
    #end try ts
    
    
    # metadata
    try:
        
        met = payloadobj.get("metadata")
        
        # Construct metadata
        if met.get("ts_human"):
            if met.get("location"):
                
                loc      = met.get("location")
                location = Location(loc.get("longitude"), loc.get("latitude"))
                
                if met.get("deviceType"):
                    metadata = Metadata(met.get("siteId"), met.get("deviceId"), met.get("sensorId"), met.get("unit"), met.get("ts_human"), location, met.get("deviceType"))

                else: 
                    metadata = Metadata(met.get("siteId"), met.get("deviceId"), met.get("sensorId"), met.get("unit"), met.get("ts_human"), location, None)

                #end if
            else:

                if met.get("deviceType"):
                    metadata = Metadata(met.get("siteId"), met.get("deviceId"), met.get("sensorId"), met.get("unit"), met.get("ts_human"), None, met.get("deviceType"))

                else: 
                    metadata = Metadata(met.get("siteId"), met.get("deviceId"), met.get("sensorId"), met.get("unit"), met.get("ts_human"), None, None)

                #end if
            #end if
        else:
            if met.get("location"):
                loc      = met.get("location")
                location = Location(loc.get("longitude"), loc.get("latitude"))
                
                if met.get("deviceType"):
                    metadata = Metadata(met.get("siteId"), met.get("deviceId"), met.get("sensorId"), met.get("unit"), None, location, met.get("deviceType"))

                else: 
                    metadata = Metadata(met.get("siteId"), met.get("deviceId"), met.get("sensorId"), met.get("unit"), None, location, None)

                #end if                
            else:
                
                if met.get("deviceType"):
                    metadata = Metadata(met.get("siteId"), met.get("deviceId"), met.get("sensorId"), met.get("unit"), None, None, met.get("deviceType"))

                else: 
                    metadata = Metadata(met.get("siteId"), met.get("deviceId"), met.get("sensorId"), met.get("unit"), None, None, None)

                #end if
            #end if
        #end if
        
    except Exception as err:
        logger.error("Payload before serialization: buildPayload.metadata: {siteId}, {err}".format(
            siteId  = siteId,
            err     = err
        ))        

    # end try metadata

            
    # measurement
    try:
        
        measurement = payloadobj.get("measurement")
    
    except Exception as err:
        logger.error("Payload before serialization: buildPayload.measurement: {siteId}, {err}".format(
            siteId  = siteId,
            err     = err
        ))

    # end try measurement


    return Payload(
         ts
        ,metadata
        ,measurement
    )

# end


def postToKafka(connection, json_serializer, key, mode, payloadmsg, topic, logger):
    
    topic = "factory_iot"
#    key   = string_serializer(str(key))
    key   = str(key)
        
    if connection is None:
        logger.error("Kafka producer is None, skipping produce.")
        
    else:
    
        try:
            if mode == 0:
                mode = "PostOne"
                                        
                payload = buildPayload(payloadmsg, key, logger)

                value = json_serializer(payload, SerializationContext(topic, MessageField.VALUE))

                connection.produce(
                    topic       = topic,
                    key         = key,
                    value       = value,
                )

                connection.poll(0)
            
            else:
                mode = "PostMany"
                
                for val in payloadmsg:     
                                    
                    payload = buildPayload(val, key, logger)
                    
                    logger.debug(f"Payload before serialization: {payload} (type: {type(payload)})")

                    value = json_serializer(payload, SerializationContext(topic, MessageField.VALUE))

                    connection.produce(
                        topic       = topic,    
                        key         = key,
                        value       = value,
                    )
                                    
                connection.flush()

            #end if
            return 1
        
        except Exception as err:
            logger.error('connection.postTokafka.produce - mode {mode} - FAILED, Err: {err}'.format(
                mode = mode,
                err  = err
            ))
            return 0
            
        # end try
        
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
