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



### Run SparkStreaming Job

$ PUBLIC_IP=`dig +short myip.opendns.com @resolver1.opendns.com`
$ sed -i "s/YourHostname/`hostname -f`/" spark_streaming.py
$ sed -i "s/YourCDSWDomain/cdsw.$PUBLIC_IP.nip.io/" spark_streaming.py
$ wget  http://central.maven.org/maven2/org/apache/kudu/kudu-spark2_2.11/1.9.0/kudu-spark2_2.11-1.9.0.jar
$ wget https://raw.githubusercontent.com/swordsmanliu/SparkStreamingHbase/master/lib/spark-core_2.11-1.5.2.logging.jar
$ rm -rf ~/.m2 ~/.ivy2/
$ mv ~/mock-data-generator/sparkstreamingkudu.py ~
$ spark-submit --master local[2] --jars kudu-spark2_2.11-1.9.0.jar,spark-core_2.11-1.5.2.logging.jar --packages org.apache.spark:spark-streaming-kafka_2.11:1.6.3 sparkstreamingkudu.py


