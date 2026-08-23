# Author: Chamika Deshan
# Created: 2026-08-23

from pyspark.sql import SparkSession, DataFrame
from etl.domain.manager.ietl_manager import IEtlManager
from pyspark.sql.functions import split, col
from core.util.logger import Logger

class SparkRepository(IEtlManager):
    
    def __init__(self, spark: SparkSession, logger: Logger):
        self.spark = spark
        self.logger = logger

    def load_data(self, file_path: str) -> DataFrame:
        raw_df = self.spark.read.text(file_path)

        # filter start with #
        filtered_df = raw_df.filter(~col("value").startswith("#"))
        
        # Edges check just to confirm
        # do not put before filter it would add 4 more (7600595)
        total_edges = filtered_df.count()
        self.logger.info(f"Total Edges: {total_edges}")
        
        # split -> spaces or tabs
        split_col = split(col("value"), r"\s+")
        
        return (filtered_df.select(
            split_col.getItem(0).cast("int").alias("from_node"),
            split_col.getItem(1).cast("int").alias("to_node")
        ))

    def count_incoming_links(self, df: DataFrame) -> DataFrame:
        # group -> to_node for counting
        count_df = df.groupBy("to_node").count()
        
        # Read from RAM if exist, like below read top 50
        count_df.cache()
        return count_df
 
    def sort_records(self, df: DataFrame, limit: int = 50) -> DataFrame:
        pass
