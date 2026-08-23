# Author: Chamika Deshan
# Created: 2026-08-23

from pyspark.sql import SparkSession, DataFrame
from etl.domain.manager.ietl_manager import IEtlManager

class SparkRepository(IEtlManager):
    
    def __init__(self, spark: SparkSession):
        self.spark = spark

    def load_data(self, file_path: str) -> DataFrame:
        pass

    def count_incoming_links(self, df: DataFrame) -> DataFrame:
        pass

    def sort_records(self, df: DataFrame, limit: int = 50) -> DataFrame:
        pass
