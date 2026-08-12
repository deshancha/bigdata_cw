# Author: Chamika Deshan
# Created: 2026-08-12

from climate.domain.interfaces.iclimate_repository import IClimateRepository
from core.util import ILogger

class InfluxDbClimateRepositoryImp(IClimateRepository):
    def __init__(self, logger: ILogger):
        self.logger = logger

    def write_records(self, records: list) -> None:
        pass

    def close(self) -> None:
        pass