# Author: Chamika Deshan
# Created: 2026-08-18

from datetime import datetime
from typing import Dict, Any

class ParseTelemetryUseCase:
    def __init__(self, logger):
        self.logger = logger

    def execute(self, row: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "camera_id": row.get("atd_device_id", "unknown_sensor"),
            "timestamp": row.get("read_date", datetime.utcnow().isoformat() + 'Z'),
            "direction": row.get("direction", "Unknown"),
            "vehicle_count": int(row.get("volume", 0))
        }
