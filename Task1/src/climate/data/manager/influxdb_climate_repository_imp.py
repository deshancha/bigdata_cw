# Author: Chamika Deshan
# Created: 2026-08-12

import os
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from climate.domain.interfaces.iclimate_repository import IClimateRepository
from core.util import ILogger

class WeatherFields:
    # comn
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    WIND_SPEED = "wind_speed"
    VISIBILITY = "visibility"
    PRESSURE = "pressure"
    # Szeged only
    APPARENT_TEMPERATURE = "apparent_temperature"
    WIND_BEARING = "wind_bearing"
    # Weather data only
    DEW_POINT_TEMPERATURE = "dew_point_temperature"
    
    

class InfluxDbClimateRepositoryImp(IClimateRepository):
    def __init__(self, logger: ILogger):
        self.logger = logger
        
        # from env var
        self.host = os.environ.get("INFLUXDB_HOST", "localhost")
        self.port = os.environ.get("INFLUXDB_PORT", "8086")
        self.token = os.environ.get("INFLUXDB_TOKEN")
        self.org = os.environ.get("INFLUXDB_ORG")
        self.bucket = os.environ.get("INFLUXDB_BUCKET")
        self.measurement_szeged = os.environ.get("INFLUXDB_MEASUREMENT_SZEGED", "szeged_weather")
        self.measurement_weather = os.environ.get("INFLUXDB_MEASUREMENT_WEATHER", "weather_data")
        self.url = f"http://{self.host}:{self.port}"
        
        self.client = None
        self.write_api = None

    def open(self) -> None:
        self.logger.info(f"Opening influx connection with: {self.url}, org: '{self.org}', bucket: '{self.bucket}'")
        self.client = InfluxDBClient(url=self.url, token=self.token, org=self.org, timeout=30000)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    def write_records(self, records: list) -> None:
        self.logger.info(f"Writing batch of {len(records)} records to InfluxDB...")
        points = []
        
        for rec in records:
            try:
                #  Szeged has Formatted Date
                if "Formatted Date" in rec:
                    point = Point(self.measurement_szeged)
                    
                    # Tags
                    if rec.get("Summary"): point.tag("summary", rec.get("Summary"))
                    if rec.get("Precip Type"): point.tag("precip_type", rec.get("Precip Type"))
                    
                    # Fields
                    if rec.get("Temperature (C)"): point.field(WeatherFields.TEMPERATURE, float(rec["Temperature (C)"]))
                    if rec.get("Apparent Temperature (C)"): point.field(WeatherFields.APPARENT_TEMPERATURE, float(rec["Apparent Temperature (C)"]))
                    if rec.get("Humidity"): point.field(WeatherFields.HUMIDITY, float(rec["Humidity"]))
                    if rec.get("Wind Speed (km/h)"): point.field(WeatherFields.WIND_SPEED, float(rec["Wind Speed (km/h)"]))
                    if rec.get("Wind Bearing (degrees)"): point.field(WeatherFields.WIND_BEARING, float(rec["Wind Bearing (degrees)"]))
                    if rec.get("Visibility (km)"): point.field(WeatherFields.VISIBILITY, float(rec["Visibility (km)"]))
                    if rec.get("Pressure (millibars)"): point.field(WeatherFields.PRESSURE, float(rec["Pressure (millibars)"]))

                    # 2006-04-01 00:00:00.000 +0200
                    date_str = rec.get("Formatted Date")
                    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f %z")
                    point.time(dt, WritePrecision.S)
                    points.append(point)

                # Weather Dataset has Date/Time
                elif "Date/Time" in rec:
                    point = Point(self.measurement_weather)
                    
                    # Tags
                    if rec.get("Weather"): point.tag("weather", rec.get("Weather"))
                    
                    # Fields
                    if rec.get("Temp_C"): point.field(WeatherFields.TEMPERATURE, float(rec["Temp_C"]))
                    if rec.get("Dew Point Temp_C"): point.field(WeatherFields.DEW_POINT_TEMPERATURE, float(rec["Dew Point Temp_C"]))
                    if rec.get("Rel Hum_%"): point.field(WeatherFields.HUMIDITY, float(rec["Rel Hum_%"]))
                    if rec.get("Wind Speed_km/h"): point.field(WeatherFields.WIND_SPEED, float(rec["Wind Speed_km/h"]))
                    if rec.get("Visibility_km"): point.field(WeatherFields.VISIBILITY, float(rec["Visibility_km"]))
                    if rec.get("Press_kPa"): point.field(WeatherFields.PRESSURE, float(rec["Press_kPa"]))

                    date_str = rec.get("Date/Time")
                    # 1/1/2012 0:00
                    dt = None
                    for fmt in ("%m/%d/%Y %H:%M", "%d/%m/%Y %H:%M", "%Y-%m-%d %H:%M:%S"):
                        try:
                            dt = datetime.strptime(date_str, fmt)
                            break
                        except ValueError:
                            pass
                    
                    if dt:
                        point.time(dt, WritePrecision.S)
                        points.append(point)
                    else:
                        self.logger.error(f"Failed to parse datetime format: {date_str}")
            except Exception as e:
                self.logger.error(f"Failed to parse row: {rec}. Error: {str(e)}")
        
        if points:
            try:
                self.write_api.write(bucket=self.bucket, org=self.org, record=points)
                self.logger.info(f"Ok wrote {len(points)} points to InfluxDB.")
            except Exception as e:
                self.logger.error(f"Error writing batch: {str(e)}")

    def drop_bucket(self) -> None:
        self.logger.info(f"Dropping Influxdb bucket: '{self.bucket}'")
        try:
            buckets_api = self.client.buckets_api()
            bucket_obj = buckets_api.find_bucket_by_name(self.bucket)
            if bucket_obj:
                buckets_api.delete_bucket(bucket_obj.id)
                self.logger.info(f"Ok dropped bucket: '{self.bucket}'.")
            else:
                self.logger.warn(f"Bucket :'{self.bucket}' not exist")
        except Exception as e:
            self.logger.error(f"Failed to drop bucket :'{self.bucket}': {str(e)}")

    def create_bucket(self) -> None:
        self.logger.info(f"Creating Influx bucket: '{self.bucket}'")
        try:
            buckets_api = self.client.buckets_api()
            
            org_api = self.client.organizations_api()
            orgs = org_api.find_organizations(org=self.org)
            if orgs:
                org_id = orgs[0].id
                buckets_api.create_bucket(bucket_name=self.bucket, org_id=org_id)
                self.logger.info(f"Ok created bucket '{self.bucket}'.")
            else:
                buckets_api.create_bucket(bucket_name=self.bucket, org=self.org)
                self.logger.info(f"Ok created bucket: '{self.bucket}' using org name.")
        except Exception as e:
            self.logger.error(f"Failed to create bucket '{self.bucket}': {str(e)}")

    def close(self) -> None:
        self.logger.info("Closing Influx client connection.")
        self.client.close()
