# Author: Chamika Deshan
# Created: 2026-08-27

from typing import Iterable, Dict
from climate.domain.interfaces.iclimate_repository import IClimateRepository
from core.util import ILogger

class WriteRecordsUseCase:
    def __init__(self, climate_repository: IClimateRepository, logger: ILogger):
        self.climate_repository = climate_repository
        self.logger = logger

    def execute(self, records: Iterable[Dict[str, str]]) -> None:
        try:
            batch = []
            total_records = 0

            for row in records:
                batch.append(row)
                if len(batch) >= 1000:
                    self.climate_repository.write_records(batch)
                    total_records += len(batch)
                    batch = []

            # write remaining records
            if batch:
                self.climate_repository.write_records(batch)
                total_records += len(batch)

            self.logger.info(f"Ok adding records of :{total_records}")
        except Exception as e:
            self.logger.error(f"Error adding records: {e}")
