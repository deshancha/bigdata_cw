
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

## source 
```
source .venv/bin/activate
```

## Drop all

```
python3 Task1/src/main.py -1
```

## create 

```
python3 Task1/src/main.py 0
```

## add all (1000 pertime) 

```
python3 Task1/src/main.py 0
```