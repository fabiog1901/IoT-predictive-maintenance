# IoT Predictive Maintenance Workshop

## Intro

Labs summary:

1. Using **CDSW**'s **Experiment** feature, train your model on the historical data.
2. Using the **Model** feature, deploy the model into production.
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

**STEP 0** : Configure CDSW

Open CDSW Web UI and click on *sign up for a new account*. As you're the first user to login into CDSW, you are granted admin privileges.

Navigate to the CDSW **Admin** page to fine tune the environment:
- in the **Security** tab, add an _Engine_ with 2 vCPUs and 4 GB RAM, while deleting the default engine.
- add the following _Environment Variable_: 
   ```
   HADOOP_CONF_DIR = /etc/hadoop/conf/
   ```
 - Save

**STEP 1** : Create the project

Return to the main page to Create a New Project from Git, using this GitHub project as the source.

Now that your project has been created, open the Workbench and start a Python3 Session, then run the following command to install some required libraries:
```
!pip3 install --upgrade pip scikit-learn
```

The project comes with a sample historical data. Copy this dataset into HDFS:

```
!hdfs dfs -put data/historical_iot.txt /user/$HADOOP_USER_NAME
```

You're now ready to run the Experiment to train the model on your historical data.

**STEP 2** : Examine `cdsw.iot_exp.py`

Open the file `cdsw.iot_exp.py`. This is a python program that builds a model to predict machine failure (the likelihood that this machine is going to fail). There is a dataset available on hdfs with customer data, including a failure indicator field.

The program is going to build a failure prediction model using the Random Forest algorithm. Random forests are ensembles of decision trees. Random forests are one of the most successful machine learning models for classification and regression. They combine many decision trees in order to reduce the risk of overfitting. Like decision trees, random forests handle categorical features, extend to the multiclass classification setting, do not require feature scaling, and are able to capture non-linearities and feature interactions.

`spark.mllib` supports random forests for binary and multiclass classification and for regression, using both continuous and categorical features. `spark.mllib` implements random forests using the existing decision tree implementation. Please see the decision tree guide for more information on trees.

The Random Forest algorithm expects a couple of parameters:

numTrees: Number of trees in the forest.
Increasing the number of trees will decrease the variance in predictions, improving the model’s test-time accuracy. Training time increases roughly linearly in the number of trees.

maxDepth: Maximum depth of each tree in the forest.
Increasing the depth makes the model more expressive and powerful. However, deep trees take longer to train and are also more prone to overfitting. In general, it is acceptable to train deeper trees when using random forests than when using a single decision tree. One tree is more likely to overfit than a random forest (because of the variance reduction from averaging multiple trees in the forest).

In the `cdsw.iot_exp.py` program, these parameters can be passed to the program at runtime, to these python variables:

```
param_numTrees = int(sys.argv[1])
param_maxDepth = int(sys.argv[2])
```

Also note the quality indicator for the Random Forest model, are written back to the Data Science Workbench repository:

```
cdsw.track_metric("auroc", auroc)
cdsw.track_metric("ap", ap)
```

These indicators will show up later in the **Experiments** dashboard.

**STEP 3** : Run the experiment for the first time

Now, run the experiment using the following parameters:

```
numTrees = 40 numDepth = 20
```

From the menu, select `Run -> Experiments`. Now, in the background, the Data Science Workbench environment will spin up a new docker container, where this program will run.

Go back to the **Projects** page in CDSW, and hit the **Experiments** button.

If the Status indicates ‘Running’, you have to wait till the run is completed. In case the status is ‘Build Failed’ or ‘Failed’, check the log information. This is accessible by clicking on the run number of your experiments. There you can find the session log, as well as the build information.

In case your status indicates ‘Success’, you should be able to see the auroc (Area Under the Curve) model quality indicator. It might be that this value is hidden by the CDSW user interface. In that case, click on the ‘3 metrics’ links, and select the auroc field. It might be needed to de-select some other fields, since the interface can only show 3 metrics at the same time.

In this example, 0.871. Not bad, but maybe there are better hyper parameter values available.

**STEP 4** : Re-run the experiment several times

Now, re-run the experiment 3 more times and try different values for NumTrees and NumDepth. Try the following values:

```
NumTrees NumDepth
15       25
25       20
```

When all runs have completed successfully, check which parameters had the best quality (best predictive value). This is represented by the highest ‘area under the curve’, auroc metric.

**STEP 5** : Save the best model to your environment

Select the run number with the best predictive value. In the Overview screen of the experiment, you can see that the model in spark format, is captured in the file `iot_model.pkl`. Select this file and hit the **Add to Project** button. This will copy the model to your project directory.


## Lab 2 - Deploy the model

**STEP 1** : Examine the program cdsw.iot_model.py

Open the project you created in the previous lab, and examine the file. This PySpark program uses the pickle.load mechanism to deploy models. The model it refers to the `iot_modelf.pkl` file, was saved in the previous lab from the experiment with the best predictive model.

There is a predict definition which is the function that calls the model, using features, and will return a result variable.

**STEP 2 **: Deploy the model

From the projects page of your project, select the **Models** button. Select **New Model** and populate specify the following configuration:

```
Name:	         "IoT Prediction Model"
Description:	 "IoT Prediction Model"
File:		       cdsw.iot_model.py
Function:	     predict	
Example Input: {"feature": "0, 65, 0, 137, 21.95, 83, 19.42, 111, 9.4, 6, 3.43, 4"}
Kernel:		     Python 3
Engine:	       2 vCPU / 4 GB Memory
Replicas:	     1
```

If all parameters are set, you can hit the **Deploy Model** button. Wait till the model is deployed. This will take several minutes.

**STEP 3** : Test the deployed model

After the several minutes, your model should get to the **Deployed** state. Now, click on the Model Name link, to go to the Model Overview page. From the that page, hit the **Test** button to check if the model is working.

The green color with success is telling that our REST call to the model is technically working. And if you examine the response: `{“result”: 1}`, it returns a 1, which mean that machine with these features is likely to stay healthy.

Now, lets change the input parameters and call the predict function again. Put the following values in the Input field:
```
{
  "feature": "0, 95, 0, 88, 26.62, 75, 21.05, 115, 8.65, 5, 3.32, 3"
}
```

With these input parameters, the model returns 0, which mean that the machine is likely to break. Take a note of the **AccessKey** as you will need this for lab 6.


## Lab 3 - Gateway host: setup machine sensors simulator and MQTT broker

In this lab you will run a simple Python script that simulates IoT sensor data from some hypotetical machines, and send the data to a MQTT broker, [mosquitto](https://mosquitto.org/). The gateway host is connnected to many and different type of sensors, but they generally all share the same trasport protocol, mqtt.

SSH into the VM, then  install required libs and start the mosquitto broker
```
$ yum install -y mosquitto
$ pip install paho-mqtt
$ systemctl enable mosquitto
$ systemctl start mosquitto
```

Now clone this repo into the VM where the Python script is located and run the simulator

```
$ cd ~
$ git clone https://github.com/fabiog1901/IoT-predictive-maintenance.git
$ mv IoT-predictive-maintenance/mqtt.* ~
$ python mqtt.iot_simulator.py mqtt.iot.config
```

You should see an output similar to the below:

```
TODO
```

You can stop the simulator now, with Ctrl+C.


## Lab 4 - Gateway host: install and run MiNiFi

$ tar xzvf minifi-0.6.0.1.0.0.0-54-bin.tar.gz
$ cd minifi-0.6.0.1.0.0.0-54

# download the NiFi Processor to read from mosquitto 
$ wget http://central.maven.org/maven2/org/apache/nifi/nifi-mqtt-nar/1.8.0/nifi-mqtt-nar-1.8.0.nar -P ./lib


## Lab 5 - 


## Lab 6 - 


## Lab 7 - 


## Lab 8 - 



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


## Appendix
<details>
  <summary>Resources</summary>
  
  [Cloudera Documentation](https://www.cloudera.com/documentation.html)
</details>
