// Author: Chamika Deshan
// Created: 2026-08-19

package com.bigdata.cw.processor.telemetry.data.manager

import com.bigdata.cw.processor.core.util.ILogger
import com.bigdata.cw.processor.telemetry.domain.interfaces.ITelemProcessor
import org.apache.flink.api.common.eventtime.WatermarkStrategy
import org.apache.flink.api.common.serialization.SimpleStringSchema
import org.apache.flink.connector.kafka.source.KafkaSource
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer
import org.apache.flink.streaming.api.datastream.DataStream
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment

// TODO: ITelemProcessor imp with Table API, may be later
class FlinkTelemetryProcessorStreamApiImp(private val logger: ILogger) : ITelemProcessor {

    override fun getEnvironment(): StreamExecutionEnvironment {
        logger.info("Init flink StreamExecutionEnvironment")
        val env = StreamExecutionEnvironment.getExecutionEnvironment()
        // env.parallelism = 1, not need we use FLINK_TASK_SLOTS=1 in .env

        return env
    }

    override fun readKafka(env: StreamExecutionEnvironment, topic: String): DataStream<String> {
        logger.info("Set Kafka src, topic: '$topic'")
        val kafkaSource = KafkaSource.builder<String>()
            .setBootstrapServers("kafka-label:9092")
            .setTopics(topic)
            .setGroupId("flink-telemetry-consumer-group")
            // Kafla key/val in bytes -> Need to get as String
            .setValueOnlyDeserializer(SimpleStringSchema())
            .build()

        // Watermark Strategy -> How to measure the progress of time and we skip it.
        // Due to possible delays of data come we handle this using timestamp value in data
        return env.fromSource(kafkaSource, WatermarkStrategy.noWatermarks(), "Telemetry Src - KaFka")
    }

    override fun doJob(env: StreamExecutionEnvironment, jobName: String) {
        logger.info("Execute flink job: '$jobName'")
        env.execute(jobName)
    }
}
