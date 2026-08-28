# Author: Chamika Deshan
# Created: 2026-08-17

from climate.domain.interfaces.iclimate_repository import IClimateRepository
from core.util import ILogger

class OpenConnectionUseCase:
    def __init__(self, climate_repository: IClimateRepository, logger: ILogger):
        self.climate_repository = climate_repository
        self.logger = logger

    def execute(self) -> None:
        self.logger.info("open con")
        self.climate_repository.open()
