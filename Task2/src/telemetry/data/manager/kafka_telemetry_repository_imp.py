# Author: Chamika Deshan
# Created: 2026-08-18

import os
from typing import List, Dict, Any
from telemetry.domain.interfaces.itelemetry_repository import ITelemetryRepository

class KafkaTelemetryRepositoryImp(ITelemetryRepository):
    def __init__(self, logger):
        self.logger = logger
        self.producer = None
        self.kafka_server = f"localhost:{os.getenv('KAFKA_PORT', '29092')}"
        
        # api config from env
        api_base = os.getenv("TELEMETRY_API_URL", "https://data.austintexas.gov/resource/sh59-i6y9.json")
        api_limit = os.getenv("TELEMETRY_API_LIMIT", "1000")
        self.api_url = f"{api_base}?$limit={api_limit}"

    def connect_producer(self) -> None:
        self.logger.info(f"connecting to Kafka Broker: {self.kafka_server}")

    def close_producer(self) -> None:
        self.logger.info(f"closing prodcuer connection")

    def fetch_source_data(self) -> List[Dict[str, Any]]:
        self.logger.info(f"fetching telemetry")

    def send_record(self, topic: str, record: Dict[str, Any]) -> None:
        self.logger.info(f"sending record")
