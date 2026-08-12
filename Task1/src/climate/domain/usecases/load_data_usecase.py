# Author: Chamika Deshan
# Created: 2026-08-12

from climate.domain.interfaces.iclimate_repository import IClimateRepository
from core.util import ILogger

class LoadDataUseCase:
    def __init__(self, climate_repository: IClimateRepository, logger: ILogger):
        self.climate_repository = climate_repository
        self.logger = logger

    def execute(self, csv_file_path: str, batch_size: int = 1000) -> None:
        self.logger.info(f"Climate data adding staryed...")
