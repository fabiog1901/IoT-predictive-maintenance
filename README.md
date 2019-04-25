# IoT Predictive Maintenance DRAFT

## Initial setup

Open the Workbench and start a Python3 Session, then run the following command to install some required libraries:
```
!pip3 install --upgrade pip dask keras matplotlib pandas_highcharts protobuf tensorflow seaborn sklearn
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


### NiFi generateFlowFile

```
{
"sensor_id": ${random():mod(10):plus(1)},
"sensor_ts": ${random():mod(999):plus(1)},
"sensor_1": ${random():mod(999):plus(1)},
"sensor_3": ${random():mod(999):plus(1)},
"sensor_4": ${random():mod(999):plus(1)},
"sensor_5": ${random():mod(999):plus(1)},
"sensor_6": ${random():mod(999):plus(1)},
"sensor_7": ${random():mod(999):plus(1)},
"sensor_8": ${random():mod(999):plus(1)},
"sensor_9": ${random():mod(999):plus(1)},
"sensor_10": ${random():mod(999):plus(1)},
"sensor_11": ${random():mod(999):plus(1)},
"sensor_12": ${random():mod(999):plus(1)},
"sensor_13": ${random():mod(999):plus(1)},
"sensor_14": ${random():mod(999):plus(1)},
"sensor_15": ${random():mod(999):plus(1)},
"sensor_16": ${random():mod(999):plus(1)},
"sensor_17": ${random():mod(999):plus(1)},
"sensor_18": ${random():mod(999):plus(1)},
"sensor_19": ${random():mod(999):plus(1)}
}
```

### Run SparkStreaming Job

```
$ ACCESS_KEY
$ PUBLIC_IP=`dig +short myip.opendns.com @resolver1.opendns.com`
$ sed -i "s/YourHostname/`hostname -f`/" spark_streaming.py
$ sed -i "s/YourCDSWDomain/cdsw.$PUBLIC_IP.nip.io/" spark_streaming.py
$ sed -i "s/YourAccessKey/$ACCESS_KEY/" spark_streaming.py
$ wget  http://central.maven.org/maven2/org/apache/kudu/kudu-spark2_2.11/1.9.0/kudu-spark2_2.11-1.9.0.jar
$ wget https://raw.githubusercontent.com/swordsmanliu/SparkStreamingHbase/master/lib/spark-core_2.11-1.5.2.logging.jar
$ rm -rf ~/.m2 ~/.ivy2/
$ mv ~/mock-data-generator/sparkstreamingkudu.py ~
$ spark-submit --master local[2] --jars kudu-spark2_2.11-1.9.0.jar,spark-core_2.11-1.5.2.logging.jar --packages org.apache.spark:spark-streaming-kafka_2.11:1.6.3 sparkstreamingkudu.py
```

### Kudu table

```
CREATE TABLE sensors
(
 sensor_id INT,
 sensor_ts INT, 
 sensor_1 DOUBLE,
 sensor_3 DOUBLE,
 sensor_4 DOUBLE,
 sensor_5 DOUBLE,
 sensor_6 DOUBLE,
 sensor_7 DOUBLE,
 sensor_8 DOUBLE,
 sensor_9 DOUBLE,
 sensor_10 DOUBLE,
 sensor_11 DOUBLE,
 sensor_12 DOUBLE,
 sensor_13 DOUBLE,
 sensor_14 DOUBLE,
 sensor_15 DOUBLE,
 sensor_16 DOUBLE,
 sensor_17 DOUBLE,
 sensor_18 DOUBLE,
 sensor_19 DOUBLE,
 is_healthy INT,
 PRIMARY KEY (sensor_ID, sensor_ts)
)
PARTITION BY HASH PARTITIONS 16
STORED AS KUDU
TBLPROPERTIES ('kudu.num_tablet_replicas' = '1');
```
