plugins {
    kotlin("jvm") version "1.9.22"
    id("com.gradleup.shadow") version "8.3.5"
}

group = "com.bigdata.cw"
version = "1.0"

repositories {
    mavenCentral()
}

val flinkVersion = "1.18.1"

kotlin {
    jvmToolchain(11)
}

dependencies {
    compileOnly("org.apache.flink:flink-core:$flinkVersion")
    compileOnly("org.apache.flink:flink-streaming-java:$flinkVersion")
    compileOnly("org.apache.flink:flink-clients:$flinkVersion")
    implementation("org.apache.flink:flink-connector-kafka:3.0.1-1.18")
    implementation("com.google.code.gson:gson:2.10.1")
    implementation("io.github.cdimascio:dotenv-java:3.0.0")
}

tasks.shadowJar {
    archiveClassifier.set("")
    // need by flink -> Service providr interfaces resolving
    mergeServiceFiles()
}
