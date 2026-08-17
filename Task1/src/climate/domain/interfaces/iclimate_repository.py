# Author: Chamika Deshan
# Created: 2026-08-12

from abc import ABC, abstractmethod

class IClimateRepository(ABC):
    @abstractmethod
    def open(self) -> None:
        """open connection"""
        pass

    @abstractmethod
    def write_records(self, records: list) -> None:
        """write to influx"""
        pass

    @abstractmethod
    def drop_bucket(self) -> None:
        """drop bucket"""
        pass

    @abstractmethod
    def create_bucket(self) -> None:
        """create bucket"""
        pass

    @abstractmethod
    def close(self) -> None:
        """close connection"""
        pass
