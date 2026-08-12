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
        
        self.logger.info(f"Init influx connection with: {self.url}, org: '{self.org}', bucket: '{self.bucket}'")

        # Clint
        self.client = InfluxDBClient(url=self.url, token=self.token, org=self.org)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    def write_records(self, records: list) -> None:
        self.logger.info(f"Writing batch of {len(records)} records to InfluxDB...")
        

    def delete_all_data(self) -> None:
        self.logger.info(f"Clear bucket '{self.bucket}'")
        

    def close(self) -> None:
        self.logger.info("Closing InfluxDB client connection.")
        self.client.close()
