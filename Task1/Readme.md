
## .env

```
DOCKERDIR=./influxdb_data
INFLUXDB_PORT=8086
INFLUXDB_ADMIN_USER=admin
INFLUXDB_ADMIN_PASSWORD=xxxx
INFLUXDB_ORG=bigdata_cw
INFLUXDB_BUCKET=fairbanks_climate_data
# admin Token for external apis
INFLUXDB_TOKEN=xxxxxxxx
```

## docker compose up

```
docker compose up -d
```

## Add records 

```
python3 Task1/src/main.py 0
```

## Delete all data 

```
python3 Task1/src/main.py -1
```