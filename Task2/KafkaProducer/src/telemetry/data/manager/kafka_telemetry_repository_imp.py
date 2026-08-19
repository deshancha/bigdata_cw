# Author: Chamika Deshan
# Created: 2026-08-18

import os
import json
import time
import random
import requests
from typing import List, Dict, Any
from datetime import datetime
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
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
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=[self.kafka_server],
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            self.logger.info("Ok connection to Kafka")
        except Exception as e:
            raise ConnectionError(f"Error conencting to broker: {e}")

    def close_producer(self) -> None:
        self.logger.info(f"closing prodcuer connection")
        self.producer.close()

    def fetch_source_data(self) -> List[Dict[str, Any]]:
        self.logger.info(f"fetching telemetry")
        try:
            response = requests.get(self.api_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.logger.info(f"Ok retrieved records from API")
                return data
        except Exception as e:
            self.logger.warn(f"Failed to fetch!")
        return []

    def send_record(self, topic: str, record: Dict[str, Any]) -> None:
        self.logger.info(f"sending record")
        
        future = self.producer.send(topic, value=record)
        # future/promise like c++ and we wait for result
        future.get(timeout=10)
