// Author: Chamika Deshan
// Created: 2026-08-19

package com.bigdata.cw.processor.telemetry.data.model

import java.io.Serializable

data class TelemetryRecord(
    val camId: String,
    val timeStamp: Long,
    val vehCount: Int
) : Serializable
