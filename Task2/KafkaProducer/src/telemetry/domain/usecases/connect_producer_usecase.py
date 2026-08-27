# Author: Chamika Deshan
# Created: 2026-08-27

from telemetry.domain.interfaces.itelemetry_repository import ITelemetryRepository
from core.util.logger import ILogger

class ConnectProducerUseCase:
    def __init__(self, telemetry_repository: ITelemetryRepository, logger: ILogger):
        self.repository = telemetry_repository
        self.logger = logger

    def execute(self) -> None:
        self.logger.info("connecting producer")
        self.repository.connect_producer()
