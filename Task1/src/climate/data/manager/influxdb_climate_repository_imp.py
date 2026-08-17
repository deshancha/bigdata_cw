# Author: Chamika Deshan
# Created: 2026-08-12

import os
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from climate.domain.interfaces.iclimate_repository import IClimateRepository
from core.util import ILogger

class InfluxDbClimateRepositoryImp(IClimateRepository):
    def __init__(self, logger: ILogger):
        self.logger = logger
        
        # from env var
        self.port = os.environ.get("INFLUXDB_PORT", "8086")
        self.token = os.environ.get("INFLUXDB_TOKEN")
        self.org = os.environ.get("INFLUXDB_ORG")
        self.bucket = os.environ.get("INFLUXDB_BUCKET")
        self.url = f"http://localhost:{self.port}"
        
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
                point = Point("fairbanks_weather")
                rec_station = rec.get("STATION")
                rec_name = rec.get("NAME")
                point.tag("station", rec_station)
                point.tag("name", rec_name)
                
                # record to point mapping
                if rec.get("PRCP"): point.field("prcp", float(rec["PRCP"]))
                if rec.get("SNOW"): point.field("snow", float(rec["SNOW"]))
                if rec.get("SNWD"): point.field("snwd", float(rec["SNWD"]))
                if rec.get("TMAX"): point.field("tmax", float(rec["TMAX"]))
                if rec.get("TMIN"): point.field("tmin", float(rec["TMIN"]))
                if rec.get("TAVG"): point.field("tavg", float(rec["TAVG"]))
                if rec.get("AWND"): point.field("awnd", float(rec["AWND"]))
                
                # Set timestamp and add point
                date_str = rec.get("DATE")
                point.time(date_str, WritePrecision.S)
                points.append(point)
            except Exception as e:
                self.logger.error(f"Failed to parse row: {rec}. Error: {str(e)}")
        
        if points:
            try:
                self.write_api.write(bucket=self.bucket, org=self.org, record=points)
                self.logger.info(f"Successfully wrote {len(points)} points to InfluxDB.")
            except Exception as e:
                self.logger.error(f"Error writing batch: {str(e)}")

    def delete_all_data(self) -> None:
        self.logger.info(f"Clear bucket '{self.bucket}'")
        

    def close(self) -> None:
        self.logger.info("Closing InfluxDB client connection.")
        self.client.close()
