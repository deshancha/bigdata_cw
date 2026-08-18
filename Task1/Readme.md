
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

## Window Aggregation to compute sliding hourly averages across an extended observation span;
### Window Aggregation (Szeged Temperature Hourly Avg)

```
from(bucket: "fairbanks_climate_data")
  // Szeged Dat Range
  |> range(start: 2006-01-01T00:00:00Z, stop: 2016-12-31T23:59:59Z)
  |> filter(fn: (r) => r["_measurement"] == "szeged_weather")
  |> filter(fn: (r) => r["_field"] == "temperature")
  // Groups to 1 hr window and get average
  |> aggregateWindow(every: 1h, fn: mean)
```

## Anomaly Isolation filters to capture observations exceeding two standard deviations from the dataset mean

```
data = from(bucket: "fairbanks_climate_data")
  |> range(start: 2012-01-01T00:00:00Z, stop: 2012-12-31T23:59:59Z)
  |> filter(fn: (r) => r["_measurement"] == "weather_data")
  |> filter(fn: (r) => r["_field"] == "temperature")
// find mean and std
mean = (data |> mean() |> findRecord(fn: (key) => true, idx: 0))._value
std = (data |> stddev() |> findRecord(fn: (key) => true, idx: 0))._value
meanPlusTwo = mean + 2.0 * std
meanMinusTwo = mean - 2.0 * std
// Filter mean +-2 anomalies
data
  |> filter(fn: (r) => r._value > (meanPlusTwo) or r._value < (meanMinusTwo))
```

## Downsampling tasks that continuously summarize historical data into an auxiliary bucket governed by an explicit 30-day retention rule
### Task runs every day, calc daily avg of hourly records, save in downsampled bucket

```
option task = {name: "Daily Weather Downsampling Task", every: 1d, offset: 1h}

from(bucket: "fairbanks_climate_data")
    // Get data from last day
    |> range(start: -1d)
    |> filter(fn: (r) => r["_measurement"] == "szeged_weather")
    // group hourly data to daily avg
    |> aggregateWindow(every: 1d, fn: mean)
    // Write to  30 day auxialry bucket
    |> to(bucket: "weather_data_downsampled")

```