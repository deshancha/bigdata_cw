# Author: Chamika Deshan
# Created: 2026-08-18

from abc import ABC, abstractmethod
from typing import List, Dict, Any

class ITelemetryRepository(ABC):
    @abstractmethod
    def connect_producer(self) -> None:
        """Init kafka broker connection"""
        pass

    @abstractmethod
    def close_producer(self) -> None:
        """Closes connection"""
        pass

    @abstractmethod
    def fetch_source_data(self) -> List[Dict[str, Any]]:
        """Fetches telemetry data from api"""
        pass

    @abstractmethod
    def send_record(self, topic: str, record: Dict[str, Any]) -> None:
        """Send telemetry record to Kafka"""
        pass
