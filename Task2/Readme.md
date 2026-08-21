
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

# InfluxDB Configuration
DOCKERDIR=./influxdb_data
INFLUXDB_HOST=localhost
INFLUXDB_PORT=8086
INFLUXDB_ADMIN_USER=admin
INFLUXDB_ADMIN_PASSWORD=Password1234
INFLUXDB_ORG=bigdata_cw
INFLUXDB_BUCKET=traffic_data
INFLUXDB_TOKEN=api-token
```

```
source .venv/bin/activate
```

## docker compose up
- Kafka UI - http://localhost:8081
- Flink UI - http://localhost:8080
- InfluxDB UI - http://localhost:8087/

```
docker compose down -v
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


## drop traffic data in influx db 
```
docker exec task2-influxdb influx delete --bucket traffic_data --start 2019-01-01T00:00:00Z --stop 2029-01-01T00:00:00Z --token api-token --org bigdata_cw
```

Influx Query
```
from(bucket: "traffic_data")
  |> range(start: 2019-12-31T08:30:00Z, stop: 2019-12-31T11:50:00Z) 
  |> filter(fn: (r) => r["_measurement"] == "camera_traffic")
  |> filter(fn: (r) => r["_field"] == "vehicle_count")

```

Dcoker 
```
docker exec task2-influxdb influx query \
  'from(bucket:"traffic_data") 
   |> range(start: 2019-11-10T12:00:00Z, stop: 2019-11-10T13:00:00Z) 
   |> filter(fn: (r) => r.cam_id == "6353")' \
  --token api-token \
  --org bigdata_cw
```