# Author: Chamika Deshan
# Created: 2026-08-12

from dependency_injector import containers, providers
from core.util import LoggerFactory, ILogger
from climate.domain.interfaces.iclimate_repository import IClimateRepository
from climate.data.manager.influxdb_climate_repository_imp import InfluxDbClimateRepositoryImp

class AppContainer(containers.DeclarativeContainer):
    """
    DI container
    """
    config = providers.Configuration()

    logger: providers.Provider[ILogger] = providers.Singleton(
        LoggerFactory.create,
        logger_type="console",
        name="Tsk1"
    )

    climate_repository: providers.Provider[IClimateRepository] = providers.Singleton(
        InfluxDbClimateRepositoryImp,
        logger=logger
    )
