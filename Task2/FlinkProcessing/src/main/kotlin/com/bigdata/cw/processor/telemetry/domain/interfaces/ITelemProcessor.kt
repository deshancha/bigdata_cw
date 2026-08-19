// Author: Chamika Deshan
// Created: 2026-08-19

package com.bigdata.cw.processor.telemetry.domain.interfaces

import org.apache.flink.streaming.api.datastream.DataStream
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment

interface ITelemProcessor {
    fun getEnvironment(): StreamExecutionEnvironment
    fun readKafka(env: StreamExecutionEnvironment, topic: String): DataStream<String>
    fun doJob(env: StreamExecutionEnvironment, jobName: String)
}
