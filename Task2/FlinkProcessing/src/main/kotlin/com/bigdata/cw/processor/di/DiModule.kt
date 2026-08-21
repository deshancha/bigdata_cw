// Author: Chamika Deshan
// Created: 2026-08-21

package com.bigdata.cw.processor.di

import com.bigdata.cw.processor.core.util.ConsoleLogger
import com.bigdata.cw.processor.core.util.ILogger
import com.bigdata.cw.processor.telemetry.data.manager.FlinkTelemetryProcessorStreamApiImp
import com.bigdata.cw.processor.telemetry.data.sink.FlinkInfluxDbSink
import com.bigdata.cw.processor.telemetry.domain.interfaces.ITelemProcessor
import com.bigdata.cw.processor.telemetry.domain.usecases.TrackCameraTrafficTotalsUseCase

// Basic DI
object DiModule {
    private val logger: ILogger = ConsoleLogger("Tsk2_Flink")

    fun getLogger(): ILogger = logger

    fun createProcessor(): ITelemProcessor {
        val sink = FlinkInfluxDbSink(logger)
        return FlinkTelemetryProcessorStreamApiImp(sink, logger)
    }

    fun createTrackCameraTrafficTotalsUseCase(): TrackCameraTrafficTotalsUseCase {
        return TrackCameraTrafficTotalsUseCase(createProcessor(), logger)
    }
}
