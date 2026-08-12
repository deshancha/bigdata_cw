# Author: Chamika Deshan
# Created: 2026-08-12

from climate.domain.interfaces.iclimate_repository import IClimateRepository
from core.util import ILogger

class ClearDataUseCase:
    def __init__(self, climate_repository: IClimateRepository, logger: ILogger):
        self.climate_repository = climate_repository
        self.logger = logger

    def execute(self) -> None:
        self.logger.info("clear data usecase")
        self.climate_repository.delete_all_data()
