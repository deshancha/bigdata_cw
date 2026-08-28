# Author: Chamika Deshan
# Created: 2026-08-18

from typing import List, Dict, Any
from telemetry.domain.interfaces.itelemetry_repository import ITelemetryRepository

class FetchTelemetryUseCase:
    def __init__(self, telemetry_repository: ITelemetryRepository, logger):
        self.repository = telemetry_repository
        self.logger = logger

    def execute(self) -> List[Dict[str, Any]]:
        self.logger.info("Fetch Telemetry Use Case")
        return self.repository.fetch_source_data()
