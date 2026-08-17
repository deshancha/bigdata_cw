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
    def delete_all_data(self) -> None:
        """clear all data"""
        pass

    @abstractmethod
    def close(self) -> None:
        """close connection"""
        pass
