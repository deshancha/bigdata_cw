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
    implementation("com.influxdb:influxdb-client-java:6.12.0")
}

tasks.shadowJar {
    archiveClassifier.set("")
    // need by flink -> Service providr interfaces resolving
    mergeServiceFiles()
}

// Helper to Deploy to Docker (Lib + .env)
tasks.register<Exec>("deployToDocker") {
    dependsOn("shadowJar")
    group = "deployment"
    description = "Copy jar and .env to Flink JobManager"

    commandLine("docker", "cp", "${tasks.shadowJar.get().archiveFile.get().asFile.absolutePath}", "task2-jobmanager:/opt/flink/")

    doLast {
        // .env copy
        ProcessBuilder("docker", "cp", "${projectDir}/../.env", "task2-jobmanager:/opt/flink/")
            .inheritIO()
            .start()
            .waitFor()

        // Flink job submit
        val jarName = tasks.shadowJar.get().archiveFile.get().asFile.name
        ProcessBuilder(
            "docker", "exec", "task2-jobmanager", 
            "flink", "run", "-d", "-c", "com.bigdata.cw.processor.TelemetryProcessorApp", 
            "/opt/flink/$jarName"
        )
        .inheritIO()
        .start()
        .waitFor()
    }
}
