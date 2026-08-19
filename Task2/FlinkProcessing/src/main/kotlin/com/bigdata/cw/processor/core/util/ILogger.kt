// Author: Chamika Deshan
// Created: 2026-08-19

package com.bigdata.cw.processor.core.util

interface ILogger {
    fun info(message: String)
    fun warn(message: String)
    fun error(message: String)
}
