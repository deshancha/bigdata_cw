# Author: Chamika Deshan
# Created: 2026-08-22

import time
from core.util.logger import Logger
from etl.domain.manager.ietl_manager import IEtlManager

class ComputeNetworkMetricsUseCase:
    
    def __init__(self, repository: IEtlManager, logger: Logger):
        self.repository = repository
        self.logger = logger

    def execute(self, file_path: str):
        self.logger.info("Starting ETL")
        
        self.logger.info(f"Loading dataset from: {file_path}")
        raw_df = self.repository.load_data(file_path)
        self.logger.info("Dataset loaded!")
        
        
