# Author: Chamika Deshan
# Created: 2026-08-22

import sys
import os

# Ensure src directory is on python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyspark.sql import SparkSession
from core.util.logger import Logger
from etl.data.manager.spark_repository import SparkRepository
from etl.domain.usecases.compute_network_metrics_usecase import ComputeNetworkMetricsUseCase

class DiContainer:
    def __init__(self):
        self._spark = (SparkSession.builder
                       .appName("ETL Process")
                       .getOrCreate())
        
        self._logger = Logger("Tsk3_Spark")
        # Initialize Repository
        self._repository = SparkRepository(self._spark, self._logger)
        
        self._usecase = ComputeNetworkMetricsUseCase(self._repository, self._logger)

    def get_spark_session(self) -> SparkSession:
        return self._spark

    def get_logger(self) -> Logger:
        return self._logger

    def get_usecase(self) -> ComputeNetworkMetricsUseCase:
        return self._usecase
