// Author: Chamika Deshan
// Created: 2026-08-19

package com.bigdata.cw.processor.telemetry.domain.usecases

import com.bigdata.cw.processor.core.util.ILogger
import com.bigdata.cw.processor.telemetry.domain.interfaces.ITelemProcessor
import com.bigdata.cw.processor.telemetry.data.model.TelemetryRecord
import com.google.gson.Gson
import com.google.gson.JsonObject
import org.apache.flink.api.common.eventtime.WatermarkStrategy
import org.apache.flink.streaming.api.functions.windowing.ProcessWindowFunction
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows
import org.apache.flink.streaming.api.windowing.time.Time
import org.apache.flink.streaming.api.windowing.windows.TimeWindow
import org.apache.flink.util.Collector
import java.time.Duration
import java.time.Instant
import java.time.LocalDateTime
import java.time.ZoneId
import java.time.format.DateTimeFormatter

class TrackCameraTrafficTotalsUseCase(
    private val repository: ITelemProcessor,
    private val logger: ILogger
) {
    fun execute(topic: String) {
        val env = repository.getEnvironment()

        val rawStream = repository.readKafka(env, topic)

        // Flatmap -> safely ignore invalid json just in case
        val parsedStream = rawStream.flatMap { value, out: Collector<TelemetryRecord> ->
            try {
                val json = Gson().fromJson(value, JsonObject::class.java)
                val camId = json.get("camera_id")?.asString ?: "unknown"
                val tsStr = json.get("timestamp")?.asString ?: ""
                val vehCount = json.get("vehicle_count")?.asInt ?: 0

                if (tsStr.isNotEmpty()) {
                    val timeStamp = LocalDateTime.parse(tsStr)
                        .atZone(ZoneId.of("UTC"))
                        .toInstant()
                        .toEpochMilli()

                    out.collect(TelemetryRecord(camId, timeStamp, vehCount))
                }
            } catch (e: Exception) {
                // Ignore and parsedStream = 0 
            }
        }
            // Flink need to class type, or cannot find serializer 
            .returns(TelemetryRecord::class.java)

        val watermarkStrategy = WatermarkStrategy
            // 10 sec delay allow
            .forBoundedOutOfOrderness<TelemetryRecord>(Duration.ofSeconds(10))
            // watermark strategy telemetryRecord->timeStamp we set above, we set noWatermarks for env src
            .withTimestampAssigner { telemetryRecord, _ -> telemetryRecord.timeStamp }

        val watermarkedStream = parsedStream.assignTimestampsAndWatermarks(watermarkStrategy)

        val summingUp = watermarkedStream
            .keyBy { it.camId }
            // 10 min window, seconds for easy monitoring
            .window(TumblingEventTimeWindows.of(Time.minutes(10)))
            .process(object : ProcessWindowFunction<TelemetryRecord, String, String, TimeWindow>() {
                override fun process(
                    key: String,
                    context: Context,
                    elements: Iterable<TelemetryRecord>,
                    out: Collector<String>
                ) {
                    val totalVehicles = elements.sumOf { it.vehCount }
                    val eventTimestamp = elements.firstOrNull()?.timeStamp ?: context.window().start
                    out.collect(
                        """
                        {
                          "cam_id": "$key",
                          "window_start": $eventTimestamp,
                          "vehicle_count": $totalVehicles
                        }
                    """
                    )
                }
            })

        // print
        summingUp.print()

        // export data
        repository.writeSink(summingUp)

        repository.doJob(env, "Cam Traffic 10 Min Summary")
    }
}
