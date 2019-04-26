# IoT Predictive Maintenance DRAFT

## Initial setup

Open the Workbench and start a Python3 Session, then run the following command to install some required libraries:
```
!pip3 install --upgrade pip scikit-learn
```

# A collapsible section with markdown
<details>
  <summary>Click to expand!</summary>
  
  ## Heading
  1. A numbered
  2. list
     * With some
     * Sub bullets
</details>

# A collapsible section with code
<details>
  <summary>Click to expand!</summary>
  
  ```javascript
    function whatIsLove() {
      console.log('Baby Don't hurt me. Don't hurt me');
      return 'No more';
    }
  ```
</details>


### NiFi 

```
### NIFI avro schema
{
  "name": "recordFormatName",
  "namespace": "nifi.examples",
  "type": "record",
  "fields": [
    { "name": "sensor_id", "type": "double" },
    { "name": "sensor_ts", "type": "double" },
    { "name": "sensor_0", "type": "double" },
    { "name": "sensor_1", "type": "double" },
    { "name": "sensor_2", "type": "double" },
    { "name": "sensor_3", "type": "double" },
    { "name": "sensor_4", "type": "double" },
    { "name": "sensor_5", "type": "double" },
    { "name": "sensor_6", "type": "double" },
    { "name": "sensor_7", "type": "double" },
    { "name": "sensor_8", "type": "double" },
    { "name": "sensor_9", "type": "double" },
    { "name": "sensor_10", "type": "double" },
    { "name": "sensor_11", "type": "double" }
  ]
}
```

### Run SparkStreaming Job

```
$ ACCESS_KEY=<put here your cdsw model access key>
$ PUBLIC_IP=`dig +short myip.opendns.com @resolver1.opendns.com`
$ mv ~/IoT-predictive-maintenance/spark_streaming.py ~
$ sed -i "s/YourHostname/`hostname -f`/" spark_streaming.py
$ sed -i "s/YourCDSWDomain/cdsw.$PUBLIC_IP.nip.io/" spark_streaming.py
$ sed -i "s/YourAccessKey/$ACCESS_KEY/" spark_streaming.py
$ wget  http://central.maven.org/maven2/org/apache/kudu/kudu-spark2_2.11/1.9.0/kudu-spark2_2.11-1.9.0.jar
$ wget https://raw.githubusercontent.com/swordsmanliu/SparkStreamingHbase/master/lib/spark-core_2.11-1.5.2.logging.jar
$ rm -rf ~/.m2 ~/.ivy2/
$ spark-submit --master local[2] --jars kudu-spark2_2.11-1.9.0.jar,spark-core_2.11-1.5.2.logging.jar --packages org.apache.spark:spark-streaming-kafka_2.11:1.6.3 spark_streaming.py
```

### Kudu table

```
CREATE TABLE sensors
(
 sensor_id INT,
 sensor_ts TIMESTAMP, 
 sensor_0 DOUBLE,
 sensor_1 DOUBLE,
 sensor_2 DOUBLE,
 sensor_3 DOUBLE,
 sensor_4 DOUBLE,
 sensor_5 DOUBLE,
 sensor_6 DOUBLE,
 sensor_7 DOUBLE,
 sensor_8 DOUBLE,
 sensor_9 DOUBLE,
 sensor_10 DOUBLE,
 sensor_11 DOUBLE,
 is_healthy INT,
 PRIMARY KEY (sensor_ID, sensor_ts)
)
PARTITION BY HASH PARTITIONS 16
STORED AS KUDU
TBLPROPERTIES ('kudu.num_tablet_replicas' = '1');
```
