# Author: Chamika Deshan
# Created: 2026-08-18

from dependency_injector import containers, providers
from core.util.logger import LoggerFactory
from telemetry.data.manager.kafka_telemetry_repository_imp import KafkaTelemetryRepositoryImp
from telemetry.domain.usecases.fetch_telemetry_usecase import FetchTelemetryUseCase
from telemetry.domain.usecases.parse_telemetry_usecase import ParseTelemetryUseCase
from telemetry.domain.usecases.send_telemetry_usecase import SendTelemetryUseCase

class AppContainer(containers.DeclarativeContainer):
    """
    DI Stuff
    """
    config = providers.Configuration()

    logger = providers.Singleton(
        LoggerFactory.create,
        name="Tsk2"
    )

    telemetry_repository = providers.Singleton(
        KafkaTelemetryRepositoryImp,
        logger=logger
    )

    fetch_telemetry_usecase = providers.Factory(
        FetchTelemetryUseCase,
        telemetry_repository=telemetry_repository,
        logger=logger
    )

    parse_telemetry_usecase = providers.Factory(
        ParseTelemetryUseCase,
        logger=logger
    )

    send_telemetry_usecase = providers.Factory(
        SendTelemetryUseCase,
        telemetry_repository=telemetry_repository,
        logger=logger
    )
