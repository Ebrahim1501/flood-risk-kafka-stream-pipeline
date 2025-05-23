## About this project :
This project is a custom implementation of Apache Kafka Streams to build a robust and scalable real-time data pipeline for monitoring and analyzing flood incidents. The system enables live visualization and logging of incoming flood warnings, as well as real-time metric measurements from various monitoring stations across high-risk areas.

The pipeline ingests and processes streamed data from both flood alert sources and station-based sensors, generating a unified analytical model. This model can be leveraged by analytics teams or integrated into machine learning workflows to enhance flood predictability and risk assessment in the future.

The architecture combines local and cloud-based compute instances to run producers, consumers, and the primary Kafka broker.



###  Key Features :
- **Live visualization and logging** of flood warnings.
- **Real-time metric measurements** from monitoring stations in high-risk areas.
- **Stream ingestion and processing** from multiple endpoints including alerts api and sensor-based station readings.
- Generates a **unified analytical data model** for downstream use.


###  Architecture Overview :
![Architecture](https://github.com/user-attachments/assets/50b5447b-d4ef-4eb5-8bad-eafcb5d309f6)




### Repository Structure :

.
├── .gitignore
├── docker-compose.yml
├── broker-cmds.txt
├── utils.py
├── warnings-producer.py
├── stations-measures-producer.py
├── analytics-consumer.py
└── webserver-warnings-consumer.py



