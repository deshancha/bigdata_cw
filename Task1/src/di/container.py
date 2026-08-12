# Author: Chamika Deshan
# Created: 2026-08-12

from dependency_injector import containers, providers
from core.util import LoggerFactory, ILogger
from climate.domain.interfaces.iclimate_repository import IClimateRepository
from climate.data.manager.influxdb_climate_repository_imp import InfluxDbClimateRepositoryImp
from climate.domain.usecases.load_data_usecase import LoadDataUseCase
from climate.domain.usecases.clear_data_usecase import ClearDataUseCase
from climate.domain.usecases.close_connection_usecase import CloseConnectionUseCase

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

    load_data_usecase = providers.Factory(
        LoadDataUseCase,
        climate_repository=climate_repository,
        logger=logger
    )

    clear_data_usecase = providers.Factory(
        ClearDataUseCase,
        climate_repository=climate_repository,
        logger=logger
    )

    close_connection_usecase = providers.Factory(
        CloseConnectionUseCase,
        climate_repository=climate_repository,
        logger=logger
    )
