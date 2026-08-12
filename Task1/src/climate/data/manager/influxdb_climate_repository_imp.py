# Author: Chamika Deshan
# Created: 2026-08-12

import os
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

    def write_records(self, records: list) -> None:
        self.logger.info("writting data to influx...")

    def close(self) -> None:
        self.logger.info("close connection")
