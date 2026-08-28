# Author: Chamika Deshan
# Created: 2026-08-18

from typing import Dict, Any
from telemetry.domain.interfaces.itelemetry_repository import ITelemetryRepository

class SendTelemetryUseCase:
    def __init__(self, telemetry_repository: ITelemetryRepository, logger):
        self.repository = telemetry_repository
        self.logger = logger

    def execute(self, topic: str, record: Dict[str, Any]) -> None:
        self.repository.send_record(topic, record)
