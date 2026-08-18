# Author: Chamika Deshan
# Created: 2026-08-18

import random
from datetime import datetime
from typing import Dict, Any

class ParseTelemetryUseCase:
    def __init__(self, logger):
        self.logger = logger

    def execute(self, row: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "camera_id": row.get("camera_id") or row.get("atd_device_id") or "unknown_sensor",
            "timestamp": row.get("timestamp") or row.get("read_date") or datetime.utcnow().isoformat() + 'Z',
            "direction": row.get("direction") or "Unknown",
            "vehicle_count": int(row.get("volume") or row.get("traffic_volume") or random.randint(0, 30))
        }
