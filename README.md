# IoT Platform

## Description

This project represents a microservice app that collects, stores and visualizes IoT data. It is organised into 4 microservices:
- mqtt: the broker that uses the eclipse-mosquitto docker image to send data
- adapter: an adapter written in python that subscribes to the broker.
- database: container with influxdb database
- graph: for data visualization

The broker sends data on various topics. The adapter connects to the broker and listenes to the messages. If they have the correct format, then the data is processed and stored into the database container which uses influxdb.
The grafana container connects to the database and uses two dashboards to view the inserted data.

## 1 Miscellaneous files

In the stack.yml file I defined the services used.

To run the theme, the run.sh script that builds a container will be called.
for the adapter, initialize docker swarn and then build the service stack.

To stop and clean the service stack, the clean.sh script will be called.

The containers are configured to communicate only within the defined networks, as specified in the statement.

## 2 The mqtt broker

It is configured to listen on port 1883, without authentication, and allow
anonymous connections.

## 3 The adapter

The adapter implementation is in the code/ folder. It is written in python and run from inside a container. The Dockerfile starts from the python image, installs the necessary packages and copies the source code into the container, and then runs the source code.

The adapter (adapter.py file) creates the database called "iot_db", then builds the mqtt client and subscribes to the "#" topic. When it receives a message, it checks if the topic is valid, in which case it proceeds to processing the message.

The adapter is configured to print logging messages if the DEBUG_DATA_FLOW value is True. (passed through a configuration file, adapter.env).

The first time the timestamp is extracted from the message (if it exists), then the fields with integer values are extracted and the json that will be sent to the database is built. If there is no timestamp, the current timestamp is used.

## 4 Database

For the database I used influxdb 1, which allows easier configuration compared to influxdb 2. The database created in influxdb will be called "iot_db" and it is configured to listen on port 8086 (default). For data storage we used a docker volume.

## 5 Grafana

To view the data I used grafana, which is configured to listen on port 80. In order to view the data, the influxdb data source (datasources.yml file) must be added, with the name "iot_db" and the url "http://database :8086".

Then I created 2 dashboards, one for location and one for battery level. The dashboards are persistently stored in the grafana/dashboards folder and are mounted in the grafana container.

Regarding the authentication credentials, I used the configuration file grafana.env in which I set the username and password.