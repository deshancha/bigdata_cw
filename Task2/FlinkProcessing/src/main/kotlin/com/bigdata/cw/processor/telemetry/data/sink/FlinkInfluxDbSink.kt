// Author: Chamika Deshan
// Created: 2026-08-20

package com.bigdata.cw.processor.telemetry.data.sink

import com.influxdb.client.InfluxDBClient
import com.influxdb.client.InfluxDBClientFactory
import com.influxdb.client.domain.WritePrecision
import com.influxdb.client.write.Point
import com.google.gson.Gson
import com.google.gson.JsonObject
import org.apache.flink.configuration.Configuration
import org.apache.flink.streaming.api.functions.sink.RichSinkFunction
import org.apache.flink.streaming.api.functions.sink.SinkFunction
import io.github.cdimascio.dotenv.Dotenv
import java.time.Instant

class FlinkInfluxDbSink : RichSinkFunction<String>() {
    private var client: InfluxDBClient? = null

    override fun open(parameters: Configuration) {
        val dotenv = Dotenv.configure().ignoreIfMissing().load()
        val url = dotenv.get("INFLUXDB_URL", "http://influxdb-label:8086")
        val token = dotenv.get("INFLUXDB_TOKEN", "my-super-secret-admin-token")
        val org = dotenv.get("INFLUXDB_ORG", "bigdata_cw")
        val bucket = dotenv.get("INFLUXDB_BUCKET", "traffic_data")

        client = InfluxDBClientFactory.create(url, token.toCharArray(), org, bucket)
    }

    override fun invoke(value: String, context: SinkFunction.Context) {
        val taskLogger = org.slf4j.LoggerFactory.getLogger("InfluxDbSink")
        try {
            val json = Gson().fromJson(value, JsonObject::class.java)
            val camId = json.get("cam_id")?.asString ?: "unknown"
            val count = json.get("vehicle_count")?.asInt ?: 0

            val point = Point.measurement("camera_traffic")
                .addTag("cam_id", camId)
                .addField("vehicle_count", count)
                .time(Instant.now(), WritePrecision.MS)

            client?.writeApiBlocking?.writePoint(point)
        } catch (e: Exception) {
            taskLogger.error("Fail to Write InfluxDB: ${e.message}", e)
        }
    }

    override fun close() {
        client?.close()
    }
}
