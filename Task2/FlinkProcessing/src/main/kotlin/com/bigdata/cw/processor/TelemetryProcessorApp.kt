// Author: Chamika Deshan
// Created: 2026-08-19

package com.bigdata.cw.processor

import com.bigdata.cw.processor.di.DiModule
import io.github.cdimascio.dotenv.Dotenv

class TelemetryProcessorApp {
    companion object {
        @JvmStatic
        fun main(args: Array<String>) {
            val dotenv = Dotenv.configure().ignoreIfMissing().load()
            val topic = dotenv.get("KAFKA_TOPIC", "traffic-telemetry")

            val logger = DiModule.getLogger()
            logger.info("Start Tele3metry Processor")
            // TODO: sink, database or opentelemtry(Newrelic) later
            // Ie - Avatarin -> Robot status -> disconnect measure with opentelemetry(Newrelic)

            val usecase = DiModule.createTrackCameraTrafficTotalsUseCase()

            usecase.execute(topic)
        }
    }
}
