// Author: Chamika Deshan
// Created: 2026-08-19

package com.bigdata.cw.processor

import com.bigdata.cw.processor.core.util.ConsoleLogger
import com.bigdata.cw.processor.telemetry.data.manager.FlinkTelemetryProcessorStreamApiImp
import com.bigdata.cw.processor.telemetry.domain.usecases.TrackCameraTrafficTotalsUseCase
import io.github.cdimascio.dotenv.Dotenv

class TelemetryProcessorApp {
    companion object {
        @JvmStatic
        fun main(args: Array<String>) {
            val dotenv = Dotenv.configure().ignoreIfMissing().load()
            val topic = dotenv.get("KAFKA_TOPIC", "traffic-telemetry")

            // Good to have a DI framework here when scaling up.

            val logger = ConsoleLogger("Tsk2_Flink")
            logger.info("Start Tele3metry Processor")
            // TODO: sink, database or opentelemtry(Newrelic) later
            // Ie - Avatarin -> Robot status -> disconnect measure with opentelemetry(Newrelic)
            
            val repository = FlinkTelemetryProcessorStreamApiImp(logger)

            val usecase = TrackCameraTrafficTotalsUseCase(repository, logger)

            usecase.execute(topic)
        }
    }
}
