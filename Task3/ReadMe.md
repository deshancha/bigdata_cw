## .env

```
# spark config
SPARK_IMAGE=apache/spark:3.5.1

# spart ports
SPARK_MASTER_PORT=7077
SPARK_MASTER_UI_PORT=8080

# Res limits
SPARK_WORKER_CORES=2
SPARK_WORKER_MEMORY=2G

# local dir
DOCKERDIR=./data
SRCDIR=./src
DIDIR=./di
```

## Docker 

```
docker compose up -d
```

## Execute job Locally 

```
pip install -r requirements.txt
python src/main.py     
```

## execute job on spark cluster in docker 

```
docker exec -it spark-master /opt/spark/bin/spark-submit --master spark://spark-master:7077  /opt/spark/work-dir/src/main.py
```