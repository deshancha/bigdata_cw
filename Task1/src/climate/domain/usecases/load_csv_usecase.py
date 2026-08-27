# Author: Chamika Deshan
# Created: 2026-08-12

import csv
import os
from typing import Generator, Dict
from core.util import ILogger

class LoadCsvUseCase:
    def __init__(self, logger: ILogger):
        self.logger = logger

    def execute(self, csv_file_path: str) -> Generator[Dict[str, str], None, None]:
        self.logger.info(f"loading csv: {csv_file_path}")

        if not os.path.exists(csv_file_path):
            self.logger.error(f"csv not found: {csv_file_path}")
            return

        try:
            with open(csv_file_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                yield from reader
        except Exception as e:
            self.logger.error(f"Error loading csv: {e}")
