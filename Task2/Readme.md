
## .env

```
# Flink
FLINK_PORT=8081
# 1 slot(worker thread) -> if many logs could be messy for explanation
FLINK_TASK_SLOTS=1
FLINK_VERSION=1.18.1

# Kafka
KAFKA_PORT=29092
KAFKA_UI_PORT=8080
KAFKA_TOPIC=traffic-telemetry


# Producer
TELEMETRY_API_URL=https://data.austintexas.gov/resource/sh59-i6y9.json
TELEMETRY_API_LIMIT=1000
LOG_ENABLED=1
```

## docker compose up
- Kafka UI - http://localhost:8081
- Flink UI - http://localhost:8080

```
docker compose up -d
```

## kafka producer 
```
source .venv/bin/activate
cd Task2/KafkaProducer 
python src/main.py
```

## Flink Processor
### This would build jar, copy to docker with .env and jobmanager
```
cd Task2/FlinkProcessing 
gradle deployToDocker
```

## See output 

```
docker logs task2-taskmanager > taskmanager_output.log
```