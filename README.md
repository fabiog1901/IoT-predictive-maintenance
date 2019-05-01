# IoT Predictive Maintenance Workshop

## Intro

Labs summary:

*PART ONE: DATA SCIENTIST*
1. Using **CDSW**'s **Experiment** feature, train your model on the historical data.
2. Using the **Model** feature, deploy the model into production.

*PART TWO: DEVOPS*
3. On the Gateway host, run a simulator to send JSON data to a **MQTT** broker.
4. On the Gateway host, install and run **MiNiFi** to read from the MQTT broker, filter and forward to the **NiFi** cluster.
5. On the NiFi cluster, prepare and send to the **Kafka** cluster.
6. On the CDH cluster, read from the Kafka topic using **Spark Streaming**, call the **Model endpoint** and save results to **Kudu**.
7. Using **Impala** and **Hue**, pull reports on upcoming predicted machine failures.

## Lab 0 - Initial setup

1. Create a CDH+CDSW cluster as per instructions [here](https://github.com/fabiog1901/OneNodeCDHCluster).
2. Ensure you can SSH into the cluster, and that traffic from the cluster is only allowed from your own IP/VPN for security reasons.
3. Login into Cloudera Manager, and familiarize youself with the services installed. The URLs to access the services are:
  - Cloudera Manager: \<public-hostname\>:7180
  - NiFi: \<public-hostname\>:8080/nifi/
  - NiFi Registry: \<public-hostname\>:18080/nifireg/
  - Hue: \<public-hostname\>:8888
  - CDSW: cdsw.\<public-IP>.nip.io 

Login into Hue. As you are the first user to login into Hue, you are granted admin privileges. At this point, you won't need to do anything on Hue, but by logging in, CDH has created your HDFS user and folder, which you will need for the next lab. 

Ensure you remember the username and password, as you will use these throughout this workshop.


## Lab 1 - Train the model

Open CDSW Web UI and click on *sign up for a new account*. As you're the first user to login into CDSW, you are granted admin privileges.

Navigate to the CDSW **Admin** page to fine tune the environment:
- in the **Security** tab, add an _Engine_ with 2 vCPUs and 4 GB RAM, while deleting the default engine.
- add the following _Environment Variable_: 
   ```
   HADOOP_CONF_DIR = /etc/hadoop/conf/
   ```
Save, then return to the main page to Create a New Project from Git, using this GitHub project as the source.

Now that your project has been created, open the Workbench and start a Python3 Session, then run the following command to install some required libraries:
```
!pip3 install --upgrade pip scikit-learn
```

The project comes with a sample historical data. copy this dataset into HDFS

You're now ready to run the Experiment to train the model on your historical data

## Lab 2 - Deploy the model

# A collapsible section with markdown
<details>
  <summary>Click to expand!</summary>
  
  ## Heading
  1. A numbered
  2. list
     * With some
     * Sub bullets
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
