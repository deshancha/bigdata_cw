# Author: Chamika Deshan
# Created: 2026-08-12

import csv
import os
from climate.domain.interfaces.iclimate_repository import IClimateRepository
from core.util import ILogger

class LoadDataUseCase:
    def __init__(self, climate_repository: IClimateRepository, logger: ILogger):
        self.climate_repository = climate_repository
        self.logger = logger

    def execute(self, csv_file_path: str) -> None:
        self.logger.info(f"data adding...")
        
        if not os.path.exists(csv_file_path):
            self.logger.error(f"CSV not found: {csv_file_path}")
            return

        try:
            with open(csv_file_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                batch = []
                total_records = 0
                
                for row in reader:
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
            self.logger.error(f"Error adding recrods: {str(e)}")
        finally:
            # finally we close always the con
            self.climate_repository.close()
