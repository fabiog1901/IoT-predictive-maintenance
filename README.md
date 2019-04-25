# Cloudera Data Science Workbench

Basic tour of Cloudera Data Science Workbench (CDSW).

## Initial setup

Open the Workbench and start a Python3 Session, then run the following command to install some required libraries:
```
!pip3 install --upgrade pip dask keras matplotlib pandas_highcharts protobuf tensorflow seaborn sklearn
```

Please note: as libraries are updated, dependancies might break: please check the output log and fix the dependancies. For example, you might have to install a specific version of setuptools or numpy for tensorflow to install properly.

Start a new R Session, and run these commands:
```
install.packages('sparklyr')
install.packages('plotly')
install.packages("nycflights13")
install.packages("Lahman")
install.packages("mgcv")
install.packages('shiny') 
```

Stop and restart all sessions for changes to take effect.

Want more Experiment and Models examples? Check our [secret excercise](Experiment-and-Models.md) 
