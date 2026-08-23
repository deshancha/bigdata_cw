# Author: Chamika Deshan
# Created: 2026-08-23

from abc import ABC, abstractmethod
from pyspark.sql import DataFrame

class IEtlManager(ABC):
    
    @abstractmethod
    def load_data(self, file_path: str) -> DataFrame:
        pass

    @abstractmethod
    def count_incoming_links(self, df: DataFrame) -> DataFrame:
        pass

    @abstractmethod
    def sort_records(self, df: DataFrame, limit: int = 50) -> DataFrame:
        pass
