import json, configparser, sys, requests
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark.storagelevel import StorageLevel
from pyspark.sql import SQLContext
from uuid import uuid1
from pyspark.sql.types import *

zk_broker = "localhost:2181"
kafka_topic = "iot"
kudu_master = "localhost"
kudu_table = "impala::default.sensors"

# define the table schema
schema = StructType([StructField("sensor_id", IntegerType(), True),
                     StructField("sensor_ts", IntegerType(), True),
                     StructField("sensor_1", DoubleType(), True),
                     StructField("sensor_3", DoubleType(), True),
                     StructField("sensor_4", DoubleType(), True),
                     StructField("sensor_5", DoubleType(), True),
                     StructField("sensor_6", DoubleType(), True),
                     StructField("sensor_7", DoubleType(), True),
                     StructField("sensor_8", DoubleType(), True),
                     StructField("sensor_9", DoubleType(), True),
                     StructField("sensor_10", DoubleType(), True),
                     StructField("sensor_11", DoubleType(), True),
                     StructField("sensor_12", DoubleType(), True),
                     StructField("sensor_13", DoubleType(), True),
                     StructField("sensor_14", DoubleType(), True),
                     StructField("sensor_15", DoubleType(), True),
                     StructField("sensor_16", DoubleType(), True),
                     StructField("sensor_17", DoubleType(), True),
                     StructField("sensor_18", DoubleType(), True),
                     StructField("sensor_19", DoubleType(), True),
                     StructField("is_healthy", IntegerType(), True)])

#Lazy SqlContext evaluation
def getSqlContextInstance(sparkContext):
    if ('sqlContextSingletonInstance' not in globals()):
        globals()['sqlContextSingletonInstance'] = SQLContext(sc)
    return globals()['sqlContextSingletonInstance']


def getPrediction(p):
    feature = "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (p['sensor_4'], p['sensor_1'], p['sensor_6'],
              p['sensor_8'], p['sensor_9'], p['sensor_11'], p['sensor_12'],p['sensor_14'],p['sensor_15'],
              p['sensor_17'], p['sensor_18'], p['sensor_19'])

    return = requests.post('http://YourCDSWdomain/api/altus-ds-1/models/call-model',
                       data='{"accessKey":"YourAccessKey", \
                             "request":{"feature":"' + feature + '"}}',
                              headers={'Content-Type': 'application/json'}).json()['response']['result']


#Insert data into Kudu
def insert_into_kudu(time,rdd):
    sqc = getSqlContextInstance(rdd.context)
    kudu_df = sqc.createDataFrame(rdd, schema)
    kudu_df.show()
    kudu_df.write.format('org.apache.kudu.spark.kudu') \
                 .option('kudu.master',kudu_master) \
                 .option('kudu.table',kudu_table) \
                 .mode("append") \
                 .save()

if __name__ == "__main__":
    sc = SparkContext(appName="SparkStreamingIntoKudu")
    ssc = StreamingContext(sc, 10) # 10 second window
    kvs = KafkaUtils.createStream(ssc, zk_broker, "iot_ss", {kafka_topic:1})

    # parse the kafka message into a tuple
    kafka_stream = kvs.map(lambda x: x[1]) \
                           .map(lambda l: json.loads(l)) \
                           .map(lambda p: (int(p['sensor_id']),
                                           int(p['sensor_ts']),
                                           float(p['sensor_1']),
                                           float(p['sensor_3']),
                                           float(p['sensor_4']),
                                           float(p['sensor_5']),
                                           float(p['sensor_6']),
                                           float(p['sensor_7']),
                                           float(p['sensor_8']),
                                           float(p['sensor_9']),
                                           float(p['sensor_10']),
                                           float(p['sensor_11']),
                                           float(p['sensor_12']),
                                           float(p['sensor_13']),
                                           float(p['sensor_14']),
                                           float(p['sensor_15']),
                                           float(p['sensor_16']),
                                           float(p['sensor_17']),
                                           float(p['sensor_18']),
                                           float(p['sensor_19']),
                                           getPrediction(p)))


    #For each RDD in the DStream, insert it into Kudu table
    kafka_stream.foreachRDD(insert_into_kudu)

    ssc.start()
    ssc.awaitTermination()

