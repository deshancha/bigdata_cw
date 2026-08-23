# Author: Chamika Deshan
# Created: 2026-08-23

from pyspark.sql import SparkSession, DataFrame
from etl.domain.manager.ietl_manager import IEtlManager
from pyspark.sql.functions import split, col

class SparkRepository(IEtlManager):
    
    def __init__(self, spark: SparkSession):
        self.spark = spark

    def load_data(self, file_path: str) -> DataFrame:
        raw_df = self.spark.read.text(file_path)
        
        # filter start with #
        filtered_df = raw_df.filter(~col("value").startswith("#"))
        
        # split -> spaces or tabs
        split_col = split(col("value"), r"\s+")
        
        return (filtered_df.select(
            split_col.getItem(0).cast("int").alias("from_node"),
            split_col.getItem(1).cast("int").alias("to_node")
        ))

    def count_incoming_links(self, df: DataFrame) -> DataFrame:
        pass

    def sort_records(self, df: DataFrame, limit: int = 50) -> DataFrame:
        pass
