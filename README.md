## About this project :
This project is a custom implementation of Apache Kafka Streams to build a robust and scalable real-time data pipeline for monitoring and analyzing flood incidents. The system enables live visualization and logging of incoming flood warnings, as well as real-time metric measurements from various monitoring stations across high-risk areas.

The pipeline ingests and processes streamed data from both flood alert sources and station-based sensors, generating a unified analytical model. This model can be leveraged by analytics teams or integrated into machine learning workflows to enhance flood predictability and risk assessment in the future.

The architecture combines local and cloud-based compute instances to run producers, consumers, and the primary Kafka broker.

**Web Page Snapshot Samples :**


![floodriskguisample3](https://github.com/user-attachments/assets/fbecbf87-c0db-462b-a22c-a3230398add2)
![FloodWarningsGUIsample](https://github.com/user-attachments/assets/ce1ce44d-8eba-47f9-b1b7-edd5e775e6d2)
![FloodWarningSample2](https://github.com/user-attachments/assets/7d18c848-d477-4058-affe-dc41e309e5f0)



###  Key Features :
- **Live visualization and logging** of flood warnings.
- **Real-time metric measurements** from monitoring stations in high-risk areas.
- **Stream ingestion and processing** from multiple endpoints including alerts api and sensor-based station readings.
- Generates a **unified analytical data model** for downstream use.


###  Architecture Overview :
![Architecture](https://github.com/user-attachments/assets/50b5447b-d4ef-4eb5-8bad-eafcb5d309f6)
#### Key Components
- **Kafka Broker:**  
  A centrally hosted EC2 instance in the cloud that acts as a message broker, receiving and streaming data from producers to consumers. It hosts two main topics:
  - `Flood-Warnings-topic`
  - `Station-metrics-topic`  
  Both topics are internally partitioned to support parallel workload handling.

- **🚨 Flood Warnings Producer:**  
  An EC2 instance responsible for capturing real-time warning data from a streaming API and publishing it to the `Flood-Warnings-topic` on the Kafka broker.

- **📊 Station Metrics Producer:**  
  A component that captures real-time measurements from various flood monitoring stations and publishes the data to the `Station-metrics-topic`.

- **🌍 Web Server Consumer Group:**  
  A set of Flask-based local servers that consume data from the `Flood-Warnings-topic`. These servers visualize the incoming data on a real-time map using GeoJSON location data provided by the API.

- **📈 Analytics Consumer Instance:**  
  One or more EC2 instances that consume data from both the warnings and station metrics streams. These instances perform data processing, joining, and aggregation to generate analytical insights that highlight relationships between flood severity and station measurements.



### Repository Structure :
```

.
├── .gitignore 
├── docker-compose.yml
├── broker-cmds.txt
├── utils.py
├── warnings-producer.py
├── stations-measures-producer.py
├── analytics-consumer.py
└── webserver-warnings-consumer.py

```

####  File Descriptions

- **`docker-compose.yml`**  
  A Docker Compose file for quickly setting up and running Kafka on a local or cloud server. *(Remember to configure it with your actual Kafka server/instance connection info.)*


- **`broker-cmds.txt`**  
  Contains shell commands to create and configure Kafka topics and partitions inside the broker.


- **`utils.py`**  
  A utility script containing reusable global functions and helper methods shared across producers and consumers.


- **`warnings-producer.py`**  
  A Kafka producer script that runs on your producer instance to ingest live flood warning data from an external API and publish it to the `Flood-Warnings-topic`.


- **`stations-measures-producer.py`**  
  Captures real-time sensor measurements from all monitoring stations and sends the data to the `Station-metrics-topic`.


- **`webserver-warnings-consumer.py`**  
  A Flask-based backend server that visualizes flood warnings in real time using geographic data (e.g., GeoJSON) streamed from Kafka.


- **`analytics-consumer.py`**  
  A Kafka consumer script (typically running on an EC2 instance) that processes and joins data from both topics, performing aggregation and saving the results as CSV files for analytical modeling.
