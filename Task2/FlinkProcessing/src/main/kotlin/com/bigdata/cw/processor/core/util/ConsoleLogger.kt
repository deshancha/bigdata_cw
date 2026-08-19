// Author: Chamika Deshan
// Created: 2026-08-19

package com.bigdata.cw.processor.core.util

import java.io.Serializable

class ConsoleLogger(private val name: String) : ILogger, Serializable {
    override fun info(message: String) {
        println("INFO  | [$name] $message")
    }

    override fun warn(message: String) {
        println("WARN  | [$name] $message")
    }

    override fun error(message: String) {
        println("ERROR | [$name] $message")
    }
}
